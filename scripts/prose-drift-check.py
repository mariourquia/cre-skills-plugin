#!/usr/bin/env python3
"""
prose-drift-check.py - detect hardcoded count references in prose that drift
from the canonical catalog.

The catalog is the single source of truth for how many skills / agents /
calculators ship in the plugin. scripts/catalog-generate.py keeps the
tables inside `<!-- CATALOG:STATS:START -->` / `END` markers in sync. But
prose elsewhere in README.md and docs/ uses the same counts and drifts
silently when a skill is added.

This script scans a curated list of current-state docs, counts items in
`src/catalog/catalog.yaml`, and fails when a prose count does not match.

Scope and design choices:
- Only strong-signal patterns are checked (see PATTERNS below) - patterns
  with low false-positive rate. Generic "X skills," in a sentence is NOT
  checked because sub-counts appear frequently in prose.
- Lines between `<!-- CATALOG:STATS:START -->` and `<!-- CATALOG:STATS:END -->`
  are skipped (already managed by catalog-generate.py).
- Lines between `<!-- PROSE-DRIFT:IGNORE-START -->` and
  `<!-- PROSE-DRIFT:IGNORE-END -->` are skipped (escape hatch for
  historical "What's New in vX.Y.Z" sections that intentionally quote
  an older count).
- docs/releases/ is NOT scanned - those are historical artifacts.
- CHANGELOG.md is NOT scanned - entries are version-scoped by design.

Usage:
    python scripts/prose-drift-check.py              # check, exit 1 on drift
    python scripts/prose-drift-check.py --verbose    # also print the catalog counts

CI: wired into .github/workflows/ci.yml as a final "prose drift" step.
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG = REPO_ROOT / "src" / "catalog" / "catalog.yaml"

SCAN_PATHS = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "docs" / "INSTALL.md",
    REPO_ROOT / "docs" / "WHAT-TO-USE-WHEN.md",
    REPO_ROOT / "docs" / "install-cowork.md",
    REPO_ROOT / "docs" / "install-desktop.md",
    REPO_ROOT / "docs" / "install-guide.md",
]

PATTERNS = [
    (re.compile(r"\b(\d{2,4})\s+institutional-grade\b"), "skill"),
    (re.compile(r"\b(\d{2,4})\s+CRE\s+skills\b"), "skill"),
    (re.compile(r"\b(\d{2,4})\s+process\s+documents\b"), "skill"),
    (re.compile(r"\b(\d{2,4})\s+skill\s+directories\b"), "skill"),
    (re.compile(r"\b(\d{2,4})\s+expert\s+agents\b"), "agent"),
    (re.compile(r"\b(\d{2,4})\s+Python\s+calculators\b"), "calculator"),
    (re.compile(r"\b(\d{2,4})\s+reference\s+files\b"), "reference_file"),
]

STATS_START = "CATALOG:STATS:START"
STATS_END = "CATALOG:STATS:END"
IGNORE_START = "PROSE-DRIFT:IGNORE-START"
IGNORE_END = "PROSE-DRIFT:IGNORE-END"


def count_catalog_items() -> dict:
    """Count items from the catalog. Reference-file counting mirrors
    scripts/catalog-generate.py so the two scripts agree."""
    data = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    counts = {"skill": 0, "agent": 0, "calculator": 0, "command": 0}
    for item in data.get("items", []):
        t = item.get("type")
        if t in counts:
            counts[t] += 1

    ref_count = 0
    skills_dir = REPO_ROOT / "src" / "skills"
    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue
        refs_dir = skill_dir / "references"
        if refs_dir.exists():
            ref_count += sum(1 for f in refs_dir.rglob("*") if f.is_file())
    counts["reference_file"] = ref_count
    return counts


def scan_file(path: Path, counts: dict) -> list:
    mismatches = []
    in_stats = False
    in_ignore = False
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if STATS_START in raw:
            in_stats = True
            continue
        if STATS_END in raw:
            in_stats = False
            continue
        if IGNORE_START in raw:
            in_ignore = True
            continue
        if IGNORE_END in raw:
            in_ignore = False
            continue
        if in_stats or in_ignore:
            continue
        for regex, key in PATTERNS:
            for m in regex.finditer(raw):
                found = int(m.group(1))
                expected = counts.get(key)
                if expected is None or found == expected:
                    continue
                mismatches.append({
                    "path": path.relative_to(REPO_ROOT),
                    "line": lineno,
                    "key": key,
                    "expected": expected,
                    "found": found,
                    "text": raw.strip(),
                })
    return mismatches


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    counts = count_catalog_items()
    if args.verbose:
        print("Catalog counts:", counts)

    all_mismatches = []
    for path in SCAN_PATHS:
        if not path.exists():
            continue
        all_mismatches.extend(scan_file(path, counts))

    if not all_mismatches:
        print(f"prose-drift-check: OK (skills={counts['skill']}, agents={counts['agent']}, "
              f"calculators={counts['calculator']}, reference_files={counts['reference_file']})")
        return 0

    print(f"prose-drift-check: FAIL - {len(all_mismatches)} hardcoded count(s) in prose drift from catalog:")
    print()
    for mm in all_mismatches:
        print(f"  {mm['path']}:{mm['line']} - expected {mm['expected']} {mm['key']}(s), found {mm['found']}")
        print(f"      >>> {mm['text']}")
    print()
    print("Fix options:")
    print("  1. Update the prose to the current catalog count, OR")
    print("  2. Wrap the intentional historical reference in")
    print("     <!-- PROSE-DRIFT:IGNORE-START --> ... <!-- PROSE-DRIFT:IGNORE-END --> markers, OR")
    print("  3. Move the count into a <!-- CATALOG:STATS:START --> block so")
    print("     scripts/catalog-generate.py manages it automatically.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
