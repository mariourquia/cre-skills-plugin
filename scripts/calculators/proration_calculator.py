#!/usr/bin/env python3
"""
CRE Proration Calculator
=========================
Calculates per diem prorations for property tax, rent, insurance, and CAM/OpEx
at a commercial real estate closing. Supports actual/365, actual/360, and 30/360
conventions.

Used by: funds-flow-calculator skill

Usage:
    python3 scripts/calculators/proration_calculator.py --json '{
        "closing_date": "2026-03-15",
        "annual_tax": 180000,
        "tax_year_start": "2026-01-01",
        "tax_paid_through": "2025-12-31",
        "monthly_rent": 125000,
        "rent_collected_through": "2026-03-31",
        "insurance_annual": 42000,
        "insurance_paid_through": "2026-06-30",
        "proration_method": "actual_365"
    }'

    # Or pipe JSON via stdin:
    echo '{"closing_date": "2026-03-15", "annual_tax": 180000}' | python3 scripts/calculators/proration_calculator.py

Output: JSON with buyer_credit, seller_credit, per_diem_amounts, and line-item detail.
"""

import argparse
import json
import sys
from datetime import date, datetime
from typing import Any


def parse_date(d: str) -> date:
    """Parse ISO date string to date object."""
    return datetime.strptime(d, "%Y-%m-%d").date()


def days_in_year(d: date) -> int:
    """Return 366 if leap year, else 365."""
    return 366 if (d.year % 4 == 0 and (d.year % 100 != 0 or d.year % 400 == 0)) else 365


def days_between(start: date, end: date, method: str) -> int:
    """
    Calculate days between two dates using the specified convention.
    'start' is inclusive, 'end' is exclusive (closing date convention:
    seller owns through day before closing, buyer owns from closing date).
    """
    if method == "30_360":
        d1 = min(start.day, 30)
        d2 = min(end.day, 30) if d1 == 30 else end.day
        m1 = start.month
        m2 = end.month
        y1 = start.year
        y2 = end.year
        return 360 * (y2 - y1) + 30 * (m2 - m1) + (d2 - d1)
    else:
        return (end - start).days


def divisor_for_method(method: str, ref_date: date) -> int:
    """Return the annual divisor for the proration method."""
    if method == "30_360":
        return 360
    elif method == "actual_360":
        return 360
    else:  # actual_365
        return days_in_year(ref_date)


def prorate_property_tax(
    closing_date: date,
    annual_tax: float,
    tax_year_start: date,
    tax_paid_through: date | None,
    method: str,
) -> dict[str, Any]:
    """
    Calculate property tax proration.

    Convention: taxes in arrears -- seller owes from tax_year_start through
    day before closing. Seller credits buyer for the unpaid portion.
    If taxes are paid in advance past the closing date, buyer credits seller.
    """
    tax_year_end = date(tax_year_start.year, 12, 31)
    divisor = divisor_for_method(method, closing_date)
    per_diem = annual_tax / divisor

    # Seller's period: tax_year_start through closing_date - 1 day
    seller_days = days_between(tax_year_start, closing_date, method)
    seller_share = round(per_diem * seller_days, 2)

    # Buyer's period: closing_date through tax_year_end
    buyer_days = days_between(closing_date, date(tax_year_end.year + 1, 1, 1), method)
    if method == "30_360":
        buyer_days = 360 - seller_days
    else:
        buyer_days = divisor - seller_days
    buyer_share = round(per_diem * buyer_days, 2)

    # Determine credit direction based on payment status
    if tax_paid_through is None or tax_paid_through < tax_year_start:
        # Taxes unpaid for current year -- seller credits buyer for seller's period
        credit_direction = "seller_credits_buyer"
        buyer_credit = seller_share
        seller_credit = 0.0
    elif tax_paid_through >= closing_date:
        # Taxes paid through or past closing -- buyer credits seller for buyer's period
        credit_direction = "buyer_credits_seller"
        buyer_credit = 0.0
        seller_credit = buyer_share
    else:
        # Partially paid -- seller owes from paid_through+1 to closing
        unpaid_days = days_between(
            date(tax_paid_through.year, tax_paid_through.month, tax_paid_through.day),
            closing_date,
            method,
        )
        credit_direction = "seller_credits_buyer"
        buyer_credit = round(per_diem * unpaid_days, 2)
        seller_credit = 0.0

    return {
        "item": "property_tax",
        "annual_amount": annual_tax,
        "per_diem": round(per_diem, 2),
        "seller_days": seller_days,
        "buyer_days": buyer_days,
        "seller_share": seller_share,
        "buyer_share": buyer_share,
        "credit_direction": credit_direction,
        "buyer_credit": buyer_credit,
        "seller_credit": seller_credit,
    }


