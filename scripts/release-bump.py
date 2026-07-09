#!/usr/bin/env python3
"""Bump the plugin version across every mechanical pin in one shot.

Usage:
    python3 scripts/release-bump.py --version 5.2.2 [--root PATH] [--no-regen]

The 5.2.0 -> 5.2.1 release showed the failure mode this tool removes: the
version lives in several files that must move together, and hand-editing
missed some (the committed AMOS sample kept plugin_version 5.2.0, breaking
tests/test_amos_manifest.py on every fresh checkout).

Mechanical rewrites (exact current-version literals, counted and verified):
  - .claude-plugin/plugin.json        "version" field (the source of truth)
  - scripts/install.sh                banner / comment / fallback literals
  - docs/INSTALL.md                   binary asset filenames
  - docs/install-desktop.md           binary asset filenames
  - docs/install-guide.md             "Version X.Y.Z |" line
  - README.md                         "vX.Y.Z ..." header line

Regenerated afterwards (skipped with --no-regen, e.g. in tests):
  - src/catalog/catalog.yaml + dist/catalog.json    scripts/catalog-build.py
  - docs/integrations/amos-skill-manifest.sample.json
        scripts/amos-manifest-build.py --emit-sample

Deliberately NOT touched (historical facts or prose that needs a human):
CHANGELOG.md, docs/ROADMAP.md, docs/DATA_GRADES.md, release notes. A manual
checklist for those is printed at the end. tests/test_version_pins.py is the
tripwire that fails the suite if a mechanical pin is ever missed again.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")

# Files rewritten by exact old-version literal replacement. install.sh and the
# install docs must only ever reference the CURRENT version, so a plain
# replace-all of the old literal is safe there (enforced by the tripwire test).
LITERAL_TARGETS = (
    "scripts/install.sh",
    "docs/INSTALL.md",
    "docs/install-desktop.md",
    "docs/install-guide.md",
    "README.md",
)

CHECKLIST = """
Manual follow-ups (prose, not mechanical -- do these before tagging):
  1. CHANGELOG.md: add the {new} section (top, above the previous release).
  2. README.md line ~9: update the release tagline text next to v{new}.
  3. docs/ROADMAP.md: update 'Current release' if this is a minor/major.
  4. Build + upload release binaries named cre-skills-plugin-v{new}.dmg /
     cre-skills-plugin-v{new}-setup.exe (docs link to these filenames).
  5. Run: python3 -m pytest && python3 -m pytest tests/
  6. Tag only after both suites are green: git tag v{new}
"""


def bump_plugin_json(path: Path, old: str, new: str) -> None:
    """Rewrite the version field in place, preserving file formatting."""
    text = path.read_text(encoding="utf-8")
    needle = f'"version": "{old}"'
    if text.count(needle) != 1:
        sys.exit(f"FAIL: expected exactly one {needle!r} in {path}")
    path.write_text(text.replace(needle, f'"version": "{new}"'), encoding="utf-8")
    parsed = json.loads(path.read_text(encoding="utf-8"))
    if parsed.get("version") != new:
        sys.exit(f"FAIL: {path} did not parse back with version {new}")


def bump_literals(path: Path, old: str, new: str) -> int:
    """Replace every exact old-version literal in path; return the count."""
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count == 0:
        sys.exit(
            f"FAIL: {path} contains no {old!r} literal. Either the pin map in "
            "scripts/release-bump.py is stale or the file already drifted; "
            "fix that before bumping."
        )
    path.write_text(text.replace(old, new), encoding="utf-8")
    return count


def regenerate(root: Path) -> None:
    """Rebuild the version-stamped generated artifacts."""
    for cmd in (
        [sys.executable, str(root / "scripts" / "catalog-build.py")],
        [sys.executable, str(root / "scripts" / "amos-manifest-build.py"), "--emit-sample"],
    ):
        result = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
        if result.returncode != 0:
            sys.exit(f"FAIL: {' '.join(cmd[1:])} exited {result.returncode}:\n{result.stderr[-2000:]}")
        print(result.stdout.strip().splitlines()[-1] if result.stdout.strip() else f"ran {cmd[1]}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bump the plugin version across all mechanical pins")
    parser.add_argument("--version", required=True, help="New version, e.g. 5.2.2")
    parser.add_argument("--root", default=None, help="Repo root (tests point this at a fixture tree)")
    parser.add_argument("--no-regen", action="store_true", help="Skip catalog/sample regeneration")
    args = parser.parse_args()

    new = args.version
    if not SEMVER.match(new):
        sys.exit(f"FAIL: {new!r} is not valid semver")

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent
    plugin_json = root / ".claude-plugin" / "plugin.json"
    old = json.loads(plugin_json.read_text(encoding="utf-8"))["version"]
    if old == new:
        sys.exit(f"FAIL: already at {new}")

    bump_plugin_json(plugin_json, old, new)
    print(f"{plugin_json.relative_to(root)}: {old} -> {new}")
    for rel in LITERAL_TARGETS:
        count = bump_literals(root / rel, old, new)
        print(f"{rel}: {count} literal(s) updated")

    if args.no_regen:
        print("skipped artifact regeneration (--no-regen)")
    else:
        regenerate(root)

    print(CHECKLIST.format(new=new))


if __name__ == "__main__":
    main()
