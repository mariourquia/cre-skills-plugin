#!/usr/bin/env python3
"""Regression gates for installer hardening fixes.

Covers BOM handling and Node argv indexing in Install.ps1, plus the defensive
JSON readers in scripts that consume files written by Windows PowerShell 5.1
(which writes UTF-8 with BOM via `Set-Content -Encoding UTF8`).
"""
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = PLUGIN_ROOT / "scripts"
INSTALL_PS1 = SCRIPTS / "Install.ps1"
SMOKE_TEST = SCRIPTS / "installer_smoke_test.py"
DIAGNOSTIC = SCRIPTS / "diagnostic_report.py"


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestInstallPs1BomFix(unittest.TestCase):
    """Install.ps1 must write JSON files without BOM regardless of PS version."""

    def setUp(self):
        self.contents = INSTALL_PS1.read_text(encoding="utf-8")

    def test_write_utf8_nobom_helper_defined(self):
        self.assertIn("function Write-Utf8NoBom", self.contents)
        self.assertIn("System.Text.UTF8Encoding($false)", self.contents,
                      "Helper must construct UTF8Encoding with includeByteOrderMark=$false")

    def test_no_set_content_utf8_for_json_targets(self):
        # The three JSON paths the smoke test parses must go through Write-Utf8NoBom.
        for target in ("InstalledPluginsFile", "SettingsFile", "DesktopConfigFile"):
            for line in self.contents.splitlines():
                if (
                    f"${target}" in line
                    and "Set-Content" in line
                    and "-Encoding UTF8" in line
                ):
                    self.fail(
                        f"${target} must not be written via 'Set-Content -Encoding UTF8' "
                        "(BOM in PS 5.1 breaks Python's json.load). Use Write-Utf8NoBom."
                    )

    def test_node_script_uses_correct_argv_indices(self):
        # process.argv[0]=node, [1]=script, [2]=first user arg.
        # cp must be argv[2] (DesktopConfigFile), sp must be argv[3] (mcpServerPath).
        self.assertIn("const cp = process.argv[2];", self.contents)
        self.assertIn("const sp = process.argv[3];", self.contents)
        self.assertNotIn("const cp = process.argv[1];", self.contents)

    def test_node_script_strips_bom(self):
        # Defensive BOM-strip in the Node helper that edits claude_desktop_config.json.
        self.assertIn("0xFEFF", self.contents,
                      "Node helper should defensively strip a leading BOM before JSON.parse")


class TestSmokeTestBomTolerance(unittest.TestCase):
    """The smoke test's load_json must tolerate files written with BOM."""

    def test_load_json_uses_utf8_sig(self):
        contents = SMOKE_TEST.read_text(encoding="utf-8")
        self.assertIn('encoding="utf-8-sig"', contents,
                      "load_json must use utf-8-sig so BOM-laden Windows PS 5.1 files parse")

    def test_load_json_accepts_bom_file(self):
        smoke = _load_module("installer_smoke_test", SMOKE_TEST)
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "settings.json"
            p.write_bytes(b"\xef\xbb\xbf" + json.dumps({"enabledPlugins": {}}).encode("utf-8"))
            data = smoke.load_json(p)
            self.assertIsNotNone(data, "load_json must accept a BOM-prefixed UTF-8 file")
            self.assertEqual(data, {"enabledPlugins": {}})


class TestDiagnosticReportBomTolerance(unittest.TestCase):
    """Diagnostic report reads ~/.claude files that may have BOM on Windows."""

    def test_diagnostic_uses_utf8_sig(self):
        contents = DIAGNOSTIC.read_text(encoding="utf-8")
        # Both reads of files in claude_home should be defensive.
        self.assertNotIn('read_text(encoding="utf-8")', contents,
                         "diagnostic_report.py reads ~/.claude files; must use utf-8-sig")


class TestHooksMatcherTightness(unittest.TestCase):
    """The PostToolUse matcher must stay scoped to the Read tool only.

    Claude Code matches `matcher` against tool names (glob), not paths.
    Broadening it to `""` or to additional tools would cause the telemetry
    hook to spawn a Node process on every call to those tools, which is
    pure overhead because the script's path filter would discard them.
    """

    def test_post_tool_use_matcher_is_read_only(self):
        hooks_path = PLUGIN_ROOT / "src" / "hooks" / "hooks.json"
        data = json.loads(hooks_path.read_text(encoding="utf-8"))
        post_tool_use = data["hooks"]["PostToolUse"]
        self.assertEqual(len(post_tool_use), 1,
                         "Only one PostToolUse handler expected (telemetry-capture)")
        matcher = post_tool_use[0]["matcher"]
        self.assertEqual(matcher, "Read",
                         f"PostToolUse matcher must be exactly 'Read'; got {matcher!r}. "
                         "Broadening it spawns Node on every call to other tools.")


if __name__ == "__main__":
    unittest.main()
