"""AMOS skill-manifest export contract (v5).

Validates the generated dist/amos-skill-manifest.json against its JSON Schema and
enforces the manifest invariants the spec calls for
(docs/architecture/v5-micro-skill-architecture.md §3, §6, §10 M-AM1..M-AM4):

  - the manifest validates against docs/integrations/amos-skill-manifest.schema.json;
  - every amos_surface value is an AMOS RoomTabKey + landing;
  - the runtime_role -> demoStatus crosswalk is TOTAL over the plugin runtime_role
    enum (read from the catalog schema, the source of truth — so a new role
    without a mapping fails here);
  - the human_gate -> amos_signoff crosswalk is TOTAL over the plugin human_gate
    enum, and every decision_grade skill has human_gate != none + a non-null,
    valid amos_signoff;
  - NO entry claims a live connector (ADR-0006);
  - the committed sample is schema-valid and a TRUE SUBSET of the full manifest.

The manifest is built in-process from dist/catalog.json (run scripts/catalog-build.py
first), so a stale dist artifact cannot mask a regression.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Dict, List

import jsonschema

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "docs" / "integrations" / "amos-skill-manifest.schema.json"
SAMPLE_PATH = REPO_ROOT / "docs" / "integrations" / "amos-skill-manifest.sample.json"
CATALOG_SCHEMA_PATH = REPO_ROOT / "src" / "catalog" / "catalog.schema.json"
BUILDER_PATH = REPO_ROOT / "scripts" / "amos-manifest-build.py"

# AMOS target vocabularies (amos-prototype types.ts / room-tabs.ts), pinned here
# so a drift in the plugin's emitted values is caught against the real AMOS enums.
AMOS_DEMO_STATUS = {"preprocessed-fixture", "deterministic-calc", "future-live-connector"}
AMOS_SIGNOFF = {"analyst-review", "am-signoff", "am-cfo-signoff", "external-attestation"}
AMOS_ROOM_TAB_KEYS_PLUS = {
    "model", "leasing", "t12", "debt", "market", "diligence",
    "sources", "memo", "feedback", "decision", "landing",
}


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------
def _load_builder():
    """Import the hyphenated scripts/amos-manifest-build.py by path."""
    spec = importlib.util.spec_from_file_location("amos_manifest_build", BUILDER_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_BUILDER = _load_builder()


def _build_manifest() -> Dict:
    # Fixed --as-of so the build is deterministic regardless of when the test runs.
    return _BUILDER.build_manifest(as_of="2026-06-03T00:00:00Z")


def _schema() -> Dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _plugin_runtime_role_enum() -> List[str]:
    """Plugin runtime_role enum from the catalog schema (source of truth),
    excluding the null sentinel."""
    schema = json.loads(CATALOG_SCHEMA_PATH.read_text(encoding="utf-8"))
    enum = schema["$defs"]["CatalogItem"]["properties"]["runtime_role"]["enum"]
    return [v for v in enum if v is not None]


def _plugin_human_gate_enum() -> List[str]:
    schema = json.loads(CATALOG_SCHEMA_PATH.read_text(encoding="utf-8"))
    return list(schema["$defs"]["CatalogItem"]["properties"]["human_gate"]["enum"])


# ---------------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------------
def test_generated_manifest_validates_against_schema():
    """Build the manifest and jsonschema.validate the whole document."""
    manifest = _build_manifest()
    jsonschema.validate(manifest, _schema())
    assert manifest["skills"], "manifest has no skills — catalog likely empty"


def test_manifest_root_shape():
    """Root carries the spec-required fields with the right contents."""
    m = _build_manifest()
    assert m["manifest_version"] == "1.0"
    # plugin_version comes from plugin.json, never hardcoded in the manifest builder.
    pj = json.loads((REPO_ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert m["plugin_version"] == pj["version"]
    assert m["repo"] == "mariourquia/cre-skills-plugin"
    assert m["ref_namespaces"] == ["data-room/*", "model/*"]
    assert m["generated_at"] == "2026-06-03T00:00:00Z"  # honored the --as-of arg


# ---------------------------------------------------------------------------
# amos_surface ∈ AMOS RoomTabKey + landing
# ---------------------------------------------------------------------------
def test_every_amos_surface_value_is_a_room_tab_key():
    m = _build_manifest()
    failures: List[str] = []
    for s in m["skills"]:
        for surface in s.get("amos_surface", []):
            if surface not in AMOS_ROOM_TAB_KEYS_PLUS:
                failures.append(f"{s['id']}: invalid amos_surface '{surface}'")
    assert not failures, "amos_surface values outside the AMOS RoomTabKey+landing set:\n  " + "\n  ".join(failures)


# ---------------------------------------------------------------------------
# Crosswalk 1 — runtime_role -> demoStatus is TOTAL over the plugin enum
# ---------------------------------------------------------------------------
def test_runtime_role_to_demo_status_is_total_over_plugin_enum():
    plugin_roles = set(_plugin_runtime_role_enum())
    mapped = set(_BUILDER.RUNTIME_ROLE_TO_DEMO_STATUS.keys())
    missing = plugin_roles - mapped
    assert not missing, (
        "runtime_role -> demoStatus crosswalk is not total; unmapped plugin roles: "
        + ", ".join(sorted(missing))
    )
    # Every mapped value must be a real AMOS DemoStatus.
    bad = {v for v in _BUILDER.RUNTIME_ROLE_TO_DEMO_STATUS.values() if v not in AMOS_DEMO_STATUS}
    assert not bad, f"crosswalk emits non-AMOS demoStatus values: {sorted(bad)}"


def test_every_skill_demo_status_matches_the_crosswalk():
    """Each entry's demo_status equals the crosswalk applied to its runtime_role."""
    m = _build_manifest()
    failures: List[str] = []
    for s in m["skills"]:
        expected = _BUILDER.demo_status_for(s.get("runtime_role"))
        if s["demo_status"] != expected:
            failures.append(f"{s['id']}: demo_status={s['demo_status']} but crosswalk expects {expected}")
        if s["demo_status"] not in AMOS_DEMO_STATUS:
            failures.append(f"{s['id']}: demo_status '{s['demo_status']}' not an AMOS DemoStatus")
    assert not failures, "demo_status crosswalk mismatches:\n  " + "\n  ".join(failures)


