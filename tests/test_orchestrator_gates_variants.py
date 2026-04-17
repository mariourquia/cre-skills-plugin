#!/usr/bin/env python3
"""v4.4 PR B: variant loader + approval gates (design doc sections 2 + 4).

End-to-end through the executor:

- --strategy value_add applies phase weight overrides (underwriting
  weight flips from 0.2 to 0.3 in dry-run output).
- --strategy value_add adds the capex_plan_sign_off approval gate on
  the underwriting phase. First real run blocks with AWAITING_APPROVAL
  before underwriting dispatches any agents.
- approve-gate.mjs flips the gate to approved; resuming the same
  deal-id clears the block and subsequent phases run.
- The audit log records gate_opened on block and gate_approved on
  sign-off, in order, with no bytes rewritten.
- An unknown --strategy with no variant dir is tolerated (warn, no
  overlay).
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
EXECUTOR = PLUGIN_ROOT / "src" / "orchestrators" / "engine" / "executor.mjs"
APPROVE = PLUGIN_ROOT / "src" / "orchestrators" / "engine" / "approve-gate.mjs"


def run_node(
    script: Path,
    cre_skills_home: Path,
    *cli_args: str,
    expect_exit_code: int | None = 0,
) -> subprocess.CompletedProcess:
    env = {**os.environ, "CRE_SKILLS_HOME": str(cre_skills_home)}
    proc = subprocess.run(
        ["node", str(script), *cli_args],
        env=env,
        cwd=PLUGIN_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if expect_exit_code is not None and proc.returncode != expect_exit_code:
        raise AssertionError(
            f"{script.name} exited {proc.returncode}, expected {expect_exit_code}\n"
            f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )
    return proc


class VariantLoader(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="cre-skills-test-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_value_add_overlay_changes_underwriting_weight(self) -> None:
        """Dry-run prints the post-overlay weight for underwriting."""
        base = run_node(
            EXECUTOR, self.tmp, "--pipeline", "acquisition", "--dry-run"
        )
        overlay = run_node(
            EXECUTOR,
            self.tmp,
            "--pipeline",
            "acquisition",
            "--strategy",
            "value_add",
            "--dry-run",
        )
        self.assertIn("underwriting) [weight=0.2]", base.stdout)
        self.assertIn("underwriting) [weight=0.3]", overlay.stdout)
        self.assertIn("Applied variant overlay: value_add", overlay.stdout)

    def test_unknown_strategy_is_tolerated(self) -> None:
        proc = run_node(
            EXECUTOR,
            self.tmp,
            "--pipeline",
            "acquisition",
            "--strategy",
            "no_such_variant",
            "--dry-run",
        )
        # No exception; dry run still completes.
        self.assertIn("Phase execution order", proc.stdout)
        self.assertIn("No variant directory", proc.stdout)


class ApprovalGateBlocksThenClears(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="cre-skills-test-"))
        self.deal_id = "deal_gate_01"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def deal_path(self) -> Path:
        return (
            self.tmp
            / ".claude"
            / "cre-skills"
            / "deals"
            / self.deal_id
        )

    def test_blocks_on_underwriting_then_clears_on_approval(self) -> None:
        # First run: hits the gate, halts with AWAITING_APPROVAL.
        proc1 = run_node(
            EXECUTOR,
            self.tmp,
            "--pipeline",
            "acquisition",
            "--strategy",
            "value_add",
            "--deal-id",
            self.deal_id,
        )
        self.assertIn("awaits approval on gate(s)", proc1.stdout)
        self.assertIn("value_add.capex_plan_sign_off", proc1.stdout)
        # Summary must report a pause, not a kill, on AWAITING_APPROVAL.
        self.assertIn("Pipeline paused, awaiting human approval", proc1.stdout)
        self.assertNotIn("Deal is not viable at current terms", proc1.stdout)

        state = json.loads((self.deal_path() / "state.json").read_text())
        self.assertEqual(
            state["verdicts_by_phase"]["underwriting"]["verdict"],
            "AWAITING_APPROVAL",
        )
        # Agents must NOT have executed for underwriting — gate fires
        # before dispatch. Financing / legal / closing must not appear
        # in verdicts_by_phase yet.
        self.assertNotIn("financing", state["verdicts_by_phase"])
        self.assertNotIn("legal", state["verdicts_by_phase"])
        self.assertNotIn("closing", state["verdicts_by_phase"])

        # Gate is recorded pending in approval_gate_log.
        gates = state["approval_gate_log"]
        self.assertEqual(len(gates), 1)
        self.assertEqual(gates[0]["gate_id"], "value_add.capex_plan_sign_off")
        self.assertEqual(gates[0]["status"], "pending")

        # Audit log recorded gate_opened and phase_blocked for underwriting.
        audit = (self.deal_path() / "audit_log.jsonl").read_text()
        events = [json.loads(l) for l in audit.splitlines() if l.strip()]
        event_types = [e["event"] for e in events]
        self.assertIn("gate_opened", event_types)
        self.assertIn("phase_blocked", event_types)
        audit_bytes_before_approval = (self.deal_path() / "audit_log.jsonl").read_bytes()

        # Operator clears the gate.
        run_node(
            APPROVE,
            self.tmp,
            "--deal-id",
            self.deal_id,
            "--gate-id",
            "value_add.capex_plan_sign_off",
            "--status",
            "approved",
            "--approved-by",
            "asset_manager",
        )

        state = json.loads((self.deal_path() / "state.json").read_text())
        self.assertEqual(state["approval_gate_log"][0]["status"], "approved")
        self.assertEqual(
            state["approval_gate_log"][0]["approved_by"], "asset_manager"
        )

        # Audit log must have appended (never rewritten) after approval.
        audit_bytes_after_approval = (self.deal_path() / "audit_log.jsonl").read_bytes()
        self.assertTrue(
            audit_bytes_after_approval.startswith(audit_bytes_before_approval),
            "audit log prefix mutated after gate approval (append-only broken)",
        )
        prefix_sha_before = hashlib.sha256(audit_bytes_before_approval).hexdigest()
        prefix_sha_after = hashlib.sha256(
            audit_bytes_after_approval[: len(audit_bytes_before_approval)]
        ).hexdigest()
        self.assertEqual(prefix_sha_before, prefix_sha_after)

        # Resume: underwriting now runs, remaining phases follow.
        proc2 = run_node(
            EXECUTOR,
            self.tmp,
            "--pipeline",
            "acquisition",
            "--strategy",
            "value_add",
            "--deal-id",
            self.deal_id,
        )
        self.assertIn("[RESUME]", proc2.stdout)

        state = json.loads((self.deal_path() / "state.json").read_text())
        for phase_id in [
            "due-diligence",
            "underwriting",
            "financing",
            "legal",
            "closing",
        ]:
            self.assertEqual(
                state["verdicts_by_phase"][phase_id]["verdict"],
                "PROCEED",
                f"phase {phase_id} should be PROCEED after gate clear",
            )


if __name__ == "__main__":
    unittest.main()
