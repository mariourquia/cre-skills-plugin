"""Procore construction adapter: manifest and integration conformance tests."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml


ADAPTER_DIR = Path(__file__).resolve().parents[1]
ADAPTERS_ROOT = ADAPTER_DIR.parent
if str(ADAPTERS_ROOT) not in sys.path:
    sys.path.insert(0, str(ADAPTERS_ROOT))

from _test_helpers import run_adapter_manifest_checks  # noqa: E402


def test_procore_adapter_conforms(adapter_manifest_schema):
    run_adapter_manifest_checks(
        adapter_dir=ADAPTER_DIR,
        schema=adapter_manifest_schema,
        expected_connector_domain="construction",
        expected_vendor_family="procore_family",
    )


def test_procore_required_files_present():
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


def test_procore_source_registry_entry_loads():
    src = ADAPTER_DIR / "source_registry_entry.yaml"
    data = yaml.safe_load(src.read_text())
    rec = data["records"][0]
    assert rec["source_id"] == "procore_prod"
    assert rec["source_domain"] == "construction"
