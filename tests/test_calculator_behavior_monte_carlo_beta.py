#!/usr/bin/env python3
"""Behavioral tests for the Monte Carlo beta-distribution copula fix (v5.1, WS-G1).

Pre-v5.1 defect: the beta branch of the per-trial sampler drew an INDEPENDENT
``rng.betavariate(alpha, beta)`` while a comment claimed "correlation preserved
through the normal copula structure". For any beta-distributed variable the
input ``correlation_matrix`` was silently ignored.

The fix maps the copula uniform ``u = normal_cdf(correlated_normals[i])`` through
the beta inverse-CDF (``beta_invcdf``), built on the regularized incomplete beta
function, so beta marginals inherit the Gaussian-copula correlation while
preserving their own marginal shape.

These tests assert:
  * the regularized incomplete beta and its inverse are numerically correct on
    known closed-form values (no rng involved),
  * the inverse-CDF is robust at the divergent endpoints (u in {0,1}) and for
    alpha/beta < 1 (reachable from the three-point fitter),
  * correlation is ACTUALLY applied to beta variables end-to-end (sign test at
    n=6k, fixed seed) — the test that fails on the pre-fix code,
  * the beta marginal mean is preserved,
  * the simulation stays deterministic under a fixed seed with a beta variable.
"""
from __future__ import annotations

import math
import os
import random
import sys
import unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PLUGIN_ROOT, "src", "calculators"))

from monte_carlo_simulator import (  # noqa: E402
    beta_invcdf,
    regularized_incomplete_beta,
    sample_trial_values,
    cholesky_decompose,
    generate_correlated_normals,
    fit_distribution,
    run_simulation,
)


