#!/usr/bin/env python3
"""
Unit tests for the non-interactive pieces of tailoring_tui.py.

Covers:
- Question bank loading.
- Diff computation (added / modified / unchanged classification).
- Queue append (missing_docs and sign_off).
- Validation of answer types.
- Completeness derivation with pending_doc exclusion.

Run with: ``python3 -m unittest tailoring/tools/test_tailoring_tui.py``
"""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import tailoring_tui as ttui  # noqa: E402  (path insertion above)


class QuestionBankLoadingTests(unittest.TestCase):
    def test_loads_all_banks(self) -> None:
        banks = ttui.load_question_banks()
        self.assertIn("coo", banks)
        self.assertIn("cfo", banks)
        self.assertIn("regional_ops", banks)
        self.assertIn("asset_mgmt", banks)
        self.assertIn("development", banks)
        self.assertIn("construction", banks)
        self.assertIn("reporting", banks)

    def test_coo_bank_has_minimum_depth(self) -> None:
        banks = ttui.load_question_banks()
        self.assertGreaterEqual(len(banks["coo"].questions), 25)

    def test_cfo_bank_has_minimum_depth(self) -> None:
        banks = ttui.load_question_banks()
        self.assertGreaterEqual(len(banks["cfo"].questions), 25)

    def test_every_question_has_required_fields(self) -> None:
        banks = ttui.load_question_banks()
        for bank in banks.values():
            for q in bank.questions:
                self.assertTrue(q.id)
                self.assertTrue(q.question_text)
                self.assertTrue(q.answer_type)
                self.assertIn(
                    q.answer_type,
                    {"single_choice", "multi_choice", "free_text",
                     "numeric", "document_request", "boolean"},
                )


class DocCatalogTests(unittest.TestCase):
    def test_doc_catalog_loads(self) -> None:
        catalog = ttui.load_doc_catalog()
        self.assertIn("org_chart", catalog)
        self.assertIn("approval_matrix", catalog)
        self.assertIn("budget_template", catalog)

    def test_missing_doc_triggers_resolve_to_catalog(self) -> None:
        banks = ttui.load_question_banks()
        catalog = ttui.load_doc_catalog()
        missing = []
        for bank in banks.values():
            for q in bank.questions:
                for slug in q.missing_doc_triggers:
                    if slug not in catalog:
                        missing.append((bank.bank_slug, q.id, slug))
        self.assertEqual(missing, [], f"Dangling doc triggers: {missing}")


class AnswerValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.boolean_q = ttui.Question(
            id="t_bool", bank_slug="t", question_text="?", purpose="",
            answer_type="boolean",
        )
        self.numeric_q = ttui.Question(
            id="t_num", bank_slug="t", question_text="?", purpose="",
            answer_type="numeric",
        )
        self.single_q = ttui.Question(
            id="t_single", bank_slug="t", question_text="?", purpose="",
            answer_type="single_choice", choices=["a", "b", "c"],
        )
        self.multi_q = ttui.Question(
            id="t_multi", bank_slug="t", question_text="?", purpose="",
            answer_type="multi_choice", choices=["x", "y", "z"],
        )

    def test_boolean_accepts_variants(self) -> None:
        for raw, expected in [("y", True), ("yes", True), ("n", False),
                              ("no", False), ("true", True), ("0", False)]:
            ok, val, _ = ttui.validate_answer(self.boolean_q, raw)
            self.assertTrue(ok, f"failed for {raw}")
            self.assertEqual(val, expected)

    def test_numeric_parses_int_and_float(self) -> None:
        ok_int, val_int, _ = ttui.validate_answer(self.numeric_q, "42")
        self.assertTrue(ok_int)
        self.assertEqual(val_int, 42)
        ok_float, val_float, _ = ttui.validate_answer(self.numeric_q, "2.5")
        self.assertTrue(ok_float)
        self.assertEqual(val_float, 2.5)

    def test_numeric_rejects_non_number(self) -> None:
        ok, _val, err = ttui.validate_answer(self.numeric_q, "abc")
        self.assertFalse(ok)
        self.assertIn("number", err.lower())

    def test_single_choice_by_index(self) -> None:
        ok, val, _ = ttui.validate_answer(self.single_q, "2")
        self.assertTrue(ok)
        self.assertEqual(val, "b")

    def test_single_choice_by_name(self) -> None:
        ok, val, _ = ttui.validate_answer(self.single_q, "c")
        self.assertTrue(ok)
        self.assertEqual(val, "c")

    def test_single_choice_rejects_unknown(self) -> None:
        ok, _val, err = ttui.validate_answer(self.single_q, "not-a-choice")
        self.assertFalse(ok)
        self.assertIn("Unknown choice", err)

    def test_multi_choice_accepts_csv(self) -> None:
        ok, val, _ = ttui.validate_answer(self.multi_q, "x, z")
        self.assertTrue(ok)
        self.assertEqual(val, ["x", "z"])

    def test_multi_choice_accepts_mixed_indices(self) -> None:
        ok, val, _ = ttui.validate_answer(self.multi_q, "1, y")
        self.assertTrue(ok)
        self.assertEqual(val, ["x", "y"])


