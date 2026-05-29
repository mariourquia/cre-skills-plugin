#!/usr/bin/env python3
"""Determinism + reproducibility tests for the ingestion calculators.

Same input dict -> byte-identical JSON. run_id varies only identity-bearing
fields, never computed aggregates. No calculator imports a wall clock (the
fund_fee_modeler datetime.now() anti-pattern must not recur here). as_of is
required for graded/payload output.

Run: python -m pytest tests/test_ingestion_determinism.py
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
import reconcile_rent_roll_t12 as R  # noqa: E402
from ingest import determinism as det  # noqa: E402

NEW_CALCULATORS = (
    "normalize_tokens.py", "map_charge_codes.py", "validate_payload.py",
    "reconcile_rent_roll_t12.py", "map_to_target_model.py", "emit_sql_ddl.py",
    "emit_load_plan.py", "grade_ingestion.py", "infer_schema.py",
)


def load(name: str) -> dict:
    with open(os.path.join(FX, name), "r", encoding="utf-8") as fh:
        return json.load(fh)


class TestByteReproducible(unittest.TestCase):
    def test_normalize_identical(self) -> None:
        fx = load("rent_roll_with_charge_codes.json")
        a = N.calculate_normalize_tokens(fx)
        b = N.calculate_normalize_tokens(fx)
        self.assertEqual(det.stable_dumps(a), det.stable_dumps(b))

    def test_reconcile_identical(self) -> None:
        fx = load("tieout_clean.json")
        rr = N.calculate_normalize_tokens(fx["rent_roll"])
        t12 = N.calculate_normalize_tokens(fx["t12"])
        inp = {"run_id": "RUN-T", "as_of": "2026-05-31", "rent_roll": rr, "t12": t12}
        self.assertEqual(
            det.stable_dumps(R.calculate_reconcile_rent_roll_t12(inp)),
            det.stable_dumps(R.calculate_reconcile_rent_roll_t12(inp)),
        )


class TestRunIdScope(unittest.TestCase):
    def test_run_id_does_not_change_aggregates(self) -> None:
        fx = load("rent_roll_with_charge_codes.json")
        a = N.calculate_normalize_tokens({**fx, "run_id": "RUN-A"})
        b = N.calculate_normalize_tokens({**fx, "run_id": "RUN-B"})
        # computed aggregates must be independent of run_id (only pseudonyms /
        # run-id-bearing identity fields may differ).
        self.assertEqual(a["aggregates"], b["aggregates"])


class TestNoWallClock(unittest.TestCase):
    def test_calculators_do_not_import_datetime(self) -> None:
        calc_dir = os.path.join(ROOT, "src", "calculators")
        for fname in NEW_CALCULATORS:
            with open(os.path.join(calc_dir, fname), "r", encoding="utf-8") as fh:
                src = fh.read()
            self.assertNotIn("import datetime", src, fname)
            self.assertNotIn("datetime.now", src, fname)
            self.assertNotIn("time.time(", src, fname)


class TestAsOfRequired(unittest.TestCase):
    def test_normalize_requires_as_of(self) -> None:
        out = N.calculate_normalize_tokens({"doc_type": "rent_roll", "run_id": "R", "tenant_id": "f", "rows": []})
        self.assertIn("error", out)

    def test_reconcile_requires_as_of(self) -> None:
        out = R.calculate_reconcile_rent_roll_t12({"run_id": "R", "rent_roll": {}, "t12": {}})
        self.assertIn("error", out)


if __name__ == "__main__":
    unittest.main()
