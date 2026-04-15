"""Master data crosswalk tests.

Validates every crosswalk YAML under reference/connectors/master_data/
against the local crosswalk.schema.yaml, plus structural invariants:
canonical_ids snake_case, (source_system, source_id) rows unique per
canonical_id, sample-data status tag present.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List

import pytest
import yaml

from conftest import SUBSYS, validate_against_schema


MASTER_ROOT = SUBSYS / "reference" / "connectors" / "master_data"
SCHEMA_FILE = MASTER_ROOT / "crosswalk.schema.yaml"

CROSSWALK_FILES = [
    "property_master_crosswalk.yaml",
    "unit_crosswalk.yaml",
    "lease_crosswalk.yaml",
    "resident_account_crosswalk.yaml",
    "vendor_master_crosswalk.yaml",
    "account_crosswalk.yaml",
    "capex_project_crosswalk.yaml",
    "change_order_crosswalk.yaml",
    "draw_request_crosswalk.yaml",
    "employee_crosswalk.yaml",
    "dev_project_crosswalk.yaml",
    "manual_overrides.yaml",
]

EXPECTED_NARRATIVE = [
    "README.md",
    "identity_resolution_framework.md",
    "survivorship_rules.md",
    "unresolved_exceptions_queue.md",
    "change_log.md",
]

SNAKE_CASE = re.compile(r"^[a-z][a-z0-9_]*$")


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _rows(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    for key in ("rows", "entries", "records", "mappings", "crosswalk"):
        if isinstance(doc.get(key), list):
            return [r for r in doc[key] if isinstance(r, dict)]
    return []


def test_master_data_family_present():
    missing: List[str] = []
    if not SCHEMA_FILE.exists():
        missing.append(str(SCHEMA_FILE.relative_to(SUBSYS)))
    for name in EXPECTED_NARRATIVE + CROSSWALK_FILES:
        p = MASTER_ROOT / name
        if not p.exists():
            missing.append(str(p.relative_to(SUBSYS)))
    assert not missing, "master_data family missing files:\n  - " + "\n  - ".join(missing)


def test_master_data_schema_parses():
    schema = _load_yaml(SCHEMA_FILE)
    assert schema.get("type") == "object"
    assert "required" in schema, "crosswalk schema must declare required fields"


def test_master_data_crosswalk_rows_conform():
    schema = _load_yaml(SCHEMA_FILE)
    failures: List[str] = []
    for name in CROSSWALK_FILES:
        path = MASTER_ROOT / name
        if name == "manual_overrides.yaml":
            continue
        if not path.exists():
            continue
        doc = _load_yaml(path)
        rows = _rows(doc)
        if not rows:
            failures.append(f"{path.relative_to(SUBSYS)}: no crosswalk rows discovered")
            continue
        for idx, row in enumerate(rows):
            errs = validate_against_schema(row, schema, path=f"{name}#[{idx}]")
            failures.extend(errs)
    assert not failures, "crosswalk row validation failed:\n  - " + "\n  - ".join(failures)


def test_master_data_canonical_ids_snake_case():
    failures: List[str] = []
    for name in CROSSWALK_FILES:
        if name == "manual_overrides.yaml":
            continue
        path = MASTER_ROOT / name
        if not path.exists():
            continue
        doc = _load_yaml(path)
        for idx, row in enumerate(_rows(doc)):
            cid = row.get("canonical_id")
            if not isinstance(cid, str):
                failures.append(f"{name}#[{idx}]: canonical_id missing or not a string")
                continue
            if not SNAKE_CASE.match(cid):
                failures.append(f"{name}#[{idx}]: canonical_id {cid!r} not snake_case")
    assert not failures, "canonical_id snake_case validation failed:\n  - " + "\n  - ".join(failures)


def test_master_data_source_rows_unique_per_canonical_id():
    """Within a crosswalk, a given (canonical_id, source_system, source_id, effective_start)
    tuple must not repeat. Multiple rows per canonical_id are allowed when
    source_system or effective_start differ (historical mappings)."""
    failures: List[str] = []
    for name in CROSSWALK_FILES:
        if name == "manual_overrides.yaml":
            continue
        path = MASTER_ROOT / name
        if not path.exists():
            continue
        doc = _load_yaml(path)
        seen: Dict[tuple, int] = {}
        for idx, row in enumerate(_rows(doc)):
            key = (
                row.get("canonical_id"),
                row.get("source_system"),
                row.get("source_id"),
                row.get("effective_start"),
            )
            if None in key[:3]:
                continue
            if key in seen:
                failures.append(
                    f"{name}#[{idx}]: duplicate row for {key}; first at #[{seen[key]}]"
                )
            else:
                seen[key] = idx
    assert not failures, "source-row uniqueness failed:\n  - " + "\n  - ".join(failures)


def test_master_data_status_tag_on_crosswalks():
    allowed = {"sample", "starter", "illustrative", "placeholder"}
    failures: List[str] = []
    for name in CROSSWALK_FILES:
        if name == "manual_overrides.yaml":
            continue
        path = MASTER_ROOT / name
        if not path.exists():
            continue
        doc = _load_yaml(path)
        tag = doc.get("status_tag")
        if tag not in allowed:
            failures.append(f"{name}: status_tag {tag!r} not in {sorted(allowed)}")
    assert not failures, "crosswalk status_tag check failed:\n  - " + "\n  - ".join(failures)
