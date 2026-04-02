#!/usr/bin/env python3
"""
NPV Trade-Out Analyzer
=======================
Compares renewal NPV vs trade-out NPV for a lease expiration decision.
Produces breakeven analysis (vacancy, rent premium, TI) and a 2D sensitivity grid.

Used by: lease-trade-out-analyzer skill

Usage:
    python3 scripts/calculators/npv_trade_out.py --json '{
        "current_rent_psf": 28.00,
        "market_rent_psf": 35.00,
        "renewal_rent_psf": 32.00,
        "renewal_ti_psf": 5.00,
        "new_ti_psf": 25.00,
        "lc_pct_renewal": 0.025,
        "lc_pct_new": 0.05,
        "vacancy_months": 4,
        "make_ready_psf": 5.00,
        "sf": 10000,
        "lease_term_years": 5,
        "discount_rate": 0.07,
        "annual_escalation": 0.03,
        "carrying_cost_psf_monthly": 2.50
    }'

Output: JSON with renewal_npv, tradeout_npv, delta, breakeven values, sensitivity_grid.
"""

import argparse
import json
import sys
from typing import Any


def npv_stream(cashflows: list[float], rate: float) -> float:
    """Calculate NPV of a list of annual cash flows (year 0 = index 0)."""
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(cashflows))


def annual_rent_with_escalation(base_rent_psf: float, sf: int, escalation: float, years: int) -> list[float]:
    """Generate annual rent amounts with escalation."""
    return [base_rent_psf * sf * (1 + escalation) ** yr for yr in range(years)]


def build_renewal_cashflows(inputs: dict[str, Any]) -> list[float]:
    """Build renewal scenario annual cash flows."""
    sf = inputs["sf"]
    term = inputs["lease_term_years"]
    renewal_rent = inputs["renewal_rent_psf"]
    escalation = inputs.get("annual_escalation", 0.03)
    renewal_ti = inputs.get("renewal_ti_psf", 0.0)
    lc_pct = inputs.get("lc_pct_renewal", 0.025)
    free_rent_months = inputs.get("free_rent_months_renewal", 0)

    rents = annual_rent_with_escalation(renewal_rent, sf, escalation, term)

    # Upfront costs applied in year 0
    ti_cost = renewal_ti * sf
    aggregate_rent = sum(rents)
    lc_cost = aggregate_rent * lc_pct
    free_rent_cost = (renewal_rent * sf / 12) * free_rent_months

    # Year 0: rent minus upfront costs and free rent
    cashflows = []
    for yr in range(term):
        cf = rents[yr]
        if yr == 0:
            cf -= ti_cost + lc_cost + free_rent_cost
        cashflows.append(cf)

    return cashflows


def build_tradeout_cashflows(inputs: dict[str, Any]) -> list[float]:
    """Build trade-out scenario annual cash flows."""
    sf = inputs["sf"]
    term = inputs["lease_term_years"]
    market_rent = inputs["market_rent_psf"]
    escalation = inputs.get("annual_escalation", 0.03)
    new_ti = inputs.get("new_ti_psf", 25.0)
    lc_pct = inputs.get("lc_pct_new", 0.05)
    vacancy_months = inputs.get("vacancy_months", 4)
    make_ready = inputs.get("make_ready_psf", 5.0)
    carrying_cost_monthly = inputs.get("carrying_cost_psf_monthly", 2.50)
    free_rent_months = inputs.get("free_rent_months_new", 0)

    rents = annual_rent_with_escalation(market_rent, sf, escalation, term)

    # Upfront costs
    ti_cost = new_ti * sf
    aggregate_rent = sum(rents)
    lc_cost = aggregate_rent * lc_pct
    make_ready_cost = make_ready * sf
    vacancy_cost = carrying_cost_monthly * sf * vacancy_months
    free_rent_cost = (market_rent * sf / 12) * free_rent_months

    # Year 0: partial year rent (12 - vacancy_months) minus all upfront costs
    months_occupied_yr1 = max(12 - vacancy_months, 0)
    yr1_rent = rents[0] * (months_occupied_yr1 / 12.0)

    cashflows = [yr1_rent - ti_cost - lc_cost - make_ready_cost - vacancy_cost - free_rent_cost]
    for yr in range(1, term):
        cashflows.append(rents[yr])

    return cashflows


def solve_breakeven_vacancy(inputs: dict[str, Any], renewal_npv: float) -> float:
    """Binary search for vacancy months where trade-out NPV equals renewal NPV."""
    rate = inputs.get("discount_rate", 0.07)
    lo, hi = 0.0, 24.0
    for _ in range(100):
        mid = (lo + hi) / 2
        test_inputs = dict(inputs)
        test_inputs["vacancy_months"] = mid
        cfs = build_tradeout_cashflows(test_inputs)
        test_npv = npv_stream(cfs, rate)
        if test_npv > renewal_npv:
            lo = mid
        else:
            hi = mid
    return round((lo + hi) / 2, 1)


def solve_breakeven_rent(inputs: dict[str, Any], renewal_npv: float) -> float:
    """Binary search for market rent PSF where trade-out NPV equals renewal NPV."""
    rate = inputs.get("discount_rate", 0.07)
    lo, hi = 0.0, inputs["market_rent_psf"] * 3
    for _ in range(100):
        mid = (lo + hi) / 2
        test_inputs = dict(inputs)
        test_inputs["market_rent_psf"] = mid
        cfs = build_tradeout_cashflows(test_inputs)
        test_npv = npv_stream(cfs, rate)
        if test_npv < renewal_npv:
            lo = mid
        else:
            hi = mid
    return round((lo + hi) / 2, 2)


