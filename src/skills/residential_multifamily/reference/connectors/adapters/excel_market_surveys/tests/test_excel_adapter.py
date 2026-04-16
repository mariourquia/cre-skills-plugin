"""Excel market surveys adapter: wave-5 conformance tests.

Covers:
  - manifest.yaml conforms to adapter_manifest.schema.yaml
  - every template_schema YAML parses and carries expected keys
  - sample_valid CSV files carry required headers per their template schema
  - sample_invalid CSV files would fail at least one dq rule / conformance check
  - dq_rules.yaml format valid (prefix ex_, required fields present)
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml


ADAPTER_DIR = Path(__file__).resolve().parents[1]
ADAPTERS_ROOT = ADAPTER_DIR.parent
if str(ADAPTERS_ROOT) not in sys.path:
    sys.path.insert(0, str(ADAPTERS_ROOT))

from _test_helpers import _load_yaml, _validate  # noqa: E402


# ---- manifest ----------------------------------------------------------------


def test_manifest_conforms(adapter_manifest_schema):
    manifest_path = ADAPTER_DIR / "manifest.yaml"
    assert manifest_path.exists(), f"missing manifest.yaml in {ADAPTER_DIR}"
    manifest = _load_yaml(manifest_path)
    errors = _validate(manifest, adapter_manifest_schema)
    assert not errors, f"excel_market_surveys manifest failed schema: {errors}"
    assert manifest["adapter_id"] == "excel_market_surveys"
    assert manifest["vendor_family"] == "excel_benchmark_family"
    assert manifest["connector_domain"] == "market_data"
    assert manifest["status"] == "stub"
    assert manifest["rollout_wave"] == "wave_4"


# ---- template schemas --------------------------------------------------------


_TEMPLATE_SCHEMAS_DIR = ADAPTER_DIR / "template_schemas"
_WAVE5_NEW_SCHEMAS = [
    "vendor_rate_card.yaml",
    "turn_cost_library.yaml",
    "capex_cost_library.yaml",
    "schedule_assumption.yaml",
    "market_commentary.yaml",
]


def test_every_template_schema_parses():
    yaml_files = sorted(_TEMPLATE_SCHEMAS_DIR.glob("*.yaml"))
    assert len(yaml_files) >= 5, f"expected at least 5 template schemas, got {len(yaml_files)}"
    for yf in yaml_files:
        data = yaml.safe_load(yf.read_text())
        assert isinstance(data, dict), f"{yf.name} did not parse to dict"
        assert data.get("status_tag") in {"template", "stub", "sample"}, (
            f"{yf.name} missing status_tag"
        )
        assert "template_slug" in data, f"{yf.name} missing template_slug"


def test_wave5_template_schemas_present():
    for name in _WAVE5_NEW_SCHEMAS:
        p = _TEMPLATE_SCHEMAS_DIR / name
        assert p.exists(), f"missing wave-5 template schema: {name}"


def _collect_columns(schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return the flat list of column dicts from either columns or sheet_schemas."""
    if "columns" in schema:
        return list(schema["columns"])
    out: List[Dict[str, Any]] = []
    for _sheet, sheet_body in (schema.get("sheet_schemas") or {}).items():
        out.extend(sheet_body.get("columns", []))
    return out


# ---- sample_valid ------------------------------------------------------------


_SAMPLE_VALID_TO_SCHEMA = {
    "vendor_rate_card_q1_2026.csv": "vendor_rate_card.yaml",
    "turn_cost_library_q1_2026.csv": "turn_cost_library.yaml",
    "capex_cost_library_q1_2026.csv": "capex_cost_library.yaml",
    "schedule_assumption_q1_2026.csv": "schedule_assumption.yaml",
    "market_commentary_q1_2026.csv": "market_commentary.yaml",
}


def _read_csv_headers(path: Path) -> List[str]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            return next(reader)
        except StopIteration:
            return []


def _required_headers_for_schema(schema: Dict[str, Any]) -> List[str]:
    required: List[str] = []
    for col in _collect_columns(schema):
        if col.get("required") is True:
            required.append(col["name"])
    return required


