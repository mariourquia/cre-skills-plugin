#!/usr/bin/env python3
"""
Transfer Tax Calculator
========================
Calculates state and local transfer taxes for CRE transactions.
Covers all 50 states + DC with tiered rate handling for NYC mansion tax,
WA REET tiers, and similar graduated structures.

Used by: transfer-document-preparer, funds-flow-calculator, title-commitment-reviewer skills

Usage:
    python3 scripts/calculators/transfer_tax.py --json '{
        "state": "NY",
        "county": "New York",
        "purchase_price": 15000000,
        "property_type": "commercial"
    }'

    python3 scripts/calculators/transfer_tax.py --json '{
        "state": "FL",
        "purchase_price": 5000000
    }'

Output: JSON with state_tax, county_tax, total_tax, buyer_portion, seller_portion, notes.
"""

import argparse
import json
import sys
from typing import Any

# Transfer tax rates by state (rate per dollar of consideration)
# Format: {"rate": base_rate, "buyer_convention": pct_buyer_pays, "notes": str}
# Some states have tiered rates implemented in functions below.
STATE_TRANSFER_TAX = {
    "AL": {"rate": 0.0005, "buyer_convention": 0.0, "notes": "Deed tax $0.50 per $500"},
    "AK": {"rate": 0.0, "buyer_convention": 0.0, "notes": "No state transfer tax"},
    "AZ": {"rate": 0.0, "buyer_convention": 0.0, "notes": "No state transfer tax; flat $2 recording fee"},
    "AR": {"rate": 0.0033, "buyer_convention": 0.5, "notes": "$3.30 per $1,000"},
    "CA": {"rate": 0.00055, "buyer_convention": 0.5, "notes": "$0.55 per $500; split by convention; county/city may add"},
    "CO": {"rate": 0.0001, "buyer_convention": 0.5, "notes": "$0.01 per $100; minimal"},
    "CT": {"rate": 0.0075, "buyer_convention": 0.0, "notes": "0.75% seller pays; >$800K residential gets additional 0.25%"},
    "DE": {"rate": 0.04, "buyer_convention": 0.5, "notes": "4% total (2% state + 2% county); split 50/50 by convention"},
    "DC": {"rate": 0.0, "buyer_convention": 0.0, "notes": "See tiered function"},
    "FL": {"rate": 0.007, "buyer_convention": 0.0, "notes": "Doc stamps $0.70 per $100; seller pays deed stamps; buyer pays intangible tax on mortgage (0.2%)"},
    "GA": {"rate": 0.001, "buyer_convention": 0.0, "notes": "$1.00 per $1,000; seller pays by custom"},
    "HI": {"rate": 0.0, "buyer_convention": 0.0, "notes": "See tiered function"},
    "ID": {"rate": 0.0, "buyer_convention": 0.0, "notes": "No state transfer tax"},
    "IL": {"rate": 0.0005, "buyer_convention": 0.0, "notes": "$0.50 per $500; county/city may add (Chicago: $10.50 per $500)"},
    "IN": {"rate": 0.0, "buyer_convention": 0.0, "notes": "No state transfer tax"},
    "IA": {"rate": 0.0008, "buyer_convention": 0.0, "notes": "$0.80 per $500"},
    "KS": {"rate": 0.0, "buyer_convention": 0.0, "notes": "No state transfer tax"},
    "KY": {"rate": 0.001, "buyer_convention": 0.0, "notes": "$0.50 per $500"},
    "LA": {"rate": 0.0, "buyer_convention": 0.0, "notes": "No state transfer tax"},
    "ME": {"rate": 0.0044, "buyer_convention": 0.5, "notes": "$2.20 per $500; split equally"},
    "MD": {"rate": 0.005, "buyer_convention": 0.5, "notes": "0.25% state + 0.25% county (typical); split by convention"},
    "MA": {"rate": 0.00456, "buyer_convention": 0.0, "notes": "$4.56 per $1,000; seller pays"},
    "MI": {"rate": 0.0075, "buyer_convention": 0.0, "notes": "$7.50 per $1,000 (state $3.75 + county $0.55 per $500); seller pays"},
    "MN": {"rate": 0.0033, "buyer_convention": 0.0, "notes": "$3.30 per $1,000; seller pays"},
    "MS": {"rate": 0.0, "buyer_convention": 0.0, "notes": "No state transfer tax"},
    "MO": {"rate": 0.0, "buyer_convention": 0.0, "notes": "No state transfer tax; some municipalities charge"},
    "MT": {"rate": 0.0, "buyer_convention": 0.0, "notes": "No state transfer tax"},
    "NE": {"rate": 0.00225, "buyer_convention": 0.0, "notes": "$2.25 per $1,000"},
    "NV": {"rate": 0.0013, "buyer_convention": 0.0, "notes": "$1.30 per $500; seller pays (Clark County adds $0.60)"},
    "NH": {"rate": 0.015, "buyer_convention": 0.5, "notes": "$7.50 per $1,000 each (buyer and seller)"},
    "NJ": {"rate": 0.0, "buyer_convention": 0.0, "notes": "See tiered function"},
    "NM": {"rate": 0.0, "buyer_convention": 0.0, "notes": "No state transfer tax"},
    "NY": {"rate": 0.0, "buyer_convention": 0.0, "notes": "See tiered function"},
    "NC": {"rate": 0.002, "buyer_convention": 0.0, "notes": "$1.00 per $500; seller pays"},
    "ND": {"rate": 0.0, "buyer_convention": 0.0, "notes": "No state transfer tax"},
    "OH": {"rate": 0.001, "buyer_convention": 0.5, "notes": "$1.00 per $1,000; county may add $0.30-$3.00 per $1,000"},
    "OK": {"rate": 0.00075, "buyer_convention": 0.0, "notes": "$0.75 per $1,000"},
    "OR": {"rate": 0.0, "buyer_convention": 0.0, "notes": "No state transfer tax; some counties charge"},
    "PA": {"rate": 0.02, "buyer_convention": 0.5, "notes": "1% state + 1% local; split 50/50 by convention"},
    "RI": {"rate": 0.0046, "buyer_convention": 0.0, "notes": "$2.30 per $500; seller pays"},
    "SC": {"rate": 0.0037, "buyer_convention": 0.0, "notes": "$1.85 per $500; deed recording fee $1.85 per $500"},
    "SD": {"rate": 0.001, "buyer_convention": 0.0, "notes": "$0.50 per $500"},
    "TN": {"rate": 0.0037, "buyer_convention": 0.0, "notes": "$0.37 per $100"},
    "TX": {"rate": 0.0, "buyer_convention": 0.0, "notes": "No state transfer tax"},
    "UT": {"rate": 0.0, "buyer_convention": 0.0, "notes": "No state transfer tax"},
    "VT": {"rate": 0.0125, "buyer_convention": 0.5, "notes": "1.25% of value; split by convention"},
    "VA": {"rate": 0.0025, "buyer_convention": 0.0, "notes": "Grantor tax $0.50 per $500 + recordation tax; varies by locality"},
    "WA": {"rate": 0.0, "buyer_convention": 0.0, "notes": "See tiered REET function"},
    "WV": {"rate": 0.0033, "buyer_convention": 0.5, "notes": "$1.65 per $500 each (seller and buyer)"},
    "WI": {"rate": 0.003, "buyer_convention": 0.0, "notes": "$0.30 per $100; seller pays"},
    "WY": {"rate": 0.0, "buyer_convention": 0.0, "notes": "No state transfer tax"},
}


