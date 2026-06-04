#!/usr/bin/env python3
"""Behavioral tests for Monte Carlo return simulator.

Complements tests/test_calculator_correctness.py with behavior-focused
checks:
- Seed determinism (same seed → same output).
- Percentile coherence (P10 ≤ P50 ≤ P90 for IRR and equity multiple).
- Monotone response to worst-case tail (increasing vacancy should not
  reduce loss probability).
- Degenerate inputs (zero trials, impossible correlation matrix) refuse
  cleanly rather than crash silently.
"""
from __future__ import annotations

import os
import sys
import unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PLUGIN_ROOT, "src", "calculators"))

from monte_carlo_simulator import run_simulation  # noqa: E402


def _base_input(seed: int = 42, trials: int = 500) -> dict:
    return {
        "purchase_price": 10_000_000,
        "equity_invested": 3_500_000,
        "hold_period": 5,
        "base_noi": 650_000,
        "financing": {
            "ltv": 0.65,
            "rate": 0.065,
            "term": 10,
            "amort_years": 30,
            "io_years": 0,
        },
        "variables": [
            {"name": "rent_growth", "best_case": 0.04, "base_case": 0.03, "worst_case": 0.01, "distribution": "triangular"},
            {"name": "exit_cap", "best_case": 0.055, "base_case": 0.065, "worst_case": 0.08, "distribution": "triangular"},
            {"name": "vacancy", "best_case": 0.03, "base_case": 0.05, "worst_case": 0.10, "distribution": "triangular"},
            {"name": "expense_growth", "best_case": 0.02, "base_case": 0.03, "worst_case": 0.05, "distribution": "triangular"},
        ],
        "correlation_matrix": {
            "rent_growth": {"rent_growth": 1.0, "exit_cap": -0.30, "vacancy": -0.50, "expense_growth": 0.20},
            "exit_cap": {"rent_growth": -0.30, "exit_cap": 1.0, "vacancy": 0.40, "expense_growth": -0.10},
            "vacancy": {"rent_growth": -0.50, "exit_cap": 0.40, "vacancy": 1.0, "expense_growth": -0.05},
            "expense_growth": {"rent_growth": 0.20, "exit_cap": -0.10, "vacancy": -0.05, "expense_growth": 1.0},
        },
        "num_trials": trials,
        "random_seed": seed,
        "target_irr": 0.12,
    }


def _irr_at(out: dict, p: str) -> float:
    return out["percentile_returns"][p]["irr"]


def _em_at(out: dict, p: str) -> float:
    return out["percentile_returns"][p]["equity_multiple"]


def _prob_loss(out: dict) -> float:
    return out["probability_metrics"]["probability_of_loss"]


class TestMonteCarloSeedDeterminism(unittest.TestCase):
    def test_same_seed_same_output(self) -> None:
        a = run_simulation(_base_input(seed=42))
        b = run_simulation(_base_input(seed=42))
        self.assertEqual(_irr_at(a, "P50"), _irr_at(b, "P50"))
        self.assertEqual(_prob_loss(a), _prob_loss(b))

    def test_different_seed_different_output(self) -> None:
        a = run_simulation(_base_input(seed=1))
        b = run_simulation(_base_input(seed=2))
        self.assertNotEqual(_irr_at(a, "P50"), _irr_at(b, "P50"))


class TestMonteCarloPercentileCoherence(unittest.TestCase):
    def test_irr_percentiles_non_decreasing(self) -> None:
        out = run_simulation(_base_input(trials=2000))
        self.assertLessEqual(_irr_at(out, "P10"), _irr_at(out, "P50"))
        self.assertLessEqual(_irr_at(out, "P50"), _irr_at(out, "P90"))

    def test_equity_multiple_percentiles_non_decreasing(self) -> None:
        out = run_simulation(_base_input(trials=2000))
        self.assertLessEqual(_em_at(out, "P10"), _em_at(out, "P50"))
        self.assertLessEqual(_em_at(out, "P50"), _em_at(out, "P90"))


class TestMonteCarloMonotonicity(unittest.TestCase):
    def test_higher_worst_case_vacancy_does_not_reduce_loss_prob(self) -> None:
        mild = _base_input(trials=2000)
        severe = _base_input(trials=2000)
        for v in severe["variables"]:
            if v["name"] == "vacancy":
                v["worst_case"] = 0.20
        a = run_simulation(mild)
        b = run_simulation(severe)
        self.assertGreaterEqual(_prob_loss(b), _prob_loss(a) - 0.01)


