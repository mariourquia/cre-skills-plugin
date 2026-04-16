"""Source registry contract tests.

Validates the source registry under reference/connectors/source_registry/.
Every record must conform to source_registry.schema.yaml, use snake_case ids,
cover only permitted source domains, and carry a status in the allowed set.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import pytest
import yaml

from conftest import SUBSYS, validate_against_schema


REGISTRY_ROOT = SUBSYS / "reference" / "connectors" / "source_registry"
REGISTRY_FILE = REGISTRY_ROOT / "source_registry.yaml"
SCHEMA_FILE = REGISTRY_ROOT / "source_registry.schema.yaml"

ALLOWED_DOMAINS = {
    "pms",
    "gl",
    "crm",
    "ap",
    "market_data",
    "construction",
    "hr_payroll",
    "manual_upload",
    "deal_pipeline",
    "other",
}
ALLOWED_STATUSES = {"planned", "stubbed", "active", "degraded", "deprecated"}
EXPECTED_FILES = [
    "README.md",
    "source_registry.schema.yaml",
    "source_registry.yaml",
    "source_inventory.md",
    "system_coverage_matrix.md",
    "vendor_family_hints.md",
    "implementation_inventory.md",
]


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict), f"{path}: expected mapping"
    return data


def test_source_registry_family_present():
    missing = [
        str((REGISTRY_ROOT / name).relative_to(SUBSYS))
        for name in EXPECTED_FILES
        if not (REGISTRY_ROOT / name).exists()
    ]
    assert not missing, "source_registry missing files:\n  - " + "\n  - ".join(missing)


def test_source_registry_schema_parses():
    schema = _load_yaml(SCHEMA_FILE)
    assert schema.get("type") == "object"
    assert "required" in schema, "schema must declare required fields"


def test_source_registry_records_conform():
    doc = _load_yaml(REGISTRY_FILE)
    records = doc.get("records")
    assert isinstance(records, list) and records, "registry must declare a non-empty 'records' list"
    schema = _load_yaml(SCHEMA_FILE)
    errors: List[str] = []
    for idx, rec in enumerate(records):
        errors.extend(validate_against_schema(rec, schema, path=f"records[{idx}]"))
    assert not errors, "source registry records failed schema validation:\n  - " + "\n  - ".join(errors)


def test_source_registry_ids_unique_and_snake_case():
    doc = _load_yaml(REGISTRY_FILE)
    records = doc.get("records") or []
    seen: Dict[str, int] = {}
    failures: List[str] = []
    for idx, rec in enumerate(records):
        sid = rec.get("source_id") if isinstance(rec, dict) else None
        if not isinstance(sid, str):
            failures.append(f"records[{idx}]: source_id missing or not a string")
            continue
        if not sid.replace("_", "").replace("0", "a").isalnum() or not sid[0].isalpha():
            failures.append(f"records[{idx}]: source_id {sid!r} not snake_case")
        if sid in seen:
            failures.append(f"records[{idx}]: duplicate source_id {sid!r} first seen at records[{seen[sid]}]")
        else:
            seen[sid] = idx
    assert not failures, "source_id validation failed:\n  - " + "\n  - ".join(failures)


def test_source_registry_domains_and_status_are_allowed():
    doc = _load_yaml(REGISTRY_FILE)
    records = doc.get("records") or []
    failures: List[str] = []
    for idx, rec in enumerate(records):
        if not isinstance(rec, dict):
            continue
        domain = rec.get("source_domain")
        status = rec.get("status")
        if domain not in ALLOWED_DOMAINS:
            failures.append(f"records[{idx}]: source_domain {domain!r} not in {sorted(ALLOWED_DOMAINS)}")
        if status not in ALLOWED_STATUSES:
            failures.append(f"records[{idx}]: status {status!r} not in {sorted(ALLOWED_STATUSES)}")
    assert not failures, "domain/status enforcement failed:\n  - " + "\n  - ".join(failures)


def test_source_registry_has_status_tag():
    doc = _load_yaml(REGISTRY_FILE)
    tag = doc.get("status_tag")
    allowed = {"sample", "starter", "illustrative", "placeholder"}
    assert tag in allowed, f"source_registry.yaml must carry status_tag in {sorted(allowed)}, got {tag!r}"


def test_source_registry_covers_every_domain():
    """Every declared connector domain should have at least one stubbed entry,
    so operators have a forkable starting record."""
    doc = _load_yaml(REGISTRY_FILE)
    records = doc.get("records") or []
    present = {rec.get("source_domain") for rec in records if isinstance(rec, dict)}
    missing = [
        d for d in ("pms", "gl", "crm", "ap", "market_data", "construction", "hr_payroll", "manual_upload")
        if d not in present
    ]
    assert not missing, f"source_registry missing entries for domains: {missing}"
