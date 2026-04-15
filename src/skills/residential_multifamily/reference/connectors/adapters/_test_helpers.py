"""Shared helper for adapter test files.

Every per-adapter tests/test_adapter.py calls run_adapter_manifest_checks()
with its adapter directory. The helper asserts manifest conformance to
adapter_manifest.schema.yaml and enforces the stub-stage invariants
(status: stub, synthetic samples, status tags on payload files).

The helper is intentionally small. It does not validate mapping template
content against the canonical mapping.yaml; that check is reserved for
starter-stage tests which are out of scope for the stub-only pass.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import yaml


def _load_yaml(path: Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def _validate(instance: Any, schema: Dict[str, Any], path: str = "$") -> List[str]:
    """Minimal JSON Schema validator. Mirrors the one in the connectors
    conftest but scoped to what adapter manifests need."""
    import re as _re

    errors: List[str] = []
    if schema is None:
        return errors
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value {instance!r} not in enum {schema['enum']}")
    t = schema.get("type")
    if t == "object":
        if not isinstance(instance, dict):
            errors.append(f"{path}: expected object, got {type(instance).__name__}")
            return errors
        for key in schema.get("required", []) or []:
            if key not in instance:
                errors.append(f"{path}: missing required field '{key}'")
        props = schema.get("properties", {}) or {}
        additional = schema.get("additionalProperties", True)
        for key, val in instance.items():
            if key in props:
                if val is None and key not in (schema.get("required", []) or []):
                    continue
                errors.extend(_validate(val, props[key], f"{path}.{key}"))
            elif additional is False:
                errors.append(f"{path}: unexpected field '{key}'")
        return errors
    if t == "array":
        if not isinstance(instance, list):
            errors.append(f"{path}: expected array, got {type(instance).__name__}")
            return errors
        min_items = schema.get("minItems")
        if min_items is not None and len(instance) < min_items:
            errors.append(f"{path}: array length {len(instance)} < minItems {min_items}")
        item_schema = schema.get("items")
        if item_schema:
            for idx, item in enumerate(instance):
                errors.extend(_validate(item, item_schema, f"{path}[{idx}]"))
        return errors
    if t == "string":
        if not isinstance(instance, str):
            errors.append(f"{path}: expected string, got {type(instance).__name__}")
            return errors
        pat = schema.get("pattern")
        if pat and not _re.match(pat, instance):
            errors.append(f"{path}: {instance!r} does not match {pat!r}")
        return errors
    if t == "integer":
        if not isinstance(instance, int) or isinstance(instance, bool):
            errors.append(f"{path}: expected integer, got {type(instance).__name__}")
        return errors
    if t == "boolean":
        if not isinstance(instance, bool):
            errors.append(f"{path}: expected boolean, got {type(instance).__name__}")
        return errors
    return errors


def run_adapter_manifest_checks(
    adapter_dir: Path,
    schema: Dict[str, Any],
    expected_connector_domain: str,
    expected_vendor_family: str,
) -> None:
    """Assert the stub-stage invariants for an adapter directory.

    Supports two layouts:
      - LEGACY (wave-0/1 vendor-family stubs): single-file payload pattern
        (example_raw_payload.jsonl + normalized_output_example.jsonl +
        mapping_template.yaml). Strict manifest schema validation.
      - STACK (wave-4/5 stack-specific adapters): multi-file directory
        pattern (sample_raw/*.jsonl + sample_normalized/*.jsonl +
        source_contract.yaml + normalized_contract.yaml + field_mapping.yaml).
        Per-adapter test files (test_<adapter>_adapter.py) cover the richer
        contract; this helper only spot-checks required-id manifest fields.

    Checks (both layouts):
      1. manifest.yaml exists and parses.
      2. status is 'stub'.
      3. connector_domain matches the expected canonical domain.
      4. vendor_family matches the expected generic placeholder slug.
      5. adapter_id matches the adapter directory name.

    Layout-specific checks are then applied.
    """
    manifest_path = adapter_dir / "manifest.yaml"
    assert manifest_path.exists(), f"Missing manifest.yaml in {adapter_dir}"
    manifest = _load_yaml(manifest_path)

    # Detect layout: STACK adapters carry one of these markers indicating
    # the wave-4/5 multi-file directory pattern instead of the legacy
    # single-file payload pattern.
    is_stack_layout = (
        (adapter_dir / "sample_raw").is_dir()
        or (adapter_dir / "sample_files").is_dir()
        or (adapter_dir / "sample_valid").is_dir()
        or (adapter_dir / "source_contract.yaml").exists()
        or (adapter_dir / "provisional_source_contract.yaml").exists()
        or (adapter_dir / "normalized_contract.yaml").exists()
        or (adapter_dir / "file_family_registry.yaml").exists()
        or (adapter_dir / "intake_manifest.yaml").exists()
    )

    if is_stack_layout:
        # Stack layout: only spot-check required-id fields. The richer
        # contract is validated by per-adapter test_<adapter>_adapter.py.
        for key in ("adapter_id", "adapter_name", "vendor_family",
                    "connector_domain", "status"):
            assert key in manifest, (
                f"Stack-layout adapter {adapter_dir.name}/manifest.yaml "
                f"missing required id field {key!r}"
            )
    else:
        # Legacy layout: full schema validation.
        errors = _validate(manifest, schema)
        assert not errors, (
            f"Adapter manifest failed schema for {adapter_dir.name}: {errors}"
        )

    assert manifest["status"] == "stub", (
        f"Adapter {adapter_dir.name} must ship at status: stub, got {manifest['status']!r}"
    )
    assert manifest["connector_domain"] == expected_connector_domain, (
        f"Adapter {adapter_dir.name} connector_domain mismatch: "
        f"expected {expected_connector_domain!r}, got {manifest['connector_domain']!r}"
    )
    assert manifest["vendor_family"] == expected_vendor_family, (
        f"Adapter {adapter_dir.name} vendor_family mismatch: "
        f"expected {expected_vendor_family!r}, got {manifest['vendor_family']!r}"
    )
    assert manifest["adapter_id"] == adapter_dir.name, (
        f"Adapter {adapter_dir.name}: adapter_id {manifest['adapter_id']!r} "
        f"must equal directory name"
    )

    if is_stack_layout:
        # Stack-layout adapters keep sample data under one of: sample_raw/,
        # sample_files/, sample_valid/, sample_normalized/. Spot-check that
        # at least one sample directory exists with content.
        sample_dirs = [
            adapter_dir / "sample_raw",
            adapter_dir / "sample_files",
            adapter_dir / "sample_valid",
            adapter_dir / "sample_normalized",
        ]
        has_any_sample = any(
            d.is_dir() and any(f for f in d.iterdir() if f.is_file() and not f.name.startswith("."))
            for d in sample_dirs
        )
        assert has_any_sample, (
            f"{adapter_dir.name} has stack layout but no sample data found in "
            f"sample_raw/, sample_files/, sample_valid/, or sample_normalized/"
        )
        return

    # Legacy-layout payload status tags.
    raw_path = adapter_dir / "example_raw_payload.jsonl"
    assert raw_path.exists(), f"Missing example_raw_payload.jsonl in {adapter_dir}"
    rows = _load_jsonl(raw_path)
    assert rows, f"example_raw_payload.jsonl is empty in {adapter_dir}"
    for idx, row in enumerate(rows):
        assert row.get("status") in ("sample", "stub", "template"), (
            f"{adapter_dir.name}/example_raw_payload.jsonl row {idx} "
            f"missing sample/stub/template status tag"
        )

    normalized_path = adapter_dir / "normalized_output_example.jsonl"
    assert normalized_path.exists(), f"Missing normalized_output_example.jsonl in {adapter_dir}"
    norm_rows = _load_jsonl(normalized_path)
    assert norm_rows, f"normalized_output_example.jsonl is empty in {adapter_dir}"
    for idx, row in enumerate(norm_rows):
        assert row.get("status") in ("sample", "stub", "template"), (
            f"{adapter_dir.name}/normalized_output_example.jsonl row {idx} "
            f"missing sample/stub/template status tag"
        )

    template_path = adapter_dir / "mapping_template.yaml"
    assert template_path.exists(), f"Missing mapping_template.yaml in {adapter_dir}"
    template = _load_yaml(template_path)
    assert isinstance(template, dict) and template.get("status_tag") in ("template", "stub"), (
        f"{adapter_dir.name}/mapping_template.yaml must carry "
        f"top-level status_tag in {{template, stub}}"
    )
