#!/usr/bin/env python3
"""Behavioral tests for the construction cost estimator (v5 -- new file).

Adds: happy path, regional-factor monotonicity (SF > Dallas), union +
prevailing wage strictly increasing TDC, contingency as a bounded share of TDC,
tdc_per_unit present iff unit_count supplied, a pinned regression snapshot, a
$/SF unit-sanity check, and a gross_sf=0 REFUSAL (was ZeroDivisionError).
"""
from __future__ import annotations

import os
import sys
import unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PLUGIN_ROOT, "src", "calculators"))

from construction_estimator import calculate_estimate  # noqa: E402


def _input(**overrides) -> dict:
    base = {
        "asset_type": "multifamily",
        "gross_sf": 200_000,
        "unit_count": 250,
        "stories": 5,
        "location": "Austin, TX",
        "construction_type": "wood_frame",
        "finish_level": "standard",
        "parking_type": "surface",
        "parking_spaces": 300,
        "union_labor": False,
        "prevailing_wage": False,
        "site_conditions": "greenfield",
    }
    base.update(overrides)
    return base


def _is_refusal(out: dict) -> bool:
    return isinstance(out, dict) and out.get("refused") is True and bool(out.get("error"))


class TestConstructionHappyPath(unittest.TestCase):
    def test_basic_estimate_has_tdc(self) -> None:
        out = calculate_estimate(_input())
        self.assertGreater(out["tdc_summary"]["tdc_excl_land"], 0)
        self.assertIn("hard_costs", out)
        self.assertIn("sensitivity", out)


class TestConstructionRegionalMonotonicity(unittest.TestCase):
    def test_sf_more_expensive_than_dallas(self) -> None:
        sf = calculate_estimate(_input(location="San Francisco, CA"))
        dallas = calculate_estimate(_input(location="Dallas, TX"))
        self.assertGreater(
            sf["regional_adjustment"]["combined_factor"],
            dallas["regional_adjustment"]["combined_factor"],
        )
        self.assertGreater(
            sf["tdc_summary"]["tdc_excl_land"],
            dallas["tdc_summary"]["tdc_excl_land"],
        )


class TestConstructionLaborPremiums(unittest.TestCase):
    def test_union_and_prevailing_wage_strictly_increase_tdc(self) -> None:
        base = calculate_estimate(_input())
        loaded = calculate_estimate(_input(union_labor=True, prevailing_wage=True))
        self.assertGreater(
            loaded["tdc_summary"]["tdc_excl_land"],
            base["tdc_summary"]["tdc_excl_land"],
        )


class TestConstructionContingency(unittest.TestCase):
    def test_contingency_is_bounded_share_of_tdc(self) -> None:
        out = calculate_estimate(_input())
        pct = out["key_metrics"]["contingency_pct_of_tdc"]
        # Conceptual-stage contingency (15% design + 7% construction of hard,
        # 4% owner of hard+soft) lands ~18% of full TDC. Bound it loosely.
        self.assertGreater(pct, 12.0)
        self.assertLess(pct, 30.0)


class TestConstructionPerUnit(unittest.TestCase):
    def test_per_unit_present_with_unit_count(self) -> None:
        out = calculate_estimate(_input(unit_count=250))
        self.assertIsNotNone(out["key_metrics"]["tdc_per_unit"])

    def test_per_unit_absent_without_unit_count(self) -> None:
        inp = _input()
        del inp["unit_count"]
        out = calculate_estimate(inp)
        self.assertIsNone(out["key_metrics"]["tdc_per_unit"])


class TestConstructionRegressionSnapshot(unittest.TestCase):
    def test_pinned_multifamily(self) -> None:
        out = calculate_estimate(_input())
        km = out["key_metrics"]
        self.assertAlmostEqual(km["tdc_per_sf"], 276.95, delta=0.5)
        self.assertAlmostEqual(km["tdc_per_unit"], 221_563.0, delta=50.0)
        self.assertAlmostEqual(km["hard_cost_per_sf"], 185.12, delta=0.5)
        self.assertAlmostEqual(
            out["tdc_summary"]["tdc_excl_land"], 55_390_866.0, delta=100.0
        )


class TestConstructionUnitSanity(unittest.TestCase):
    def test_tdc_per_sf_in_plausible_band(self) -> None:
        out = calculate_estimate(_input())
        # Multifamily TDC $/SF is in the low hundreds, not thousands or single
        # digits; catches a gross_sf / total mix-up.
        self.assertGreater(out["key_metrics"]["tdc_per_sf"], 50.0)
        self.assertLess(out["key_metrics"]["tdc_per_sf"], 2_000.0)


class TestConstructionDegenerateRefusals(unittest.TestCase):
    def test_zero_gross_sf_refuses(self) -> None:
        out = calculate_estimate(_input(gross_sf=0))
        self.assertTrue(_is_refusal(out), f"expected refusal, got {out}")

    def test_negative_gross_sf_refuses(self) -> None:
        out = calculate_estimate(_input(gross_sf=-100))
        self.assertTrue(_is_refusal(out))

    def test_refusal_is_typed(self) -> None:
        out = calculate_estimate(_input(gross_sf=0))
        self.assertEqual(out.get("code"), "construction_estimator_degenerate")


if __name__ == "__main__":
    unittest.main()
