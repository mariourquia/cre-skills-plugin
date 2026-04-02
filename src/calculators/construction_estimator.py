#!/usr/bin/env python3
"""
Construction Cost Estimator
============================
Produces a TDC (Total Development Cost) estimate for a CRE project by
CSI division, with regional adjustment, soft cost layering, contingency,
and sensitivity analysis.

Used by: construction-cost-estimator skill

Usage:
    python3 scripts/calculators/construction_estimator.py --json '{
        "asset_type": "multifamily",
        "gross_sf": 200000,
        "unit_count": 250,
        "stories": 5,
        "location": "Austin, TX",
        "construction_type": "wood_frame",
        "finish_level": "standard",
        "parking_type": "surface",
        "parking_spaces": 300,
        "union_labor": false,
        "prevailing_wage": false,
        "site_conditions": "greenfield"
    }'

Output: JSON with division-level hard costs, regional adjustment, soft costs,
        contingency, TDC summary, key metrics, and 3-scenario sensitivity.
"""

import argparse
import json
import sys
from typing import Any


# ---------------------------------------------------------------------------
# Embedded cost tables (national-average mid-range $/SF by CSI division)
# Keyed by (asset_type, construction_type, finish_level)
# These are the "mid" values from csi-cost-database.yaml
# ---------------------------------------------------------------------------

# Base costs per SF by division for common combinations
# Format: {(asset_type, construction_type): {finish_level: {division: cost_per_sf}}}

