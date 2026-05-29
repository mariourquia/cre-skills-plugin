#!/usr/bin/env python3
"""Ingestion self-grader tests: weakest-link letter is primary, gates require
no critical failure, a PII-redaction breach is a non-overridable block, and a
rent-arithmetic contradiction blocks regardless of the numeric score.

Run: python -m pytest tests/test_ingestion_grading.py
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
import reconcile_rent_roll_t12 as R  # noqa: E402
import grade_ingestion as G  # noqa: E402


def load(name: str) -> dict:
    with open(os.path.join(FX, name), "r", encoding="utf-8") as fh:
        return json.load(fh)


class TestCleanGrade(unittest.TestCase):
    def setUp(self) -> None:
        fx = load("tieout_clean.json")
        self.rr = N.calculate_normalize_tokens(fx["rent_roll"])
        t12 = N.calculate_normalize_tokens(fx["t12"])
        self.val = V.calculate_validate_payload({"property_type": "multifamily", "payload": self.rr})
        self.rec = R.calculate_reconcile_rent_roll_t12({"run_id": "RUN-T", "as_of": "2026-05-31", "rent_roll": self.rr, "t12": t12})
        self.grade = G.calculate_grade_ingestion({"run_id": "RUN-T", "as_of": "2026-05-31",
                                                  "payload": self.rr, "validation": self.val, "reconciliation": self.rec})

    def test_merge_ready_no_breach(self) -> None:
        self.assertTrue(self.grade["merge_ready"])
        self.assertFalse(self.grade["pii_redaction_breach"])
        self.assertEqual(self.grade["critical_failures"], [])

    def test_weakest_link_caps_at_b(self) -> None:
        # credit + options dimensions are honestly B -> weakest-link B -> not prod.
        self.assertEqual(self.grade["weakest_link_grade"], "B")
        self.assertFalse(self.grade["production_ready"])
        self.assertGreaterEqual(self.grade["score_100"], 85)


class TestCriticalBlocks(unittest.TestCase):
    def test_rent_arithmetic_contradiction_blocks(self) -> None:
        # Flat lease (no free rent/step) where annual != monthly*12 -> critical.
        rr = N.calculate_normalize_tokens({
            "doc_type": "rent_roll", "run_id": "RUN-X", "as_of": "2026-05-31", "tenant_id": "synthetic-fund",
            "source": {"document_id": "RR-X"}, "property": {"property_id": "PX", "property_type": "multifamily"},
            "rows": [{"row_number": 1, "unit": "1", "rentable_sf": 800, "unit_status": "occupied", "lease_status": "active",
                      "lease_start": "2024-01-01", "lease_expire": "2026-12-31", "lease_type": "gross",
                      "charges": [{"charge_code": "RENT", "monthly_amount": 1000, "annual_amount": 15000}]}],
        })
        val = V.calculate_validate_payload({"property_type": "multifamily", "payload": rr})
        grade = G.calculate_grade_ingestion({"run_id": "RUN-X", "as_of": "2026-05-31", "payload": rr, "validation": val})
        self.assertIn("rent_arithmetic_contradiction", grade["critical_failures"])
        self.assertTrue(grade["blocked"])
        self.assertFalse(grade["merge_ready"])


class TestPiiBreachNonOverridable(unittest.TestCase):
    def test_leak_blocks_at_any_score(self) -> None:
        fx = load("tieout_clean.json")
        rr = N.calculate_normalize_tokens(fx["rent_roll"])
        # Inject a raw natural-person value that the banned list will catch.
        rr["leases"][0]["tenant_code"] = "Jane Q Public"
        val = V.calculate_validate_payload({"property_type": "multifamily", "payload": rr})
        grade = G.calculate_grade_ingestion({"run_id": "RUN-T", "as_of": "2026-05-31", "payload": rr,
                                             "validation": val, "banned_pii_values": ["Jane Q Public"]})
        self.assertTrue(grade["pii_redaction_breach"])
        self.assertFalse(grade["merge_ready"])
        self.assertIn("pii_redaction_breach", grade["critical_failures"])
        # report field paths, never the value
        self.assertTrue(grade["leak_field_paths"])
        self.assertNotIn("Jane Q Public", json.dumps(grade["leak_field_paths"]))


class TestContextGuards(unittest.TestCase):
    def test_missing_as_of_errors(self) -> None:
        out = G.calculate_grade_ingestion({"run_id": "R", "payload": {"doc_type": "rent_roll"}})
        self.assertIn("error", out)


if __name__ == "__main__":
    unittest.main()
