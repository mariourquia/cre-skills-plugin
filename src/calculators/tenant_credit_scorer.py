#!/usr/bin/env python3
"""
Tenant Credit Scorer
====================
Calculates HHI concentration index, WALT-weighted credit score, expected annual
loss per tenant, and occupancy cost ratios for a commercial property rent roll.

Used by: tenant-credit-analyzer skill

Usage:
    python3 scripts/calculators/tenant_credit_scorer.py --json '{
        "tenants": [
            {
                "name": "Walgreens",
                "annual_rent": 378000,
                "sf": 14700,
                "lease_remaining_years": 6.5,
                "credit_rating": "Baa2",
                "revenue": 2500000,
                "property_type": "retail"
            },
            {
                "name": "Local Restaurant",
                "annual_rent": 128000,
                "sf": 3200,
                "lease_remaining_years": 1.5,
                "credit_rating": null,
                "revenue": 850000,
                "property_type": "retail"
            }
        ]
    }'

Output: JSON with hhi, walt, walt_weighted_score, expected_loss_by_tenant,
        ocr_by_tenant, concentration_flags.
"""

import argparse
import json
import sys
from typing import Any

# Default probability tables (5-year cumulative)
# Based on Moody's/S&P historical default studies
DEFAULT_PROBABILITY_5YR = {
    # S&P / Fitch ratings
    "AAA": 0.0007, "AA+": 0.0010, "AA": 0.0015, "AA-": 0.0020,
    "A+": 0.0030, "A": 0.0040, "A-": 0.0055,
    "BBB+": 0.0080, "BBB": 0.0110, "BBB-": 0.0150,
    "BB+": 0.0400, "BB": 0.0600, "BB-": 0.0800,
    "B+": 0.1100, "B": 0.1500, "B-": 0.2000,
    "CCC+": 0.3000, "CCC": 0.4200, "CCC-": 0.5000,
    # Moody's ratings
    "Aaa": 0.0007, "Aa1": 0.0010, "Aa2": 0.0015, "Aa3": 0.0020,
    "A1": 0.0030, "A2": 0.0040, "A3": 0.0055,
    "Baa1": 0.0080, "Baa2": 0.0110, "Baa3": 0.0150,
    "Ba1": 0.0400, "Ba2": 0.0600, "Ba3": 0.0800,
    "B1": 0.1100, "B2": 0.1500, "B3": 0.2000,
    "Caa1": 0.3000, "Caa2": 0.4200, "Caa3": 0.5000,
    # Shadow ratings for unrated tenants
    "Shadow_A": 0.0040, "Shadow_B": 0.0800,
    "Shadow_C": 0.2500, "Shadow_D": 0.4500,
    # Unrated / no data -- conservative
    "NR": 0.4500,
}

# Recovery rate assumptions by property type
RECOVERY_RATES = {
    "retail_ig": 0.75,
    "retail_hy": 0.45,
    "retail_nr": 0.35,
    "office_ig": 0.65,
    "office_hy": 0.50,
    "office_nr": 0.40,
    "industrial_ig": 0.75,
    "industrial_hy": 0.60,
    "industrial_nr": 0.50,
}

# Credit score mapping by tier
TIER_SCORES = {
    "A": 90,
    "Near_IG": 70,
    "B": 55,
    "C": 35,
    "D": 15,
}

# OCR flag thresholds by property type
OCR_THRESHOLDS = {
    "retail": 0.12,
    "restaurant": 0.10,
    "office": 0.15,
    "industrial": 0.08,
}


