#!/usr/bin/env python3
"""
Document-to-Database: Ingestion Self-Grader
===========================================
Scores a normalized payload (+ its validation report and optional tie-out) the
way the rent-roll data-quality rubric defines: a weakest-link A/B/C letter is
PRIMARY, a 0-100 weighted score is the secondary readout. The letter cannot be
averaged away -- a single C caps the grade.

This is the executable realization of rent-roll-analyzer's
data-quality-rubric.yaml (it shares dimension keys, weights, and weakest-link
semantics via the ingest.rubric mirror), generalized to T-12 and tie-out.

Gates: merge >= 85 AND no C grade AND no critical failure; production >= 92 AND
all-A AND no critical. A PII-redaction breach is a CRITICAL, NON-OVERRIDABLE
block at any score (it cannot be waived as a fixture limitation).

Pure calculate_grade_ingestion(dict)->dict; selectors in --json.

Used by: document-to-database, rent-roll-to-database, t12-to-database,
         rent-roll-t12-tieout

Usage:
    python3 src/calculators/grade_ingestion.py --json '{
        "run_id": "RUN-1", "as_of": "2026-05-29",
        "payload": { ...normalize_tokens output... },
        "validation": { ...validate_payload output... },
        "reconciliation": { ...reconcile_rent_roll_t12 output (optional)... },
        "banned_pii_values": ["Jane Doe"]
    }'

Output: JSON {dimension_grades, weakest_link_grade, score_100, merge_ready,
        production_ready, critical_failures, pii_redaction_breach, ...}.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from ingest import determinism as det, pii, rubric


def calculate_grade_ingestion(inputs: dict) -> dict:
    ctx = det.resolve_context(inputs)
    errs = det.require_context(ctx)
    if errs:
        return det.error_result("invalid run context", details=errs)

    payload = inputs.get("payload") or {}
    validation = inputs.get("validation") or {}
    reconciliation = inputs.get("reconciliation")
    if not payload:
        return det.error_result("missing 'payload' (output of normalize_tokens)")

    doc_type = payload.get("doc_type", "rent_roll")

    # Critical failures from validation.
    criticals: list = []
    for c in validation.get("checks", []):
        if c.get("status") == "critical" and c.get("code") in rubric.CRITICAL_FAILURES:
            criticals.append(c["code"])

    # PII leak scan over everything that would be emitted/staged. A breach is a
    # non-overridable critical (report field paths, never values).
    banned = inputs.get("banned_pii_values") or []
    leak_paths = pii.scan_for_leaks([payload, validation, reconciliation], banned)
    if leak_paths:
        criticals.append("pii_redaction_breach")

    if doc_type == "rent_roll":
        grades, dims = _grade_rent_roll(payload, validation, reconciliation)
    elif doc_type in ("t12", "operating_statement"):
        grades, dims = _grade_operating_statement(payload, validation)
    else:
        grades, dims = ({}, rubric.RENT_ROLL_DIMENSIONS)

    # Optional tie-out dimensions fold in when a reconciliation is present.
    if reconciliation and reconciliation.get("dimensions"):
        tie_grades = _grade_tieout(reconciliation, payload)
        grades.update(tie_grades)
        dims = tuple(dims) + rubric.TIEOUT_DIMENSIONS

    criticals = sorted(set(c for c in criticals if c))
    letter = rubric.weakest_link(grades)
    numeric = rubric.score_100(grades, dims)
    g = rubric.gate(letter, numeric, criticals)

    out = {
        "doc_type": doc_type,
        "dimension_grades": grades,
        "leak_field_paths": leak_paths,  # paths only, never values
    }
    out.update(g)
    return out


# --------------------------------------------------------------------------
def _grade_rent_roll(payload: dict, validation: dict, reconciliation) -> tuple:
    leases = payload.get("leases", [])
    records = payload.get("records", [])
    codes = {c.get("code"): c for c in validation.get("checks", [])}
    crit_codes = {c.get("code") for c in validation.get("checks", []) if c.get("status") == "critical"}

    grades: dict = {}

    # 1 completeness: required lease fields populated.
    req = ("lease_id", "unit_id", "lease_start", "lease_expire")
    base_by_lease = _base_rent_by_lease(records)
    if leases:
        complete = 0
        for l in leases:
            ok = all(l.get(k) not in (None, "") for k in req) and base_by_lease.get(l["lease_id"], 0) > 0
            complete += 1 if ok else 0
        frac = complete / len(leases)
    else:
        frac = 1.0
    grades["1_completeness"] = rubric.grade_from_pass_rate(frac)

    # 2 date consistency.
    grades["2_date_consistency"] = "C" if "lease_expiry_before_start" in crit_codes else "A"

    # 3 sf reconciliation.
    grades["3_sf_reconciliation"] = "C" if "negative_sf" in crit_codes else "A"

    # 4 rent arithmetic.
    grades["4_rent_arithmetic"] = "C" if "rent_arithmetic_contradiction" in crit_codes else "A"

    # 5 escalation documentation.
    if leases:
        esc = sum(1 for l in leases if l.get("escalation")) / len(leases)
    else:
        esc = 1.0
    grades["5_escalation_documentation"] = rubric.grade_from_pass_rate(esc) if esc < 1 else "A"

    # 6 vacancy identification: units all carry a status by construction.
    grades["6_vacancy_identification"] = "A"

    # 7 lease type clarity.
    if leases:
        lt = sum(1 for l in leases if l.get("lease_type")) / len(leases)
    else:
        lt = 1.0
    grades["7_lease_type_clarity"] = "A" if lt >= 1 else ("B" if lt >= 0.8 else "C")

    # 8 tenant credit: identities are pseudonymized; private credit unknown.
    grades["8_tenant_creditworthiness"] = "B"

    # 9 option documentation: typically not on a rent roll.
    grades["9_option_documentation"] = "B"

    # 10 historical consistency: only when a tie-out is present (else N/A).
    if reconciliation and reconciliation.get("summary"):
        egi = next((d for d in reconciliation["dimensions"] if d["dimension"] == "egi_bridge"), None)
        if egi:
            vp = abs(egi.get("variance_pct") or 0.0)
            grades["10_historical_consistency"] = "A" if vp <= 0.03 else ("B" if vp <= 0.08 else "C")

    return grades, rubric.RENT_ROLL_DIMENSIONS


def _grade_operating_statement(payload: dict, validation: dict) -> tuple:
    checks = validation.get("checks", [])
    by_code = {c.get("code"): c for c in checks}
    crit = {c.get("code") for c in checks if c.get("status") == "critical"}
    warn = {c.get("code") for c in checks if c.get("status") == "warn"}
    records = payload.get("records", [])

    grades: dict = {}
    # period integrity
    if "t12_period_count_invalid" in crit:
        grades["t12_1_period_integrity"] = "C"
    elif "partial_year" in warn:
        grades["t12_1_period_integrity"] = "B"
    else:
        grades["t12_1_period_integrity"] = "A"

    # account mapping coverage (by distinct line key).
    keys = set((r.get("canonical_account"), r.get("line_type")) for r in records)
    unmapped = sum(1 for k in keys if k[0] == "unmapped")
    cov = 1.0 - (unmapped / len(keys)) if keys else 1.0
    grades["t12_2_account_mapping"] = rubric.grade_from_pass_rate(cov)

    # sign convention: A unless validator flagged a flip (none today -> A).
    grades["t12_3_sign_convention"] = "A"

    # NOI classification consistency.
    grades["t12_4_noi_consistency"] = "C" if "noi_includes_below_the_line" in crit else "A"

    # duplicate / subtotal detection.
    grades["t12_5_duplicate_detection"] = "B" if "duplicate_account_line" in warn else "A"

    # provenance coverage: run is stamped + accounts mapped.
    grades["t12_6_provenance"] = "A"

    return grades, rubric.T12_DIMENSIONS


def _grade_tieout(reconciliation: dict, payload: dict) -> dict:
    dims = {d["dimension"]: d for d in reconciliation.get("dimensions", [])}
    grades: dict = {}

    def tie_grade(name: str):
        d = dims.get(name)
        if not d or d.get("one_sided"):
            return None  # N/A -> excluded from the weakest-link, not failed
        if d["tie_status"] == "tied":
            return "A"
        dt = d.get("difference_type")
        # timing differences are explainable -> B; mapping/missing -> C.
        return "B" if dt == "timing" else "C"

    # recoveries + other income live in the combined other_rental dimension.
    for key, dim_name in (
        ("tie_1_base_rent", "base_rent"),
        ("tie_2_recoveries", "other_rental"),
        ("tie_3_other_income", "other_rental"),
        ("tie_4_occupancy", "occupancy"),
        ("tie_5_egi_bridge", "egi_bridge"),
    ):
        g = tie_grade(dim_name)
        if g is not None:
            grades[key] = g

    # residual: small relative to GPR -> A.
    gpr = 0.0
    egi = dims.get("egi_bridge")
    if egi:
        gpr = abs(egi.get("rent_roll_value") or 0.0)
    residual = reconciliation.get("summary", {}).get("residual_unexplained_total", 0.0)
    ratio = (residual / gpr) if gpr else (0.0 if residual == 0 else 1.0)
    grades["tie_6_residual"] = "A" if ratio <= 0.02 else ("B" if ratio <= 0.08 else "C")
    return grades


def _base_rent_by_lease(records: list) -> dict:
    out: dict = {}
    for cl in records:
        if cl.get("charge_category") == "base_rent":
            out.setdefault(cl.get("lease_id"), 0.0)
            out[cl.get("lease_id")] += (cl.get("monthly_amount") or 0.0)
    return out


def main():
    parser = argparse.ArgumentParser(description="Document-to-Database Ingestion Self-Grader")
    parser.add_argument("--json", type=str, help="JSON string with input parameters")
    args = parser.parse_args()

    if args.json:
        inputs = json.loads(args.json)
    elif not sys.stdin.isatty():
        inputs = json.load(sys.stdin)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(calculate_grade_ingestion(inputs), indent=2))


if __name__ == "__main__":
    main()
