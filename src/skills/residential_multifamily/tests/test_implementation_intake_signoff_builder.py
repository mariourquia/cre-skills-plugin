"""Implementation intake and leader sign-off workflow tests."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any, Dict, List

import yaml

from conftest import SUBSYS, validate_against_schema


WORKFLOW_ROOT = (
    SUBSYS / "workflows" / "implementation_intake_signoff_builder"
)


def _load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _load_tool_module():
    tool_path = WORKFLOW_ROOT / "tools" / "implementation_intake_tui.py"
    spec = importlib.util.spec_from_file_location("implementation_intake_tui", tool_path)
    assert spec and spec.loader, f"Unable to load tool module from {tool_path}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _schema(name: str) -> Dict[str, Any]:
    return _load_yaml(WORKFLOW_ROOT / "schemas" / name)


def test_workflow_package_files_present():
    required = [
        WORKFLOW_ROOT / "README.md",
        WORKFLOW_ROOT / "SKILL.md",
        WORKFLOW_ROOT / "routing.yaml",
        WORKFLOW_ROOT / "reference_manifest.yaml",
        WORKFLOW_ROOT / "workflows.md",
        WORKFLOW_ROOT / "interview_modes.md",
        WORKFLOW_ROOT / "question_bank.yaml",
        WORKFLOW_ROOT / "evidence_model.yaml",
        WORKFLOW_ROOT / "templates" / "implementation_intake_packet_template.md",
        WORKFLOW_ROOT / "templates" / "signoff_packet_template.md",
        WORKFLOW_ROOT / "templates" / "action_queue_template.md",
        WORKFLOW_ROOT / "examples" / "sample_evidence_set.yaml",
        WORKFLOW_ROOT / "examples" / "sample_blocker_log.yaml",
        WORKFLOW_ROOT / "examples" / "sample_assumptions_log.yaml",
        WORKFLOW_ROOT / "examples" / "sample_decision_log.yaml",
        WORKFLOW_ROOT / "examples" / "sample_session_state.yaml",
        WORKFLOW_ROOT / "examples" / "sample_implementation_intake_packet.md",
        WORKFLOW_ROOT / "examples" / "sample_leader_signoff_packet.md",
        WORKFLOW_ROOT / "examples" / "sample_action_queue.md",
        WORKFLOW_ROOT / "examples" / "ex01_owner_oversight_multisystem" / "INPUT.md",
        WORKFLOW_ROOT / "examples" / "ex01_owner_oversight_multisystem" / "ROUTING.md",
        WORKFLOW_ROOT / "examples" / "ex01_owner_oversight_multisystem" / "OUTPUT.md",
        WORKFLOW_ROOT / "sessions" / "README.md",
        WORKFLOW_ROOT / "sessions" / ".gitignore",
        WORKFLOW_ROOT / "tests" / "README.md",
        WORKFLOW_ROOT / "tools" / "implementation_intake_tui.py",
    ]
    missing = [str(path.relative_to(SUBSYS)) for path in required if not path.exists()]
    assert not missing, "implementation intake workflow missing files:\n  - " + "\n  - ".join(missing)


def test_question_bank_has_required_modes_categories_and_metadata():
    bank = _load_yaml(WORKFLOW_ROOT / "question_bank.yaml")
    required_modes = {
        "executive_overview",
        "source_by_source_implementation_discovery",
        "field_level_export_and_file_inventory",
        "crosswalk_and_identity_mapping",
        "reporting_calendar_and_sla",
        "approval_and_controls",
        "missing_doc_chase",
        "signoff_packaging",
        "exception_resolution",
    }
    mode_ids = {item["mode_id"] for item in bank.get("interview_modes") or []}
    assert required_modes == mode_ids

    required_categories = {
        "source inventory",
        "environment and access",
        "exports and files",
        "field names and semantics",
        "source-of-truth",
        "crosswalk rules",
        "reporting calendar",
        "approvals and controls",
        "third-party manager reporting",
        "development and construction reporting",
        "benchmark updates",
        "blocker resolution",
    }
    categories = {question["category"] for question in bank.get("questions") or []}
    assert required_categories.issubset(categories)

    required_fields = {
        "question_id",
        "category",
        "audience",
        "trigger_condition",
        "prerequisite_questions",
        "question_text",
        "why_this_matters",
        "expected_answer_type",
        "evidence_requested",
        "severity_if_unanswered",
        "confidence_effect",
        "related_objects",
        "related_outputs",
        "skip_logic",
        "follow_up_logic",
    }
    errors: List[str] = []
    for question in bank.get("questions") or []:
        missing = required_fields - set(question.keys())
        if missing:
            errors.append(f"{question.get('question_id')}: missing fields {sorted(missing)}")
        if not question.get("audience"):
            errors.append(f"{question.get('question_id')}: empty audience")
        if not question.get("evidence_requested"):
            errors.append(f"{question.get('question_id')}: empty evidence_requested")
    assert not errors, "\n".join(errors)


def test_reference_manifest_writes_are_confined_to_workflow_sessions():
    manifest = _load_yaml(WORKFLOW_ROOT / "reference_manifest.yaml")
    bad = []
    for entry in manifest.get("writes") or []:
        path = str(entry.get("path") or "")
        if not path.startswith("workflows/implementation_intake_signoff_builder/sessions/"):
            bad.append(path)
    assert not bad, f"unexpected write targets: {bad}"


def test_examples_validate_against_workflow_schemas():
    validations = [
        (
            _load_yaml(WORKFLOW_ROOT / "examples" / "sample_blocker_log.yaml"),
            _schema("blocker_log_schema.yaml"),
            "sample_blocker_log.yaml",
        ),
        (
            _load_yaml(WORKFLOW_ROOT / "examples" / "sample_assumptions_log.yaml"),
            _schema("assumptions_log_schema.yaml"),
            "sample_assumptions_log.yaml",
        ),
        (
            _load_yaml(WORKFLOW_ROOT / "examples" / "sample_decision_log.yaml"),
            _schema("decision_log_schema.yaml"),
            "sample_decision_log.yaml",
        ),
        (
            _load_yaml(WORKFLOW_ROOT / "examples" / "sample_evidence_set.yaml"),
            _schema("evidence_item_schema.yaml"),
            "sample_evidence_set.yaml",
        ),
        (
            _load_yaml(WORKFLOW_ROOT / "examples" / "sample_session_state.yaml"),
            _schema("session_state_schema.yaml"),
            "sample_session_state.yaml",
        ),
    ]
    failures: List[str] = []
    for instance, schema, label in validations:
        failures.extend(validate_against_schema(instance, schema, path=label))

    signoff_sample = {
        "version": "0.1.0",
        "status": "draft",
        "document_purpose": "Authorize build execution.",
        "implementation_objective": "Complete evidence-backed intake.",
        "systems_covered": ["appfolio", "sage_intacct"],
        "environments_covered": ["appfolio_prod", "intacct_prod"],
        "confirmed_facts": ["AppFolio scope confirmed."],
        "unresolved_assumptions": ["GraySail owner pending."],
        "missing_evidence": ["Intacct field dictionary."],
        "blockers": ["Yardi crosswalk conflict."],
        "top_risks": ["Crosswalk conflict can break rollups."],
        "ownership_assignments": [
            {
                "owner": "Controller",
                "role": "Finance owner",
                "due_date": "2026-04-18",
                "scope": "Provide field dictionary.",
            }
        ],
        "decisions_requested": ["Confirm source-of-truth owner."],
        "approvals_requested": ["Approve build readiness with conditions."],
        "recommended_next_phase": "Conditional build preparation",
        "signoff_status": "pending leadership review",
        "review_metadata": [
            {
                "reviewer_name": "TBD",
                "reviewer_role": "COO",
                "review_date": "2026-04-19",
                "approval_status": "pending leadership review",
                "approval_notes": "",
                "conditions_if_any": "",
            }
        ],
    }
    failures.extend(
        validate_against_schema(
            signoff_sample,
            _schema("signoff_packet_schema.yaml"),
            path="inline_signoff_packet",
        )
    )
    assert not failures, "\n".join(failures)


def test_question_trigger_and_skip_logic():
    tool = _load_tool_module()
    bank = tool.load_question_bank()
    index = tool.question_index(bank)
    context = {
        "mode": "source_by_source_implementation_discovery",
        "role": "implementation_pm",
        "management_mode": "owner_oversight",
        "systems_in_scope": ["appfolio", "sage_intacct", "yardi"],
    }
    answers = {
        "exec_objective": {"value": "Prepare intake packet."},
        "exec_scope_systems": {"value": ["appfolio", "sage_intacct", "yardi"]},
        "exec_scope_environments": {"value": ["appfolio_prod", "intacct_prod", "yardi_legacy"]},
        "management_access_path": {"value": "mixed_direct_and_file_only"},
        "sys_appfolio_scope": {"value": "in scope"},
        "access_export_methods": {"value": ["manual_export", "scheduled_export"]},
    }
    assert tool.question_is_active(index["sys_appfolio_scope"], context, answers)
    assert tool.question_is_active(index["sys_yardi_legacy_scope"], context, answers)
    assert not tool.question_is_active(index["sys_procore_scope"], context, answers)
    assert tool.question_is_active(index["tpm_submission_channel"], context, answers)

    answers_direct = dict(answers)
    answers_direct["management_access_path"] = {"value": "direct_owner_access"}
    assert tool.should_skip(index["tpm_submission_channel"], answers_direct, context)

    follow_ups = tool.follow_up_question_ids(
        index["exec_scope_systems"],
        ["appfolio", "sage_intacct", "yardi"],
    )
    assert "sys_appfolio_scope" in follow_ups
    assert "sys_intacct_scope" in follow_ups
    assert "sys_yardi_legacy_scope" in follow_ups


def test_blocker_and_missing_doc_detection():
    tool = _load_tool_module()
    bank = tool.load_question_bank()
    state = _load_yaml(WORKFLOW_ROOT / "examples" / "sample_session_state.yaml")
    blockers = tool.collect_blockers(state, bank)
    missing_docs = tool.collect_missing_docs(state, bank)
    blocker_ids = {item["blocker_id"] for item in blockers}
    missing_qids = {item["question_id"] for item in missing_docs}

    assert "blk_001" in blocker_ids
    assert "derived_field_dictionary_location" in blocker_ids
    assert "field_dictionary_location" in missing_qids


def test_conflict_detection_finds_competing_rules():
    tool = _load_tool_module()
    conflicts = tool.detect_conflicts(
        [
            {
                "canonical_entity": "property",
                "source_system": "appfolio",
                "preferred_match_key": "property_code",
                "primary_source": "appfolio",
                "effective_date_rule": "as_of_extract",
            },
            {
                "canonical_entity": "property",
                "source_system": "appfolio",
                "preferred_match_key": "legacy_property_name",
                "primary_source": "appfolio",
                "effective_date_rule": "as_of_extract",
            },
        ]
    )
    assert conflicts, "expected at least one detected conflict"


def test_confidence_scoring_downgrades_incomplete_and_tpm_evidence():
    tool = _load_tool_module()
    evidence = _load_yaml(WORKFLOW_ROOT / "examples" / "sample_evidence_set.yaml")["evidence_items"]
    appfolio_score = tool.score_question_confidence(
        "sys_appfolio_scope",
        {"evidence_status": "confirmed_by_export"},
        evidence,
    )
    tpm_score = tool.score_question_confidence(
        "tpm_submission_channel",
        {"evidence_status": "confirmed_by_document"},
        evidence,
    )
    assert appfolio_score > tpm_score
    assert tpm_score < 0.90


def test_signoff_packet_generation_contains_required_sections():
    tool = _load_tool_module()
    bank = tool.load_question_bank()
    state = _load_yaml(WORKFLOW_ROOT / "examples" / "sample_session_state.yaml")
    packet = tool.render_leader_signoff_packet(state, bank)
    required_headings = [
        "## Document Purpose",
        "## Implementation Objective",
        "## Systems And Environments Covered",
        "## What Has Been Confirmed",
        "## What Is Still Assumed",
        "## What Is Blocked",
        "## Top Three Risks",
        "## Decisions Requested",
        "## Approvals Requested",
        "## Owners And Dates",
        "## Recommendation",
        "## Approval Section",
    ]
    missing = [heading for heading in required_headings if heading not in packet]
    assert not missing, missing
    assert "Prepare a build-ready implementation packet" in packet


def test_action_queue_generation_contains_required_groups_and_validates():
    tool = _load_tool_module()
    state = _load_yaml(WORKFLOW_ROOT / "examples" / "sample_session_state.yaml")
    queue = tool.build_action_queue(state)
    errors = validate_against_schema(
        queue,
        _schema("action_queue_schema.yaml"),
        path="generated_action_queue",
    )
    assert not errors, "\n".join(errors)

    rendered = tool.render_action_queue(state)
    for heading in [
        "## Business",
        "## Technical",
        "## Data",
        "## Reporting",
        "## Controls",
        "## Dependencies",
    ]:
        assert heading in rendered


def test_resume_behavior_returns_remaining_questions_in_priority_order():
    tool = _load_tool_module()
    bank = tool.load_question_bank()
    state = tool.initialize_session(
        engagement_id="demo_engagement",
        session_id="demo_session",
        mode="source_by_source_implementation_discovery",
        role="implementation_pm",
        management_mode="owner_oversight",
        systems=["appfolio", "sage_intacct"],
    )
    state["answers"]["exec_objective"] = {"value": "Prepare intake packet.", "evidence_status": "confirmed_by_document"}
    state["answers"]["exec_scope_systems"] = {"value": ["appfolio", "sage_intacct"], "evidence_status": "confirmed_by_document"}
    state["answers"]["exec_scope_environments"] = {"value": ["appfolio_prod", "intacct_prod"], "evidence_status": "confirmed_by_document"}
    state["answers"]["management_access_path"] = {"value": "mixed_direct_and_file_only", "evidence_status": "confirmed_by_document"}
    queue = tool.next_question_ids(bank, state)
    assert queue[:2] == ["sys_appfolio_scope", "sys_intacct_scope"]


def test_no_secret_storage_guard_and_examples_are_clean():
    tool = _load_tool_module()
    assert tool.contains_secret("api_key: sk-abcdefghijklmnopqrstuv")
    assert tool.contains_secret("Bearer aabbccddeeffgghhiijjkkllmm")
    assert not tool.contains_secret("api_key_placeholder")

    sample_paths = [
        WORKFLOW_ROOT / "examples" / "sample_session_state.yaml",
        WORKFLOW_ROOT / "examples" / "sample_evidence_set.yaml",
        WORKFLOW_ROOT / "examples" / "sample_blocker_log.yaml",
    ]
    bad = []
    for path in sample_paths:
        text = path.read_text(encoding="utf-8")
        if "sk-" in text or "Bearer " in text or "AKIA" in text:
            bad.append(str(path.relative_to(SUBSYS)))
    assert not bad, f"secret-like content found in examples: {bad}"


def test_third_party_manager_mode_behavior_is_first_class():
    tool = _load_tool_module()
    bank = tool.load_question_bank()
    index = tool.question_index(bank)
    context = {
        "mode": "reporting_calendar_and_sla",
        "role": "third_party_manager_oversight_lead",
        "management_mode": "owner_oversight",
        "systems_in_scope": ["third_party_manager_submission", "appfolio"],
    }
    answers = {
        "management_access_path": {"value": "mixed_direct_and_file_only"},
        "tpm_submission_channel": {"value": ["owner pack", "variance backup"]},
    }
    assert tool.question_is_active(index["tpm_submission_channel"], context, answers)
    assert tool.question_is_active(index["tpm_calendar_alignment"], context, answers)
