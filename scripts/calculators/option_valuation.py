#!/usr/bin/env python3
"""
Lease Option Valuation
======================
Calculates termination fees, renewal option cap rate impact, and compares
conservative/moderate/aggressive option packages by NPV impact.

Used by: lease-option-structurer skill

Usage:
    python3 scripts/calculators/option_valuation.py --json '{
        "ti_total": 250000,
        "ti_amortization_months": 120,
        "lc_total": 95000,
        "lc_amortization_months": 120,
        "months_remaining": 72,
        "market_rent_psf": 35.00,
        "sf": 10000,
        "expected_vacancy_months": 6,
        "releasing_cost_psf": 30.00,
        "discount_rate": 0.07,
        "noi": 2000000,
        "cap_rate": 0.055,
        "tenant_pct_of_nra": 0.25,
        "lease_term_years": 10,
        "remaining_term_years": 6
    }'

Output: JSON with termination_fee, fee_components, cap_rate_impact_bps,
        package_comparison (conservative/moderate/aggressive).
"""

import argparse
import json
import sys
from typing import Any


def termination_fee(inputs: dict[str, Any]) -> dict[str, Any]:
    """
    Calculate minimum acceptable termination fee.

    Fee = max(hard_cost_recovery, npv_breakeven)

    hard_cost_recovery = unamortized_TI + unamortized_LC + re_leasing_cost
    npv_breakeven = NPV(remaining rent) - NPV(projected re-lease income)
    """
    ti_total = inputs.get("ti_total", 0)
    ti_amort = inputs.get("ti_amortization_months", 120)
    lc_total = inputs.get("lc_total", 0)
    lc_amort = inputs.get("lc_amortization_months", 120)
    months_remaining = inputs.get("months_remaining", 60)

    market_rent_psf = inputs.get("market_rent_psf", 30)
    sf = inputs.get("sf", 10000)
    vacancy_months = inputs.get("expected_vacancy_months", 6)
    releasing_cost_psf = inputs.get("releasing_cost_psf", 25)
    discount_rate = inputs.get("discount_rate", 0.07)

    # Unamortized TI
    months_elapsed_ti = ti_amort - months_remaining
    if months_elapsed_ti < 0:
        months_elapsed_ti = 0
    unamortized_ti = ti_total * (months_remaining / ti_amort) if ti_amort > 0 else 0
    unamortized_ti = max(unamortized_ti, 0)

    # Unamortized LC
    months_elapsed_lc = lc_amort - months_remaining
    if months_elapsed_lc < 0:
        months_elapsed_lc = 0
    unamortized_lc = lc_total * (months_remaining / lc_amort) if lc_amort > 0 else 0
    unamortized_lc = max(unamortized_lc, 0)

    # Vacancy cost (NPV of carrying cost during vacancy)
    monthly_market_rent = market_rent_psf * sf / 12
    vacancy_cost_npv = 0
    monthly_rate = discount_rate / 12
    for m in range(vacancy_months):
        vacancy_cost_npv += monthly_market_rent / (1 + monthly_rate) ** (m + 1)

    # Re-leasing cost (new TI + new LC for replacement tenant)
    releasing_cost = releasing_cost_psf * sf

    # Hard cost recovery
    hard_cost_recovery = unamortized_ti + unamortized_lc + vacancy_cost_npv + releasing_cost

    # NPV breakeven: remaining rent stream vs projected re-lease income
    # Remaining rent (current tenant) -- using market rent as proxy
    remaining_rent_npv = 0
    for m in range(months_remaining):
        remaining_rent_npv += monthly_market_rent / (1 + monthly_rate) ** (m + 1)

    # Projected re-lease income (after vacancy)
    release_months = months_remaining - vacancy_months
    release_npv = 0
    for m in range(max(release_months, 0)):
        t = vacancy_months + m + 1
        release_npv += monthly_market_rent / (1 + monthly_rate) ** t

    npv_breakeven = remaining_rent_npv - release_npv

    # Minimum termination fee = max of the two methods
    min_fee = max(hard_cost_recovery, npv_breakeven)

    return {
        "unamortized_ti": round(unamortized_ti, 2),
        "unamortized_lc": round(unamortized_lc, 2),
        "vacancy_cost_npv": round(vacancy_cost_npv, 2),
        "releasing_cost": round(releasing_cost, 2),
        "hard_cost_recovery": round(hard_cost_recovery, 2),
        "npv_breakeven": round(npv_breakeven, 2),
        "minimum_termination_fee": round(min_fee, 2),
        "fee_method": "hard_cost_recovery" if hard_cost_recovery >= npv_breakeven else "npv_breakeven",
    }


