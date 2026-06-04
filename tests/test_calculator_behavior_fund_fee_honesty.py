#!/usr/bin/env python3
"""Honesty-labeling tests for fund_fee_modeler promote sensitivity (v5.1, WS-G2).

``promote_sensitivity`` reports ``breakeven_irr_*`` values computed by a linear
fee-drag approximation (``pref_return + weighted_avg_fee_drag``), NOT a true
discounted-cashflow IRR root-find. v5.1 keeps the numeric keys for back-compat
but labels the output honestly so a reader cannot mistake the screening-grade
approximation for a decision-grade DCF-IRR.

These tests assert the honesty labels exist and propagate into the scenario
command's nested promote-sensitivity block, and that the numeric back-compat
keys are unchanged.
"""
from __future__ import annotations

import os
import sys
import unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PLUGIN_ROOT, "src", "calculators"))

from fund_fee_modeler import promote_sensitivity, cmd_scenario  # noqa: E402


def _state() -> dict:
    return {
        "fundName": "Honesty Fund",
        "fundId": "fund-h",
        "standardTerms": {
            "managementFee": 0.015,
            "fundTerm": 10,
            "investmentPeriod": 5,
            "preferredReturn": 0.08,
            "carry": 0.20,
        },
        "targetRaise": 200_000_000,
        "hardCap": 250_000_000,
        "mfnProvisions": {"enabled": True, "minimumCommitmentForMFN": 10_000_000},
        "investors": [
            {"lpId": "lp-001", "name": "Anchor LP", "commitment": 50_000_000,
             "status": "signed", "tier": "anchor",
             "negotiatedTerms": {"managementFee": 0.0125}},
            {"lpId": "lp-002", "name": "Tiered LP", "commitment": 75_000_000,
             "status": "signed", "tier": "standard"},
        ],
    }


class TestPromoteSensitivityHonesty(unittest.TestCase):
    def test_output_is_labeled_screening_grade(self) -> None:
        out = promote_sensitivity(0.0135, 200_000_000, _state())
        self.assertEqual(out.get("grade"), "screening")

    def test_method_names_the_approximation(self) -> None:
        out = promote_sensitivity(0.0135, 200_000_000, _state())
        self.assertEqual(out.get("method"), "linear_fee_drag_approximation")

    def test_backcompat_numeric_keys_preserved(self) -> None:
        out = promote_sensitivity(0.0135, 200_000_000, _state())
        for key in ("breakeven_irr_standard", "breakeven_irr_blended",
                    "breakeven_delta_bps", "promote_delta_fund_life"):
            self.assertIn(key, out)
            self.assertIsInstance(out[key], (int, float))

    def test_scenario_command_carries_grade_in_nested_sensitivity(self) -> None:
        result = cmd_scenario(_state(), lp_id="lp-001", proposed_fee=0.011)
        ps = result["promoteSensitivity"]
        self.assertEqual(ps["current"].get("grade"), "screening")
        self.assertEqual(ps["proposed"].get("grade"), "screening")


if __name__ == "__main__":
    unittest.main()
