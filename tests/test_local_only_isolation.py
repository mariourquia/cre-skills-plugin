#!/usr/bin/env python3
"""Network isolation tests for feedback_mode=local_only.

The privacy contract is: when a user sets feedback.mode = "local_only",
no plugin code path should call fetch() to a remote endpoint. These tests
verify that contract from two angles:

1. Static: the gate `feedbackMode !== 'local_only'` is present in the only
   hook that initiates a remote call (telemetry-init.mjs).
2. Runtime: spawn telemetry-init.mjs with a temp HOME containing
   feedback.mode=local_only and a populated outbox; assert no fetch is
   invoked even though entries are pending.

Adding a new fetch-calling code path requires either gating it on
feedbackMode or updating these tests with the new gate.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
HOOKS_DIR = PLUGIN_ROOT / "src" / "hooks"
TELEMETRY_INIT = HOOKS_DIR / "telemetry-init.mjs"
FEEDBACK_OUTBOX = HOOKS_DIR / "feedback-outbox.mjs"


def _node_available() -> bool:
    return shutil.which("node") is not None


class TestStaticLocalOnlyGate(unittest.TestCase):
    """The drainOutbox call site must be gated by feedbackMode !== 'local_only'."""

    def test_drainoutbox_call_is_gated(self):
        src = TELEMETRY_INIT.read_text(encoding="utf-8")
        self.assertIn(
            "feedbackMode !== 'local_only'", src,
            "telemetry-init.mjs must gate the drainOutbox call on "
            "feedbackMode !== 'local_only' to honor the privacy contract."
        )
        # The gate must precede the drainOutbox call (rough check: the gate
        # appears in the source before the only `drainOutbox(` call site).
        gate_idx = src.index("feedbackMode !== 'local_only'")
        drain_idx = src.index("drainOutbox(")
        self.assertLess(
            gate_idx, drain_idx,
            "The local_only gate must appear before the drainOutbox(...) call"
        )

    def test_only_outbox_module_initiates_fetch(self):
        # Currently fetch() is only called inside feedback-outbox.mjs::drain.
        # If a new file under src/hooks/ adds a fetch() call, this test will
        # alert us to add an analogous local_only gate test for it.
        offenders = []
        for f in HOOKS_DIR.glob("*.mjs"):
            if f.name == "feedback-outbox.mjs":
                continue
            text = f.read_text(encoding="utf-8")
            # Look for a real fetch invocation, not the word in a comment
            for line in text.splitlines():
                stripped = line.strip()
                if stripped.startswith(("//", "*", "/*")):
                    continue
                if "fetch(" in stripped and "globalThis.fetch" not in stripped:
                    offenders.append(f"{f.name}: {stripped}")
        self.assertEqual(
            offenders, [],
            "A new hook initiates fetch(). Add a local_only gate test for it: "
            + str(offenders)
        )


@unittest.skipUnless(_node_available(), "node not installed")
class TestRuntimeLocalOnlyIsolation(unittest.TestCase):
    """Runtime: with local_only config and pending outbox, fetch is never called."""

    def _run_with_mocked_fetch(self, mode: str) -> dict:
        """Spawn telemetry-init.mjs in a sandboxed HOME with fetch instrumented.

        Returns dict with keys:
            fetch_calls: count of fetch invocations the wrapper observed
            stdout, stderr, returncode: subprocess result details
            outbox_after: list of entries left in outbox after run
        """
        tmp_home = tempfile.mkdtemp()
        try:
            cre_dir = Path(tmp_home) / ".cre-skills"
            cre_dir.mkdir()
            config = {
                "telemetry": True,
                "survey": False,
                "feedback": {
                    "mode": mode,
                    "include_context": True,
                    "backend_url": "https://example.invalid/feedback",
                },
                "anonymousId": "test-anon",
                "firstRunComplete": True,
                "firstRunAt": "2026-04-15",
                "version": "4.1.2",
            }
            (cre_dir / "config.json").write_text(json.dumps(config), encoding="utf-8")
            # Seed outbox with one pending entry so drain() would call fetch
            # if the local_only gate is broken.
            outbox_entry = {
                "type": "feedback",
                "message": "test",
                "_outbox": {
                    "queued_at": "2026-04-15T00:00:00Z",
                    "attempts": 0,
                    "last_attempt_at": None,
                },
            }
            (cre_dir / "outbox.jsonl").write_text(
                json.dumps(outbox_entry) + "\n", encoding="utf-8"
            )

            # Wrapper script: install a recording fetch shim, dynamic-import the
            # hook, then await microtasks so the fire-and-forget drain completes.
            fetch_log = Path(tmp_home) / "fetch-log.txt"
            wrapper = textwrap.dedent(f"""
                let fetchCalls = 0;
                globalThis.fetch = async (url, init) => {{
                  fetchCalls++;
                  await import('fs').then(m => m.appendFileSync(
                    {json.dumps(str(fetch_log))}, url + '\\n', 'utf8'
                  ));
                  return new Response('blocked', {{ status: 599 }});
                }};
                await import({json.dumps(str(TELEMETRY_INIT))});
                // Yield to allow the fire-and-forget drain to settle.
                await new Promise(r => setTimeout(r, 1500));
                process.stdout.write('FETCH_CALLS=' + fetchCalls + '\\n');
            """)
            wrapper_path = Path(tmp_home) / "wrapper.mjs"
            wrapper_path.write_text(wrapper, encoding="utf-8")

            env = dict(os.environ, HOME=tmp_home)
            result = subprocess.run(
                ["node", str(wrapper_path)],
                env=env, capture_output=True, text=True, timeout=15,
            )
            fetch_calls = 0
            for line in result.stdout.splitlines():
                if line.startswith("FETCH_CALLS="):
                    fetch_calls = int(line.split("=", 1)[1])
            outbox_after = []
            outbox_path = cre_dir / "outbox.jsonl"
            if outbox_path.exists():
                for line in outbox_path.read_text(encoding="utf-8").splitlines():
                    if line.strip():
                        outbox_after.append(json.loads(line))
            return {
                "fetch_calls": fetch_calls,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "outbox_after": outbox_after,
            }
        finally:
            shutil.rmtree(tmp_home, ignore_errors=True)

    def test_local_only_never_calls_fetch(self):
        result = self._run_with_mocked_fetch("local_only")
        self.assertEqual(
            result["returncode"], 0,
            f"telemetry-init.mjs failed: {result['stderr']}"
        )
        self.assertEqual(
            result["fetch_calls"], 0,
            f"local_only mode invoked fetch {result['fetch_calls']} time(s). "
            f"stdout={result['stdout']!r} stderr={result['stderr']!r}"
        )

    def test_non_local_mode_does_call_fetch(self):
        # Sanity check: if the mode is anonymous_remote, fetch IS called.
        # If this test fails, the runtime harness itself is broken (not the gate).
        result = self._run_with_mocked_fetch("anonymous_remote")
        self.assertEqual(
            result["returncode"], 0,
            f"telemetry-init.mjs failed: {result['stderr']}"
        )
        self.assertGreaterEqual(
            result["fetch_calls"], 1,
            "Test harness sanity: anonymous_remote with a pending outbox "
            "must invoke fetch at least once. If this fails, the wrapper "
            "is not being applied correctly."
        )


if __name__ == "__main__":
    unittest.main()
