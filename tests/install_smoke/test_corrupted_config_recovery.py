"""Smoke test: recovery from a corrupted Claude Code config.

Scope: when `~/.claude/settings.json` or `~/.claude/mcp.json` is
malformed (bad JSON, missing fields, truncated), the installer should
detect + back up + rewrite rather than proceed blindly.

Scaffolding: assert the installer scripts contain JSON-validation
branches and back-up-on-corrupt behavior. End-to-end recovery is
future work.
"""
from __future__ import annotations

import unittest
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent.parent


class TestCorruptConfigDetection(unittest.TestCase):
    def test_install_sh_validates_settings_json(self) -> None:
        body = (PLUGIN_ROOT / "scripts" / "install.sh").read_text(encoding="utf-8")
        # Look for a JSON-parsing invocation.
        self.assertRegex(
            body,
            r"(?is)(json\.load|jq\b|python.*json|node.*JSON\.parse)",
            "install.sh must validate settings.json before editing",
        )

    @unittest.expectedFailure
    def test_install_command_backs_up_before_edit_DEFECT(self) -> None:
        """KNOWN GAP: Install.command edits settings.json in place without
        a backup copy. Acceptance: writes settings.json.bak-<timestamp>
        before any mutating edit."""
        body = (PLUGIN_ROOT / "Install.command").read_text(encoding="utf-8")
        self.assertRegex(
            body,
            r"(?is)(\.bak|backup|cp\s+-[a-z]*\s+\S*settings)",
            "Install.command must back up settings before editing",
        )


@unittest.expectedFailure
class TestEndToEndCorruptRecovery(unittest.TestCase):
    def test_rewrites_after_detecting_bad_json(self) -> None:
        self.fail("sandbox runner not wired yet (docs/ROADMAP.md v4.3)")


if __name__ == "__main__":
    unittest.main()
