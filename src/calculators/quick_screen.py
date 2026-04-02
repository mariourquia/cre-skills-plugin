#!/usr/bin/env python3
"""
Deal Quick Screen Calculator
=============================
Back-of-napkin deal screening: cap rate, price per unit/SF, rent vs market,
DSCR at assumed financing, cash-on-cash, replacement cost ratio.
Produces a KEEP/KILL/MAYBE verdict.

Used by: deal-quick-screen skill

Usage:
    python3 scripts/calculators/quick_screen.py --json '{
        "purchase_price": 8500000,
        "noi": 510000,
        "units_or_sf": 48,
        "unit_type": "units",
        "market_rent_per_unit": 1350,
        "in_place_rent_per_unit": 1100,
        "loan_amount": 5525000,
        "rate": 0.065,
        "amort_years": 30,
        "replacement_cost_estimate": 10500000,
        "property_type": "multifamily",
        "submarket_vacancy": 0.05
    }'

Output: JSON with cap_rate, price_per_unit, rent_vs_market, dscr, cash_on_cash,
        replacement_ratio, verdict, scenario_irrs.
"""

import argparse
import json
import sys
from typing import Any


def mortgage_payment_annual(principal: float, annual_rate: float, amort_years: int) -> float:
    """Calculate annual P&I payment."""
    if annual_rate == 0:
        return principal / amort_years
    monthly_rate = annual_rate / 12
    n = amort_years * 12
    monthly = principal * (monthly_rate * (1 + monthly_rate) ** n) / ((1 + monthly_rate) ** n - 1)
    return monthly * 12


def estimate_irr(
    equity: float,
    annual_cf: float,
    cf_growth: float,
    exit_noi: float,
    exit_cap: float,
    loan_amount: float,
    rate: float,
    amort_years: int,
    hold_years: int,
) -> float | None:
    """Estimate levered IRR using Newton-Raphson."""
    # Build cashflows
    cfs = [-equity]
    annual_ds = mortgage_payment_annual(loan_amount, rate, amort_years)
    noi = annual_cf + annual_ds  # reconstruct NOI from cash flow + debt service

    for yr in range(1, hold_years + 1):
        yr_noi = noi * (1 + cf_growth) ** yr
        yr_cf = yr_noi - annual_ds
        if yr < hold_years:
            cfs.append(yr_cf)
        else:
            # Terminal: sale proceeds - loan payoff + final year CF
            exit_value = exit_noi / exit_cap if exit_cap > 0 else 0
            # Approximate remaining balance
            if rate > 0:
                monthly_rate = rate / 12
                n_total = amort_years * 12
                n_paid = hold_years * 12
                remaining = loan_amount * (
                    ((1 + monthly_rate) ** n_total - (1 + monthly_rate) ** n_paid)
                    / ((1 + monthly_rate) ** n_total - 1)
                )
            else:
                remaining = loan_amount * (1 - hold_years / amort_years)
            net_proceeds = exit_value - remaining
            cfs.append(yr_cf + net_proceeds)

    # Newton-Raphson IRR
    r = 0.10
    for _ in range(500):
        npv = sum(cf / (1 + r) ** t for t, cf in enumerate(cfs))
        dnpv = sum(-t * cf / (1 + r) ** (t + 1) for t, cf in enumerate(cfs))
        if abs(dnpv) < 1e-14:
            break
        new_r = r - npv / dnpv
        if abs(new_r - r) < 1e-8:
            return round(new_r, 4)
        r = new_r
    return round(r, 4)