_BASE_COSTS: dict[str, dict[str, dict[str, dict[str, float]]]] = {
    "multifamily": {
        "wood_frame": {
            "value": {
                "01": 12.00, "03": 12.00, "04": 4.00, "05": 3.50,
                "06": 24.00, "07": 7.50, "08": 8.00, "09": 16.00,
                "10": 1.50, "11": 3.50, "12": 0.50, "14": 2.00,
                "21": 4.00, "22": 11.00, "23": 14.00, "26": 12.00,
                "31": 3.50, "32": 5.00, "33": 3.50,
            },
            "standard": {
                "01": 14.50, "03": 14.00, "04": 5.50, "05": 5.00,
                "06": 29.00, "07": 10.00, "08": 11.00, "09": 22.00,
                "10": 2.50, "11": 5.50, "12": 1.00, "14": 2.50,
                "21": 4.50, "22": 14.00, "23": 19.00, "26": 15.00,
                "31": 5.00, "32": 6.50, "33": 4.50,
            },
            "premium": {
                "01": 18.00, "03": 16.00, "04": 8.00, "05": 6.50,
                "06": 36.00, "07": 13.00, "08": 15.00, "09": 30.00,
                "10": 3.50, "11": 8.00, "12": 2.50, "14": 3.50,
                "21": 5.00, "22": 18.00, "23": 25.00, "26": 19.00,
                "31": 6.00, "32": 9.00, "33": 5.00,
            },
            "luxury": {
                "01": 23.00, "03": 18.00, "04": 12.00, "05": 9.00,
                "06": 45.00, "07": 16.00, "08": 22.00, "09": 44.00,
                "10": 5.00, "11": 12.00, "12": 5.00, "14": 5.00,
                "21": 5.50, "22": 24.00, "23": 33.00, "26": 25.00,
                "31": 7.50, "32": 12.00, "33": 5.50,
            },
        },
        "steel": {
            "value": {
                "01": 18.00, "03": 24.00, "04": 5.00, "05": 28.00,
                "06": 6.00, "07": 9.00, "08": 11.00, "09": 19.00,
                "10": 1.50, "11": 3.50, "12": 0.50, "14": 3.50,
                "21": 4.00, "22": 11.00, "23": 14.00, "26": 12.00,
                "31": 3.50, "32": 5.00, "33": 3.50,
            },
            "standard": {
                "01": 22.00, "03": 28.00, "04": 7.50, "05": 33.00,
                "06": 9.00, "07": 12.00, "08": 15.00, "09": 26.00,
                "10": 2.50, "11": 5.50, "12": 1.00, "14": 4.50,
                "21": 4.50, "22": 14.00, "23": 19.00, "26": 15.00,
                "31": 5.00, "32": 6.50, "33": 4.50,
            },
            "premium": {
                "01": 27.00, "03": 33.00, "04": 10.50, "05": 40.00,
                "06": 12.00, "07": 15.00, "08": 21.00, "09": 35.00,
                "10": 3.50, "11": 8.00, "12": 2.50, "14": 6.00,
                "21": 5.00, "22": 18.00, "23": 25.00, "26": 19.00,
                "31": 6.00, "32": 9.00, "33": 5.00,
            },
            "luxury": {
                "01": 33.00, "03": 38.00, "04": 15.00, "05": 48.00,
                "06": 17.00, "07": 19.00, "08": 30.00, "09": 52.00,
                "10": 5.00, "11": 12.00, "12": 5.00, "14": 8.00,
                "21": 5.50, "22": 24.00, "23": 33.00, "26": 25.00,
                "31": 7.50, "32": 12.00, "33": 5.50,
            },
        },
        "concrete": {
            "value": {
                "01": 21.00, "03": 45.00, "04": 4.00, "05": 6.00,
                "06": 5.00, "07": 9.00, "08": 12.00, "09": 19.00,
                "10": 1.50, "11": 3.50, "12": 0.50, "14": 5.00,
                "21": 4.00, "22": 11.00, "23": 14.00, "26": 12.00,
                "31": 3.50, "32": 5.00, "33": 3.50,
            },
            "standard": {
                "01": 26.00, "03": 54.00, "04": 6.50, "05": 8.00,
                "06": 8.00, "07": 12.00, "08": 16.00, "09": 26.00,
                "10": 2.50, "11": 5.50, "12": 1.00, "14": 6.00,
                "21": 4.50, "22": 14.00, "23": 19.00, "26": 15.00,
                "31": 5.00, "32": 6.50, "33": 4.50,
            },
            "premium": {
                "01": 32.00, "03": 64.00, "04": 9.50, "05": 10.00,
                "06": 11.00, "07": 15.00, "08": 22.00, "09": 35.00,
                "10": 3.50, "11": 8.00, "12": 2.50, "14": 8.00,
                "21": 5.00, "22": 18.00, "23": 25.00, "26": 19.00,
                "31": 6.00, "32": 9.00, "33": 5.00,
            },
            "luxury": {
                "01": 38.00, "03": 74.00, "04": 15.00, "05": 13.00,
                "06": 16.00, "07": 19.00, "08": 33.00, "09": 52.00,
                "10": 5.00, "11": 12.00, "12": 5.00, "14": 10.00,
                "21": 5.50, "22": 24.00, "23": 33.00, "26": 25.00,
                "31": 7.50, "32": 12.00, "33": 5.50,
            },
        },
    },
    "office": {
        "steel": {
            "value": {
                "01": 18.00, "03": 26.00, "04": 4.00, "05": 32.00,
                "06": 5.00, "07": 9.00, "08": 15.00, "09": 16.00,
                "10": 1.50, "11": 0.50, "12": 0.25, "14": 4.00,
                "21": 4.00, "22": 6.00, "23": 19.00, "26": 16.00,
                "31": 3.50, "32": 5.00, "33": 3.50,
            },
            "standard": {
                "01": 23.00, "03": 31.00, "04": 6.00, "05": 38.00,
                "06": 8.00, "07": 12.00, "08": 20.00, "09": 24.00,
                "10": 2.50, "11": 1.00, "12": 0.50, "14": 5.00,
                "21": 4.50, "22": 8.00, "23": 25.00, "26": 22.00,
                "31": 5.00, "32": 7.00, "33": 4.50,
            },
            "premium": {
                "01": 29.00, "03": 38.00, "04": 9.00, "05": 48.00,
                "06": 12.00, "07": 15.00, "08": 30.00, "09": 35.00,
                "10": 3.50, "11": 1.50, "12": 1.50, "14": 7.00,
                "21": 5.50, "22": 10.00, "23": 34.00, "26": 30.00,
                "31": 6.00, "32": 9.00, "33": 5.00,
            },
            "luxury": {
                "01": 36.00, "03": 46.00, "04": 14.00, "05": 57.00,
                "06": 17.00, "07": 19.00, "08": 44.00, "09": 50.00,
                "10": 5.00, "11": 2.50, "12": 4.00, "14": 9.00,
                "21": 6.50, "22": 13.00, "23": 45.00, "26": 40.00,
                "31": 7.50, "32": 12.00, "33": 5.50,
            },
        },
        "concrete": {
            "standard": {
                "01": 28.00, "03": 57.00, "04": 5.00, "05": 9.00,
                "06": 7.00, "07": 11.00, "08": 20.00, "09": 24.00,
                "10": 2.50, "11": 1.00, "12": 0.50, "14": 6.00,
                "21": 4.50, "22": 8.00, "23": 25.00, "26": 22.00,
                "31": 5.00, "32": 7.00, "33": 4.50,
            },
        },
    },
    "industrial": {
        "steel": {
            "value": {
                "01": 7.00, "03": 9.00, "04": 2.00, "05": 18.00,
                "06": 2.00, "07": 6.00, "08": 3.50, "09": 3.50,
                "10": 0.50, "11": 1.00, "12": 0.00, "14": 0.00,
                "21": 3.00, "22": 3.00, "23": 5.00, "26": 6.00,
                "31": 2.50, "32": 5.00, "33": 3.00,
            },
            "standard": {
                "01": 9.50, "03": 11.00, "04": 3.00, "05": 23.00,
                "06": 3.00, "07": 8.00, "08": 5.00, "09": 5.00,
                "10": 0.75, "11": 1.50, "12": 0.25, "14": 0.00,
                "21": 4.00, "22": 4.00, "23": 7.50, "26": 8.00,
                "31": 3.50, "32": 6.00, "33": 4.00,
            },
            "premium": {
                "01": 12.00, "03": 14.00, "04": 4.50, "05": 28.00,
                "06": 4.50, "07": 10.00, "08": 7.50, "09": 8.00,
                "10": 1.00, "11": 2.50, "12": 0.50, "14": 0.00,
                "21": 5.50, "22": 5.50, "23": 12.00, "26": 11.00,
                "31": 5.00, "32": 7.50, "33": 5.00,
            },
        },
    },
    "retail": {
        "steel": {
            "value": {
                "01": 11.00, "03": 11.00, "04": 3.50, "05": 16.00,
                "06": 3.50, "07": 6.50, "08": 9.00, "09": 9.00,
                "10": 1.00, "11": 0.50, "12": 0.25, "14": 0.00,
                "21": 3.50, "22": 4.50, "23": 11.00, "26": 9.00,
                "31": 2.50, "32": 6.00, "33": 3.00,
            },
            "standard": {
                "01": 14.50, "03": 14.00, "04": 5.50, "05": 21.00,
                "06": 6.00, "07": 9.00, "08": 13.00, "09": 14.00,
                "10": 1.50, "11": 1.00, "12": 0.50, "14": 0.00,
                "21": 4.00, "22": 6.50, "23": 15.00, "26": 12.00,
                "31": 4.00, "32": 7.50, "33": 4.00,
            },
            "premium": {
                "01": 19.00, "03": 18.00, "04": 9.00, "05": 28.00,
                "06": 9.00, "07": 12.00, "08": 20.00, "09": 22.00,
                "10": 2.50, "11": 2.00, "12": 1.50, "14": 0.00,
                "21": 5.00, "22": 8.50, "23": 20.00, "26": 16.00,
                "31": 5.00, "32": 10.00, "33": 4.50,
            },
        },
    },
    "mixed_use": {
        "steel": {
            "standard": {
                "01": 22.00, "03": 31.00, "04": 7.00, "05": 36.00,
                "06": 9.00, "07": 12.00, "08": 18.00, "09": 24.00,
                "10": 2.50, "11": 4.50, "12": 1.00, "14": 5.00,
                "21": 4.50, "22": 13.00, "23": 22.00, "26": 19.00,
                "31": 5.00, "32": 7.00, "33": 4.50,
            },
        },
        "concrete": {
            "standard": {
                "01": 27.00, "03": 56.00, "04": 6.00, "05": 9.00,
                "06": 8.00, "07": 11.00, "08": 18.00, "09": 24.00,
                "10": 2.50, "11": 4.50, "12": 1.00, "14": 6.00,
                "21": 4.50, "22": 13.00, "23": 22.00, "26": 19.00,
                "31": 5.00, "32": 7.00, "33": 4.50,
            },
        },
    },
}

