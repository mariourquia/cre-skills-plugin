"""Structural smoke test for the portable ZIP release artifact.

This test validates that the portable ZIP (``dist/cre-skills-portable.zip``)
packaged by ``tools/package/package-portable.ts`` carries a structurally
coherent skills/ tree and does not leak runtime files that portable targets
(Codex / Gemini / Grok / Manus) do not support.

Scope
-----
This is **structural** coverage only:

- the ZIP opens cleanly;
- every source skill directory under ``src/skills/`` that the portable target
  profile (``config/targets/portable.yaml``) does not explicitly exclude has a
  matching ``skills/<slug>/SKILL.md`` in the extracted artifact;
- each extracted ``SKILL.md`` parses and carries the portable-contract
  frontmatter (``name``, ``description``) — portable **strips** ``slug``,
  ``status``, ``version`` by design per the target profile, so this test
  records their absence rather than asserting their presence;
- no MCP server, orchestrator runtime, or Python calculator leaks into the
  artifact (the portable target profile sets ``mcp_server.include``,
  ``orchestrators.include``, and ``calculators.include`` to ``false``).

What is NOT covered
-------------------
Cross-runtime invocation (Codex / Gemini / Grok / Manus actually loading and
running a skill from the extracted ZIP) is **not** exercised by this test.
That remains a documented gap — tracked in
``docs/install_smoke_test_matrix.md`` row "Portable ZIP" — until a cross-CLI
harness lands.
"""
from __future__ import annotations

import re
import unittest
import zipfile
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent.parent
DIST_ZIP = PLUGIN_ROOT / "dist" / "cre-skills-portable.zip"
SRC_SKILLS = PLUGIN_ROOT / "src" / "skills"
PORTABLE_TARGET_CONFIG = PLUGIN_ROOT / "config" / "targets" / "portable.yaml"

# Skills the portable target profile explicitly excludes. Kept in sync with
# ``config/targets/portable.yaml`` and the build-target normalizer. The
# residential_multifamily subsystem ships only via Claude Code / Desktop
# surfaces today because its overlay contract is not portable-safe.
PORTABLE_EXCLUDED_SKILL_SLUGS = frozenset({"residential_multifamily"})

# Per portable target profile: skills/allowed_frontmatter is {name, description}
# and strip_fields = {slug, version, status, category, targets}. This test
# pins both, so a silent change to the profile fails loudly here.
PORTABLE_REQUIRED_FRONTMATTER_FIELDS = frozenset({"name", "description"})
PORTABLE_STRIPPED_FRONTMATTER_FIELDS = frozenset(
    {"slug", "version", "status", "category", "targets"}
)


def _zip_exists() -> bool:
    return DIST_ZIP.is_file()


def _extract_frontmatter(md_text: str) -> dict[str, str]:
    """Parse the leading ``---`` YAML-ish frontmatter block.

    The portable SKILL.md files have a tiny flat frontmatter (name + description
    only), so a stdlib regex parser is sufficient and avoids a PyYAML
    dependency in the smoke-test venv.
    """
    if not md_text.startswith("---\n"):
        return {}
    try:
        end = md_text.index("\n---\n", 4)
    except ValueError:
        return {}
    out: dict[str, str] = {}
    for line in md_text[4:end].splitlines():
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if not m:
            continue
        key = m.group(1)
        val = m.group(2).strip().strip('"').strip("'")
        out[key] = val
    return out