def cap_rate_impact(inputs: dict[str, Any]) -> dict[str, Any]:
    """
    Calculate cap rate impact of various option types.

    Termination option on >10% of NRA: +10-25 bps
    Below-market renewal option: +5-15 bps
    Long-term renewal commitment: -5-10 bps
    ROFR on building sale: +5-15 bps
    """
    noi = inputs.get("noi", 2000000)
    cap_rate = inputs.get("cap_rate", 0.055)
    tenant_pct = inputs.get("tenant_pct_of_nra", 0.20)
    remaining_years = inputs.get("remaining_term_years", 5)

    base_value = noi / cap_rate

    impacts = {}

    # Termination option impact
    if tenant_pct > 0.10:
        term_bps = round(10 + (tenant_pct - 0.10) * 100, 0)  # Scale with tenant size
        term_bps = min(term_bps, 25)
    else:
        term_bps = 5
    impacts["termination_option"] = {
        "bps": term_bps,
        "adjusted_cap": round(cap_rate + term_bps / 10000, 4),
        "value_impact": round(noi / (cap_rate + term_bps / 10000) - base_value, 0),
    }

    # Renewal commitment impact (positive -- value accretive)
    renewal_bps = -5 if remaining_years < 5 else -10
    impacts["renewal_commitment"] = {
        "bps": renewal_bps,
        "adjusted_cap": round(cap_rate + renewal_bps / 10000, 4),
        "value_impact": round(noi / (cap_rate + renewal_bps / 10000) - base_value, 0),
    }

    # Below-market renewal impact
    impacts["below_market_renewal"] = {
        "bps": 10,
        "adjusted_cap": round(cap_rate + 10 / 10000, 4),
        "value_impact": round(noi / (cap_rate + 10 / 10000) - base_value, 0),
    }

    # Contraction right impact
    contraction_bps = round(10 + (tenant_pct * 50), 0)
    contraction_bps = min(contraction_bps, 20)
    impacts["contraction_right"] = {
        "bps": contraction_bps,
        "adjusted_cap": round(cap_rate + contraction_bps / 10000, 4),
        "value_impact": round(noi / (cap_rate + contraction_bps / 10000) - base_value, 0),
    }

    # ROFR on sale impact
    impacts["rofr_on_sale"] = {
        "bps": 10,
        "adjusted_cap": round(cap_rate + 10 / 10000, 4),
        "value_impact": round(noi / (cap_rate + 10 / 10000) - base_value, 0),
    }

    return {
        "base_value": round(base_value, 0),
        "base_cap_rate": cap_rate,
        "noi": noi,
        "impacts_by_option_type": impacts,
    }


