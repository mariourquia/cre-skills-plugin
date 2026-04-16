"""AppFolio PMS adapter: wave-5 completeness tests.

Checks the wave-5 content additions (dq_rules, reconciliation, crosswalk,
workflow_activation, runbooks, per-entity sample fixtures). The
manifest-conformance tests live in test_adapter.py; this file verifies
the richer content gaps filled in wave-5.
"""
from __future__ import annotations

import json
import re
import yaml
from pathlib import Path

import pytest


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
# must appear on the normalized record are listed; optional fields are
# tested via presence of at least one optional to confirm shape.
CANONICAL_REQUIRED_FIELDS = {
    "WorkOrder": {"work_order_id", "property_id", "reported_date", "priority", "status"},
    "Lead": {"lead_id", "property_id", "source_channel", "inquiry_date", "pipeline_stage"},
    "Application": {"application_id", "lead_id", "applied_date", "approval_status"},
    "Vendor": {"vendor_id", "vendor_name"},
    "TurnProject": {"turn_id", "property_id", "unit_id", "move_out_date", "status"},
}


CANONICAL_WORK_ORDER_PRIORITY = {"p1_safety", "p2_habitability", "p3_standard", "p4_cosmetic"}
CANONICAL_LEAD_PIPELINE_STAGES = {
    "inquiry",
    "contacted",
    "tour_scheduled",
    "toured",
    "applied",
    "approved",
    "leased",
    "lost",
}
CANONICAL_APP_STATUS = {
    "pending",
    "in_review",
    "approved",
    "approved_with_conditions",
    "declined",
    "withdrawn",
}
CANONICAL_TURN_STATUS = {"planned", "in_progress", "awaiting_parts", "punchlist", "ready", "leased"}


# ---------------------------------------------------------------------------
# File presence
# ---------------------------------------------------------------------------


def test_appfolio_expected_files_present():
    """Every wave-5 file the adapter promises is on disk."""
    expected = [
        "manifest.yaml",
        "source_contract.yaml",
        "normalized_contract.yaml",
        "field_mapping.yaml",
        "mapping_template.yaml",
        "source_registry_entry.yaml",
        "dq_rules.yaml",
        "reconciliation_rules.md",
        "reconciliation_checks.yaml",
        "edge_cases.md",
        "crosswalk_additions.yaml",
        "workflow_activation_additions.yaml",
        "runbooks/appfolio_onboarding.md",
        "runbooks/appfolio_common_issues.md",
        "README.md",
    ]
    for name in expected:
        assert (ADAPTER_DIR / name).exists(), f"missing expected file: {name}"


def test_appfolio_expected_sample_raw_files_present():
    expected = {
        "properties.jsonl",
        "units.jsonl",
        "leases.jsonl",
        "charges.jsonl",
        "payments.jsonl",
        "tenants.jsonl",
        "lease_events.jsonl",
        "work_orders.jsonl",
        "leads.jsonl",
        "applications.jsonl",
        "vendors.jsonl",
        "turns.jsonl",
    }
    sample_raw = ADAPTER_DIR / "sample_raw"
    actual = {p.name for p in sample_raw.iterdir() if p.is_file()}
    missing = expected - actual
    assert not missing, f"sample_raw missing: {missing}"


def test_appfolio_expected_sample_normalized_files_present():
    expected = {
        "work_orders.jsonl",
        "leads.jsonl",
        "applications.jsonl",
        "vendors.jsonl",
        "turns.jsonl",
    }
    sample_normalized = ADAPTER_DIR / "sample_normalized"
    actual = {p.name for p in sample_normalized.iterdir() if p.is_file()}
    missing = expected - actual
    assert not missing, f"sample_normalized missing: {missing}"


# ---------------------------------------------------------------------------
# Sample raw: parse + fixture integrity
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "fname,expected_count",
    [
        ("work_orders.jsonl", 5),
        ("leads.jsonl", 5),
        ("applications.jsonl", 5),
        ("vendors.jsonl", 5),
        ("turns.jsonl", 5),
    ],
)
def test_appfolio_sample_raw_parses_and_count(fname, expected_count):
    path = ADAPTER_DIR / "sample_raw" / fname
    rows = _load_jsonl(path)
    assert len(rows) == expected_count, f"{fname}: expected {expected_count} rows, got {len(rows)}"
    for idx, row in enumerate(rows):
        assert row.get("status") == "sample", f"{fname} row {idx} missing status: sample"
        for pf in ("source_name", "source_type", "source_date", "extracted_at", "source_row_id"):
            assert pf in row, f"{fname} row {idx} missing provenance field: {pf}"
        assert row["source_name"] == "appfolio_prod"
        assert row["source_type"] == "pms"


