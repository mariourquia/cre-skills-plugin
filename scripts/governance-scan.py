#!/usr/bin/env python3
"""Corpus-wide STATIC + GENERATED-ARTIFACT governance scanner (v5.2.0).

Scope and honesty (read this before trusting it):
  This scanner validates governance DECLARATIONS over (a) SKILL.md frontmatter
  read from the filesystem (so a stale catalog cannot mask a removed disclaimer)
  and (b) the generated catalog (dist/catalog.json) for derived/projected fields.
  It proves a skill *declares* the right posture; it does NOT inspect emitted
  output. Runtime emitted-output enforcement (source-class tagging + placeholder
  refusal on every cell at emit time) is deployed ONLY inside the
  residential_multifamily subsystem and remains a tracked backlog item (see
  docs/ROADMAP.md "Generalized cross-skill governance scanner"). Nothing here
  should be read as universal runtime enforcement.

Four layers, kept distinct:
  1. static frontmatter validation        (this scanner)
  2. generated catalog/manifest validation (this scanner + test_amos_manifest)
  3. RMF runtime emitted-output enforcement (residential_multifamily only)
  4. generalized runtime scanner           (backlog, NOT shipped)

Rules carry a severity:
  ERROR  -> fail closed, exit 1 (liability + structural integrity)
  WARN   -> reported, exit 0    (completeness / backfill candidates)

The scanner core is a pure function (`scan`) so tests can drive it with in-memory
fixtures; the CLI builds the document accessor from the filesystem. Liability
rules (not-an-appraisal, statute/tax disclaimer) trigger on EXPLICIT governance
fields, never description keyword-sniffing, so generalizing them cannot conscript
advisory skills into stub inflation.

Usage:
  python3 scripts/catalog-build.py        # build dist/catalog.json first
  python3 scripts/governance-scan.py            # report (exit 1 on any ERROR)
  python3 scripts/governance-scan.py --warnings # also fail on WARN
  python3 scripts/governance-scan.py --json     # machine-readable
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_JSON = REPO_ROOT / "dist" / "catalog.json"
SKILLS_ROOT = REPO_ROOT / "src" / "skills"

ERROR = "ERROR"
WARN = "WARN"

# Severity-floor allowlists. Generalization may never LOSE a curated slug, so
# these are asserted as a subset of the rule's triggers (Governance M5).
NOT_AN_APPRAISAL_FLOOR = {
    "comp-snapshot", "om-reverse-pricing", "acquisition-underwriting-engine",
}
# produces_artifact_kind values that are valuation conclusions and therefore must
# carry the "not an appraisal" stamp (explicit-field trigger, not keyword).
VALUATION_ARTIFACT_KINDS = {"valuation_support"}
# Acceptable "not legal/tax advice" disclaimer phrasings (any one satisfies).
TAX_LEGAL_DISCLAIMERS = (
    "not legal", "not tax advice", "not tax or legal", "qualified counsel",
    "qualified tax", "tax professional", "tax advis", "qualified professional",
    "consult counsel", "consult a qualified", "consult your tax", "consult a tax",
    "licensed professional", "not a substitute for",
)
SOURCE_REF_OK_ON_UNRESOLVABLE = {"refuse", "cite_best_effort"}
PII_ENUM = {"none", "business_contact", "tenant_or_personal", "sensitive_financial"}
REMOVED_POSTURE_VALUES = {"aggregate_only", "pseudonymized", "redacted_at_extraction"}
SENSITIVE_SCOPES = {"leasing", "investor_relations", "fund"}
STATUTE_HORIZON_DAYS = 730


def _split_frontmatter(text: str) -> Tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    try:
        end = text.index("\n---\n", 4)
    except ValueError:
        return "", text
    return text[4:end], text[end + 5:]


def _load_doc_from_fs(skill_id: str) -> Tuple[Optional[dict], str]:
    """Return (frontmatter_dict, body) for a skill id, or (None, '')."""
    p = SKILLS_ROOT / skill_id / "SKILL.md"
    if not p.exists():
        return None, ""
    try:
        import yaml
    except ImportError:  # pragma: no cover
        yaml = None
    text = p.read_text(encoding="utf-8")
    front_raw, body = _split_frontmatter(text)
    front: dict = {}
    if yaml is not None and front_raw:
        loaded = yaml.safe_load(front_raw)
        if isinstance(loaded, dict):
            front = loaded
    return front, body


def _statute_stale(front: dict, today: _dt.date) -> List[str]:
    """Return human messages for any stale/malformed statute_review entries."""
    sr = front.get("statute_review")
    if not sr or not isinstance(sr, list):
        return []
    msgs = []
    for entry in sr:
        if not isinstance(entry, dict) or "last_verified" not in entry:
            continue
        try:
            d = _dt.date.fromisoformat(str(entry["last_verified"]))
        except ValueError:
            msgs.append(f"statute_review entry '{entry.get('code','?')}' last_verified not ISO")
            continue
        age = (today - d).days
        if age > STATUTE_HORIZON_DAYS:
            msgs.append(
                f"statute_review '{entry.get('code','?')}' is {age}d old (>{STATUTE_HORIZON_DAYS}); re-verify"
            )
    return msgs


def scan(
    items: List[dict],
    get_doc: Callable[[str], Tuple[Optional[dict], str]],
    today: Optional[_dt.date] = None,
) -> List[Tuple[str, str, str, str]]:
    """Pure scanner. Returns list of (severity, item_id, rule, message).

    `items` are catalog items (carry the derived/projected governance fields).
    `get_doc(skill_id)` -> (frontmatter_dict|None, body_str) for body/frontmatter
    checks that the catalog does not project (refusal_trigger, statute_review,
    disclaimers).
    """
    today = today or _dt.date.today()
    v: List[Tuple[str, str, str, str]] = []
    catalog_ids = {i["id"] for i in items}

    def add(sev, iid, rule, msg):
        v.append((sev, iid, rule, msg))

    for it in items:
        iid = it["id"]
        itype = it.get("type")
        is_skill = itype == "skill"
        dg = bool(it.get("decision_grade"))
        gate = it.get("human_gate", "none")
        srp = it.get("source_ref_policy")
        pak = it.get("produces_artifact_kind")
        pii = it.get("pii_policy", "none")
        ws = it.get("workspace_scope")
        outputs = it.get("outputs") or []
        calc_file = it.get("calculator_file")

        front, body = get_doc(iid) if is_skill else (None, "")
        front = front or {}
        body_l = (body or "").lower()

        # --- ERROR: decision-grade must be gated + source-grounded -------------
        if dg:
            if gate in (None, "none", ""):
                add(ERROR, iid, "decision_grade_requires_gate",
                    "decision_grade skill must declare a human_gate != none")
            if not srp:
                add(ERROR, iid, "decision_grade_requires_source_ref_policy",
                    "decision_grade skill must declare source_ref_policy")
            if is_skill and not (front.get("refusal_trigger") or "").strip():
                add(ERROR, iid, "decision_grade_requires_refusal_trigger",
                    "decision_grade skill must declare a refusal_trigger in frontmatter")

        # --- ERROR: source_ref_policy shape + refusal posture ------------------
        if srp:
            if not isinstance(srp, dict) or not all(
                k in srp for k in ("emits", "on_unresolvable", "forbids_fabricated_model_ref")
            ):
                add(ERROR, iid, "source_ref_policy_shape",
                    "source_ref_policy must carry emits/on_unresolvable/forbids_fabricated_model_ref")
            else:
                onu = srp.get("on_unresolvable")
                if onu not in SOURCE_REF_OK_ON_UNRESOLVABLE:
                    add(ERROR, iid, "source_ref_refusal_posture",
                        f"source_ref_policy.on_unresolvable '{onu}' must be one of "
                        f"{sorted(SOURCE_REF_OK_ON_UNRESOLVABLE)} (fail-closed posture)")

        # --- ERROR: decomposition references resolve ---------------------------
        for field in ("decomposes_to", "composed_from"):
            for ref in (it.get(field) or []):
                if ref not in catalog_ids:
                    add(ERROR, iid, "dangling_decomposition",
                        f"{field} id '{ref}' does not resolve to a catalog item")

        # --- ERROR: pii_policy enum + no removed posture value -----------------
        if pii in REMOVED_POSTURE_VALUES:
            add(ERROR, iid, "pii_policy_removed_value",
                f"pii_policy '{pii}' is a removed v5.1 posture value; use the v5.2 sensitivity enum")
        elif pii not in PII_ENUM:
            add(ERROR, iid, "pii_policy_enum",
                f"pii_policy '{pii}' not in {sorted(PII_ENUM)}")

        # --- ERROR: valuation conclusion must carry "not an appraisal" --------
        valuation = (pak in VALUATION_ARTIFACT_KINDS) or (iid in NOT_AN_APPRAISAL_FLOOR)
        if valuation and is_skill and "not an appraisal" not in body_l:
            add(ERROR, iid, "valuation_requires_not_an_appraisal",
                "valuation/comp output must carry a 'not an appraisal' stamp in the body")

        # --- ERROR: statute-encoding skills (legal/tax) ------------------------
        if is_skill and front.get("statute_review"):
            for msg in _statute_stale(front, today):
                add(ERROR, iid, "statute_review_stale", msg)
            if not any(d in body_l for d in TAX_LEGAL_DISCLAIMERS):
                add(ERROR, iid, "statute_requires_disclaimer",
                    "skill encoding a tax/legal/regulatory regime (statute_review set) "
                    "must carry a 'not legal/tax advice / qualified counsel' disclaimer")

        # --- ERROR: calculator-typed must resolve + be calculator_result ------
        is_calc = (itype == "calculator") or bool(calc_file)
        if is_calc:
            if pak != "calculator_result":
                add(ERROR, iid, "calculator_artifact_kind",
                    f"calculator-typed item must have produces_artifact_kind='calculator_result', got {pak!r}")
            if calc_file and not (REPO_ROOT / calc_file).exists():
                add(ERROR, iid, "calculator_file_unresolved",
                    f"calculator_file '{calc_file}' does not exist on disk")

        # --- WARN: completeness / backfill candidates --------------------------
        if (dg or it.get("amos_surface")) and not outputs:
            add(WARN, iid, "consumer_facing_outputs",
                "consumer-facing (decision_grade or amos_surface) skill declares no outputs[]")
        if pak and not outputs:
            add(WARN, iid, "artifact_without_outputs",
                f"declares produces_artifact_kind={pak} but no outputs[]")
        if is_skill and ws in SENSITIVE_SCOPES and pii == "none":
            add(WARN, iid, "pii_backfill_candidate",
                f"workspace_scope={ws} but pii_policy=none (candidate for a sensitivity tier)")

    return v


def run(check_warnings: bool = False) -> Tuple[List[Tuple[str, str, str, str]], int]:
    if not CATALOG_JSON.exists():
        print("ERROR: dist/catalog.json missing; run scripts/catalog-build.py first", file=sys.stderr)
        return [], 2
    items = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))["items"]
    violations = scan(items, _load_doc_from_fs)
    errors = [x for x in violations if x[0] == ERROR]
    warns = [x for x in violations if x[0] == WARN]
    code = 1 if (errors or (check_warnings and warns)) else 0
    return violations, code


def main() -> int:
    ap = argparse.ArgumentParser(description="Corpus-wide static governance scanner")
    ap.add_argument("--warnings", action="store_true", help="fail (exit 1) on WARN too")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    violations, code = run(check_warnings=args.warnings)
    if args.json:
        print(json.dumps([
            {"severity": s, "id": i, "rule": r, "message": m} for s, i, r, m in violations
        ], indent=2))
        return code

    errors = [x for x in violations if x[0] == ERROR]
    warns = [x for x in violations if x[0] == WARN]
    for sev, iid, rule, msg in errors + warns:
        print(f"  {sev:5s} {iid:40s} [{rule}] {msg}")
    print(f"\ngovernance-scan: {len(errors)} error(s), {len(warns)} warning(s)")
    if code == 0 and not errors:
        print("RESULT: PASS" + (" (warnings present)" if warns else ""))
    elif code != 0:
        print("RESULT: FAIL")
    return code


if __name__ == "__main__":
    sys.exit(main())
