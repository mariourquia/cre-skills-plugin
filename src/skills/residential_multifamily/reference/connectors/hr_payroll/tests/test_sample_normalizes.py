"""HR/Payroll connector sample input + normalized + mapping coherence tests."""
from __future__ import annotations

import copy
from pathlib import Path

import pytest


CONNECTOR_DIR = Path(__file__).resolve().parents[1]


def _entities_with_mapped_fields(mapping):
    """Return entity names that have a populated fields: list (not TODO stubs)."""
    out = []
    for name, block in mapping.items():
        if isinstance(block, dict) and isinstance(block.get("fields"), list):
            out.append(name)
    return out


def test_sample_input_shape_matches_mapping_source_columns(connector_helpers):
    mapping = connector_helpers["load_yaml"](CONNECTOR_DIR / "mapping.yaml")
    sample_input = connector_helpers["load_json"](CONNECTOR_DIR / "sample_input.json")
    for entity in _entities_with_mapped_fields(mapping):
        source_cols = {f["source_column"] for f in mapping[entity]["fields"] if f.get("required")}
        records = sample_input.get(entity, [])
        assert records, f"sample_input has no rows for entity '{entity}'"
        for idx, rec in enumerate(records):
            missing = source_cols - set(rec.keys())
            assert not missing, (
                f"sample_input[{entity}][{idx}] missing required source columns: {missing}"
            )


def test_sample_input_only_references_declared_entities(connector_helpers):
    schema = connector_helpers["load_yaml"](CONNECTOR_DIR / "schema.yaml")
    sample_input = connector_helpers["load_json"](CONNECTOR_DIR / "sample_input.json")
    declared = set(connector_helpers["entities_of"](schema).keys())
    stray = set(sample_input.keys()) - declared
    assert not stray, f"sample_input references undeclared entities: {stray}"


def test_sample_normalized_has_primary_keys_for_every_entity(connector_helpers):
    schema = connector_helpers["load_yaml"](CONNECTOR_DIR / "schema.yaml")
    normalized = connector_helpers["load_json"](CONNECTOR_DIR / "sample_normalized.json")
    entities = connector_helpers["entities_of"](schema)
    for entity in entities:
        if entity not in normalized:
            continue
        connector_helpers["assert_sample_conforms"](normalized, schema, entity)


def test_sample_normalized_required_fields_non_null(connector_helpers):
    """Every required field in each entity contract is non-null in sample_normalized."""
    schema = connector_helpers["load_yaml"](CONNECTOR_DIR / "schema.yaml")
    normalized = connector_helpers["load_json"](CONNECTOR_DIR / "sample_normalized.json")
    entities = connector_helpers["entities_of"](schema)
    for entity_name, contract in entities.items():
        rows = normalized.get(entity_name, [])
        if not rows:
            continue
        required_names = [f["name"] for f in contract.get("required_fields", [])]
        for idx, row in enumerate(rows):
            for fname in required_names:
                assert fname in row, (
                    f"sample_normalized[{entity_name}][{idx}] missing required field '{fname}'"
                )
                assert row[fname] is not None, (
                    f"sample_normalized[{entity_name}][{idx}] required field '{fname}' is null"
                )


def test_sample_provenance_fields_present(connector_helpers):
    """Every normalized record carries at minimum source_name, source_date, source_row_id."""
    normalized = connector_helpers["load_json"](CONNECTOR_DIR / "sample_normalized.json")
    for entity, rows in normalized.items():
        for idx, row in enumerate(rows):
            for pf in ("source_name", "source_date", "source_row_id"):
                assert row.get(pf), (
                    f"sample_normalized[{entity}][{idx}] missing provenance '{pf}'"
                )


def test_sample_tagged_as_sample(connector_helpers):
    """Every sample record carries source_name='sample_feed' as the stub tag."""
    sample_input = connector_helpers["load_json"](CONNECTOR_DIR / "sample_input.json")
    sample_normalized = connector_helpers["load_json"](CONNECTOR_DIR / "sample_normalized.json")
    for entity, rows in sample_input.items():
        assert isinstance(rows, list), f"{entity} must be a list"
        for row in rows:
            assert row.get("source_name") == "sample_feed", (
                f"sample_input[{entity}] record missing sample_feed tag"
            )
    for entity, rows in sample_normalized.items():
        for row in rows:
            assert row.get("source_name") == "sample_feed", (
                f"sample_normalized[{entity}] record missing sample_feed tag"
            )


def test_malformed_sample_raises_readable_error(connector_helpers):
    """Negative case: strip primary key from a record and confirm the helper surfaces it."""
    schema = connector_helpers["load_yaml"](CONNECTOR_DIR / "schema.yaml")
    normalized = connector_helpers["load_json"](CONNECTOR_DIR / "sample_normalized.json")
    broken = copy.deepcopy(normalized)
    assert broken["payroll_line"], "test requires at least one payroll_line sample"
    broken["payroll_line"][0].pop("payroll_line_id", None)
    with pytest.raises(ValueError) as exc:
        connector_helpers["assert_sample_conforms"](broken, schema, "payroll_line")
    assert "payroll_line_id" in str(exc.value)
