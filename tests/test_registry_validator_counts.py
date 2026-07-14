"""Regression guards for public catalog counts in registry-validator.py."""
from __future__ import annotations

import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_registry_validator():
    path = REPO_ROOT / "scripts" / "registry-validator.py"
    spec = importlib.util.spec_from_file_location("registry_validator", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_full_counts_excludes_internal_nested_agents(tmp_path, monkeypatch) -> None:
    module = _load_registry_validator()
    src_dir = tmp_path / "src"
    agents_dir = src_dir / "agents"
    nested_dir = agents_dir / "asset-management"
    hooks_dir = src_dir / "hooks"
    nested_dir.mkdir(parents=True)
    hooks_dir.mkdir(parents=True)

    (agents_dir / "_index.md").write_text("# Index\n", encoding="utf-8")
    (agents_dir / "public-persona.md").write_text("# Public\n", encoding="utf-8")
    (nested_dir / "internal-specialist.md").write_text("# Internal\n", encoding="utf-8")
    (tmp_path / "README.md").write_text(
        "| Expert Agents | **1** |\n", encoding="utf-8"
    )
    (hooks_dir / "hooks.json").write_text("{}\n", encoding="utf-8")

    monkeypatch.setattr(module, "PLUGIN_ROOT", tmp_path)
    monkeypatch.setattr(module, "SRC_DIR", src_dir)
    monkeypatch.setattr(module, "SKILLS_DIR", src_dir / "skills")

    assert module.validate_full_counts() == []