def get_credit_tier(rating: str | None) -> str:
    """Map a credit rating to a tier (A, Near_IG, B, C, D)."""
    if rating is None or rating == "" or rating == "NR":
        return "D"

    ig_ratings = {
        "AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-",
        "Aaa", "Aa1", "Aa2", "Aa3", "A1", "A2", "A3", "Baa1", "Baa2", "Baa3",
    }
    near_ig_ratings = {
        "BB+", "BB", "Ba1", "Ba2",
    }
    spec_b_ratings = {
        "BB-", "Ba3",
    }

    if rating in ig_ratings:
        return "A"
    elif rating in near_ig_ratings:
        return "Near_IG"
    elif rating in spec_b_ratings:
        return "B"
    elif rating.startswith("Shadow_"):
        tier_map = {"Shadow_A": "A", "Shadow_B": "B", "Shadow_C": "C", "Shadow_D": "D"}
        return tier_map.get(rating, "D")
    else:
        # B-range or lower
        return "C" if rating in DEFAULT_PROBABILITY_5YR else "D"


def get_default_probability(rating: str | None) -> float:
    """Get 5-year cumulative default probability for a rating."""
    if rating is None or rating == "":
        return DEFAULT_PROBABILITY_5YR["NR"]
    return DEFAULT_PROBABILITY_5YR.get(rating, DEFAULT_PROBABILITY_5YR["NR"])


def get_recovery_rate(property_type: str, tier: str) -> float:
    """Get recovery rate based on property type and credit tier."""
    ptype = property_type.lower()
    if ptype not in ("retail", "office", "industrial"):
        ptype = "retail"  # default

    if tier == "A":
        return RECOVERY_RATES.get(f"{ptype}_ig", 0.50)
    elif tier in ("Near_IG", "B"):
        return RECOVERY_RATES.get(f"{ptype}_hy", 0.45)
    else:
        return RECOVERY_RATES.get(f"{ptype}_nr", 0.35)