# CSI division labels
_DIVISION_NAMES: dict[str, str] = {
    "01": "General Requirements",
    "03": "Concrete",
    "04": "Masonry",
    "05": "Metals",
    "06": "Wood/Plastics/Composites",
    "07": "Thermal & Moisture Protection",
    "08": "Openings",
    "09": "Finishes",
    "10": "Specialties",
    "11": "Equipment",
    "12": "Furnishings",
    "14": "Conveying Equipment",
    "21": "Fire Suppression",
    "22": "Plumbing",
    "23": "HVAC",
    "26": "Electrical",
    "31": "Earthwork",
    "32": "Exterior Improvements",
    "33": "Utilities",
}

# Regional cost factors (subset -- full list in regional-cost-factors.yaml)
_REGIONAL_FACTORS: dict[str, float] = {
    "new york, ny": 1.45, "brooklyn, ny": 1.38, "newark, nj": 1.28,
    "jersey city, nj": 1.32, "boston, ma": 1.32, "hartford, ct": 1.15,
    "stamford, ct": 1.22, "philadelphia, pa": 1.22, "pittsburgh, pa": 1.08,
    "washington, dc": 1.18, "baltimore, md": 1.05, "providence, ri": 1.12,
    "atlanta, ga": 0.92, "miami, fl": 1.05, "orlando, fl": 0.90,
    "tampa, fl": 0.90, "jacksonville, fl": 0.87, "charlotte, nc": 0.88,
    "raleigh, nc": 0.88, "nashville, tn": 0.90, "memphis, tn": 0.84,
    "charleston, sc": 0.86, "richmond, va": 0.92, "new orleans, la": 0.88,
    "birmingham, al": 0.82, "chicago, il": 1.22, "minneapolis, mn": 1.08,
    "milwaukee, wi": 1.05, "detroit, mi": 1.02, "columbus, oh": 0.95,
    "cleveland, oh": 1.00, "cincinnati, oh": 0.95, "indianapolis, in": 0.92,
    "kansas city, mo": 0.95, "st. louis, mo": 1.00, "omaha, ne": 0.88,
    "des moines, ia": 0.88, "dallas, tx": 0.88, "houston, tx": 0.85,
    "austin, tx": 0.92, "san antonio, tx": 0.83, "phoenix, az": 0.90,
    "tucson, az": 0.85, "denver, co": 0.98, "salt lake city, ut": 0.90,
    "las vegas, nv": 0.98, "albuquerque, nm": 0.85,
    "los angeles, ca": 1.25, "san francisco, ca": 1.42,
    "san jose, ca": 1.35, "oakland, ca": 1.32, "san diego, ca": 1.15,
    "sacramento, ca": 1.12, "riverside, ca": 1.08,
    "portland, or": 1.08, "seattle, wa": 1.15, "honolulu, hi": 1.35,
    "boise, id": 0.88, "anchorage, ak": 1.30,
    "louisville, ky": 0.88, "norfolk, va": 0.90, "savannah, ga": 0.84,
    "oklahoma city, ok": 0.82, "tulsa, ok": 0.80,
    "little rock, ar": 0.78, "jackson, ms": 0.76,
    "fort lauderdale, fl": 0.98, "sioux falls, sd": 0.82,
    "fargo, nd": 0.85, "billings, mt": 0.90, "cheyenne, wy": 0.85,
    "burlington, vt": 1.06, "portland, me": 1.04,
}

