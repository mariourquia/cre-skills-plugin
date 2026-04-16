"""Smoke test: uninstall then reinstall clean.

Scope: after an uninstall, re-running the installer restores the full
plugin state (cache directory, installed_plugins.json entry, MCP config
entry) without stale fragments from the prior install.

Scaffolding only today — validates installer scripts contain uninstall
branches and that the reinstall path is idempotent (detects absence and
creates, vs. failing on missing-state).
"""
from __future__ import annotations

import unittest
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent.parent


class TestUninstallBranchesPresent(unittest.TestCase):
    """KNOWN GAP: installer scripts do not yet expose an uninstall flow.
    Marked expectedFailure until v4.3 closes the gap. The acceptance
    criterion is an `--uninstall` flag (or equivalent) on install.sh
    and Install.command that removes the plugin cache and drops the
    MCP registration atomically."""

    @unittest.expectedFailure
    def test_install_sh_has_uninstall_flag_DEFECT(self) -> None:
        body = (PLUGIN_ROOT / "scripts" / "install.sh").read_text(encoding="utf-8")
        self.assertRegex(
            body,
            r"(?is)(--uninstall|uninstall\s*\(\)|\$ACTION.*uninstall)",
            "install.sh must expose an uninstall flow",
        )

    @unittest.expectedFailure
    def test_install_command_has_uninstall_flag_DEFECT(self) -> None:
        body = (PLUGIN_ROOT / "Install.command").read_text(encoding="utf-8")
        self.assertRegex(
            body,
            r"(?is)(--uninstall|uninstall|REMOVE_PLUGIN)",
            "Install.command must expose an uninstall flow",
        )


class TestReinstallIsIdempotent(unittest.TestCase):
    def test_install_sh_handles_missing_prior_install(self) -> None:
        body = (PLUGIN_ROOT / "scripts" / "install.sh").read_text(encoding="utf-8")
        # Check for defensive directory creation.
        self.assertIn("mkdir -p", body, "install.sh must be idempotent on fresh install")


@unittest.expectedFailure
class TestEndToEndUninstallReinstall(unittest.TestCase):
    def test_uninstall_reinstall_round_trip(self) -> None:
        self.fail("sandbox runner not wired yet (docs/ROADMAP.md v4.3)")


if __name__ == "__main__":
    unittest.main()
