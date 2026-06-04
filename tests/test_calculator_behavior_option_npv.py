#!/usr/bin/env python3
"""Behavioral tests for npv_trade_out + option_valuation (v5 -- new file).

Neither calculator had a behavioral test file. This covers, for npv_trade_out:
delta sign flips with market premium, breakeven-vacancy monotonicity and the
binary-search fixed point (delta ~ 0 at the breakeven), a pinned snapshot, a
unit-sanity check, and an sf=0 REFUSAL (was ZeroDivisionError). For
option_valuation: termination fee = max(hard_cost, npv_breakeven) and never
below unamortized TI+LC, a pinned snapshot, and a cap_rate=0 REFUSAL (was
ZeroDivisionError).
"""
from __future__ import annotations

import os
import sys
import unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PLUGIN_ROOT, "src", "calculators"))

from npv_trade_out import calculate_trade_out  # noqa: E402
from option_valuation import calculate_option_valuation  # noqa: E402


def _npv_input(**overrides) -> dict:
    base = {
        "current_rent_psf": 25.00,
        "market_rent_psf": 45.00,
        "renewal_rent_psf": 28.00,
        "renewal_ti_psf": 5.00,
        "new_ti_psf": 20.00,
        "lc_pct_renewal": 0.025,
        "lc_pct_new": 0.05,
        "vacancy_months": 3,
        "make_ready_psf": 5.00,
        "sf": 10_000,
        "lease_term_years": 5,
        "discount_rate": 0.07,
        "annual_escalation": 0.03,
        "carrying_cost_psf_monthly": 2.00,
    }
    base.update(overrides)
    return base


def _opt_input(**overrides) -> dict:
    base = {
        "ti_total": 250_000,
        "ti_amortization_months": 120,
        "lc_total": 95_000,
        "lc_amortization_months": 120,
        "months_remaining": 72,
        "market_rent_psf": 35.00,
        "sf": 10_000,
        "expected_vacancy_months": 6,
        "releasing_cost_psf": 30.00,
        "discount_rate": 0.07,
        "noi": 2_000_000,
        "cap_rate": 0.055,
        "tenant_pct_of_nra": 0.25,
        "lease_term_years": 10,
        "remaining_term_years": 6,
    }
    base.update(overrides)
    return base


def _is_refusal(out: dict) -> bool:
    return isinstance(out, dict) and out.get("refused") is True and bool(out.get("error"))


# --------------------------------------------------------------------------- #
# npv_trade_out
# --------------------------------------------------------------------------- #
class TestNpvHappyAndSignFlip(unittest.TestCase):
    def test_large_premium_favors_trade_out(self) -> None:
        out = calculate_trade_out(_npv_input(market_rent_psf=45.00))
        self.assertGreater(out["npv_delta"], 0)
        self.assertEqual(out["verdict"], "TRADE_OUT")

    def test_small_premium_favors_renew(self) -> None:
        out = calculate_trade_out(_npv_input(market_rent_psf=29.00, new_ti_psf=30.00))
        self.assertLess(out["npv_delta"], 0)


class TestNpvBreakeven(unittest.TestCase):
    def test_breakeven_vacancy_is_a_fixed_point(self) -> None:
        out = calculate_trade_out(_npv_input())
        bk = out["breakeven_vacancy_months"]
        self.assertGreater(bk, 0)
        self.assertLess(bk, 24)
        # Recomputing trade-out at the breakeven vacancy should zero the delta.
        recomputed = calculate_trade_out(_npv_input(vacancy_months=bk))
        self.assertAlmostEqual(recomputed["npv_delta"], 0, delta=1_000)

    def test_more_vacancy_monotonically_worsens_trade_out(self) -> None:
        deltas = [
            calculate_trade_out(_npv_input(vacancy_months=v))["npv_delta"]
            for v in (2, 4, 6, 9, 12)
        ]
        for i in range(len(deltas) - 1):
            self.assertGreaterEqual(deltas[i], deltas[i + 1])


class TestNpvRegressionSnapshot(unittest.TestCase):
    def test_pinned(self) -> None:
        out = calculate_trade_out(_npv_input())
        self.assertAlmostEqual(out["renewal_npv"], 1_212_004.0, delta=1.0)
        self.assertAlmostEqual(out["tradeout_npv"], 1_545_992.0, delta=1.0)
        self.assertAlmostEqual(out["breakeven_vacancy_months"], 8.8, delta=0.1)


