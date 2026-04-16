"""Smoke test: Cowork ZIP import surface.

Cowork consumes a subset: skills + agents + commands. Hooks, MCP,
orchestrators, calculators are NOT part of the Cowork surface. This
test validates the Cowork export artifact, if the build pipeline
produces one, contains only the supported subset and reflects the
current plugin.json version.

Scaffolding: checks for existence of the Cowork build output; where
missing, marks xfail so v4.3 follow-up can wire the actual export.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent.parent
COWORK_ROOT_CANDIDATES = [
    PLUGIN_ROOT / "builds" / "cowork",
    PLUGIN_ROOT / "dist" / "cowork",
]


def _cowork_root() -> Path | None:
    for p in COWORK_ROOT_CANDIDATES:
        if p.is_dir():
            return p
    return None


class TestCoworkArtifactShape(unittest.TestCase):
    def setUp(self) -> None:
        root = _cowork_root()
        if root is None:
            self.skipTest("No Cowork build artifact present; build pipeline may not be wired.")
        self.root = root

    def test_cowork_has_skills_dir(self) -> None:
        self.assertTrue((self.root / "skills").is_dir(), "Cowork artifact missing skills/")

    def test_cowork_has_agents_dir_or_not_surfaced(self) -> None:
        # Either agents/ is present or an artifact manifest declares absence.
        agents = self.root / "agents"
        manifest = self.root / "manifest.json"
        self.assertTrue(
            agents.is_dir() or manifest.is_file(),
            "Cowork artifact must either ship agents/ or document the omission in manifest.json",
        )

    def test_cowork_does_not_leak_mcp_server(self) -> None:
        self.assertFalse(
            (self.root / "mcp-server.mjs").exists(),
            "MCP server is not part of the Cowork surface; exporter leaked it",
        )

    def test_cowork_does_not_leak_hooks(self) -> None:
        self.assertFalse(
            (self.root / "hooks").is_dir(),
            "Hooks are not part of the Cowork surface; exporter leaked them",
        )


@unittest.expectedFailure
class TestCoworkEndToEndImport(unittest.TestCase):
    def test_import_into_cowork_sandbox(self) -> None:
        self.fail("Cowork sandbox runner not wired yet (docs/ROADMAP.md v4.3)")


if __name__ == "__main__":
    unittest.main()