def test_sample_valid_headers_match_schema():
    sv_dir = ADAPTER_DIR / "sample_valid"
    assert sv_dir.exists()
    for csv_name, schema_name in _SAMPLE_VALID_TO_SCHEMA.items():
        csv_path = sv_dir / csv_name
        schema_path = _TEMPLATE_SCHEMAS_DIR / schema_name
        assert csv_path.exists(), f"missing sample_valid file: {csv_name}"
        assert schema_path.exists(), f"missing template schema: {schema_name}"
        schema = yaml.safe_load(schema_path.read_text())
        observed = set(_read_csv_headers(csv_path))
        required = set(_required_headers_for_schema(schema))
        # Each sample_valid drop exercises a primary sheet; required columns
        # for that sheet must all appear as observed headers. Cover metadata
        # sheet columns (quarterly artifacts) are not in the CSV sibling.
        # Accept the sample when every required column for the primary
        # lines sheet is present.
        primary_sheet_required = _primary_sheet_required(schema)
        missing = primary_sheet_required - observed
        assert not missing, (
            f"{csv_name} missing required headers from primary sheet "
            f"of {schema_name}: {sorted(missing)}"
        )


def _primary_sheet_required(schema: Dict[str, Any]) -> set:
    """Return required columns of the first non-cover_metadata sheet, or the
    top-level columns list."""
    if "columns" in schema:
        return {c["name"] for c in schema["columns"] if c.get("required")}
    sheets = schema.get("sheet_schemas") or {}
    for sheet, body in sheets.items():
        if sheet == "cover_metadata":
            continue
        return {c["name"] for c in body.get("columns", []) if c.get("required")}
    return set()


# ---- sample_invalid ---------------------------------------------------------


def test_sample_invalid_files_violate_rules():
    si_dir = ADAPTER_DIR / "sample_invalid"
    assert si_dir.exists()

    # missing_as_of: vendor rate card rows with empty as_of
    missing = si_dir / "missing_as_of.csv"
    assert missing.exists()
    with missing.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert rows, "missing_as_of.csv must have data rows"
    as_of_values = {r["as_of"] for r in rows}
    assert as_of_values == {""}, (
        "missing_as_of.csv must have every as_of blank (rule ex_completeness_as_of_present)"
    )

    # stale_export_q3_2024: capex rows with 2024-09-30 as_of
    stale = si_dir / "stale_export_q3_2024.csv"
    assert stale.exists()
    with stale.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert rows
    for r in rows:
        assert r["as_of"].startswith("2024"), (
            "stale_export_q3_2024.csv rows must land in 2024 to trigger freshness rule"
        )

    # header_drift: renamed headers vs turn_cost_library template
    drift = si_dir / "header_drift.csv"
    assert drift.exists()
    observed = set(_read_csv_headers(drift))
    turn_cost_schema = yaml.safe_load(
        (_TEMPLATE_SCHEMAS_DIR / "turn_cost_library.yaml").read_text()
    )
    required = _primary_sheet_required(turn_cost_schema)
    # header_drift must NOT contain the required turn_cost_library columns
    intersection = observed & required
    assert not intersection, (
        f"header_drift.csv must not satisfy turn_cost_library required headers; "
        f"found overlap: {intersection}"
    )


# ---- dq_rules --------------------------------------------------------------


def test_dq_rules_format_valid():
    dq_path = ADAPTER_DIR / "dq_rules.yaml"
    assert dq_path.exists()
    data = yaml.safe_load(dq_path.read_text())
    assert isinstance(data, dict) and "rules" in data
    rules = data["rules"]
    assert isinstance(rules, list)
    assert len(rules) >= 16, f"expected >= 16 dq rules, got {len(rules)}"
    seen_ids: set = set()
    allowed_severity = {"blocker", "warning", "info"}
    for r in rules:
        assert isinstance(r, dict), "each rule must be a dict"
        for key in ("rule_id", "dimension", "severity", "description"):
            assert key in r, f"rule missing {key}: {r}"
        rid = r["rule_id"]
        assert rid.startswith("ex_"), f"rule_id must start with ex_: {rid}"
        assert rid not in seen_ids, f"duplicate rule_id: {rid}"
        seen_ids.add(rid)
        assert r["severity"] in allowed_severity, (
            f"rule {rid} severity {r['severity']!r} not in {allowed_severity}"
        )


# ---- reconciliation checks + workflow fragment -----------------------------