# ---------------------------------------------------------------------------
# Sample normalized: canonical field conformance
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "fname,expected_entity,expected_count",
    [
        ("work_orders.jsonl", "WorkOrder", 5),
        ("leads.jsonl", "Lead", 5),
        ("applications.jsonl", "Application", 5),
        ("vendors.jsonl", "Vendor", 5),
        ("turns.jsonl", "TurnProject", 5),
    ],
)
def test_appfolio_sample_normalized_conforms(fname, expected_entity, expected_count):
    """Normalized fixture rows conform to canonical field shape.

    Note on `status` key: canonical entities WorkOrder and TurnProject
    carry a `status` field per ontology. The fixture-tag convention uses
    `"status": "sample"` as the first key; JSON last-key-wins means the
    parsed record carries the canonical status. The raw JSONL is scanned
    for the fixture tag via a text check, while the canonical field
    content is asserted on the parsed record. Entities without a
    canonical `status` field are checked directly on the parsed dict.
    """
    path = ADAPTER_DIR / "sample_normalized" / fname
    rows = _load_jsonl(path)
    assert len(rows) == expected_count, f"{fname}: expected {expected_count} rows"

    raw_lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    for idx, raw in enumerate(raw_lines):
        assert '"status": "sample"' in raw, (
            f"{fname} line {idx} missing fixture tag '\"status\": \"sample\"'"
        )

    required_fields = CANONICAL_REQUIRED_FIELDS[expected_entity]
    for idx, row in enumerate(rows):
        assert row.get("entity") == expected_entity, (
            f"{fname} row {idx} entity mismatch: expected {expected_entity}, got {row.get('entity')}"
        )
        missing = required_fields - set(row.keys())
        assert not missing, f"{fname} row {idx} missing canonical required fields: {missing}"


def test_appfolio_work_orders_priority_enum():
    rows = _load_jsonl(ADAPTER_DIR / "sample_normalized" / "work_orders.jsonl")
    for idx, row in enumerate(rows):
        assert row["priority"] in CANONICAL_WORK_ORDER_PRIORITY, (
            f"work_orders row {idx}: priority {row['priority']!r} not in canonical enum"
        )


def test_appfolio_leads_pipeline_stage_enum():
    rows = _load_jsonl(ADAPTER_DIR / "sample_normalized" / "leads.jsonl")
    for idx, row in enumerate(rows):
        assert row["pipeline_stage"] in CANONICAL_LEAD_PIPELINE_STAGES, (
            f"leads row {idx}: pipeline_stage {row['pipeline_stage']!r} not in canonical enum"
        )


def test_appfolio_applications_status_enum():
    rows = _load_jsonl(ADAPTER_DIR / "sample_normalized" / "applications.jsonl")
    for idx, row in enumerate(rows):
        assert row["approval_status"] in CANONICAL_APP_STATUS, (
            f"applications row {idx}: approval_status {row['approval_status']!r} not in canonical enum"
        )


def test_appfolio_turns_status_enum():
    rows = _load_jsonl(ADAPTER_DIR / "sample_normalized" / "turns.jsonl")
    for idx, row in enumerate(rows):
        assert row["status"] in CANONICAL_TURN_STATUS, (
            f"turns row {idx}: status {row['status']!r} not in canonical enum"
        )


# ---------------------------------------------------------------------------
# dq_rules.yaml shape
# ---------------------------------------------------------------------------


def test_appfolio_dq_rules_shape():
    data = _load_yaml("dq_rules.yaml")
    assert "rules" in data, "dq_rules.yaml must carry a top-level 'rules' list"
    rules = data["rules"]
    assert isinstance(rules, list)
    assert len(rules) >= 18, f"expected at least 18 af_ rules, got {len(rules)}"

    seen_ids = set()
    valid_dimensions = {"freshness", "completeness", "conformance", "uniqueness", "consistency"}
    valid_severities = {"blocker", "warning", "info"}
    required_fields = {"rule_id", "dimension", "severity", "description", "expected", "remediation"}

    for rule in rules:
        missing = required_fields - set(rule.keys())
        assert not missing, f"rule {rule.get('rule_id')} missing fields {missing}"
        rid = rule["rule_id"]
        assert rid.startswith("af_"), f"rule_id {rid!r} must start with 'af_'"
        assert rid not in seen_ids, f"duplicate rule_id {rid!r}"
        seen_ids.add(rid)
        assert rule["dimension"] in valid_dimensions, (
            f"rule {rid}: dimension {rule['dimension']!r} invalid"
        )
        assert rule["severity"] in valid_severities, (
            f"rule {rid}: severity {rule['severity']!r} invalid"
        )


def test_appfolio_dq_rules_cover_required_dimensions():
    data = _load_yaml("dq_rules.yaml")
    dims = {r["dimension"] for r in data["rules"]}
    required = {"freshness", "completeness", "conformance", "uniqueness", "consistency"}
    missing = required - dims
    assert not missing, f"dq_rules.yaml missing dimensions: {missing}"


def test_appfolio_dq_rules_cite_tolerance_band_not_hardcoded():
    """Any rule that names a band must reference the tolerance-band file,
    not hardcode a numeric threshold."""
    text = (ADAPTER_DIR / "dq_rules.yaml").read_text(encoding="utf-8")
    # Rules that mention _band must cite the schema file to avoid hardcoding.
    if "_band" in text:
        assert "reconciliation_tolerance_band.yaml" in text, (
            "dq_rules.yaml references bands; must cite reconciliation_tolerance_band.yaml"
        )


