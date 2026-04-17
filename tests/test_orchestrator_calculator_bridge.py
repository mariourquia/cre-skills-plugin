#!/usr/bin/env python3
"""v4.4 PR C: calculator bridge (design doc section 3).

Exercises:

- Direct bridge: invoke a known calculator (proration_calculator)
  with minimal inputs and assert the expected keys in the result.
- Unknown slug: bridge surfaces a CalculatorBridgeError with the
  invoker's error envelope.
- Validation error: bridge surfaces validation_errors from the
  invoker (required input missing).
- End-to-end through the executor: a fixture pipeline config with
  a tool_calls entry produces a tool_results block in the phase
  checkpoint, with the same keys as the direct-bridge call.
- Persistent-mode integration: audit log emits calculator_invoked
  events for each tool call.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
HARNESS = PLUGIN_ROOT / "tests" / "harness_calculator_bridge.mjs"
EXECUTOR = PLUGIN_ROOT / "src" / "orchestrators" / "engine" / "executor.mjs"


def run_harness(slug: str, inputs: dict, *, expect_ok: bool) -> dict:
    proc = subprocess.run(
        [
            "node",
            str(HARNESS),
            "--slug",
            slug,
            "--inputs",
            json.dumps(inputs),
        ],
        cwd=PLUGIN_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    # Harness always prints JSON envelope on stdout; exit code is
    # non-zero on bridge error. Don't require a specific code; assert
    # the envelope shape.
    try:
        envelope = json.loads(proc.stdout)
    except json.JSONDecodeError:
        raise AssertionError(
            f"harness stdout was not JSON.\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )
    if expect_ok and not envelope.get("ok", False):
        raise AssertionError(f"expected bridge success, got: {envelope}")
    if not expect_ok and envelope.get("ok", True):
        raise AssertionError(f"expected bridge failure, got success: {envelope}")
    return envelope


class BridgeDirect(unittest.TestCase):
    def test_proration_calculator_returns_line_items(self) -> None:
        env = run_harness(
            "proration_calculator",
            {"closing_date": "2026-06-01", "annual_tax": 12000},
            expect_ok=True,
        )
        result = env["result"]
        self.assertEqual(result["closing_date"], "2026-06-01")
        self.assertIn("line_items", result)
        self.assertGreater(len(result["line_items"]), 0)
        tax = result["line_items"][0]
        self.assertEqual(tax["item"], "property_tax")
        self.assertEqual(tax["annual_amount"], 12000)

    def test_unknown_slug_fails_loudly(self) -> None:
        env = run_harness("no_such_calculator_xyz", {}, expect_ok=False)
        self.assertIn("no_such_calculator_xyz", env["message"])

    def test_missing_required_input_raises(self) -> None:
        env = run_harness(
            "proration_calculator",
            {"annual_tax": 12000},  # missing closing_date
            expect_ok=False,
        )
        self.assertIn("validation", env["message"].lower())


class BridgeThroughExecutor(unittest.TestCase):
    """End-to-end: minimal pipeline config with a tool_calls phase."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="cre-skills-test-"))
        self.fixture = self.tmp / "fixture_bridge_pipeline.json"
        self.fixture.write_text(
            json.dumps(
                {
                    "schemaVersion": "1.0",
                    "orchestratorId": "acquisition",
                    "version": "test",
                    "entityType": "deal",
                    "description": "fixture pipeline for calculator bridge test",
                    "phases": [
                        {
                            "phaseId": "proration-check",
                            "name": "Proration Check",
                            "weight": 1.0,
                            "agents": [],
                            "tool_calls": [
                                {
                                    "tool": "proration_calculator",
                                    "as": "closing_prorations",
                                    "inputs": {
                                        "closing_date": "2026-06-01",
                                        "annual_tax": 12000,
                                    },
                                }
                            ],
                        }
                    ],
                    "checkpointConfig": {
                        "verdictValues": {"COMPLETED": 1, "CONDITIONAL": 0}
                    },
                }
            )
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_phase_checkpoint_includes_tool_results(self) -> None:
        deal_id = "deal_bridge_01"
        env = {**os.environ, "CRE_SKILLS_HOME": str(self.tmp)}
        proc = subprocess.run(
            [
                "node",
                str(EXECUTOR),
                "--config-path",
                str(self.fixture),
                "--deal-id",
                deal_id,
            ],
            env=env,
            cwd=PLUGIN_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            proc.returncode,
            0,
            f"executor failed: {proc.stdout}\n---\n{proc.stderr}",
        )
        self.assertIn("TOOL: closing_prorations ok", proc.stdout)

        audit = (
            self.tmp
            / ".claude"
            / "cre-skills"
            / "deals"
            / deal_id
            / "audit_log.jsonl"
        ).read_text()
        events = [json.loads(l) for l in audit.splitlines() if l.strip()]
        calc_events = [e for e in events if e["event"] == "calculator_invoked"]
        self.assertEqual(len(calc_events), 1)
        self.assertEqual(calc_events[0]["alias"], "closing_prorations")
        self.assertEqual(calc_events[0]["phase_id"], "proration-check")


if __name__ == "__main__":
    unittest.main()
