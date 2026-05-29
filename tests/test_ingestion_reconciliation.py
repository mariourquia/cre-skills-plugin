#!/usr/bin/env python3
"""Rent roll <-> T-12 tie-out tests.

Proves the classifier separates clean / mapping / timing / missing on distinct
deterministic signatures, that a forced tie is impossible (tie_status is only
tied|untied and untied dimensions surface residual_unexplained == |variance|),
and that untied dimensions route to human review.

Run: python -m pytest tests/test_ingestion_reconciliation.py
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


def load(name: str) -> dict:
    with open(os.path.join(FX, name), "r", encoding="utf-8") as fh:
        return json.load(fh)


def reconcile(fixture: str) -> dict:
    fx = load(fixture)
    rr = N.calculate_normalize_tokens(fx["rent_roll"])
    t12 = N.calculate_normalize_tokens(fx["t12"])
    return R.calculate_reconcile_rent_roll_t12({"run_id": "RUN-T", "as_of": "2026-05-31", "rent_roll": rr, "t12": t12})


def dims(result: dict) -> dict:
    return {d["dimension"]: d for d in result["dimensions"]}


class TestNeverForce(unittest.TestCase):
    def test_tie_status_only_tied_or_untied(self) -> None:
        for fixture in ("tieout_clean.json", "tieout_mapping_variance.json",
                        "tieout_timing_variance.json", "tieout_missing_tenant.json"):
            res = reconcile(fixture)
            for d in res["dimensions"]:
                self.assertIn(d["tie_status"], ("tied", "untied"), fixture)

    def test_untied_surfaces_residual(self) -> None:
        # On the mapping fixture, an untied non-one-sided dimension must report
        # residual_unexplained == |variance| (the gap is surfaced, not absorbed).
        res = reconcile("tieout_mapping_variance.json")
        base = dims(res)["base_rent"]
        self.assertEqual(base["tie_status"], "untied")
        self.assertEqual(base["residual_unexplained"], abs(base["variance"]))
        self.assertGreater(res["summary"]["residual_unexplained_total"], 0)


class TestClean(unittest.TestCase):
    def setUp(self) -> None:
        self.d = dims(reconcile("tieout_clean.json"))

    def test_revenue_dimensions_tie(self) -> None:
        self.assertEqual(self.d["base_rent"]["tie_status"], "tied")
        self.assertEqual(self.d["other_rental"]["tie_status"], "tied")
        self.assertEqual(self.d["egi_bridge"]["tie_status"], "tied")

    def test_basis_labeled(self) -> None:
        self.assertEqual(self.d["base_rent"]["basis"]["rent_roll"], "annualized_contractual_in_place")
        self.assertEqual(self.d["base_rent"]["basis"]["t12"], "recognized_accrual_annualized")


class TestMapping(unittest.TestCase):
    def setUp(self) -> None:
        self.res = reconcile("tieout_mapping_variance.json")
        self.d = dims(self.res)

    def test_total_ties_categories_offset_classified_mapping(self) -> None:
        self.assertEqual(self.d["egi_bridge"]["tie_status"], "tied")
        self.assertEqual(self.d["base_rent"]["difference_type"], "mapping")
        self.assertEqual(self.d["other_rental"]["difference_type"], "mapping")

    def test_routes_to_human_review(self) -> None:
        reasons = {r["reason"] for r in self.res["human_review_items"]}
        self.assertIn("mapping", reasons)


class TestTiming(unittest.TestCase):
    def setUp(self) -> None:
        self.d = dims(reconcile("tieout_timing_variance.json"))

    def test_recovery_trueup_classified_timing(self) -> None:
        # EGI does not tie (T-12 recovery exceeds contractual run-rate) and the
        # recovery drift is timing, not a mapping error.
        self.assertEqual(self.d["egi_bridge"]["tie_status"], "untied")
        self.assertEqual(self.d["other_rental"]["difference_type"], "timing")


class TestMissing(unittest.TestCase):
    def setUp(self) -> None:
        self.d = dims(reconcile("tieout_missing_tenant.json"))

    def test_income_gap_classified_missing(self) -> None:
        # Rent roll base exceeds T-12 base and the total does not tie -> missing.
        self.assertEqual(self.d["egi_bridge"]["tie_status"], "untied")
        self.assertEqual(self.d["base_rent"]["difference_type"], "missing")


if __name__ == "__main__":
    unittest.main()
