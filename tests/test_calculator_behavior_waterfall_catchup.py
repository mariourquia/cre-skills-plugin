#!/usr/bin/env python3
"""Waterfall catch-up base fix + honest labeling + degenerate refusals (v5).

Three v5 changes are driven here:

1. CATCH-UP BASE FIX. The pre-v5 catch-up measured the GP target against
   (preferred + return-of-capital), double-counting return-of-capital as
   "profit". Standard full-catch-up measures against the PREFERRED tier only.
   On the baseline deal this moves the GP catch-up from swallowing the entire
   4.9M residual down to 3.6M (= pref_paid * c/(1-c) at c=0.5), leaving the rest
   to flow into the IRR profit-split tiers.

2. HONEST LABELING. The IRR-tier distribution is a proportional spread
   approximation, not an IRR-solved sequential waterfall. The result must say so
   (a "screening-grade proportional approximation" method label) and must NOT
   claim the tiers are IRR-solved.

3. DEGENERATE REFUSALS. Zero total equity and <2-element cashflow series must
   return a typed refusal, not raise ZeroDivisionError / IndexError.
"""
from __future__ import annotations

import os
import sys
import unittest
from typing import List

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PLUGIN_ROOT, "src", "calculators"))

from waterfall_calculator import calculate_waterfall  # noqa: E402


def _input(cashflows: List[float] = None, catch_up_pct: float = 0.50) -> dict:
    return {
        "lp_equity": 9_000_000,
        "gp_equity": 1_000_000,
        "preferred_return": 0.08,
        "tiers": [
            {"hurdle_irr": 0.08, "gp_split": 0.20, "lp_split": 0.80},
            {"hurdle_irr": 0.12, "gp_split": 0.30, "lp_split": 0.70},
            {"hurdle_irr": 0.18, "gp_split": 0.40, "lp_split": 0.60},
        ],
        "cashflows_by_period": cashflows
        if cashflows is not None
        else [-10_000_000, 800_000, 850_000, 900_000, 950_000, 15_000_000],
        "catch_up_pct": catch_up_pct,
        "compounding": True,
    }


def _catchup_tier(out: dict) -> dict | None:
    for t in out["waterfall_tiers"]:
        if "Catch-Up" in t["name"]:
            return t
    return None


def _is_refusal(out: dict) -> bool:
    return isinstance(out, dict) and out.get("refused") is True and bool(out.get("error"))


class TestCatchUpExcludesReturnOfCapital(unittest.TestCase):
    def test_catchup_measured_against_pref_only(self) -> None:
        """At c=0.5, GP catch-up == pref_paid (= pref_paid * 0.5/0.5).

        Pref accrued/paid on the baseline = 9_000_000 * 0.08 * 5 = 3_600_000.
        With the bug it was (pref + 10M capital returned) -> GP swallowed the
        full 4_900_000 residual. The fix pins it to 3_600_000.
        """
        out = calculate_waterfall(_input())
        catchup = _catchup_tier(out)
        self.assertIsNotNone(catchup, "expected a GP Catch-Up tier")
        self.assertAlmostEqual(catchup["gp_distribution"], 3_600_000.0, delta=1.0)

    def test_residual_flows_into_profit_tiers_after_catchup(self) -> None:
        # The bug left remaining=0 after catch-up (no profit-split tiers fired).
        # The fix leaves 1.3M to distribute through the IRR tiers.
        out = calculate_waterfall(_input())
        profit_tiers = [t for t in out["waterfall_tiers"] if "Profit Split" in t["name"]]
        self.assertTrue(profit_tiers, "expected profit-split tiers to receive residual")
        total_profit_split = sum(
            t["lp_distribution"] + t["gp_distribution"] for t in profit_tiers
        )
        self.assertGreater(total_profit_split, 0)

    def test_catchup_never_exceeds_full_catchup_target(self) -> None:
        # GP catch-up must not exceed pref_paid * c/(1-c); previously it did
        # (it equaled the entire residual).
        out = calculate_waterfall(_input())
        catchup = _catchup_tier(out)
        pref_paid = 9_000_000 * 0.08 * 5
        full_target = pref_paid * 0.50 / (1 - 0.50)
        self.assertLessEqual(catchup["gp_distribution"], full_target + 1.0)

    def test_conservation_still_holds_after_fix(self) -> None:
        inp = _input()
        out = calculate_waterfall(inp)
        lp = float(out["lp_results"]["total_distributions"])
        gp = float(out["gp_results"]["total_distributions"])
        total_cf = sum(cf for cf in inp["cashflows_by_period"] if cf > 0)
        self.assertAlmostEqual(lp + gp, total_cf, delta=1.0)


class TestWaterfallHonestLabeling(unittest.TestCase):
    def test_result_declares_screening_grade_approximation(self) -> None:
        out = calculate_waterfall(_input())
        method = out.get("method") or out.get("methodology") or {}
        # Accept either a top-level string field or a nested method block.
        blob = str(method) + str(out.get("disclaimer", ""))
        self.assertIn("approximation", blob.lower())
        self.assertIn("screening", blob.lower())

    def test_does_not_claim_irr_solved(self) -> None:
        out = calculate_waterfall(_input())
        blob = (str(out.get("method", "")) + str(out.get("disclaimer", ""))).lower()
        # It must explicitly disclaim IRR-solving (the honest phrasing is
        # "not irr-solved"), and must NOT positively advertise an IRR-based
        # lookback as the prior docstring did.
        self.assertIn("not irr-solved", blob)
        self.assertNotIn("irr-based lookback", blob)


class TestWaterfallDegenerateRefusals(unittest.TestCase):
    def test_zero_total_equity_refuses(self) -> None:
        bad = _input()
        bad["lp_equity"] = 0
        bad["gp_equity"] = 0
        out = calculate_waterfall(bad)
        self.assertTrue(_is_refusal(out), f"expected refusal, got {out}")

    def test_empty_cashflows_refuses(self) -> None:
        out = calculate_waterfall(_input(cashflows=[]))
        self.assertTrue(_is_refusal(out), f"expected refusal, got {out}")

    def test_single_cashflow_refuses(self) -> None:
        out = calculate_waterfall(_input(cashflows=[-10_000_000]))
        self.assertTrue(_is_refusal(out), f"expected refusal, got {out}")

    def test_refusal_is_typed(self) -> None:
        out = calculate_waterfall(_input(cashflows=[]))
        self.assertEqual(out.get("code"), "waterfall_degenerate")


class TestWaterfallUnitSanity(unittest.TestCase):
    def test_promote_is_dollar_scale_not_fraction(self) -> None:
        out = calculate_waterfall(_input())
        # GP promote on a 10M deal returning 17.5M is in the millions, not a
        # fraction; catches a units regression (e.g. returning a pct).
        self.assertGreater(float(out["gp_results"]["promote"]), 100_000)


if __name__ == "__main__":
    unittest.main()
