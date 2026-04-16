"""AppFolio PMS adapter: manifest and integration conformance tests."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml


ADAPTER_DIR = Path(__file__).resolve().parents[1]
ADAPTERS_ROOT = ADAPTER_DIR.parent
if str(ADAPTERS_ROOT) not in sys.path:
    sys.path.insert(0, str(ADAPTERS_ROOT))

from _test_helpers import run_adapter_manifest_checks  # noqa: E402


def test_appfolio_adapter_conforms(adapter_manifest_schema):
    run_adapter_manifest_checks(
        adapter_dir=ADAPTER_DIR,
        schema=adapter_manifest_schema,
        expected_connector_domain="pms",
        expected_vendor_family="appfolio_family",
    )


def test_appfolio_required_files_present():
    required = [
        "manifest.yaml",
        "README.md",
        "source_contract.yaml",
        "normalized_contract.yaml",
        "field_mapping.yaml",
        "source_registry_entry.yaml",
    ]
    for name in required:
        assert (ADAPTER_DIR / name).exists(), f"missing required file: {name}"


def test_appfolio_sample_raw_present():
    sample_raw = ADAPTER_DIR / "sample_raw"
    assert sample_raw.exists() and sample_raw.is_dir()
    expected = {"properties.jsonl", "units.jsonl", "leases.jsonl"}
    actual = {p.name for p in sample_raw.iterdir() if p.is_file()}
    missing = expected - actual
    assert not missing, f"sample_raw missing: {missing}"


def test_appfolio_source_registry_entry_loads():
    src = ADAPTER_DIR / "source_registry_entry.yaml"
    data = yaml.safe_load(src.read_text())
    rec = data["records"][0]
    assert rec["source_id"] == "appfolio_prod"
    assert rec["source_domain"] == "pms"
    assert rec["pii_classification"] == "high"
