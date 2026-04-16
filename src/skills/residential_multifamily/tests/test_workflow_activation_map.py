"""Workflow activation map tests.

Validates reference/connectors/_core/workflow_activation_map.yaml against the
canonical workflow directory and connector family. Every workflow declared in
the map must exist as a canonical workflow pack; every workflow pack must be
covered by an activation entry.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Set

import pytest
import yaml

from conftest import SUBSYS


MAP_YAML = SUBSYS / "reference" / "connectors" / "_core" / "workflow_activation_map.yaml"
MAP_MD = SUBSYS / "reference" / "connectors" / "_core" / "workflow_activation_map.md"
WORKFLOWS_ROOT = SUBSYS / "workflows"

ALLOWED_DOMAINS: Set[str] = {
    "pms", "gl", "crm", "ap", "market_data", "construction", "hr_payroll", "manual_uploads", "deal_pipeline"
}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict), f"{path}: expected mapping"
    return data


def _canonical_workflow_slugs() -> Set[str]:
    if not WORKFLOWS_ROOT.exists():
        return set()
    return {
        p.name for p in WORKFLOWS_ROOT.iterdir()
        if p.is_dir() and not p.name.startswith("_") and not p.name.startswith(".")
    }


def test_workflow_activation_map_files_present():
    missing = [str(p.relative_to(SUBSYS)) for p in (MAP_YAML, MAP_MD) if not p.exists()]
    assert not missing, "workflow activation map files missing:\n  - " + "\n  - ".join(missing)


def test_workflow_activation_map_keys_are_canonical():
    doc = _load_yaml(MAP_YAML)
    workflows = doc.get("workflows")
    assert isinstance(workflows, dict), "workflow_activation_map.yaml must declare a 'workflows' mapping"
    canonical = _canonical_workflow_slugs()
    declared = set(workflows.keys())
    invented = sorted(declared - canonical)
    missing = sorted(canonical - declared)
    problems: List[str] = []
    if invented:
        problems.append(f"workflow activation map declares non-canonical slugs: {invented}")
    if missing:
        problems.append(f"workflow activation map missing canonical slugs: {missing}")
    assert not problems, "\n  - ".join(problems)


def test_workflow_activation_entries_shape():
    doc = _load_yaml(MAP_YAML)
    workflows = doc.get("workflows") or {}
    failures: List[str] = []
    for slug, entry in workflows.items():
        if not isinstance(entry, dict):
            failures.append(f"{slug}: entry must be a mapping, got {type(entry).__name__}")
            continue
        reqd = entry.get("required_domains")
        if not isinstance(reqd, list):
            failures.append(f"{slug}: required_domains must be a list")
            continue
        for dom in reqd:
            if dom not in ALLOWED_DOMAINS:
                failures.append(f"{slug}: required_domain {dom!r} not in {sorted(ALLOWED_DOMAINS)}")
        conf = entry.get("minimum_confidence")
        if conf is not None and conf not in ALLOWED_CONFIDENCE:
            failures.append(f"{slug}: minimum_confidence {conf!r} not in {sorted(ALLOWED_CONFIDENCE)}")
    assert not failures, "workflow activation entry validation failed:\n  - " + "\n  - ".join(failures)


def test_workflow_activation_map_md_mentions_every_workflow():
    """Smoke check: readable companion should mention every workflow slug."""
    text = MAP_MD.read_text(encoding="utf-8")
    canonical = _canonical_workflow_slugs()
    missing = sorted(s for s in canonical if s not in text)
    assert not missing, f"workflow_activation_map.md does not mention these slugs: {missing}"
