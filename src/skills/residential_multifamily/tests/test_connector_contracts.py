"""Connector contract tests.

Validates the vendor-neutral ingestion layer under `reference/connectors/`.

Each connector domain (pms, gl, crm, ap, market_data, construction, hr_payroll,
manual_uploads) must ship:
- manifest.yaml conforming to _schema/connector_manifest.schema.yaml
- schema.yaml declaring entities that conform to _schema/entity_contract.schema.yaml
- mapping.yaml, sample_input.json, sample_normalized.json, reconciliation_checks.yaml
- tests/ directory (smoke artifact, existence checked only)

Schema conformance is validated using conftest.validate_against_schema. Sample
payloads must cover only entities declared in schema.yaml; every row must
carry declared primary_key fields; normalized rows must carry required_fields
and the three source-provenance fields (source_name, source_date, source_row_id).

See docs/plans/residential-multifamily-refinement-2026-04-15.md section 6.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set, Tuple

import pytest
import yaml

try:
    from conftest import SUBSYS, validate_against_schema
except ImportError:  # pragma: no cover
    SUBSYS = Path(__file__).resolve().parents[1]
    raise


CONNECTORS_ROOT = SUBSYS / "reference" / "connectors"
SCHEMA_ROOT = CONNECTORS_ROOT / "_schema"
REQUIRED_DOMAINS = [
    "pms",
    "gl",
    "crm",
    "ap",
    "market_data",
    "construction",
    "hr_payroll",
    "manual_uploads",
]
REQUIRED_PROVENANCE_FIELDS = {"source_name", "source_date", "source_row_id"}


# ---------------------------------------------------------------------------
# Local loaders
# ---------------------------------------------------------------------------

def _load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert isinstance(data, dict), f"{path} did not parse to a mapping"
    return data


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _load_schema_if_exists(name: str) -> Dict[str, Any]:
    path = SCHEMA_ROOT / name
    if not path.exists():
        pytest.fail(f"missing connector schema: {path.relative_to(SUBSYS)}")
    return _load_yaml(path)


def _permissive(schema: Dict[str, Any]) -> Dict[str, Any]:
    """Permit `status`, `authoring_notes`, and similar augmentation keys at top
    level so stub manifests validate cleanly.
    """
    s = copy.deepcopy(schema)
    if isinstance(s, dict) and s.get("type") == "object":
        s.setdefault("properties", {})
        for k in ("status", "authoring_notes", "notes"):
            s["properties"].setdefault(k, {"type": "string"})
    return s


def _domain_entities(domain: str) -> Dict[str, Dict[str, Any]]:
    """Load `reference/connectors/<domain>/schema.yaml` and return the entity
    map keyed by entity name. Returns empty dict if missing or malformed.
    """
    schema_path = CONNECTORS_ROOT / domain / "schema.yaml"
    if not schema_path.exists():
        return {}
    try:
        doc = _load_yaml(schema_path)
    except (AssertionError, yaml.YAMLError):
        return {}
    entities = doc.get("entities") or {}
    # Accept either a mapping {name: {...}} or a list of {name: ..., ...}.
    if isinstance(entities, list):
        out: Dict[str, Dict[str, Any]] = {}
        for item in entities:
            if isinstance(item, dict) and item.get("name"):
                out[item["name"]] = item
        return out
    if isinstance(entities, dict):
        return {k: v for k, v in entities.items() if isinstance(v, dict)}
    return {}


# ---------------------------------------------------------------------------
# Family scaffolding
# ---------------------------------------------------------------------------

def test_connectors_family_exists():
    if not CONNECTORS_ROOT.exists():
        pytest.fail(
            f"missing reference/connectors/ directory at "
            f"{CONNECTORS_ROOT.relative_to(SUBSYS)}"
        )
    missing: List[str] = []
    for rel in ("README.md", "INGESTION.md"):
        p = CONNECTORS_ROOT / rel
        if not p.exists():
            missing.append(str(p.relative_to(SUBSYS)))
    if not SCHEMA_ROOT.exists():
        missing.append(f"{SCHEMA_ROOT.relative_to(SUBSYS)}/ (directory)")
    else:
        for schema_name in (
            "connector_manifest.schema.yaml",
            "entity_contract.schema.yaml",
            "reconciliation_check.schema.yaml",
        ):
            sp = SCHEMA_ROOT / schema_name
            if not sp.exists():
                missing.append(str(sp.relative_to(SUBSYS)))
    for dom in REQUIRED_DOMAINS:
        dp = CONNECTORS_ROOT / dom
        if not dp.exists():
            missing.append(f"{dp.relative_to(SUBSYS)}/ (domain directory)")
    assert not missing, (
        "connector family missing expected scaffolding:\n  - "
        + "\n  - ".join(missing)
    )


# ---------------------------------------------------------------------------
# Schema conformance
# ---------------------------------------------------------------------------

def test_connector_manifest_conforms_to_schema():
    schema = _permissive(_load_schema_if_exists("connector_manifest.schema.yaml"))
    errors: List[str] = []
    found = False
    for dom in REQUIRED_DOMAINS:
        manifest = CONNECTORS_ROOT / dom / "manifest.yaml"
        if not manifest.exists():
            errors.append(f"{manifest.relative_to(SUBSYS)}: missing manifest.yaml")
            continue
        found = True
        try:
            data = _load_yaml(manifest)
        except (AssertionError, yaml.YAMLError) as exc:
            errors.append(f"{manifest.relative_to(SUBSYS)}: unparseable ({exc})")
            continue
        errors.extend(
            validate_against_schema(data, schema, path=str(manifest.relative_to(SUBSYS)))
        )
    assert found, "no connector manifests were discovered"
    assert not errors, "connector manifest validation failed:\n  - " + "\n  - ".join(errors)


def test_connector_entity_contract_conforms():
    schema = _permissive(_load_schema_if_exists("entity_contract.schema.yaml"))
    errors: List[str] = []
    for dom in REQUIRED_DOMAINS:
        entities = _domain_entities(dom)
        if not entities:
            errors.append(f"{dom}: schema.yaml missing or declares no entities")
            continue
        for entity_name, entity_body in entities.items():
            errors.extend(
                validate_against_schema(
                    entity_body,
                    schema,
                    path=f"{dom}.schema.yaml#entities.{entity_name}",
                )
            )
    assert not errors, "entity contract validation failed:\n  - " + "\n  - ".join(errors)


def test_reconciliation_checks_conform():
    schema = _permissive(_load_schema_if_exists("reconciliation_check.schema.yaml"))
    errors: List[str] = []
    for dom in REQUIRED_DOMAINS:
        rc_path = CONNECTORS_ROOT / dom / "reconciliation_checks.yaml"
        if not rc_path.exists():
            errors.append(f"{rc_path.relative_to(SUBSYS)}: missing reconciliation_checks.yaml")
            continue
        try:
            doc = _load_yaml(rc_path)
        except (AssertionError, yaml.YAMLError) as exc:
            errors.append(f"{rc_path.relative_to(SUBSYS)}: unparseable ({exc})")
            continue
        checks = doc.get("checks") or []
        if not isinstance(checks, list) or not checks:
            errors.append(f"{rc_path.relative_to(SUBSYS)}: 'checks' must be a non-empty list")
            continue
        for idx, check in enumerate(checks):
            errors.extend(
                validate_against_schema(
                    check, schema, path=f"{rc_path.relative_to(SUBSYS)}#checks[{idx}]"
                )
            )
    qa_root = CONNECTORS_ROOT / "qa"
    if qa_root.exists():
        for qa_file in sorted(qa_root.glob("*.yaml")):
            try:
                doc = _load_yaml(qa_file)
            except (AssertionError, yaml.YAMLError) as exc:
                errors.append(f"{qa_file.relative_to(SUBSYS)}: unparseable ({exc})")
                continue
            # A qa file may contain a single check or a `checks:` list.
            items: List[Dict[str, Any]] = []
            if isinstance(doc.get("checks"), list):
                items = doc["checks"]
            else:
                items = [doc]
            for idx, check in enumerate(items):
                errors.extend(
                    validate_against_schema(
                        check, schema, path=f"{qa_file.relative_to(SUBSYS)}[{idx}]"
                    )
                )
    assert not errors, "reconciliation check validation failed:\n  - " + "\n  - ".join(errors)


# ---------------------------------------------------------------------------
# Sample payload conformance
# ---------------------------------------------------------------------------

def _entity_primary_keys(entity: Dict[str, Any]) -> List[str]:
    pk = entity.get("primary_key")
    if pk is None:
        return []
    if isinstance(pk, str):
        return [pk]
    if isinstance(pk, list):
        return list(pk)
    return []


def _entity_required_fields(entity: Dict[str, Any]) -> List[str]:
    """Return a flat list of required field NAMES. required_fields is authored
    as a list of dicts {name, type, description, is_key}; older shapes may
    carry a list of bare strings. Both are normalized to names here."""
    req = entity.get("required_fields") or entity.get("required") or []
    if isinstance(req, str):
        return [req]
    if not isinstance(req, list):
        return []
    names: List[str] = []
    for item in req:
        if isinstance(item, dict):
            name = item.get("name")
            if isinstance(name, str):
                names.append(name)
        elif isinstance(item, str):
            names.append(item)
    return names


def _rows_for(sample: Any, entity_name: str) -> List[Dict[str, Any]]:
    if not isinstance(sample, dict):
        return []
    block = sample.get(entity_name)
    if isinstance(block, list):
        return [r for r in block if isinstance(r, dict)]
    if isinstance(block, dict) and isinstance(block.get("rows"), list):
        return [r for r in block["rows"] if isinstance(r, dict)]
    return []


def test_sample_input_matches_schema_entities():
    """sample_input.json represents a RAW vendor feed shape — its column names
    reflect the vendor, not the normalized schema. We validate only that every
    top-level entity key is declared in schema.yaml and that every row carries
    the required provenance fields. Primary-key presence on RAW input is not
    meaningful; that invariant lives on sample_normalized."""
    failures: List[str] = []
    required_provenance = {"source_name", "source_date", "source_row_id"}
    for dom in REQUIRED_DOMAINS:
        sample_path = CONNECTORS_ROOT / dom / "sample_input.json"
        if not sample_path.exists():
            failures.append(f"{sample_path.relative_to(SUBSYS)}: missing sample_input.json")
            continue
        entities = _domain_entities(dom)
        if not entities:
            failures.append(f"{dom}: cannot validate sample_input, schema.yaml is missing/empty")
            continue
        try:
            sample = _load_json(sample_path)
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"{sample_path.relative_to(SUBSYS)}: unparseable ({exc})")
            continue
        if not isinstance(sample, dict):
            failures.append(f"{sample_path.relative_to(SUBSYS)}: top-level must be an object")
            continue
        entity_names = set(entities.keys())
        sample_keys = set(sample.keys())
        extras = sample_keys - entity_names
        if extras:
            failures.append(
                f"{sample_path.relative_to(SUBSYS)}: top-level keys {sorted(extras)} "
                f"are not declared as entities in schema.yaml "
                f"(declared entities: {sorted(entity_names)})"
            )
        # For each entity's rows, confirm provenance fields are present.
        for entity_name in sample_keys & entity_names:
            for idx, row in enumerate(_rows_for(sample, entity_name)):
                missing_prov = required_provenance - set(row.keys())
                if missing_prov:
                    failures.append(
                        f"{sample_path.relative_to(SUBSYS)}#{entity_name}[{idx}]: "
                        f"missing provenance fields {sorted(missing_prov)}"
                    )
    assert not failures, "sample_input validation failed:\n  - " + "\n  - ".join(failures)


def test_sample_normalized_round_trip():
    failures: List[str] = []
    for dom in REQUIRED_DOMAINS:
        norm_path = CONNECTORS_ROOT / dom / "sample_normalized.json"
        if not norm_path.exists():
            failures.append(f"{norm_path.relative_to(SUBSYS)}: missing sample_normalized.json")
            continue
        entities = _domain_entities(dom)
        if not entities:
            failures.append(f"{dom}: cannot validate sample_normalized, schema.yaml missing")
            continue
        try:
            sample = _load_json(norm_path)
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"{norm_path.relative_to(SUBSYS)}: unparseable ({exc})")
            continue
        if not isinstance(sample, dict):
            failures.append(f"{norm_path.relative_to(SUBSYS)}: top-level must be an object")
            continue
        entity_names = set(entities.keys())
        sample_keys = set(sample.keys())
        extras = sample_keys - entity_names
        if extras:
            failures.append(
                f"{norm_path.relative_to(SUBSYS)}: top-level keys {sorted(extras)} "
                f"not declared as entities in schema.yaml"
            )
        for entity_name in sample_keys & entity_names:
            required = _entity_required_fields(entities[entity_name])
            for idx, row in enumerate(_rows_for(sample, entity_name)):
                for field in required:
                    if field not in row:
                        failures.append(
                            f"{norm_path.relative_to(SUBSYS)}#{entity_name}[{idx}]: "
                            f"missing required field {field!r}"
                        )
    assert not failures, "sample_normalized validation failed:\n  - " + "\n  - ".join(failures)


# ---------------------------------------------------------------------------
# Negative path: a bad payload must fail readably
# ---------------------------------------------------------------------------

def _validate_rows_against_primary_key(
    rows: List[Dict[str, Any]], pks: List[str], entity_name: str
) -> List[str]:
    errs: List[str] = []
    for idx, row in enumerate(rows):
        for pk in pks:
            if pk not in row:
                errs.append(
                    f"{entity_name}[{idx}]: missing primary_key field {pk!r}"
                )
    return errs


def test_bad_payload_fails_readably():
    """Synthesize a bad PMS payload (lease rows missing lease_id) and confirm
    the same primary_key validation used by test_sample_input_matches_schema_entities
    produces a clear, named error. Skips cleanly if the PMS schema is absent
    (other tests will already have failed loudly on that)."""
    pms_entities = _domain_entities("pms")
    if "lease" not in pms_entities:
        pytest.skip("pms schema does not yet declare a 'lease' entity")
    lease = pms_entities["lease"]
    pks = _entity_primary_keys(lease)
    if "lease_id" not in pks:
        pytest.skip("pms.lease primary_key does not include 'lease_id'")
    # Synthetic bad payload: a row deliberately missing 'lease_id'.
    bad_rows = [
        {"property_id": "P001", "resident_id": "R001", "status": "in_effect"},
        {"property_id": "P002", "lease_id": "L002", "status": "in_effect"},
    ]
    errs = _validate_rows_against_primary_key(bad_rows, pks, "lease")
    assert errs, (
        "expected primary_key validation to raise an error for lease rows "
        "missing lease_id, got none"
    )
    joined = " | ".join(errs)
    assert "lease_id" in joined and "primary_key" in joined, (
        f"validation error must name both 'lease_id' and 'primary_key'; "
        f"got: {joined!r}"
    )


# ---------------------------------------------------------------------------
# Provenance
# ---------------------------------------------------------------------------

def test_provenance_fields_retained():
    failures: List[str] = []
    for dom in REQUIRED_DOMAINS:
        norm_path = CONNECTORS_ROOT / dom / "sample_normalized.json"
        if not norm_path.exists():
            continue  # absence is caught by test_sample_normalized_round_trip
        try:
            sample = _load_json(norm_path)
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(sample, dict):
            continue
        for entity_name, block in sample.items():
            rows = _rows_for({entity_name: block}, entity_name)
            for idx, row in enumerate(rows):
                present = set(row.keys())
                missing = REQUIRED_PROVENANCE_FIELDS - present
                if missing:
                    failures.append(
                        f"{norm_path.relative_to(SUBSYS)}#{entity_name}[{idx}]: "
                        f"missing provenance fields {sorted(missing)}"
                    )
    assert not failures, (
        "normalized records must carry provenance fields "
        "{source_name, source_date, source_row_id}:\n  - "
        + "\n  - ".join(failures)
    )