class TestPortableZipArtifact(unittest.TestCase):
    """Structural assertions against the packaged ZIP itself."""

    @classmethod
    def setUpClass(cls) -> None:
        if not _zip_exists():
            raise unittest.SkipTest(
                f"Portable ZIP not found at {DIST_ZIP.relative_to(PLUGIN_ROOT)}. "
                "Build it with: npx tsx tools/package/package-portable.ts"
            )
        cls.zf = zipfile.ZipFile(DIST_ZIP, "r")
        cls.names = cls.zf.namelist()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.zf.close()

    def test_zip_is_openable_and_nonempty(self) -> None:
        self.assertGreater(
            len(self.names), 0, "portable ZIP extracted an empty namelist"
        )
        # zipfile.testzip returns the first bad entry name or None; None = OK.
        bad = self.zf.testzip()
        self.assertIsNone(bad, f"zip CRC failure on {bad!r}")

    def test_skills_tree_mirrors_source_minus_excluded(self) -> None:
        """Every non-excluded source skill has a matching SKILL.md in the ZIP."""
        zip_skill_slugs = {
            name.split("/", 2)[1]
            for name in self.names
            if name.startswith("skills/") and name.endswith("/SKILL.md")
        }
        src_skill_slugs = {
            p.name
            for p in SRC_SKILLS.iterdir()
            if p.is_dir() and (p / "SKILL.md").is_file()
        }
        expected = src_skill_slugs - PORTABLE_EXCLUDED_SKILL_SLUGS

        missing = sorted(expected - zip_skill_slugs)
        leaked_excluded = sorted(PORTABLE_EXCLUDED_SKILL_SLUGS & zip_skill_slugs)
        self.assertFalse(
            missing,
            f"portable ZIP missing SKILL.md for: {missing}",
        )
        self.assertFalse(
            leaked_excluded,
            f"portable ZIP leaked excluded slugs: {leaked_excluded}. "
            "Update PORTABLE_EXCLUDED_SKILL_SLUGS or the portable target profile.",
        )

    def test_skill_files_carry_portable_frontmatter(self) -> None:
        """Each extracted SKILL.md parses and exposes the portable contract."""
        failures: list[str] = []
        seen = 0
        for name in self.names:
            if not (name.startswith("skills/") and name.endswith("/SKILL.md")):
                continue
            seen += 1
            with self.zf.open(name) as fh:
                text = fh.read().decode("utf-8")
            fm = _extract_frontmatter(text)
            if not fm:
                failures.append(f"{name}: unparseable frontmatter")
                continue
            missing = PORTABLE_REQUIRED_FRONTMATTER_FIELDS - fm.keys()
            if missing:
                failures.append(f"{name}: missing required fields {sorted(missing)}")
            leaked = PORTABLE_STRIPPED_FRONTMATTER_FIELDS & fm.keys()
            if leaked:
                # Portable target strips these by profile; a leak means the
                # build-target normalizer regressed.
                failures.append(
                    f"{name}: leaked stripped fields {sorted(leaked)} "
                    "(portable target should remove them)"
                )
        self.assertGreater(seen, 0, "no SKILL.md entries in portable ZIP")
        self.assertFalse(failures, "\n  " + "\n  ".join(failures))

    def test_zip_does_not_leak_mcp_server(self) -> None:
        self.assertNotIn(
            "mcp-server.mjs",
            self.names,
            "MCP server is not part of the portable surface; normalizer leaked it",
        )

    def test_zip_does_not_leak_orchestrator_runtime(self) -> None:
        orch_entries = [n for n in self.names if n.startswith("orchestrators/")]
        self.assertFalse(
            orch_entries,
            f"portable ZIP leaked orchestrator runtime files: {orch_entries[:5]}",
        )

    def test_zip_does_not_leak_python_calculators(self) -> None:
        # Portable target sets calculators.include=false. Any .py file is a
        # regression (skills/ tree is .md; no other .py should be present).
        py_entries = [n for n in self.names if n.endswith(".py")]
        self.assertFalse(
            py_entries,
            f"portable ZIP leaked Python calculator/runtime files: {py_entries[:5]}",
        )


@unittest.expectedFailure
class TestPortableZipCrossRuntimeInvocation(unittest.TestCase):
    """Cross-runtime invocation is an explicit gap — tracked in
    docs/install_smoke_test_matrix.md. Remains xfail until a cross-CLI
    harness exists."""

    def test_extract_and_invoke_in_foreign_runtime(self) -> None:
        self.fail(
            "Cross-runtime invocation (Codex / Gemini / Grok / Manus) is not "
            "wired; see docs/install_smoke_test_matrix.md row 'Portable ZIP'."
        )


if __name__ == "__main__":
    unittest.main()