def solve_breakeven_ti(inputs: dict[str, Any], renewal_npv: float) -> float:
    """Binary search for new TI PSF where trade-out NPV equals renewal NPV."""
    rate = inputs.get("discount_rate", 0.07)
    lo, hi = 0.0, 100.0
    for _ in range(100):
        mid = (lo + hi) / 2
        test_inputs = dict(inputs)
        test_inputs["new_ti_psf"] = mid
        cfs = build_tradeout_cashflows(test_inputs)
        test_npv = npv_stream(cfs, rate)
        if test_npv > renewal_npv:
            lo = mid
        else:
            hi = mid
    return round((lo + hi) / 2, 2)


def build_sensitivity_grid(inputs: dict[str, Any], rate: float) -> list[dict[str, Any]]:
    """
    2D sensitivity grid: vacancy months (columns) x rent premium (rows).
    Each cell shows trade-out NPV minus renewal NPV.
    """
    renewal_cfs = build_renewal_cashflows(inputs)
    renewal_npv = npv_stream(renewal_cfs, rate)

    vacancy_scenarios = [2, 4, 6, 9, 12]
    # Rent premium as % above current rent
    current = inputs.get("renewal_rent_psf", inputs["current_rent_psf"])
    rent_premiums = [0.05, 0.10, 0.15, 0.20, 0.25]  # 5% to 25% above renewal

    grid = []
    for prem in rent_premiums:
        row = {"rent_psf": round(current * (1 + prem), 2), "premium_pct": prem}
        for vac in vacancy_scenarios:
            test_inputs = dict(inputs)
            test_inputs["market_rent_psf"] = current * (1 + prem)
            test_inputs["vacancy_months"] = vac
            cfs = build_tradeout_cashflows(test_inputs)
            delta = round(npv_stream(cfs, rate) - renewal_npv, 0)
            row[f"vacancy_{vac}mo"] = delta
        grid.append(row)

    return grid


def calculate_trade_out(inputs: dict[str, Any]) -> dict[str, Any]:
    """Main calculation entry point."""
    rate = inputs.get("discount_rate", 0.07)

    renewal_cfs = build_renewal_cashflows(inputs)
    tradeout_cfs = build_tradeout_cashflows(inputs)

    renewal_npv = round(npv_stream(renewal_cfs, rate), 0)
    tradeout_npv = round(npv_stream(tradeout_cfs, rate), 0)
    delta = round(tradeout_npv - renewal_npv, 0)

    # Breakeven analysis
    breakeven_vacancy = solve_breakeven_vacancy(inputs, renewal_npv)
    breakeven_rent = solve_breakeven_rent(inputs, renewal_npv)
    breakeven_ti = solve_breakeven_ti(inputs, renewal_npv)

    # Effective rent calculations
    sf = inputs["sf"]
    term = inputs["lease_term_years"]
    renewal_total = sum(renewal_cfs)
    tradeout_total = sum(tradeout_cfs)
    renewal_effective = round(renewal_total / term / sf, 2)
    tradeout_effective = round(tradeout_total / term / sf, 2)

    # Sensitivity grid
    grid = build_sensitivity_grid(inputs, rate)

    # Verdict
    pct_delta = abs(delta) / abs(renewal_npv) * 100 if renewal_npv != 0 else 0
    if delta > 0 and pct_delta > 15:
        verdict = "TRADE_OUT"
        confidence = "HIGH"
    elif delta > 0 and pct_delta > 5:
        verdict = "TRADE_OUT"
        confidence = "MEDIUM"
    elif delta < 0 and pct_delta > 15:
        verdict = "RENEW"
        confidence = "HIGH"
    elif delta < 0 and pct_delta > 5:
        verdict = "RENEW"
        confidence = "MEDIUM"
    else:
        verdict = "MARGINAL"
        confidence = "LOW"

    return {
        "renewal_npv": renewal_npv,
        "tradeout_npv": tradeout_npv,
        "npv_delta": delta,
        "delta_pct_of_renewal": round(pct_delta, 1),
        "verdict": verdict,
        "confidence": confidence,
        "renewal_effective_rent_psf": renewal_effective,
        "tradeout_effective_rent_psf": tradeout_effective,
        "breakeven_vacancy_months": breakeven_vacancy,
        "breakeven_rent_psf": breakeven_rent,
        "breakeven_ti_psf": breakeven_ti,
        "renewal_cashflows": [round(c, 0) for c in renewal_cfs],
        "tradeout_cashflows": [round(c, 0) for c in tradeout_cfs],
        "sensitivity_grid": grid,
        "discount_rate": rate,
        "assumptions": {
            "current_rent_psf": inputs["current_rent_psf"],
            "market_rent_psf": inputs["market_rent_psf"],
            "renewal_rent_psf": inputs.get("renewal_rent_psf"),
            "sf": sf,
            "term_years": term,
            "vacancy_months": inputs.get("vacancy_months", 4),
            "new_ti_psf": inputs.get("new_ti_psf", 25.0),
            "renewal_ti_psf": inputs.get("renewal_ti_psf", 0.0),
        },
    }


def main():
    parser = argparse.ArgumentParser(description="NPV Trade-Out Analyzer for lease decisions")
    parser.add_argument("--json", type=str, help="JSON string with input parameters")
    args = parser.parse_args()

    if args.json:
        inputs = json.loads(args.json)
    elif not sys.stdin.isatty():
        inputs = json.load(sys.stdin)
    else:
        parser.print_help()
        sys.exit(1)

    result = calculate_trade_out(inputs)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
