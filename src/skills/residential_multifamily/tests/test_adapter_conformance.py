"""Adapter conformance tests.

Validates reference/connectors/adapters/ directory. Every vendor-family adapter
must ship a manifest.yaml conforming to adapter_manifest.schema.yaml plus a
README, example_raw_payload.jsonl, mapping_template.yaml, and
normalized_output_example.jsonl. All stub manifests must declare status=stub.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import pytest
import yaml

from conftest import SUBSYS, validate_against_schema


ADAPTERS_ROOT = SUBSYS / "reference" / "connectors" / "adapters"
ADAPTER_SCHEMA = ADAPTERS_ROOT / "adapter_manifest.schema.yaml"
REGISTRY = ADAPTERS_ROOT / "vendor_family_registry.yaml"

# wave-0/1 generic vendor-family stubs follow the full legacy ADAPTER_FILES
# layout (single example_raw_payload.jsonl + mapping_template.yaml +
# normalized_output_example.jsonl).
LEGACY_ADAPTER_DIRS = [
    "pms_vendor_family_stub",
    "gl_vendor_family_stub",
    "crm_vendor_family_stub",
    "ap_vendor_family_stub",
    "market_data_provider_stub",
    "construction_platform_stub",
    "manual_excel_ingestion_stub",
    "hr_payroll_vendor_family_stub",
]

# wave-4 / wave-5 stack-specific adapters use a different layout:
# source_contract.yaml + normalized_contract.yaml + field_mapping.yaml
# + sample_raw/*.jsonl + sample_normalized/*.jsonl. Per-adapter local
# test files validate the richer contract; this conformance file checks
# only the lowest-common-denominator (manifest.yaml + README.md).
STACK_ADAPTER_DIRS = [
    "appfolio_pms",
    "sage_intacct_gl",
    "procore_construction",
    "dealpath_deal_pipeline",
    "excel_market_surveys",
    "manual_sources_expanded",
    "graysail_placeholder",
    "yardi_multi_role",
]

EXPECTED_ADAPTER_DIRS = LEGACY_ADAPTER_DIRS + STACK_ADAPTER_DIRS

LEGACY_ADAPTER_FILES = [
    "manifest.yaml",
    "README.md",
    "example_raw_payload.jsonl",
    "mapping_template.yaml",
    "normalized_output_example.jsonl",
]

STACK_ADAPTER_FILES = [
    "manifest.yaml",
    "README.md",
]


def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict), f"{path}: expected mapping"
    return data


def test_adapters_directory_present():
    missing: List[str] = []
    for top in ("README.md", "adapter_manifest.schema.yaml", "adapter_lifecycle.md",
                "example_adapter_authoring_guide.md", "gotchas_and_antipatterns.md",
                "vendor_family_registry.yaml"):
        if not (ADAPTERS_ROOT / top).exists():
            missing.append(str((ADAPTERS_ROOT / top).relative_to(SUBSYS)))
    for adapter in EXPECTED_ADAPTER_DIRS:
        if not (ADAPTERS_ROOT / adapter).is_dir():
            missing.append(f"{(ADAPTERS_ROOT / adapter).relative_to(SUBSYS)}/ (directory)")
    assert not missing, "adapter family missing:\n  - " + "\n  - ".join(missing)


def test_adapter_internal_files_present():
    failures: List[str] = []
    for adapter in LEGACY_ADAPTER_DIRS:
        ad_root = ADAPTERS_ROOT / adapter
        if not ad_root.is_dir():
            continue
        for rel in LEGACY_ADAPTER_FILES:
            p = ad_root / rel
            if not p.exists():
                failures.append(str(p.relative_to(SUBSYS)))
    for adapter in STACK_ADAPTER_DIRS:
        ad_root = ADAPTERS_ROOT / adapter
        if not ad_root.is_dir():
            continue
        for rel in STACK_ADAPTER_FILES:
            p = ad_root / rel
            if not p.exists():
                failures.append(str(p.relative_to(SUBSYS)))
    assert not failures, "adapter files missing:\n  - " + "\n  - ".join(failures)


def test_adapter_manifests_conform_to_schema():
    schema = _load_yaml(ADAPTER_SCHEMA)
    failures: List[str] = []
    # Legacy stub manifests are validated strictly against the canonical schema.
    for adapter in LEGACY_ADAPTER_DIRS:
        manifest = ADAPTERS_ROOT / adapter / "manifest.yaml"
        if not manifest.exists():
            continue
        doc = _load_yaml(manifest)
        errs = validate_against_schema(doc, schema, path=f"adapters/{adapter}/manifest.yaml")
        failures.extend(errs)
    # Stack-specific manifests carry additional fields (object_coverage,
    # multi-line gotchas) that the legacy schema rejects via additionalProperties.
    # Per-adapter test files cover the richer schema. Here we only spot-check
    # the required-id fields so adapter directories stay registry-resolvable.
    REQUIRED_IDS = ["adapter_id", "adapter_name", "vendor_family", "connector_domain", "status"]
    for adapter in STACK_ADAPTER_DIRS:
        manifest = ADAPTERS_ROOT / adapter / "manifest.yaml"
        if not manifest.exists():
            continue
        doc = _load_yaml(manifest)
        for key in REQUIRED_IDS:
            if key not in doc:
                failures.append(f"adapters/{adapter}/manifest.yaml missing required id field '{key}'")
    assert not failures, "adapter manifest validation failed:\n  - " + "\n  - ".join(failures)


def test_adapter_manifests_declare_stub_status():
    failures: List[str] = []
    for adapter in EXPECTED_ADAPTER_DIRS:
        manifest = ADAPTERS_ROOT / adapter / "manifest.yaml"
        if not manifest.exists():
            continue
        doc = _load_yaml(manifest)
        status = doc.get("status")
        if status != "stub":
            failures.append(f"{adapter}: status={status!r}, expected 'stub'")
    assert not failures, "adapter status check failed:\n  - " + "\n  - ".join(failures)


def test_vendor_family_registry_matches_adapter_dirs():
    doc = _load_yaml(REGISTRY)
    adapters = doc.get("adapters") or doc.get("records") or doc.get("entries") or []
    if isinstance(adapters, dict):
        adapters = list(adapters.values())
    assert isinstance(adapters, list) and adapters, "vendor_family_registry.yaml must list adapters"
    ids = {entry.get("adapter_id") for entry in adapters if isinstance(entry, dict)}
    missing = sorted(set(EXPECTED_ADAPTER_DIRS) - ids)
    extra = sorted(ids - set(EXPECTED_ADAPTER_DIRS))
    problems: List[str] = []
    if missing:
        problems.append(f"registry missing adapter_ids: {missing}")
    if extra:
        problems.append(f"registry has unknown adapter_ids: {extra}")
    assert not problems, "\n  - ".join(problems)