def package_comparison(inputs: dict[str, Any]) -> dict[str, Any]:
    """
    Compare three option packages: conservative, moderate, aggressive.
    Each package is a combination of options with cumulative cap rate impact.
    """
    noi = inputs.get("noi", 2000000)
    cap_rate = inputs.get("cap_rate", 0.055)
    tenant_pct = inputs.get("tenant_pct_of_nra", 0.20)
    base_value = noi / cap_rate

    packages = {}

    # Conservative: renewal only (2 x 5yr at FMV)
    cons_bps = -8  # Two renewals compress cap slightly
    cons_cap = cap_rate + cons_bps / 10000
    cons_value = noi / cons_cap
    packages["conservative"] = {
        "options_included": ["2x 5-yr renewal at FMV", "ROFO on adjacent space"],
        "options_excluded": ["termination", "contraction", "purchase option", "ROFR"],
        "net_cap_rate_impact_bps": cons_bps,
        "adjusted_cap_rate": round(cons_cap, 4),
        "adjusted_value": round(cons_value, 0),
        "value_delta": round(cons_value - base_value, 0),
        "value_at_risk": 0,
        "best_for": "Landlord market, lender-constrained, or anchor replacement",
    }

    # Moderate: renewal + contraction + ROFO
    mod_bps = -8 + 12 + 0  # renewal benefit, contraction cost, ROFO neutral
    mod_cap = cap_rate + mod_bps / 10000
    mod_value = noi / mod_cap
    # Value at risk = if contraction exercised
    contraction_noi_loss = noi * tenant_pct * 0.15  # 15% of tenant's space
    var_mod = round(contraction_noi_loss / mod_cap, 0)
    packages["moderate"] = {
        "options_included": [
            "2x 5-yr renewal at FMV",
            "1x contraction at mid-term (12mo notice, fee = unamortized TI+LC+3mo rent)",
            "ROFO on adjacent space",
        ],
        "options_excluded": ["termination", "purchase option"],
        "net_cap_rate_impact_bps": mod_bps,
        "adjusted_cap_rate": round(mod_cap, 4),
        "adjusted_value": round(mod_value, 0),
        "value_delta": round(mod_value - base_value, 0),
        "value_at_risk": var_mod,
        "best_for": "Balanced market, creditworthy tenants, standard new leases",
    }

    # Aggressive: full option stack
    agg_bps = -8 + 12 + 20 + 10  # renewal, contraction, termination, ROFR
    agg_cap = cap_rate + agg_bps / 10000
    agg_value = noi / agg_cap
    # Value at risk = termination scenario
    term_noi_loss = noi * tenant_pct
    var_agg = round(term_noi_loss / agg_cap, 0)
    packages["aggressive"] = {
        "options_included": [
            "3x 5-yr renewal at hybrid FMV (floor + ceiling)",
            "1x contraction at yr 5 (12mo notice, fee = unamortized TI+LC only)",
            "1x termination at yr 7 (18mo notice, full fee)",
            "ROFO + ROFR on adjacent space",
            "Purchase option at appraised FMV in final 2 years",
        ],
        "options_excluded": [],
        "net_cap_rate_impact_bps": agg_bps,
        "adjusted_cap_rate": round(agg_cap, 4),
        "adjusted_value": round(agg_value, 0),
        "value_delta": round(agg_value - base_value, 0),
        "value_at_risk": var_agg,
        "best_for": "Tenant market, high-vacancy, trophy tenant retention",
    }

    return {
        "base_value": round(base_value, 0),
        "packages": packages,
    }


def calculate_option_valuation(inputs: dict[str, Any]) -> dict[str, Any]:
    """Main calculation entry point."""
    result = {}

    # Termination fee calculation
    result["termination_fee"] = termination_fee(inputs)

    # Cap rate impact analysis
    result["cap_rate_impact"] = cap_rate_impact(inputs)

    # Package comparison
    result["package_comparison"] = package_comparison(inputs)

    return result


def main():
    parser = argparse.ArgumentParser(description="Lease Option Valuation for CRE")
    parser.add_argument("--json", type=str, help="JSON string with input parameters")
    args = parser.parse_args()

    if args.json:
        inputs = json.loads(args.json)
    elif not sys.stdin.isatty():
        inputs = json.load(sys.stdin)
    else:
        parser.print_help()
        sys.exit(1)

    result = calculate_option_valuation(inputs)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