# Parking cost per space (mid values)
_PARKING_COST: dict[str, int] = {
    "surface": 5000,
    "structured": 35000,
    "underground": 60000,
    "none": 0,
}

# Soft cost percentages (of hard cost) -- standard ground-up
_SOFT_COST_PCT: dict[str, dict[str, float]] = {
    "multifamily": {
        "architecture_engineering": 0.065,
        "civil_geotech": 0.015,
        "permits_fees": 0.018,
        "legal": 0.005,
        "insurance": 0.005,
        "financing_interest": 0.038,
        "financing_fees": 0.012,
        "property_tax": 0.008,
        "marketing_leaseup": 0.015,
        "developer_fee": 0.035,
        "accounting_audit": 0.003,
        "testing_inspection": 0.005,
        "commissioning": 0.003,
    },
    "office": {
        "architecture_engineering": 0.070,
        "civil_geotech": 0.015,
        "permits_fees": 0.020,
        "legal": 0.006,
        "insurance": 0.005,
        "financing_interest": 0.040,
        "financing_fees": 0.012,
        "property_tax": 0.010,
        "marketing_leaseup": 0.025,
        "developer_fee": 0.035,
        "accounting_audit": 0.003,
        "testing_inspection": 0.005,
        "commissioning": 0.004,
    },
    "industrial": {
        "architecture_engineering": 0.055,
        "civil_geotech": 0.015,
        "permits_fees": 0.012,
        "legal": 0.004,
        "insurance": 0.004,
        "financing_interest": 0.030,
        "financing_fees": 0.010,
        "property_tax": 0.006,
        "marketing_leaseup": 0.010,
        "developer_fee": 0.030,
        "accounting_audit": 0.002,
        "testing_inspection": 0.004,
        "commissioning": 0.002,
    },
    "retail": {
        "architecture_engineering": 0.060,
        "civil_geotech": 0.015,
        "permits_fees": 0.018,
        "legal": 0.005,
        "insurance": 0.005,
        "financing_interest": 0.035,
        "financing_fees": 0.012,
        "property_tax": 0.008,
        "marketing_leaseup": 0.020,
        "developer_fee": 0.035,
        "accounting_audit": 0.003,
        "testing_inspection": 0.005,
        "commissioning": 0.003,
    },
    "mixed_use": {
        "architecture_engineering": 0.080,
        "civil_geotech": 0.018,
        "permits_fees": 0.025,
        "legal": 0.008,
        "insurance": 0.006,
        "financing_interest": 0.042,
        "financing_fees": 0.012,
        "property_tax": 0.010,
        "marketing_leaseup": 0.020,
        "developer_fee": 0.040,
        "accounting_audit": 0.003,
        "testing_inspection": 0.006,
        "commissioning": 0.004,
    },
}


