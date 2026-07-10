"""Regression guard for scripts/catalog-generate.py's hooks.json template.

catalog-generate.py regenerates src/hooks/hooks.json's SessionStart prompt on
every CI run (the "Build catalog" step runs before tests). Its template
hardcoded the routing index path as ${CLAUDE_PLUGIN_ROOT}/routing/CRE-ROUTING.md
(the flattened, build-output-only form), silently overwriting the correct
${CLAUDE_PLUGIN_ROOT}/src/routing/CRE-ROUTING.md (the primary/repo-root install
form that tests/test_plugin_integrity.py::test_hook_paths_resolve_in_repo_layout
checks) every time it ran -- a repeat of the exact class of bug that test was
added to catch, just one step upstream where nothing exercised it directly.
"""
from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_catalog_generate():
    path = REPO_ROOT / "scripts" / "catalog-generate.py"
    spec = importlib.util.spec_from_file_location("catalog_generate", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_update_hooks_prompt_uses_primary_install_routing_path(tmp_path, monkeypatch):
    mod = _load_catalog_generate()

    tmp_hooks_dir = tmp_path / "src" / "hooks"
    tmp_hooks_dir.mkdir(parents=True)
    shutil.copy(REPO_ROOT / "src" / "hooks" / "hooks.json", tmp_hooks_dir / "hooks.json")
    monkeypatch.setattr(mod, "SRC_DIR", tmp_path / "src")

    mod.update_hooks({"skills": 127, "agents": 55, "workflows": 6, "orchestrators": 10}, dry_run=False)

    data = json.loads((tmp_hooks_dir / "hooks.json").read_text(encoding="utf-8"))
    prompt = data["hooks"]["SessionStart"][0]["hooks"][0]["prompt"]
    assert "${CLAUDE_PLUGIN_ROOT}/src/routing/CRE-ROUTING.md" in prompt, (
        "catalog-generate.py's hooks.json template regressed to the flattened "
        "routing/ path -- this breaks the primary (repo-root) install, where "
        "CRE-ROUTING.md only exists at src/routing/, not routing/."
    )