def calculate_quick_screen(inputs: dict[str, Any]) -> dict[str, Any]:
    """Main calculation entry point."""
    price = inputs["purchase_price"]
    noi = inputs["noi"]
    units_sf = inputs["units_or_sf"]
    unit_type = inputs.get("unit_type", "units")  # "units" or "sf"
    market_rent = inputs.get("market_rent_per_unit")
    in_place_rent = inputs.get("in_place_rent_per_unit")
    loan_amount = inputs.get("loan_amount", price * 0.65)
    rate = inputs.get("rate", 0.07)
    amort_years = inputs.get("amort_years", 30)
    replacement_cost = inputs.get("replacement_cost_estimate")
    hold_years = inputs.get("hold_years", 5)
    target_irr = inputs.get("target_irr", 0.15)
    submarket_vacancy = inputs.get("submarket_vacancy", 0.05)

    # Core metrics
    cap_rate = noi / price if price > 0 else 0
    price_per_unit = price / units_sf if units_sf > 0 else 0

    # Rent comparison
    if market_rent and in_place_rent and market_rent > 0:
        rent_vs_market = (in_place_rent - market_rent) / market_rent
        rent_gap_pct = round(rent_vs_market * 100, 1)
    else:
        rent_vs_market = None
        rent_gap_pct = None

    # DSCR
    annual_ds = mortgage_payment_annual(loan_amount, rate, amort_years)
    dscr = noi / annual_ds if annual_ds > 0 else float("inf")

    # Cash-on-cash
    closing_costs = price * 0.015
    equity = price - loan_amount + closing_costs
    cash_flow = noi - annual_ds
    cash_on_cash = cash_flow / equity if equity > 0 else 0

    # Replacement cost ratio
    replacement_ratio = price / replacement_cost if replacement_cost and replacement_cost > 0 else None

    # Spread (positive leverage check)
    spread = cap_rate - rate
    positive_leverage = spread > 0

    # --- Scenario IRR Estimates ---
    # NOI for exit at hold_years end
    scenarios = {}
    scenario_defs = {
        "bull": {"cf_growth": 0.035, "exit_cap_adj": -0.0025, "occ_adj": 0.02},
        "base": {"cf_growth": 0.025, "exit_cap_adj": 0.0025, "occ_adj": 0.0},
        "bear": {"cf_growth": 0.00, "exit_cap_adj": 0.0075, "occ_adj": -0.05},
    }

    for name, params in scenario_defs.items():
        exit_noi = noi * (1 + params["cf_growth"]) ** hold_years
        exit_cap = cap_rate + params["exit_cap_adj"]
        if exit_cap <= 0:
            exit_cap = 0.04
        irr = estimate_irr(
            equity, cash_flow, params["cf_growth"], exit_noi, exit_cap,
            loan_amount, rate, amort_years, hold_years
        )
        exit_value = exit_noi / exit_cap
        equity_multiple = (cash_flow * hold_years + exit_value - loan_amount * 0.95) / equity if equity > 0 else 0

        scenarios[name] = {
            "noi_growth": params["cf_growth"],
            "exit_cap": round(exit_cap, 4),
            "exit_noi": round(exit_noi, 0),
            "exit_value": round(exit_value, 0),
            "estimated_irr": irr,
            "estimated_equity_multiple": round(equity_multiple, 2),
        }

    # --- Verdict ---
    kill_reasons = []
    keep_reasons = []

    if cap_rate < 0.05:
        kill_reasons.append(f"Cap rate {cap_rate:.1%} below 5.0% threshold")
    elif cap_rate >= 0.06:
        keep_reasons.append(f"Cap rate {cap_rate:.1%} above 6.0%")

    if dscr < 1.15:
        kill_reasons.append(f"DSCR {dscr:.2f}x below 1.15x minimum")
    elif dscr >= 1.25:
        keep_reasons.append(f"DSCR {dscr:.2f}x above 1.25x")

    if replacement_ratio is not None and replacement_ratio > 1.10:
        kill_reasons.append(f"Price at {replacement_ratio:.0%} of replacement cost")
    elif replacement_ratio is not None and replacement_ratio < 0.90:
        keep_reasons.append(f"Price at {replacement_ratio:.0%} of replacement cost (below replacement)")

    if not positive_leverage:
        kill_reasons.append(f"Negative leverage: cap {cap_rate:.1%} < rate {rate:.1%}")
    else:
        keep_reasons.append(f"Positive leverage: {spread:.1%} spread")

    base_irr = scenarios["base"]["estimated_irr"]
    if base_irr is not None and base_irr < target_irr - 0.02:
        kill_reasons.append(f"Base case IRR {base_irr:.1%} well below {target_irr:.0%} target")
    elif base_irr is not None and abs(base_irr - target_irr) <= 0.02:
        keep_reasons.append(f"Base case IRR {base_irr:.1%} within 200bps of {target_irr:.0%} target")
    elif base_irr is not None:
        keep_reasons.append(f"Base case IRR {base_irr:.1%} meets {target_irr:.0%} target")

    if len(kill_reasons) >= 2:
        verdict = "KILL"
    elif len(kill_reasons) == 0 and len(keep_reasons) >= 3:
        verdict = "KEEP"
    else:
        verdict = "MAYBE"

    unit_label = "unit" if unit_type == "units" else "SF"

    return {
        "verdict": verdict,
        "kill_reasons": kill_reasons,
        "keep_reasons": keep_reasons,
        "metrics": {
            "purchase_price": price,
            f"price_per_{unit_label}": round(price_per_unit, 0),
            "going_in_cap_rate": round(cap_rate, 4),
            "noi": noi,
            "annual_debt_service": round(annual_ds, 2),
            "dscr": round(dscr, 3),
            "equity_required": round(equity, 0),
            "year_1_cash_flow": round(cash_flow, 0),
            "cash_on_cash": round(cash_on_cash, 4),
            "leverage_spread": round(spread, 4),
            "positive_leverage": positive_leverage,
            "replacement_cost_ratio": round(replacement_ratio, 3) if replacement_ratio else None,
            "rent_gap_pct": rent_gap_pct,
        },
        "scenarios": scenarios,
        "assumptions": {
            "loan_amount": loan_amount,
            "rate": rate,
            "amortization_years": amort_years,
            "hold_years": hold_years,
            "target_irr": target_irr,
            "closing_cost_pct": 0.015,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="CRE Deal Quick Screen Calculator")
    parser.add_argument("--json", type=str, help="JSON string with input parameters")
    args = parser.parse_args()

    if args.json:
        inputs = json.loads(args.json)
    elif not sys.stdin.isatty():
        inputs = json.load(sys.stdin)
    else:
        parser.print_help()
        sys.exit(1)

    result = calculate_quick_screen(inputs)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
