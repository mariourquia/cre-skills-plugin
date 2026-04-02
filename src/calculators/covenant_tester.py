#!/usr/bin/env python3
"""
Loan Covenant Tester
====================
Tests loan covenants (DSCR, LTV, debt yield) against multi-year projections.
Detects first breach year and cash sweep trigger activation.

Used by: loan-document-reviewer skill

Usage:
    python3 scripts/calculators/covenant_tester.py --json '{
        "noi_by_year": [1200000, 1250000, 1300000, 1350000, 1400000],
        "loan_amount": 10000000,
        "rate": 0.065,
        "amortization_years": 30,
        "io_years": 2,
        "property_value_by_year": [16000000, 16500000, 17000000, 17500000, 18000000],
        "dscr_covenant": 1.25,
        "ltv_covenant": 0.75,
        "debt_yield_covenant": 0.08,
        "cash_sweep_dscr": 1.15
    }'

Output: JSON with dscr_by_year, ltv_by_year, debt_yield_by_year, breach_year,
        cash_sweep_years, annual_detail.
"""

import argparse
import json
import math
import sys
from typing import Any


def mortgage_payment(principal: float, annual_rate: float, amort_years: int) -> float:
    """Calculate annual mortgage payment (P&I) using standard amortization formula."""
    if annual_rate == 0:
        return principal / amort_years
    monthly_rate = annual_rate / 12
    n_payments = amort_years * 12
    monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** n_payments) / (
        (1 + monthly_rate) ** n_payments - 1
    )
    return monthly_payment * 12


def loan_balance_at_year(
    principal: float, annual_rate: float, amort_years: int, years_elapsed: int
) -> float:
    """Calculate remaining loan balance after N years of amortization."""
    if annual_rate == 0:
        return principal - (principal / amort_years) * years_elapsed

    monthly_rate = annual_rate / 12
    n_total = amort_years * 12
    n_paid = years_elapsed * 12

    if n_paid >= n_total:
        return 0.0

    # Remaining balance formula
    balance = principal * (
        ((1 + monthly_rate) ** n_total - (1 + monthly_rate) ** n_paid)
        / ((1 + monthly_rate) ** n_total - 1)
    )
    return balance


