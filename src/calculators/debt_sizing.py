#!/usr/bin/env python3
"""
Debt Sizing Engine
==================
Sizes a CRE loan against simultaneous DSCR, LTV, and debt yield constraints.
Identifies the binding constraint and recommends the maximum loan amount.

Used by: loan-sizing-engine skill

Usage:
    python3 scripts/calculators/debt_sizing.py --json '{
        "noi": 1500000,
        "property_value": 20000000,
        "target_dscr": 1.25,
        "target_ltv": 0.65,
        "target_debt_yield": 0.09,
        "rate": 0.065,
        "amortization_years": 30,
        "io_years": 2
    }'

Output: JSON with max_loan_dscr, max_loan_ltv, max_loan_dy, binding_constraint,
        recommended_loan, annual_debt_service, rate_sensitivity.
"""

import argparse
import json
import sys
from typing import Any


def mortgage_constant(annual_rate: float, amort_years: int) -> float:
    """
    Calculate the annual mortgage constant (annual debt service per dollar of loan).
    This is the ratio of annual P&I payment to the loan amount.
    """
    if annual_rate == 0:
        return 1.0 / amort_years
    monthly_rate = annual_rate / 12
    n_payments = amort_years * 12
    monthly_constant = (monthly_rate * (1 + monthly_rate) ** n_payments) / (
        (1 + monthly_rate) ** n_payments - 1
    )
    return monthly_constant * 12


def annual_debt_service(loan_amount: float, annual_rate: float, amort_years: int) -> float:
    """Calculate annual P&I payment."""
    return loan_amount * mortgage_constant(annual_rate, amort_years)


def size_by_dscr(
    noi: float, target_dscr: float, annual_rate: float, amort_years: int, io_years: int
) -> dict[str, Any]:
    """Size loan based on DSCR constraint."""
    # Size on amortizing payment (more conservative)
    mc = mortgage_constant(annual_rate, amort_years)
    max_loan_amort = noi / (target_dscr * mc)

    # Also check IO sizing
    if io_years > 0:
        max_loan_io = noi / (target_dscr * annual_rate) if annual_rate > 0 else float("inf")
    else:
        max_loan_io = max_loan_amort

    # Use the more conservative (lower) of the two
    max_loan = min(max_loan_amort, max_loan_io)

    return {
        "max_loan": round(max_loan, 0),
        "max_loan_amortizing": round(max_loan_amort, 0),
        "max_loan_io": round(max_loan_io, 0) if io_years > 0 else None,
        "binding_on": "amortizing" if max_loan_amort <= max_loan_io else "io",
        "mortgage_constant": round(mc, 6),
        "annual_ds_at_max": round(max_loan * mc, 2),
        "dscr_at_max": target_dscr,
    }


def size_by_ltv(property_value: float, target_ltv: float) -> dict[str, Any]:
    """Size loan based on LTV constraint."""
    max_loan = property_value * target_ltv
    return {
        "max_loan": round(max_loan, 0),
        "ltv_at_max": target_ltv,
    }


def size_by_debt_yield(noi: float, target_debt_yield: float) -> dict[str, Any]:
    """Size loan based on debt yield constraint."""
    if target_debt_yield <= 0:
        return {"max_loan": float("inf"), "debt_yield_at_max": target_debt_yield}
    max_loan = noi / target_debt_yield
    return {
        "max_loan": round(max_loan, 0),
        "debt_yield_at_max": target_debt_yield,
    }


def rate_sensitivity_grid(
    noi: float,
    property_value: float,
    target_dscr: float,
    target_ltv: float,
    target_dy: float | None,
    base_rate: float,
    amort_years: int,
    io_years: int,
) -> list[dict[str, Any]]:
    """
    Generate rate sensitivity grid showing max loan at various rate levels.
    Debt yield is rate-independent -- DY column stays constant.
    """
    scenarios = [0, 50, 100, 150, 200, 300]  # bps above base
    grid = []

    for bps in scenarios:
        rate = base_rate + bps / 10000
        mc = mortgage_constant(rate, amort_years)
        max_dscr = round(noi / (target_dscr * mc), 0)
        max_ltv = round(property_value * target_ltv, 0)
        max_dy = round(noi / target_dy, 0) if target_dy and target_dy > 0 else None

        candidates = [max_dscr, max_ltv]
        if max_dy is not None:
            candidates.append(max_dy)
        binding_loan = min(candidates)

        if binding_loan == max_dscr:
            binding = "DSCR"
        elif binding_loan == max_ltv:
            binding = "LTV"
        else:
            binding = "Debt Yield"

        ds = annual_debt_service(binding_loan, rate, amort_years)
        actual_dscr = round(noi / ds, 3) if ds > 0 else float("inf")
        actual_ltv = round(binding_loan / property_value, 4) if property_value > 0 else 0
        actual_dy = round(noi / binding_loan, 4) if binding_loan > 0 else float("inf")

        grid.append({
            "rate_bps_over_base": bps,
            "rate": round(rate, 4),
            "mortgage_constant": round(mc, 6),
            "max_loan_dscr": max_dscr,
            "max_loan_ltv": max_ltv,
            "max_loan_dy": max_dy,
            "recommended_loan": binding_loan,
            "binding_constraint": binding,
            "annual_debt_service": round(ds, 2),
            "actual_dscr": actual_dscr,
            "actual_ltv": actual_ltv,
            "actual_debt_yield": actual_dy,
        })

    return grid


