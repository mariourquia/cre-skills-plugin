#!/usr/bin/env python3
"""Target-model mapping, DDL emission, load-plan, and schema-inference tests.

Institutional reviewers read the emitted DDL, so it is regression-locked: every
profile emits parseable CREATE TABLE statements with NO DML, and the load plan
is topologically valid (FK targets precede referrers).

Run: python -m pytest tests/test_ingestion_target_model.py
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
import map_to_target_model as M  # noqa: E402
import emit_sql_ddl as D  # noqa: E402
import emit_load_plan as L  # noqa: E402
import infer_schema as S  # noqa: E402
from ingest import profiles  # noqa: E402

DML_TOKENS = ("insert ", "update ", "delete ", " drop ", "drop table", "truncate", "alter table")


def load(name: str) -> dict:
    with open(os.path.join(FX, name), "r", encoding="utf-8") as fh:
        return json.load(fh)


class TestMapToTargetModel(unittest.TestCase):
    def test_normalized_charge_rows(self) -> None:
        rr = N.calculate_normalize_tokens(load("rent_roll_with_charge_codes.json"))
        out = M.calculate_map_to_target_model({"profile": "normalized_relational", "payload": rr})
        self.assertEqual(out["tables"]["cre_charge_schedule"]["row_count"], 7)
        self.assertEqual(out["tables"]["cre_unit"]["row_count"], 4)

    def test_unknown_profile_errors(self) -> None:
        out = M.calculate_map_to_target_model({"profile": "nope", "payload": {"doc_type": "rent_roll"}})
        self.assertIn("error", out)


class TestEmitDdl(unittest.TestCase):
    def test_all_profiles_emit_dml_free_ddl(self) -> None:
        for prof in profiles.TARGET_PROFILES:
            out = D.calculate_emit_sql_ddl({"profile": prof})
            self.assertGreater(out["table_count"], 0, prof)
            self.assertIn("create table if not exists", out["ddl"].lower(), prof)
            low = out["ddl"].lower()
            for tok in DML_TOKENS:
                self.assertNotIn(tok, low, "%s emitted DML token %r" % (prof, tok))

    def test_only_postgres(self) -> None:
        out = D.calculate_emit_sql_ddl({"profile": "normalized_relational", "dialect": "mysql"})
        self.assertIn("error", out)


class TestEmitLoadPlan(unittest.TestCase):
    def test_topologically_valid(self) -> None:
        for prof in ("normalized_relational", "star_schema", "data_vault", "hybrid_recommended"):
            out = L.calculate_emit_load_plan({"profile": prof})
            self.assertTrue(out["topologically_valid"], prof)
            for step in out["load_order"]:
                self.assertEqual(step["unmet_dependencies"], [], "%s:%s" % (prof, step["table"]))


class TestInferSchema(unittest.TestCase):
    def test_type_inference(self) -> None:
        out = S.calculate_infer_schema({"rows": [
            {"unit": "101", "rent": "1,700.00", "start": "2024-01-01", "period": "2025-06", "occupied": True},
            {"unit": "102", "rent": "1800", "start": "2024-03-01", "period": "2025-05", "occupied": False},
        ]})
        cols = {c["name"]: c for c in out["columns"]}
        self.assertEqual(cols["rent"]["type"], "numeric")
        self.assertEqual(cols["start"]["type"], "date")
        self.assertEqual(cols["period"]["type"], "period")
        self.assertEqual(cols["occupied"]["type"], "boolean")

    def test_empty_errors(self) -> None:
        self.assertIn("error", S.calculate_infer_schema({"rows": []}))


if __name__ == "__main__":
    unittest.main()
