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


if __name__ == "__main__":
    unittest.main()
