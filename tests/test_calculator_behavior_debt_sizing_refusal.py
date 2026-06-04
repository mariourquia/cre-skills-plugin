#!/usr/bin/env python3
"""Refusal behavior for debt sizing (v5 hardening).

The pre-v5 calculator silently returned a wrong-sign recommended loan on
negative NOI and an undefined LTV on zero property value. These are MORE
dangerous than a crash because they look like a real answer. v5 requires a
typed refusal dict ({"error", "refused": true, "code"}) instead.

This file is the TDD driver for the debt_sizing P0 guard. It complements
tests/test_calculator_behavior_debt_sizing.py (which keeps its older
"zero NOI -> zero loan" expectation removed/migrated here).
"""
from __future__ import annotations

import os
import sys
import unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PLUGIN_ROOT, "src", "calculators"))

from debt_sizing import calculate_debt_sizing  # noqa: E402


def _input(
    noi: float = 1_500_000,
    prop_value: float = 20_000_000,
    dscr: float = 1.25,
    ltv: float = 0.65,
    dy: float = 0.09,
    rate: float = 0.065,
    io_years: int = 0,
) -> dict:
    return {
        "noi": noi,
        "property_value": prop_value,
        "target_dscr": dscr,
        "target_ltv": ltv,
        "target_debt_yield": dy,
        "rate": rate,
        "amortization_years": 30,
        "io_years": io_years,
    }


def _is_refusal(out: dict) -> bool:
    return isinstance(out, dict) and out.get("refused") is True and bool(out.get("error"))


class TestDebtSizingRefusesDegenerate(unittest.TestCase):
    def test_negative_noi_refuses_not_wrong_sign_loan(self) -> None:
        out = calculate_debt_sizing(_input(noi=-500_000))
        self.assertTrue(_is_refusal(out), f"expected refusal, got {out}")
        # The dangerous pre-v5 behavior: a negative recommended_loan.
        self.assertNotIn("sizing_results", out)

    def test_zero_noi_refuses(self) -> None:
        out = calculate_debt_sizing(_input(noi=0))
        self.assertTrue(_is_refusal(out), f"expected refusal, got {out}")

    def test_zero_property_value_refuses(self) -> None:
        out = calculate_debt_sizing(_input(prop_value=0))
        self.assertTrue(_is_refusal(out), f"expected refusal, got {out}")

    def test_negative_property_value_refuses(self) -> None:
        out = calculate_debt_sizing(_input(prop_value=-1))
        self.assertTrue(_is_refusal(out), f"expected refusal, got {out}")

    def test_refusal_carries_typed_code(self) -> None:
        out = calculate_debt_sizing(_input(noi=-1))
        self.assertEqual(out.get("code"), "debt_sizing_degenerate")


class TestDebtSizingValidInputsUnchanged(unittest.TestCase):
    """Guard must not perturb the valid-input answer (regression snapshot)."""

    def test_pinned_scenario_still_holds(self) -> None:
        out = calculate_debt_sizing(_input())
        self.assertFalse(_is_refusal(out))
        sizing = out["sizing_results"]
        self.assertEqual(sizing["binding_constraint"], "LTV")
        self.assertAlmostEqual(sizing["recommended_loan"], 13_000_000.0, delta=1.0)
        self.assertAlmostEqual(out["loan_metrics"]["dscr_amortizing"], 1.521, delta=0.01)

    def test_positive_loan_recommended_for_healthy_deal(self) -> None:
        out = calculate_debt_sizing(_input())
        self.assertGreater(out["sizing_results"]["recommended_loan"], 0)


if __name__ == "__main__":
    unittest.main()
