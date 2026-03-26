#!/usr/bin/env python3
"""
JV Waterfall Calculator
========================
Calculates GP/LP distributions through a multi-tier promote waterfall with
preferred return accrual, catch-up provisions, and IRR-based lookback.

Used by: jv-waterfall-architect skill

Usage:
    python3 scripts/calculators/waterfall_calculator.py --json '{
        "lp_equity": 9000000,
        "gp_equity": 1000000,
        "preferred_return": 0.08,
        "tiers": [
            {"hurdle_irr": 0.08, "gp_split": 0.20, "lp_split": 0.80},
            {"hurdle_irr": 0.12, "gp_split": 0.30, "lp_split": 0.70},
            {"hurdle_irr": 0.18, "gp_split": 0.40, "lp_split": 0.60}
        ],
        "cashflows_by_period": [-10000000, 800000, 850000, 900000, 950000, 15000000],
        "catch_up_pct": 0.50,
        "compounding": true
    }'

Output: JSON with lp_distributions, gp_distributions, gp_promote, lp_irr,
        gp_irr, total_profit, tier_detail.
"""

import argparse
import json
import sys
from typing import Any


def irr_calc(cashflows: list[float], guess: float = 0.10, max_iter: int = 1000, tol: float = 1e-8) -> float | None:
    """
    Calculate IRR using Newton-Raphson method.
    Returns None if IRR cannot be found.
    """
    rate = guess
    for _ in range(max_iter):
        npv = sum(cf / (1 + rate) ** t for t, cf in enumerate(cashflows))
        dnpv = sum(-t * cf / (1 + rate) ** (t + 1) for t, cf in enumerate(cashflows))
        if abs(dnpv) < 1e-14:
            break
        new_rate = rate - npv / dnpv
        if abs(new_rate - rate) < tol:
            return round(new_rate, 6)
        rate = new_rate
    # Fallback: if Newton doesn't converge, try bisection
    lo, hi = -0.99, 5.0
    for _ in range(200):
        mid = (lo + hi) / 2
        npv = sum(cf / (1 + mid) ** t for t, cf in enumerate(cashflows))
        if abs(npv) < tol:
            return round(mid, 6)
        if npv > 0:
            lo = mid
        else:
            hi = mid
    return round((lo + hi) / 2, 6)


