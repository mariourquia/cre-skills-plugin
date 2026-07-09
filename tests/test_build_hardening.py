"""Guards for the sweep's build/catalog hardening: catalog-build idempotence and the
normalizer path rewrites that keep flattened build targets pointing at real files.

These close the test-coverage gaps the review panel flagged: without them a revert of the
idempotency block or the normalizer replaceAll passes both pytest suites green while
reintroducing timestamp churn (catalog) or a desktop/marketplace 404 (built targets)."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_BUILD = REPO_ROOT / "scripts" / "catalog-build.py"
CATALOG_YAML = REPO_ROOT / "src" / "catalog" / "catalog.yaml"

STAMP_RE = re.compile(r"^generated_at:\s*(.+)$", re.MULTILINE)


def _run_build(*args: str) -> None:
    result = subprocess.run(
        [sys.executable, str(CATALOG_BUILD), *args],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr[-2000:]


def test_json_build_does_not_write_catalog_yaml():
    """`catalog-build.py --json` must emit only dist/catalog.json, never touch the tracked
    catalog.yaml (conftest runs it every session; it must not dirty the tree)."""
    before = CATALOG_YAML.read_bytes()
    try:
        _run_build("--json")
        assert CATALOG_YAML.read_bytes() == before, "--json rewrote src/catalog/catalog.yaml"
    finally:
        CATALOG_YAML.write_bytes(before)


def test_full_rebuild_is_idempotent_on_generated_at():
    """A content-identical full rebuild preserves the existing generated_at stamp, so repeated
    builds produce no timestamp-only diff on the tracked catalog."""
    before = CATALOG_YAML.read_bytes()
    stamp_before = STAMP_RE.search(before.decode("utf-8")).group(1)
    try:
        _run_build()  # full build: writes catalog.yaml
        after = CATALOG_YAML.read_text(encoding="utf-8")
        stamp_after = STAMP_RE.search(after).group(1)
        assert stamp_after == stamp_before, (
            "a no-op rebuild changed generated_at (idempotency regressed): "
            f"{stamp_before!r} -> {stamp_after!r}"
        )
    finally:
        CATALOG_YAML.write_bytes(before)


def test_normalizers_rewrite_src_paths_for_flattened_targets():
    """The source hooks.json / command files use src/-prefixed ${CLAUDE_PLUGIN_ROOT} paths
    (correct for the repo-root install). Built targets flatten src/<dir> -> <dir>, so the
    normalizers MUST rewrite those paths or the built artifact 404s. Guard against silent
    removal of that rewrite (the primary-install repo layout is covered separately by
    test_plugin_integrity.test_{hook,command}_paths_resolve_in_repo_layout)."""
    hooks_ts = (REPO_ROOT / "tools" / "normalize" / "hooks.ts").read_text(encoding="utf-8")
    commands_ts = (REPO_ROOT / "tools" / "normalize" / "commands.ts").read_text(encoding="utf-8")
    for src_prefix, flat in (("/src/hooks/", "/hooks/"), ("/src/routing/", "/routing/")):
        assert f"${{CLAUDE_PLUGIN_ROOT}}{src_prefix}" in hooks_ts, f"hooks normalizer lost the {src_prefix} rewrite"
    for src_prefix in ("/src/routing/", "/src/hooks/", "/src/agents/"):
        assert f"${{CLAUDE_PLUGIN_ROOT}}{src_prefix}" in commands_ts, f"commands normalizer lost the {src_prefix} rewrite"
