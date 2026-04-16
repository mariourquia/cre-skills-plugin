"""Market data connector sample input + normalized + mapping coherence tests."""
from __future__ import annotations

import copy
from pathlib import Path

import pytest


CONNECTOR_DIR = Path(__file__).resolve().parents[1]


def _entities_with_mapped_fields(mapping):
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


def test_sample_normalized_has_primary_keys_for_every_entity(connector_helpers):
    schema = connector_helpers["load_yaml"](CONNECTOR_DIR / "schema.yaml")
    normalized = connector_helpers["load_json"](CONNECTOR_DIR / "sample_normalized.json")
    entities = connector_helpers["entities_of"](schema)
    for entity in entities:
        if entity not in normalized:
            continue
        connector_helpers["assert_sample_conforms"](normalized, schema, entity)


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
    schema = connector_helpers["load_yaml"](CONNECTOR_DIR / "schema.yaml")
    normalized = connector_helpers["load_json"](CONNECTOR_DIR / "sample_normalized.json")
    broken = copy.deepcopy(normalized)
    assert broken["rent_comp"], "test requires at least one rent_comp sample"
    broken["rent_comp"][0].pop("comp_observation_id", None)
    with pytest.raises(ValueError) as exc:
        connector_helpers["assert_sample_conforms"](broken, schema, "rent_comp")
    assert "comp_observation_id" in str(exc.value)