def calculate_debt_sizing(inputs: dict[str, Any]) -> dict[str, Any]:
    """Main calculation entry point."""
    noi = inputs["noi"]
    prop_value = inputs["property_value"]
    target_dscr = inputs.get("target_dscr", 1.25)
    target_ltv = inputs.get("target_ltv", 0.65)
    target_dy = inputs.get("target_debt_yield")
    rate = inputs["rate"]
    amort_years = inputs.get("amortization_years", 30)
    io_years = inputs.get("io_years", 0)

    # Size against each constraint
    dscr_result = size_by_dscr(noi, target_dscr, rate, amort_years, io_years)
    ltv_result = size_by_ltv(prop_value, target_ltv)
    dy_result = size_by_debt_yield(noi, target_dy) if target_dy else None

    # Determine binding constraint
    candidates = {
        "DSCR": dscr_result["max_loan"],
        "LTV": ltv_result["max_loan"],
    }
    if dy_result:
        candidates["Debt Yield"] = dy_result["max_loan"]

    binding_constraint = min(candidates, key=candidates.get)
    recommended_loan = candidates[binding_constraint]

    # Calculate actual metrics at recommended loan
    mc = mortgage_constant(rate, amort_years)
    ds_amort = recommended_loan * mc
    ds_io = recommended_loan * rate

    actual_dscr_amort = round(noi / ds_amort, 3) if ds_amort > 0 else float("inf")
    actual_dscr_io = round(noi / ds_io, 3) if ds_io > 0 else float("inf")
    actual_ltv = round(recommended_loan / prop_value, 4) if prop_value > 0 else 0
    actual_dy = round(noi / recommended_loan, 4) if recommended_loan > 0 else float("inf")

    equity_required = prop_value - recommended_loan
    cash_on_cash = round((noi - ds_amort) / equity_required, 4) if equity_required > 0 else 0

    # Positive leverage check
    going_in_cap = noi / prop_value if prop_value > 0 else 0
    positive_leverage = going_in_cap > rate

    # Rate sensitivity
    grid = rate_sensitivity_grid(
        noi, prop_value, target_dscr, target_ltv, target_dy or 0, rate, amort_years, io_years
    )

    return {
        "sizing_results": {
            "max_loan_dscr": dscr_result["max_loan"],
            "max_loan_ltv": ltv_result["max_loan"],
            "max_loan_debt_yield": dy_result["max_loan"] if dy_result else None,
            "binding_constraint": binding_constraint,
            "recommended_loan": recommended_loan,
        },
        "loan_metrics": {
            "recommended_loan": recommended_loan,
            "annual_debt_service_amort": round(ds_amort, 2),
            "annual_debt_service_io": round(ds_io, 2),
            "mortgage_constant": round(mc, 6),
            "dscr_amortizing": actual_dscr_amort,
            "dscr_io": actual_dscr_io,
            "ltv": actual_ltv,
            "debt_yield": actual_dy,
            "equity_required": round(equity_required, 0),
            "cash_on_cash_yr1": cash_on_cash,
            "positive_leverage": positive_leverage,
            "going_in_cap": round(going_in_cap, 4),
        },
        "constraints_applied": {
            "target_dscr": target_dscr,
            "target_ltv": target_ltv,
            "target_debt_yield": target_dy,
            "rate": rate,
            "amortization_years": amort_years,
            "io_years": io_years,
        },
        "dscr_detail": dscr_result,
        "ltv_detail": ltv_result,
        "debt_yield_detail": dy_result,
        "rate_sensitivity": grid,
    }


def main():
    parser = argparse.ArgumentParser(description="CRE Debt Sizing Engine")
    parser.add_argument("--json", type=str, help="JSON string with input parameters")
    args = parser.parse_args()

    if args.json:
        inputs = json.loads(args.json)
    elif not sys.stdin.isatty():
        inputs = json.load(sys.stdin)
    else:
        parser.print_help()
        sys.exit(1)

    result = calculate_debt_sizing(inputs)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
