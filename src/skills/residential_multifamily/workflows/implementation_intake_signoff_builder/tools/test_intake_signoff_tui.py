from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
import sys

sys.path.insert(0, str(HERE))

import intake_signoff_tui as tool  # noqa: E402


class ParserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.questions = {q.question_id: q for q in tool.load_questions()}

    def test_yaml_list_validation(self) -> None:
        question = self.questions["exec_002"]
        raw = """
- source_id: appfolio_ops
  system_name: AppFolio
  business_purpose: PMS
  in_scope_modules: [leasing]
  lifecycle_status: active
  source_role: system_of_record
  owner: ops
  admin_contact: admin@example.com
  export_api_availability: scheduled_export
  export_delivery_methods: [csv]
  instance_count: 1
  environment_details: prod
  portfolio_coverage: all assets
  module_variance_notes: ""
  source_caveats: ""
  credential_pattern: sftp_key_placeholder
  secrets_owner: it
  approval_requirements: [ops]
  sample_files_available: true
  sandbox_available: false
  refresh_cadence: daily
  latency_expectation: next day
  evidence_status: confirmed
  evidence_detail: file
  blocker_notes: ""
  notes: ""
  confidence: high
"""
        ok, value, error = tool.parse_answer(question, raw)
        self.assertTrue(ok, error)
        self.assertEqual(value[0]["source_id"], "appfolio_ops")

    def test_yaml_list_rejects_missing_required_fields(self) -> None:
        question = self.questions["exec_002"]
        raw = """
- source_id: broken
  system_name: Broken
"""
        ok, _value, error = tool.parse_answer(question, raw)
        self.assertFalse(ok)
        self.assertIn("missing required field", error)


class WorkflowLogicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.questions = tool.load_questions()
        cls.by_id = {q.question_id: q for q in cls.questions}

    def make_session(self) -> dict:
        return tool.create_session(
            org_id="beacon",
            engagement_id="beacon_impl",
            selected_modes=sorted({q.mode for q in self.questions}),
            session_id="sess1",
        )

    def test_required_sections_completeness(self) -> None:
        session = self.make_session()
        status = tool.required_section_status(session, self.questions)
        self.assertIn("exec_001", status["missing"])
        tool.record_answer(session, self.by_id["exec_001"], "Context", "confirmed", "verbal")
        status = tool.required_section_status(session, self.questions)
        self.assertNotIn("exec_001", status["missing"])

    def test_blocker_detection(self) -> None:
        session = self.make_session()
        tool.record_answer(
            session,
            self.by_id["docs_001"],
            [{
                "item_id": "missing_crosswalk",
                "area": "crosswalk",
                "status": "blocked",
                "description": "Vendor crosswalk workbook not received",
                "missing_evidence": "mapping workbook",
                "owner": "finance systems",
                "next_step": "request workbook",
                "due_date": "2026-04-18",
                "downstream_impact": "cannot finalize vendor reconciliation",
            }],
            "confirmed",
            "file",
        )
        blockers = tool.derive_blockers(session, self.questions)
        self.assertTrue(any("missing_crosswalk" in item for item in blockers))

    def test_missing_doc_detection(self) -> None:
        session = self.make_session()
        missing = tool.derive_missing_docs(session, self.questions)
        self.assertTrue(any(item["question_id"] == "exec_001" for item in missing))

    def test_evidence_tagging_validation(self) -> None:
        session = self.make_session()
        with self.assertRaises(ValueError):
            tool.record_answer(session, self.by_id["exec_001"], "Context", "confirmed", "assumed")

    def test_no_secret_capture_in_outputs(self) -> None:
        session = self.make_session()
        tool.record_answer(
            session,
            self.by_id["src_001"],
            [{
                "source_id": "intacct",
                "access_method": "api",
                "direct_api_access": True,
                "scheduled_export_available": True,
                "manual_export_only": False,
                "file_delivery_method": "api",
                "sandbox_available": True,
                "credential_owner": "finance systems",
                "provisioning_method": "ticketed access",
                "secret_storage_system": "password=abc123SUPERSECRET",
                "least_privilege_notes": "scoped to reports only",
                "secret_rotation_owner": "security",
                "approval_requirements": ["CFO"],
                "environment_notes": "Bearer abcdefghijklmnopqrstuvwxyz123456",
                "blocker_notes": "",
                "evidence_status": "confirmed",
                "evidence_detail": "verbal",
                "notes": "api_key=sk-live-1234567890abcdef",
            }],
            "confirmed",
            "verbal",
        )
        bundle = tool.build_artifact_bundle(session, self.questions)
        joined = "\n".join(bundle.values())
        self.assertNotIn("SUPERSECRET", joined)
        self.assertNotIn("sk-live-", joined)
        self.assertIn("[REDACTED_SECRET]", joined)

    def test_signoff_packet_generation(self) -> None:
        session = self.make_session()
        tool.record_answer(session, self.by_id["exec_001"], "Context summary", "confirmed", "verbal")
        tool.record_answer(session, self.by_id["sign_002"], "approved", "confirmed", "verbal")
        bundle = tool.build_artifact_bundle(session, self.questions)
        self.assertIn("leader_signoff_pack.md", bundle)
        self.assertIn("Status: approved", bundle["leader_signoff_pack.md"])

    def test_section_resume_behavior(self) -> None:
        session = self.make_session()
        tool.record_answer(session, self.by_id["exec_001"], "Context summary", "confirmed", "verbal")
        with tempfile.TemporaryDirectory() as tmpdir:
            original = tool.SESSIONS_DIR
            try:
                tool.SESSIONS_DIR = Path(tmpdir)
                path = tool.save_session(session)
                loaded = tool.load_session(path)
            finally:
                tool.SESSIONS_DIR = original
        self.assertIn("exec_001", loaded["answers"])
        self.assertEqual(loaded["answers"]["exec_001"]["value"], "Context summary")

    def test_conflict_detection(self) -> None:
        session = self.make_session()
        tool.record_answer(
            session,
            self.by_id["exec_002"],
            [
                {
                    "source_id": "appfolio",
                    "system_name": "AppFolio",
                    "business_purpose": "PMS",
                    "in_scope_modules": ["leasing"],
                    "lifecycle_status": "active",
                    "source_role": "system_of_record",
                    "owner": "ops",
                    "admin_contact": "ops@example.com",
                    "export_api_availability": "api",
                    "export_delivery_methods": ["api"],
                    "instance_count": 1,
                    "environment_details": "prod",
                    "portfolio_coverage": "all",
                    "module_variance_notes": "",
                    "source_caveats": "",
                    "credential_pattern": "oauth_placeholder",
                    "secrets_owner": "it",
                    "approval_requirements": ["ops"],
                    "sample_files_available": True,
                    "sandbox_available": False,
                    "refresh_cadence": "daily",
                    "latency_expectation": "1 day",
                    "evidence_status": "confirmed",
                    "evidence_detail": "file",
                    "blocker_notes": "",
                    "notes": "",
                    "confidence": "high",
                },
                {
                    "source_id": "appfolio",
                    "system_name": "AppFolio Legacy",
                    "business_purpose": "PMS",
                    "in_scope_modules": ["leasing"],
                    "lifecycle_status": "active",
                    "source_role": "system_of_record",
                    "owner": "ops",
                    "admin_contact": "ops@example.com",
                    "export_api_availability": "api",
                    "export_delivery_methods": ["api"],
                    "instance_count": 1,
                    "environment_details": "prod",
                    "portfolio_coverage": "all",
                    "module_variance_notes": "",
                    "source_caveats": "",
                    "credential_pattern": "oauth_placeholder",
                    "secrets_owner": "it",
                    "approval_requirements": ["ops"],
                    "sample_files_available": True,
                    "sandbox_available": False,
                    "refresh_cadence": "daily",
                    "latency_expectation": "1 day",
                    "evidence_status": "confirmed",
                    "evidence_detail": "file",
                    "blocker_notes": "",
                    "notes": "",
                    "confidence": "high",
                },
            ],
            "confirmed",
            "file",
        )
        conflicts = tool.detect_conflicts(session)
        self.assertTrue(any("source_inventory" in item for item in conflicts))

    def test_confidence_scoring_prefers_file_evidence(self) -> None:
        session = self.make_session()
        tool.record_answer(session, self.by_id["exec_001"], "Context", "confirmed", "file")
        high = tool.compute_confidence_score(session, self.questions)
        session2 = self.make_session()
        tool.record_answer(session2, self.by_id["exec_001"], "Context", "assumed", "assumed")
        low = tool.compute_confidence_score(session2, self.questions)
        self.assertGreater(high, low)

    def test_leader_packet_readability(self) -> None:
        session = self.make_session()
        tool.record_answer(session, self.by_id["exec_001"], "Context", "confirmed", "verbal")
        tool.record_answer(session, self.by_id["sign_002"], "pending review", "confirmed", "verbal")
        bundle = tool.build_artifact_bundle(session, self.questions)
        packet = bundle["leader_signoff_pack.md"]
        for heading in [
            "## Purpose",
            "## Scope",
            "## What Is Confirmed",
            "## What Remains Assumed",
            "## What Is Blocked",
            "## Approval Requests",
            "## Decisions Required Before Build",
            "## Sign-Off",
        ]:
            self.assertIn(heading, packet)


if __name__ == "__main__":
    unittest.main()