def test_reconciliation_checks_format_valid():
    rc_path = ADAPTER_DIR / "reconciliation_checks.yaml"
    assert rc_path.exists()
    data = yaml.safe_load(rc_path.read_text())
    assert "checks" in data
    checks = data["checks"]
    assert len(checks) >= 10, f"expected >= 10 reconciliation checks, got {len(checks)}"
    for c in checks:
        assert c["check_id"].startswith("ex_recon_"), (
            f"check_id must start with ex_recon_: {c['check_id']}"
        )
        assert "tolerance_band_ref" in c
        assert "reconciliation_tolerance_band.yaml" in c["tolerance_band_ref"]


def test_workflow_activation_additions_valid():
    wa_path = ADAPTER_DIR / "workflow_activation_additions.yaml"
    assert wa_path.exists()
    data = yaml.safe_load(wa_path.read_text())
    assert "workflows" in data
    required_fields = {
        "workflow",
        "role",
        "objects_supplied",
        "blocking_issues",
        "partial_mode_behavior",
        "human_approvals_required",
    }
    for wf in data["workflows"]:
        missing = required_fields - set(wf.keys())
        assert not missing, f"workflow {wf.get('workflow')} missing {missing}"


# ---- normalized_contract and field_mapping ---------------------------------


def test_normalized_contract_loads():
    nc = ADAPTER_DIR / "normalized_contract.yaml"
    assert nc.exists()
    data = yaml.safe_load(nc.read_text())
    assert "mappings" in data
    expected_objects = {
        "rent_comp",
        "market_rent_benchmark",
        "concession_benchmark",
        "occupancy_benchmark",
        "labor_rate_reference",
        "material_cost_reference",
        "turn_cost_reference",
        "vendor_rate",
        "market_commentary",
        "schedule_assumption",
        "capex_cost_reference",
    }
    observed = set(data["mappings"].keys())
    missing = expected_objects - observed
    assert not missing, f"normalized_contract missing object shapes: {missing}"
    for name, body in data["mappings"].items():
        assert body.get("as_of_required") is True, (
            f"normalized_contract mapping {name} must set as_of_required: true"
        )


def test_field_mapping_loads():
    fm = ADAPTER_DIR / "field_mapping.yaml"
    assert fm.exists()
    data = yaml.safe_load(fm.read_text())
    assert "template_schemas" in data
    for tpl_name, tpl_body in data["template_schemas"].items():
        for row in tpl_body["mappings"]:
            assert "transform_hint" in row, (
                f"{tpl_name} mapping row missing transform_hint: {row}"
            )
            assert "as_of_required" in row, (
                f"{tpl_name} mapping row missing as_of_required: {row}"
            )


# ---- runbooks --------------------------------------------------------------


def test_runbooks_present():
    rb = ADAPTER_DIR / "runbooks"
    for name in ("excel_onboarding.md", "excel_common_issues.md"):
        assert (rb / name).exists(), f"missing runbook: {name}"


# ---- crosswalk_additions ---------------------------------------------------


def test_crosswalk_additions_loads():
    cw = ADAPTER_DIR / "crosswalk_additions.yaml"
    assert cw.exists()
    data = yaml.safe_load(cw.read_text())
    for key in (
        "market_crosswalk",
        "submarket_crosswalk",
        "vendor_master_crosswalk",
        "cost_code_crosswalk",
    ):
        assert key in data, f"crosswalk_additions missing {key}"


# ---- purpose comments ------------------------------------------------------


def test_every_yaml_leads_with_purpose_comment():
    # Every new adapter-authored YAML file must lead with a '#' purpose comment
    new_files = [
        ADAPTER_DIR / "normalized_contract.yaml",
        ADAPTER_DIR / "field_mapping.yaml",
        ADAPTER_DIR / "dq_rules.yaml",
        ADAPTER_DIR / "reconciliation_checks.yaml",
        ADAPTER_DIR / "crosswalk_additions.yaml",
        ADAPTER_DIR / "workflow_activation_additions.yaml",
    ]
    for p in new_files:
        assert p.exists(), f"missing {p.name}"
        first_line = p.read_text().splitlines()[0].strip()
        assert first_line.startswith("#"), (
            f"{p.name} must lead with a '#' purpose comment, got: {first_line!r}"
        )
