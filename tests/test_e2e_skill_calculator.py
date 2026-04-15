#!/usr/bin/env python3
"""End-to-end test: skill router -> calculator registry -> calculator invocation.

The existing tests/test_calculator_correctness.py exercises calculator math in
isolation (importing the Python modules directly). This file exercises the
plumbing that connects a user query to a calculator at runtime:

    user query
        -> src/routing/skill-dispatcher.mjs (Node, catalog-driven)
            -> skill slug
                -> scripts/calculator-registry.json (used_by)
                    -> scripts/calculator-invoker.py
                        -> src/calculators/<calc>.py

A regression in any of those layers will fail this test even though the
calculator math itself is correct.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import unittest
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
DISPATCHER = PLUGIN_ROOT / "src" / "routing" / "skill-dispatcher.mjs"
INVOKER = PLUGIN_ROOT / "scripts" / "calculator-invoker.py"
REGISTRY = PLUGIN_ROOT / "scripts" / "calculator-registry.json"


def _node_available() -> bool:
    return shutil.which("node") is not None


def _route(query: str) -> dict:
    result = subprocess.run(
        ["node", str(DISPATCHER), query],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(f"dispatcher failed: {result.stderr}")
    return json.loads(result.stdout)


def _calculator_for_skill(slug: str) -> str | None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    for calc_slug, defn in registry["calculators"].items():
        if slug in defn.get("used_by", []):
            return calc_slug
    return None


def _invoke_calculator(slug: str, inputs: dict) -> dict:
    result = subprocess.run(
        ["python3", str(INVOKER), slug, "--json", json.dumps(inputs)],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"calculator-invoker failed for {slug}: stderr={result.stderr!r} stdout={result.stdout!r}"
        )
    return json.loads(result.stdout)


class TestCalculatorRegistryPaths(unittest.TestCase):
    """Every script path in the registry must point to an existing file.

    Caught a real bug in 2026-04: registry pointed to scripts/calculators/
    after the calculator move to src/calculators/, breaking the entire
    skill -> calculator runtime path silently because no test exercised it.
    """

    def test_all_calculator_scripts_exist(self):
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        missing = []
        for slug, defn in registry["calculators"].items():
            script_path = PLUGIN_ROOT / defn["script"]
            if not script_path.exists():
                missing.append(f"{slug} -> {defn['script']}")
        self.assertEqual(
            missing, [],
            "calculator-registry.json references nonexistent scripts: " + str(missing)
        )


@unittest.skipUnless(_node_available(), "node not installed")
class TestSkillToCalculatorRouting(unittest.TestCase):
    """Verify a query reaches its calculator end-to-end."""

    def test_screen_query_routes_to_deal_quick_screen_with_calculator(self):
        routed = _route("screen this deal")
        rec = routed["recommendation"]
        self.assertEqual(
            rec["skill"], "deal-quick-screen",
            f"Expected dispatcher to route 'screen this deal' to deal-quick-screen; got {rec['skill']}"
        )
        self.assertTrue(
            rec.get("has_calculator"),
            "deal-quick-screen must declare a calculator in the catalog"
        )

    def test_routed_skill_resolves_to_calculator_in_registry(self):
        routed = _route("screen this deal")
        skill = routed["recommendation"]["skill"]
        calc_slug = _calculator_for_skill(skill)
        self.assertIsNotNone(
            calc_slug,
            f"Skill {skill} reports has_calculator=true but no calculator-registry entry "
            f"lists it under used_by"
        )

    def test_invoking_routed_calculator_produces_valid_output(self):
        routed = _route("screen this deal")
        skill = routed["recommendation"]["skill"]
        calc_slug = _calculator_for_skill(skill)

        sample_inputs = {
            "purchase_price": 8_500_000,
            "noi": 510_000,
            "units_or_sf": 48,
            "unit_type": "units",
            "market_rent_per_unit": 1350,
            "in_place_rent_per_unit": 1100,
            "loan_amount": 5_525_000,
            "rate": 0.065,
            "amort_years": 30,
            "replacement_cost_estimate": 10_500_000,
            "property_type": "multifamily",
        }
        output = _invoke_calculator(calc_slug, sample_inputs)

        # Calculator-invoker wraps results; the wrapper signals success/failure.
        self.assertNotIn("error", output,
                         f"calculator-invoker returned an error: {output.get('error')}")

        metrics = output.get("metrics") or output.get("result", {}).get("metrics", {})
        self.assertIn("going_in_cap_rate", metrics,
                      f"Expected metrics.going_in_cap_rate in output; got keys={list(output)}")
        self.assertAlmostEqual(metrics["going_in_cap_rate"], 0.06, places=2)


if __name__ == "__main__":
    unittest.main()
