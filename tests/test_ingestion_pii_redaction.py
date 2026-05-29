#!/usr/bin/env python3
"""PII redaction tests -- the governance gate.

The executable layer must be no weaker than the prose layer it sits beneath:
synthetic natural-person names are pseudonymized and never appear in any
emitted record or in the printed JSON; PII-classified fields never carry a
verbatim source_text_span; and an injected leak is a critical, non-overridable
grade block (reported as field paths, never values).

Run: python -m pytest tests/test_ingestion_pii_redaction.py
"""
from __future__ import annotations

import io
import json
import os
import sys
import unittest
from contextlib import redirect_stdout

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src", "calculators"))
FX = os.path.join(ROOT, "tests", "fixtures", "ingestion")

import normalize_tokens as N  # noqa: E402
from ingest import pii, provenance  # noqa: E402

SYNTHETIC_NAMES = ("Tenant Alpha LLC", "Acme Retail Co", "J. Fixture")


def load(name: str) -> dict:
    with open(os.path.join(FX, name), "r", encoding="utf-8") as fh:
        return json.load(fh)


class TestNoNameLeak(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = load("rent_roll_with_charge_codes.json")
        self.payload = N.calculate_normalize_tokens(self.fx)

    def test_no_raw_name_in_payload(self) -> None:
        blob = json.dumps(self.payload)
        for name in SYNTHETIC_NAMES:
            self.assertNotIn(name, blob)

    def test_no_raw_name_on_stdout(self) -> None:
        # The CLI prints json.dumps(result); none of the synthetic names may
        # appear on the printed surface.
        buf = io.StringIO()
        with redirect_stdout(buf):
            print(json.dumps(N.calculate_normalize_tokens(self.fx), indent=2))
        out = buf.getvalue()
        for name in SYNTHETIC_NAMES:
            self.assertNotIn(name, out)

    def test_scan_reports_paths_not_values(self) -> None:
        leak = {"rows": [{"note": "signed by Acme Retail Co"}]}
        hits = pii.scan_for_leaks(leak, ["Acme Retail Co"])
        self.assertEqual(hits, ["rows[0].note"])


class TestProvenancePiiRule(unittest.TestCase):
    def test_pii_field_has_no_span(self) -> None:
        p = provenance.build_provenance(
            field_name="tenant_name", source_document_id="RR-001", source_ref_anchor="tenant",
            skill_name="rent-roll-to-database", skill_version="0.1.0", run_id="R", as_of="2026-05-31",
            source_cell_address="RR-001!Detail!B2", source_text_span="Jane Doe",
        )
        self.assertIsNone(p["source_text_span"])
        self.assertEqual(p["redaction_status"], "redacted")
        self.assertEqual(p["source_cell_address"], "RR-001!Detail!B2")  # locator retained

    def test_non_pii_field_keeps_span(self) -> None:
        p = provenance.build_provenance(
            field_name="occupancy_rate", source_document_id="RR-001", source_ref_anchor="occ",
            skill_name="rent-roll-to-database", skill_version="0.1.0", run_id="R", as_of="2026-05-31",
            source_text_span="98.1%",
        )
        self.assertEqual(p["source_text_span"], "98.1%")


class TestTenantIdSafety(unittest.TestCase):
    def test_path_traversal_rejected(self) -> None:
        self.assertTrue(pii.assert_safe_tenant_id("../secret"))
        self.assertTrue(pii.assert_safe_tenant_id("a/b"))
        self.assertEqual(pii.assert_safe_tenant_id("synthetic-fund"), [])


if __name__ == "__main__":
    unittest.main()
