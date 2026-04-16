"""Smoke test: upgrade from v4.1.x to v4.2.0.

Scope: installer scripts (Install.ps1, install.sh, Install.command)
handle the case where a prior-version plugin.json already lives at
`~/.claude/plugins/cache/local/cre-skills-plugin/`. The expected
behavior is:
  1. Detect the prior install.
  2. Preserve user config (settings.json, telemetry-init.json).
  3. Replace plugin files with current version.
  4. Update registration + MCP config atomically.

Until a sandbox runner lands, this test asserts that the installer
scripts contain the control-flow branches for the upgrade scenario.
"""
from __future__ import annotations

import os
import re
import unittest
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent.parent


class TestUpgradeScenarioInShellInstaller(unittest.TestCase):
    def test_install_sh_detects_existing_plugin(self) -> None:
        body = (PLUGIN_ROOT / "scripts" / "install.sh").read_text(encoding="utf-8")
        self.assertRegex(
            body,
            r"(?is)(existing|already installed|upgrade|reinstall|plugin_version)",
            "install.sh must contain upgrade-detection branch",
        )

    def test_install_sh_reads_prior_version(self) -> None:
        body = (PLUGIN_ROOT / "scripts" / "install.sh").read_text(encoding="utf-8")
        self.assertIn(
            "plugin.json",
            body,
            "install.sh must read plugin.json to detect installed version",
        )


class TestUpgradeScenarioInPowerShellInstaller(unittest.TestCase):
    def test_install_ps1_detects_existing_plugin(self) -> None:
        body = (PLUGIN_ROOT / "scripts" / "Install.ps1").read_text(encoding="utf-8")
        self.assertRegex(
            body,
            r"(?is)(existing|already installed|upgrade|reinstall|PluginVersion)",
            "Install.ps1 must contain upgrade-detection branch",
        )


class TestUpgradeScenarioInMacCommand(unittest.TestCase):
    def test_install_command_detects_existing_plugin(self) -> None:
        body = (PLUGIN_ROOT / "Install.command").read_text(encoding="utf-8")
        self.assertRegex(
            body,
            r"(?is)(existing|already installed|upgrade|reinstall|PLUGIN_VERSION)",
            "Install.command must contain upgrade-detection branch",
        )


@unittest.expectedFailure
class TestUpgradeEndToEndOnSandbox(unittest.TestCase):
    """End-to-end upgrade run requires a sandbox Linux/macOS/Windows
    runner with Claude Code CLI present. Marked expectedFailure until
    the sandbox runner lands (docs/ROADMAP.md v4.3)."""

    def test_upgrade_preserves_user_config(self) -> None:
        self.fail("sandbox runner not wired yet")


if __name__ == "__main__":
    unittest.main()