def _get_regional_factor(location: str) -> tuple[float, str]:
    """Look up regional cost factor by location. Returns (factor, matched_city)."""
    loc = location.strip().lower()
    if loc in _REGIONAL_FACTORS:
        return _REGIONAL_FACTORS[loc], location

    # Try partial match on city name
    for city, factor in _REGIONAL_FACTORS.items():
        if city.split(",")[0] in loc or loc in city:
            return factor, city

    # Fall back to 1.00 (national average)
    return 1.00, f"{location} (defaulting to national average)"


def _get_base_costs(
    asset_type: str, construction_type: str, finish_level: str
) -> dict[str, float] | None:
    """Look up base $/SF costs for each division."""
    at = _BASE_COSTS.get(asset_type, {})
    ct = at.get(construction_type, {})
    fl = ct.get(finish_level)
    return fl


def _fallback_base_cost(asset_type: str, finish_level: str) -> dict[str, float]:
    """Generate rough fallback costs when exact combo is not in the embedded table."""
    # Use multifamily/wood_frame/standard as baseline and scale
    base = _BASE_COSTS["multifamily"]["wood_frame"]["standard"].copy()
    asset_multiplier = {
        "multifamily": 1.0, "office": 1.15, "industrial": 0.55,
        "retail": 0.75, "mixed_use": 1.20, "hospitality": 1.35,
        "medical": 1.50, "self_storage": 0.45,
    }.get(asset_type, 1.0)
    finish_multiplier = {
        "value": 0.80, "standard": 1.00, "premium": 1.30, "luxury": 1.70,
    }.get(finish_level, 1.0)
    return {
        div: round(cost * asset_multiplier * finish_multiplier, 2)
        for div, cost in base.items()
    }


