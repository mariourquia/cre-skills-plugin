"""Dealpath deal pipeline adapter: manifest and integration conformance tests."""
from __future__ import annotations

import sys
from pathlib import Path


ADAPTER_DIR = Path(__file__).resolve().parents[1]
ADAPTERS_ROOT = ADAPTER_DIR.parent
if str(ADAPTERS_ROOT) not in sys.path:
    sys.path.insert(0, str(ADAPTERS_ROOT))

from _test_helpers import run_adapter_manifest_checks  # noqa: E402


def test_dealpath_adapter_conforms(adapter_manifest_schema):
    run_adapter_manifest_checks(
        adapter_dir=ADAPTER_DIR,
        schema=adapter_manifest_schema,
        expected_connector_domain="deal_pipeline",
        expected_vendor_family="dealpath_family",
    )


def test_dealpath_required_files_present():
    required = [
        "manifest.yaml",
        "README.md",
        "dq_rules.yaml",
        "source_registry_entry.yaml",
        "workflow_activation_additions.yaml",
    ]
    for name in required:
        assert (ADAPTER_DIR / name).exists(), f"missing required file: {name}"


def test_dealpath_source_registry_entry_loads():
    import yaml
    src = ADAPTER_DIR / "source_registry_entry.yaml"
    data = yaml.safe_load(src.read_text())
    assert "records" in data
    assert len(data["records"]) >= 1
    rec = data["records"][0]
    assert rec["source_id"] == "dealpath_prod"
    assert rec["source_domain"] == "deal_pipeline"
    assert rec["status"] in {"planned", "stubbed", "active", "degraded", "deprecated"}
