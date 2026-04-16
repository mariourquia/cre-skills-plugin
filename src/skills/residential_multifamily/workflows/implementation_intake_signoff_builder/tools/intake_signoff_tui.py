#!/usr/bin/env python3
"""
Implementation intake and sign-off TUI.

This workflow-local tool provides:
- staged question sequencing by mode
- structured YAML validation against workflow-local schemas
- evidence tagging and confidence scoring
- blocker, missing-doc, and conflict detection
- session save / resume
- markdown preview generation for the required output artifacts

Dependencies: Python stdlib + PyYAML.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import os
import re
import sys
import textwrap
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover
    print("ERROR: PyYAML is required. Install with `pip install pyyaml`.", file=sys.stderr)
    sys.exit(2)


PACK_ROOT = Path(__file__).resolve().parent.parent
QUESTION_BANK_PATH = PACK_ROOT / "question_bank.yaml"
SCHEMAS_DIR = PACK_ROOT / "schemas"
SESSIONS_DIR = PACK_ROOT / "sessions"

REQUIRED_QUESTION_IDS = [
    "exec_001",
    "exec_002",
    "src_001",
    "field_001",
    "map_001",
    "report_001",
    "ctrl_001",
    "docs_001",
    "sign_001",
    "sign_002",
]

ALLOWED_EVIDENCE_STATUS = {"confirmed", "assumed", "inferred", "missing", "blocked", "conflicting"}
ALLOWED_EVIDENCE_DETAIL = {"file", "screenshot", "verbal", "assumed", "inferred", "missing", "blocked", "conflicting"}
CONFIRMING_DETAILS = {"file", "screenshot", "verbal"}

CONFIDENCE_IMPACT_WEIGHT = {"high": 1.0, "medium": 0.6, "low": 0.3}
EVIDENCE_WEIGHT = {
    ("confirmed", "file"): 1.0,
    ("confirmed", "screenshot"): 0.9,
    ("confirmed", "verbal"): 0.75,
    ("assumed", "assumed"): 0.35,
    ("inferred", "inferred"): 0.5,
    ("missing", "missing"): 0.0,
    ("blocked", "blocked"): 0.0,
    ("conflicting", "conflicting"): 0.1,
}

STRUCTURED_CONFLICT_KEYS = {
    "source_inventory": ("source_id",),
    "credentials_access_model": ("source_id",),
    "export_field_inventory": ("source_id", "object_name", "export_name"),
    "crosswalk_rules": ("canonical_entity", "source_system"),
    "reporting_calendar": ("cadence_id",),
    "approval_controls": ("control_id",),
}


class Ansi:
    def __init__(self, enabled: bool | None = None) -> None:
        if enabled is None:
            enabled = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None
        self.enabled = bool(enabled)

    def _wrap(self, code: str, text: str) -> str:
        if not self.enabled:
            return text
        return f"\x1b[{code}m{text}\x1b[0m"

    def bold(self, text: str) -> str:
        return self._wrap("1", text)

    def cyan(self, text: str) -> str:
        return self._wrap("36", text)

    def yellow(self, text: str) -> str:
        return self._wrap("33", text)

    def red(self, text: str) -> str:
        return self._wrap("31", text)

    def green(self, text: str) -> str:
        return self._wrap("32", text)


ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _visible_len(s: str) -> int:
    return len(ANSI_RE.sub("", s))


def render_progress_bar(completed: int, total: int, width: int = 28) -> str:
    if total <= 0:
        filled = 0
    else:
        filled = int(round((completed / total) * width))
    return "[" + ("#" * filled) + ("-" * (width - filled)) + f"] {completed}/{total}"


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def safe_load_yaml(path: Path) -> Any:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def safe_dump_yaml(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(value, f, sort_keys=False, default_flow_style=False, allow_unicode=True)


def validate_against_schema(instance: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    errors: list[str] = []
    if schema is None:
        return errors

    if "const" in schema and instance != schema["const"]:
        return [f"{path}: expected const {schema['const']!r}, got {instance!r}"]

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value {instance!r} not in enum {schema['enum']}")

    expected_type = schema.get("type")
    if expected_type == "object":
        if not isinstance(instance, dict):
            return [f"{path}: expected object, got {type(instance).__name__}"]
        required = schema.get("required", []) or []
        properties = schema.get("properties", {}) or {}
        additional = schema.get("additionalProperties", True)
        for key in required:
            if key not in instance:
                errors.append(f"{path}: missing required field '{key}'")
        for key, value in instance.items():
            if key in properties:
                errors.extend(validate_against_schema(value, properties[key], f"{path}.{key}"))
            elif additional is False:
                errors.append(f"{path}: unexpected field '{key}'")
        return errors

    if expected_type == "array":
        if not isinstance(instance, list):
            return [f"{path}: expected array, got {type(instance).__name__}"]
        min_items = schema.get("minItems")
        if min_items is not None and len(instance) < min_items:
            errors.append(f"{path}: array length {len(instance)} < minItems {min_items}")
        item_schema = schema.get("items")
        if item_schema:
            for idx, item in enumerate(instance):
                errors.extend(validate_against_schema(item, item_schema, f"{path}[{idx}]"))
        return errors

    if expected_type == "string":
        if not isinstance(instance, str):
            return [f"{path}: expected string, got {type(instance).__name__}"]
        pattern = schema.get("pattern")
        if pattern and re.match(pattern, instance) is None:
            errors.append(f"{path}: string {instance!r} does not match pattern {pattern!r}")
        return errors

    if expected_type == "integer":
        if not isinstance(instance, int) or isinstance(instance, bool):
            return [f"{path}: expected integer, got {type(instance).__name__}"]
        minimum = schema.get("minimum")
        if minimum is not None and instance < minimum:
            errors.append(f"{path}: integer {instance} < minimum {minimum}")
        return errors

    if expected_type == "boolean":
        if not isinstance(instance, bool):
            return [f"{path}: expected boolean, got {type(instance).__name__}"]
        return errors

    return errors


def schema_for_ref(schema_ref: str | None) -> dict[str, Any] | None:
    if not schema_ref:
        return None
    return safe_load_yaml(PACK_ROOT / schema_ref)


@dataclass
class Question:
    question_id: str
    mode: str
    audience: list[str]
    category: str
    trigger_condition: str
    prerequisite_questions: list[str]
    question_text: str
    why_it_matters: str
    evidence_requested: list[str]
    answer_type: str
    confidence_impact: str
    blocking_severity_if_unanswered: str
    related_output_artifacts: list[str]
    artifact_key: str
    schema_ref: str | None = None
    allowed_values: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Question":
        return cls(
            question_id=raw["question_id"],
            mode=raw["mode"],
            audience=list(raw.get("audience") or []),
            category=raw["category"],
            trigger_condition=raw["trigger_condition"],
            prerequisite_questions=list(raw.get("prerequisite_questions") or []),
            question_text=raw["question_text"],
            why_it_matters=raw["why_it_matters"],
            evidence_requested=list(raw.get("evidence_requested") or []),
            answer_type=raw["answer_type"],
            confidence_impact=raw["confidence_impact"],
            blocking_severity_if_unanswered=raw["blocking_severity_if_unanswered"],
            related_output_artifacts=list(raw.get("related_output_artifacts") or []),
            artifact_key=raw["artifact_key"],
            schema_ref=raw.get("schema_ref"),
            allowed_values=list(raw.get("allowed_values") or []),
        )


def load_questions() -> list[Question]:
    data = safe_load_yaml(QUESTION_BANK_PATH) or {}
    return [Question.from_dict(q) for q in data.get("questions", [])]


def create_session(org_id: str, engagement_id: str, selected_modes: list[str], session_id: str | None = None) -> dict[str, Any]:
    return {
        "schema_version": "0.1.0",
        "org_id": org_id,
        "engagement_id": engagement_id,
        "session_id": session_id or dt.datetime.now().strftime("%Y%m%d") + "_" + uuid.uuid4().hex[:8],
        "selected_modes": selected_modes,
        "answers": {},
        "current_question_id": None,
        "updated_at": now_iso(),
    }


def session_path(session: dict[str, Any]) -> Path:
    return SESSIONS_DIR / session["engagement_id"] / f"{session['session_id']}.yaml"


def save_session(session: dict[str, Any]) -> Path:
    session["updated_at"] = now_iso()
    path = session_path(session)
    safe_dump_yaml(path, session)
    return path


def load_session(path: Path) -> dict[str, Any]:
    data = safe_load_yaml(path) or {}
    if "answers" not in data:
        data["answers"] = {}
    return data


def normalize_multiline(value: str) -> str:
    return "\n".join(line.rstrip() for line in value.strip().splitlines()).strip()


def parse_answer(question: Question, raw_text: str) -> tuple[bool, Any, str]:
    raw_text = raw_text.strip()
    if question.answer_type == "multiline_text":
        if not raw_text:
            return False, None, "answer cannot be empty"
        return True, normalize_multiline(raw_text), ""
    if question.answer_type == "single_select":
        if raw_text in question.allowed_values:
            return True, raw_text, ""
        try:
            idx = int(raw_text)
        except ValueError:
            idx = 0
        if 1 <= idx <= len(question.allowed_values):
            return True, question.allowed_values[idx - 1], ""
        return False, None, f"unknown choice: {raw_text!r}"
    if question.answer_type in {"yaml_list", "yaml_object"}:
        try:
            value = yaml.safe_load(raw_text)
        except yaml.YAMLError as exc:
            return False, None, f"invalid YAML: {exc}"
        expected = "list" if question.answer_type == "yaml_list" else "object"
        if question.answer_type == "yaml_list" and not isinstance(value, list):
            return False, None, f"expected YAML {expected}"
        if question.answer_type == "yaml_object" and not isinstance(value, dict):
            return False, None, f"expected YAML {expected}"
        schema = schema_for_ref(question.schema_ref)
        if schema:
            errors = validate_against_schema(value, schema)
            if errors:
                return False, None, "; ".join(errors)
        return True, value, ""
    return False, None, f"unsupported answer_type {question.answer_type!r}"


SECRET_KEY_RE = re.compile(r"(?i)\b(password|secret|token|api[_-]?key|client[_-]?secret|private[_-]?key)\b")
INLINE_SECRET_RE = re.compile(r"(?i)\b(password|secret|token|api[_-]?key|client[_-]?secret)\b\s*[:=]\s*([^\s,;]+)")
TOKEN_SHAPE_RE = re.compile(r"\b(sk-[A-Za-z0-9]{12,}|Bearer\s+[A-Za-z0-9._-]{12,}|AIza[0-9A-Za-z\-_]{20,})\b")


def sanitize_string(value: str, key_hint: str | None = None) -> str:
    text = INLINE_SECRET_RE.sub(lambda m: f"{m.group(1)}=[REDACTED_SECRET]", value)
    text = TOKEN_SHAPE_RE.sub("[REDACTED_SECRET]", text)
    if key_hint and SECRET_KEY_RE.search(key_hint) and text and "[REDACTED_SECRET]" not in text:
        placeholders = {"none", "oauth_placeholder", "api_key_placeholder", "basic_auth_placeholder", "sftp_key_placeholder", "mtls_placeholder", "shared_drive_placeholder", "email_inbox_placeholder"}
        if text not in placeholders:
            return "[REDACTED_SECRET]"
    return text


def sanitize_value(value: Any, key_hint: str | None = None) -> Any:
    if isinstance(value, dict):
        return {k: sanitize_value(v, key_hint=str(k)) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize_value(v, key_hint=key_hint) for v in value]
    if isinstance(value, str):
        return sanitize_string(value, key_hint=key_hint)
    return value


def record_answer(
    session: dict[str, Any],
    question: Question,
    value: Any,
    evidence_status: str,
    evidence_detail: str,
    evidence_refs: list[str] | None = None,
) -> None:
    if evidence_status not in ALLOWED_EVIDENCE_STATUS:
        raise ValueError(f"invalid evidence_status: {evidence_status}")
    if evidence_detail not in ALLOWED_EVIDENCE_DETAIL:
        raise ValueError(f"invalid evidence_detail: {evidence_detail}")
    if evidence_status == "confirmed" and evidence_detail not in CONFIRMING_DETAILS:
        raise ValueError("confirmed evidence must be file, screenshot, or verbal")
    if evidence_status != "confirmed" and evidence_detail in CONFIRMING_DETAILS:
        raise ValueError("non-confirmed evidence cannot use a confirming detail")
    session["answers"][question.question_id] = {
        "artifact_key": question.artifact_key,
        "value": sanitize_value(value),
        "evidence_status": evidence_status,
        "evidence_detail": evidence_detail,
        "evidence_refs": evidence_refs or [],
        "updated_at": now_iso(),
    }
    session["current_question_id"] = question.question_id


def answered(session: dict[str, Any], question_id: str) -> bool:
    return question_id in session.get("answers", {})


def required_section_status(session: dict[str, Any], questions: list[Question]) -> dict[str, list[str]]:
    missing: list[str] = []
    for qid in REQUIRED_QUESTION_IDS:
        if not answered(session, qid):
            missing.append(qid)
    return {
        "complete": [] if missing else REQUIRED_QUESTION_IDS[:],
        "missing": missing,
    }


def section_progress(session: dict[str, Any], questions: list[Question]) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    for q in questions:
        bucket = result.setdefault(q.mode, {"answered": 0, "total": 0})
        bucket["total"] += 1
        if answered(session, q.question_id):
            bucket["answered"] += 1
    return result


def compute_confidence_score(session: dict[str, Any], questions: list[Question]) -> float:
    total_weight = 0.0
    score = 0.0
    by_id = {q.question_id: q for q in questions}
    for qid, answer in session.get("answers", {}).items():
        q = by_id.get(qid)
        if not q:
            continue
        weight = CONFIDENCE_IMPACT_WEIGHT[q.confidence_impact]
        pair = (answer["evidence_status"], answer["evidence_detail"])
        evidence_weight = EVIDENCE_WEIGHT.get(pair, 0.0)
        score += weight * evidence_weight
        total_weight += weight
    return round(score / total_weight, 3) if total_weight else 0.0


def derive_missing_docs(session: dict[str, Any], questions: list[Question]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    by_id = {q.question_id: q for q in questions}
    for q in questions:
        answer = session.get("answers", {}).get(q.question_id)
        if answer is None and q.blocking_severity_if_unanswered in {"high", "medium"} and q.evidence_requested:
            items.append({"question_id": q.question_id, "status": "missing", "requests": q.evidence_requested})
            continue
        if answer and answer["evidence_status"] in {"missing", "blocked", "conflicting"} and q.evidence_requested:
            items.append({"question_id": q.question_id, "status": answer["evidence_status"], "requests": q.evidence_requested})
    return items


def _stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=True)


def detect_conflicts(session: dict[str, Any]) -> list[str]:
    conflicts: list[str] = []
    artifact_map: dict[str, Any] = {}
    for answer in session.get("answers", {}).values():
        artifact_key = answer.get("artifact_key")
        if artifact_key:
            artifact_map[artifact_key] = answer.get("value")
    for artifact_key, keys in STRUCTURED_CONFLICT_KEYS.items():
        rows = artifact_map.get(artifact_key)
        if not isinstance(rows, list):
            continue
        seen: dict[tuple[Any, ...], str] = {}
        for row in rows:
            if not isinstance(row, dict):
                continue
            key_tuple = tuple(row.get(k) for k in keys)
            signature = _stable_json(row)
            if key_tuple in seen and seen[key_tuple] != signature:
                conflicts.append(f"{artifact_key}:{key_tuple}")
            else:
                seen[key_tuple] = signature
    blockers = artifact_map.get("assumptions_gaps_blockers")
    if isinstance(blockers, list):
        for row in blockers:
            if isinstance(row, dict) and row.get("status") == "conflicting":
                conflicts.append(f"assumptions_gaps_blockers:{row.get('item_id')}")
    return conflicts


def derive_blockers(session: dict[str, Any], questions: list[Question]) -> list[str]:
    blockers: list[str] = []
    status = required_section_status(session, questions)
    for qid in status["missing"]:
        blockers.append(f"required section unanswered: {qid}")
    artifact_map = {answer.get("artifact_key"): answer.get("value") for answer in session.get("answers", {}).values()}
    gaps = artifact_map.get("assumptions_gaps_blockers")
    if isinstance(gaps, list):
        for row in gaps:
            if isinstance(row, dict) and row.get("status") in {"missing", "blocked", "conflicting"}:
                blockers.append(f"{row.get('item_id')}: {row.get('description')}")
    blockers.extend(f"conflict: {item}" for item in detect_conflicts(session))
    return blockers


def _answer_value(session: dict[str, Any], artifact_key: str, default: Any) -> Any:
    for answer in session.get("answers", {}).values():
        if answer.get("artifact_key") == artifact_key:
            return copy.deepcopy(answer.get("value"))
    return copy.deepcopy(default)


def markdown_table(rows: list[list[str]]) -> str:
    if not rows:
        return "_No rows captured._"
    lines = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join(lines)


def _status_label(answer: dict[str, Any]) -> str:
    return f"{answer['evidence_status']} ({answer['evidence_detail']})"


def render_source_inventory(rows: list[dict[str, Any]]) -> str:
    out = []
    for row in rows:
        out.append([
            row.get("system_name", ""),
            row.get("business_purpose", ""),
            row.get("source_role", ""),
            row.get("owner", ""),
            row.get("export_api_availability", ""),
            "yes" if row.get("sample_files_available") else "no",
            row.get("confidence", ""),
            row.get("blocker_notes", ""),
        ])
    header = [
        ["Source", "Purpose", "Role", "Owner", "Access path", "Samples", "Confidence", "Blockers"],
        ["---", "---", "---", "---", "---", "---", "---", "---"],
    ]
    return markdown_table(header + out)


def render_field_inventory(rows: list[dict[str, Any]]) -> str:
    out = []
    for row in rows:
        out.append([
            row.get("source_id", ""),
            row.get("export_name", ""),
            row.get("layout_name", ""),
            ", ".join(row.get("actual_column_names") or []),
            ", ".join(row.get("missing_fields") or []),
            row.get("evidence_source", ""),
            ", ".join(row.get("known_quirks") or []),
            ", ".join(row.get("next_actions") or []),
        ])
    header = [
        ["Source", "Export", "Layout", "Actual field names", "Missing fields", "Evidence", "Known quirks", "Next actions"],
        ["---", "---", "---", "---", "---", "---", "---", "---"],
    ]
    return markdown_table(header + out)


def render_access_model(rows: list[dict[str, Any]]) -> str:
    out = []
    for row in rows:
        out.append([
            row.get("source_id", ""),
            row.get("access_method", ""),
            row.get("provisioning_method", ""),
            row.get("credential_owner", ""),
            ", ".join(row.get("approval_requirements") or []),
            row.get("environment_notes", ""),
            row.get("blocker_notes", ""),
        ])
    header = [
        ["Source", "Access method", "Provisioning", "Credential owner", "Approvals", "Environment notes", "Blockers"],
        ["---", "---", "---", "---", "---", "---", "---"],
    ]
    return markdown_table(header + out)


def render_crosswalk_rules(rows: list[dict[str, Any]]) -> str:
    out = []
    for row in rows:
        out.append([
            row.get("canonical_entity", ""),
            row.get("source_system", ""),
            ", ".join(row.get("match_keys") or []),
            ", ".join(row.get("fallback_keys") or []),
            row.get("source_priority", ""),
            row.get("manual_override_rule", ""),
            row.get("mapping_owner", ""),
            row.get("exception_path", ""),
        ])
    header = [
        ["Canonical entity", "Source", "Match keys", "Fallback keys", "Precedence", "Override rule", "Owner", "Exception path"],
        ["---", "---", "---", "---", "---", "---", "---", "---"],
    ]
    return markdown_table(header + out)


def render_reporting_calendar(rows: list[dict[str, Any]]) -> str:
    out = []
    for row in rows:
        out.append([
            row.get("cadence_type", ""),
            row.get("deliverable", ""),
            row.get("owner", ""),
            row.get("due_rule", ""),
            row.get("dependency", ""),
            row.get("escalation_path", ""),
        ])
    header = [
        ["Cadence", "Deliverable", "Owner", "Due rule", "Dependency", "Escalation"],
        ["---", "---", "---", "---", "---", "---"],
    ]
    return markdown_table(header + out)


def render_assumptions(rows: list[dict[str, Any]]) -> str:
    out = []
    for row in rows:
        out.append([
            row.get("item_id", ""),
            row.get("area", ""),
            row.get("status", ""),
            row.get("description", ""),
            row.get("owner", ""),
            row.get("next_step", ""),
            row.get("downstream_impact", ""),
        ])
    header = [
        ["Item", "Area", "Status", "Description", "Owner", "Next step", "Impact"],
        ["---", "---", "---", "---", "---", "---", "---"],
    ]
    return markdown_table(header + out)


def render_decision_log(rows: list[dict[str, Any]]) -> str:
    out = []
    for row in rows:
        out.append([
            row.get("decision", ""),
            row.get("decision_owner", ""),
            row.get("decision_date", ""),
            row.get("reason", ""),
            row.get("downstream_impact", ""),
            row.get("unresolved_follow_up", ""),
            row.get("status", ""),
        ])
    header = [
        ["Decision", "Owner", "Date", "Reason", "Downstream impact", "Follow-up", "Status"],
        ["---", "---", "---", "---", "---", "---", "---"],
    ]
    return markdown_table(header + out)


def build_artifact_bundle(session: dict[str, Any], questions: list[Question]) -> dict[str, str]:
    source_inventory = _answer_value(session, "source_inventory", [])
    access_model = _answer_value(session, "credentials_access_model", [])
    field_inventory = _answer_value(session, "export_field_inventory", [])
    crosswalk_rules = _answer_value(session, "crosswalk_rules", [])
    reporting_calendar = _answer_value(session, "reporting_calendar", [])
    approval_controls = _answer_value(session, "approval_controls", [])
    assumptions = _answer_value(session, "assumptions_gaps_blockers", [])
    decision_log = _answer_value(session, "decision_log", [])
    context = _answer_value(session, "executive_context_summary", "")
    success_criteria = _answer_value(session, "success_criteria", "")
    requested_decisions = _answer_value(session, "requested_decisions", "")
    signoff_status = _answer_value(session, "signoff_status", "draft")
    field_gap_summary = _answer_value(session, "field_gap_summary", "")
    missing_document_plan = _answer_value(session, "missing_document_plan", "")

    blockers = derive_blockers(session, questions)
    missing_docs = derive_missing_docs(session, questions)
    confidence = compute_confidence_score(session, questions)
    conflicts = detect_conflicts(session)

    systems = ", ".join(row.get("system_name", row.get("source_id", "")) for row in source_inventory) or "No systems captured"
    confirmed = []
    assumed = []
    blocked = []
    for row in assumptions:
        status = row.get("status")
        line = f"- {row.get('description', '')} ({row.get('owner', 'owner unknown')})"
        if status == "confirmed":
            confirmed.append(line)
        elif status in {"assumed", "inferred"}:
            assumed.append(line)
        elif status in {"missing", "blocked", "conflicting"}:
            blocked.append(line)
    if not blocked and blockers:
        blocked = [f"- {item}" for item in blockers]

    approval_lines = []
    for row in approval_controls:
        approval_lines.append(f"- {row.get('approver', 'Approver TBD')} — {row.get('approval_area', '')}")
    blocker_lines = [f"- {item}" for item in blockers] or ["- None logged"]
    system_lines = [f"- {row.get('system_name', '')}: {row.get('environment_details', '')}" for row in source_inventory] or ["- No source inventory captured"]
    ownership_lines = [f"- {row.get('owner', '')} owns {row.get('deliverable', '')}" for row in reporting_calendar] or ["- Ownership not yet summarized"]
    approval_request_lines = [f"- {row.get('approval_area', '')}: {row.get('approver', '')}" for row in approval_controls] or ["- Approval controls not yet captured"]
    signoff_lines = approval_lines or ["- Approver TBD"]

    intake_packet = "\n".join([
        "# Implementation Intake Packet",
        "",
        "## Purpose",
        "",
        context or "_Not yet captured._",
        "",
        "## Scope Summary",
        "",
        success_criteria or "_Not yet captured._",
        "",
        "## Systems In Scope",
        "",
        f"- {systems}",
        "",
        "## Operating Model Summary",
        "",
        f"- {len(source_inventory)} source systems captured",
        f"- {len(access_model)} access model rows captured",
        f"- {len(crosswalk_rules)} crosswalk rules captured",
        "",
        "## Reporting Cadence Summary",
        "",
        f"- {len(reporting_calendar)} reporting cadence rows captured",
        "",
        "## Main Integration Assumptions",
        "",
        ("\n".join(assumed) if assumed else "_No open assumptions logged._"),
        "",
        "## Confidence and Blockers",
        "",
        f"- Confidence score: {confidence}",
        f"- Missing-doc requests: {len(missing_docs)}",
        f"- Conflicts: {len(conflicts)}",
        *blocker_lines,
        "",
        "## Recommended Next Step",
        "",
        requested_decisions or missing_document_plan or "_Collect missing evidence and reopen preview._",
    ])

    leader_pack = "\n".join([
        "# Leader Sign-Off Pack",
        "",
        "## Purpose",
        "",
        context or "_Not yet captured._",
        "",
        "## Scope",
        "",
        success_criteria or "_Not yet captured._",
        "",
        "## Systems and Environments Covered",
        "",
        *system_lines,
        "",
        "## What Is Confirmed",
        "",
        ("\n".join(confirmed) if confirmed else "_No confirmed items logged._"),
        "",
        "## What Remains Assumed",
        "",
        ("\n".join(assumed) if assumed else "_No assumptions logged._"),
        "",
        "## What Is Blocked",
        "",
        ("\n".join(blocked) if blocked else "_No blockers logged._"),
        "",
        "## Implementation Risks",
        "",
        field_gap_summary or "_See blockers and assumptions log._",
        "",
        "## Ownership Assignments",
        "",
        *ownership_lines,
        "",
        "## Approval Requests",
        "",
        *approval_request_lines,
        "",
        "## Decisions Required Before Build",
        "",
        requested_decisions or "_No requested decisions logged._",
        "",
        "## Recommended Next Step",
        "",
        "_Review the open blockers, missing evidence, and requested decisions before moving to build._",
        "",
        "## Sign-Off",
        "",
        f"Status: {signoff_status}",
        "",
        "Approver lines:",
        "",
        *signoff_lines,
    ])

    bundle = {
        "implementation_intake_packet.md": sanitize_string(intake_packet),
        "source_inventory_register.md": sanitize_string("# Source Inventory Register\n\n" + render_source_inventory(source_inventory)),
        "export_field_inventory.md": sanitize_string("# Export & Field Inventory\n\n" + render_field_inventory(field_inventory)),
        "credentials_access_model.md": sanitize_string("# Credentials & Access Model\n\n" + render_access_model(access_model)),
        "crosswalk_rules_register.md": sanitize_string("# Crosswalk Rules Register\n\n" + render_crosswalk_rules(crosswalk_rules)),
        "reporting_calendar_sla_register.md": sanitize_string("# Reporting Calendar & SLA Register\n\n" + render_reporting_calendar(reporting_calendar)),
        "assumptions_gaps_blockers_log.md": sanitize_string("# Assumptions, Gaps, and Blockers Log\n\n" + render_assumptions(assumptions)),
        "leader_signoff_pack.md": sanitize_string(leader_pack),
        "decision_log.md": sanitize_string("# Decision Log\n\n" + render_decision_log(decision_log)),
    }
    return bundle


def write_bundle(session: dict[str, Any], bundle: dict[str, str]) -> dict[str, Path]:
    base = session_path(session).parent
    paths = {}
    for name, content in bundle.items():
        target = base / f"{session['session_id']}__{name}"
        target.write_text(content + "\n", encoding="utf-8")
        paths[name] = target
    preview = base / f"{session['session_id']}__preview.md"
    preview.write_text("\n\n".join(bundle.values()) + "\n", encoding="utf-8")
    paths["preview"] = preview
    return paths


def prompt_multiline(prompt: str) -> str:
    print(prompt)
    print("Enter response. Finish with ':done' on its own line.")
    lines: list[str] = []
    while True:
        line = input("> ")
        if line.strip() == ":done":
            break
        lines.append(line)
    return "\n".join(lines)


def run_interactive(session: dict[str, Any], questions: list[Question], ansi: Ansi) -> None:
    selected = [q for q in questions if q.mode in session["selected_modes"]]
    total = len(selected)
    answered_count = 0
    for index, question in enumerate(selected, start=1):
        if any(not answered(session, dep) for dep in question.prerequisite_questions):
            continue
        if answered(session, question.question_id):
            answered_count += 1
            continue
        print()
        print(ansi.bold(f"[{question.mode}] {question.question_id}"))
        print(render_progress_bar(answered_count, total))
        print(textwrap.fill(question.question_text, width=100))
        print(ansi.cyan("Why it matters: ") + question.why_it_matters)
        if question.allowed_values:
            for idx, choice in enumerate(question.allowed_values, start=1):
                print(f"  {idx}. {choice}")
        if question.answer_type in {"yaml_list", "yaml_object", "multiline_text"}:
            raw = prompt_multiline("")
        else:
            raw = input("> ")
        ok, value, error = parse_answer(question, raw)
        if not ok:
            print(ansi.red(error))
            continue
        evidence_status = input("Evidence status [confirmed/assumed/inferred/missing/blocked/conflicting]: ").strip()
        evidence_detail = input("Evidence detail [file/screenshot/verbal/assumed/inferred/missing/blocked/conflicting]: ").strip()
        try:
            record_answer(session, question, value, evidence_status, evidence_detail)
        except ValueError as exc:
            print(ansi.red(str(exc)))
            continue
        save_session(session)
        answered_count += 1
        print(ansi.green("Saved."))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Implementation intake and sign-off TUI")
    parser.add_argument("--org-id", required=True)
    parser.add_argument("--engagement-id", default=None)
    parser.add_argument("--session-id", default=None)
    parser.add_argument("--modes", default=None, help="Comma-separated mode ids")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    questions = load_questions()
    modes = args.modes.split(",") if args.modes else sorted({q.mode for q in questions})
    if args.session_id:
        path = SESSIONS_DIR / (args.engagement_id or args.org_id) / f"{args.session_id}.yaml"
        session = load_session(path)
    else:
        session = create_session(
            org_id=args.org_id,
            engagement_id=args.engagement_id or args.org_id,
            selected_modes=modes,
        )

    ansi = Ansi()
    if not args.dry_run:
        run_interactive(session, questions, ansi)

    save_session(session)
    bundle = build_artifact_bundle(session, questions)
    write_bundle(session, bundle)
    print(ansi.green(f"Session saved to {session_path(session)}"))
    print(ansi.green(f"Generated {len(bundle)} packet artifacts"))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