def _pearson(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx <= 0 or syy <= 0:
        return 0.0
    return sxy / math.sqrt(sxx * syy)


class TestRegularizedIncompleteBeta(unittest.TestCase):
    def test_identity_when_a_b_are_one(self) -> None:
        # Beta(1,1) is Uniform(0,1): I_x(1,1) == x.
        for x in (0.1, 0.25, 0.5, 0.8, 0.95):
            self.assertAlmostEqual(regularized_incomplete_beta(x, 1.0, 1.0), x, places=6)

    def test_symmetric_median(self) -> None:
        # Symmetric Beta(a,a): I_0.5(a,a) == 0.5.
        for a in (2.0, 4.63, 10.0):
            self.assertAlmostEqual(regularized_incomplete_beta(0.5, a, a), 0.5, places=6)

    def test_monotone_increasing(self) -> None:
        prev = -1.0
        for x in (0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0):
            val = regularized_incomplete_beta(x, 2.0, 5.0)
            self.assertGreaterEqual(val, prev)
            prev = val
        self.assertAlmostEqual(regularized_incomplete_beta(0.0, 2.0, 5.0), 0.0, places=9)
        self.assertAlmostEqual(regularized_incomplete_beta(1.0, 2.0, 5.0), 1.0, places=9)


class TestBetaInverseCDF(unittest.TestCase):
    def test_uniform_when_a_b_are_one(self) -> None:
        # Beta(1,1) inverse-CDF is the identity.
        for u in (0.1, 0.3, 0.5, 0.7, 0.9):
            self.assertAlmostEqual(beta_invcdf(u, 1.0, 1.0), u, places=5)

    def test_symmetric_median_is_half(self) -> None:
        for a in (2.0, 4.63, 10.0):
            self.assertAlmostEqual(beta_invcdf(0.5, a, a), 0.5, places=5)

    def test_round_trip_cdf_invcdf(self) -> None:
        for (a, b) in ((2.0, 5.0), (4.63, 4.63), (0.783, 0.783)):
            for u in (0.05, 0.2, 0.5, 0.75, 0.99):
                x = beta_invcdf(u, a, b)
                self.assertGreaterEqual(x, 0.0)
                self.assertLessEqual(x, 1.0)
                self.assertAlmostEqual(regularized_incomplete_beta(x, a, b), u, places=4)

    def test_monotone(self) -> None:
        self.assertLess(beta_invcdf(0.2, 2.0, 5.0), beta_invcdf(0.8, 2.0, 5.0))

    def test_endpoints_do_not_raise_or_nan(self) -> None:
        # normal_cdf saturates to exactly 0.0 / 1.0 beyond +/-8 sigma, which is
        # reachable under correlated normals. The inverse-CDF must clamp.
        lo = beta_invcdf(0.0, 2.0, 2.0)
        hi = beta_invcdf(1.0, 2.0, 2.0)
        self.assertFalse(math.isnan(lo))
        self.assertFalse(math.isnan(hi))
        self.assertGreaterEqual(lo, 0.0)
        self.assertLessEqual(hi, 1.0)
        self.assertLess(lo, hi)

    def test_alpha_beta_below_one_is_finite(self) -> None:
        # alpha,beta < 1 (e.g. base 0.5 over a wide 0.1..0.9 range) makes the
        # density diverge at the endpoints; the CDF/inverse must stay finite.
        for u in (0.01, 0.5, 0.99):
            x = beta_invcdf(u, 0.783, 0.783)
            self.assertFalse(math.isnan(x))
            self.assertGreater(x, 0.0)
            self.assertLess(x, 1.0)


def _beta_fitted(base: float = 0.5, best: float = 0.7, worst: float = 0.3) -> dict:
    f = fit_distribution(
        {"name": "x", "best_case": best, "base_case": base, "worst_case": worst, "distribution": "beta"}
    )
    assert f["type"] == "beta", f
    return f


class TestCopulaCorrelationAppliedToBeta(unittest.TestCase):
    """The discriminating test: fails on the pre-fix independent-draw code."""

    def _sample_corr(self, rho: float, trials: int = 6_000, seed: int = 42) -> float:
        fitted = {"a": _beta_fitted(), "b": _beta_fitted()}
        var_names = ["a", "b"]
        corr = [[1.0, rho], [rho, 1.0]]
        L = cholesky_decompose(corr)
        rng = random.Random(seed)
        a_samples: list[float] = []
        b_samples: list[float] = []
        for _ in range(trials):
            cn = generate_correlated_normals(rng, L, 2)
            vals = sample_trial_values(cn, fitted, var_names)
            a_samples.append(vals["a"])
            b_samples.append(vals["b"])
        return _pearson(a_samples, b_samples)

    def test_positive_correlation_is_applied(self) -> None:
        r = self._sample_corr(0.8)
        # Gaussian-copula correlation on beta marginals attenuates below the
        # input 0.8; 0.3 is a wide, non-flaky floor at n=6k. Pre-fix r ~ 0.
        self.assertGreater(r, 0.3, f"expected strong positive sample corr, got {r}")

    def test_negative_correlation_is_applied(self) -> None:
        r = self._sample_corr(-0.8)
        self.assertLess(r, -0.3, f"expected strong negative sample corr, got {r}")

    def test_marginal_mean_preserved(self) -> None:
        fitted = {"a": _beta_fitted()}
        var_names = ["a"]
        L = cholesky_decompose([[1.0]])
        rng = random.Random(7)
        samples = [sample_trial_values(generate_correlated_normals(rng, L, 1), fitted, var_names)["a"]
                   for _ in range(6_000)]
        self.assertAlmostEqual(sum(samples) / len(samples), fitted["a"]["mean"], delta=0.01)


class TestSimulationBetaDeterminism(unittest.TestCase):
    def _cfg(self, seed: int = 42) -> dict:
        return {
            "purchase_price": 10_000_000,
            "equity_invested": 3_500_000,
            "hold_period": 5,
            "base_noi": 650_000,
            "financing": {"ltv": 0.65, "rate": 0.065, "term": 10, "amort_years": 30, "io_years": 0},
            "variables": [
                {"name": "rent_growth", "best_case": 0.04, "base_case": 0.03, "worst_case": 0.01, "distribution": "triangular"},
                {"name": "vacancy", "best_case": 0.30, "base_case": 0.50, "worst_case": 0.70, "distribution": "beta"},
            ],
            "correlation_matrix": {
                "rent_growth": {"rent_growth": 1.0, "vacancy": -0.5},
                "vacancy": {"rent_growth": -0.5, "vacancy": 1.0},
            },
            "num_trials": 2000,
            "random_seed": seed,
        }

    def test_seeded_run_is_deterministic_with_beta(self) -> None:
        a = run_simulation(self._cfg())
        b = run_simulation(self._cfg())
        self.assertEqual(a["summary_statistics"], b["summary_statistics"])

    def test_beta_marginal_mean_through_public_api(self) -> None:
        out = run_simulation(self._cfg())
        ds = out["distribution_summary"]["vacancy"]
        self.assertEqual(ds["fitted_type"], "beta")
        self.assertAlmostEqual(ds["sample_mean"], ds["fitted_mean"], delta=0.02)


if __name__ == "__main__":
    unittest.main()
