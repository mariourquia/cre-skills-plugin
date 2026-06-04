#!/usr/bin/env python3
"""Behavioral tests for the loan covenant tester (v5 -- new file).

The covenant tester previously had ZERO behavioral tests (only correctness
smoke). This file adds: happy path, IO-vs-amort debt-service ordering,
first-breach-year detection on a declining-NOI series, cash-sweep year set,
amortization-balance behavior across the IO boundary, a pinned regression
snapshot, a unit-sanity check, and degenerate-input REFUSALS (empty NOI series,
zero loan amount) which previously raised ValueError / ZeroDivisionError.
"""
from __future__ import annotations

import os
import sys
import unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PLUGIN_ROOT, "src", "calculators"))

from covenant_tester import calculate_covenants  # noqa: E402


def _input(**overrides) -> dict:
    base = {
        "noi_by_year": [1_200_000, 1_250_000, 1_300_000, 1_350_000, 1_400_000],
        "loan_amount": 10_000_000,
        "rate": 0.065,
        "amortization_years": 30,
        "io_years": 2,
        "property_value_by_year": [
            16_000_000, 16_500_000, 17_000_000, 17_500_000, 18_000_000
        ],
        "dscr_covenant": 1.25,
        "ltv_covenant": 0.75,
        "debt_yield_covenant": 0.08,
        "cash_sweep_dscr": 1.15,
    }
    base.update(overrides)
    return base


def _is_refusal(out: dict) -> bool:
    return isinstance(out, dict) and out.get("refused") is True and bool(out.get("error"))


class TestCovenantHappyPath(unittest.TestCase):
    def test_healthy_loan_no_breach(self) -> None:
        out = calculate_covenants(_input())
        self.assertFalse(out["breach_detected"])
        self.assertIsNone(out["first_breach_year"])
        self.assertEqual(len(out["dscr_by_year"]), 5)


class TestCovenantIoVsAmort(unittest.TestCase):
    def test_io_debt_service_below_amort(self) -> None:
        out = calculate_covenants(_input())
        io_ds = out["summary"]["annual_debt_service_io"]
        amort_ds = out["summary"]["annual_debt_service_amort"]
        self.assertLess(io_ds, amort_ds)

    def test_first_amort_year_switches_payment_type(self) -> None:
        out = calculate_covenants(_input())
        self.assertEqual(out["annual_detail"][0]["debt_service_type"], "IO")
        self.assertEqual(out["annual_detail"][2]["debt_service_type"], "P&I")


class TestCovenantAmortBalance(unittest.TestCase):
    def test_balance_amortizes_after_io_boundary(self) -> None:
        # io_years=2: years 1-2 IO (balance == loan), year 3 is the FIRST amort
        # year (0 payments elapsed -> still == loan), balance first drops below
        # the original loan in year io+2 (= year 4).
        out = calculate_covenants(_input(noi_by_year=[1_200_000] * 6,
                                         property_value_by_year=[16_000_000] * 6))
        loan = 10_000_000
        self.assertEqual(out["annual_detail"][2]["loan_balance"], loan)  # yr 3
        self.assertLess(out["annual_detail"][3]["loan_balance"], loan)   # yr 4

    def test_ltv_uses_amortizing_balance_not_original_loan(self) -> None:
        # By a late amort year, LTV must reflect the paid-down balance, so the
        # LTV implied by the original loan would be strictly higher.
        out = calculate_covenants(_input(noi_by_year=[1_200_000] * 6,
                                         property_value_by_year=[16_000_000] * 6))
        yr6 = out["annual_detail"][5]
        ltv_from_balance = yr6["ltv"]
        ltv_from_original = round(10_000_000 / 16_000_000, 4)
        self.assertLess(ltv_from_balance, ltv_from_original)


class TestCovenantBreachDetection(unittest.TestCase):
    def test_first_breach_year_is_first_dscr_crossing(self) -> None:
        # Declining NOI, no IO. DSCR crosses below the 1.25 covenant at year 3.
        out = calculate_covenants(_input(
            noi_by_year=[1_400_000, 1_000_000, 700_000, 600_000, 500_000],
            io_years=0,
        ))
        dscr = out["dscr_by_year"]
        covenant = 1.25
        expected_first = next(i + 1 for i, d in enumerate(dscr) if d < covenant)
        self.assertEqual(out["first_breach_year"], expected_first)
        self.assertEqual(out["first_breach_type"], "DSCR")

    def test_cash_sweep_years_are_below_threshold(self) -> None:
        out = calculate_covenants(_input(
            noi_by_year=[1_400_000, 1_000_000, 700_000, 600_000, 500_000],
            io_years=0,
            cash_sweep_dscr=1.15,
        ))
        for yr in out["cash_sweep_years"]:
            self.assertLess(out["dscr_by_year"][yr - 1], 1.15)


class TestCovenantRegressionSnapshot(unittest.TestCase):
    def test_pinned_baseline(self) -> None:
        out = calculate_covenants(_input())
        self.assertAlmostEqual(out["summary"]["annual_debt_service_io"], 650_000.0, delta=1.0)
        self.assertAlmostEqual(out["summary"]["annual_debt_service_amort"], 758_481.63, delta=1.0)
        self.assertAlmostEqual(out["summary"]["min_dscr"], 1.714, delta=0.01)
        self.assertEqual(out["summary"]["min_dscr_year"], 3)
        self.assertEqual(out["dscr_by_year"], [1.846, 1.923, 1.714, 1.78, 1.846])


class TestCovenantUnitSanity(unittest.TestCase):
    def test_dscr_is_ratio_scale(self) -> None:
        out = calculate_covenants(_input())
        # DSCR is a coverage ratio ~1-2x, not a percentage; a healthy loan must
        # land comfortably above 1 and well below 100.
        for d in out["dscr_by_year"]:
            self.assertGreater(d, 0.5)
            self.assertLess(d, 100.0)

    def test_ltv_is_fraction_scale(self) -> None:
        out = calculate_covenants(_input())
        for ltv in out["ltv_by_year"]:
            if ltv is not None:
                self.assertGreater(ltv, 0.0)
                self.assertLess(ltv, 1.5)


class TestCovenantDegenerateRefusals(unittest.TestCase):
    def test_empty_noi_series_refuses(self) -> None:
        out = calculate_covenants(_input(noi_by_year=[], property_value_by_year=[]))
        self.assertTrue(_is_refusal(out), f"expected refusal, got {out}")

    def test_zero_loan_amount_refuses(self) -> None:
        out = calculate_covenants(_input(loan_amount=0))
        self.assertTrue(_is_refusal(out), f"expected refusal, got {out}")

    def test_negative_loan_amount_refuses(self) -> None:
        out = calculate_covenants(_input(loan_amount=-5))
        self.assertTrue(_is_refusal(out), f"expected refusal, got {out}")

    def test_refusal_is_typed(self) -> None:
        out = calculate_covenants(_input(noi_by_year=[], property_value_by_year=[]))
        self.assertEqual(out.get("code"), "covenant_tester_degenerate")


if __name__ == "__main__":
    unittest.main()
