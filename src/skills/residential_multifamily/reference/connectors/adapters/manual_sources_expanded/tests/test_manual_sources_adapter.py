"""Manual Sources Expanded adapter: conformance and fill tests.

Covers:
  - manifest conforms to adapter_manifest.schema.yaml
  - required wave-5 files present
  - file_family_registry.yaml parses and every entry has required keys
  - normalized_contract.yaml parses and covers every family
  - every sample CSV has the expected header row and at least 3 data rows
  - dq_rules.yaml and reconciliation_checks.yaml parse and carry ms_ prefix
  - crosswalk_additions.yaml parses and fragments conform to crosswalk schema shape

Conformance note: the shared run_adapter_manifest_checks() helper in
../../_test_helpers.py additionally asserts the presence of
example_raw_payload.jsonl, normalized_output_example.jsonl, and
mapping_template.yaml. Those artifacts are scoped to row-level vendor
adapters (appfolio_pms, sage_intacct_gl, etc.), not to the
file-family-based manual_sources_expanded adapter. We therefore validate
the manifest directly against adapter_manifest.schema.yaml rather than
routing through the helper, matching the same posture as
excel_market_surveys (a sibling file-family adapter).
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml


ADAPTER_DIR = Path(__file__).resolve().parents[1]
ADAPTERS_ROOT = ADAPTER_DIR.parent
if str(ADAPTERS_ROOT) not in sys.path:
    sys.path.insert(0, str(ADAPTERS_ROOT))

from _test_helpers import _validate  # noqa: E402


SAMPLE_FILE_HEADERS = {
    "tpm_submission_monthly_report_2026_03.csv": [
        "property_code",
        "period",
        "occupancy_physical",
        "occupancy_economic",
        "collections_rate",
        "delinquency_balance",
        "narrative_summary",
        "submitted_by",
        "submitted_date",
        "signed_off",
    ],
    "operator_variance_narrative_2026_03.csv": [
        "property_code",
        "period",
        "account",
        "budget",
        "actual",
        "variance_amount",
        "variance_pct",
        "driver_category",
        "narrative",
        "author",
        "reviewed_by",
    ],
    "bid_tab_construction_2026_03.csv": [
        "project",
        "scope",
        "bidder",
        "base_bid",
        "alt_1",
        "alt_2",
        "qualifications",
        "exclusions",
        "leveling_notes",
        "recommended_award",
        "recommendation_rationale",
        "approver_required",
    ],
    "approval_matrix_threshold_set_2026_03.csv": [
        "action_type",
        "tier_1_threshold",
        "tier_2_threshold",
        "tier_3_threshold",
        "tier_1_approver",
        "tier_2_approver",
        "tier_3_approver",
        "effective_start",
        "effective_end",
        "change_log_ref",
    ],
    "escalation_log_2026_03.csv": [
        "event_id",
        "source_pack",
        "kind",
        "severity",
        "opened_at",
        "routed_to",
        "status",
    ],
    "operator_payroll_summary_2026_03.csv": [
        "property_code",
        "period",
        "role_slug",
        "headcount_fte",
        "gross_wages",
        "benefits_burden",
        "payroll_taxes",
        "total_labor_cost",
        "prepared_by",
    ],
    "manual_property_correction_2026_03.csv": [
        "object_type",
        "object_id",
        "field_changed",
        "prior_value",
        "new_value",
        "rationale",
        "requested_by",
        "approver",
        "approved_date",
    ],
}


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_manual_sources_manifest_conforms(adapter_manifest_schema):
    """manifest.yaml validates against adapter_manifest.schema.yaml."""
    manifest = _load_yaml(ADAPTER_DIR / "manifest.yaml")
    errors: List[str] = _validate(manifest, adapter_manifest_schema)
    assert not errors, f"manifest schema errors: {errors}"
    assert manifest["adapter_id"] == ADAPTER_DIR.name
    assert manifest["connector_domain"] == "manual_uploads"
    assert manifest["vendor_family"] == "manual_file_family"
    assert manifest["status"] == "stub"


def test_manual_sources_required_files_present():
    required = [
        "manifest.yaml",
        "README.md",
        "dq_rules.yaml",
        "source_registry_entry.yaml",
        "workflow_activation_additions.yaml",
        "file_family_registry.yaml",
        "normalized_contract.yaml",
        "reconciliation_rules.md",
        "reconciliation_checks.yaml",
        "edge_cases.md",
        "crosswalk_additions.yaml",
        "runbooks/manual_sources_onboarding.md",
        "runbooks/manual_common_issues.md",
    ]
    for name in required:
        assert (ADAPTER_DIR / name).exists(), f"missing required file: {name}"


def test_file_family_registry_valid():
    data = _load_yaml(ADAPTER_DIR / "file_family_registry.yaml")
    assert isinstance(data, dict)
    assert data.get("status_tag") in {"template", "sample", "stub"}
    families = data.get("file_families")
    assert isinstance(families, list) and len(families) >= 10, (
        "expected at least 10 file families"
    )

    required_keys = {
        "family_id",
        "family_name",
        "expected_format",
        "expected_headers",
        "delivery_channel",
        "cadence",
        "provenance_required",
        "staleness_threshold_days",
        "target_canonical_object",
    }
    valid_formats = {"xlsx", "csv", "pdf", "email_table"}
    valid_channels = {"sftp", "shared_drive", "email", "portal"}
    valid_cadences = {
        "monthly",
        "quarterly",
        "event_driven",
        "ad_hoc",
        "weekly",
        "annual",
    }
    seen_ids = set()
    for fam in families:
        assert isinstance(fam, dict)
        missing = required_keys - fam.keys()
        assert not missing, f"family {fam.get('family_id')} missing keys: {missing}"
        assert fam["family_id"] not in seen_ids, (
            f"duplicate family_id: {fam['family_id']}"
        )
        seen_ids.add(fam["family_id"])
        assert fam["expected_format"] in valid_formats
        assert fam["delivery_channel"] in valid_channels
        assert fam["cadence"] in valid_cadences
        assert isinstance(fam["expected_headers"], list) and fam["expected_headers"]
        assert (
            isinstance(fam["provenance_required"], list)
            and fam["provenance_required"]
        )
        assert isinstance(fam["staleness_threshold_days"], int)
        assert fam["staleness_threshold_days"] > 0


def test_normalized_contract_parses_and_covers_families():
    registry = _load_yaml(ADAPTER_DIR / "file_family_registry.yaml")
    contract = _load_yaml(ADAPTER_DIR / "normalized_contract.yaml")
    assert isinstance(contract, dict)
    assert contract.get("status_tag") in {"template", "sample", "stub"}
    mappings: Dict[str, Any] = contract.get("mappings", {})
    family_ids = {f["family_id"] for f in registry["file_families"]}
    missing = family_ids - set(mappings.keys())
    assert not missing, (
        f"normalized_contract.yaml missing mappings for: {missing}"
    )
    for family_id, mapping in mappings.items():
        assert "canonical_object" in mapping, (
            f"{family_id} missing canonical_object"
        )
        assert "precedence" in mapping, f"{family_id} missing precedence"
        assert mapping["precedence"] in {"primary", "secondary", "tertiary"}


def test_sample_files_parse_with_expected_headers():
    sample_dir = ADAPTER_DIR / "sample_files"
    assert sample_dir.exists(), "sample_files/ missing"
    for filename, expected_headers in SAMPLE_FILE_HEADERS.items():
        path = sample_dir / filename
        assert path.exists(), f"missing sample file: {filename}"
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            rows = list(reader)
        assert rows, f"{filename} empty"
        header = rows[0]
        assert header == expected_headers, (
            f"{filename} header mismatch; expected {expected_headers}, got {header}"
        )
        data_rows = rows[1:]
        assert len(data_rows) >= 3, (
            f"{filename} has {len(data_rows)} data rows, need >= 3"
        )


def test_dq_rules_format_valid():
    data = _load_yaml(ADAPTER_DIR / "dq_rules.yaml")
    assert isinstance(data, dict)
    rules = data.get("rules")
    assert isinstance(rules, list) and rules, "dq_rules.yaml has no rules"
    valid_severities = {"blocker", "warning", "info"}
    for rule in rules:
        assert isinstance(rule, dict)
        for key in ("rule_id", "dimension", "severity", "description", "expected"):
            assert key in rule, f"rule missing {key}: {rule}"
        assert rule["severity"] in valid_severities
        assert rule["rule_id"].startswith(("msx_", "ms_")), (
            f"rule_id {rule['rule_id']} missing ms_/msx_ prefix"
        )


def test_reconciliation_checks_ms_recon_prefix():
    data = _load_yaml(ADAPTER_DIR / "reconciliation_checks.yaml")
    assert isinstance(data, dict)
    checks = data.get("checks")
    assert isinstance(checks, list) and len(checks) >= 10, (
        "expected >= 10 reconciliation checks"
    )
    valid_severities = {"blocker", "warning", "info"}
    valid_kinds = {
        "record_count",
        "duplicate_id",
        "null_critical",
        "date_coverage",
        "unit_count",
        "lease_status",
        "budget_actual",
        "commitment_draw",
    }
    for check in checks:
        assert check["check_id"].startswith("ms_recon_"), (
            f"check_id {check['check_id']} missing ms_recon_ prefix"
        )
        assert check["severity"] in valid_severities
        assert check["check_kind"] in valid_kinds
        assert isinstance(check.get("inputs"), list) and check["inputs"]
        assert check.get("expected_invariant")
        assert check.get("remediation")


def test_crosswalk_additions_fragments_shape():
    data = _load_yaml(ADAPTER_DIR / "crosswalk_additions.yaml")
    assert isinstance(data, dict)
    for fragment_key in (
        "property_master_crosswalk_additions",
        "employee_crosswalk_additions",
        "vendor_master_crosswalk_additions",
    ):
        rows = data.get(fragment_key)
        assert isinstance(rows, list) and rows, (
            f"{fragment_key} missing or empty"
        )
        for row in rows:
            for key in (
                "canonical_id",
                "source_system",
                "source_id",
                "match_confidence",
                "match_method",
                "effective_start",
                "survivorship_rule",
                "manual_override",
                "reviewer",
                "last_validated_at",
            ):
                assert key in row, f"{fragment_key} row missing {key}: {row}"
            assert row["match_confidence"] in {
                "high",
                "medium",
                "low",
                "unresolved",
            }
            assert row["match_method"] in {
                "exact",
                "fuzzy",
                "composite",
                "manual",
            }
