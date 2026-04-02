#!/usr/bin/env python3
"""
Registry Validator & Documentation Drift Checker
=================================================
Zero-dependency script that validates:
  - registry.yaml integrity (chain refs, SKILL.md presence, orphan dirs)
  - Count consistency: skills, agents, commands, calculators, references
  - Version consistency: plugin.json version matches all docs and scripts
  - Stale version detection: no references to prior versions in non-CHANGELOG files
  - Legacy file detection: completed plan docs, duplicate files, empty dirs
  - Asset-type neutrality in orchestrator configs

Parses YAML manually (line-by-line) since PyYAML is not guaranteed.
Runs in CI and blocks releases on any FAIL result.

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
SRC_DIR = PLUGIN_ROOT / "src"
REGISTRY_PATH = PLUGIN_ROOT / "registry.yaml"
SKILLS_DIR = SRC_DIR / "skills"


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


def validate_count_consistency(skills: list[dict]) -> list[str]:
    """
    Verify that skill/agent/calculator counts in key files match the actual
    counts on disk. Catches stale numbers after adding/removing skills.
    Returns list of failure messages.
    """
    failures: list[str] = []

    # Actual counts from disk
    actual_skills = len(list(SKILLS_DIR.glob("*/SKILL.md")))
    actual_agents = len(list((SRC_DIR / "agents").glob("*.md"))) if (SRC_DIR / "agents").is_dir() else 0
    actual_calcs = len(list((SRC_DIR / "calculators").glob("*.py"))) if (SRC_DIR / "calculators").is_dir() else 0

    # Files that embed counts -- check each for the expected number
    count_files = {
        "plugin/plugin.json": None,
        "hooks/hooks.json": None,
        "routing/CRE-ROUTING.md": None,
    }

    import re

    for relpath in count_files:
        fpath = SRC_DIR / relpath
        if not fpath.is_file():
            continue
        content = fpath.read_text(encoding="utf-8")

        # Check for skill count mismatches
        # Look for patterns like "105 CRE skills" or "105 skills"
        for match in re.finditer(r"(\d+)\s+(?:CRE\s+)?skills", content):
            found = int(match.group(1))
            if found != actual_skills:
                failures.append(
                    f"FAIL  {relpath}: says {found} skills but disk has {actual_skills}"
                )
                break  # one failure per file is enough

    # Check registry metadata
    reg_content = REGISTRY_PATH.read_text(encoding="utf-8")
    for match in re.finditer(r"total_skills:\s*(\d+)", reg_content):
        found = int(match.group(1))
        if found != actual_skills:
            failures.append(
                f"FAIL  registry.yaml: total_skills says {found} but disk has {actual_skills}"
            )

    return failures


def validate_asset_type_neutrality() -> list[str]:
    """
    Scan orchestrator configs for hardcoded asset-type assumptions that should
    be parameterized. Catches regressions like 'multifamily-acquisition'.
    Returns list of failure messages.
    """
    failures: list[str] = []
    configs_dir = SRC_DIR / "orchestrators" / "configs"

    if not configs_dir.is_dir():
        return failures

    # Patterns that indicate hardcoded asset-type bias in orchestrator configs.
    # The orchestratorId and cross-chain references should be asset-agnostic.
    banned_patterns = [
        "multifamily-acquisition",
        "office-acquisition",
        "retail-acquisition",
        "industrial-acquisition",
    ]

    for config_file in sorted(configs_dir.glob("*.json")):
        content = config_file.read_text(encoding="utf-8")
        for pattern in banned_patterns:
            if pattern in content:
                failures.append(
                    f"FAIL  orchestrators/configs/{config_file.name}: "
                    f"contains hardcoded '{pattern}' -- should be asset-agnostic"
                )

    # Also check handoff registry
    handoff_file = SRC_DIR / "orchestrators" / "engine" / "handoff-registry.json"
    if handoff_file.is_file():
        content = handoff_file.read_text(encoding="utf-8")
        for pattern in banned_patterns:
            if pattern in content:
                failures.append(
                    f"FAIL  orchestrators/engine/handoff-registry.json: "
                    f"contains hardcoded '{pattern}'"
                )

    return failures


def validate_version_consistency() -> list[str]:
    """
    The version in plugin.json is the source of truth.
    Every file that embeds a version string must match it.
    Returns list of failure messages.
    """
    import json, re
    failures: list[str] = []

    # Source of truth
    pj_path = SRC_DIR / "plugin" / "plugin.json"
    if not pj_path.is_file():
        failures.append("FAIL  src/plugin/plugin.json not found")
        return failures

    pj = json.loads(pj_path.read_text(encoding="utf-8"))
    sot_version = pj.get("version", "")
    if not sot_version:
        failures.append("FAIL  plugin.json has no version field")
        return failures

    # Files that must contain this version
    # (base_dir, relative_path, pattern) -- hooks are under SRC_DIR, docs at PLUGIN_ROOT
    version_files = [
        (SRC_DIR, "hooks/telemetry-init.mjs", re.compile(r"version:\s*['\"](\d+\.\d+\.\d+)['\"]")),
        (PLUGIN_ROOT, "docs/install-guide.md", re.compile(r"Version\s+(\d+\.\d+\.\d+)")),
        (PLUGIN_ROOT, "PRIVACY.md", re.compile(r"Plugin\s+v(\d+\.\d+\.\d+)")),
    ]

    for base, relpath, pattern in version_files:
        fpath = base / relpath
        if not fpath.is_file():
            continue
        content = fpath.read_text(encoding="utf-8")
        match = pattern.search(content)
        if match:
            found = match.group(1)
            if found != sot_version:
                failures.append(
                    f"FAIL  {relpath}: version {found} != plugin.json {sot_version}"
                )

    return failures


def validate_stale_versions() -> list[str]:
    """
    Detect references to prior major/minor versions in non-historical files.
    CHANGELOG.md and docs/releases/ are exempt (they document history).
    Returns list of failure messages.
    """
    import json, re
    failures: list[str] = []

    pj_path = SRC_DIR / "plugin" / "plugin.json"
    if not pj_path.is_file():
        return failures

    pj = json.loads(pj_path.read_text(encoding="utf-8"))
    current = pj.get("version", "")
    if not current:
        return failures

    current_major_minor = ".".join(current.split(".")[:2])

    # Build list of prior versions to detect
    # Only flag versions that are clearly stale (prior major.minor)
    prior_patterns = []
    major, minor = int(current.split(".")[0]), int(current.split(".")[1])
    for m in range(1, major + 1):
        for n in range(0, 10):
            vm = f"{m}.{n}"
            if vm != current_major_minor:
                prior_patterns.append(vm)

    # Files to scan (exclude history files and files with legitimate prior-version context)
    exempt = {"CHANGELOG.md", "NOTICE", "LICENSE"}
    exempt_dirs = {"docs/releases", "docs/plans"}
    # Files that legitimately reference prior versions (migration tables, examples)
    exempt_contextual = {
        "scripts/create-dmg.sh",   # example command in header comment
        "scripts/install.sh",      # v1->v2 migration messaging
        "docs/install-guide.md",   # migration comparison table
        "docs/MIGRATION.md",       # migration guide references source version by design
    }

    scan_extensions = {".md", ".json", ".mjs", ".sh", ".ps1", ".iss", ".yml"}

    for fpath in sorted(PLUGIN_ROOT.rglob("*")):
        if not fpath.is_file():
            continue
        if ".git" in fpath.parts:
            continue
        if fpath.suffix not in scan_extensions:
            continue
        relpath_str = str(fpath.relative_to(PLUGIN_ROOT))
        if fpath.name in exempt:
            continue
        if any(relpath_str.startswith(d) for d in exempt_dirs):
            continue
        if relpath_str in exempt_contextual:
            continue

        try:
            content = fpath.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue

        relpath = str(fpath.relative_to(PLUGIN_ROOT))

        # Look for version patterns like "v2.0.0" or "v2.5.0" (with 'v' prefix)
        for match in re.finditer(r"v(\d+\.\d+\.\d+)", content):
            found_ver = match.group(1)
            found_mm = ".".join(found_ver.split(".")[:2])
            if found_mm in prior_patterns:
                # Get line number for context
                line_start = content[:match.start()].count("\n") + 1
                failures.append(
                    f"FAIL  {relpath}:{line_start}: stale version reference v{found_ver} (current is v{current})"
                )
                break  # one per file is enough

    return failures


def validate_full_counts() -> list[str]:
    """
    Validate that all catalog counts (skills, agents, commands, calculators)
    are consistent between the source of truth (disk) and documentation files.
    Returns list of failure messages.
    """
    import json, re
    failures: list[str] = []

    # Actual counts from disk
    counts = {
        "skills": len(list(SKILLS_DIR.glob("*/SKILL.md"))) if SKILLS_DIR.is_dir() else 0,
        "agents": len(list((SRC_DIR / "agents").glob("*.md"))) if (SRC_DIR / "agents").is_dir() else 0,
        "commands": len(list((SRC_DIR / "commands").glob("*.md"))) if (SRC_DIR / "commands").is_dir() else 0,
        "calculators": len(list((SRC_DIR / "calculators").glob("*.py"))) if (SRC_DIR / "calculators").is_dir() else 0,
    }

    # Subtract _index.md from agents count (it's an index, not an agent)
    if (SRC_DIR / "agents" / "_index.md").is_file():
        counts["agents"] -= 1

    # Also count agents in subdirectories
    for subdir in (SRC_DIR / "agents").iterdir() if (SRC_DIR / "agents").is_dir() else []:
        if subdir.is_dir():
            counts["agents"] += len(list(subdir.glob("*.md")))

    # Files to check and what to look for
    # (base_dir, relative_path, patterns) -- README at PLUGIN_ROOT, hooks under SRC_DIR
    check_files = [
        (PLUGIN_ROOT, "README.md", {
            "skills": re.compile(r"\*\*(\d+)\*\*.*Skills|Skills\s*\|\s*\*\*(\d+)\*\*"),
            "agents": re.compile(r"Expert\s+Agents\s*\|\s*\*\*(\d+)\*\*|(\d+)\s+expert\s+agents", re.IGNORECASE),
            "commands": re.compile(r"Slash\s+Commands\s*\|\s*\*\*(\d+)\*\*"),
            "calculators": re.compile(r"Python\s+Calculators\s*\|\s*\*\*(\d+)\*\*"),
        }),
        (SRC_DIR, "hooks/hooks.json", {
            "skills": re.compile(r"(\d+)\s+(?:CRE\s+)?skills"),
            "agents": re.compile(r"(\d+)\s+expert\s+agents"),
        }),
    ]

    for base, relpath, patterns in check_files:
        fpath = base / relpath
        if not fpath.is_file():
            continue
        content = fpath.read_text(encoding="utf-8")

        for asset_type, pattern in patterns.items():
            for match in pattern.finditer(content):
                # Get the first non-None group
                found = next((int(g) for g in match.groups() if g is not None), None)
                if found is not None and found != counts[asset_type]:
                    failures.append(
                        f"FAIL  {relpath}: says {found} {asset_type} but disk has {counts[asset_type]}"
                    )
                    break

    return failures


def validate_legacy_files() -> list[str]:
    """
    Detect files that should not be present in a release:
    - Completed plan docs in docs/plans/
    - Duplicate files with ' 2' suffix (macOS conflict copies)
    - Empty directories under skills/
    - .env files or credentials
    Returns list of failure messages.
    """
    failures: list[str] = []

    # Plan docs should be removed after completion
    plans_dir = PLUGIN_ROOT / "docs" / "plans"
    if plans_dir.is_dir():
        plan_files = list(plans_dir.glob("*.md"))
        if plan_files:
            for pf in plan_files:
                failures.append(
                    f"FAIL  docs/plans/{pf.name}: completed plan doc should be removed before release"
                )

    # Duplicate files with " 2" suffix (macOS conflict copies)
    for fpath in PLUGIN_ROOT.rglob("* 2*"):
        if ".git" in fpath.parts:
            continue
        relpath = str(fpath.relative_to(PLUGIN_ROOT))
        failures.append(
            f"FAIL  {relpath}: duplicate file (macOS conflict copy) -- delete before release"
        )

    # Empty skill directories
    if SKILLS_DIR.is_dir():
        for entry in sorted(SKILLS_DIR.iterdir()):
            if entry.is_dir() and not any(entry.iterdir()):
                failures.append(
                    f"FAIL  skills/{entry.name}/: empty directory -- remove or populate"
                )

    # Sensitive files that should never be committed
    sensitive_patterns = [".env", ".env.local", "credentials.json", "*.pem", "*.key"]
    for pattern in sensitive_patterns:
        for fpath in PLUGIN_ROOT.glob(pattern):
            if ".git" in fpath.parts:
                continue
            failures.append(
                f"FAIL  {fpath.name}: sensitive file detected -- must not be in release"
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

    # Run all checks
    checks = [
        ("Chain References", validate_chain_references(skills)),
        ("SKILL.md Presence", validate_skill_md(skills)),
        ("Skill Count Consistency", validate_count_consistency(skills)),
        ("Full Catalog Counts", validate_full_counts()),
        ("Version Consistency", validate_version_consistency()),
        ("Stale Version References", validate_stale_versions()),
        ("Asset-Type Neutrality", validate_asset_type_neutrality()),
        ("Legacy & Sensitive Files", validate_legacy_files()),
    ]
    orphan_warnings = validate_orphan_dirs(skills)

    all_failures = []
    for name, failures in checks:
        if failures:
            print(f"--- {name} ---")
            for msg in failures:
                print(f"  {msg}")
            print()
            all_failures.extend(failures)

    if orphan_warnings:
        print("--- Orphan Directory Warnings ---")
        for msg in orphan_warnings:
            print(f"  {msg}")
        print()

    # Summary
    check_count = sum(len(f) == 0 for _, f in checks)
    print("=" * 60)
    print(f"CHECKS: {check_count}/{len(checks)} categories clean, "
          f"{len(all_failures)} failures, {len(orphan_warnings)} warnings")

    if all_failures:
        print("STATUS: FAIL")
        sys.exit(1)
    else:
        print("STATUS: PASS")
        sys.exit(0)


if __name__ == "__main__":
    main()
