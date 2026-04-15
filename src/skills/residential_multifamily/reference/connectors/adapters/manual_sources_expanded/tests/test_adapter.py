"""Manual sources expanded adapter: conformance tests."""
from __future__ import annotations

import sys
from pathlib import Path


ADAPTER_DIR = Path(__file__).resolve().parents[1]
ADAPTERS_ROOT = ADAPTER_DIR.parent
if str(ADAPTERS_ROOT) not in sys.path:
    sys.path.insert(0, str(ADAPTERS_ROOT))

from _test_helpers import run_adapter_manifest_checks  # noqa: E402


def test_manual_sources_adapter_conforms(adapter_manifest_schema):
    run_adapter_manifest_checks(
        adapter_dir=ADAPTER_DIR,
        schema=adapter_manifest_schema,
        expected_connector_domain="manual_uploads",
        expected_vendor_family="manual_file_family",
    )


def test_manual_sources_required_files_present():
    required = [
        "manifest.yaml",
        "README.md",
        "dq_rules.yaml",
        "source_registry_entry.yaml",
        "workflow_activation_additions.yaml",
    ]
    for name in required:
        assert (ADAPTER_DIR / name).exists(), f"missing required file: {name}"