class TestNpvUnitSanity(unittest.TestCase):
    def test_effective_rent_psf_in_plausible_band(self) -> None:
        out = calculate_trade_out(_npv_input())
        # Effective rent PSF must be on a per-SF scale (tens of dollars), not a
        # whole-suite dollar figure.
        self.assertGreater(out["tradeout_effective_rent_psf"], 1.0)
        self.assertLess(out["tradeout_effective_rent_psf"], 200.0)


class TestNpvDegenerateRefusals(unittest.TestCase):
    def test_zero_sf_refuses(self) -> None:
        out = calculate_trade_out(_npv_input(sf=0))
        self.assertTrue(_is_refusal(out), f"expected refusal, got {out}")

    def test_negative_sf_refuses(self) -> None:
        out = calculate_trade_out(_npv_input(sf=-100))
        self.assertTrue(_is_refusal(out))

    def test_zero_term_refuses(self) -> None:
        out = calculate_trade_out(_npv_input(lease_term_years=0))
        self.assertTrue(_is_refusal(out))

    def test_refusal_is_typed(self) -> None:
        out = calculate_trade_out(_npv_input(sf=0))
        self.assertEqual(out.get("code"), "npv_trade_out_degenerate")


# --------------------------------------------------------------------------- #
# option_valuation
# --------------------------------------------------------------------------- #
class TestOptionTerminationFee(unittest.TestCase):
    def test_fee_is_max_of_two_methods(self) -> None:
        out = calculate_option_valuation(_opt_input())
        tf = out["termination_fee"]
        self.assertAlmostEqual(
            tf["minimum_termination_fee"],
            max(tf["hard_cost_recovery"], tf["npv_breakeven"]),
            delta=1.0,
        )

    def test_fee_never_below_unamortized_ti_plus_lc(self) -> None:
        out = calculate_option_valuation(_opt_input())
        tf = out["termination_fee"]
        floor = tf["unamortized_ti"] + tf["unamortized_lc"]
        self.assertGreaterEqual(tf["minimum_termination_fee"], floor)

    def test_unamortized_ti_straight_line(self) -> None:
        # 72 of 120 months remaining -> 60% of TI unamortized.
        out = calculate_option_valuation(_opt_input())
        self.assertAlmostEqual(out["termination_fee"]["unamortized_ti"], 150_000.0, delta=1.0)


class TestOptionRegressionSnapshot(unittest.TestCase):
    def test_pinned(self) -> None:
        out = calculate_option_valuation(_opt_input())
        tf = out["termination_fee"]
        self.assertAlmostEqual(tf["minimum_termination_fee"], 678_481.94, delta=1.0)
        self.assertEqual(tf["fee_method"], "hard_cost_recovery")
        self.assertAlmostEqual(out["cap_rate_impact"]["base_value"], 36_363_636.0, delta=1.0)


class TestOptionUnitSanity(unittest.TestCase):
    def test_base_value_is_noi_over_cap(self) -> None:
        out = calculate_option_valuation(_opt_input())
        self.assertAlmostEqual(
            out["cap_rate_impact"]["base_value"], 2_000_000 / 0.055, delta=1.0
        )


class TestOptionDegenerateRefusals(unittest.TestCase):
    def test_zero_cap_rate_refuses(self) -> None:
        out = calculate_option_valuation(_opt_input(cap_rate=0))
        self.assertTrue(_is_refusal(out), f"expected refusal, got {out}")

    def test_negative_cap_rate_refuses(self) -> None:
        out = calculate_option_valuation(_opt_input(cap_rate=-0.01))
        self.assertTrue(_is_refusal(out))

    def test_zero_sf_refuses(self) -> None:
        out = calculate_option_valuation(_opt_input(sf=0))
        self.assertTrue(_is_refusal(out))

    def test_refusal_is_typed(self) -> None:
        out = calculate_option_valuation(_opt_input(cap_rate=0))
        self.assertEqual(out.get("code"), "option_valuation_degenerate")


if __name__ == "__main__":
    unittest.main()
