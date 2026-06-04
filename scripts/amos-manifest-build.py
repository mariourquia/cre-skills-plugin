#!/usr/bin/env python3
"""
amos-manifest-build.py — Emit dist/amos-skill-manifest.json.

A STATIC generated export (NOT committed; dist/ is gitignored) that AMOS
consumes as a governed skill layer without hardcoding any skill. It is a
SUPERSET of dist/catalog.json: every catalog item, plus two code-computed
crosswalks that collapse the plugin's governance vocabulary onto AMOS's:

  1. runtime_role -> AMOS demoStatus   (RUNTIME_ROLE_TO_DEMO_STATUS, 7 -> 3)
  2. human_gate   -> AMOS amos_signoff (HUMAN_GATE_TO_SIGNOFF,      6 -> 4)

Both are total over the plugin enums. Debt/hedging-exposed decision-grade
skills escalate to am-cfo-signoff + external-attestation per AMOS ADR-0004
(see DEBT_HEDGING_SLUGS + escalation logic in skill_signoff()).

HONEST FRAMING (AMOS ADR-0006): this is a documented contract + static export.
NO skill is marked live-connected; AMOS references skills, it does not invoke
them live. The manifest never claims a live connector.

Sources of truth:
  - dist/catalog.json                       (the enriched catalog — run catalog-build.py)
  - .claude-plugin/plugin.json              (plugin_version)
  - docs/integrations/amos-skill-manifest.schema.json (the manifest schema)
  - amos-prototype room-tabs.ts             (amos_surface enum; READ-ONLY upstream)

generated_at determinism: NEVER wall-clock by default. Resolution order is
  --as-of arg  >  $AMOS_MANIFEST_AS_OF env  >  the catalog's own generated_at.
The catalog timestamp is itself a build input, so a manifest built from a fixed
catalog is byte-stable. Pass --now only to deliberately stamp wall-clock.

Usage:
    python3 scripts/amos-manifest-build.py                 # -> dist/amos-skill-manifest.json
    python3 scripts/amos-manifest-build.py --as-of 2026-06-03T00:00:00Z
    python3 scripts/amos-manifest-build.py --stdout        # print, do not write
    python3 scripts/amos-manifest-build.py --check         # fail if dist/ manifest is stale
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_JSON = REPO_ROOT / "dist" / "catalog.json"
PLUGIN_JSON = REPO_ROOT / ".claude-plugin" / "plugin.json"
OUT_PATH = REPO_ROOT / "dist" / "amos-skill-manifest.json"

MANIFEST_VERSION = "1.0"
REPO_SLUG = "mariourquia/cre-skills-plugin"

# Root-level allowed sourceRef namespaces. A skill's source_ref_policy.emits
# entries (data-room/*, model/*, market/*) must namespace-match these roots
# (M-D2: a declared model/* / data-room/* namespace must be in ref_namespaces).
REF_NAMESPACES = ["data-room/*", "model/*"]


# ---------------------------------------------------------------------------
# CROSSWALK 1 — runtime_role (7 plugin roles) -> AMOS DemoStatus (3 values).
# AMOS DemoStatus = preprocessed-fixture | deterministic-calc | future-live-connector
# (amos-prototype data/icomm/prose-frontier/types.ts). 09-amos-integration.md §4:
# deterministic-calc -> deterministic-calc; prompt-guided/orchestrator ->
# preprocessed-fixture; future-live-connector -> future-live-connector.
# TOTAL over the plugin runtime_role enum (M-AM3).
# ---------------------------------------------------------------------------
RUNTIME_ROLE_TO_DEMO_STATUS = {
    "deterministic_calculator": "deterministic-calc",     # live stdlib arithmetic on source facts
    "callable_tool": "preprocessed-fixture",              # prompt-guided; output prepared & reviewed
    "workflow_conductor": "preprocessed-fixture",         # orchestrators run prepared in the demo
    "workspace_router": "preprocessed-fixture",           # business-surface router; prepared output
    "agent_persona": "preprocessed-fixture",              # role/persona worker; prepared output
    "human_review_surface": "preprocessed-fixture",       # human-in-the-loop surface; prepared
    "reference_only": "future-live-connector",            # documentation/reference; live connector is the target
}

# ---------------------------------------------------------------------------
# CROSSWALK 2 — human_gate (6 plugin gates) -> AMOS amos_signoff (4 values).
# AMOS sign-off ladder (09-amos-integration.md §3, ADR-0004 Addendum §1/§3):
# analyst-review | am-signoff | am-cfo-signoff | external-attestation.
# The plugin gate is CRE-business-semantic and stays in the plugin (M-AM2);
# the generator emits this projection for AMOS. TOTAL over the plugin enum.
# ---------------------------------------------------------------------------
HUMAN_GATE_TO_SIGNOFF = {
    "none": "analyst-review",                                    # AMOS floor is analyst-review (no "ungated" tier)
    "review_recommended": "analyst-review",
    "approval_required": "am-signoff",
    "lender_or_investor_review_required": "am-cfo-signoff",
    "investment_committee_approval_required": "am-cfo-signoff",
    "legal_tax_regulatory_review_required": "external-attestation",
}

# Debt/hedging-exposed slugs. Per AMOS ADR-0004 a decision-grade skill that
# certifies or restructures debt/coverage carries the highest sign-off:
# am-cfo-signoff + external-attestation (the escalated chain). Membership +
# decision_grade triggers the escalation in skill_signoff().
DEBT_HEDGING_SLUGS = {
    "amos-icomm-demo-orchestrator",   # its debt stage sizes/structures agency debt
    "loan-sizing-engine",
    "capital-stack-optimizer",
    "mezz-pref-structurer",
    "debt-covenant-monitor",
    "debt-portfolio-monitor",
    "refi-decision-analyzer",
    "agency-loan-quote-analyzer",
}

ESCALATED_DEBT_SIGNOFF_CHAIN = ["am-cfo-signoff", "external-attestation"]

# The full set of AMOS sign-off values, ordered low -> high. Used to build the
# escalation chain (every gate at or below the primary, up to the primary).
SIGNOFF_LADDER = ["analyst-review", "am-signoff", "am-cfo-signoff", "external-attestation"]

# AMOS DemoStatus value set — load-bearing for the totality self-check.
AMOS_DEMO_STATUS = {"preprocessed-fixture", "deterministic-calc", "future-live-connector"}


# ---------------------------------------------------------------------------
# Crosswalk application
# ---------------------------------------------------------------------------
def demo_status_for(runtime_role: str | None) -> str:
    """runtime_role -> AMOS demoStatus. Unknown/None falls back to the most
    conservative honest label (preprocessed-fixture: prepared, not live)."""
    return RUNTIME_ROLE_TO_DEMO_STATUS.get(runtime_role or "", "preprocessed-fixture")


def skill_signoff(slug: str, human_gate: str | None, decision_grade: bool) -> dict:
    """human_gate -> AMOS sign-off, with the ADR-0004 debt/hedging escalation.

    Returns { amos_signoff, amos_signoff_chain }:
      - amos_signoff       the single primary AMOS gate (highest required).
      - amos_signoff_chain the ordered ladder up to the primary (so AMOS can
                           render the full sequence). Debt/hedging decision-grade
                           skills carry am-cfo-signoff + external-attestation.
    """
    base = HUMAN_GATE_TO_SIGNOFF.get(human_gate or "none", "analyst-review")

    if decision_grade and slug in DEBT_HEDGING_SLUGS:
        chain = list(ESCALATED_DEBT_SIGNOFF_CHAIN)
        primary = chain[-1]  # external-attestation
    else:
        primary = base
        idx = SIGNOFF_LADDER.index(base)
        chain = SIGNOFF_LADDER[: idx + 1]

    return {"amos_signoff": primary, "amos_signoff_chain": chain}


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------
def load_catalog() -> dict:
    if not CATALOG_JSON.exists():
        print(
            "ERROR: dist/catalog.json missing. Run: python3 scripts/catalog-build.py",
            file=sys.stderr,
        )
        sys.exit(1)
    return json.loads(CATALOG_JSON.read_text(encoding="utf-8"))


def plugin_version() -> str:
    if PLUGIN_JSON.exists():
        return json.loads(PLUGIN_JSON.read_text(encoding="utf-8")).get("version", "0.0.0")
    return "0.0.0"


def resolve_generated_at(catalog: dict, as_of: str | None, use_now: bool) -> str:
    """Determinism-preserving generated_at (see module docstring):
      --as-of  >  $AMOS_MANIFEST_AS_OF  >  catalog['generated_at']  ( >  now() only with --now )."""
    if use_now:
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()
    if as_of:
        return as_of
    env = os.environ.get("AMOS_MANIFEST_AS_OF")
    if env:
        return env
    return catalog.get("generated_at", "")


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------
def build_skill_entry(item: dict) -> dict:
    """One SkillManifestEntry: the catalog item's AMOS-relevant fields, the
    governance metadata verbatim, and the two computed crosswalks."""
    runtime_role = item.get("runtime_role")
    human_gate = item.get("human_gate", "none")
    decision_grade = bool(item.get("decision_grade", False))

    signoff = skill_signoff(item["id"], human_gate, decision_grade)

    return {
        # --- identity / linking (from catalog) ---
        "id": item["id"],
        "display_name": item.get("display_name", item["id"]),
        "type": item.get("type"),
        "status": item.get("status"),
        "source_path": item.get("source_path"),
        "version": item.get("version"),
        # --- plugin classification + governance (verbatim from catalog) ---
        "classification": item.get("classification"),
        "runtime_role": runtime_role,
        "decision_grade": decision_grade,
        "human_gate": human_gate,
        "source_ref_policy": item.get("source_ref_policy"),
        "amos_surface": item.get("amos_surface", []),
        "decomposes_to": item.get("decomposes_to", []),
        "composed_from": item.get("composed_from", []),
        # --- catalog IO + chaining (drive AMOS source map + timeline) ---
        "input_artifacts": item.get("input_artifacts", []),
        "outputs": item.get("outputs", []),
        "chains_to": item.get("downstream_items", []),
        "chains_from": item.get("upstream_items", []),
        "calculator_file": item.get("calculator_file"),
        # --- COMPUTED CROSSWALKS (code, not prose) ---
        "demo_status": demo_status_for(runtime_role),
        "amos_signoff": signoff["amos_signoff"],
        "amos_signoff_chain": signoff["amos_signoff_chain"],
        # --- honest framing (ADR-0006): never live-connected ---
        "live_connector": False,
    }


def build_manifest(as_of: str | None = None, use_now: bool = False) -> dict:
    catalog = load_catalog()
    generated_at = resolve_generated_at(catalog, as_of, use_now)
    skills = [build_skill_entry(it) for it in catalog.get("items", [])]
    return {
        "manifest_version": MANIFEST_VERSION,
        "plugin_version": plugin_version(),
        "generated_at": generated_at,
        "repo": REPO_SLUG,
        "ref_namespaces": REF_NAMESPACES,
        # The crosswalk tables are emitted as data so AMOS (and the test) can read
        # the projection without re-deriving it from prose.
        "crosswalks": {
            "runtime_role_to_demo_status": RUNTIME_ROLE_TO_DEMO_STATUS,
            "human_gate_to_signoff": HUMAN_GATE_TO_SIGNOFF,
            "debt_hedging_signoff_chain": ESCALATED_DEBT_SIGNOFF_CHAIN,
        },
        "skills": skills,
    }


def _serialize(manifest: dict) -> str:
    return json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build dist/amos-skill-manifest.json")
    parser.add_argument("--as-of", help="ISO-8601 generated_at override (determinism)")
    parser.add_argument("--now", action="store_true", help="Stamp wall-clock generated_at (non-deterministic)")
    parser.add_argument("--stdout", action="store_true", help="Print to stdout, do not write")
    parser.add_argument("--check", action="store_true", help="Fail if dist manifest differs from a fresh build")
    args = parser.parse_args()

    manifest = build_manifest(as_of=args.as_of, use_now=args.now)
    payload = _serialize(manifest)

    if args.check:
        if not OUT_PATH.exists():
            print("FAIL: dist/amos-skill-manifest.json missing. Run: python3 scripts/amos-manifest-build.py")
            sys.exit(1)
        existing = OUT_PATH.read_text(encoding="utf-8")
        if existing != payload:
            print("FAIL: dist/amos-skill-manifest.json is stale. Run: python3 scripts/amos-manifest-build.py")
            sys.exit(1)
        print(f"OK: manifest up to date ({len(manifest['skills'])} skills)")
        return

    if args.stdout:
        sys.stdout.write(payload)
        return

    OUT_PATH.parent.mkdir(exist_ok=True)
    OUT_PATH.write_text(payload, encoding="utf-8")
    print(f"Wrote {OUT_PATH} ({len(manifest['skills'])} skills)")
    print(f"  manifest_version: {manifest['manifest_version']}")
    print(f"  plugin_version:   {manifest['plugin_version']}")
    print(f"  generated_at:     {manifest['generated_at']}")
    print(f"  ref_namespaces:   {manifest['ref_namespaces']}")
    dg = sum(1 for s in manifest["skills"] if s["decision_grade"])
    af = sum(1 for s in manifest["skills"] if s["amos_surface"])
    print(f"  decision_grade:   {dg}")
    print(f"  amos-facing:      {af}")


if __name__ == "__main__":
    main()