def calc_ny_transfer_tax(price: float, property_type: str, county: str | None) -> dict[str, Any]:
    """
    New York transfer tax calculation.
    State: 0.4% of consideration ($2 per $500)
    NYC (if applicable):
      - Commercial: 1.425% if > $500K; 1% if <= $500K
      - Residential: mansion tax tiers above $1M
    """
    # State tax
    state_tax = price * 0.004

    # NYC additional tax
    nyc_counties = {"new york", "kings", "queens", "bronx", "richmond"}
    county_lower = (county or "").lower().strip()

    city_tax = 0.0
    mansion_tax = 0.0
    notes = "NY State transfer tax: 0.4%"

    if county_lower in nyc_counties:
        if property_type == "residential":
            if price <= 500000:
                city_tax = price * 0.01
            else:
                city_tax = price * 0.01425

            # Mansion tax (buyer pays) -- tiered for residential > $1M
            if price >= 25000000:
                mansion_tax = price * 0.0390
            elif price >= 20000000:
                mansion_tax = price * 0.0365
            elif price >= 15000000:
                mansion_tax = price * 0.0340
            elif price >= 10000000:
                mansion_tax = price * 0.0315
            elif price >= 5000000:
                mansion_tax = price * 0.0225
            elif price >= 3000000:
                mansion_tax = price * 0.0200
            elif price >= 2000000:
                mansion_tax = price * 0.0175
            elif price >= 1000000:
                mansion_tax = price * 0.0100
        else:
            # Commercial
            if price <= 500000:
                city_tax = price * 0.01
            else:
                city_tax = price * 0.01425

        notes += f"; NYC transfer tax: {'1.425%' if price > 500000 else '1.0%'}"
        if mansion_tax > 0:
            notes += f"; NYC mansion tax: ${mansion_tax:,.0f} (buyer)"

    return {
        "state_tax": round(state_tax, 2),
        "city_tax": round(city_tax, 2),
        "mansion_tax": round(mansion_tax, 2),
        "total_tax": round(state_tax + city_tax + mansion_tax, 2),
        "buyer_portion": round(mansion_tax, 2),
        "seller_portion": round(state_tax + city_tax, 2),
        "notes": notes,
    }


