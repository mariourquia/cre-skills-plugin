#!/usr/bin/env python3
"""v4.4 PR A: persistent deal state + audit log (design doc sections 1 + 5).

Shells out to the executor with a temp CRE_SKILLS_HOME so no files land
in the operator's real home directory. Exercises:

- First run with --deal-id creates state.json conforming to the schema.
- A second run with the same --deal-id (after partial progress) resumes
  from the recorded verdicts instead of re-executing cleared phases.
- audit_log.jsonl grows monotonically: appending never rewrites prior
  bytes, each line parses as JSON, required keys are present.
- Deal-id + mismatched pipeline exits non-zero (refuses to mix
  pipelines under one deal).
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
EXECUTOR = PLUGIN_ROOT / "src" / "orchestrators" / "engine" / "executor.mjs"


def run_executor(
    cre_skills_home: Path,
    *cli_args: str,
    expect_exit_code: int | None = 0,
) -> subprocess.CompletedProcess:
    env = {**os.environ, "CRE_SKILLS_HOME": str(cre_skills_home)}
    proc = subprocess.run(
        ["node", str(EXECUTOR), *cli_args],
        env=env,
        cwd=PLUGIN_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if expect_exit_code is not None and proc.returncode != expect_exit_code:
        raise AssertionError(
            f"executor exited {proc.returncode}, expected {expect_exit_code}\n"
            f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )
    return proc


class DealStateRoundtrip(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="cre-skills-test-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def deal_path(self, deal_id: str) -> Path:
        return self.tmp / ".claude" / "cre-skills" / "deals" / deal_id

    def test_first_run_creates_valid_state_and_audit_log(self) -> None:
        deal_id = "deal_roundtrip_01"
        run_executor(self.tmp, "--pipeline", "acquisition", "--deal-id", deal_id)

        state_path = self.deal_path(deal_id) / "state.json"
        audit_path = self.deal_path(deal_id) / "audit_log.jsonl"
        self.assertTrue(state_path.is_file(), f"expected state at {state_path}")
        self.assertTrue(audit_path.is_file(), f"expected audit log at {audit_path}")

        state = json.loads(state_path.read_text())
        self.assertEqual(state["deal_id"], deal_id)
        self.assertEqual(state["pipeline"], "acquisition")
        self.assertIn("run_id", state)
        self.assertIn("verdicts_by_phase", state)
        # Executor stub emits COMPLETED -> normalized PROCEED for every phase.
        for phase_id in [
            "due-diligence",
            "underwriting",
            "financing",
            "legal",
            "closing",
        ]:
            self.assertIn(phase_id, state["verdicts_by_phase"])
            self.assertEqual(
                state["verdicts_by_phase"][phase_id]["verdict"],
                "PROCEED",
                f"phase {phase_id} should be PROCEED in stub execution",
            )

        # Audit log: every line parses; we see pipeline_started and
        # pipeline_completed bracketing phase events.
        lines = [json.loads(l) for l in audit_path.read_text().splitlines() if l.strip()]
        events = [e["event"] for e in lines]
        self.assertEqual(events[0], "pipeline_started")
        self.assertEqual(events[-1], "pipeline_completed")
        self.assertEqual(events.count("phase_started"), 5)
        self.assertEqual(events.count("phase_completed"), 5)
        for e in lines:
            for required in ("timestamp", "event", "actor", "deal_id"):
                self.assertIn(required, e)

    def test_second_run_resumes_from_state(self) -> None:
        deal_id = "deal_resume_01"
        run_executor(self.tmp, "--pipeline", "acquisition", "--deal-id", deal_id)

        # Delete the legacy-checkpoint sidecar to prove resume is driven
        # by state.json, not by the checkpoint file.
        legacy_dir = self.tmp / ".cre-skills" / "checkpoints"
        if legacy_dir.exists():
            shutil.rmtree(legacy_dir)

        proc = run_executor(
            self.tmp, "--pipeline", "acquisition", "--deal-id", deal_id
        )
        self.assertIn("[RESUME]", proc.stdout)
        self.assertIn("already-resolved phase", proc.stdout)

    def test_pipeline_mismatch_rejected(self) -> None:
        deal_id = "deal_mismatch_01"
        run_executor(self.tmp, "--pipeline", "acquisition", "--deal-id", deal_id)
        proc = run_executor(
            self.tmp,
            "--pipeline",
            "capital-stack",
            "--deal-id",
            deal_id,
            expect_exit_code=3,
        )
        self.assertIn("Refusing to mix pipelines", proc.stderr)


class AuditLogAppendOnly(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="cre-skills-test-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_second_run_never_rewrites_prior_bytes(self) -> None:
        deal_id = "deal_append_01"
        run_executor(self.tmp, "--pipeline", "acquisition", "--deal-id", deal_id)

        audit = (
            self.tmp
            / ".claude"
            / "cre-skills"
            / "deals"
            / deal_id
            / "audit_log.jsonl"
        )
        before_bytes = audit.read_bytes()
        before_sha = hashlib.sha256(before_bytes).hexdigest()

        run_executor(self.tmp, "--pipeline", "acquisition", "--deal-id", deal_id)

        after_bytes = audit.read_bytes()
        # Prefix must match exactly (append-only invariant).
        self.assertTrue(
            after_bytes.startswith(before_bytes),
            "audit log prefix mutated between runs: append-only invariant violated",
        )
        # Strict growth: second run appends at least one resume event.
        self.assertGreater(len(after_bytes), len(before_bytes))
        after_prefix_sha = hashlib.sha256(after_bytes[: len(before_bytes)]).hexdigest()
        self.assertEqual(after_prefix_sha, before_sha)


class NonPersistentModeUnchanged(unittest.TestCase):
    """Back-compat: omitting --deal-id keeps the legacy ephemeral flow."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="cre-skills-test-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_no_deal_id_no_deal_dir(self) -> None:
        run_executor(self.tmp, "--pipeline", "acquisition")
        deals_dir = self.tmp / ".claude" / "cre-skills" / "deals"
        self.assertFalse(
            deals_dir.exists(),
            "executor without --deal-id must not create deal state files",
        )


if __name__ == "__main__":
    unittest.main()
