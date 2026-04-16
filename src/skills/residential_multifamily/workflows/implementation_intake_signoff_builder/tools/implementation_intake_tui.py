#!/usr/bin/env python3
"""
Implementation intake and leader sign-off terminal helper.

The helper is intentionally lightweight:

- Loads the workflow question bank and example-friendly schemas.
- Persists session state under workflows/implementation_intake_signoff_builder/sessions/.
- Supports resume, preview, and minimal interactive intake.
- Computes progress, confidence, blockers, and next-question order.
- Renders the implementation intake packet, leader sign-off packet, and action queue.
- Refuses to store obvious secret-like values.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover
    print("PyYAML is required.", file=sys.stderr)
    raise


ROOT = Path(__file__).resolve().parent.parent
QUESTION_BANK_PATH = ROOT / "question_bank.yaml"
SESSION_SCHEMA_PATH = ROOT / "schemas" / "session_state_schema.yaml"
INTAKE_TEMPLATE_PATH = ROOT / "templates" / "implementation_intake_packet_template.md"
SIGNOFF_TEMPLATE_PATH = ROOT / "templates" / "signoff_packet_template.md"
ACTION_QUEUE_TEMPLATE_PATH = ROOT / "templates" / "action_queue_template.md"
SESSIONS_DIR = ROOT / "sessions"

ANSWER_WEIGHTS = {
    "confirmed_by_artifact": 1.00,
    "confirmed_by_export": 0.95,
    "confirmed_by_document": 0.95,
    "confirmed_by_screenshot": 0.90,
    "confirmed_verbal": 0.70,
    "inferred": 0.50,
    "assumed": 0.30,
    "missing": 0.00,
    "blocked": 0.00,
    "conflicting": 0.10,
}

VALIDATION_PENALTIES = {
    "received_not_reviewed": 0.10,
    "reviewed_incomplete": 0.15,
    "reviewed_sufficient": 0.00,
    "conflicting_with_prior": 0.20,
}

SECRET_PATTERNS = [
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._\-]{16,}\b"),
    re.compile(r"(?i)\b(api[_-]?key|token|secret|password)\b\s*[:=]\s*\S{8,}"),
]


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def dump_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=False)


def load_question_bank(path: Path = QUESTION_BANK_PATH) -> dict[str, Any]:
    return load_yaml(path)


def question_index(bank: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {question["question_id"]: question for question in bank.get("questions", [])}


def contains_secret(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    if len(value.strip()) < 8:
        return False
    return any(pattern.search(value) for pattern in SECRET_PATTERNS)


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _normalize_string_list(values: list[Any]) -> list[str]:
    return [str(value).strip().lower() for value in values if str(value).strip()]


def _answer_value(answers: dict[str, Any], question_id: str) -> Any:
    return (answers.get(question_id) or {}).get("value")


def _answer_matches(rule: dict[str, Any], answers: dict[str, Any]) -> bool:
    value = _answer_value(answers, str(rule.get("question_id") or ""))
    value_list = _normalize_string_list(_as_list(value))
    equals_any = _normalize_string_list(rule.get("equals_any") or [])
    contains_any = _normalize_string_list(rule.get("contains_any") or [])
    if equals_any and any(item in equals_any for item in value_list):
        return True
    if contains_any and any(item in value_list for item in contains_any):
        return True
    return False


def question_is_active(
    question: dict[str, Any],
    context: dict[str, Any],
    answers: dict[str, Any],
) -> bool:
    trigger = question.get("trigger_condition") or {}
    mode = str(context.get("mode") or context.get("current_mode") or "").strip()
    role = str(context.get("role") or "").strip()
    management_mode = str(context.get("management_mode") or "").strip()
    systems = _normalize_string_list(context.get("systems_in_scope") or [])

    if trigger.get("modes_any") and mode not in trigger["modes_any"]:
        return False
    if trigger.get("roles_any") and role not in trigger["roles_any"]:
        return False
    if trigger.get("management_modes_any") and management_mode not in trigger["management_modes_any"]:
        return False
    if trigger.get("systems_any"):
        required = _normalize_string_list(trigger["systems_any"])
        if not set(systems).intersection(required):
            return False
    for prerequisite in trigger.get("requires_answers_all") or []:
        value = _answer_value(answers, str(prerequisite))
        if value in (None, "", []):
            return False
    for rule in trigger.get("requires_answer_values") or []:
        if not _answer_matches(rule, answers):
            return False
    return True


def should_skip(
    question: dict[str, Any],
    answers: dict[str, Any],
    context: dict[str, Any],
) -> bool:
    skip = question.get("skip_logic") or {}
    if skip.get("skip_if_answered"):
        existing = answers.get(question["question_id"]) or {}
        if existing.get("value") not in (None, "", []):
            return True
    for rule in skip.get("skip_if_answer_values") or []:
        if _answer_matches(rule, answers):
            return True
    for rule in skip.get("skip_if_context_values") or []:
        field = str(rule.get("field") or "")
        value = context.get(field)
        normalized = _normalize_string_list(_as_list(value))
        equals_any = _normalize_string_list(rule.get("equals_any") or [])
        excludes_all = _normalize_string_list(rule.get("excludes_all") or [])
        if equals_any and any(item in equals_any for item in normalized):
            return True
        if excludes_all and not set(normalized).intersection(excludes_all):
            return True
    return False


def follow_up_question_ids(question: dict[str, Any], answer_value: Any) -> list[str]:
    rules = ((question.get("follow_up_logic") or {}).get("rules")) or []
    normalized = _normalize_string_list(_as_list(answer_value))
    out: list[str] = []
    for rule in rules:
        matched = False
        if rule.get("when_answer_present") and answer_value not in (None, "", []):
            matched = True
        if rule.get("when_answer_missing_or_empty") and answer_value in (None, "", []):
            matched = True
        if rule.get("when_answer_equals") and str(answer_value) == str(rule["when_answer_equals"]):
            matched = True
        if rule.get("when_answer_conflicting") and str(answer_value).strip().lower() == "conflicting":
            matched = True
        if rule.get("when_answer_contains_any"):
            targets = _normalize_string_list(rule["when_answer_contains_any"])
            if set(normalized).intersection(targets):
                matched = True
        if matched:
            for question_id in rule.get("enqueue_question_ids") or []:
                if question_id not in out:
                    out.append(question_id)
    return out


def normalize_answer(question: dict[str, Any], raw: str) -> Any:
    if contains_secret(raw):
        raise ValueError("Refusing to store an actual secret. Capture owner, method, or approval path only.")
    answer_type = str(question.get("expected_answer_type") or "paragraph")
    if answer_type in {"multi_select", "record_list", "file_inventory", "schedule_table"}:
        return [item.strip() for item in raw.split(",") if item.strip()]
    return raw.strip()


def score_question_confidence(question_id: str, answer: dict[str, Any], evidence_items: list[dict[str, Any]]) -> float:
    status = str(answer.get("evidence_status") or "assumed")
    score = ANSWER_WEIGHTS.get(status, 0.0)
    related = [item for item in evidence_items if question_id in (item.get("related_questions") or [])]
    for item in related:
        validation_status = str(item.get("validation_status") or "received_not_reviewed")
        score -= VALIDATION_PENALTIES.get(validation_status, 0.0)
        source_system = str(item.get("source_system") or "").lower()
        received_from = str(item.get("received_from") or "").lower()
        if source_system == "third_party_manager_submission" or "third-party manager" in received_from:
            score -= 0.15
    return max(0.0, min(1.0, score))


def compute_section_progress(bank: dict[str, Any], state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    context = copy.deepcopy(state.get("context") or {})
    context.setdefault("mode", state.get("current_mode"))
    answers = state.get("answers") or {}
    evidence_items = state.get("evidence_items") or []
    sections: dict[str, dict[str, Any]] = {}
    for question in bank.get("questions") or []:
        if not question_is_active(question, context, answers):
            continue
        if should_skip(question, answers, context):
            continue
        section = str(question.get("section") or "unsectioned")
        bucket = sections.setdefault(
            section,
            {
                "total": 0,
                "answered": 0,
                "blocked": 0,
                "assumed": 0,
                "confidence": 0.0,
            },
        )
        bucket["total"] += 1
        answer = answers.get(question["question_id"])
        if not answer:
            continue
        bucket["answered"] += 1
        status = str(answer.get("evidence_status") or "assumed")
        if status in {"blocked", "missing", "conflicting"}:
            bucket["blocked"] += 1
        if status in {"assumed", "inferred", "confirmed_verbal"}:
            bucket["assumed"] += 1
        bucket["confidence"] += score_question_confidence(question["question_id"], answer, evidence_items)
    for values in sections.values():
        if values["answered"]:
            values["confidence"] = round(values["confidence"] / values["answered"], 2)
        else:
            values["confidence"] = 0.0
    return sections


def compute_overall_completion(bank: dict[str, Any], state: dict[str, Any]) -> int:
    sections = compute_section_progress(bank, state)
    total = sum(section["total"] for section in sections.values())
    answered = sum(section["answered"] for section in sections.values())
    if not total:
        return 0
    return int(round((answered / total) * 100))


def collect_blockers(state: dict[str, Any], bank: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    blockers = list(state.get("blockers") or [])
    answers = state.get("answers") or {}
    if bank is not None:
        index = question_index(bank)
        for question_id, answer in answers.items():
            status = str(answer.get("evidence_status") or "")
            if status not in {"missing", "blocked", "conflicting"}:
                continue
            question = index.get(question_id, {})
            blockers.append(
                {
                    "blocker_id": f"derived_{question_id}",
                    "description": f"{question.get('question_text', question_id)}",
                    "severity": question.get("severity_if_unanswered", "medium"),
                    "impacted_area": question.get("section", "unknown"),
                    "owner": "unassigned",
                    "requested_from": "unassigned",
                    "date_requested": "",
                    "follow_up_due": "",
                    "status": status,
                }
            )
    deduped: dict[str, dict[str, Any]] = {}
    for blocker in blockers:
        deduped[str(blocker.get("blocker_id") or blocker.get("description"))] = blocker
    return list(deduped.values())


def collect_missing_docs(state: dict[str, Any], bank: dict[str, Any]) -> list[dict[str, Any]]:
    missing: list[dict[str, Any]] = []
    answers = state.get("answers") or {}
    index = question_index(bank)
    for question_id, answer in answers.items():
        status = str(answer.get("evidence_status") or "")
        if status not in {"missing", "blocked"}:
            continue
        question = index.get(question_id, {})
        missing.append(
            {
                "question_id": question_id,
                "section": question.get("section", "unknown"),
                "evidence_requested": question.get("evidence_requested") or [],
                "severity": question.get("severity_if_unanswered", "medium"),
            }
        )
    return missing


def detect_conflicts(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: dict[tuple[str, str], tuple[Any, Any, Any]] = {}
    conflicts: list[dict[str, Any]] = []
    for record in records:
        entity = str(record.get("canonical_entity") or record.get("subject_area") or "")
        source = str(record.get("source_system") or record.get("primary_source") or "")
        key = (entity, source)
        signature = (
            record.get("preferred_match_key"),
            record.get("primary_source"),
            record.get("effective_date_rule"),
        )
        if key in seen and seen[key] != signature:
            conflicts.append(
                {
                    "entity": entity,
                    "source": source,
                    "prior_signature": seen[key],
                    "new_signature": signature,
                }
            )
        else:
            seen[key] = signature
    return conflicts


def next_question_ids(bank: dict[str, Any], state: dict[str, Any]) -> list[str]:
    context = copy.deepcopy(state.get("context") or {})
    context.setdefault("mode", state.get("current_mode"))
    answers = state.get("answers") or {}
    index = question_index(bank)
    follow_ups: list[str] = []
    for question_id, answer in answers.items():
        question = index.get(question_id)
        if not question:
            continue
        for follow_up in follow_up_question_ids(question, answer.get("value")):
            if follow_up not in follow_ups:
                follow_ups.append(follow_up)

    ordered: list[str] = []
    for question_id in follow_ups + [question["question_id"] for question in bank.get("questions") or []]:
        if question_id in ordered:
            continue
        question = index.get(question_id)
        if not question:
            continue
        if question_id in answers and (answers[question_id] or {}).get("value") not in (None, "", []):
            continue
        if not question_is_active(question, context, answers):
            continue
        if should_skip(question, answers, context):
            continue
        ordered.append(question_id)
    return ordered


def _bullet_list(items: list[str]) -> str:
    if not items:
        return "- None recorded"
    return "\n".join(f"- {item}" for item in items)


def _owners_and_dates(items: list[dict[str, Any]]) -> str:
    if not items:
        return "- No owners recorded"
    lines = []
    for item in items:
        owner = item.get("owner", "TBD")
        role = item.get("role", "TBD")
        due_date = item.get("due_date", "TBD")
        scope = item.get("item", item.get("scope", "TBD"))
        lines.append(f"- {owner} ({role}) by {due_date}: {scope}")
    return "\n".join(lines)


def _load_template(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _render_template(text: str, replacements: dict[str, str]) -> str:
    for key, value in replacements.items():
        text = text.replace(f"{{{{{key}}}}}", value)
    return text


def build_packet_context(state: dict[str, Any], bank: dict[str, Any]) -> dict[str, str]:
    answers = state.get("answers") or {}
    objective = str((answers.get("exec_objective") or {}).get("value") or state.get("recommendation") or "")
    systems = [str(item) for item in (state.get("context") or {}).get("systems_in_scope") or []]
    environments = [str(item) for item in (state.get("context") or {}).get("environments_in_scope") or []]
    confirmed_facts = []
    unresolved_assumptions = [item.get("statement", "") for item in state.get("assumptions") or []]
    for question_id, answer in answers.items():
        status = str(answer.get("evidence_status") or "")
        if status.startswith("confirmed"):
            confirmed_facts.append(str(answer.get("value")))
        elif status in {"assumed", "inferred"} and answer.get("value"):
            unresolved_assumptions.append(str(answer.get("value")))
    blockers = [blocker.get("description", "") for blocker in collect_blockers(state, bank)]
    top_risks = [str(item) for item in (state.get("top_risks") or [])[:3]]
    decisions = [str(item) for item in state.get("decisions_requested") or []]
    approvals = [str(item) for item in state.get("approvals_requested") or []]
    owners = [dict(item) for item in state.get("owners_and_dates") or []]

    section_progress = compute_section_progress(bank, state)
    confidence_values = [section["confidence"] for section in section_progress.values() if section["total"]]
    current_confidence = "low"
    if confidence_values:
        average = sum(confidence_values) / len(confidence_values)
        if average >= 0.85:
            current_confidence = "high"
        elif average >= 0.60:
            current_confidence = "medium"
    readiness_summary = f"Overall confidence is {current_confidence}. Completion is {compute_overall_completion(bank, state)} percent."
    approval_section = "\n".join(
        [
            f"- Approval status: {state.get('status', 'draft')}",
            "- Reviewer name:",
            "- Reviewer role:",
            "- Review date:",
            "- Approval notes:",
            "- Conditions if any:",
        ]
    )
    return {
        "document_purpose": "Authorize or reject the move from planning into build execution using evidence-backed intake facts.",
        "implementation_objective": objective,
        "systems_and_environments": _bullet_list(systems + environments),
        "systems_in_scope": _bullet_list(systems),
        "environments_in_scope": _bullet_list(environments),
        "current_confidence": current_confidence,
        "key_blockers": _bullet_list(blockers),
        "main_dependencies": _bullet_list([item.get("description", "") for item in collect_missing_docs(state, bank)]),
        "readiness_summary": readiness_summary,
        "immediate_next_actions": _owners_and_dates(owners),
        "confirmed_facts": _bullet_list([fact for fact in confirmed_facts if fact]),
        "unresolved_assumptions": _bullet_list([item for item in unresolved_assumptions if item]),
        "blocked_items": _bullet_list([item for item in blockers if item]),
        "top_three_risks": _bullet_list(top_risks),
        "decisions_requested": _bullet_list(decisions),
        "approvals_requested": _bullet_list(approvals),
        "owners_and_dates": _owners_and_dates(owners),
        "recommendation": str(state.get("recommendation") or ""),
        "approval_section": approval_section,
    }


def render_implementation_intake_packet(state: dict[str, Any], bank: dict[str, Any], template_path: Path = INTAKE_TEMPLATE_PATH) -> str:
    context = build_packet_context(state, bank)
    return _render_template(_load_template(template_path), context)


def render_leader_signoff_packet(state: dict[str, Any], bank: dict[str, Any], template_path: Path = SIGNOFF_TEMPLATE_PATH) -> str:
    context = build_packet_context(state, bank)
    return _render_template(_load_template(template_path), context)


def build_action_queue(state: dict[str, Any]) -> dict[str, list[dict[str, str]]]:
    queue: dict[str, Any] = {
        "schema_version": "0.1.0",
        "business": [],
        "technical": [],
        "data": [],
        "reporting": [],
        "controls": [],
        "dependencies": [],
    }
    for owner_record in state.get("owners_and_dates") or []:
        item_text = str(owner_record.get("item") or "")
        lower = item_text.lower()
        record = {
            "description": item_text,
            "owner": str(owner_record.get("owner") or "TBD"),
            "due_date": str(owner_record.get("due_date") or "TBD"),
            "priority": "high",
            "blocking_dependency": "yes" if "missing" in lower or "resolve" in lower or "obtain" in lower else "no",
        }
        if "dictionary" in lower or "report" in lower or "calendar" in lower:
            queue["reporting"].append(record)
        elif "crosswalk" in lower or "mapping" in lower or "data" in lower or "bridge" in lower:
            queue["data"].append(record)
        elif "approval" in lower or "override" in lower:
            queue["controls"].append(record)
        elif "access" in lower or "export" in lower or "systems" in lower:
            queue["technical"].append(record)
        elif "manager" in lower or "backup" in lower or "dependency" in lower:
            queue["dependencies"].append(record)
        else:
            queue["business"].append(record)
    return queue


def _render_action_items(items: list[dict[str, str]]) -> str:
    if not items:
        return "- None recorded"
    return "\n".join(
        f"- {item['description']} Owner: {item['owner']}. Due: {item['due_date']}. Blocking dependency: {item['blocking_dependency']}."
        for item in items
    )


def render_action_queue(state: dict[str, Any], template_path: Path = ACTION_QUEUE_TEMPLATE_PATH) -> str:
    queue = build_action_queue(state)
    replacements = {
        "business_actions": _render_action_items(queue["business"]),
        "technical_actions": _render_action_items(queue["technical"]),
        "data_actions": _render_action_items(queue["data"]),
        "reporting_actions": _render_action_items(queue["reporting"]),
        "controls_actions": _render_action_items(queue["controls"]),
        "dependency_actions": _render_action_items(queue["dependencies"]),
    }
    return _render_template(_load_template(template_path), replacements)


def session_path(engagement_id: str, session_id: str) -> Path:
    return SESSIONS_DIR / engagement_id / f"{session_id}.yaml"


def initialize_session(
    engagement_id: str,
    session_id: str,
    mode: str,
    role: str,
    management_mode: str,
    systems: list[str],
) -> dict[str, Any]:
    return {
        "schema_version": "0.1.0",
        "engagement_id": engagement_id,
        "session_id": session_id,
        "version": "0.1.0",
        "status": "draft",
        "current_mode": mode,
        "progress": {
            "completion_percent": 0,
            "current_section": "objective_scope",
            "answered_questions": 0,
            "total_questions": 0,
        },
        "context": {
            "role": role,
            "management_mode": management_mode,
            "systems_in_scope": systems,
            "environments_in_scope": [],
        },
        "answers": {},
        "evidence_items": [],
        "blockers": [],
        "assumptions": [],
        "decisions_requested": [],
        "approvals_requested": [],
        "top_risks": [],
        "owners_and_dates": [],
        "recommendation": "",
    }


def update_progress(state: dict[str, Any], bank: dict[str, Any]) -> None:
    sections = compute_section_progress(bank, state)
    state["progress"]["completion_percent"] = compute_overall_completion(bank, state)
    state["progress"]["answered_questions"] = sum(section["answered"] for section in sections.values())
    state["progress"]["total_questions"] = sum(section["total"] for section in sections.values())
    queue = next_question_ids(bank, state)
    if queue:
        current_question = question_index(bank)[queue[0]]
        state["progress"]["current_section"] = current_question.get("section", "objective_scope")


def write_preview_artifacts(state: dict[str, Any], bank: dict[str, Any]) -> None:
    base = SESSIONS_DIR / state["engagement_id"]
    base.mkdir(parents=True, exist_ok=True)
    preview_prefix = base / state["session_id"]
    (preview_prefix.with_name(f"{state['session_id']}__preview.md")).write_text(
        render_implementation_intake_packet(state, bank),
        encoding="utf-8",
    )
    (preview_prefix.with_name(f"{state['session_id']}__leader_signoff.md")).write_text(
        render_leader_signoff_packet(state, bank),
        encoding="utf-8",
    )
    (preview_prefix.with_name(f"{state['session_id']}__action_queue.md")).write_text(
        render_action_queue(state),
        encoding="utf-8",
    )


def render_dashboard(state: dict[str, Any], bank: dict[str, Any]) -> str:
    sections = compute_section_progress(bank, state)
    lines = [
        f"Engagement: {state['engagement_id']}",
        f"Session: {state['session_id']}",
        f"Mode: {state['current_mode']}",
        f"Completion: {state['progress'].get('completion_percent', 0)} percent",
        "",
        "Sections:",
    ]
    for section, values in sections.items():
        lines.append(
            f"- {section}: answered {values['answered']} of {values['total']}, blocked {values['blocked']}, confidence {values['confidence']:.2f}"
        )
    lines.append("")
    lines.append(f"Open blockers: {len(collect_blockers(state, bank))}")
    return "\n".join(lines)


def prompt_for_answer(question: dict[str, Any]) -> tuple[Any, str]:
    print("")
    print(question["question_text"])
    print(f"Why it matters: {question['why_this_matters']}")
    raw = input("Answer (:skip, :preview, :quit): ").strip()
    return raw, raw


def run_interactive(state: dict[str, Any], state_path: Path) -> None:
    bank = load_question_bank()
    index = question_index(bank)
    while True:
        update_progress(state, bank)
        queue = next_question_ids(bank, state)
        print("")
        print(render_dashboard(state, bank))
        if not queue:
            print("")
            print("No active questions remain for the current mode.")
            print(render_leader_signoff_packet(state, bank))
            break
        question = index[queue[0]]
        raw, command = prompt_for_answer(question)
        if command == ":quit":
            dump_yaml(state_path, state)
            print(f"Saved session to {state_path}")
            return
        if command == ":preview":
            print("")
            print(render_implementation_intake_packet(state, bank))
            print("")
            print(render_leader_signoff_packet(state, bank))
            continue
        if command == ":skip":
            state["answers"][question["question_id"]] = {
                "value": "",
                "evidence_status": "missing",
            }
            dump_yaml(state_path, state)
            continue
        try:
            normalized = normalize_answer(question, raw)
        except ValueError as exc:
            print(str(exc))
            continue
        evidence_status = input(
            "Evidence status [confirmed_verbal, confirmed_by_document, confirmed_by_export, assumed, missing, blocked, conflicting]: "
        ).strip() or "confirmed_verbal"
        if evidence_status not in ANSWER_WEIGHTS:
            print("Unknown evidence status.")
            continue
        state["answers"][question["question_id"]] = {
            "value": normalized,
            "evidence_status": evidence_status,
        }
        dump_yaml(state_path, state)
        write_preview_artifacts(state, bank)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Implementation intake helper")
    parser.add_argument("--engagement-id", default="demo_engagement")
    parser.add_argument("--session-id", default=f"session_{dt.datetime.utcnow().strftime('%Y%m%d%H%M%S')}")
    parser.add_argument("--mode", default="executive_overview")
    parser.add_argument("--role", default="implementation_pm")
    parser.add_argument("--management-mode", default="owner_oversight")
    parser.add_argument("--systems", default="appfolio,sage_intacct,procore,dealpath")
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--session-file", default="")
    parser.add_argument("--new", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    bank = load_question_bank()
    if args.session_file:
        state_path = Path(args.session_file)
    else:
        state_path = session_path(args.engagement_id, args.session_id)
    if state_path.exists() and not args.new:
        state = load_yaml(state_path)
    else:
        state = initialize_session(
            engagement_id=args.engagement_id,
            session_id=args.session_id,
            mode=args.mode,
            role=args.role,
            management_mode=args.management_mode,
            systems=[item.strip() for item in args.systems.split(",") if item.strip()],
        )
    state.setdefault("context", {})
    state["current_mode"] = args.mode or state.get("current_mode", "executive_overview")
    state["context"]["role"] = args.role or state["context"].get("role", "implementation_pm")
    state["context"]["management_mode"] = args.management_mode or state["context"].get("management_mode", "owner_oversight")
    if args.systems:
        state["context"]["systems_in_scope"] = [item.strip() for item in args.systems.split(",") if item.strip()]
    update_progress(state, bank)
    dump_yaml(state_path, state)
    write_preview_artifacts(state, bank)
    if args.preview:
        print(render_dashboard(state, bank))
        print("")
        print(render_implementation_intake_packet(state, bank))
        print("")
        print(render_leader_signoff_packet(state, bank))
        print("")
        print(render_action_queue(state))
        return 0
    run_interactive(state, state_path)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
