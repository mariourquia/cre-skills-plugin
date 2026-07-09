"""Shared fixtures for the top-level integration suite.

Tests in this directory consume dist/catalog.json, which is gitignored.
Historically a fresh checkout failed its first run (17 failures across the
amos-manifest, compatibility-count, governance-scan, and e2e-routing tests)
because those consumers run alphabetically before the test that builds the
catalog as a side effect; a second run then passed on the artifact the first
run left behind. Building once per session up front makes a single run from
a fresh checkout deterministic and ensures the suite always exercises the
CURRENT sources instead of a stale dist/.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_BUILD = REPO_ROOT / "scripts" / "catalog-build.py"


@pytest.fixture(scope="session", autouse=True)
def fresh_catalog() -> None:
    """Rebuild dist/catalog.json from current sources before any test runs."""
    result = subprocess.run(
        [sys.executable, str(CATALOG_BUILD), "--json"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        pytest.fail(
            "scripts/catalog-build.py failed during session setup "
            f"(exit {result.returncode}):\n{result.stderr[-2000:]}",
            pytrace=False,
        )