# ---------------------------------------------------------------------------
# Crosswalk 2 — human_gate -> amos_signoff (+ decision-grade gate invariants)
# ---------------------------------------------------------------------------
def test_human_gate_to_signoff_is_total_over_plugin_enum():
    plugin_gates = set(_plugin_human_gate_enum())
    mapped = set(_BUILDER.HUMAN_GATE_TO_SIGNOFF.keys())
    missing = plugin_gates - mapped
    assert not missing, (
        "human_gate -> amos_signoff crosswalk is not total; unmapped gates: "
        + ", ".join(sorted(missing))
    )
    bad = {v for v in _BUILDER.HUMAN_GATE_TO_SIGNOFF.values() if v not in AMOS_SIGNOFF}
    assert not bad, f"crosswalk emits non-AMOS sign-off values: {sorted(bad)}"


def test_every_amos_signoff_value_is_valid():
    m = _build_manifest()
    failures: List[str] = []
    for s in m["skills"]:
        if s["amos_signoff"] not in AMOS_SIGNOFF:
            failures.append(f"{s['id']}: amos_signoff '{s['amos_signoff']}' not an AMOS sign-off")
        for step in s["amos_signoff_chain"]:
            if step not in AMOS_SIGNOFF:
                failures.append(f"{s['id']}: amos_signoff_chain step '{step}' not an AMOS sign-off")
    assert not failures, "invalid amos_signoff values:\n  " + "\n  ".join(failures)