def prorate_rent(
    closing_date: date,
    monthly_rent: float,
    rent_collected_through: date | None,
    method: str,
) -> dict[str, Any]:
    """
    Calculate rent proration.

    Convention: rent is collected in advance. If rent for closing month is
    already collected, seller credits buyer for the post-closing portion.
    """
    # Days in closing month
    month_start = closing_date.replace(day=1)
    if closing_date.month == 12:
        next_month = date(closing_date.year + 1, 1, 1)
    else:
        next_month = closing_date.replace(month=closing_date.month + 1, day=1)

    if method == "30_360":
        days_in_month = 30
    else:
        days_in_month = (next_month - month_start).days

    daily_rent = monthly_rent / days_in_month

    # Seller's days: 1st through closing_date - 1
    seller_days = closing_date.day - 1
    seller_share = round(daily_rent * seller_days, 2)

    # Buyer's days: closing_date through end of month
    buyer_days = days_in_month - seller_days
    buyer_share = round(daily_rent * buyer_days, 2)

    # If rent is collected through end of closing month or later,
    # seller credits buyer for buyer's portion
    collected = rent_collected_through is not None and rent_collected_through >= closing_date
    if collected:
        credit_direction = "seller_credits_buyer"
        buyer_credit = buyer_share
        seller_credit = 0.0
    else:
        # Rent not yet collected -- buyer collects and keeps
        credit_direction = "no_proration_rent_uncollected"
        buyer_credit = 0.0
        seller_credit = 0.0

    return {
        "item": "rent",
        "monthly_rent": monthly_rent,
        "daily_rent": round(daily_rent, 2),
        "days_in_month": days_in_month,
        "seller_days": seller_days,
        "buyer_days": buyer_days,
        "seller_share": seller_share,
        "buyer_share": buyer_share,
        "credit_direction": credit_direction,
        "buyer_credit": buyer_credit,
        "seller_credit": seller_credit,
    }


def prorate_insurance(
    closing_date: date,
    insurance_annual: float,
    insurance_paid_through: date | None,
    method: str,
) -> dict[str, Any]:
    """
    Calculate insurance proration.

    Convention: insurance is typically prepaid annually. If paid through a date
    past closing, buyer credits seller for the post-closing prepaid portion.
    """
    divisor = divisor_for_method(method, closing_date)
    per_diem = insurance_annual / divisor

    if insurance_paid_through is None or insurance_paid_through < closing_date:
        # Insurance not prepaid past closing -- no proration
        return {
            "item": "insurance",
            "annual_amount": insurance_annual,
            "per_diem": round(per_diem, 2),
            "credit_direction": "no_proration_not_prepaid",
            "buyer_credit": 0.0,
            "seller_credit": 0.0,
            "prepaid_days_remaining": 0,
        }

    # Seller prepaid past closing -- buyer credits seller
    prepaid_days = days_between(closing_date, insurance_paid_through, method)
    seller_credit = round(per_diem * prepaid_days, 2)

    return {
        "item": "insurance",
        "annual_amount": insurance_annual,
        "per_diem": round(per_diem, 2),
        "credit_direction": "buyer_credits_seller",
        "buyer_credit": 0.0,
        "seller_credit": seller_credit,
        "prepaid_days_remaining": prepaid_days,
    }


