"""GraySail placeholder adapter: wave-5 classification-pending conformance.

These tests enforce the deferred-mode posture of the placeholder adapter:
  - manifest conforms to the adapter manifest schema contract where it can
    (status: stub, adapter_id == directory name, connector_domain valid).
  - classification_worksheet.md is present and carries unchecked operator
    questions (operator action is still pending).
  - bounded_assumptions.yaml is present and parseable as YAML.
  - provisional_source_contract.yaml is present and carries
    classification_status: pending.
  - workflow_relevance_map.yaml is present and lists every candidate
    dependency as blocked_until_classified.
  - runbooks/graysail_classification_path.md is present and includes the
    required Checkpoints section.
  - dq_rules.yaml is present, carries gs_classification_pending_blocker,
    and every rule has severity: warning (deferred mode).

None of these tests attempt to advance the adapter past `stub`; that
path runs only when the adapter is forked into
graysail_<role>_<pattern>/ per runbooks/graysail_classification_path.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml


ADAPTER_DIR = Path(__file__).resolve().parents[1]
ADAPTERS_ROOT = ADAPTER_DIR.parent
if str(ADAPTERS_ROOT) not in sys.path:
    sys.path.insert(0, str(ADAPTERS_ROOT))


# ----------------------------------------------------------------------
# Manifest conformance
# ----------------------------------------------------------------------

def test_graysail_manifest_conforms_to_placeholder_contract():
    """Manifest loads and carries the bounded-placeholder invariants.

    Does NOT call run_adapter_manifest_checks because the placeholder does
    not ship example_raw_payload.jsonl / normalized_output_example.jsonl /
    mapping_template.yaml (every field is classification_pending per
    provisional_source_contract.yaml). The required-field set below is the
    subset of the adapter_manifest.schema.yaml contract that applies to a
    bounded placeholder.
    """
    manifest_path = ADAPTER_DIR / "manifest.yaml"
    assert manifest_path.exists(), "manifest.yaml missing"
    manifest = yaml.safe_load(manifest_path.read_text())

    for key in (
        "adapter_id",
        "adapter_name",
        "vendor_family",
        "connector_domain",
        "status",
        "supported_source_systems",
        "mapping_hints",
        "known_gotchas",
        "reference_documentation",
        "author_metadata",
        "last_updated",
    ):
        assert key in manifest, f"manifest.yaml missing required field {key!r}"

    assert manifest["adapter_id"] == ADAPTER_DIR.name, (
        f"adapter_id {manifest['adapter_id']!r} must equal directory name "
        f"{ADAPTER_DIR.name!r}"
    )
    assert manifest["status"] == "stub", (
        "placeholder MUST remain status: stub until classification_path runbook closes"
    )
    assert manifest["vendor_family"] == "graysail_family"
    assert manifest["connector_domain"] in {
        "pms",
        "gl",
        "crm",
        "ap",
        "market_data",
        "construction",
        "hr_payroll",
        "manual_uploads",
        "deal_pipeline",
    }, f"connector_domain {manifest['connector_domain']!r} not in schema enum"


# ----------------------------------------------------------------------
# Classification worksheet is present and unchecked
# ----------------------------------------------------------------------

def test_classification_worksheet_present_and_unchecked():
    """Worksheet exists and carries the operator question sections.

    Unchecked means: no Section 1-5 question has been answered with an
    operator response. The placeholder ships with the question bank only.
    The heuristic below checks that every Section heading is present AND
    that no "Answer:" or operator-filled artifact has been injected.
    """
    worksheet = ADAPTER_DIR / "classification_worksheet.md"
    assert worksheet.exists(), "classification_worksheet.md missing"
    text = worksheet.read_text()

    # The worksheet structure must be intact.
    for section in (
        "## Section 1: role and scope",
        "## Section 2: access and ingestion",
        "## Section 3: content type and shape",
        "## Section 4: sensitivity and governance",
        "## Section 5: workflow dependencies",
    ):
        assert section in text, f"classification_worksheet.md missing {section!r}"

    # Operator action must still be pending. No ad-hoc "Answer:" or
    # "Confirmed:" lines may have been added (those would indicate a
    # partial classification that should have gone into the forked
    # adapter, not the placeholder).
    forbidden_markers = ("\nAnswer:", "\nConfirmed:", "\n**Operator response:**")
    for marker in forbidden_markers:
        assert marker not in text, (
            f"worksheet appears to carry operator responses ({marker!r}); "
            "classification should move to the forked adapter, not remain in the placeholder"
        )


# ----------------------------------------------------------------------
# Bounded assumptions parseable
# ----------------------------------------------------------------------

def test_bounded_assumptions_present_and_parseable():
    src = ADAPTER_DIR / "bounded_assumptions.yaml"
    assert src.exists(), "bounded_assumptions.yaml missing"
    data = yaml.safe_load(src.read_text())
    assert isinstance(data, dict), "bounded_assumptions.yaml must parse as a mapping"
    assert "assumptions" in data, "bounded_assumptions.yaml missing 'assumptions' key"
    assert isinstance(data["assumptions"], list) and len(data["assumptions"]) >= 1, (
        "bounded_assumptions.yaml must list at least one assumption"
    )
    for assumption in data["assumptions"]:
        for field in ("id", "assumption", "confidence", "evidence_basis",
                      "blast_radius_if_wrong", "remediation_if_wrong"):
            assert field in assumption, (
                f"bounded_assumption {assumption.get('id', '<unknown>')!r} "
                f"missing required field {field!r}"
            )


# ----------------------------------------------------------------------
# Provisional source contract present and classification_pending
# ----------------------------------------------------------------------

def test_provisional_source_contract_present():
    src = ADAPTER_DIR / "provisional_source_contract.yaml"
    assert src.exists(), "provisional_source_contract.yaml missing"
    data = yaml.safe_load(src.read_text())
    assert isinstance(data, dict)
    assert data.get("classification_status") == "pending", (
        "provisional_source_contract.yaml must carry classification_status: pending"
    )
    assert data.get("status_tag") in {"stub", "sample", "template"}, (
        "provisional_source_contract.yaml must carry a stub/sample/template status_tag"
    )
    # Every placeholder entity must be marked classification_pending.
    entities = data.get("entities") or {}
    assert entities, "provisional_source_contract.yaml must declare at least one entity"
    for name, entity in entities.items():
        assert entity.get("classification_pending") is True, (
            f"entity {name!r} must carry classification_pending: true"
        )


# ----------------------------------------------------------------------
# Workflow relevance map present and all blocked_until_classified
# ----------------------------------------------------------------------

def test_workflow_relevance_map_present_and_all_blocked():
    src = ADAPTER_DIR / "workflow_relevance_map.yaml"
    assert src.exists(), "workflow_relevance_map.yaml missing"
    data = yaml.safe_load(src.read_text())
    assert isinstance(data, dict)

    global_rules = data.get("global_rules") or {}
    assert global_rules.get("default_dependency_status") == "blocked_until_classified", (
        "workflow_relevance_map.yaml::global_rules.default_dependency_status "
        "must be blocked_until_classified"
    )

    candidates = data.get("candidate_dependencies") or []
    assert len(candidates) >= 1, (
        "workflow_relevance_map.yaml must list at least one candidate_dependency"
    )
    for entry in candidates:
        assert entry.get("blocked_until_classified") is True, (
            f"candidate dependency {entry.get('workflow_slug', '<unknown>')!r} "
            "must carry blocked_until_classified: true"
        )


# ----------------------------------------------------------------------
# Classification-path runbook present and carries Checkpoints
# ----------------------------------------------------------------------

def test_classification_path_runbook_present_with_checkpoints():
    runbook = ADAPTER_DIR / "runbooks" / "graysail_classification_path.md"
    assert runbook.exists(), "runbooks/graysail_classification_path.md missing"
    text = runbook.read_text()
    assert "## Checkpoints" in text, (
        "graysail_classification_path.md must declare a '## Checkpoints' section"
    )
    # At least the eight checkpoints the adapter relies on.
    for checkpoint in ("C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"):
        assert f"Checkpoint {checkpoint}" in text, (
            f"graysail_classification_path.md missing Checkpoint {checkpoint}"
        )
    # Fork-and-rename closure rule.
    assert "graysail_<role>_<pattern>" in text, (
        "graysail_classification_path.md must name the forked slug pattern"
    )


# ----------------------------------------------------------------------
# dq_rules.yaml carries gs_classification_pending_blocker; every rule is
# severity: warning (deferred mode)
# ----------------------------------------------------------------------

def test_dq_rules_deferred_mode_posture():
    src = ADAPTER_DIR / "dq_rules.yaml"
    assert src.exists(), "dq_rules.yaml missing"
    data = yaml.safe_load(src.read_text())
    assert isinstance(data, dict)

    rules = data.get("rules") or []
    assert len(rules) >= 10, (
        f"dq_rules.yaml must declare >= 10 deferred-mode rules; got {len(rules)}"
    )

    rule_ids = {rule["rule_id"] for rule in rules}
    assert "gs_classification_pending_blocker" in rule_ids, (
        "dq_rules.yaml must include gs_classification_pending_blocker master gate"
    )

    # Every rule must be severity: warning until classification closes.
    for rule in rules:
        rid = rule.get("rule_id", "<unknown>")
        assert rule.get("severity") == "warning", (
            f"dq_rule {rid!r} must be severity: warning while placeholder is in stub; "
            f"got {rule.get('severity')!r}"
        )
        # Every rule id must carry the gs_ prefix.
        assert rid.startswith("gs_"), (
            f"dq_rule {rid!r} must use the gs_ prefix per adapter rule_id convention"
        )