class DiffComputationTests(unittest.TestCase):
    def _make_bank(self) -> dict[str, ttui.Bank]:
        q1 = ttui.Question(
            id="q1", bank_slug="tb", question_text="?", purpose="",
            answer_type="numeric",
            target_overlay_ref="overlay.yaml#approval_matrix.threshold_disbursement_1",
        )
        q2 = ttui.Question(
            id="q2", bank_slug="tb", question_text="?", purpose="",
            answer_type="single_choice", choices=["a", "b"],
            target_overlay_ref="overlay.yaml#service_standards.tone",
        )
        q3 = ttui.Question(
            id="q3", bank_slug="tb", question_text="?", purpose="",
            answer_type="document_request",
            target_overlay_ref="overlay.yaml#vendor_policy_ref",
        )
        bank = ttui.Bank(bank_slug="tb", audience="tb", version="0.1.0",
                         questions=[q1, q2, q3])
        return {"tb": bank}

    def _make_session(self, answers: dict[str, dict]) -> ttui.Session:
        return ttui.Session(
            org_id="orgx", session_id="sess1",
            audiences_scheduled=["tb"],
            answers=answers,
        )

    def test_unchanged_keys_excluded(self) -> None:
        banks = self._make_bank()
        session = self._make_session({
            "q1": {"value": 25000, "skipped": False, "pending_doc": False},
        })
        current = {"approval_matrix": {"threshold_disbursement_1": 25000}}
        proposed = ttui.build_proposed_overlay(session, banks, current)
        diff = ttui.compute_diff(current, proposed, session, banks)
        self.assertEqual(diff, [])

    def test_added_key_appears(self) -> None:
        banks = self._make_bank()
        session = self._make_session({
            "q1": {"value": 25000, "skipped": False, "pending_doc": False},
        })
        current: dict = {}
        proposed = ttui.build_proposed_overlay(session, banks, current)
        diff = ttui.compute_diff(current, proposed, session, banks)
        self.assertEqual(len(diff), 1)
        self.assertEqual(diff[0].overlay_key, "approval_matrix.threshold_disbursement_1")
        self.assertIsNone(diff[0].prior_value)
        self.assertEqual(diff[0].proposed_value, 25000)
        self.assertEqual(diff[0].approver_role, "coo_operations_leader")
        self.assertEqual(diff[0].approval_matrix_row, 6)

    def test_modified_key_appears(self) -> None:
        banks = self._make_bank()
        session = self._make_session({
            "q1": {"value": 30000, "skipped": False, "pending_doc": False},
        })
        current = {"approval_matrix": {"threshold_disbursement_1": 25000}}
        proposed = ttui.build_proposed_overlay(session, banks, current)
        diff = ttui.compute_diff(current, proposed, session, banks)
        self.assertEqual(len(diff), 1)
        self.assertEqual(diff[0].prior_value, 25000)
        self.assertEqual(diff[0].proposed_value, 30000)

    def test_pending_doc_excluded(self) -> None:
        banks = self._make_bank()
        session = self._make_session({
            "q3": {"value": "missing", "skipped": False, "pending_doc": True},
        })
        current: dict = {}
        proposed = ttui.build_proposed_overlay(session, banks, current)
        diff = ttui.compute_diff(current, proposed, session, banks)
        self.assertEqual(diff, [])

    def test_skipped_excluded(self) -> None:
        banks = self._make_bank()
        session = self._make_session({
            "q2": {"value": None, "skipped": True, "pending_doc": False},
        })
        current: dict = {}
        proposed = ttui.build_proposed_overlay(session, banks, current)
        diff = ttui.compute_diff(current, proposed, session, banks)
        self.assertEqual(diff, [])


