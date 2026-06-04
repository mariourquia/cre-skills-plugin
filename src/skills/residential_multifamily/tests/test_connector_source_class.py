"""Connector source_class hardening tests (v5.1).

Two invariants:

1. Single source of truth. The `source_class` enum declared in
   _schema/entity_contract.schema.yaml must equal the canonical list in
   _schema/source_class.yaml. If they drift, decision-grade refusal logic
   keyed on source_class would silently diverge from the contract.

2. Every entity in the 4 v5.1 connector domains (debt, entity, valuation,
   funds) declares a `source_class` drawn from the canonical list. Scope is
   limited to the new domains so the 8 legacy stubs are not forced to
   retrofit the optional field.

Loading + path resolution mirror test_connector_contracts.py (SUBSYS from
conftest, stdlib + PyYAML only).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import pytest
import yaml

try:
    from conftest import SUBSYS
except ImportError:  # pragma: no cover
    SUBSYS = Path(__file__).resolve().parents[1]
    raise


CONNECTORS_ROOT = SUBSYS / "reference" / "connectors"
SCHEMA_ROOT = CONNECTORS_ROOT / "_schema"
# The v5.1 domains that MUST declare source_class. Legacy stubs are out of scope.
SOURCE_CLASS_DOMAINS = ["debt", "entity", "valuation", "funds"]


# ---------------------------------------------------------------------------
# Local loaders (kept in step with test_connector_contracts.py)
# ---------------------------------------------------------------------------

def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict), f"{path} did not parse to a mapping"
    return data


def _domain_entities(domain: str) -> Dict[str, Dict[str, Any]]:
    """Load `reference/connectors/<domain>/schema.yaml` and return the entity
    map keyed by entity name. Returns empty dict if missing or malformed."""
    schema_path = CONNECTORS_ROOT / domain / "schema.yaml"
    if not schema_path.exists():
        return {}
    try:
        doc = _load_yaml(schema_path)
    except (AssertionError, yaml.YAMLError):
        return {}
    entities = doc.get("entities") or {}
    if isinstance(entities, list):
        out: Dict[str, Dict[str, Any]] = {}
        for item in entities:
            if isinstance(item, dict) and item.get("name"):
                out[item["name"]] = item
        return out
    if isinstance(entities, dict):
        return {k: v for k, v in entities.items() if isinstance(v, dict)}
    return {}


def _canonical_source_class_values() -> List[str]:
    path = SCHEMA_ROOT / "source_class.yaml"
    assert path.exists(), (
        f"missing canonical source_class vocabulary at {path.relative_to(SUBSYS)}"
    )
    doc = _load_yaml(path)
    values = doc.get("source_class_values")
    assert isinstance(values, list) and values, (
        f"{path.relative_to(SUBSYS)}: 'source_class_values' must be a non-empty list"
    )
    return values


def _entity_contract_source_class_enum() -> List[str]:
    path = SCHEMA_ROOT / "entity_contract.schema.yaml"
    assert path.exists(), (
        f"missing entity_contract schema at {path.relative_to(SUBSYS)}"
    )
    doc = _load_yaml(path)
    props = doc.get("properties") or {}
    sc = props.get("source_class") or {}
    enum = sc.get("enum")
    assert isinstance(enum, list) and enum, (
        f"{path.relative_to(SUBSYS)}: properties.source_class.enum must be a "
        f"non-empty list"
    )
    return enum


# ---------------------------------------------------------------------------
# (1) Single source of truth: schema enum == canonical list
# ---------------------------------------------------------------------------

def test_source_class_enum_matches_canonical_list():
    """entity_contract.schema.yaml source_class enum must equal the list in
    _schema/source_class.yaml — order included, so neither can drift."""
    canonical = _canonical_source_class_values()
    schema_enum = _entity_contract_source_class_enum()
    assert schema_enum == canonical, (
        "source_class enum in entity_contract.schema.yaml does not match the "
        "canonical list in _schema/source_class.yaml.\n"
        f"  schema enum: {schema_enum}\n"
        f"  canonical:   {canonical}"
    )


# ---------------------------------------------------------------------------
# (2) Every entity in the 4 new domains declares a canonical source_class
# ---------------------------------------------------------------------------

def test_new_domain_entities_declare_source_class():
    canonical = set(_canonical_source_class_values())
    failures: List[str] = []
    for dom in SOURCE_CLASS_DOMAINS:
        entities = _domain_entities(dom)
        if not entities:
            failures.append(f"{dom}: schema.yaml missing or declares no entities")
            continue
        for entity_name, entity_body in entities.items():
            sc = entity_body.get("source_class")
            if sc is None:
                failures.append(
                    f"{dom}.schema.yaml#entities.{entity_name}: missing source_class"
                )
            elif sc not in canonical:
                failures.append(
                    f"{dom}.schema.yaml#entities.{entity_name}: source_class "
                    f"{sc!r} not in canonical list {sorted(canonical)}"
                )
    assert not failures, (
        "new-domain source_class validation failed:\n  - " + "\n  - ".join(failures)
    )
