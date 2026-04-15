"""Sage Intacct GL adapter: wave-5 completeness tests.

Checks the wave-5 content additions (dq_rules, reconciliation, crosswalk,
workflow_activation, runbooks, per-entity sample fixtures). The manifest-
conformance tests live in test_adapter.py; this file verifies the richer
content gaps filled in wave-5.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml


ADAPTER_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_yaml(name: str):
    with (ADAPTER_DIR / name).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_jsonl(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


# Canonical field sets, derived from _core/ontology.md. Only fields that
# must appear on the normalized record are listed.
CANONICAL_REQUIRED_FIELDS = {
    "ActualLine": {"account_id", "amount_cents", "posting_date", "period", "posting_side"},
    "BudgetLine": {"account_id", "amount_cents", "period", "scenario"},
    "ForecastLine": {"account_id", "amount_cents", "period", "forecast_version", "as_of_date"},
    "Vendor": {"vendor_id", "vendor_name"},
    "Project": {"source_project_id", "project_name", "project_type"},
}


CANONICAL_POSTING_SIDE = {"debit", "credit"}
CANONICAL_PUBLICATION_STATE = {"draft", "published", "approved", "retired"}
CANONICAL_PROJECT_TYPE = {"capex", "opex", "development", "reserve-funded", "reserve_funded"}


# ---------------------------------------------------------------------------
# File presence
# ---------------------------------------------------------------------------


def test_intacct_expected_files_present():
    """Every wave-5 file the adapter promises is on disk."""
    expected = [
        "manifest.yaml",
        "source_contract.yaml",
        "normalized_contract.yaml",
        "field_mapping.yaml",
        "source_registry_entry.yaml",
        "dq_rules.yaml",
        "reconciliation_rules.md",
        "reconciliation_checks.yaml",
        "edge_cases.md",
        "crosswalk_additions.yaml",
        "workflow_activation_additions.yaml",
        "runbooks/sage_intacct_onboarding.md",
        "runbooks/sage_intacct_common_issues.md",
        "README.md",
    ]
    for name in expected:
        assert (ADAPTER_DIR / name).exists(), f"missing expected file: {name}"


def test_intacct_expected_sample_raw_files_present():
    expected = {
        "chart_of_accounts.jsonl",
        "dimensions.jsonl",
        "journal_entries.jsonl",
        "actual_lines.jsonl",
        "budget_lines.jsonl",
        "forecast_lines.jsonl",
        "vendors.jsonl",
        "projects.jsonl",
    }
    sample_raw = ADAPTER_DIR / "sample_raw"
    actual = {p.name for p in sample_raw.iterdir() if p.is_file()}
    missing = expected - actual
    assert not missing, f"sample_raw missing: {missing}"


def test_intacct_expected_sample_normalized_files_present():
    expected = {
        "actual_lines.jsonl",
        "budget_lines.jsonl",
        "forecast_lines.jsonl",
        "vendors.jsonl",
        "projects.jsonl",
    }
    sample_normalized = ADAPTER_DIR / "sample_normalized"
    actual = {p.name for p in sample_normalized.iterdir() if p.is_file()}
    missing = expected - actual
    assert not missing, f"sample_normalized missing: {missing}"


# ---------------------------------------------------------------------------
# Sample raw: parse + fixture integrity
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "fname,min_count",
    [
        ("actual_lines.jsonl", 8),
        ("budget_lines.jsonl", 6),
        ("forecast_lines.jsonl", 6),
        ("vendors.jsonl", 5),
        ("projects.jsonl", 5),
    ],
)
def test_intacct_sample_raw_parses_and_count(fname, min_count):
    path = ADAPTER_DIR / "sample_raw" / fname
    rows = _load_jsonl(path)
    assert len(rows) >= min_count, (
        f"{fname}: expected at least {min_count} rows, got {len(rows)}"
    )
    for idx, row in enumerate(rows):
        assert row.get("status") == "sample", (
            f"{fname} row {idx} missing status: sample"
        )
        for pf in (
            "source_name",
            "source_type",
            "source_date",
            "extracted_at",
            "source_row_id",
        ):
            assert pf in row, f"{fname} row {idx} missing provenance field: {pf}"
        assert row["source_name"] == "sage_intacct_prod"
        assert row["source_type"] == "gl"


# ---------------------------------------------------------------------------
# Sample normalized: canonical field conformance
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "fname,expected_entity,min_count",
    [
        ("actual_lines.jsonl", "ActualLine", 8),
        ("budget_lines.jsonl", "BudgetLine", 6),
        ("forecast_lines.jsonl", "ForecastLine", 6),
        ("vendors.jsonl", "Vendor", 5),
        ("projects.jsonl", "Project", 5),
    ],
)
def test_intacct_sample_normalized_conforms(fname, expected_entity, min_count):
    path = ADAPTER_DIR / "sample_normalized" / fname
    rows = _load_jsonl(path)
    assert len(rows) >= min_count, (
        f"{fname}: expected at least {min_count} rows, got {len(rows)}"
    )

    raw_lines = [
        ln
        for ln in path.read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]
    for idx, raw in enumerate(raw_lines):
        assert '"status": "sample"' in raw, (
            f"{fname} line {idx} missing fixture tag '\"status\": \"sample\"'"
        )

    required_fields = CANONICAL_REQUIRED_FIELDS[expected_entity]
    for idx, row in enumerate(rows):
        missing = required_fields - set(row.keys())
        assert not missing, (
            f"{fname} row {idx} missing canonical required fields: {missing}"
        )


def test_intacct_actual_lines_posting_side_enum():
    rows = _load_jsonl(ADAPTER_DIR / "sample_normalized" / "actual_lines.jsonl")
    for idx, row in enumerate(rows):
        assert row["posting_side"] in CANONICAL_POSTING_SIDE, (
            f"actual_lines row {idx}: posting_side {row['posting_side']!r} invalid"
        )


def test_intacct_budget_lines_publication_state_enum():
    rows = _load_jsonl(ADAPTER_DIR / "sample_normalized" / "budget_lines.jsonl")
    for idx, row in enumerate(rows):
        assert row.get("publication_state") in CANONICAL_PUBLICATION_STATE, (
            f"budget_lines row {idx}: publication_state "
            f"{row.get('publication_state')!r} invalid"
        )


def test_intacct_projects_project_type_enum():
    rows = _load_jsonl(ADAPTER_DIR / "sample_normalized" / "projects.jsonl")
    for idx, row in enumerate(rows):
        pt = row.get("project_type")
        assert pt in CANONICAL_PROJECT_TYPE, (
            f"projects row {idx}: project_type {pt!r} invalid"
        )


# ---------------------------------------------------------------------------
# dq_rules.yaml shape
# ---------------------------------------------------------------------------


def test_intacct_dq_rules_shape():
    data = _load_yaml("dq_rules.yaml")
    assert "rules" in data, "dq_rules.yaml must carry a top-level 'rules' list"
    rules = data["rules"]
    assert isinstance(rules, list)
    assert len(rules) >= 18, f"expected at least 18 ic_ rules, got {len(rules)}"

    seen_ids = set()
    valid_dimensions = {
        "freshness",
        "completeness",
        "conformance",
        "uniqueness",
        "consistency",
    }
    valid_severities = {"blocker", "warning", "info"}
    required_fields = {
        "rule_id",
        "dimension",
        "severity",
        "description",
        "expected",
        "remediation",
    }

    for rule in rules:
        missing = required_fields - set(rule.keys())
        assert not missing, f"rule {rule.get('rule_id')} missing fields {missing}"
        rid = rule["rule_id"]
        assert rid.startswith("ic_"), f"rule_id {rid!r} must start with 'ic_'"
        assert rid not in seen_ids, f"duplicate rule_id {rid!r}"
        seen_ids.add(rid)
        assert rule["dimension"] in valid_dimensions, (
            f"rule {rid}: dimension {rule['dimension']!r} invalid"
        )
        assert rule["severity"] in valid_severities, (
            f"rule {rid}: severity {rule['severity']!r} invalid"
        )


def test_intacct_dq_rules_cover_required_dimensions():
    data = _load_yaml("dq_rules.yaml")
    dims = {r["dimension"] for r in data["rules"]}
    required = {
        "freshness",
        "completeness",
        "conformance",
        "uniqueness",
        "consistency",
    }
    missing = required - dims
    assert not missing, f"dq_rules.yaml missing dimensions: {missing}"


def test_intacct_dq_rules_cite_tolerance_band_not_hardcoded():
    """Any rule that names a band must reference the tolerance-band file,
    not hardcode a numeric threshold."""
    text = (ADAPTER_DIR / "dq_rules.yaml").read_text(encoding="utf-8")
    if "_band" in text:
        assert "reconciliation_tolerance_band.yaml" in text, (
            "dq_rules.yaml references bands; must cite "
            "reconciliation_tolerance_band.yaml"
        )


# ---------------------------------------------------------------------------
# reconciliation_checks.yaml shape
# ---------------------------------------------------------------------------


def test_intacct_reconciliation_checks_shape():
    data = _load_yaml("reconciliation_checks.yaml")
    assert "checks" in data, (
        "reconciliation_checks.yaml needs a top-level 'checks' list"
    )
    checks = data["checks"]
    assert isinstance(checks, list)
    assert len(checks) >= 12, f"expected at least 12 checks, got {len(checks)}"
    seen = set()
    for c in checks:
        cid = c.get("check_id", "")
        assert cid.startswith("ic_recon_"), (
            f"check_id {cid!r} must start with 'ic_recon_'"
        )
        assert cid not in seen, f"duplicate check_id {cid!r}"
        seen.add(cid)
        assert "sources" in c and isinstance(c["sources"], list)
        assert "sage_intacct_gl" in c["sources"], (
            f"check {cid!r} must include sage_intacct_gl in sources"
        )
        assert "tolerance_band" in c, f"check {cid!r} missing tolerance_band"
        assert "remediation_runbook" in c, (
            f"check {cid!r} missing remediation_runbook"
        )


def test_intacct_reconciliation_checks_cover_pairs():
    """The checks must reference every pair called out in the task brief:
    AppFolio, Procore, HR/Payroll, Manual, Dealpath."""
    data = _load_yaml("reconciliation_checks.yaml")
    all_sources = set()
    for c in data["checks"]:
        all_sources.update(c.get("sources", []))
    required = {
        "appfolio_pms",
        "procore_construction",
        "hr_payroll",
        "manual_sources_expanded",
        "dealpath_deal_pipeline",
    }
    missing = required - all_sources
    assert not missing, (
        f"reconciliation_checks.yaml missing pair source(s): {missing}"
    )


# ---------------------------------------------------------------------------
# crosswalk_additions.yaml shape
# ---------------------------------------------------------------------------


def test_intacct_crosswalk_additions_shape():
    data = _load_yaml("crosswalk_additions.yaml")
    assert data.get("status_tag") in {"stub", "template", "sample"}
    required_sections = {
        "account_crosswalk_additions",
        "vendor_master_crosswalk_additions",
        "property_master_crosswalk_additions",
        "capex_project_crosswalk_additions",
        "employee_crosswalk_additions",
    }
    missing = required_sections - set(data.keys())
    assert not missing, f"crosswalk_additions missing section(s): {missing}"

    for section in required_sections:
        rows = data[section]
        assert isinstance(rows, list) and rows, (
            f"{section}: must carry at least one row"
        )
        for row in rows:
            required_keys = {
                "intacct_id",
                "canonical_id",
                "effective_start",
                "survivorship_rule",
            }
            missing_keys = required_keys - set(row.keys())
            assert not missing_keys, (
                f"{section}: row missing keys {missing_keys}"
            )
            # match_confidence is the crosswalk.schema.yaml "confidence" field.
            assert (
                "match_confidence" in row or "confidence" in row
            ), f"{section}: row missing confidence"


# ---------------------------------------------------------------------------
# workflow_activation_additions.yaml shape
# ---------------------------------------------------------------------------


def test_intacct_workflow_activation_additions_shape():
    data = _load_yaml("workflow_activation_additions.yaml")
    assert "intacct_role" in data
    existing = data.get("activates_existing_workflows", []) or []
    by_name = {w["workflow"]: w for w in existing}
    expected_primary_workflows = {
        "monthly_property_operating_review",
        "reforecast",
        "budget_build",
        "executive_operating_summary_generation",
        "quarterly_portfolio_review",
    }
    missing = expected_primary_workflows - set(by_name.keys())
    assert not missing, (
        f"workflow_activation_additions missing workflows: {missing}"
    )
    # draw_package_review is allowed as contributing (not primary).
    assert "draw_package_review" in by_name

    # Every entry with a blocking_issues list must reference ic_* or ic_recon_ ids.
    for w in existing:
        blocks = w.get("blocking_issues") or []
        for b in blocks:
            assert b.startswith("ic_"), (
                f"workflow {w['workflow']}: blocking_issue {b!r} must be an "
                f"ic_* id"
            )
        # Each workflow entry must declare role, objects_supplied,
        # partial_mode_behavior, and human_approvals_required.
        for required in (
            "role",
            "objects_supplied",
            "partial_mode_behavior",
            "human_approvals_required",
        ):
            assert required in w, (
                f"workflow {w['workflow']}: missing field {required}"
            )


# ---------------------------------------------------------------------------
# Runbooks exist and are non-empty
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "runbook",
    [
        "runbooks/sage_intacct_onboarding.md",
        "runbooks/sage_intacct_common_issues.md",
    ],
)
def test_intacct_runbook_non_empty(runbook):
    path = ADAPTER_DIR / runbook
    text = path.read_text(encoding="utf-8").strip()
    assert len(text) > 500, (
        f"{runbook} appears too short to be a real runbook"
    )


# ---------------------------------------------------------------------------
# edge_cases.md presence + structure
# ---------------------------------------------------------------------------


def test_intacct_edge_cases_cover_required_scenarios():
    text = (ADAPTER_DIR / "edge_cases.md").read_text(encoding="utf-8").lower()
    section_matches = re.findall(r"^##\s+\d+\.", text, flags=re.MULTILINE)
    assert len(section_matches) >= 12, (
        f"edge_cases.md should document at least 12 cases; "
        f"found {len(section_matches)}"
    )
    required_keywords = [
        "late-arriving",
        "period reopen",
        "budget version unmapped",
        "multi-entity allocation",
        "placeholder",
        "appfolio before intacct",
        "payroll",
        "capex commitment",
        "intercompany",
        "reorg",
        "accrual reversal",
        "variance narrative absent",
        "consolidation",
    ]
    for kw in required_keywords:
        assert kw in text, f"edge_cases.md missing required keyword: {kw!r}"
