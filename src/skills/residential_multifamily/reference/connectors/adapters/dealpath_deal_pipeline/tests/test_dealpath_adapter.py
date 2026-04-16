"""Dealpath adapter wave-5 conformance tests.

Covers the wave-5 fill-in artifacts:
  - manifest.yaml schema conformance
  - sample_raw/*.jsonl parses as JSONL and carries status tag
  - sample_normalized/*.jsonl conforms to canonical shape
  - dq_rules.yaml format validity
  - reconciliation_checks.yaml format validity
  - crosswalk_additions.yaml structural correctness
  - source_contract.yaml, normalized_contract.yaml, field_mapping.yaml
    parse and declare the expected entities
  - runbooks and edge_cases markdown files present

Stdlib + PyYAML only; consistent with other adapter-local tests.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml


ADAPTER_DIR = Path(__file__).resolve().parents[1]
ADAPTERS_ROOT = ADAPTER_DIR.parent
if str(ADAPTERS_ROOT) not in sys.path:
    sys.path.insert(0, str(ADAPTERS_ROOT))


# Entities covered by this adapter (deal_pipeline domain).
EXPECTED_ENTITIES = [
    "deal",
    "asset",
    "deal_milestone",
    "deal_key_date",
    "deal_team_member",
    "ic_decision",
    "deal_document",
    "deal_status_history",
]

# Sample files present in sample_raw/ and sample_normalized/.
EXPECTED_SAMPLE_FILES = [
    "deals.jsonl",
    "assets.jsonl",
    "deal_milestones.jsonl",
    "deal_key_dates.jsonl",
    "ic_decisions.jsonl",
    "deal_team.jsonl",
]


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                rows.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise AssertionError(
                    f"{path}: line {idx + 1} is not valid JSON: {exc}"
                ) from exc
    return rows


# ---------------------------------------------------------------------
# Manifest conformance
# ---------------------------------------------------------------------
def test_dealpath_manifest_conforms():
    manifest = _load_yaml(ADAPTER_DIR / "manifest.yaml")
    assert manifest["adapter_id"] == "dealpath_deal_pipeline"
    assert manifest["connector_domain"] == "deal_pipeline"
    assert manifest["vendor_family"] == "dealpath_family"
    assert manifest["status"] in {"stub", "starter", "production", "deprecated"}
    assert isinstance(manifest["supported_source_systems"], list)
    assert "dealpath_prod" in manifest["supported_source_systems"]
    assert isinstance(manifest["mapping_hints"], list) and manifest["mapping_hints"]
    assert isinstance(manifest["known_gotchas"], list) and manifest["known_gotchas"]


# ---------------------------------------------------------------------
# Sample files: sample_raw parses and carries status tags
# ---------------------------------------------------------------------
def test_dealpath_sample_raw_parses_and_carries_status_tag():
    sample_raw = ADAPTER_DIR / "sample_raw"
    assert sample_raw.exists() and sample_raw.is_dir()
    found = {p.name for p in sample_raw.iterdir() if p.is_file()}
    missing = set(EXPECTED_SAMPLE_FILES) - found
    assert not missing, f"sample_raw missing files: {sorted(missing)}"

    for fname in EXPECTED_SAMPLE_FILES:
        rows = _load_jsonl(sample_raw / fname)
        assert rows, f"sample_raw/{fname} is empty"
        for idx, row in enumerate(rows):
            assert row.get("status") in ("sample", "stub", "template"), (
                f"sample_raw/{fname} row {idx}: missing status tag"
            )
            # Provenance envelope per _test_helpers convention.
            for required in (
                "source_name",
                "source_type",
                "source_date",
                "extracted_at",
                "extractor_version",
                "source_row_id",
            ):
                assert required in row, (
                    f"sample_raw/{fname} row {idx}: missing provenance field {required!r}"
                )
            assert row["source_name"] == "dealpath_prod"
            assert row["source_type"] == "deal_pipeline"


# ---------------------------------------------------------------------
# Sample normalized: conforms to canonical shape
# ---------------------------------------------------------------------
def test_dealpath_sample_normalized_conforms_to_canonical():
    sample_norm = ADAPTER_DIR / "sample_normalized"
    assert sample_norm.exists() and sample_norm.is_dir()
    found = {p.name for p in sample_norm.iterdir() if p.is_file()}
    missing = set(EXPECTED_SAMPLE_FILES) - found
    assert not missing, f"sample_normalized missing files: {sorted(missing)}"

    # Canonical key fields for each entity (mirrors normalized_contract.yaml
    # required_canonical_fields).
    # Note: entity-level `status` fields are disambiguated as
    # deal_status / milestone_status / approval_status in the sample
    # output to avoid JSON serialization collision with the envelope
    # status tag (envelope: "sample" vs entity: "active" / "achieved" /
    # "approved"). The canonical contract still names the concept
    # `status`; the rename is a sample-file serialization convention.
    canonical_keys = {
        "deals.jsonl": [
            "deal_id",
            "deal_name",
            "canonical_asset_id",
            "deal_type",
            "pipeline_stage",
            "market",
            "deal_status",
        ],
        "assets.jsonl": [
            "canonical_asset_id",
            "asset_name",
            "market",
            "asset_type",
        ],
        "deal_milestones.jsonl": [
            "deal_milestone_id",
            "deal_id",
            "milestone_type",
            "milestone_status",
        ],
        "deal_key_dates.jsonl": [
            "deal_key_date_id",
            "deal_id",
            "date_type",
            "date_value",
        ],
        "ic_decisions.jsonl": [
            "approval_request_id",
            "subject_object_type",
            "subject_object_id",
            "decision",
            "decided_date",
            "approval_status",
        ],
        "deal_team.jsonl": [
            "deal_team_member_id",
            "deal_id",
            "member_id_ref",
            "role",
        ],
    }

    for fname, keys in canonical_keys.items():
        rows = _load_jsonl(sample_norm / fname)
        assert rows, f"sample_normalized/{fname} is empty"
        for idx, row in enumerate(rows):
            for key in keys:
                assert key in row, (
                    f"sample_normalized/{fname} row {idx}: missing canonical key {key!r}"
                )


# ---------------------------------------------------------------------
# DQ rules format valid
# ---------------------------------------------------------------------
def test_dealpath_dq_rules_format_valid():
    dq = _load_yaml(ADAPTER_DIR / "dq_rules.yaml")
    assert "rules" in dq and isinstance(dq["rules"], list)
    assert dq["rules"], "dq_rules.yaml must declare at least one rule"
    seen_ids = set()
    for rule in dq["rules"]:
        for key in ("rule_id", "dimension", "severity", "description",
                    "expected", "remediation"):
            assert key in rule, f"rule missing field {key!r}: {rule.get('rule_id')}"
        assert rule["severity"] in {"blocker", "warning", "info"}
        assert rule["rule_id"].startswith("dp_"), (
            f"rule_id must be dp_ prefixed: {rule['rule_id']!r}"
        )
        assert rule["rule_id"] not in seen_ids, (
            f"duplicate rule_id: {rule['rule_id']!r}"
        )
        seen_ids.add(rule["rule_id"])


# ---------------------------------------------------------------------
# Reconciliation checks format valid
# ---------------------------------------------------------------------
def test_dealpath_reconciliation_checks_format_valid():
    data = _load_yaml(ADAPTER_DIR / "reconciliation_checks.yaml")
    assert "checks" in data and isinstance(data["checks"], list)
    assert len(data["checks"]) >= 10, (
        "reconciliation_checks.yaml must declare at least 10 checks; "
        f"found {len(data['checks'])}"
    )
    seen = set()
    for check in data["checks"]:
        for key in ("check_id", "check_kind", "severity", "description",
                    "inputs", "expected_invariant", "remediation"):
            assert key in check, (
                f"check missing field {key!r}: {check.get('check_id')}"
            )
        assert check["check_id"].startswith("dp_recon_"), (
            f"check_id must be dp_recon_ prefixed: {check['check_id']!r}"
        )
        assert check["severity"] in {"blocker", "warning", "info"}
        assert check["check_id"] not in seen, (
            f"duplicate check_id: {check['check_id']!r}"
        )
        seen.add(check["check_id"])


# ---------------------------------------------------------------------
# Source contract parses and covers expected entities
# ---------------------------------------------------------------------
def test_dealpath_source_contract_covers_expected_entities():
    data = _load_yaml(ADAPTER_DIR / "source_contract.yaml")
    assert "entities" in data
    entities = data["entities"]
    for name in EXPECTED_ENTITIES:
        assert name in entities, (
            f"source_contract.yaml missing entity {name!r}"
        )


# ---------------------------------------------------------------------
# Normalized contract parses and covers expected entities
# ---------------------------------------------------------------------
def test_dealpath_normalized_contract_covers_expected_entities():
    data = _load_yaml(ADAPTER_DIR / "normalized_contract.yaml")
    assert "mappings" in data
    mappings = data["mappings"]
    for name in EXPECTED_ENTITIES:
        assert name in mappings, (
            f"normalized_contract.yaml missing mapping {name!r}"
        )
    # Required canonical extensions flagged.
    required_extensions = {
        "deal",
        "deal_milestone",
        "deal_key_date",
        "deal_team_member",
        "ic_decision",
        "deal_document",
    }
    for name in required_extensions:
        mapping = mappings[name]
        assert mapping.get("requires_canonical_extension") is True, (
            f"mapping {name!r} must set requires_canonical_extension: true"
        )


# ---------------------------------------------------------------------
# Field mapping parses and covers expected entities
# ---------------------------------------------------------------------
def test_dealpath_field_mapping_covers_expected_entities():
    data = _load_yaml(ADAPTER_DIR / "field_mapping.yaml")
    assert "entities" in data
    entities = data["entities"]
    for name in EXPECTED_ENTITIES:
        assert name in entities, (
            f"field_mapping.yaml missing entity {name!r}"
        )
        mappings = entities[name].get("mappings", [])
        assert mappings, f"field_mapping.yaml entity {name!r} has no mappings"
        for m in mappings:
            for key in ("source_field", "target_field", "transform", "required"):
                assert key in m, (
                    f"field_mapping entity {name!r} mapping missing {key!r}: {m}"
                )


# ---------------------------------------------------------------------
# Crosswalk additions structural
# ---------------------------------------------------------------------
def test_dealpath_crosswalk_additions_structural():
    data = _load_yaml(ADAPTER_DIR / "crosswalk_additions.yaml")
    for section in (
        "asset_crosswalk",
        "property_master_crosswalk",
        "dev_project_crosswalk",
        "market_crosswalk",
    ):
        assert section in data, f"crosswalk_additions.yaml missing {section!r}"
        assert "rows" in data[section]
        rows = data[section]["rows"]
        assert rows, f"{section}.rows is empty"
        for row in rows:
            for key in (
                "dealpath_id",
                "canonical_id",
                "effective_start",
                "survivorship_rule",
                "confidence",
            ):
                assert key in row, (
                    f"{section} row missing field {key!r}: {row}"
                )


# ---------------------------------------------------------------------
# Workflow activation fragment
# ---------------------------------------------------------------------
def test_dealpath_workflow_activation_fragment_loads():
    data = _load_yaml(ADAPTER_DIR / "workflow_activation_additions.yaml")
    assert data.get("dealpath_role") == "primary_for_deal_pipeline_domain"
    assert isinstance(data.get("proposes_new_workflows"), list)
    assert data["proposes_new_workflows"], "must propose at least one new workflow"


# ---------------------------------------------------------------------
# Runbooks and narrative docs present
# ---------------------------------------------------------------------
def test_dealpath_narrative_docs_present():
    for rel in (
        "README.md",
        "edge_cases.md",
        "reconciliation_rules.md",
        "runbooks/dealpath_onboarding.md",
        "runbooks/dealpath_common_issues.md",
    ):
        path = ADAPTER_DIR / rel
        assert path.exists(), f"missing narrative doc: {rel}"
        assert path.stat().st_size > 0, f"{rel} is empty"