def calculate_estimate(inputs: dict[str, Any]) -> dict[str, Any]:
    """Main estimation engine."""
    asset_type = inputs["asset_type"]
    gross_sf = inputs["gross_sf"]
    unit_count = inputs.get("unit_count")
    stories = inputs.get("stories", 1)
    location = inputs["location"]
    construction_type = inputs["construction_type"]
    finish_level = inputs["finish_level"]
    parking_type = inputs.get("parking_type", "none")
    parking_spaces = inputs.get("parking_spaces", 0)
    union_labor = inputs.get("union_labor", False)
    prevailing_wage = inputs.get("prevailing_wage", False)
    site_conditions = inputs.get("site_conditions", "greenfield")

    # Step 1: Base division costs
    division_costs = _get_base_costs(asset_type, construction_type, finish_level)
    if division_costs is None:
        division_costs = _fallback_base_cost(asset_type, finish_level)

    base_hard_cost_psf = sum(division_costs.values())
    base_hard_cost = round(base_hard_cost_psf * gross_sf, 0)

    # Step 2: Regional adjustment
    regional_factor, matched_city = _get_regional_factor(location)

    # Union and prevailing wage adjustments
    union_adj = 0.12 if union_labor else 0.0
    pw_adj = 0.08 if prevailing_wage else 0.0
    combined_factor = regional_factor * (1 + union_adj) * (1 + pw_adj)

    adjusted_hard_psf = round(base_hard_cost_psf * combined_factor, 2)
    adjusted_hard_cost = round(adjusted_hard_psf * gross_sf, 0)

    # Division-level adjusted costs
    division_detail = []
    for div_code in sorted(division_costs.keys()):
        adj_psf = round(division_costs[div_code] * combined_factor, 2)
        div_total = round(adj_psf * gross_sf, 0)
        pct = round(adj_psf / adjusted_hard_psf * 100, 1) if adjusted_hard_psf else 0
        division_detail.append({
            "division": div_code,
            "name": _DIVISION_NAMES.get(div_code, f"Division {div_code}"),
            "cost_per_sf": adj_psf,
            "total": div_total,
            "pct_of_hard": pct,
        })

    # Step 3: Site adjustments
    site_adj_total = 0
    site_adjustments = []
    if site_conditions == "brownfield":
        env_cost = round(gross_sf * 8.00 * combined_factor, 0)
        site_adj_total += env_cost
        site_adjustments.append({"item": "Environmental remediation (brownfield)", "cost": env_cost})
    if site_conditions == "constrained":
        shoring = round(150 * stories * 350 * combined_factor, 0)
        site_adj_total += shoring
        site_adjustments.append({"item": "Shoring/constrained site access", "cost": shoring})
    if site_conditions in ("brownfield", "constrained", "infill"):
        traffic = round(75000 * combined_factor, 0)
        site_adj_total += traffic
        site_adjustments.append({"item": "Traffic management/logistics", "cost": traffic})
    stormwater = round(gross_sf * 2.50, 0)
    site_adj_total += stormwater
    site_adjustments.append({"item": "Stormwater management", "cost": stormwater})

    # Step 4: Parking
    parking_cost_per_space = round(_PARKING_COST.get(parking_type, 0) * combined_factor, 0)
    parking_total = parking_cost_per_space * parking_spaces

    # Total hard cost
    total_hard = adjusted_hard_cost + site_adj_total + parking_total

    # Step 5: Soft costs
    soft_pcts = _SOFT_COST_PCT.get(asset_type, _SOFT_COST_PCT["multifamily"])
    soft_detail = []
    total_soft = 0
    for category, pct in soft_pcts.items():
        cost = round(total_hard * pct, 0)
        total_soft += cost
        soft_detail.append({
            "category": category.replace("_", " ").title(),
            "pct_of_hard": round(pct * 100, 2),
            "cost": cost,
        })

    # Step 6: Contingency (assume conceptual stage = 15% design + 7% construction + 4% owner)
    design_contingency = round(total_hard * 0.15, 0)
    construction_contingency = round(total_hard * 0.07, 0)
    owner_contingency = round((total_hard + total_soft) * 0.04, 0)
    total_contingency = design_contingency + construction_contingency + owner_contingency

    # TDC (excluding land)
    tdc_excl_land = total_hard + total_soft + total_contingency

    # Key metrics
    tdc_per_sf = round(tdc_excl_land / gross_sf, 2) if gross_sf else 0
    hard_per_sf = round(total_hard / gross_sf, 2) if gross_sf else 0
    tdc_per_unit = round(tdc_excl_land / unit_count, 0) if unit_count else None
    soft_pct_of_hard = round(total_soft / total_hard * 100, 1) if total_hard else 0
    contingency_pct_of_tdc = round(total_contingency / tdc_excl_land * 100, 1) if tdc_excl_land else 0

    # Step 7: Sensitivity analysis
    scenarios = {}
    for label, hard_mult, soft_mult, conting_usage in [
        ("low", 0.88, 0.92, 0.25),
        ("base", 1.00, 1.00, 0.50),
        ("high", 1.13, 1.08, 0.80),
    ]:
        s_hard = round(total_hard * hard_mult, 0)
        s_soft = round(total_soft * soft_mult, 0)
        s_cont = round(total_contingency * conting_usage, 0)
        s_tdc = s_hard + s_soft + s_cont
        scenarios[label] = {
            "hard_costs": s_hard,
            "soft_costs": s_soft,
            "contingency_used": s_cont,
            "tdc_excl_land": s_tdc,
            "tdc_per_sf": round(s_tdc / gross_sf, 2) if gross_sf else 0,
            "tdc_per_unit": round(s_tdc / unit_count, 0) if unit_count else None,
            "delta_from_base_pct": round((s_tdc / (total_hard + total_soft + total_contingency * 0.50) - 1) * 100, 1)
            if label != "base" else 0.0,
        }

    return {
        "project_parameters": {
            "asset_type": asset_type,
            "gross_sf": gross_sf,
            "unit_count": unit_count,
            "stories": stories,
            "location": location,
            "matched_city": matched_city,
            "construction_type": construction_type,
            "finish_level": finish_level,
            "parking_type": parking_type,
            "parking_spaces": parking_spaces,
            "union_labor": union_labor,
            "prevailing_wage": prevailing_wage,
            "site_conditions": site_conditions,
        },
        "regional_adjustment": {
            "base_factor": regional_factor,
            "union_premium": union_adj,
            "prevailing_wage_premium": pw_adj,
            "combined_factor": round(combined_factor, 4),
        },
        "hard_costs": {
            "base_hard_cost_psf": round(base_hard_cost_psf, 2),
            "adjusted_hard_cost_psf": adjusted_hard_psf,
            "building_hard_cost": adjusted_hard_cost,
            "site_adjustments": site_adjustments,
            "site_adjustment_total": site_adj_total,
            "parking_cost_per_space": parking_cost_per_space,
            "parking_total": parking_total,
            "total_hard_cost": total_hard,
            "division_detail": division_detail,
        },
        "soft_costs": {
            "detail": soft_detail,
            "total_soft_cost": total_soft,
            "soft_pct_of_hard": soft_pct_of_hard,
        },
        "contingency": {
            "design_contingency": design_contingency,
            "construction_contingency": construction_contingency,
            "owner_contingency": owner_contingency,
            "total_contingency": total_contingency,
            "note": "Conceptual/pre-design stage assumptions (15% design, 7% construction, 4% owner)",
        },
        "tdc_summary": {
            "total_hard_cost": total_hard,
            "total_soft_cost": total_soft,
            "total_contingency": total_contingency,
            "tdc_excl_land": tdc_excl_land,
        },
        "key_metrics": {
            "tdc_per_sf": tdc_per_sf,
            "tdc_per_unit": tdc_per_unit,
            "hard_cost_per_sf": hard_per_sf,
            "soft_pct_of_hard": soft_pct_of_hard,
            "contingency_pct_of_tdc": contingency_pct_of_tdc,
        },
        "sensitivity": scenarios,
    }