def calc_nj_transfer_tax(price: float) -> dict[str, Any]:
    """
    New Jersey Realty Transfer Fee -- graduated rates.
    Seller pays base fee; buyer pays 1% mansion tax on > $1M.
    """
    # NJ graduated fee schedule (seller)
    if price <= 150000:
        fee_rate = 0.002
    elif price <= 200000:
        fee_rate = 0.0033
    elif price <= 350000:
        fee_rate = 0.00405
    elif price <= 550000:
        fee_rate = 0.00505
    elif price <= 850000:
        fee_rate = 0.00605
    elif price <= 1000000:
        fee_rate = 0.00705
    else:
        fee_rate = 0.00805

    seller_fee = price * fee_rate

    # Mansion tax on > $1M (buyer pays)
    mansion_tax = price * 0.01 if price > 1000000 else 0

    return {
        "state_tax": round(seller_fee, 2),
        "city_tax": 0,
        "mansion_tax": round(mansion_tax, 2),
        "total_tax": round(seller_fee + mansion_tax, 2),
        "buyer_portion": round(mansion_tax, 2),
        "seller_portion": round(seller_fee, 2),
        "notes": f"NJ graduated fee at {fee_rate:.3%}" + ("; buyer mansion tax 1%" if mansion_tax > 0 else ""),
    }


def calc_dc_transfer_tax(price: float, property_type: str) -> dict[str, Any]:
    """
    DC transfer and recordation taxes.
    Deed transfer tax: 1.1% (residential) or 1.1% (commercial; 2.9% if > $400K)
    Deed recordation tax: 1.1% (residential) or 1.1% (commercial; 2.9% if > $400K)
    Split: seller pays transfer, buyer pays recordation by convention.
    """
    if property_type == "residential" or price <= 400000:
        transfer_rate = 0.011
        record_rate = 0.011
    else:
        transfer_rate = 0.029
        record_rate = 0.029

    transfer_tax = price * transfer_rate
    recordation_tax = price * record_rate

    return {
        "state_tax": round(transfer_tax + recordation_tax, 2),
        "city_tax": 0,
        "mansion_tax": 0,
        "total_tax": round(transfer_tax + recordation_tax, 2),
        "buyer_portion": round(recordation_tax, 2),
        "seller_portion": round(transfer_tax, 2),
        "notes": f"DC transfer {transfer_rate:.1%} + recordation {record_rate:.1%}",
    }


