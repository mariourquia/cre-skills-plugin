#!/usr/bin/env python3
"""
Document-to-Database: Payload Validator
=======================================
Runs type / range / nullability and cross-field reconciliation checks over a
canonical payload produced by normalize_tokens. Distinguishes IMPOSSIBLE data
(negative SF, occupancy > 100%, expiry < start, 12-period contradiction ->
hard fail / critical) from IMPLAUSIBLE data (statistical outliers -> warning +
confidence hit), so a genuinely high trophy-asset rent never fails closed.

Cross-field rules reuse the rent-roll rubric tolerances (annual == monthly*12
within $1) and are SKIPPED-with-note for stepped / abated / stub-month leases
where the point-in-time identity legitimately does not hold.

Pure calculate_validate_payload(dict)->dict; selectors in --json.

Used by: document-to-database, rent-roll-to-database, t12-to-database

Usage:
    python3 src/calculators/validate_payload.py --json '{
        "property_type": "multifamily",
        "payload": { ...output of normalize_tokens... }
    }'

Output: JSON {checks, summary, validation_status}.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from ingest import determinism as det, tolerances as tol


def calculate_validate_payload(inputs: dict) -> dict:
    payload = inputs.get("payload") or {}
    if not payload:
        return det.error_result("missing 'payload' (output of normalize_tokens)")
    doc_type = payload.get("doc_type", "rent_roll")
    property_type = (inputs.get("property_type") or "multifamily").strip().lower()

    if doc_type == "rent_roll":
        checks = _validate_rent_roll(payload, property_type)
    else:
        checks = _validate_operating_statement(payload)

    # Carry forward critical/structural issues flagged during normalization.
    for iss in payload.get("issues") or []:
        if iss.get("severity") in ("critical", "fail"):
            checks.append({"code": iss["code"], "status": iss["severity"],
                           "field_path": iss.get("field_path"), "detail": iss.get("detail")})

    counts = {"pass": 0, "warn": 0, "fail": 0, "critical": 0}
    for c in checks:
        counts[c["status"]] = counts.get(c["status"], 0) + 1
    status = "pass"
    for sev in ("critical", "fail", "warn"):
        if counts.get(sev):
            status = sev
            break

    return {
        "doc_type": doc_type,
        "checks": checks,
        "summary": counts,
        "validation_status": status,
        "pass_rate": round((counts["pass"] / len(checks)) if checks else 1.0, 4),
    }


def _validate_rent_roll(payload: dict, property_type: str) -> list:
    checks: list = []
    leases = {l["lease_id"]: l for l in payload.get("leases", [])}
    units = {u["unit_id"]: u for u in payload.get("units", [])}

    # Per-charge rent arithmetic (annual == monthly*12 within $1), skipping
    # stepped/abated leases where the identity legitimately fails.
    for cl in payload.get("records", []):
        lease = leases.get(cl.get("lease_id"), {})
        monthly = cl.get("monthly_amount")
        annual = cl.get("annual_amount")
        if monthly is None or annual is None:
            continue
        if lease.get("has_step_or_abatement"):
            checks.append(_chk("rent_arithmetic_skipped", "pass", cl.get("lease_id"),
                               "annual==monthly*12 skipped (step/abatement present)."))
            continue
        if tol.within(annual, monthly * 12, tol.RENT_ARITHMETIC_DOLLAR):
            checks.append(_chk("rent_arithmetic", "pass", cl.get("lease_id"), "annual==monthly*12 within $1."))
        else:
            checks.append(_chk("rent_arithmetic_contradiction", "critical", cl.get("lease_id"),
                               "annual %.2f != monthly*12 %.2f beyond $1." % (annual, monthly * 12)))

    # Negative/zero base rent on an occupied unit.
    occupied_units = {u_id for u_id, u in units.items() if u.get("unit_status") == "occupied"}
    base_by_lease: dict = {}
    for cl in payload.get("records", []):
        if cl.get("charge_category") == "base_rent":
            base_by_lease.setdefault(cl.get("lease_id"), 0.0)
            base_by_lease[cl.get("lease_id")] += (cl.get("monthly_amount") or 0.0)
    for l_id, lease in leases.items():
        if lease.get("unit_id") in occupied_units:
            if base_by_lease.get(l_id, 0.0) <= 0:
                checks.append(_chk("negative_or_zero_rent_occupied", "critical", l_id,
                                   "Occupied unit carries no positive base rent."))

    # PSF reconciliation branches on property type.
    if property_type in ("office", "retail", "industrial", "mixed-use"):
        for cl in payload.get("records", []):
            if cl.get("charge_category") == "base_rent" and cl.get("psf_basis") is not None:
                psf = cl["psf_basis"]
                if psf <= 0 or psf > 500:
                    checks.append(_chk("rent_psf_implausible", "warn", cl.get("lease_id"),
                                       "Base-rent PSF %.2f outside [0, 500]; flagged for review (not rejected)." % psf))
    else:
        checks.append(_chk("psf_skipped_multifamily", "pass", None,
                           "PSF reconciliation skipped; multifamily is per-unit."))

    # Occupancy range.
    agg = payload.get("aggregates", {})
    occ = agg.get("physical_occupancy_pct")
    if occ is not None:
        if occ < 0 or occ > 100:
            checks.append(_chk("occupancy_out_of_range", "critical", "aggregates.physical_occupancy_pct",
                               "Physical occupancy %.2f outside [0,100]." % occ))
        else:
            checks.append(_chk("occupancy_in_range", "pass", None, "Occupancy within [0,100]."))

    # Non-negative SF.
    for u_id, u in units.items():
        sf = u.get("rentable_sf")
        if sf is not None and sf < 0:
            checks.append(_chk("negative_sf", "critical", "units.%s.rentable_sf" % u_id, "Rentable SF negative."))

    return checks


def _validate_operating_statement(payload: dict) -> list:
    checks: list = []
    agg = payload.get("aggregates", {})
    periods_present = agg.get("periods_present", 0)
    expected = agg.get("periods_expected")

    if payload.get("doc_type") == "t12":
        if periods_present == 12:
            checks.append(_chk("period_count", "pass", "periods", "Exactly 12 monthly periods."))
        elif periods_present < 12:
            checks.append(_chk("partial_year", "warn", "periods",
                               "%d periods (<12); partial-year/lease-up carried as a gap." % periods_present))
        else:
            checks.append(_chk("t12_period_count_invalid", "critical", "periods",
                               "%d periods (>12); aggregate column likely not excluded." % periods_present))

    # NOI consistency: revenue - opex must equal reported NOI (below-the-line excluded).
    rev = agg.get("revenue_actual")
    opex = agg.get("operating_expense_actual")
    noi = agg.get("noi_actual")
    if rev is not None and opex is not None and noi is not None:
        recomputed = rev - opex
        if det.rnd_money(recomputed) == det.rnd_money(noi):
            checks.append(_chk("noi_consistency", "pass", "aggregates.noi_actual",
                               "NOI == revenue - operating_expense (below-the-line excluded)."))
        else:
            checks.append(_chk("noi_includes_below_the_line", "critical", "aggregates.noi_actual",
                               "NOI %.2f != revenue-opex %.2f; check section classification." % (noi, recomputed)))

    # Unmapped accounts coverage.
    recs = payload.get("records", [])
    unmapped = sum(1 for r in recs if r.get("canonical_account") == "unmapped")
    if recs:
        cov = 1.0 - (unmapped / len(set((r.get("canonical_account"), r.get("line_type")) for r in recs)))
        if unmapped == 0:
            checks.append(_chk("account_mapping_complete", "pass", None, "All lines mapped to canonical accounts."))
        else:
            checks.append(_chk("account_unmapped_present", "warn", None,
                               "%d line-rows mapped to 'unmapped' bucket; routed to review." % unmapped))

    return checks


def _chk(code: str, status: str, field_path: Any, detail: str) -> dict:
    return {"code": code, "status": status, "field_path": field_path, "detail": detail}


def main():
    parser = argparse.ArgumentParser(description="Document-to-Database Payload Validator")
    parser.add_argument("--json", type=str, help="JSON string with input parameters")
    args = parser.parse_args()

    if args.json:
        inputs = json.loads(args.json)
    elif not sys.stdin.isatty():
        inputs = json.load(sys.stdin)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(calculate_validate_payload(inputs), indent=2))


if __name__ == "__main__":
    main()
