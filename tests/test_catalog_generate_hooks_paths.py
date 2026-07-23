"""Regression guards for the generated SessionStart hook surface."""
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


def test_update_hooks_preserves_command_session_context(tmp_path, monkeypatch):
    mod = _load_catalog_generate()

    tmp_hooks_dir = tmp_path / "src" / "hooks"
    tmp_hooks_dir.mkdir(parents=True)
    shutil.copy(REPO_ROOT / "src" / "hooks" / "hooks.json", tmp_hooks_dir / "hooks.json")
    monkeypatch.setattr(mod, "SRC_DIR", tmp_path / "src")

    changed = mod.update_hooks(
        {"skills": 127, "agents": 55, "workflows": 6, "orchestrators": 10},
        dry_run=False,
    )

    data = json.loads((tmp_hooks_dir / "hooks.json").read_text(encoding="utf-8"))
    hooks = data["hooks"]["SessionStart"][0]["hooks"]
    assert changed is False
    assert all(hook["type"] == "command" for hook in hooks)
    assert hooks[0]["command"] == (
        'node "${CLAUDE_PLUGIN_ROOT}/src/hooks/session-context.mjs"'
    )

    context_script = (REPO_ROOT / "src" / "hooks" / "session-context.mjs").read_text(
        encoding="utf-8"
    )
    assert "resolve(pluginRoot, 'src', 'routing', 'CRE-ROUTING.md')" in context_script
    assert "resolve(pluginRoot, 'routing', 'CRE-ROUTING.md')" in context_script
