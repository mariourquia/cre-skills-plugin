#!/usr/bin/env python3
"""Behavioral tests for debt sizing.

Complements test_calculator_correctness.py with:
- Binding constraint selection (DSCR/LTV/DY) under different regimes.
- Zero-NOI and tiny-NOI refusal shapes.
- Rate sensitivity monotonicity (higher rate → smaller max loan).
- IO vs amortizing DSCR ordering (IO DSCR >= amortizing DSCR).
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


class TestBindingConstraintSelection(unittest.TestCase):
    def test_ltv_binds_when_ltv_is_tight(self) -> None:
        # Keep DY loose (low target) so LTV wins.
        out = calculate_debt_sizing(_input(ltv=0.45, dscr=2.0, dy=0.05))
        self.assertEqual(out["sizing_results"]["binding_constraint"], "LTV")

    def test_dscr_binds_when_dscr_is_tight(self) -> None:
        # LTV and DY both loose, DSCR tight.
        out = calculate_debt_sizing(_input(ltv=0.95, dscr=2.00, dy=0.05))
        self.assertEqual(out["sizing_results"]["binding_constraint"], "DSCR")

    def test_debt_yield_binds_when_dy_is_tight(self) -> None:
        out = calculate_debt_sizing(_input(ltv=0.95, dscr=1.05, dy=0.12))
        self.assertEqual(out["sizing_results"]["binding_constraint"], "Debt Yield")


class TestRateMonotonicity(unittest.TestCase):
    def test_higher_rate_reduces_max_loan_under_dscr(self) -> None:
        low = calculate_debt_sizing(_input(ltv=0.95, dscr=1.25, dy=0.05, rate=0.05))
        high = calculate_debt_sizing(_input(ltv=0.95, dscr=1.25, dy=0.05, rate=0.10))
        self.assertGreater(
            low["sizing_results"]["max_loan_dscr"],
            high["sizing_results"]["max_loan_dscr"],
        )


class TestIoVsAmortDscr(unittest.TestCase):
    def test_io_dscr_at_least_amort_dscr(self) -> None:
        out = calculate_debt_sizing(_input(io_years=5))
        io_dscr = out["loan_metrics"]["dscr_io"]
        amort_dscr = out["loan_metrics"]["dscr_amortizing"]
        self.assertGreaterEqual(io_dscr, amort_dscr)


class TestDegenerateInputs(unittest.TestCase):
    def test_zero_noi_produces_zero_loan(self) -> None:
        out = calculate_debt_sizing(_input(noi=0))
        self.assertEqual(out["sizing_results"]["recommended_loan"], 0)

    def test_tiny_noi_produces_small_loan(self) -> None:
        out = calculate_debt_sizing(_input(noi=10_000))
        self.assertLess(out["sizing_results"]["recommended_loan"], 500_000)


class TestRegressionSnapshot(unittest.TestCase):
    """A pinned deal to detect unintended formula changes."""

    def test_pinned_scenario(self) -> None:
        out = calculate_debt_sizing(_input())
        sizing = out["sizing_results"]
        metrics = out["loan_metrics"]
        self.assertEqual(sizing["binding_constraint"], "LTV")
        self.assertAlmostEqual(sizing["recommended_loan"], 13_000_000.0, delta=1.0)
        self.assertAlmostEqual(metrics["ltv"], 0.65, delta=0.0001)
        self.assertAlmostEqual(metrics["dscr_amortizing"], 1.521, delta=0.01)


if __name__ == "__main__":
    unittest.main()
