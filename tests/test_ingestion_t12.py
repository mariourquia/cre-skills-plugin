#!/usr/bin/env python3
"""T-12 / operating-statement normalization + validation tests.

Covers: Total/aggregate column exclusion from the period set, partial-year
lease-up warning (not a hard fail), NOI = revenue - opex with below-the-line
capex excluded, sign-convention normalization (bracketed negatives), and
account-name inference when codes are absent.

Run: python -m pytest tests/test_ingestion_t12.py
"""
from __future__ import annotations

import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src", "calculators"))
FX = os.path.join(ROOT, "tests", "fixtures", "ingestion")

import normalize_tokens as N  # noqa: E402
import validate_payload as V  # noqa: E402


def load(name: str) -> dict:
    with open(os.path.join(FX, name), "r", encoding="utf-8") as fh:
        return json.load(fh)


class TestT12WithCodes(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = N.calculate_normalize_tokens(load("t12_with_account_codes.json"))
        self.rep = V.calculate_validate_payload({"payload": self.payload})

    def test_total_column_excluded(self) -> None:
        # 13 declared columns incl. "Total"; the period set must be exactly 12.
        self.assertEqual(self.payload["aggregates"]["periods_present"], 12)

    def test_noi_excludes_below_the_line_capex(self) -> None:
        agg = self.payload["aggregates"]
        # revenue 624000, opex 132000 -> NOI 492000; the 25000 capex is excluded.
        self.assertEqual(agg["revenue_actual"], 624000.0)
        self.assertEqual(agg["operating_expense_actual"], 132000.0)
        self.assertEqual(agg["noi_actual"], 492000.0)

    def test_validation_noi_consistency(self) -> None:
        codes = {c["code"]: c for c in self.rep["checks"]}
        self.assertIn("period_count", codes)
        self.assertEqual(codes["period_count"]["status"], "pass")
        self.assertIn("noi_consistency", codes)
        self.assertEqual(codes["noi_consistency"]["status"], "pass")


class TestT12NamesOnly(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = N.calculate_normalize_tokens(load("t12_without_account_codes.json"))

    def test_name_inference_maps_accounts(self) -> None:
        accts = {r["canonical_account"] for r in self.payload["records"]}
        self.assertIn("revenue_base_rent", accts)
        self.assertIn("expense_payroll", accts)
        self.assertIn("expense_repairs_maintenance", accts)
        self.assertNotIn("unmapped", accts)


class TestT12PartialYear(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = N.calculate_normalize_tokens(load("t12_partial_year_leaseup.json"))
        self.rep = V.calculate_validate_payload({"payload": self.payload})

    def test_partial_year_is_warning_not_fail(self) -> None:
        self.assertEqual(self.payload["aggregates"]["periods_present"], 8)
        self.assertNotEqual(self.rep["validation_status"], "critical")
        codes = {c["code"] for c in self.rep["checks"]}
        self.assertIn("partial_year", codes)


class TestT12SignConvention(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = N.calculate_normalize_tokens(load("t12_signed_negative_expenses.json"))

    def test_negative_expenses_normalized_noi_not_inflated(self) -> None:
        agg = self.payload["aggregates"]
        # revenue 480000, opex |(-7000)|*12 + |(-3000)|*12 = 120000 -> NOI 360000.
        self.assertEqual(agg["revenue_actual"], 480000.0)
        self.assertEqual(agg["operating_expense_actual"], 120000.0)
        self.assertEqual(agg["noi_actual"], 360000.0)


if __name__ == "__main__":
    unittest.main()
