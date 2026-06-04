#!/usr/bin/env python3
"""v5.1 calculator-fidelity hardening tests (WS-G3 / WS-G4).

  * debt_sizing: non-breaking ``interest_only`` alias keys clarify the ``_io``
    abbreviation (math unchanged).
  * transfer_tax / proration_calculator: typed refusal envelopes on value-domain
    degeneracy that previously produced plausible-but-wrong output (negative tax,
    negative prorations) or a raw traceback (unparseable date).
  * quick_screen: verdict-boundary behavior + refusal on a non-positive price
    that otherwise fabricates a zero-cap-rate screen.

Refusal envelope convention (matches test_calculator_behavior_degenerate_contract):
``{"error": <str>, "refused": True, "code": "<slug>_degenerate"}``.
"""
from __future__ import annotations

import os
import sys
import unittest

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PLUGIN_ROOT, "src", "calculators"))

from debt_sizing import calculate_debt_sizing  # noqa: E402
from transfer_tax import calculate_transfer_tax  # noqa: E402
from proration_calculator import calculate_prorations  # noqa: E402
from quick_screen import calculate_quick_screen  # noqa: E402


# --------------------------------------------------------------------------- #
# WS-G3 debt_sizing interest-only label clarity
# --------------------------------------------------------------------------- #
class TestDebtSizingInterestOnlyAliases(unittest.TestCase):
    def _metrics(self, io_years: int = 5) -> dict:
        out = calculate_debt_sizing({
            "noi": 1_500_000, "property_value": 20_000_000, "target_dscr": 1.25,
            "target_ltv": 0.65, "target_debt_yield": 0.09, "rate": 0.065,
            "amortization_years": 30, "io_years": io_years,
        })
        return out["loan_metrics"]

    def test_interest_only_aliases_match_io_keys(self) -> None:
        m = self._metrics()
        self.assertEqual(m["annual_debt_service_interest_only"], m["annual_debt_service_io"])
        self.assertEqual(m["dscr_interest_only"], m["dscr_io"])

    def test_legacy_io_keys_preserved(self) -> None:
        m = self._metrics()
        self.assertIn("annual_debt_service_io", m)
        self.assertIn("dscr_io", m)


# --------------------------------------------------------------------------- #
# WS-G4 transfer_tax refusal
# --------------------------------------------------------------------------- #
class TestTransferTaxRefusal(unittest.TestCase):
    def _ok(self) -> dict:
        return {"state": "NY", "purchase_price": 5_000_000, "property_type": "commercial"}

    def test_negative_price_refuses(self) -> None:
        out = calculate_transfer_tax({**self._ok(), "purchase_price": -1})
        self.assertTrue(out.get("refused"))
        self.assertEqual(out.get("code"), "transfer_tax_degenerate")

    def test_unknown_state_refuses_rather_than_silent_zero(self) -> None:
        out = calculate_transfer_tax({**self._ok(), "state": "ZZ"})
        self.assertTrue(out.get("refused"))
        self.assertEqual(out.get("code"), "transfer_tax_degenerate")

    def test_valid_input_still_computes(self) -> None:
        out = calculate_transfer_tax(self._ok())
        self.assertFalse(out.get("refused", False))
        self.assertIn("total_tax", out)
        self.assertGreaterEqual(out["total_tax"], 0)


# --------------------------------------------------------------------------- #
# WS-G4 proration refusal (incl. the raw-traceback path)
# --------------------------------------------------------------------------- #
class TestProrationRefusal(unittest.TestCase):
    def _ok(self) -> dict:
        return {
            "closing_date": "2026-07-01", "annual_tax": 120_000,
            "tax_year_start": "2026-01-01",
        }

    def test_unparseable_date_refuses_instead_of_traceback(self) -> None:
        out = calculate_prorations({**self._ok(), "closing_date": "not-a-date"})
        self.assertTrue(out.get("refused"))
        self.assertEqual(out.get("code"), "proration_calculator_degenerate")

    def test_closing_date_outside_tax_year_refuses(self) -> None:
        out = calculate_prorations({**self._ok(), "closing_date": "2030-07-01"})
        self.assertTrue(out.get("refused"))
        self.assertEqual(out.get("code"), "proration_calculator_degenerate")

    def test_negative_annual_tax_refuses(self) -> None:
        out = calculate_prorations({**self._ok(), "annual_tax": -5})
        self.assertTrue(out.get("refused"))
        self.assertEqual(out.get("code"), "proration_calculator_degenerate")

    def test_valid_input_still_computes(self) -> None:
        out = calculate_prorations(self._ok())
        self.assertFalse(out.get("refused", False))


# --------------------------------------------------------------------------- #
# WS-G4 quick_screen refusal + verdict boundary
# --------------------------------------------------------------------------- #
class TestQuickScreen(unittest.TestCase):
    def _ok(self) -> dict:
        return {
            "purchase_price": 10_000_000, "noi": 650_000, "units_or_sf": 50,
            "unit_type": "units",
        }

    def test_nonpositive_price_refuses(self) -> None:
        out = calculate_quick_screen({**self._ok(), "purchase_price": 0})
        self.assertTrue(out.get("refused"))
        self.assertEqual(out.get("code"), "quick_screen_degenerate")

    def test_valid_input_returns_a_verdict(self) -> None:
        out = calculate_quick_screen(self._ok())
        self.assertFalse(out.get("refused", False))
        self.assertIn(out.get("verdict"), {"KEEP", "KILL", "MAYBE"})


if __name__ == "__main__":
    unittest.main()