# ---------------------------------------------------------------------------
# reconciliation_checks.yaml shape
# ---------------------------------------------------------------------------


def test_appfolio_reconciliation_checks_shape():
    data = _load_yaml("reconciliation_checks.yaml")
    assert "checks" in data, "reconciliation_checks.yaml needs a top-level 'checks' list"
    checks = data["checks"]
    assert isinstance(checks, list)
    assert len(checks) >= 8, f"expected at least 8 checks, got {len(checks)}"
    seen = set()
    for c in checks:
        cid = c.get("check_id", "")
        assert cid.startswith("af_recon_"), f"check_id {cid!r} must start with 'af_recon_'"
        assert cid not in seen, f"duplicate check_id {cid!r}"
        seen.add(cid)
        assert "sources" in c and isinstance(c["sources"], list)
        assert "appfolio_prod" in c["sources"], f"check {cid!r} must include appfolio_prod"
        assert "tolerance_ref" in c, f"check {cid!r} missing tolerance_ref"
        assert c["severity"] in {"blocker", "warning", "info"}
        assert "remediation_runbook" in c


# ---------------------------------------------------------------------------
# crosswalk_additions.yaml shape
# ---------------------------------------------------------------------------


def test_appfolio_crosswalk_additions_shape():
    data = _load_yaml("crosswalk_additions.yaml")
    assert data.get("status_tag") in {"stub", "template", "sample"}
    dest = data.get("destination_crosswalks")
    assert isinstance(dest, dict) and dest
    expected = {
        "property_master_crosswalk",
        "unit_crosswalk",
        "lease_crosswalk",
        "resident_account_crosswalk",
        "vendor_master_crosswalk",
    }
    missing = expected - set(dest.keys())
    assert not missing, f"crosswalk_additions missing destination(s): {missing}"
    for name, fragment in dest.items():
        assert "file" in fragment, f"{name}: missing file target"
        assert "survivorship_rule" in fragment, f"{name}: missing survivorship_rule"
        assert isinstance(fragment.get("rows"), list) and fragment["rows"], (
            f"{name}: must carry at least one row"
        )
        for row in fragment["rows"]:
            required_keys = {
                "canonical_id",
                "appfolio_id",
                "effective_start",
                "survivorship_rule",
                "confidence",
                "source_of_record_per_attribute",
            }
            assert required_keys.issubset(row.keys()), (
                f"{name}: row missing keys {required_keys - set(row.keys())}"
            )


# ---------------------------------------------------------------------------
# workflow_activation_additions.yaml shape
# ---------------------------------------------------------------------------


def test_appfolio_workflow_activation_additions_shape():
    data = _load_yaml("workflow_activation_additions.yaml")
    assert "appfolio_role" in data
    primary_workflows = {
        w["workflow"]
        for w in (data.get("activates_existing_workflows", []) + data.get("proposes_new_workflows", []))
        if w.get("role") == "primary"
    }
    expected_primary = {
        "monthly_property_operating_review",
        "lead_to_lease_funnel_review",
        "delinquency_collections",
        "work_order_triage",
        "vendor_dispatch_sla_review",
        "unit_turn_make_ready",
        "move_in_administration",
        "move_out_administration",
        "renewal_retention",
        "third_party_manager_scorecard_review",
    }
    missing = expected_primary - primary_workflows
    assert not missing, f"workflow_activation_additions missing primary workflows: {missing}"
    # Every entry with a blocking_issues list must reference af_* ids.
    for group_key in ("activates_existing_workflows", "proposes_new_workflows"):
        for w in data.get(group_key, []):
            blocks = w.get("blocking_issues")
            if blocks:
                for b in blocks:
                    assert b.startswith("af_"), (
                        f"workflow {w['workflow']}: blocking_issue {b!r} must be an af_* id"
                    )


# ---------------------------------------------------------------------------
# Runbooks exist and are non-empty
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "runbook",
    ["runbooks/appfolio_onboarding.md", "runbooks/appfolio_common_issues.md"],
)
def test_appfolio_runbook_non_empty(runbook):
    path = ADAPTER_DIR / runbook
    text = path.read_text(encoding="utf-8").strip()
    assert len(text) > 500, f"{runbook} appears too short to be a real runbook"


# ---------------------------------------------------------------------------
# edge_cases.md presence + structure
# ---------------------------------------------------------------------------


def test_appfolio_edge_cases_cover_required_scenarios():
    text = (ADAPTER_DIR / "edge_cases.md").read_text(encoding="utf-8").lower()
    # Number of H2 sections is a proxy for case count.
    section_matches = re.findall(r"^##\s+\d+\.", text, flags=re.MULTILINE)
    assert len(section_matches) >= 12, (
        f"edge_cases.md should document at least 12 cases; found {len(section_matches)}"
    )
    required_keywords = [
        "renumber",
        "wrong unit",
        "mid-month rent",
        "concession",
        "proration",
        "transferred resident",
        "expired insurance",
        "different market",
        "legal entity",
        "blank email",
        "out-of-service",
        "bulk renewal",
    ]
    for kw in required_keywords:
        assert kw in text, f"edge_cases.md missing required keyword: {kw!r}"
