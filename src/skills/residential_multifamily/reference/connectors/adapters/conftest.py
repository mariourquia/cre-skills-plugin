"""Shared fixtures for adapter stub tests.

Loads the adapter manifest schema once so every per-adapter test file can
assert conformance without duplicating loading logic. Reuses the connector
subsystem's lightweight JSON Schema validator via the parent conftest.

Only stdlib + PyYAML.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import pytest
import yaml


ADAPTERS_ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = ADAPTERS_ROOT / "adapter_manifest.schema.yaml"
REGISTRY_PATH = ADAPTERS_ROOT / "vendor_family_registry.yaml"


def _load_yaml(path: Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


ADAPTER_MANIFEST_SCHEMA = _load_yaml(SCHEMA_PATH)
VENDOR_FAMILY_REGISTRY = _load_yaml(REGISTRY_PATH)


@pytest.fixture(scope="session")
def adapter_manifest_schema() -> Dict[str, Any]:
    return ADAPTER_MANIFEST_SCHEMA


@pytest.fixture(scope="session")
def vendor_family_registry() -> Dict[str, Any]:
    return VENDOR_FAMILY_REGISTRY


@pytest.fixture(scope="session")
def adapters_root() -> Path:
    return ADAPTERS_ROOT