def calculate_tenant_credit(inputs: dict[str, Any]) -> dict[str, Any]:
    """Main calculation entry point."""
    tenants = inputs["tenants"]
    total_rent = sum(t["annual_rent"] for t in tenants)

    if total_rent == 0:
        return {"error": "Total rent is zero -- cannot compute metrics."}

    # --- HHI Concentration Index ---
    hhi = 0.0
    for t in tenants:
        share = t["annual_rent"] / total_rent
        hhi += (share ** 2) * 10000
    hhi = round(hhi, 0)

    if hhi < 1500:
        hhi_interpretation = "Diversified -- low concentration risk"
    elif hhi < 2500:
        hhi_interpretation = "Moderate concentration -- monitor top tenants"
    elif hhi < 5000:
        hhi_interpretation = "High concentration -- significant single-tenant dependency"
    else:
        hhi_interpretation = "Dominant tenant -- underwrite as effectively single-tenant"

    # --- WALT ---
    weighted_term_sum = sum(t["annual_rent"] * t["lease_remaining_years"] for t in tenants)
    walt = round(weighted_term_sum / total_rent, 2) if total_rent > 0 else 0

    # --- WALT-Weighted Credit Score ---
    tenant_results = []
    total_score_weighted = 0.0
    total_rent_term = 0.0

    for t in tenants:
        tier = get_credit_tier(t.get("credit_rating"))
        score = TIER_SCORES.get(tier, 15)
        rent = t["annual_rent"]
        term = t["lease_remaining_years"]
        rent_term = rent * term
        score_weighted = rent_term * score

        total_score_weighted += score_weighted
        total_rent_term += rent_term

        # Default probability and expected loss
        pd = get_default_probability(t.get("credit_rating"))
        ptype = t.get("property_type", "retail")
        recovery = get_recovery_rate(ptype, tier)
        lgd = 1 - recovery
        # EAD = annual rent * min(remaining term, 5) -- 5-year horizon
        horizon = min(term, 5)
        ead = rent * horizon
        expected_loss = round(pd * lgd * ead, 2)
        annual_expected_loss = round(expected_loss / max(horizon, 1), 2)

        # Occupancy cost ratio
        revenue = t.get("revenue")
        ocr = round(rent / revenue, 4) if revenue and revenue > 0 else None
        ocr_flag = False
        if ocr is not None:
            threshold = OCR_THRESHOLDS.get(ptype.lower(), 0.12)
            ocr_flag = ocr > threshold

        # Rent share for concentration
        rent_share = round(t["annual_rent"] / total_rent, 4)

        tenant_results.append({
            "name": t["name"],
            "annual_rent": rent,
            "sf": t.get("sf"),
            "rent_share_pct": round(rent_share * 100, 1),
            "lease_remaining_years": term,
            "credit_rating": t.get("credit_rating"),
            "tier": tier,
            "credit_score": score,
            "default_probability_5yr": round(pd, 4),
            "recovery_rate": round(recovery, 2),
            "expected_loss_5yr": expected_loss,
            "annual_expected_loss": annual_expected_loss,
            "occupancy_cost_ratio": round(ocr, 4) if ocr else None,
            "ocr_flagged": ocr_flag,
            "segment": "Anchor" if rent_share > 0.10 else "Major" if rent_share > 0.05 else "Inline",
        })

    walt_weighted_score = round(total_score_weighted / total_rent_term, 1) if total_rent_term > 0 else 0

    # Map score to equivalent rating
    if walt_weighted_score >= 80:
        score_equivalent = "Investment Grade equivalent (BBB- or better)"
    elif walt_weighted_score >= 60:
        score_equivalent = "Near Investment Grade (BB+/BB)"
    elif walt_weighted_score >= 40:
        score_equivalent = "Speculative Grade (BB-/B+)"
    elif walt_weighted_score >= 20:
        score_equivalent = "High Yield (B/CCC equivalent)"
    else:
        score_equivalent = "Distressed"

    # Aggregate expected loss
    total_expected_loss = sum(t["expected_loss_5yr"] for t in tenant_results)
    total_annual_expected_loss = sum(t["annual_expected_loss"] for t in tenant_results)
    expected_loss_pct_egi = round(total_annual_expected_loss / total_rent * 100, 2) if total_rent > 0 else 0

    # Concentration flags
    concentration_flags = []
    for t in tenant_results:
        if t["rent_share_pct"] > 40:
            concentration_flags.append(
                f"{t['name']}: {t['rent_share_pct']}% of rent -- single tenant > 40%"
            )
        if t["rent_share_pct"] > 10 and t["tier"] in ("C", "D"):
            concentration_flags.append(
                f"{t['name']}: Anchor/Major tenant ({t['rent_share_pct']}%) with {t['tier']}-tier credit"
            )
        if t["ocr_flagged"]:
            concentration_flags.append(
                f"{t['name']}: OCR {t['occupancy_cost_ratio']:.1%} exceeds threshold"
            )
        if t["lease_remaining_years"] < 2 and t["rent_share_pct"] > 10:
            concentration_flags.append(
                f"{t['name']}: Anchor/Major ({t['rent_share_pct']}%) expires in {t['lease_remaining_years']} years"
            )

    if hhi > 2500:
        concentration_flags.insert(0, f"HHI = {hhi:.0f} -- high concentration risk")

    return {
        "hhi": hhi,
        "hhi_interpretation": hhi_interpretation,
        "walt_years": walt,
        "walt_weighted_credit_score": walt_weighted_score,
        "score_equivalent_rating": score_equivalent,
        "total_annual_rent": total_rent,
        "total_expected_loss_5yr": round(total_expected_loss, 2),
        "total_annual_expected_loss": round(total_annual_expected_loss, 2),
        "expected_loss_pct_of_egi": expected_loss_pct_egi,
        "credit_reserve_recommendation_pct": round(expected_loss_pct_egi * 1.25, 2),
        "concentration_flags": concentration_flags,
        "tenants": tenant_results,
    }


def main():
    parser = argparse.ArgumentParser(description="Tenant Credit Scorer for CRE rent rolls")
    parser.add_argument("--json", type=str, help="JSON string with input parameters")
    args = parser.parse_args()

    if args.json:
        inputs = json.loads(args.json)
    elif not sys.stdin.isatty():
        inputs = json.load(sys.stdin)
    else:
        parser.print_help()
        sys.exit(1)

    result = calculate_tenant_credit(inputs)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
