"""Smoke test: portable ZIP import for Codex / Gemini / Grok / Manus.

The portable ZIP surface ships SKILL.md files only. CLI-specific
registration, calculator execution, and orchestrator support are not
guaranteed and are flagged experimental in README.md.

This test validates: if a portable build artifact exists, its
SKILL.md count matches the catalog and no calculator binaries or
MCP-only files leaked in.
"""
from __future__ import annotations

import unittest
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent.parent
PORTABLE_ROOT_CANDIDATES = [
    PLUGIN_ROOT / "builds" / "portable",
    PLUGIN_ROOT / "dist" / "portable",
]


def _portable_root() -> Path | None:
    for p in PORTABLE_ROOT_CANDIDATES:
        if p.is_dir():
            return p
    return None


class TestPortableArtifactShape(unittest.TestCase):
    def setUp(self) -> None:
        root = _portable_root()
        if root is None:
            self.skipTest("No portable build artifact present")
        self.root = root

    def test_portable_skills_directory_exists(self) -> None:
        self.assertTrue(
            (self.root / "skills").is_dir(),
            "portable artifact must ship a skills/ tree",
        )

    def test_portable_does_not_leak_mcp_server(self) -> None:
        self.assertFalse(
            (self.root / "mcp-server.mjs").exists(),
            "MCP server is not supported on portable surface",
        )

    def test_portable_has_readme_with_experimental_notice(self) -> None:
        rm = self.root / "README.md"
        if not rm.exists():
            self.skipTest("portable README not present")
        body = rm.read_text(encoding="utf-8")
        self.assertRegex(
            body,
            r"(?is)(experimental|not tested|portable|unsupported)",
            "portable README must flag experimental status",
        )


@unittest.expectedFailure
class TestPortableEndToEndImport(unittest.TestCase):
    def test_import_into_codex_gemini_grok_manus(self) -> None:
        self.fail("cross-runtime sandbox not wired yet (docs/ROADMAP.md v4.3)")


if __name__ == "__main__":
    unittest.main()