def _fmt_currency(val: float | int | None) -> str:
    """Format a number as currency."""
    if val is None:
        return "N/A"
    return f"${val:,.0f}"


def _print_report(result: dict[str, Any]) -> None:
    """Print a human-readable formatted report."""
    p = result["project_parameters"]
    r = result["regional_adjustment"]
    h = result["hard_costs"]
    s = result["soft_costs"]
    c = result["contingency"]
    t = result["tdc_summary"]
    m = result["key_metrics"]
    sens = result["sensitivity"]

    print("=" * 70)
    print("CONSTRUCTION COST ESTIMATE")
    print("=" * 70)
    print()
    print(f"  Project:    {p['asset_type'].replace('_', ' ').title()}, "
          f"{p['construction_type'].replace('_', ' ').title()}, "
          f"{p['finish_level'].title()} finish")
    print(f"  Size:       {p['gross_sf']:,} SF gross | {p['stories']} stories")
    if p["unit_count"]:
        print(f"  Units:      {p['unit_count']:,}")
    print(f"  Location:   {p['location']} (factor: {r['combined_factor']:.2f})")
    print(f"  Parking:    {p['parking_spaces']} spaces ({p['parking_type']})")
    print()

    # Division detail
    print("-" * 70)
    print(f"{'Div':>4}  {'Description':<30} {'$/SF':>8} {'Total':>14} {'%':>6}")
    print("-" * 70)
    for d in h["division_detail"]:
        print(f"  {d['division']:>2}  {d['name']:<30} ${d['cost_per_sf']:>6.2f}"
              f"  {_fmt_currency(d['total']):>14} {d['pct_of_hard']:>5.1f}%")
    print("-" * 70)
    print(f"{'':>4}  {'Building Hard Cost':<30} ${h['adjusted_hard_cost_psf']:>6.2f}"
          f"  {_fmt_currency(h['building_hard_cost']):>14}")
    print()

    # Site adjustments
    if h["site_adjustments"]:
        print("  Site Adjustments:")
        for adj in h["site_adjustments"]:
            print(f"    {adj['item']:<40} {_fmt_currency(adj['cost']):>14}")
    if h["parking_total"] > 0:
        print(f"    Parking ({p['parking_spaces']} x "
              f"{_fmt_currency(h['parking_cost_per_space'])})"
              f"{'':>12} {_fmt_currency(h['parking_total']):>14}")
    print(f"{'':>4}  {'TOTAL HARD COST':<30} ${h['total_hard_cost']/p['gross_sf']:>6.2f}"
          f"  {_fmt_currency(h['total_hard_cost']):>14}")
    print()

    # Soft costs
    print("-" * 70)
    print("  SOFT COSTS")
    print("-" * 70)
    for item in s["detail"]:
        print(f"    {item['category']:<36} {item['pct_of_hard']:>5.1f}%"
              f"  {_fmt_currency(item['cost']):>14}")
    print(f"    {'TOTAL SOFT COSTS':<36} {s['soft_pct_of_hard']:>5.1f}%"
          f"  {_fmt_currency(s['total_soft_cost']):>14}")
    print()

    # Contingency
    print("-" * 70)
    print("  CONTINGENCY")
    print("-" * 70)
    print(f"    Design (15% of hard){'':>20} {_fmt_currency(c['design_contingency']):>14}")
    print(f"    Construction (7% of hard){'':>15} {_fmt_currency(c['construction_contingency']):>14}")
    print(f"    Owner (4% of hard+soft){'':>17} {_fmt_currency(c['owner_contingency']):>14}")
    print(f"    {'TOTAL CONTINGENCY':<42} {_fmt_currency(c['total_contingency']):>14}")
    print()

    # TDC Summary
    print("=" * 70)
    print(f"  TOTAL DEVELOPMENT COST (excl. land){'':>5}"
          f" {_fmt_currency(t['tdc_excl_land']):>14}")
    print("=" * 70)
    print()
    print("  KEY METRICS")
    print(f"    TDC / SF:                 {_fmt_currency(m['tdc_per_sf'])}")
    if m["tdc_per_unit"]:
        print(f"    TDC / Unit:               {_fmt_currency(m['tdc_per_unit'])}")
    print(f"    Hard Cost / SF:           {_fmt_currency(m['hard_cost_per_sf'])}")
    print(f"    Soft % of Hard:           {m['soft_pct_of_hard']:.1f}%")
    print(f"    Contingency % of TDC:     {m['contingency_pct_of_tdc']:.1f}%")
    print()

    # Sensitivity
    print("-" * 70)
    print("  SENSITIVITY ANALYSIS")
    print("-" * 70)
    header = f"{'':>24} {'Low':>14} {'Base':>14} {'High':>14}"
    print(header)
    print(f"    {'Hard Costs':<20}"
          f" {_fmt_currency(sens['low']['hard_costs']):>14}"
          f" {_fmt_currency(sens['base']['hard_costs']):>14}"
          f" {_fmt_currency(sens['high']['hard_costs']):>14}")
    print(f"    {'Soft Costs':<20}"
          f" {_fmt_currency(sens['low']['soft_costs']):>14}"
          f" {_fmt_currency(sens['base']['soft_costs']):>14}"
          f" {_fmt_currency(sens['high']['soft_costs']):>14}")
    print(f"    {'Contingency Used':<20}"
          f" {_fmt_currency(sens['low']['contingency_used']):>14}"
          f" {_fmt_currency(sens['base']['contingency_used']):>14}"
          f" {_fmt_currency(sens['high']['contingency_used']):>14}")
    print(f"    {'-'*20:<20} {'-'*14:>14} {'-'*14:>14} {'-'*14:>14}")
    print(f"    {'TDC (excl. land)':<20}"
          f" {_fmt_currency(sens['low']['tdc_excl_land']):>14}"
          f" {_fmt_currency(sens['base']['tdc_excl_land']):>14}"
          f" {_fmt_currency(sens['high']['tdc_excl_land']):>14}")
    print(f"    {'TDC / SF':<20}"
          f" {_fmt_currency(sens['low']['tdc_per_sf']):>14}"
          f" {_fmt_currency(sens['base']['tdc_per_sf']):>14}"
          f" {_fmt_currency(sens['high']['tdc_per_sf']):>14}")
    if sens["low"]["tdc_per_unit"]:
        print(f"    {'TDC / Unit':<20}"
              f" {_fmt_currency(sens['low']['tdc_per_unit']):>14}"
              f" {_fmt_currency(sens['base']['tdc_per_unit']):>14}"
              f" {_fmt_currency(sens['high']['tdc_per_unit']):>14}")
    print(f"    {'Delta from Base':<20}"
          f" {sens['low']['delta_from_base_pct']:>13.1f}%"
          f" {'--':>14}"
          f" {sens['high']['delta_from_base_pct']:>+13.1f}%")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="CRE Construction Cost Estimator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  python3 construction_estimator.py --json '{
    "asset_type": "multifamily",
    "gross_sf": 200000,
    "unit_count": 250,
    "stories": 5,
    "location": "Austin, TX",
    "construction_type": "wood_frame",
    "finish_level": "standard",
    "parking_type": "surface",
    "parking_spaces": 300,
    "union_labor": false,
    "prevailing_wage": false,
    "site_conditions": "greenfield"
  }'
        """,
    )
    parser.add_argument("--json", type=str, help="JSON string with project parameters")
    parser.add_argument(
        "--output",
        choices=["json", "report", "both"],
        default="both",
        help="Output format (default: both)",
    )
    args = parser.parse_args()

    if args.json:
        inputs = json.loads(args.json)
    elif not sys.stdin.isatty():
        inputs = json.load(sys.stdin)
    else:
        parser.print_help()
        sys.exit(1)

    result = calculate_estimate(inputs)

    if args.output in ("report", "both"):
        _print_report(result)
    if args.output in ("json", "both"):
        if args.output == "both":
            print("\n--- JSON OUTPUT ---\n")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
