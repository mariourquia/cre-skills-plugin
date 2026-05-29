#!/usr/bin/env python3
"""
Document-to-Database: Rent Roll <-> T-12 Tie-Out
================================================
Reconciles a normalized rent roll against a normalized T-12 on a STATED,
CONSISTENT basis and never forces a tie.

Basis (labeled on every row): the rent roll is annualized CONTRACTUAL in-place
income; the T-12 is RECOGNIZED ACCRUAL (annualized from the months present);
collected cash is out of scope (no AR feed). Comparing contractual to accrual
produces legitimate variances (free rent, vacancy, CAM true-ups), so those are
classified, not flagged as errors.

Dimensions: base_rent, other_rental (recoveries + other income -- the canonical
chart combines these in one account, so they are reconciled jointly and the
rent-roll-side breakdown is reported), occupancy, and the EGI / NOI-revenue
bridge (the fifth and most important: does the rent roll prove the revenue that
drives NOI?). The OpEx -> NOI leg is owned by t12-to-database, not the tie-out.

Difference classification is deterministic and keyed on whether the TOTAL
reconciles:
  * total (EGI) ties, per-category variances offset  -> MAPPING (reclassification)
  * total ties, a single category drifts (e.g. CAM)  -> TIMING (estimate/true-up)
  * total does NOT tie                                -> MISSING (income present
                                                          in one source, absent in
                                                          the other)

A "forced" tie is impossible by construction: nothing adjusts a number to make
it tie. Untied dimensions carry residual_unexplained and route to human review.

Takes ONE input dict {rent_roll, t12, tolerance_overrides?, run_id, as_of}.
Pure calculate_reconcile_rent_roll_t12(dict)->dict.

Used by: rent-roll-t12-tieout, document-to-database

Usage:
    python3 src/calculators/reconcile_rent_roll_t12.py --json '{
        "run_id": "RUN-1", "as_of": "2026-05-29",
        "rent_roll": { ...normalize_tokens output (rent_roll)... },
        "t12":       { ...normalize_tokens output (t12)... }
    }'

Output: JSON {dimensions, summary, human_review_items, basis}.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from ingest import determinism as det, pii, tolerances as tol

RR_BASIS = "annualized_contractual_in_place"
T12_BASIS = "recognized_accrual_annualized"
COLLECTED_BASIS = "not_available"

RECOVERY_CATS = ("cam_recovery", "tax_recovery", "insurance_recovery")
OTHER_INCOME_CATS = ("parking", "storage", "percentage_rent", "other_recurring", "one_time_amortized")


def calculate_reconcile_rent_roll_t12(inputs: dict) -> dict:
    ctx = det.resolve_context(inputs)
    errs = det.require_context(ctx)
    if ctx.get("tenant_id"):
        errs = errs + pii.assert_safe_tenant_id(ctx["tenant_id"])
    if errs:
        return det.error_result("invalid run context", details=errs)

    rr = inputs.get("rent_roll")
    t12 = inputs.get("t12")
    if not rr or not t12:
        return det.error_result("reconcile requires both 'rent_roll' and 't12' normalized payloads")
    overrides = inputs.get("tolerance_overrides") or {}

    rr_vals = _rent_roll_values(rr)
    t12_vals = _t12_values(t12)

    # EGI bridge first -- its tie/untie drives mapping-vs-missing classification.
    egi = _dimension(
        "egi_bridge", rr_vals["gpr"], t12_vals["total_revenue"],
        tol.reconcile_tolerance("egi_bridge", overrides),
        explanation="Rent-roll annualized contractual gross vs T-12 recognized total revenue. "
                    "OpEx->NOI leg owned by t12-to-database.",
    )
    egi_ties = egi["tie_status"] == "tied"

    base = _dimension(
        "base_rent", rr_vals["base"], t12_vals["base"],
        tol.reconcile_tolerance("base_rent", overrides),
        explanation="Annualized contractual base rent vs T-12 base-rent actual.",
    )
    other = _dimension(
        "other_rental", rr_vals["other_rental"], t12_vals["other_rental"],
        tol.reconcile_tolerance("recoveries", overrides),
        explanation="Recoveries + other income (canonical chart combines these). "
                    "Rent-roll breakdown: recoveries %.2f, other income %.2f."
                    % (rr_vals["recoveries"], rr_vals["other_income"]),
        rr_breakdown={"recoveries": rr_vals["recoveries"], "other_income": rr_vals["other_income"]},
    )

    # Occupancy: one-sided if the T-12 carries no occupancy metric.
    if t12_vals["occupancy"] is None:
        occ = _one_sided(
            "occupancy", rr_vals["occupancy"], None,
            "T-12 reports no occupancy/vacancy metric; not reconcilable against the rent roll here.",
        )
    else:
        occ = _dimension(
            "occupancy", rr_vals["occupancy"], t12_vals["occupancy"],
            tol.reconcile_tolerance("occupancy", overrides),
            explanation="Physical occupancy (count basis).", unit="pct",
        )

    # Classify the untied revenue dimensions with distinct, deterministic
    # signatures (domain definition):
    #   total (EGI) ties + offsetting categories -> MAPPING (reclassification)
    #   total ties + single-category drift        -> TIMING
    #   total does NOT tie + T-12 recoveries > RR  -> TIMING (CAM true-up)
    #   total does NOT tie otherwise               -> MISSING (income gap)
    egi_tol = tol.reconcile_tolerance("egi_bridge", overrides)
    base_var = base["variance"]
    other_var = other["variance"]
    offsetting = (base_var * other_var < 0) and tol.within(
        abs(base_var + other_var), 0.0, max(abs(rr_vals["gpr"]), 1.0) * egi_tol
    )

    def _classify(dim: dict, is_other: bool) -> None:
        if dim["tie_status"] == "tied":
            return
        if egi_ties:
            if offsetting:
                dim["difference_type"] = "mapping"
                dim["confidence"] = "medium"
                dim["candidate_explanation"] += " Offsetting category variance with total tied -> a charge is reclassified into the wrong account."
            else:
                dim["difference_type"] = "timing"
                dim["confidence"] = "medium"
                dim["candidate_explanation"] += " Single-category drift with total tied -> estimate-vs-true-up / period attribution."
        else:
            if is_other and (dim["variance"] or 0.0) < 0:
                dim["difference_type"] = "timing"
                dim["confidence"] = "medium"
                dim["candidate_explanation"] += " T-12 recovery income exceeds the contractual run-rate -> CAM estimate-vs-annual-true-up timing."
            else:
                dim["difference_type"] = "missing"
                dim["confidence"] = "low"
                dim["candidate_explanation"] += " Total revenue does not tie -> income present in one source and absent in the other."

    _classify(base, False)
    _classify(other, True)

    dimensions = [base, other, occ, egi]
    residual_total = round(sum(d.get("residual_unexplained", 0.0) or 0.0 for d in dimensions), 2)

    review: list = []
    for d in dimensions:
        if d["tie_status"] != "tied":
            review.append({
                "dimension": d["dimension"],
                "reason": d["difference_type"],
                "variance": d["variance"],
                "residual_unexplained": d["residual_unexplained"],
                "confidence": d["confidence"],
                "action": "Route to analyst: confirm %s difference." % d["difference_type"],
            })

    tied = sum(1 for d in dimensions if d["tie_status"] == "tied")
    return {
        "dimensions": dimensions,
        "summary": {
            "dimension_count": len(dimensions),
            "tied": tied,
            "untied": len(dimensions) - tied,
            "residual_unexplained_total": residual_total,
            "egi_ties": egi_ties,
        },
        "human_review_items": review,
        "basis": {
            "rent_roll_basis": RR_BASIS,
            "t12_basis": T12_BASIS,
            "collected_basis": COLLECTED_BASIS,
            "t12_annualization_months": t12_vals["periods_present"],
        },
        "run_id": ctx["run_id"],
        "as_of": ctx["as_of"],
    }


def _rent_roll_values(rr: dict) -> dict:
    agg = rr.get("aggregates", {})
    base = float(agg.get("gpr_in_place_annual") or 0.0)
    recoveries = 0.0
    other_income = 0.0
    for cl in rr.get("records", []):
        annual = cl.get("annual_amount")
        if annual is None and cl.get("monthly_amount") is not None:
            annual = cl["monthly_amount"] * 12
        annual = float(annual or 0.0)
        cat = cl.get("charge_category")
        if cat in RECOVERY_CATS:
            recoveries += annual
        elif cat in OTHER_INCOME_CATS:
            other_income += annual
    other_rental = recoveries + other_income
    return {
        "base": det.rnd_money(base),
        "recoveries": det.rnd_money(recoveries),
        "other_income": det.rnd_money(other_income),
        "other_rental": det.rnd_money(other_rental),
        "gpr": det.rnd_money(base + other_rental),
        "occupancy": agg.get("physical_occupancy_pct"),
    }


def _t12_values(t12: dict) -> dict:
    periods = t12.get("aggregates", {}).get("periods_present") or 1
    scale = 12.0 / periods if periods else 1.0
    totals: dict = {}
    for r in t12.get("records", []):
        if r.get("line_type") != "actual":
            continue
        acct = r.get("canonical_account")
        totals[acct] = totals.get(acct, 0.0) + float(r.get("amount") or 0.0)
    base = totals.get("revenue_base_rent", 0.0) * scale
    other_rental = (totals.get("revenue_other_rental", 0.0) + totals.get("revenue_other_non_rental", 0.0)) * scale
    return {
        "base": det.rnd_money(base),
        "other_rental": det.rnd_money(other_rental),
        "total_revenue": det.rnd_money(base + other_rental),
        "occupancy": t12.get("aggregates", {}).get("physical_occupancy_pct"),
        "periods_present": periods,
    }


def _dimension(name: str, rr_value: float, t12_value: float, frac_tol: float,
               explanation: str = "", unit: str = "usd", rr_breakdown: dict | None = None) -> dict:
    rr_v = float(rr_value or 0.0)
    t12_v = float(t12_value or 0.0)
    variance = det.rnd_money(rr_v - t12_v)
    base = max(abs(rr_v), abs(t12_v))
    variance_pct = det.rnd_rate((variance / base)) if base else 0.0
    tied = tol.within_pct(rr_v, t12_v, frac_tol)
    row = {
        "dimension": name,
        "rent_roll_value": det.rnd_money(rr_v),
        "t12_value": det.rnd_money(t12_v),
        "unit": unit,
        "basis": {"rent_roll": RR_BASIS, "t12": T12_BASIS},
        "variance": variance,
        "variance_pct": variance_pct,
        "tolerance_pct": frac_tol,
        "tie_status": "tied" if tied else "untied",
        "difference_type": "within_tolerance" if tied else "unclassified",
        "candidate_explanation": explanation,
        "confidence": "high" if tied else "low",
        # residual_unexplained is 0 when tied; otherwise the full gap is
        # surfaced (NEVER absorbed into a plug).
        "residual_unexplained": 0.0 if tied else abs(variance),
    }
    if rr_breakdown:
        row["rent_roll_breakdown"] = rr_breakdown
    return row


def _one_sided(name: str, rr_value: Any, t12_value: Any, note: str) -> dict:
    return {
        "dimension": name,
        "rent_roll_value": rr_value,
        "t12_value": t12_value,
        "basis": {"rent_roll": RR_BASIS, "t12": T12_BASIS},
        "variance": None,
        "variance_pct": None,
        "tolerance_pct": None,
        "tie_status": "untied",
        "difference_type": "missing",
        "candidate_explanation": note,
        "confidence": "low",
        "residual_unexplained": 0.0,  # cannot quantify a one-sided gap
        "one_sided": True,
    }


def main():
    parser = argparse.ArgumentParser(description="Document-to-Database Rent Roll <-> T-12 Tie-Out")
    parser.add_argument("--json", type=str, help="JSON string with input parameters")
    args = parser.parse_args()

    if args.json:
        inputs = json.loads(args.json)
    elif not sys.stdin.isatty():
        inputs = json.load(sys.stdin)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(calculate_reconcile_rent_roll_t12(inputs), indent=2))


if __name__ == "__main__":
    main()
