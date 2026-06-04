"""Corpus-wide v5.2 contract (Tier-1).

Every catalog SKILL carries valid, non-null governance + forward-compat metadata.
This is the "all 127 contract-checked" floor:

  - Tier-1 (here)        : every skill has a valid classification, runtime_role,
                           and v5.2 forward-compat fields (enum-valid), plus the
                           calculator -> calculator_result crosswalk.
  - Tier-2 (v5_contract) : the deep section/field contract on the opted-in
                           decision-grade set (test_skill_v5_contract).
  - Invariants           : decision-grade gating, source-ref posture, liability
                           stamps, decomposition resolution (test_governance_scan).

Reads the generated catalog (dist/catalog.json) so derived/projected fields are
checked as the consumer will see them; run scripts/catalog-build.py first.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_JSON = REPO_ROOT / "dist" / "catalog.json"
CATALOG_SCHEMA = REPO_ROOT / "src" / "catalog" / "catalog.schema.json"
CALC_REGISTRY = REPO_ROOT / "scripts" / "calculator-registry.json"
CATALOG_BUILD = REPO_ROOT / "scripts" / "catalog-build.py"

PII_ENUM = {"none", "business_contact", "tenant_or_personal", "sensitive_financial"}


def _items():
    assert CATALOG_JSON.exists(), "run scripts/catalog-build.py first"
    return json.loads(CATALOG_JSON.read_text(encoding="utf-8"))["items"]


def _skills():
    return [i for i in _items() if i["type"] == "skill"]


def _schema_enum(field):
    s = json.loads(CATALOG_SCHEMA.read_text(encoding="utf-8"))
    return set(s["$defs"]["CatalogItem"]["properties"][field]["enum"])


def _load_catalog_build():
    spec = importlib.util.spec_from_file_location("catalog_build", CATALOG_BUILD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_every_skill_has_non_null_classification_and_runtime_role():
    class_enum = _schema_enum("classification") - {None}
    role_enum = _schema_enum("runtime_role") - {None}
    failures = []
    for it in _skills():
        c, r = it.get("classification"), it.get("runtime_role")
        if c is None or c not in class_enum:
            failures.append(f"{it['id']}: classification {c!r} invalid")
        if r is None or r not in role_enum:
            failures.append(f"{it['id']}: runtime_role {r!r} invalid")
    assert not failures, "classification/runtime_role corpus violations:\n  " + "\n  ".join(failures)


def test_every_skill_has_enum_valid_forward_compat_fields():
    pak_enum = _schema_enum("produces_artifact_kind")  # includes None
    ws_enum = _schema_enum("workspace_scope")  # includes None
    failures = []
    for it in _skills():
        if it.get("pii_policy") not in PII_ENUM:
            failures.append(f"{it['id']}: pii_policy {it.get('pii_policy')!r} not in enum")
        if it.get("produces_artifact_kind") not in pak_enum:
            failures.append(f"{it['id']}: produces_artifact_kind {it.get('produces_artifact_kind')!r} not in enum")
        if it.get("workspace_scope") not in ws_enum:
            failures.append(f"{it['id']}: workspace_scope {it.get('workspace_scope')!r} not in enum")
        if not isinstance(it.get("outputs"), list):
            failures.append(f"{it['id']}: outputs is not a list")
    assert not failures, "forward-compat corpus violations:\n  " + "\n  ".join(failures)


def test_calculator_bridged_skills_emit_calculator_result():
    """Every SKILL_CALCULATOR_MAP slug must surface as a catalog skill with its
    calculator_file set AND produces_artifact_kind == 'calculator_result' (the
    derivation must key off calculator_file, never classification, since all
    calc-bridged skills are classification:normal)."""
    cb = _load_catalog_build()
    by_id = {i["id"]: i for i in _items()}
    failures = []
    for slug in cb.SKILL_CALCULATOR_MAP:
        it = by_id.get(slug)
        if it is None:
            failures.append(f"{slug}: in SKILL_CALCULATOR_MAP but not a catalog item")
            continue
        if not it.get("calculator_file"):
            failures.append(f"{slug}: calculator_file not set in catalog")
        if it.get("produces_artifact_kind") != "calculator_result":
            failures.append(f"{slug}: produces_artifact_kind={it.get('produces_artifact_kind')!r}, expected calculator_result")
    assert not failures, "calculator->artifact crosswalk violations:\n  " + "\n  ".join(failures)


def test_skill_calculator_map_targets_resolve_in_registry():
    """Every SKILL_CALCULATOR_MAP target resolves to a real registry calculator
    AND a real .py file (Calc QA S1 — the two hand-maintained crosswalks agree)."""
    cb = _load_catalog_build()
    registry = json.loads(CALC_REGISTRY.read_text(encoding="utf-8"))
    calc_keys = set(registry.get("calculators", {}).keys())
    failures = []
    for slug, path in cb.SKILL_CALCULATOR_MAP.items():
        stem = Path(path).stem
        if stem not in calc_keys:
            failures.append(f"{slug}: calculator '{stem}' not a key in calculator-registry.json")
        if not (REPO_ROOT / path).exists():
            failures.append(f"{slug}: calculator file '{path}' does not exist")
    assert not failures, "SKILL_CALCULATOR_MAP/registry consistency violations:\n  " + "\n  ".join(failures)