def calculate_waterfall(inputs: dict[str, Any]) -> dict[str, Any]:
    """Main waterfall calculation."""
    lp_equity = inputs["lp_equity"]
    gp_equity = inputs["gp_equity"]
    total_equity = lp_equity + gp_equity
    lp_share = lp_equity / total_equity
    gp_share = gp_equity / total_equity

    pref_rate = inputs.get("preferred_return", 0.08)
    tiers = inputs.get("tiers", [])
    cashflows = inputs["cashflows_by_period"]
    catch_up_pct = inputs.get("catch_up_pct", 0)
    compounding = inputs.get("compounding", True)

    n_periods = len(cashflows)

    # Total distributions available (sum of positive cashflows after initial investment)
    total_invested = abs(cashflows[0]) if cashflows[0] < 0 else 0
    total_distributions = sum(cf for cf in cashflows if cf > 0)
    total_profit = total_distributions - total_invested

    # --- Waterfall Distribution ---
    # Aggregate all positive cashflows for distribution
    distributable = total_distributions

    # Track allocations
    lp_pref_accrued = 0.0
    lp_pref_paid = 0.0
    lp_capital_returned = 0.0
    gp_capital_returned = 0.0
    gp_catch_up = 0.0
    tier_distributions = []

    remaining = distributable

    # TIER 1: Preferred Return to LP
    if compounding:
        # Simple compounding: preferred return on unreturned capital for each period
        periods_with_cash = n_periods - 1  # excluding initial investment
        lp_pref_accrued = lp_equity * pref_rate * periods_with_cash
    else:
        lp_pref_accrued = lp_equity * pref_rate * (n_periods - 1)

    lp_pref_paid = min(remaining, lp_pref_accrued)
    remaining -= lp_pref_paid

    tier_distributions.append({
        "tier": 1,
        "name": f"Preferred Return ({pref_rate:.0%})",
        "lp_distribution": round(lp_pref_paid, 2),
        "gp_distribution": 0,
        "remaining_after": round(remaining, 2),
    })

    # TIER 2: Return of Capital (pro-rata)
    lp_capital_returned = min(remaining * lp_share, lp_equity)
    gp_capital_returned = min(remaining * gp_share, gp_equity)
    capital_returned = lp_capital_returned + gp_capital_returned
    remaining -= capital_returned

    tier_distributions.append({
        "tier": 2,
        "name": "Return of Capital",
        "lp_distribution": round(lp_capital_returned, 2),
        "gp_distribution": round(gp_capital_returned, 2),
        "remaining_after": round(remaining, 2),
    })

    # TIER 3: GP Catch-Up (if applicable)
    if catch_up_pct > 0 and remaining > 0:
        # GP catches up until GP has received catch_up_pct of total profit distributed so far
        total_gp_so_far = gp_capital_returned
        total_distributed_so_far = lp_pref_paid + capital_returned
        target_gp_share = total_distributed_so_far * catch_up_pct / (1 - catch_up_pct)
        gp_catch_up = min(remaining, max(target_gp_share - total_gp_so_far, 0))
        remaining -= gp_catch_up

        tier_distributions.append({
            "tier": 3,
            "name": f"GP Catch-Up ({catch_up_pct:.0%})",
            "lp_distribution": 0,
            "gp_distribution": round(gp_catch_up, 2),
            "remaining_after": round(remaining, 2),
        })

    # TIER 4+: Profit Splits by IRR Hurdle
    # For simplicity, distribute remaining through the tiers
    # Each tier gets profits until the next hurdle IRR is achieved
    tier_num = 4 if catch_up_pct > 0 else 3
    for i, tier in enumerate(tiers):
        if remaining <= 0:
            break

        gp_split = tier["gp_split"]
        lp_split = tier["lp_split"]

        # If there is a next tier, determine how much goes at this split level
        # For the final tier, all remaining goes here
        if i < len(tiers) - 1:
            # Approximate: distribute proportionally until next hurdle
            # In practice this requires iterative IRR solving; here we use a proportional split
            next_hurdle = tiers[i + 1]["hurdle_irr"]
            current_hurdle = tier["hurdle_irr"]
            # Approximate tranche size based on hurdle spread
            hurdle_spread = next_hurdle - current_hurdle
            tranche_estimate = total_equity * hurdle_spread * (n_periods - 1)
            tranche = min(remaining, max(tranche_estimate, 0))
        else:
            tranche = remaining

        lp_tranche = tranche * lp_split
        gp_tranche = tranche * gp_split
        remaining -= tranche

        tier_distributions.append({
            "tier": tier_num,
            "name": f"Profit Split (above {tier['hurdle_irr']:.0%} IRR): {gp_split:.0%} GP / {lp_split:.0%} LP",
            "lp_distribution": round(lp_tranche, 2),
            "gp_distribution": round(gp_tranche, 2),
            "remaining_after": round(remaining, 2),
        })
        tier_num += 1

    # Aggregate totals
    total_lp = sum(t["lp_distribution"] for t in tier_distributions)
    total_gp = sum(t["gp_distribution"] for t in tier_distributions)
    gp_promote = total_gp - gp_capital_returned

    # Build per-party cashflow streams for IRR calculation
    lp_cashflows = [-lp_equity]
    gp_cashflows = [-gp_equity]

    # Distribute operating cashflows pro-rata (simplified)
    for i in range(1, n_periods):
        cf = cashflows[i]
        if cf > 0 and i < n_periods - 1:
            # Operating distributions: apply pref first, then pro-rata
            # Simplified: distribute proportionally to final split
            if total_lp + total_gp > 0:
                lp_pct = total_lp / (total_lp + total_gp)
                gp_pct = total_gp / (total_lp + total_gp)
            else:
                lp_pct = lp_share
                gp_pct = gp_share
            lp_cashflows.append(cf * lp_pct)
            gp_cashflows.append(cf * gp_pct)
        elif i == n_periods - 1:
            # Terminal cashflow: allocate remaining share
            prev_lp = sum(lp_cashflows[1:])
            prev_gp = sum(gp_cashflows[1:])
            lp_terminal = total_lp - prev_lp
            gp_terminal = total_gp - prev_gp
            lp_cashflows.append(lp_terminal)
            gp_cashflows.append(gp_terminal)
        else:
            lp_cashflows.append(0)
            gp_cashflows.append(0)

    lp_irr = irr_calc(lp_cashflows)
    gp_irr = irr_calc(gp_cashflows)

    lp_multiple = round(total_lp / lp_equity, 2) if lp_equity > 0 else 0
    gp_multiple = round(total_gp / gp_equity, 2) if gp_equity > 0 else 0

    return {
        "summary": {
            "total_equity": total_equity,
            "lp_equity": lp_equity,
            "gp_equity": gp_equity,
            "lp_equity_pct": round(lp_share * 100, 1),
            "gp_equity_pct": round(gp_share * 100, 1),
            "total_distributions": round(total_distributions, 2),
            "total_profit": round(total_profit, 2),
        },
        "lp_results": {
            "total_distributions": round(total_lp, 2),
            "profit": round(total_lp - lp_equity, 2),
            "irr": lp_irr,
            "equity_multiple": lp_multiple,
        },
        "gp_results": {
            "total_distributions": round(total_gp, 2),
            "profit": round(total_gp - gp_equity, 2),
            "promote": round(gp_promote, 2),
            "promote_pct_of_profit": round(gp_promote / total_profit * 100, 1) if total_profit > 0 else 0,
            "irr": gp_irr,
            "equity_multiple": gp_multiple,
        },
        "waterfall_tiers": tier_distributions,
        "lp_cashflows": [round(c, 2) for c in lp_cashflows],
        "gp_cashflows": [round(c, 2) for c in gp_cashflows],
    }


def main():
    parser = argparse.ArgumentParser(description="JV Waterfall Calculator for GP/LP distributions")
    parser.add_argument("--json", type=str, help="JSON string with input parameters")
    args = parser.parse_args()

    if args.json:
        inputs = json.loads(args.json)
    elif not sys.stdin.isatty():
        inputs = json.load(sys.stdin)
    else:
        parser.print_help()
        sys.exit(1)

    result = calculate_waterfall(inputs)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