def calculate_prorations(inputs: dict[str, Any]) -> dict[str, Any]:
    """Main calculation entry point."""
    closing_date = parse_date(inputs["closing_date"])
    method = inputs.get("proration_method", "actual_365")

    results = {"closing_date": inputs["closing_date"], "proration_method": method, "line_items": []}
    total_buyer_credit = 0.0
    total_seller_credit = 0.0

    # Property tax proration
    if "annual_tax" in inputs and inputs["annual_tax"]:
        tax_year_start = parse_date(inputs.get("tax_year_start", f"{closing_date.year}-01-01"))
        tax_paid_through = (
            parse_date(inputs["tax_paid_through"]) if inputs.get("tax_paid_through") else None
        )
        tax_result = prorate_property_tax(
            closing_date, inputs["annual_tax"], tax_year_start, tax_paid_through, method
        )
        results["line_items"].append(tax_result)
        total_buyer_credit += tax_result["buyer_credit"]
        total_seller_credit += tax_result["seller_credit"]

    # Rent proration
    if "monthly_rent" in inputs and inputs["monthly_rent"]:
        rent_collected_through = (
            parse_date(inputs["rent_collected_through"])
            if inputs.get("rent_collected_through")
            else None
        )
        rent_result = prorate_rent(closing_date, inputs["monthly_rent"], rent_collected_through, method)
        results["line_items"].append(rent_result)
        total_buyer_credit += rent_result["buyer_credit"]
        total_seller_credit += rent_result["seller_credit"]

    # Insurance proration
    if "insurance_annual" in inputs and inputs["insurance_annual"]:
        insurance_paid_through = (
            parse_date(inputs["insurance_paid_through"])
            if inputs.get("insurance_paid_through")
            else None
        )
        ins_result = prorate_insurance(
            closing_date, inputs["insurance_annual"], insurance_paid_through, method
        )
        results["line_items"].append(ins_result)
        total_buyer_credit += ins_result["buyer_credit"]
        total_seller_credit += ins_result["seller_credit"]

    # CAM/OpEx proration (treated like property tax -- arrears)
    if "cam_annual" in inputs and inputs["cam_annual"]:
        cam_year_start = parse_date(inputs.get("cam_year_start", f"{closing_date.year}-01-01"))
        cam_paid_through = (
            parse_date(inputs["cam_paid_through"]) if inputs.get("cam_paid_through") else None
        )
        cam_result = prorate_property_tax(
            closing_date, inputs["cam_annual"], cam_year_start, cam_paid_through, method
        )
        cam_result["item"] = "cam_opex"
        results["line_items"].append(cam_result)
        total_buyer_credit += cam_result["buyer_credit"]
        total_seller_credit += cam_result["seller_credit"]

    results["total_buyer_credit"] = round(total_buyer_credit, 2)
    results["total_seller_credit"] = round(total_seller_credit, 2)
    results["net_proration"] = round(total_buyer_credit - total_seller_credit, 2)
    results["net_direction"] = (
        "buyer_net_credit"
        if results["net_proration"] > 0
        else "seller_net_credit" if results["net_proration"] < 0 else "even"
    )

    return results


def main():
    parser = argparse.ArgumentParser(
        description="CRE Proration Calculator for closing settlements"
    )
    parser.add_argument(
        "--json",
        type=str,
        help="JSON string with input parameters",
    )
    args = parser.parse_args()

    if args.json:
        inputs = json.loads(args.json)
    elif not sys.stdin.isatty():
        inputs = json.load(sys.stdin)
    else:
        parser.print_help()
        sys.exit(1)

    result = calculate_prorations(inputs)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