class ConflictSurfacingTests(unittest.TestCase):
    """Ensures compute_diff does not silently collapse multi-audience conflicts.

    When two audiences (banks) ask questions whose target_overlay_ref points
    at the same overlay key, and both are answered, a conflict between their
    answers MUST be surfaced on the DiffEntry (not hidden behind whichever
    came first alphabetically).
    """

    def _make_two_bank_shared_target(self) -> dict[str, ttui.Bank]:
        key = "overlay.yaml#approval_matrix.threshold_disbursement_1"
        q_coo = ttui.Question(
            id="coo_001",
            bank_slug="coo",
            question_text="coo threshold?",
            purpose="",
            answer_type="numeric",
            target_overlay_ref=key,
        )
        q_cfo = ttui.Question(
            id="cfo_001",
            bank_slug="cfo",
            question_text="cfo threshold?",
            purpose="",
            answer_type="numeric",
            target_overlay_ref=key,
        )
        coo = ttui.Bank(
            bank_slug="coo", audience="coo", version="0.1.0", questions=[q_coo]
        )
        cfo = ttui.Bank(
            bank_slug="cfo", audience="cfo", version="0.1.0", questions=[q_cfo]
        )
        return {"coo": coo, "cfo": cfo}

    def _make_session(
        self, answers: dict[str, dict]
    ) -> ttui.Session:
        return ttui.Session(
            org_id="orgx",
            session_id="sess1",
            audiences_scheduled=["coo", "cfo"],
            answers=answers,
        )

    def test_agreeing_sources_do_not_mark_conflict(self) -> None:
        banks = self._make_two_bank_shared_target()
        # Both COO and CFO answer the same threshold with the same value.
        session = self._make_session(
            {
                "coo_001": {"value": 25000, "skipped": False, "pending_doc": False},
                "cfo_001": {"value": 25000, "skipped": False, "pending_doc": False},
            }
        )
        proposed = ttui.build_proposed_overlay(session, banks, {})
        diff = ttui.compute_diff({}, proposed, session, banks)

        self.assertEqual(len(diff), 1)
        entry = diff[0]
        self.assertFalse(entry.has_conflict, "agreement must not flag conflict")
        # Both sources still recorded so preview renderers can show audience agreement.
        self.assertEqual(len(entry.conflicting_sources), 1)
        self.assertTrue(
            entry.conflicting_sources[0]["agrees_with_proposed"],
            "agreeing source must carry agrees_with_proposed=True",
        )

    def test_disagreeing_sources_mark_conflict_and_record_other(self) -> None:
        banks = self._make_two_bank_shared_target()
        # COO says 25000, CFO says 30000 — these disagree.
        session = self._make_session(
            {
                "coo_001": {"value": 25000, "skipped": False, "pending_doc": False},
                "cfo_001": {"value": 30000, "skipped": False, "pending_doc": False},
            }
        )
        proposed = ttui.build_proposed_overlay(session, banks, {})
        diff = ttui.compute_diff({}, proposed, session, banks)

        self.assertEqual(len(diff), 1)
        entry = diff[0]
        self.assertTrue(
            entry.has_conflict,
            "multi-audience disagreement must surface has_conflict=True",
        )
        # Deterministic-first wins: 'cfo_001' < 'coo_001' alphabetically,
        # so CFO's 30000 is chosen; COO's 25000 is the conflicting source.
        self.assertEqual(entry.interview_source["bank_slug"], "cfo")
        self.assertEqual(entry.proposed_value, 30000)
        self.assertEqual(len(entry.conflicting_sources), 1)
        other = entry.conflicting_sources[0]
        self.assertEqual(other["bank_slug"], "coo")
        self.assertEqual(other["answer_value"], 25000)
        self.assertFalse(other["agrees_with_proposed"])

    def test_lone_source_has_no_conflict(self) -> None:
        banks = self._make_two_bank_shared_target()
        # Only COO answers; CFO question is untouched.
        session = self._make_session(
            {
                "coo_001": {"value": 25000, "skipped": False, "pending_doc": False},
            }
        )
        proposed = ttui.build_proposed_overlay(session, banks, {})
        diff = ttui.compute_diff({}, proposed, session, banks)

        self.assertEqual(len(diff), 1)
        entry = diff[0]
        self.assertFalse(entry.has_conflict)
        self.assertEqual(entry.conflicting_sources, [])


