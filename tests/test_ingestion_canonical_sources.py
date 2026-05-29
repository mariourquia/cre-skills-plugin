#!/usr/bin/env python3
"""Parity + foundation tests for the document-to-database ingestion package.

The ingestion calculators stay stdlib-only by MIRRORING the plugin's canonical
YAML sources of truth (the rent-roll data-quality rubric, the GL chart of
accounts, the PII redaction policy) as Python constants. This suite loads those
YAML files and FAILS if the Python mirror drifts -- so there is one source of
truth (ADR-0001) even though the runtime path never imports pyyaml.

It also exercises the pure foundation helpers (determinism, pseudonymization,
leak scanning, provenance PII rule, weakest-link grading).

Run: python -m pytest tests/test_ingestion_canonical_sources.py
"""
from __future__ import annotations

import os
import sys
import unittest

import yaml  # CI installs pytest + pyyaml

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PLUGIN_ROOT, "src", "calculators"))

from ingest import accounts, determinism, pii, profiles, provenance, rubric, schema, tolerances  # noqa: E402


def _load_yaml(rel_path: str) -> dict:
    with open(os.path.join(PLUGIN_ROOT, rel_path), "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


class TestRubricParity(unittest.TestCase):
    def setUp(self) -> None:
        self.doc = _load_yaml(rubric.RUBRIC_PATH)

    def test_version_matches(self) -> None:
        self.assertEqual(self.doc["rubric"]["version"], rubric.RUBRIC_VERSION)

    def test_weakest_link_method(self) -> None:
        self.assertEqual(self.doc["scoring"]["method"], "weakest_link")

    def test_dimensions_and_weights_match(self) -> None:
        yaml_dims = self.doc["dimensions"]
        mirror = {k: w for (k, _name, w) in rubric.RENT_ROLL_DIMENSIONS}
        self.assertEqual(set(yaml_dims.keys()), set(mirror.keys()))
        for key, weight in mirror.items():
            self.assertEqual(
                yaml_dims[key]["weight"], weight,
                "weight drift on rubric dimension %s" % key,
            )

    def test_rent_roll_weights_sum_to_100(self) -> None:
        total = sum(w for (_k, _n, w) in rubric.RENT_ROLL_DIMENSIONS)
        self.assertEqual(total, 100)


class TestGlSchemaParity(unittest.TestCase):
    def setUp(self) -> None:
        self.doc = _load_yaml(accounts.GL_SCHEMA_PATH)

    def test_account_type_and_normal_balance_enums(self) -> None:
        coa = self.doc["entities"]["chart_of_accounts"]["required_fields"]
        by_name = {f["name"]: f for f in coa}
        self.assertEqual(tuple(by_name["account_type"]["enum_values"]), accounts.ACCOUNT_TYPES)
        self.assertEqual(tuple(by_name["normal_balance"]["enum_values"]), accounts.NORMAL_BALANCE)


class TestCrosswalkParity(unittest.TestCase):
    def setUp(self) -> None:
        self.doc = _load_yaml(accounts.CROSSWALK_PATH)

    def test_canonical_slugs_present_in_crosswalk(self) -> None:
        crosswalk_ids = {row["canonical_id"] for row in self.doc["rows"]}
        for slug in accounts.CANONICAL_ACCOUNTS:
            self.assertIn(
                slug, crosswalk_ids,
                "canonical slug %s is not in the GL crosswalk (drift)" % slug,
            )

    def test_canonical_accounts_well_typed(self) -> None:
        for slug, meta in accounts.CANONICAL_ACCOUNTS.items():
            self.assertIn(meta["account_type"], accounts.ACCOUNT_TYPES)
            self.assertIn(meta["normal_balance"], accounts.NORMAL_BALANCE)


class TestPiiPolicyParity(unittest.TestCase):
    def setUp(self) -> None:
        self.doc = _load_yaml(pii.PII_POLICY_PATH)

    def test_never_emit_is_subset_of_policy(self) -> None:
        policy = self.doc["never_emit"]
        for category, fields in pii.NEVER_EMIT.items():
            self.assertIn(category, policy, "PII category %s missing from policy" % category)
            for f in fields:
                self.assertIn(
                    f, policy[category],
                    "PII field %s/%s drifted from pii-redaction-policy.yaml" % (category, f),
                )


class TestDeterminism(unittest.TestCase):
    def test_rounding(self) -> None:
        self.assertEqual(determinism.rnd_money(1.005 + 0.005), 1.01)
        self.assertEqual(determinism.rnd_rate(0.053349), 0.0533)
        self.assertEqual(determinism.rnd_ratio(1.2567), 1.257)

    def test_safe_div_zero(self) -> None:
        self.assertIsNone(determinism.safe_div(10, 0))
        self.assertEqual(determinism.safe_div(10, 2), 5.0)

    def test_require_context_demands_as_of(self) -> None:
        ctx = determinism.resolve_context({"run_id": "R1"})
        self.assertTrue(determinism.require_context(ctx))  # as_of missing -> error
        ctx2 = determinism.resolve_context({"run_id": "R1", "as_of": "2026-05-29"})
        self.assertEqual(determinism.require_context(ctx2), [])

    def test_no_wall_clock_imported(self) -> None:
        # The package must not depend on datetime/time anywhere in its source.
        import ingest  # noqa: F401
        pkg_dir = os.path.join(PLUGIN_ROOT, "src", "calculators", "ingest")
        for fname in os.listdir(pkg_dir):
            if not fname.endswith(".py"):
                continue
            with open(os.path.join(pkg_dir, fname), "r", encoding="utf-8") as fh:
                src = fh.read()
            self.assertNotIn("import datetime", src, "%s imports datetime" % fname)
            self.assertNotIn("datetime.now", src, "%s uses datetime.now" % fname)
            self.assertNotIn("time.time(", src, "%s uses time.time" % fname)


class TestPii(unittest.TestCase):
    def test_classify_field(self) -> None:
        self.assertEqual(pii.classify_field("tenant_name"), "natural_person")
        self.assertEqual(pii.classify_field("ssn"), "identifier")
        self.assertEqual(pii.classify_field("occupancy_rate"), "aggregate_safe")

    def test_pseudonymize_stable_and_salted(self) -> None:
        a = pii.pseudonymize("Jane Doe", "RUN-1")
        b = pii.pseudonymize("Jane Doe", "RUN-1")
        c = pii.pseudonymize("Jane Doe", "RUN-2")
        self.assertEqual(a, b)          # stable within a run
        self.assertNotEqual(a, c)       # salted across runs
        self.assertTrue(a.startswith("Tenant "))

    def test_scan_for_leaks_paths_only(self) -> None:
        payload = {"rows": [{"note": "paid by Jane Doe"}, {"note": "clean"}]}
        leaks = pii.scan_for_leaks(payload, ["Jane Doe"])
        self.assertEqual(leaks, ["rows[0].note"])

    def test_assert_safe_tenant_id(self) -> None:
        self.assertEqual(pii.assert_safe_tenant_id("acme-fund-1"), [])
        self.assertTrue(pii.assert_safe_tenant_id(""))
        self.assertTrue(pii.assert_safe_tenant_id("../etc/passwd"))


class TestProvenancePiiRule(unittest.TestCase):
    def _build(self, field_name: str):
        return provenance.build_provenance(
            field_name=field_name,
            source_document_id="RR-001",
            source_ref_anchor="occupancy",
            skill_name="rent-roll-to-database",
            skill_version="0.1.0",
            run_id="R1",
            as_of="2026-05-29",
            source_cell_address="RR-001!Detail!D14",
            source_text_span="98.1%",
        )

    def test_non_pii_keeps_span(self) -> None:
        p = self._build("occupancy_rate")
        self.assertEqual(p["source_text_span"], "98.1%")
        self.assertEqual(p["redaction_status"], "raw")
        self.assertEqual(p["source_ref"], "data-room/RR-001#occupancy")

    def test_pii_field_drops_span_keeps_locator(self) -> None:
        p = self._build("tenant_name")
        self.assertIsNone(p["source_text_span"])
        self.assertEqual(p["redaction_status"], "redacted")
        self.assertEqual(p["source_cell_address"], "RR-001!Detail!D14")  # locator kept

    def test_superset_of_warehouse_columns(self) -> None:
        p = self._build("occupancy_rate")
        for col in provenance.WAREHOUSE_PROVENANCE_COLUMNS:
            self.assertIn(col, p, "provenance missing warehouse column %s" % col)


class TestRubricGrading(unittest.TestCase):
    def test_weakest_link(self) -> None:
        self.assertEqual(rubric.weakest_link({"a": "A", "b": "B", "c": "A"}), "B")
        self.assertEqual(rubric.weakest_link({"a": "A", "b": "C"}), "C")
        self.assertEqual(rubric.weakest_link({"a": "A"}), "A")

    def test_gate_blocks_on_critical(self) -> None:
        g = rubric.gate("A", 99.0, ["pii_redaction_breach"])
        self.assertFalse(g["merge_ready"])
        self.assertTrue(g["pii_redaction_breach"])
        self.assertTrue(g["blocked"])

    def test_gate_merge_ready(self) -> None:
        g = rubric.gate("B", 88.0, [])
        self.assertTrue(g["merge_ready"])
        self.assertFalse(g["production_ready"])  # B grade can't be prod-ready


class TestProfiles(unittest.TestCase):
    def test_all_profiles_resolve(self) -> None:
        for p in profiles.TARGET_PROFILES:
            tables = profiles.profile_tables(p)
            self.assertTrue(tables, "profile %s resolved to no tables" % p)

    def test_hybrid_composes(self) -> None:
        tables = profiles.profile_tables("hybrid_recommended")
        self.assertIn("cre_raw_extraction_record", tables)
        self.assertIn("cre_property", tables)
        self.assertIn("fact_operating_statement", tables)


class TestSchemaEnums(unittest.TestCase):
    def test_charge_categories_align_with_account_map(self) -> None:
        for cat in schema.CHARGE_CATEGORIES:
            self.assertIn(cat, accounts.CHARGE_CATEGORY_TO_ACCOUNT)


if __name__ == "__main__":
    unittest.main()
