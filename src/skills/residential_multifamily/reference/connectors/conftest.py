"""Shared fixtures and helpers for connector test stubs.

Re-uses the lightweight JSON Schema validator pattern from
residential_multifamily/tests/conftest.py. Loads the three connector schemas
once so every connector's tests/ can assert conformance without duplicating
loading logic.

Helpers (load_yaml, load_json, validate_against_schema, assert_sample_conforms)
are exposed both as module-level callables AND as pytest fixtures so per-connector
tests can use either style.

Only stdlib + PyYAML.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

import pytest
import yaml


CONNECTORS_ROOT = Path(__file__).resolve().parent
SUBSYS_ROOT = CONNECTORS_ROOT.parents[1]
SCHEMA_DIR = CONNECTORS_ROOT / "_schema"


def load_yaml(path: Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path: Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


CONNECTOR_MANIFEST_SCHEMA = load_yaml(SCHEMA_DIR / "connector_manifest.schema.yaml")
ENTITY_CONTRACT_SCHEMA = load_yaml(SCHEMA_DIR / "entity_contract.schema.yaml")
RECON_CHECK_SCHEMA = load_yaml(SCHEMA_DIR / "reconciliation_check.schema.yaml")


def validate_against_schema(instance: Any, schema: Dict[str, Any], path: str = "$") -> List[str]:
    """Subset JSON Schema validator. Mirrors residential_multifamily/tests/conftest.py."""
    errors: List[str] = []
    if schema is None:
        return errors
    if "const" in schema:
        if instance != schema["const"]:
            errors.append(f"{path}: expected const {schema['const']!r}, got {instance!r}")
        return errors
    if "enum" in schema:
        if instance not in schema["enum"]:
            errors.append(f"{path}: value {instance!r} not in enum {schema['enum']}")
    t = schema.get("type")
    if t == "object":
        if not isinstance(instance, dict):
            errors.append(f"{path}: expected object, got {type(instance).__name__}")
            return errors
        required = schema.get("required", []) or []
        for key in required:
            if key not in instance:
                errors.append(f"{path}: missing required field '{key}'")
        props = schema.get("properties", {}) or {}
        additional = schema.get("additionalProperties", True)
        for key, val in instance.items():
            if key in props:
                if val is None and key not in required:
                    continue
                errors.extend(validate_against_schema(val, props[key], f"{path}.{key}"))
            elif additional is False:
                errors.append(f"{path}: unexpected field '{key}'")
        return errors
    if t == "array":
        if not isinstance(instance, list):
            errors.append(f"{path}: expected array, got {type(instance).__name__}")
            return errors
        min_items = schema.get("minItems")
        if min_items is not None and len(instance) < min_items:
            errors.append(f"{path}: array length {len(instance)} < minItems {min_items}")
        item_schema = schema.get("items")
        if item_schema:
            for idx, item in enumerate(instance):
                errors.extend(validate_against_schema(item, item_schema, f"{path}[{idx}]"))
        return errors
    if t == "string":
        if not isinstance(instance, str):
            errors.append(f"{path}: expected string, got {type(instance).__name__}")
            return errors
        pat = schema.get("pattern")
        if pat and not re.match(pat, instance):
            errors.append(f"{path}: string {instance!r} does not match pattern {pat!r}")
        return errors
    if t == "integer":
        if not isinstance(instance, int) or isinstance(instance, bool):
            errors.append(f"{path}: expected integer, got {type(instance).__name__}")
        return errors
    if t == "number":
        if not isinstance(instance, (int, float)) or isinstance(instance, bool):
            errors.append(f"{path}: expected number, got {type(instance).__name__}")
        return errors
    if t == "boolean":
        if not isinstance(instance, bool):
            errors.append(f"{path}: expected boolean, got {type(instance).__name__}")
        return errors
    return errors


def entities_of(schema_yaml: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Return the entity map from a schema.yaml that wraps entities under
    the top-level `entities:` key. Accepts the legacy shape (entities as
    top-level mapping keys) for backward compatibility.
    """
    if "entities" in schema_yaml and isinstance(schema_yaml["entities"], dict):
        return schema_yaml["entities"]
    return schema_yaml


def assert_sample_conforms(sample: Dict[str, Any], schema_yaml: Dict[str, Any], entity_name: str) -> None:
    """Primary-key shape check. Raises ValueError on malformed.

    Asserts that every record under sample[entity_name] carries non-null values
    for every field in the entity contract's primary_key list.
    """
    entities = entities_of(schema_yaml)
    entity_contract = entities.get(entity_name)
    if entity_contract is None:
        raise ValueError(f"No entity contract for '{entity_name}' in schema.yaml")
    records = sample.get(entity_name, [])
    if not isinstance(records, list):
        raise ValueError(f"sample[{entity_name}] must be a list, got {type(records).__name__}")
    pk_fields = entity_contract["primary_key"]
    for idx, rec in enumerate(records):
        for pk in pk_fields:
            if pk not in rec or rec[pk] is None:
                raise ValueError(
                    f"sample[{entity_name}][{idx}] missing primary key field '{pk}'"
                )


# Fixtures -----------------------------------------------------------------

@pytest.fixture(scope="session")
def connector_manifest_schema() -> Dict[str, Any]:
    return CONNECTOR_MANIFEST_SCHEMA


@pytest.fixture(scope="session")
def entity_contract_schema() -> Dict[str, Any]:
    return ENTITY_CONTRACT_SCHEMA


@pytest.fixture(scope="session")
def recon_check_schema() -> Dict[str, Any]:
    return RECON_CHECK_SCHEMA


@pytest.fixture(scope="session")
def connector_helpers():
    """Exposes helper callables for tests that prefer fixture injection."""
    return {
        "load_yaml": load_yaml,
        "load_json": load_json,
        "validate_against_schema": validate_against_schema,
        "assert_sample_conforms": assert_sample_conforms,
        "entities_of": entities_of,
    }