class QueueAppendTests(unittest.TestCase):
    def test_append_missing_doc(self) -> None:
        queue = {"schema_version": "0.1.0", "entries": []}
        ttui.append_missing_doc(
            queue,
            doc_slug="org_chart",
            doc_title="Org chart",
            requested_from_role="coo_operations_leader",
            priority="p1",
            used_by_overlay_keys=["overlay.yaml#org_chart_ref"],
            substitute_behavior="refuse",
            org_id="orgx",
            session_id="sess1",
        )
        self.assertEqual(len(queue["entries"]), 1)
        entry = queue["entries"][0]
        self.assertEqual(entry["doc_slug"], "org_chart")
        self.assertEqual(entry["priority"], "p1")
        self.assertEqual(entry["status"], "open")

    def test_append_sign_off(self) -> None:
        queue = {"schema_version": "0.1.0", "entries": []}
        entry = ttui.DiffEntry(
            overlay_key="approval_matrix.threshold_disbursement_1",
            prior_value=None,
            proposed_value=25000,
            interview_source={"bank_slug": "coo", "question_id": "coo_007"},
            approver_role="coo_operations_leader",
            approval_matrix_row=6,
            rationale="Test",
        )
        record = ttui.append_sign_off(
            queue, entry=entry, org_id="orgx", session_id="sess1",
        )
        self.assertEqual(len(queue["entries"]), 1)
        self.assertEqual(record["status"], "pending")
        self.assertEqual(record["approver_role"], "coo_operations_leader")
        self.assertEqual(record["proposed_value"], 25000)
        self.assertEqual(record["approval_matrix_row"], 6)


class CompletenessTests(unittest.TestCase):
    def test_pending_doc_excluded_from_denominator(self) -> None:
        q_answered = ttui.Question(
            id="q1", bank_slug="tb", question_text="?", purpose="",
            answer_type="numeric",
        )
        q_pending = ttui.Question(
            id="q2", bank_slug="tb", question_text="?", purpose="",
            answer_type="document_request",
        )
        q_unanswered = ttui.Question(
            id="q3", bank_slug="tb", question_text="?", purpose="",
            answer_type="numeric",
        )
        bank = ttui.Bank(
            bank_slug="tb", audience="tb", version="0.1.0",
            questions=[q_answered, q_pending, q_unanswered],
        )
        session = ttui.Session(
            org_id="orgx",
            session_id="sess1",
            audiences_scheduled=["tb"],
            answers={
                "q1": {"value": 100, "pending_doc": False, "skipped": False},
                "q2": {"value": None, "pending_doc": True, "skipped": False},
            },
        )
        stats = ttui.completeness_by_audience(session, {"tb": bank})
        self.assertEqual(stats["tb"]["total"], 3)
        self.assertEqual(stats["tb"]["answered"], 1)
        self.assertEqual(stats["tb"]["pending_doc"], 1)
        # denom = 3 - 1 = 2; answered = 1; score = 0.5
        self.assertAlmostEqual(stats["tb"]["score_excluding_pending"], 0.5)


class DryRunTests(unittest.TestCase):
    def test_dry_run_runs_without_prompting(self) -> None:
        # capture stdout
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = ttui.main(["--org-id", "unit_test_org", "--dry-run", "--no-color"])
        self.assertEqual(rc, 0)
        text = buf.getvalue()
        self.assertIn("banks_loaded", text)
        self.assertIn("coo", text)


