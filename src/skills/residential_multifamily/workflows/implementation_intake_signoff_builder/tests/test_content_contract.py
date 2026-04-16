from __future__ import annotations

from pathlib import Path

import yaml


PACK_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "SKILL.md",
    "routing.yaml",
    "reference_manifest.yaml",
    "change_log.md",
    "interview_modes.md",
    "evidence_request_catalog.md",
    "question_bank.yaml",
    "schemas/source_inventory_schema.yaml",
    "schemas/export_field_inventory_schema.yaml",
    "schemas/credentials_model_schema.yaml",
    "schemas/crosswalk_rules_schema.yaml",
    "schemas/reporting_calendar_schema.yaml",
    "schemas/approval_control_schema.yaml",
    "schemas/assumptions_gaps_blockers_schema.yaml",
    "schemas/decision_log_schema.yaml",
    "templates/implementation_intake_packet.md",
    "templates/source_inventory_register.md",
    "templates/export_field_inventory.md",
    "templates/credentials_access_model.md",
    "templates/crosswalk_rules_register.md",
    "templates/reporting_calendar_sla_register.md",
    "templates/assumptions_gaps_blockers_log.md",
    "templates/leader_signoff_pack.md",
    "templates/decision_log.md",
    "examples/ex01_sample_session.yaml",
    "examples/ex01_implementation_intake_packet.md",
    "examples/ex01_leader_signoff_pack.md",
]

REQUIRED_MODES = {
    "executive_summary_mode",
    "source_by_source_onboarding_mode",
    "field_level_export_mode",
    "crosswalk_and_mapping_mode",
    "reporting_calendar_mode",
    "approvals_and_controls_mode",
    "missing_docs_chase_mode",
    "final_signoff_packaging_mode",
}

REQUIRED_ARTIFACT_KEYS = {
    "implementation_intake_packet",
    "source_inventory_register",
    "export_field_inventory",
    "credentials_access_model",
    "crosswalk_rules_register",
    "reporting_calendar_sla_register",
    "assumptions_gaps_blockers_log",
    "leader_signoff_pack",
    "decision_log",
}


def _load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_required_files_present():
    missing = [rel for rel in REQUIRED_FILES if not (PACK_ROOT / rel).exists()]
    assert not missing, f"missing required implementation-intake artifacts: {missing}"


def test_question_bank_modes_and_fields():
    data = _load_yaml(PACK_ROOT / "question_bank.yaml")
    modes = {entry["mode_id"] for entry in data["modes"]}
    assert REQUIRED_MODES.issubset(modes)

    seen = set()
    for question in data["questions"]:
        qid = question["question_id"]
        assert qid not in seen, f"duplicate question_id: {qid}"
        seen.add(qid)
        for field in [
            "question_id",
            "mode",
            "audience",
            "category",
            "trigger_condition",
            "prerequisite_questions",
            "question_text",
            "why_it_matters",
            "evidence_requested",
            "answer_type",
            "confidence_impact",
            "blocking_severity_if_unanswered",
            "related_output_artifacts",
            "artifact_key",
        ]:
            assert field in question, f"{qid} missing {field}"


def test_question_bank_covers_required_artifacts():
    data = _load_yaml(PACK_ROOT / "question_bank.yaml")
    covered = set()
    for question in data["questions"]:
        covered.update(question.get("related_output_artifacts") or [])
    assert REQUIRED_ARTIFACT_KEYS.issubset(covered)


def test_reference_manifest_writes_stay_local():
    data = _load_yaml(PACK_ROOT / "reference_manifest.yaml")
    writes = data.get("writes") or []
    assert writes, "writes must declare session artifacts"
    for entry in writes:
        path = entry["path"]
        assert path.startswith("workflows/implementation_intake_signoff_builder/sessions/"), path
        assert "_core/" not in path
        assert "reference/connectors/" not in path


def test_examples_use_allowed_signoff_status():
    text = (PACK_ROOT / "examples/ex01_leader_signoff_pack.md").read_text(encoding="utf-8")
    assert "approved with conditions" in text
