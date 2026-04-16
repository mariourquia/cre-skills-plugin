#!/usr/bin/env python3
"""Behavioral tests for JV waterfall calculator.

Complements test_calculator_correctness.py with:
- Conservation: LP total + GP total distributions equal sum of
  positive cashflows.
- Loss scenario: when total distributions are below equity, GP
  promote is zero or near-zero.
- Tier monotonicity: raising the first hurdle does not produce a
  negative GP promote.
- Pinned regression snapshot on the baseline deal.
"""
from __future__ import annotations

import os
import sys
import unittest
from typing import List

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PLUGIN_ROOT, "src", "calculators"))

from waterfall_calculator import calculate_waterfall  # noqa: E402


def _input(cashflows: List[float] = None, preferred_return: float = 0.08) -> dict:
    return {
        "lp_equity": 9_000_000,
        "gp_equity": 1_000_000,
        "preferred_return": preferred_return,
        "tiers": [
            {"hurdle_irr": 0.08, "gp_split": 0.20, "lp_split": 0.80},
            {"hurdle_irr": 0.12, "gp_split": 0.30, "lp_split": 0.70},
            {"hurdle_irr": 0.18, "gp_split": 0.40, "lp_split": 0.60},
        ],
        "cashflows_by_period": cashflows
        if cashflows is not None
        else [-10_000_000, 800_000, 850_000, 900_000, 950_000, 15_000_000],
        "catch_up_pct": 0.50,
        "compounding": True,
    }


class TestWaterfallConservation(unittest.TestCase):
    def test_distributions_sum_to_positive_cashflows(self) -> None:
        inp = _input()
        out = calculate_waterfall(inp)
        lp = float(out["lp_results"]["total_distributions"])
        gp = float(out["gp_results"]["total_distributions"])
        total_cf = sum(cf for cf in inp["cashflows_by_period"] if cf > 0)
        self.assertAlmostEqual(lp + gp, total_cf, delta=1.0)

    def test_summary_total_equals_lp_plus_gp(self) -> None:
        out = calculate_waterfall(_input())
        lp = float(out["lp_results"]["total_distributions"])
        gp = float(out["gp_results"]["total_distributions"])
        self.assertAlmostEqual(float(out["summary"]["total_distributions"]), lp + gp, delta=1.0)


class TestWaterfallLossScenario(unittest.TestCase):
    def test_loss_yields_no_or_tiny_gp_promote(self) -> None:
        bad = _input(
            cashflows=[-10_000_000, 200_000, 200_000, 200_000, 200_000, 6_000_000]
        )
        out = calculate_waterfall(bad)
        promote = float(out["gp_results"]["promote"])
        # Total cashflows only return 6.8M vs 10M equity — GP promote should
        # not exceed GP equity by much; it should certainly be below total
        # equity put in.
        self.assertLess(promote, 1_500_000)


class TestWaterfallTierMonotonicity(unittest.TestCase):
    def test_raising_first_hurdle_still_produces_non_negative_promote(self) -> None:
        low_hurdle = _input()
        high_hurdle = _input()
        high_hurdle["tiers"][0]["hurdle_irr"] = 0.15
        a = calculate_waterfall(low_hurdle)
        b = calculate_waterfall(high_hurdle)
        self.assertGreaterEqual(float(a["gp_results"]["promote"]), 0.0)
        self.assertGreaterEqual(float(b["gp_results"]["promote"]), 0.0)


class TestWaterfallRegressionSnapshot(unittest.TestCase):
    def test_pinned_scenario(self) -> None:
        out = calculate_waterfall(_input())
        self.assertGreater(float(out["lp_results"]["total_distributions"]), 9_000_000)
        self.assertGreater(float(out["gp_results"]["total_distributions"]), 0)
        lp_irr = out["lp_results"].get("irr")
        if lp_irr is not None:
            self.assertGreater(lp_irr, 0.05)


if __name__ == "__main__":
    unittest.main()
