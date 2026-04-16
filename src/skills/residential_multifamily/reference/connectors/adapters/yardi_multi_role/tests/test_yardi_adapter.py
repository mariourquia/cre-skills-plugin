"""Yardi multi-role adapter: manifest and integration conformance tests."""
import json
import yaml
from pathlib import Path
import pytest

ADAPTER_DIR = Path(__file__).resolve().parent.parent


def _load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_jsonl(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            rows.append(json.loads(line))
    return rows


def test_manifest_loads_and_has_required_fields():
    manifest = _load_yaml(ADAPTER_DIR / "manifest.yaml")
    assert manifest["adapter_id"] == "yardi_multi_role"
    assert manifest["vendor_family"] == "yardi_family"
    assert manifest["connector_domain"] == "pms"
    assert manifest["status"] == "stub"
    assert manifest["rollout_wave"] == "wave_2"
    assert len(manifest["supported_source_systems"]) >= 1
    assert len(manifest["mapping_hints"]) >= 1
    assert len(manifest["known_gotchas"]) >= 1
    assert "author_metadata" in manifest
    assert "last_updated" in manifest


def test_manifest_conforms_to_adapter_schema():
    schema_path = ADAPTER_DIR.parent / "adapter_manifest.schema.yaml"
    assert schema_path.exists(), f"Schema missing: {schema_path}"
    schema = _load_yaml(schema_path)
    manifest = _load_yaml(ADAPTER_DIR / "manifest.yaml")
    # minimal check: every required field in schema is present in manifest
    for required in schema.get("required", []):
        assert required in manifest, f"manifest missing required field: {required}"


def test_adapter_id_matches_directory_name():
    manifest = _load_yaml(ADAPTER_DIR / "manifest.yaml")
    assert manifest["adapter_id"] == ADAPTER_DIR.name


def test_required_files_present():
    required = [
        "manifest.yaml",
        "classification_worksheet.md",
        "bounded_assumptions.yaml",
        "provisional_source_contract.yaml",
        "source_contract.yaml",
        "normalized_contract.yaml",
        "field_mapping.yaml",
        "dq_rules.yaml",
        "reconciliation_rules.md",
        "reconciliation_checks.yaml",
        "edge_cases.md",
        "crosswalk_additions.yaml",
        "workflow_activation_additions.yaml",
        "README.md",
        "__init__.py",
    ]
    for name in required:
        assert (ADAPTER_DIR / name).exists(), f"missing required file: {name}"


def test_required_runbooks_present():
    runbooks = ADAPTER_DIR / "runbooks"
    assert runbooks.exists() and runbooks.is_dir()
    for name in [
        "yardi_classification_path.md",
        "yardi_onboarding.md",
        "yardi_common_issues.md",
        "yardi_migration_to_appfolio.md",
    ]:
        assert (runbooks / name).exists(), f"missing runbook: {name}"


def test_sample_raw_files_parse():
    raw = ADAPTER_DIR / "sample_raw"
    assert raw.exists() and raw.is_dir()
    expected = {
        "properties.jsonl",
        "units.jsonl",
        "leases.jsonl",
        "lease_events.jsonl",
        "charges.jsonl",
        "payments.jsonl",
        "work_orders.jsonl",
        "vendors.jsonl",
        "leads.jsonl",
        "applications.jsonl",
        "gl_actuals.jsonl",
    }
    actual = {p.name for p in raw.iterdir() if p.is_file()}
    missing = expected - actual
    assert not missing, f"sample_raw missing: {missing}"
    for name in expected:
        rows = _load_jsonl(raw / name)
        assert len(rows) >= 3, f"{name} must have at least 3 records"
        for row in rows:
            assert row.get("status") in ("sample", "stub", "template"), (
                f"{name}: row missing sample/stub/template status tag"
            )


def test_sample_normalized_files_parse():
    norm = ADAPTER_DIR / "sample_normalized"
    assert norm.exists() and norm.is_dir()
    expected = {
        "properties.jsonl",
        "units.jsonl",
        "leases.jsonl",
        "lease_events.jsonl",
        "charges.jsonl",
        "payments.jsonl",
        "work_orders.jsonl",
        "vendors.jsonl",
        "leads.jsonl",
        "applications.jsonl",
        "gl_actuals.jsonl",
    }
    actual = {p.name for p in norm.iterdir() if p.is_file()}
    missing = expected - actual
    assert not missing, f"sample_normalized missing: {missing}"
    for name in expected:
        rows = _load_jsonl(norm / name)
        assert len(rows) >= 3, f"normalized {name} must have at least 3 records"
        for row in rows:
            assert row.get("status") in ("sample", "stub", "template"), (
                f"normalized {name}: row missing status tag"
            )


def test_sample_raw_and_normalized_counts_match():
    raw = ADAPTER_DIR / "sample_raw"
    norm = ADAPTER_DIR / "sample_normalized"
    for name in [
        "properties.jsonl",
        "units.jsonl",
        "leases.jsonl",
        "lease_events.jsonl",
        "charges.jsonl",
        "payments.jsonl",
        "work_orders.jsonl",
        "vendors.jsonl",
        "leads.jsonl",
        "applications.jsonl",
        "gl_actuals.jsonl",
    ]:
        raw_rows = _load_jsonl(raw / name)
        norm_rows = _load_jsonl(norm / name)
        assert len(raw_rows) == len(norm_rows), (
            f"{name}: raw/normalized record count mismatch "
            f"({len(raw_rows)} vs {len(norm_rows)})"
        )


def test_dq_rules_format_valid():
    dq = _load_yaml(ADAPTER_DIR / "dq_rules.yaml")
    assert "rules" in dq
    rules = dq["rules"]
    assert len(rules) >= 18, f"expected at least 18 DQ rules, got {len(rules)}"
    for rule in rules:
        assert "rule_id" in rule
        assert rule["rule_id"].startswith("yd_"), (
            f"rule_id must start with yd_: {rule['rule_id']}"
        )
        assert "dimension" in rule
        assert "severity" in rule
        assert rule["severity"] in ("blocker", "warning", "info")
        assert "description" in rule


def test_classification_worksheet_present_and_has_dimensions():
    worksheet = (ADAPTER_DIR / "classification_worksheet.md").read_text()
    for dimension in [
        "Dimension 1: Role",
        "Dimension 2: Access Path",
        "Dimension 3: Operating Pattern",
        "Dimension 4: Data Sensitivity",
    ]:
        assert dimension in worksheet, (
            f"classification_worksheet.md missing section: {dimension}"
        )


def test_bounded_assumptions_structure():
    ba = _load_yaml(ADAPTER_DIR / "bounded_assumptions.yaml")
    assert "assumptions" in ba
    for assumption in ba["assumptions"]:
        assert "id" in assumption
        assert "assumption" in assumption
        assert "lifts_when" in assumption
        assert "default_behavior_until_lifted" in assumption


def test_reconciliation_checks_format():
    rc = _load_yaml(ADAPTER_DIR / "reconciliation_checks.yaml")
    assert "checks" in rc
    for check in rc["checks"]:
        assert "check_id" in check
        assert check["check_id"].startswith("yd_recon_"), (
            f"check_id must start with yd_recon_: {check['check_id']}"
        )
        assert "paired_sources" in check
        assert "grain" in check
        assert "tolerance_reference" in check
        assert "reconciliation_tolerance_band.yaml" in check["tolerance_reference"], (
            f"check {check['check_id']} must cite reconciliation_tolerance_band.yaml"
        )
        assert "severity" in check
        assert "remediation_runbook" in check


def test_provisional_source_contract_flags_classification():
    psc = _load_yaml(ADAPTER_DIR / "provisional_source_contract.yaml")
    assert psc.get("classification_status") == "pending"
    assert "entities" in psc
    for entity_name, entity in psc["entities"].items():
        assert entity.get("requires_classification") is True, (
            f"provisional entity {entity_name} must have requires_classification: true"
        )


def test_crosswalk_additions_have_effective_dating():
    cw = _load_yaml(ADAPTER_DIR / "crosswalk_additions.yaml")
    # check every crosswalk top-level key has additions with effective_start and survivorship_rule
    for cw_name, payload in cw.items():
        if cw_name == "status_tag":
            continue
        if not isinstance(payload, dict) or "additions" not in payload:
            continue
        for row in payload["additions"]:
            assert "effective_start" in row, (
                f"{cw_name} addition missing effective_start: {row}"
            )
            assert "survivorship_rule" in row, (
                f"{cw_name} addition missing survivorship_rule: {row}"
            )


def test_workflow_activation_has_role_by_classification():
    wf = _load_yaml(ADAPTER_DIR / "workflow_activation_additions.yaml")
    assert "yardi_role_by_classification" in wf
    assert "proposes_new_workflows" in wf
    # every proposed workflow must declare role_by_classification
    for proposed in wf["proposes_new_workflows"]:
        assert "workflow" in proposed
        assert "role_by_classification" in proposed
        assert "minimum_viable_data_set" in proposed
        assert "blockers" in proposed
        assert "fallback_mode" in proposed
