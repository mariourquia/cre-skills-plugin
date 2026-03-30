#!/usr/bin/env python3
"""
Registry Validator
==================
Zero-dependency script that validates registry.yaml integrity:
  - For each skill with chains_to/chains_from, verify referenced skill directory exists
  - Verify all skill directories have a SKILL.md
  - Print pass/fail report, exit 0 (all pass) or 1 (any failure)

Parses YAML manually (line-by-line) since PyYAML is not guaranteed.

Usage:
    python3 scripts/registry-validator.py
"""

import os
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = SCRIPT_DIR.parent
REGISTRY_PATH = PLUGIN_ROOT / "registry.yaml"
SKILLS_DIR = PLUGIN_ROOT / "skills"


# ---------------------------------------------------------------------------
# Lightweight YAML parser (registry-specific)
# ---------------------------------------------------------------------------

def parse_registry(filepath: Path) -> list[dict]:
    """
    Parse registry.yaml by scanning for skill entries.
    Returns a list of dicts with keys: slug, chains_to, chains_from.
    """
    skills: list[dict] = []
    current_skill: dict | None = None

    with open(filepath, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.rstrip()
            stripped = line.lstrip()

            # Skip comments and blank lines
            if not stripped or stripped.startswith("#"):
                continue

            # Detect new skill entry: "  - slug: <value>"
            if stripped.startswith("- slug:"):
                if current_skill is not None:
                    skills.append(current_skill)
                slug_val = stripped.split(":", 1)[1].strip().strip('"').strip("'")
                current_skill = {
                    "slug": slug_val,
                    "chains_to": [],
                    "chains_from": [],
                }
                continue

            if current_skill is None:
                continue

            # Parse chains_to: [slug1, slug2, ...]
            if stripped.startswith("chains_to:"):
                current_skill["chains_to"] = _parse_inline_list(stripped)
                continue

            # Parse chains_from: [slug1, slug2, ...]
            if stripped.startswith("chains_from:"):
                current_skill["chains_from"] = _parse_inline_list(stripped)
                continue

    # Don't forget the last skill
    if current_skill is not None:
        skills.append(current_skill)

    return skills


def _parse_inline_list(line: str) -> list[str]:
    """
    Parse a YAML inline list like:
        chains_to: [slug-a, slug-b, slug-c]
        chains_to: []
    Returns list of strings.
    """
    _, _, value = line.partition(":")
    value = value.strip()

    if not value or value == "[]":
        return []

    # Strip brackets
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]

    items = []
    for item in value.split(","):
        cleaned = item.strip().strip('"').strip("'")
        if cleaned:
            items.append(cleaned)

    return items


# ---------------------------------------------------------------------------
# Validation checks
# ---------------------------------------------------------------------------

def validate_chain_references(skills: list[dict]) -> list[str]:
    """
    For each skill's chains_to and chains_from, verify the referenced
    skill directory exists under skills/.
    Returns list of failure messages.
    """
    failures: list[str] = []
    all_slugs = {s["slug"] for s in skills}

    for skill in skills:
        slug = skill["slug"]

        for ref in skill["chains_to"]:
            ref_dir = SKILLS_DIR / ref
            if not ref_dir.is_dir():
                failures.append(
                    f"FAIL  {slug} chains_to '{ref}' -- "
                    f"directory skills/{ref}/ not found"
                )

        for ref in skill["chains_from"]:
            ref_dir = SKILLS_DIR / ref
            if not ref_dir.is_dir():
                failures.append(
                    f"FAIL  {slug} chains_from '{ref}' -- "
                    f"directory skills/{ref}/ not found"
                )

    return failures


def validate_skill_md(skills: list[dict]) -> list[str]:
    """
    Verify every skill directory listed in the registry has a SKILL.md file.
    Returns list of failure messages.
    """
    failures: list[str] = []

    for skill in skills:
        slug = skill["slug"]
        skill_dir = SKILLS_DIR / slug

        if not skill_dir.is_dir():
            failures.append(
                f"FAIL  {slug} -- directory skills/{slug}/ not found"
            )
            continue

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            failures.append(
                f"FAIL  {slug} -- skills/{slug}/SKILL.md not found"
            )

    return failures


def validate_orphan_dirs(skills: list[dict]) -> list[str]:
    """
    Check for skill directories that exist on disk but are not in the registry.
    These are warnings, not failures.
    """
    warnings: list[str] = []
    registry_slugs = {s["slug"] for s in skills}

    if not SKILLS_DIR.is_dir():
        return warnings

    for entry in sorted(SKILLS_DIR.iterdir()):
        if entry.is_dir() and entry.name not in registry_slugs:
            warnings.append(
                f"WARN  skills/{entry.name}/ exists on disk but is not in registry.yaml"
            )

    return warnings


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if not REGISTRY_PATH.exists():
        print(f"ERROR: registry.yaml not found at {REGISTRY_PATH}")
        sys.exit(1)

    if not SKILLS_DIR.is_dir():
        print(f"ERROR: skills/ directory not found at {SKILLS_DIR}")
        sys.exit(1)

    print(f"Validating {REGISTRY_PATH}")
    print(f"Skills directory: {SKILLS_DIR}")
    print()

    skills = parse_registry(REGISTRY_PATH)
    print(f"Parsed {len(skills)} skill entries from registry.yaml")
    print()

    # Run checks
    chain_failures = validate_chain_references(skills)
    skillmd_failures = validate_skill_md(skills)
    orphan_warnings = validate_orphan_dirs(skills)

    all_failures = chain_failures + skillmd_failures

    # Print results
    if chain_failures:
        print("--- Chain Reference Checks ---")
        for msg in chain_failures:
            print(f"  {msg}")
        print()

    if skillmd_failures:
        print("--- SKILL.md Checks ---")
        for msg in skillmd_failures:
            print(f"  {msg}")
        print()

    if orphan_warnings:
        print("--- Orphan Directory Warnings ---")
        for msg in orphan_warnings:
            print(f"  {msg}")
        print()

    # Summary
    total_checks = len(skills) * 2  # chain refs + SKILL.md per entry
    pass_count = total_checks - len(all_failures)
    print("=" * 60)
    print(f"RESULT: {pass_count}/{total_checks} checks passed, "
          f"{len(all_failures)} failures, {len(orphan_warnings)} warnings")

    if all_failures:
        print("STATUS: FAIL")
        sys.exit(1)
    else:
        print("STATUS: PASS")
        sys.exit(0)


if __name__ == "__main__":
    main()