def test_decision_grade_skills_are_gated_with_a_signoff():
    """Each decision_grade entry: human_gate != none AND a non-null amos_signoff."""
    m = _build_manifest()
    failures: List[str] = []
    dg = [s for s in m["skills"] if s["decision_grade"]]
    assert dg, "expected at least one decision_grade skill in the manifest"
    for s in dg:
        if s["human_gate"] == "none":
            failures.append(f"{s['id']}: decision_grade but human_gate == none")
        if not s.get("amos_signoff"):
            failures.append(f"{s['id']}: decision_grade but amos_signoff is null/empty")
        if s["amos_signoff"] not in AMOS_SIGNOFF:
            failures.append(f"{s['id']}: decision_grade amos_signoff '{s['amos_signoff']}' not an AMOS sign-off")
    assert not failures, "decision-grade gate/sign-off violations:\n  " + "\n  ".join(failures)


def test_debt_hedging_decision_grade_skills_require_external_attestation():
    """ADR-0004: a debt/hedging-exposed decision-grade skill escalates to
    am-cfo-signoff + external-attestation."""
    m = _build_manifest()
    failures: List[str] = []
    for s in m["skills"]:
        if s["decision_grade"] and s["id"] in _BUILDER.DEBT_HEDGING_SLUGS:
            if s["amos_signoff"] != "external-attestation":
                failures.append(f"{s['id']}: debt/hedging decision-grade must reach external-attestation, got {s['amos_signoff']}")
            if s["amos_signoff_chain"] != ["am-cfo-signoff", "external-attestation"]:
                failures.append(f"{s['id']}: debt/hedging chain must be [am-cfo-signoff, external-attestation], got {s['amos_signoff_chain']}")
    assert not failures, "debt/hedging sign-off escalation violations:\n  " + "\n  ".join(failures)


# ---------------------------------------------------------------------------
# Honest framing — no live connector (ADR-0006)
# ---------------------------------------------------------------------------
def test_no_entry_claims_a_live_connector():
    m = _build_manifest()
    offenders = [s["id"] for s in m["skills"] if s.get("live_connector") is not False]
    assert not offenders, (
        "ADR-0006 violation: the manifest must never mark a skill live-connected. "
        f"Offenders: {offenders}"
    )


# ---------------------------------------------------------------------------
# Committed sample — schema-valid + a true subset of the full manifest
# ---------------------------------------------------------------------------
def test_sample_validates_against_schema():
    sample = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    jsonschema.validate(sample, _schema())


def test_sample_is_a_true_subset_of_the_generated_manifest():
    """Every sample skill entry is byte-for-byte one of the full manifest's
    entries; the sample's root metadata matches too. (dist/ is gitignored, so the
    sample is the committed proof — it must not drift from the generator.)"""
    sample = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    full = _build_manifest()
    full_by_id = {s["id"]: s for s in full["skills"]}

    failures: List[str] = []
    for s in sample["skills"]:
        full_entry = full_by_id.get(s["id"])
        if full_entry is None:
            failures.append(f"{s['id']}: in sample but not in generated manifest")
        elif s != full_entry:
            failures.append(f"{s['id']}: sample entry differs from generated manifest entry")
    assert not failures, "sample is not a true subset of the manifest:\n  " + "\n  ".join(failures)

    # Root metadata (other than the explanatory _sample_note) matches the manifest.
    for key in ("manifest_version", "plugin_version", "generated_at", "repo", "ref_namespaces", "crosswalks"):
        assert sample[key] == full[key], f"sample root '{key}' differs from generated manifest"


def test_sample_covers_the_eight_priority_skills():
    """The committed sample includes all 8 v5 priority skills (§5) so reviewers
    see the real governance values for the reclassified set."""
    sample = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    present = {s["id"] for s in sample["skills"]}
    priority = {
        "amos-icomm-demo-orchestrator",
        "document-to-database",
        "document-to-warehouse-pipeline",
        "property-management-orchestrator",
        "residential_multifamily",
        "lease-negotiation-analyzer",
        "sourcing-outreach-system",
        "fund-lp-reporting",
    }
    missing = priority - present
    assert not missing, f"sample missing priority skills: {sorted(missing)}"
