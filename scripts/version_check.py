#!/usr/bin/env python3
"""Validate that all installer version references match plugin.json.

Source of truth: .claude-plugin/plugin.json  (field: "version")

The primary code path reads from plugin.json at install time. This script
validates that the FALLBACK values embedded in each installer still match
the source of truth, so they never silently drift.

Usage::

    python3 scripts/version_check.py

Exit codes:
    0 -- all checks pass
    1 -- at least one mismatch detected
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
PLUGIN_JSON = REPO_ROOT / ".claude-plugin" / "plugin.json"

INSTALLER_CHECKS: list[tuple[str, list[tuple[str, str]]]] = [
    ("scripts/Install.ps1", [
        (
            r'if\s*\(\s*-not\s+\$PluginVersion\s*\)\s*\{\s*\$PluginVersion\s*=\s*"([^"]+)"',
            "PowerShell fallback version",
        ),
    ]),
    ("scripts/install.sh", [
        (
            r"plugin\.json.*\|\|\s*echo\s+\"([^\"]+)\"\)",
            "Bash install.sh fallback version",
        ),
    ]),
    ("Install.command", [
        (
            r"plugin\.json.*\|\|\s*echo\s+\"([^\"]+)\"\)",
            "Install.command fallback version",
        ),
    ]),
]


def load_source_version() -> str:
    if not PLUGIN_JSON.is_file():
        print(f"FAIL  Source of truth not found: {PLUGIN_JSON}")
        sys.exit(1)
    data = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
    version = data.get("version")
    if not version:
        print("FAIL  No 'version' field in plugin.json")
        sys.exit(1)
    return version


def check_installers(expected: str) -> list[dict]:
    results: list[dict] = []

    for relpath, patterns in INSTALLER_CHECKS:
        fpath = REPO_ROOT / relpath
        if not fpath.is_file():
            results.append({
                "file": relpath,
                "status": "SKIP",
                "details": "file not found",
            })
            continue

        content = fpath.read_text(encoding="utf-8")

        for pattern, description in patterns:
            matches = re.findall(pattern, content)
            if not matches:
                results.append({
                    "file": relpath,
                    "status": "WARN",
                    "details": f"no match for {description} pattern",
                })
                continue

            for found in matches:
                if found == expected:
                    results.append({
                        "file": relpath,
                        "status": "PASS",
                        "details": f"{description}: {found}",
                    })
                else:
                    results.append({
                        "file": relpath,
                        "status": "FAIL",
                        "details": f"{description}: found {found}, expected {expected}",
                    })

    return results


def check_dynamic_read() -> list[dict]:
    """Verify that each installer reads version dynamically from plugin.json."""
    results: list[dict] = []

    ps1 = REPO_ROOT / "scripts" / "Install.ps1"
    if ps1.is_file():
        content = ps1.read_text(encoding="utf-8")
        if "ConvertFrom-Json" in content and "plugin.json" in content:
            results.append({
                "file": "scripts/Install.ps1",
                "status": "PASS",
                "details": "reads version dynamically from plugin.json",
            })
        else:
            results.append({
                "file": "scripts/Install.ps1",
                "status": "FAIL",
                "details": "does not read version dynamically from plugin.json",
            })

    for relpath in ("scripts/install.sh", "Install.command"):
        fpath = REPO_ROOT / relpath
        if fpath.is_file():
            content = fpath.read_text(encoding="utf-8")
            if "plugin.json" in content and "json.load" in content:
                results.append({
                    "file": relpath,
                    "status": "PASS",
                    "details": "reads version dynamically from plugin.json",
                })
            else:
                results.append({
                    "file": relpath,
                    "status": "FAIL",
                    "details": "does not read version dynamically from plugin.json",
                })

    return results


def main() -> int:
    expected = load_source_version()

    print("cre-skills-plugin Version Check")
    print("=" * 50)
    print(f"Source of truth: .claude-plugin/plugin.json")
    print(f"Expected version: {expected}")
    print()

    all_pass = True

    print("Dynamic version read:")
    dynamic_results = check_dynamic_read()
    for r in dynamic_results:
        tag = r["status"]
        print(f"  {tag:4s}  {r['file']}: {r['details']}")
        if tag == "FAIL":
            all_pass = False
    print()

    print("Fallback version values:")
    fallback_results = check_installers(expected)
    for r in fallback_results:
        tag = r["status"]
        print(f"  {tag:4s}  {r['file']}: {r['details']}")
        if tag == "FAIL":
            all_pass = False
    print()

    if all_pass:
        print("RESULT: PASS")
        return 0
    else:
        print("RESULT: FAIL")
        return 1


if __name__ == "__main__":
    sys.exit(main())