def calc_wa_reet(price: float) -> dict[str, Any]:
    """
    Washington Real Estate Excise Tax (REET) -- tiered.
    Effective 1/1/2023: graduated rate.
    """
    tiers = [
        (525000, 0.016),
        (1525000, 0.018),    # $525K to $1.525M
        (3025000, 0.0275),   # $1.525M to $3.025M
        (float("inf"), 0.03), # above $3.025M
    ]

    tax = 0.0
    prev_limit = 0
    for limit, rate in tiers:
        taxable = min(price, limit) - prev_limit
        if taxable <= 0:
            break
        tax += taxable * rate
        prev_limit = limit

    return {
        "state_tax": round(tax, 2),
        "city_tax": 0,
        "mansion_tax": 0,
        "total_tax": round(tax, 2),
        "buyer_portion": 0,
        "seller_portion": round(tax, 2),
        "notes": f"WA REET graduated tiers; seller pays",
    }


def calc_hi_transfer_tax(price: float) -> dict[str, Any]:
    """Hawaii conveyance tax -- tiered rates."""
    tiers = [
        (600000, 0.0010),
        (1000000, 0.0020),
        (2000000, 0.0030),
        (4000000, 0.0040),
        (6000000, 0.0050),
        (10000000, 0.0060),
        (float("inf"), 0.0070),
    ]

    tax = 0.0
    prev_limit = 0
    for limit, rate in tiers:
        taxable = min(price, limit) - prev_limit
        if taxable <= 0:
            break
        tax += taxable * rate
        prev_limit = limit

    return {
        "state_tax": round(tax, 2),
        "city_tax": 0,
        "mansion_tax": 0,
        "total_tax": round(tax, 2),
        "buyer_portion": 0,
        "seller_portion": round(tax, 2),
        "notes": "HI conveyance tax graduated tiers; seller pays",
    }


def calculate_transfer_tax(inputs: dict[str, Any]) -> dict[str, Any]:
    """Main calculation entry point."""
    state = inputs["state"].upper()
    county = inputs.get("county")
    price = inputs["purchase_price"]
    ptype = inputs.get("property_type", "commercial").lower()

    # Handle states with tiered/special calculations
    if state == "NY":
        result = calc_ny_transfer_tax(price, ptype, county)
    elif state == "NJ":
        result = calc_nj_transfer_tax(price)
    elif state == "DC":
        result = calc_dc_transfer_tax(price, ptype)
    elif state == "WA":
        result = calc_wa_reet(price)
    elif state == "HI":
        result = calc_hi_transfer_tax(price)
    else:
        # Standard flat-rate states
        info = STATE_TRANSFER_TAX.get(state, {"rate": 0.0, "buyer_convention": 0.0, "notes": "State not found"})
        total = round(price * info["rate"], 2)
        buyer = round(total * info["buyer_convention"], 2)
        seller = round(total * (1 - info["buyer_convention"]), 2)

        result = {
            "state_tax": total,
            "city_tax": 0,
            "mansion_tax": 0,
            "total_tax": total,
            "buyer_portion": buyer,
            "seller_portion": seller,
            "notes": info["notes"],
        }

    result["state"] = state
    result["county"] = county
    result["purchase_price"] = price
    result["property_type"] = ptype
    result["effective_rate_pct"] = round(result["total_tax"] / price * 100, 3) if price > 0 else 0

    return result


def main():
    parser = argparse.ArgumentParser(description="CRE Transfer Tax Calculator (all 50 states + DC)")
    parser.add_argument("--json", type=str, help="JSON string with input parameters")
    args = parser.parse_args()

    if args.json:
        inputs = json.loads(args.json)
    elif not sys.stdin.isatty():
        inputs = json.load(sys.stdin)
    else:
        parser.print_help()
        sys.exit(1)

    result = calculate_transfer_tax(inputs)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
