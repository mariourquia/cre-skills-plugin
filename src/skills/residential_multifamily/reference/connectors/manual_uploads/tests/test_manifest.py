"""Manual Uploads connector manifest conformance tests.

Uses fixtures from reference/connectors/conftest.py (auto-discovered by pytest).
"""
from __future__ import annotations

from pathlib import Path


CONNECTOR_DIR = Path(__file__).resolve().parents[1]


def test_manifest_conforms_to_schema(connector_manifest_schema, connector_helpers):
    manifest = connector_helpers["load_yaml"](CONNECTOR_DIR / "manifest.yaml")
    errors = connector_helpers["validate_against_schema"](manifest, connector_manifest_schema)
    assert not errors, f"manual_uploads manifest failed schema: {errors}"


def test_manifest_entities_present_in_schema(connector_helpers):
    manifest = connector_helpers["load_yaml"](CONNECTOR_DIR / "manifest.yaml")
    schema = connector_helpers["load_yaml"](CONNECTOR_DIR / "schema.yaml")
    entities = connector_helpers["entities_of"](schema)
    missing = [e for e in manifest["entities"] if e not in entities]
    assert not missing, f"Entities in manifest missing from schema.yaml: {missing}"


def test_manifest_is_vendor_neutral_stub(connector_helpers):
    manifest = connector_helpers["load_yaml"](CONNECTOR_DIR / "manifest.yaml")
    assert manifest["vendor_neutral"] is True
    assert manifest["status"] == "stub"
    assert manifest["connector_id"] == "manual_uploads"


def test_entity_contracts_conform(entity_contract_schema, connector_helpers):
    schema = connector_helpers["load_yaml"](CONNECTOR_DIR / "schema.yaml")
    entities = connector_helpers["entities_of"](schema)
    for entity_name, contract in entities.items():
        errors = connector_helpers["validate_against_schema"](contract, entity_contract_schema)
        assert not errors, f"manual_uploads entity {entity_name} failed: {errors}"
        assert contract["entity_name"] == entity_name


def test_reconciliation_checks_conform(recon_check_schema, connector_helpers):
    recon = connector_helpers["load_yaml"](CONNECTOR_DIR / "reconciliation_checks.yaml")
    checks = recon.get("checks", recon if isinstance(recon, list) else [])
    assert isinstance(checks, list) and len(checks) >= 3
    for idx, check in enumerate(checks):
        errors = connector_helpers["validate_against_schema"](check, recon_check_schema)
        assert not errors, f"manual_uploads check #{idx} failed: {errors}"