def calculate_covenants(inputs: dict[str, Any]) -> dict[str, Any]:
    """Main calculation entry point."""
    noi_by_year = inputs["noi_by_year"]
    loan_amount = inputs["loan_amount"]
    rate = inputs["rate"]
    amort_years = inputs.get("amortization_years", 30)
    io_years = inputs.get("io_years", 0)
    property_values = inputs.get("property_value_by_year", [])
    dscr_covenant = inputs.get("dscr_covenant", 1.25)
    ltv_covenant = inputs.get("ltv_covenant", 0.75)
    dy_covenant = inputs.get("debt_yield_covenant")
    cash_sweep_dscr = inputs.get("cash_sweep_dscr")

    # Annual P&I payment (amortizing)
    annual_pi = mortgage_payment(loan_amount, rate, amort_years)
    # IO payment
    annual_io = loan_amount * rate

    n_years = len(noi_by_year)
    annual_detail = []
    dscr_by_year = []
    ltv_by_year = []
    dy_by_year = []
    breach_year = None
    breach_type = None
    cash_sweep_years = []

    # Track amortization start year for balance calculation
    amort_start_year = io_years  # amortization begins after IO period

    for yr in range(n_years):
        noi = noi_by_year[yr]
        year_label = yr + 1

        # Debt service depends on whether we are in IO or amortizing period
        if yr < io_years:
            debt_service = annual_io
            ds_type = "IO"
            # During IO, loan balance is unchanged
            balance = loan_amount
        else:
            debt_service = annual_pi
            ds_type = "P&I"
            # Calculate remaining balance
            amort_years_elapsed = yr - io_years
            balance = loan_balance_at_year(loan_amount, rate, amort_years, amort_years_elapsed)

        # DSCR
        dscr = round(noi / debt_service, 3) if debt_service > 0 else float("inf")
        dscr_by_year.append(dscr)

        # LTV (only if property values provided)
        if yr < len(property_values) and property_values[yr] > 0:
            ltv = round(balance / property_values[yr], 4)
            ltv_by_year.append(ltv)
        else:
            ltv = None
            ltv_by_year.append(None)

        # Debt Yield
        dy = round(noi / balance, 4) if balance > 0 else float("inf")
        dy_by_year.append(dy)

        # Cash flow after debt service
        cash_flow = round(noi - debt_service, 2)

        # Check for breaches
        dscr_breach = dscr < dscr_covenant
        ltv_breach = ltv is not None and ltv > ltv_covenant
        dy_breach = dy_covenant is not None and dy < dy_covenant

        any_breach = dscr_breach or ltv_breach or dy_breach
        if any_breach and breach_year is None:
            breach_year = year_label
            if dscr_breach:
                breach_type = "DSCR"
            elif ltv_breach:
                breach_type = "LTV"
            else:
                breach_type = "Debt Yield"

        # Cash sweep check
        cash_sweep_active = cash_sweep_dscr is not None and dscr < cash_sweep_dscr
        if cash_sweep_active:
            cash_sweep_years.append(year_label)

        annual_detail.append({
            "year": year_label,
            "noi": noi,
            "debt_service": round(debt_service, 2),
            "debt_service_type": ds_type,
            "loan_balance": round(balance, 2),
            "property_value": property_values[yr] if yr < len(property_values) else None,
            "cash_flow": cash_flow,
            "dscr": dscr,
            "dscr_covenant": dscr_covenant,
            "dscr_in_compliance": not dscr_breach,
            "ltv": ltv,
            "ltv_covenant": ltv_covenant,
            "ltv_in_compliance": not ltv_breach if ltv is not None else True,
            "debt_yield": dy,
            "debt_yield_covenant": dy_covenant,
            "dy_in_compliance": not dy_breach if dy_covenant else True,
            "cash_sweep_active": cash_sweep_active,
        })

    # Summary metrics
    min_dscr = min(dscr_by_year)
    min_dscr_year = dscr_by_year.index(min_dscr) + 1
    avg_dscr = round(sum(dscr_by_year) / len(dscr_by_year), 3)

    # DSCR at stressed rate (+200bps)
    stressed_rate = rate + 0.02
    stressed_pi = mortgage_payment(loan_amount, stressed_rate, amort_years)
    stressed_io = loan_amount * stressed_rate
    stressed_dscr_yr1 = round(
        noi_by_year[0] / (stressed_io if io_years > 0 else stressed_pi), 3
    )

    # Breakeven NOI for DSCR covenant
    if io_years > 0:
        breakeven_noi_io = round(annual_io * dscr_covenant, 2)
    else:
        breakeven_noi_io = None
    breakeven_noi_amort = round(annual_pi * dscr_covenant, 2)

    return {
        "summary": {
            "loan_amount": loan_amount,
            "rate": rate,
            "amortization_years": amort_years,
            "io_years": io_years,
            "annual_debt_service_io": round(annual_io, 2),
            "annual_debt_service_amort": round(annual_pi, 2),
            "min_dscr": min_dscr,
            "min_dscr_year": min_dscr_year,
            "avg_dscr": avg_dscr,
            "stressed_dscr_yr1_plus200bps": stressed_dscr_yr1,
            "breakeven_noi_io": breakeven_noi_io,
            "breakeven_noi_amort": breakeven_noi_amort,
        },
        "covenants": {
            "dscr_covenant": dscr_covenant,
            "ltv_covenant": ltv_covenant,
            "debt_yield_covenant": dy_covenant,
            "cash_sweep_dscr": cash_sweep_dscr,
        },
        "breach_detected": breach_year is not None,
        "first_breach_year": breach_year,
        "first_breach_type": breach_type,
        "cash_sweep_years": cash_sweep_years,
        "dscr_by_year": dscr_by_year,
        "ltv_by_year": ltv_by_year,
        "debt_yield_by_year": dy_by_year,
        "annual_detail": annual_detail,
    }


def main():
    parser = argparse.ArgumentParser(description="Loan Covenant Tester for CRE debt")
    parser.add_argument("--json", type=str, help="JSON string with input parameters")
    args = parser.parse_args()

    if args.json:
        inputs = json.loads(args.json)
    elif not sys.stdin.isatty():
        inputs = json.load(sys.stdin)
    else:
        parser.print_help()
        sys.exit(1)

    result = calculate_covenants(inputs)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
