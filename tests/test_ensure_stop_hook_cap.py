#!/usr/bin/env python3
"""Tests for scripts/ensure_stop_hook_cap.py.

Verifies the Stop-hook block-cap enforcer is idempotent, raise-only, and safe:
  (a) missing settings.json        -> created with cap "100"
  (b) cap below the floor          -> raised to "100"
  (c) cap >= floor (e.g. 500)      -> left unchanged (lets cre-skills-pro win)
  (d) invalid JSON                 -> never corrupted; exit 0
  (e) all other keys preserved

Every case uses a temp claude-home; the real ~/.claude is never touched. The
helper must always exit 0 (it is wired into install.sh / verify-install.sh,
which run under `set -e` and must not abort on it).
"""
import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
HELPER = PLUGIN_ROOT / "scripts" / "ensure_stop_hook_cap.py"


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cap_mod = _load_module("ensure_stop_hook_cap", HELPER)


def _run(claude_home: Path):
    """Invoke ensure_cap, capturing (rc, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        rc = cap_mod.ensure_cap(claude_home)
    return rc, out.getvalue(), err.getvalue()


class TestEnsureStopHookCap(unittest.TestCase):
    def test_helper_constants(self):
        self.assertEqual(cap_mod.FLOOR, 100)
        self.assertEqual(cap_mod.ENV_KEY, "CLAUDE_CODE_STOP_HOOK_BLOCK_CAP")

    # (a) missing file -> created with cap 100 ------------------------------
    def test_missing_file_created_with_cap_100(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / ".claude"  # does not exist yet
            settings = home / "settings.json"
            self.assertFalse(settings.exists())

            rc, out, _ = _run(home)

            self.assertEqual(rc, 0)
            self.assertTrue(settings.is_file(), "settings.json should be created")
            data = json.loads(settings.read_text(encoding="utf-8"))
            self.assertEqual(data["env"]["CLAUDE_CODE_STOP_HOOK_BLOCK_CAP"], "100")
            self.assertIsInstance(
                data["env"]["CLAUDE_CODE_STOP_HOOK_BLOCK_CAP"], str,
                "cap must be stored as a STRING (env-block values are strings)",
            )
            self.assertIn("stop-hook block cap: raised to 100 (was unset)", out)

    # (b) below floor -> raised --------------------------------------------
    def test_below_floor_raised(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / ".claude"
            home.mkdir(parents=True)
            settings = home / "settings.json"
            settings.write_text(
                json.dumps({"env": {"CLAUDE_CODE_STOP_HOOK_BLOCK_CAP": "9"}}),
                encoding="utf-8",
            )

            rc, out, _ = _run(home)

            self.assertEqual(rc, 0)
            data = json.loads(settings.read_text(encoding="utf-8"))
            self.assertEqual(data["env"]["CLAUDE_CODE_STOP_HOOK_BLOCK_CAP"], "100")
            self.assertIn("stop-hook block cap: raised to 100 (was 9)", out)

    def test_integer_below_floor_raised(self):
        # Tolerate an int (not just a string) below the floor and raise it.
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / ".claude"
            home.mkdir(parents=True)
            settings = home / "settings.json"
            settings.write_text(
                json.dumps({"env": {"CLAUDE_CODE_STOP_HOOK_BLOCK_CAP": 50}}),
                encoding="utf-8",
            )

            rc, out, _ = _run(home)

            self.assertEqual(rc, 0)
            data = json.loads(settings.read_text(encoding="utf-8"))
            self.assertEqual(data["env"]["CLAUDE_CODE_STOP_HOOK_BLOCK_CAP"], "100")
            self.assertIn("raised to 100 (was 50)", out)

    def test_non_numeric_value_raised(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / ".claude"
            home.mkdir(parents=True)
            settings = home / "settings.json"
            settings.write_text(
                json.dumps({"env": {"CLAUDE_CODE_STOP_HOOK_BLOCK_CAP": "lots"}}),
                encoding="utf-8",
            )

            rc, out, _ = _run(home)

            self.assertEqual(rc, 0)
            data = json.loads(settings.read_text(encoding="utf-8"))
            self.assertEqual(data["env"]["CLAUDE_CODE_STOP_HOOK_BLOCK_CAP"], "100")
            self.assertIn("raised to 100 (was lots)", out)

    # (c) >= floor -> unchanged --------------------------------------------
    def test_at_or_above_floor_unchanged(self):
        # cre-skills-pro sets 500; raise-only must leave it so the higher wins.
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / ".claude"
            home.mkdir(parents=True)
            settings = home / "settings.json"
            original = {"env": {"CLAUDE_CODE_STOP_HOOK_BLOCK_CAP": "500"}}
            settings.write_text(json.dumps(original), encoding="utf-8")
            before = settings.read_text(encoding="utf-8")

            rc, out, _ = _run(home)

            self.assertEqual(rc, 0)
            self.assertEqual(
                settings.read_text(encoding="utf-8"), before,
                "file must be byte-identical when cap already >= floor",
            )
            self.assertIn("stop-hook block cap: already 500 (>=100), left as-is", out)

    def test_exactly_floor_unchanged(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / ".claude"
            home.mkdir(parents=True)
            settings = home / "settings.json"
            settings.write_text(
                json.dumps({"env": {"CLAUDE_CODE_STOP_HOOK_BLOCK_CAP": "100"}}),
                encoding="utf-8",
            )
            before = settings.read_text(encoding="utf-8")

            rc, out, _ = _run(home)

            self.assertEqual(rc, 0)
            self.assertEqual(settings.read_text(encoding="utf-8"), before)
            self.assertIn("already 100 (>=100), left as-is", out)

    # (d) invalid JSON -> not corrupted ------------------------------------
    def test_invalid_json_not_corrupted(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / ".claude"
            home.mkdir(parents=True)
            settings = home / "settings.json"
            garbage = '{ this is not valid json,,, '
            settings.write_text(garbage, encoding="utf-8")

            rc, out, err = _run(home)

            self.assertEqual(rc, 0, "must never crash the caller")
            self.assertEqual(
                settings.read_text(encoding="utf-8"), garbage,
                "invalid JSON must be left exactly as-is, never overwritten",
            )
            self.assertEqual(out, "", "no status line on the unparseable path")
            self.assertIn("not valid JSON", err)

    def test_non_object_json_not_corrupted(self):
        # A valid JSON array/scalar at top level can't take a key -> leave it.
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / ".claude"
            home.mkdir(parents=True)
            settings = home / "settings.json"
            settings.write_text("[1, 2, 3]", encoding="utf-8")

            rc, _, err = _run(home)

            self.assertEqual(rc, 0)
            self.assertEqual(settings.read_text(encoding="utf-8"), "[1, 2, 3]")
            self.assertIn("not valid JSON", err)

    # (e) other keys preserved ---------------------------------------------
    def test_other_keys_preserved(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / ".claude"
            home.mkdir(parents=True)
            settings = home / "settings.json"
            original = {
                "enabledPlugins": {"cre-skills@local": True},
                "env": {
                    "SOME_OTHER_VAR": "keepme",
                    "CLAUDE_CODE_STOP_HOOK_BLOCK_CAP": "9",
                },
                "model": "claude-opus-4",
                "nested": {"a": [1, 2, {"b": "c"}]},
            }
            settings.write_text(json.dumps(original), encoding="utf-8")

            rc, _, _ = _run(home)

            self.assertEqual(rc, 0)
            data = json.loads(settings.read_text(encoding="utf-8"))
            # Cap raised...
            self.assertEqual(data["env"]["CLAUDE_CODE_STOP_HOOK_BLOCK_CAP"], "100")
            # ...everything else byte-for-byte intact.
            self.assertEqual(data["enabledPlugins"], {"cre-skills@local": True})
            self.assertEqual(data["env"]["SOME_OTHER_VAR"], "keepme")
            self.assertEqual(data["model"], "claude-opus-4")
            self.assertEqual(data["nested"], {"a": [1, 2, {"b": "c"}]})

    def test_preserves_existing_env_when_cap_missing(self):
        # env exists with other vars but no cap key -> add cap, keep the rest.
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / ".claude"
            home.mkdir(parents=True)
            settings = home / "settings.json"
            settings.write_text(
                json.dumps({"env": {"FOO": "bar"}}), encoding="utf-8"
            )

            rc, out, _ = _run(home)

            self.assertEqual(rc, 0)
            data = json.loads(settings.read_text(encoding="utf-8"))
            self.assertEqual(data["env"]["FOO"], "bar")
            self.assertEqual(data["env"]["CLAUDE_CODE_STOP_HOOK_BLOCK_CAP"], "100")
            self.assertIn("raised to 100 (was unset)", out)

    # Idempotence: run twice, second run is a no-op -------------------------
    def test_idempotent_second_run_noop(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / ".claude"
            settings = home / "settings.json"

            _run(home)  # first run creates + raises
            after_first = settings.read_text(encoding="utf-8")
            rc, out, _ = _run(home)  # second run
            after_second = settings.read_text(encoding="utf-8")

            self.assertEqual(rc, 0)
            self.assertEqual(after_first, after_second, "second run must be a no-op")
            self.assertIn("already 100 (>=100), left as-is", out)

    # Output is exactly one line on the happy paths ------------------------
    def test_single_status_line(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td) / ".claude"
            _, out, _ = _run(home)
            self.assertEqual(
                len([ln for ln in out.splitlines() if ln.strip()]), 1,
                "exactly one status line expected",
            )


if __name__ == "__main__":
    unittest.main()