class TestMonteCarloDegenerateInputs(unittest.TestCase):
    def test_zero_trials_should_refuse_DEFECT(self) -> None:
        """FIXED in v5: zero (or negative) trials now returns a typed refusal
        dict instead of silently floor-clamping 0 -> 1000 and fabricating a
        full distribution. Per the calculator degenerate-input contract the
        refusal is a returned envelope (not a raised exception), so the bridge
        surfaces a clean reason.
        """
        bad = _base_input(trials=0)
        out = run_simulation(bad)
        self.assertTrue(
            out.get("refused") is True and bool(out.get("error")),
            f"expected typed refusal for zero trials, got {out}",
        )
        # The fabricated-distribution symptom must be gone: no convergence block
        # claiming trials_run=1000 for a request of 0.
        self.assertNotIn("convergence", out)

    def test_negative_trials_refuses(self) -> None:
        out = run_simulation(_base_input(trials=-5))
        self.assertTrue(out.get("refused") is True and bool(out.get("error")))

    def test_zero_equity_refuses(self) -> None:
        bad = _base_input()
        bad["equity_invested"] = 0
        out = run_simulation(bad)
        self.assertTrue(
            out.get("refused") is True and bool(out.get("error")),
            f"expected refusal for zero equity, got keys={list(out)}",
        )

    def test_valid_trials_in_clamp_range_still_run(self) -> None:
        # A small but valid request (1..999) is still allowed and clamped up to
        # the 1000-trial floor for statistical stability -- only <1 refuses.
        out = run_simulation(_base_input(trials=10))
        self.assertGreaterEqual(out["convergence"]["trials_run"], 1000)

    def test_impossible_correlation_degrades_gracefully(self) -> None:
        bad = _base_input()
        for k in bad["correlation_matrix"]:
            for j in bad["correlation_matrix"][k]:
                if k != j:
                    bad["correlation_matrix"][k][j] = -1.0
        try:
            out = run_simulation(bad)
        except Exception:
            return
        self.assertLessEqual(_irr_at(out, "P10"), _irr_at(out, "P90"))


class TestMonteCarloRegressionSnapshot(unittest.TestCase):
    """Pinned P10/P50/P90 IRR at seed=42, trials=2000.

    The pre-v5 file only checked percentile ORDERING, not values, so a silent
    change to a sampler or DCF constant would not be caught. These are
    seed-deterministic; the small deltas guard against float drift while
    failing on any real change to the distribution.
    """

    def test_pinned_irr_percentiles(self) -> None:
        out = run_simulation(_base_input(seed=42, trials=2000))
        self.assertAlmostEqual(_irr_at(out, "P10"), 0.005746, delta=2e-4)
        self.assertAlmostEqual(_irr_at(out, "P50"), 0.098291, delta=2e-4)
        self.assertAlmostEqual(_irr_at(out, "P90"), 0.174556, delta=2e-4)

    def test_pinned_equity_multiples(self) -> None:
        out = run_simulation(_base_input(seed=42, trials=2000))
        self.assertAlmostEqual(_em_at(out, "P50"), 2.5495, delta=2e-3)

    def test_pinned_probability_of_loss(self) -> None:
        out = run_simulation(_base_input(seed=42, trials=2000))
        self.assertAlmostEqual(_prob_loss(out), 0.08, delta=0.01)


class TestMonteCarloUnitSanity(unittest.TestCase):
    """A scale/unit sanity check: IRR is a decimal fraction, not a percent;
    equity multiple is a positive ratio."""

    def test_irr_is_decimal_fraction_scale(self) -> None:
        out = run_simulation(_base_input(seed=42, trials=1000))
        # A 5-yr value-add CRE IRR distribution should sit well within (-1, 1)
        # as a decimal; if a constant were expressed as a percent (e.g. 9.8),
        # this band would catch it.
        self.assertGreater(_irr_at(out, "P50"), -1.0)
        self.assertLess(_irr_at(out, "P90"), 1.0)
        self.assertGreater(_em_at(out, "P50"), 0.0)


if __name__ == "__main__":
    unittest.main()