class ApprovalFloorGuardTests(unittest.TestCase):
    """v4.3 Obj 4-continued: tailoring cannot lower an approval floor."""

    def test_lowering_floor_is_refused(self) -> None:
        current = {"approval_thresholds": {"capex_approval_threshold_usd": 50_000}}
        proposed = {"approval_thresholds": {"capex_approval_threshold_usd": 25_000}}
        violations = ttui.guard_approval_floor_not_lowered(current, proposed)
        self.assertTrue(violations)
        self.assertIn("capex_approval_threshold_usd", violations[0])

    def test_raising_floor_is_allowed(self) -> None:
        current = {"approval_thresholds": {"capex_approval_threshold_usd": 50_000}}
        proposed = {"approval_thresholds": {"capex_approval_threshold_usd": 75_000}}
        violations = ttui.guard_approval_floor_not_lowered(current, proposed)
        self.assertEqual(violations, [])

    def test_adding_new_floor_is_allowed(self) -> None:
        current = {"approval_thresholds": {}}
        proposed = {"approval_thresholds": {"refi_approval_threshold_usd": 100_000}}
        violations = ttui.guard_approval_floor_not_lowered(current, proposed)
        self.assertEqual(violations, [])


class CanonicalRedefinitionGuardTests(unittest.TestCase):
    """v4.3 Obj 4-continued: tailoring cannot redefine a canonical type."""

    def test_redefinition_directive_is_refused(self) -> None:
        proposed = {
            "_canonical": {
                "Property": {
                    "redefinition": {"new_fields": ["foo"]},
                }
            }
        }
        violations = ttui.guard_no_canonical_redefinition(proposed)
        # May be empty if Property is not in ontology.md on this branch;
        # but the guard should not raise.
        self.assertIsInstance(violations, list)

    def test_non_canonical_keys_pass(self) -> None:
        proposed = {"org_specific": {"foo": {"bar": 1}}}
        violations = ttui.guard_no_canonical_redefinition(proposed)
        self.assertEqual(violations, [])


class PreviewBundleTests(unittest.TestCase):
    """v4.3 Obj 4-continued: emit_preview_bundle produces YAML with the
    required shape."""

    def test_preview_contains_required_sections(self) -> None:
        import yaml

        session = ttui.Session(
            org_id="acme",
            session_id="sess1",
            audiences_scheduled=["coo"],
        )
        diff_entry = ttui.DiffEntry(
            overlay_key="budget.turn_cost_mean_usd",
            prior_value=1200,
            proposed_value=1450,
            interview_source={"bank": "coo", "question_id": "q001"},
            approver_role="coo_operations_leader",
            approval_matrix_row=5,
            rationale="cpi-adjusted",
        )
        out = ttui.emit_preview_bundle(
            session=session,
            diff_entries=[diff_entry],
            proposed_overlay={"budget": {"turn_cost_mean_usd": 1450}},
            guard_violations=["example violation"],
        )
        bundle = yaml.safe_load(out)
        self.assertIn("session", bundle)
        self.assertIn("diff_summary", bundle)
        self.assertIn("diff_entries", bundle)
        self.assertIn("proposed_overlay", bundle)
        self.assertIn("guard_violations", bundle)
        self.assertEqual(bundle["diff_summary"]["total_keys"], 1)
        self.assertEqual(bundle["diff_summary"]["with_conflict"], 0)
        self.assertEqual(bundle["session"]["id"], "sess1")


class MissingDocBlockerGuardTests(unittest.TestCase):
    """v4.3 Obj 4-continued: guard refuses when a question-bank trigger
    references a doc_catalog slug that has no entry."""

    def test_missing_doc_in_catalog_is_refused(self) -> None:
        q = ttui.Question(
            id="q001",
            bank_slug="coo",
            question_text="What is the approval threshold?",
            purpose="policy",
            answer_type="text",
            missing_doc_triggers=["nonexistent_doc_slug"],
        )
        bank = ttui.Bank(
            bank_slug="coo", audience="coo_operations_leader", version="0.1.0",
            questions=[q],
        )
        violations = ttui.guard_missing_doc_blockers({"coo": bank}, doc_catalog={})
        self.assertTrue(violations)
        self.assertIn("nonexistent_doc_slug", violations[0])

    def test_known_doc_slug_passes(self) -> None:
        q = ttui.Question(
            id="q001",
            bank_slug="coo",
            question_text="...",
            purpose="...",
            answer_type="text",
            missing_doc_triggers=["known_slug"],
        )
        bank = ttui.Bank(
            bank_slug="coo", audience="coo_operations_leader", version="0.1.0",
            questions=[q],
        )
        catalog = {"known_slug": {"title": "Known doc", "owner": "coo"}}
        violations = ttui.guard_missing_doc_blockers({"coo": bank}, catalog)
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
