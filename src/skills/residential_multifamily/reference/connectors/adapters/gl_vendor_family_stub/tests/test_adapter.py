"""GL vendor family stub: manifest and payload conformance tests."""
from __future__ import annotations

import sys
from pathlib import Path


ADAPTER_DIR = Path(__file__).resolve().parents[1]
ADAPTERS_ROOT = ADAPTER_DIR.parent
if str(ADAPTERS_ROOT) not in sys.path:
    sys.path.insert(0, str(ADAPTERS_ROOT))

from _test_helpers import run_adapter_manifest_checks  # noqa: E402


def test_gl_adapter_conforms(adapter_manifest_schema):
    run_adapter_manifest_checks(
        adapter_dir=ADAPTER_DIR,
        schema=adapter_manifest_schema,
        expected_connector_domain="gl",
        expected_vendor_family="generic_erp_stub",
    )
