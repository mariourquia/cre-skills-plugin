#!/usr/bin/env python3
"""Rent-roll normalization + validation tests (charge-line decomposition,
charge-code vs description mapping, PII pseudonymization, free-rent skip,
GPR/occupancy, leased-not-occupied handling).

Run: python -m pytest tests/test_ingestion_rent_roll.py
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


class TestRentRollWithCodes(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = N.calculate_normalize_tokens(load("rent_roll_with_charge_codes.json"))

    def test_charge_line_decomposition(self) -> None:
        # 2 + 4 + 1 + 0 charge lines across the four rows.
        self.assertEqual(len(self.payload["records"]), 7)

    def test_known_codes_map_high_confidence(self) -> None:
        # RENT/CAM/RET/PKG are known aliases -> no inferred/unmapped issues.
        codes = [i["code"] for i in self.payload["issues"]]
        self.assertNotIn("charge_code_inferred", codes)
        self.assertNotIn("charge_code_unmapped", codes)

    def test_pii_pseudonymized(self) -> None:
        blob = json.dumps(self.payload)
        for name in ("Tenant Alpha LLC", "Acme Retail Co", "J. Fixture"):
            self.assertNotIn(name, blob)
        # tenant identity is carried as a pseudonym
        self.assertTrue(any(l["tenant_code"] and l["tenant_code"].startswith("Tenant ")
                            for l in self.payload["leases"]))

    def test_gpr_and_occupancy(self) -> None:
        agg = self.payload["aggregates"]
        # base rent on the 3 revenue-bearing units: (1700 + 25000 + 1750) * 12
        self.assertEqual(agg["gpr_in_place_annual"], 341400.0)
        # 4 revenue units (incl. vacant_available), 3 occupied
        self.assertEqual(agg["total_units"], 4)
        self.assertEqual(agg["physical_occupancy_pct"], 75.0)

    def test_vacant_unit_no_active_lease_issue(self) -> None:
        codes = [i["code"] for i in self.payload["issues"]]
        self.assertNotIn("vacant_unit_active_lease", codes)

    def test_validation_passes_with_freerent_skip(self) -> None:
        rep = V.calculate_validate_payload({"property_type": "mixed-use", "payload": self.payload})
        self.assertEqual(rep["validation_status"], "pass")
        codes = {c["code"] for c in rep["checks"]}
        # the free-rent lease (unit 102) skips the annual==monthly*12 identity
        self.assertIn("rent_arithmetic_skipped", codes)
        self.assertNotIn("rent_arithmetic_contradiction", codes)


class TestRentRollDescriptionsOnly(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = N.calculate_normalize_tokens(load("rent_roll_descriptions_only.json"))

    def test_descriptions_inferred(self) -> None:
        codes = [i["code"] for i in self.payload["issues"]]
        self.assertIn("charge_code_inferred", codes)

    def test_unmappable_description_flagged_not_guessed(self) -> None:
        # "Mystery surcharge" matches no keyword -> unmapped + review, never guessed.
        codes = [i["code"] for i in self.payload["issues"]]
        self.assertIn("charge_code_unmapped", codes)
        cats = {r.get("charge_category") for r in self.payload["records"]}
        self.assertIn("base_rent", cats)
        self.assertIn("storage", cats)

    def test_leased_not_occupied_not_flagged(self) -> None:
        # future-commencement unit must not trip vacant/active checks.
        codes = [i["code"] for i in self.payload["issues"]]
        self.assertNotIn("vacant_unit_active_lease", codes)
        rep = V.calculate_validate_payload({"property_type": "multifamily", "payload": self.payload})
        self.assertNotEqual(rep["validation_status"], "critical")


if __name__ == "__main__":
    unittest.main()
