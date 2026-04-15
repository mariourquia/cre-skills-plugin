#!/usr/bin/env python3
"""
Tailoring TUI — terminal UI for the residential_multifamily tailoring skill.

This is a reference implementation. Dependencies are limited to the Python
standard library plus PyYAML (`pyyaml` is the one non-stdlib dependency in
the subsystem's test environment already). Rich and Textual are intentionally
avoided so the UI is portable; if `rich` or `textual` is installed, a future
revision could opt into prettier rendering.

What it does
------------
- Loads all question banks under ``tailoring/question_banks/``.
- Loads the document catalog from ``tailoring/doc_catalog.yaml``.
- Sequences audiences selected at the top of the session.
- Renders questions one at a time with ANSI-styled borders and headers.
- Accepts answers with per-question-type validation.
- Exposes navigation shortcuts (``:b`` back, ``:s`` skip, ``:w`` where-it-goes,
  ``:p`` preview, ``:q`` save and quit, ``:h`` help).
- Maintains a per-session persisted state file at
  ``tailoring/sessions/{org_id}/{session_id}.yaml`` (directory is in
  ``.gitignore`` by convention).
- Detects missing-doc triggers and appends entries to
  ``tailoring/missing_docs_queue.yaml`` when the operator indicates the
  document is not in hand.
- Renders a YAML diff preview between the current overlay state (or
  ``overlays/org/_defaults/`` for a new org) and the proposed updates.
- Opens ``tailoring/sign_off_queue.yaml`` entries for every proposed change.
- Writes a session summary markdown to
  ``tailoring/sessions/{org_id}/{session_id}__summary.md``.

What it does not do
-------------------
- Never writes to ``overlays/org/{org_id}/``. The commit step is external.
- Never mutates anything under ``_core/``.
- Never auto-fills keys whose source doc is open in the missing-docs queue.

Usage
-----
Interactive onboarding::

    python3 tailoring/tools/tailoring_tui.py --org-id acme_mf

Resume an existing session::

    python3 tailoring/tools/tailoring_tui.py --org-id acme_mf \\
        --session-id 20260415_acme_coo_01

Non-interactive (CI) dry run::

    python3 tailoring/tools/tailoring_tui.py --org-id acme_mf --dry-run

Degrades gracefully when stdout is not a TTY (no ANSI escape codes, plain line
input). This is the mode used by the unit tests in
``tailoring/tools/test_tailoring_tui.py``.
"""

from __future__ import annotations

import argparse
import copy
import datetime as _dt
import json
import os
import re
import sys
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover
    print(
        "ERROR: PyYAML is required. Install with `pip install pyyaml`.",
        file=sys.stderr,
    )
    sys.exit(2)


# --------------------------------------------------------------------------- #
# Paths                                                                        #
# --------------------------------------------------------------------------- #

TAILORING_DIR = Path(__file__).resolve().parent.parent
QUESTION_BANKS_DIR = TAILORING_DIR / "question_banks"
DOC_CATALOG_PATH = TAILORING_DIR / "doc_catalog.yaml"
MISSING_DOCS_QUEUE_PATH = TAILORING_DIR / "missing_docs_queue.yaml"
SIGN_OFF_QUEUE_PATH = TAILORING_DIR / "sign_off_queue.yaml"
SESSIONS_DIR = TAILORING_DIR / "sessions"
OVERLAYS_ORG_DEFAULTS = (
    TAILORING_DIR.parent / "overlays" / "org" / "_defaults"
)
OVERLAYS_ORG_DIR = TAILORING_DIR.parent / "overlays" / "org"


# --------------------------------------------------------------------------- #
# ANSI rendering — optional; degrades when not on TTY                          #
# --------------------------------------------------------------------------- #

class _AnsiStyle:
    """Tiny ANSI palette. Suppresses escapes when stdout is not a TTY."""

    def __init__(self, enabled: bool | None = None) -> None:
        if enabled is None:
            enabled = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None
        self.enabled = bool(enabled)

    def _wrap(self, code: str, text: str) -> str:
        if not self.enabled:
            return text
        return f"\x1b[{code}m{text}\x1b[0m"

    def bold(self, text: str) -> str: return self._wrap("1", text)
    def dim(self, text: str) -> str: return self._wrap("2", text)
    def italic(self, text: str) -> str: return self._wrap("3", text)
    def red(self, text: str) -> str: return self._wrap("31", text)
    def green(self, text: str) -> str: return self._wrap("32", text)
    def yellow(self, text: str) -> str: return self._wrap("33", text)
    def blue(self, text: str) -> str: return self._wrap("34", text)
    def magenta(self, text: str) -> str: return self._wrap("35", text)
    def cyan(self, text: str) -> str: return self._wrap("36", text)


BOX = {
    "tl": "\u250c", "tr": "\u2510", "bl": "\u2514", "br": "\u2518",
    "h": "\u2500", "v": "\u2502",
    "tl_d": "\u2554", "tr_d": "\u2557", "bl_d": "\u255a", "br_d": "\u255d",
    "h_d": "\u2550", "v_d": "\u2551",
    "t_tee": "\u252c", "b_tee": "\u2534", "l_tee": "\u251c", "r_tee": "\u2524",
}


def render_box(lines: list[str], width: int, double: bool = False) -> str:
    """Render a list of strings surrounded by a box-drawing border."""
    h = BOX["h_d"] if double else BOX["h"]
    v = BOX["v_d"] if double else BOX["v"]
    tl = BOX["tl_d"] if double else BOX["tl"]
    tr = BOX["tr_d"] if double else BOX["tr"]
    bl = BOX["bl_d"] if double else BOX["bl"]
    br = BOX["br_d"] if double else BOX["br"]
    inner = width - 2
    top = tl + (h * inner) + tr
    bottom = bl + (h * inner) + br
    middle = [v + _pad_ansi(line, inner) + v for line in lines]
    return "\n".join([top, *middle, bottom])


_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _visible_len(s: str) -> int:
    """Length excluding ANSI escapes."""
    return len(_ANSI_RE.sub("", s))


def _pad_ansi(s: str, width: int) -> str:
    """Pad right to width using visible length (ignoring ANSI)."""
    visible = _visible_len(s)
    if visible >= width:
        return s
    return s + " " * (width - visible)


def render_progress_bar(completed: int, total: int, width: int = 40) -> str:
    """Render a progress bar of width characters."""
    if total <= 0:
        filled = 0
    else:
        filled = int(round((completed / total) * width))
    bar = "\u2588" * filled + "\u2591" * (width - filled)
    pct = (completed / total * 100.0) if total else 0.0
    return f"[{bar}] {completed}/{total} ({pct:.0f}%)"


# --------------------------------------------------------------------------- #
# Domain types                                                                 #
# --------------------------------------------------------------------------- #

@dataclass
class Question:
    id: str
    bank_slug: str
    question_text: str
    purpose: str
    answer_type: str
    choices: list[str] = field(default_factory=list)
    target_overlay_ref: str | None = None
    follow_up_ids: list[str] = field(default_factory=list)
    missing_doc_triggers: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, raw: dict[str, Any], bank_slug: str) -> "Question":
        return cls(
            id=str(raw["id"]),
            bank_slug=bank_slug,
            question_text=str(raw["question_text"]),
            purpose=str(raw.get("purpose", "")),
            answer_type=str(raw["answer_type"]),
            choices=list(raw.get("choices") or []),
            target_overlay_ref=raw.get("target_overlay_ref"),
            follow_up_ids=list(raw.get("follow_up_ids") or []),
            missing_doc_triggers=list(raw.get("missing_doc_triggers") or []),
        )


@dataclass
class Bank:
    bank_slug: str
    audience: str
    version: str
    questions: list[Question]

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Bank":
        bank_slug = str(raw["bank_slug"])
        questions = [
            Question.from_dict(q, bank_slug=bank_slug)
            for q in raw.get("questions", [])
        ]
        return cls(
            bank_slug=bank_slug,
            audience=str(raw.get("audience", bank_slug)),
            version=str(raw.get("version", "0.0.0")),
            questions=questions,
        )


# --------------------------------------------------------------------------- #
# YAML helpers                                                                 #
# --------------------------------------------------------------------------- #

def _load_yaml(path: Path) -> Any:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _dump_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            data,
            f,
            sort_keys=False,
            default_flow_style=False,
            allow_unicode=True,
        )


def load_question_banks(banks_dir: Path = QUESTION_BANKS_DIR) -> dict[str, Bank]:
    """Load all YAML banks under banks_dir. Keyed by bank_slug."""
    banks: dict[str, Bank] = {}
    if not banks_dir.exists():
        return banks
    for path in sorted(banks_dir.glob("*.yaml")):
        raw = _load_yaml(path) or {}
        bank = Bank.from_dict(raw)
        banks[bank.bank_slug] = bank
    return banks


def load_doc_catalog(catalog_path: Path = DOC_CATALOG_PATH) -> dict[str, dict[str, Any]]:
    """Load the doc catalog keyed by doc_slug."""
    raw = _load_yaml(catalog_path) or {}
    return {
        str(entry["doc_slug"]): entry
        for entry in raw.get("documents", [])
    }


# --------------------------------------------------------------------------- #
# Session                                                                      #
# --------------------------------------------------------------------------- #

@dataclass
class Session:
    org_id: str
    session_id: str
    audiences_scheduled: list[str] = field(default_factory=list)
    audiences_completed: list[str] = field(default_factory=list)
    current_audience: str | None = None
    current_question_id: str | None = None
    answers: dict[str, dict[str, Any]] = field(default_factory=dict)
    pending_doc_keys: list[str] = field(default_factory=list)
    missing_docs_opened: list[str] = field(default_factory=list)
    sign_offs_opened: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: _now())
    updated_at: str = field(default_factory=lambda: _now())
    notes: str = ""

    def path(self) -> Path:
        return SESSIONS_DIR / self.org_id / f"{self.session_id}.yaml"

    def summary_path(self) -> Path:
        return SESSIONS_DIR / self.org_id / f"{self.session_id}__summary.md"

    def to_dict(self) -> dict[str, Any]:
        return {
            "org_id": self.org_id,
            "session_id": self.session_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "audiences_scheduled": list(self.audiences_scheduled),
            "audiences_completed": list(self.audiences_completed),
            "current_audience": self.current_audience,
            "current_question_id": self.current_question_id,
            "answers": dict(self.answers),
            "pending_doc_keys": list(self.pending_doc_keys),
            "missing_docs_opened": list(self.missing_docs_opened),
            "sign_offs_opened": list(self.sign_offs_opened),
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Session":
        return cls(
            org_id=str(raw["org_id"]),
            session_id=str(raw["session_id"]),
            audiences_scheduled=list(raw.get("audiences_scheduled") or []),
            audiences_completed=list(raw.get("audiences_completed") or []),
            current_audience=raw.get("current_audience"),
            current_question_id=raw.get("current_question_id"),
            answers=dict(raw.get("answers") or {}),
            pending_doc_keys=list(raw.get("pending_doc_keys") or []),
            missing_docs_opened=list(raw.get("missing_docs_opened") or []),
            sign_offs_opened=list(raw.get("sign_offs_opened") or []),
            created_at=str(raw.get("created_at") or _now()),
            updated_at=str(raw.get("updated_at") or _now()),
            notes=str(raw.get("notes") or ""),
        )

    def save(self) -> None:
        self.updated_at = _now()
        _dump_yaml(self.path(), self.to_dict())


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_session_id(audience: str | None = None) -> str:
    stamp = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%d_%H%M%S")
    suffix = f"_{audience}" if audience else ""
    short = uuid.uuid4().hex[:4]
    return f"{stamp}{suffix}_{short}"


def find_latest_session(org_id: str) -> Session | None:
    org_dir = SESSIONS_DIR / org_id
    if not org_dir.exists():
        return None
    candidates = sorted(
        [p for p in org_dir.glob("*.yaml") if not p.name.endswith("__summary.md")],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        return None
    raw = _load_yaml(candidates[0])
    if not raw:
        return None
    return Session.from_dict(raw)


def load_session_by_id(org_id: str, session_id: str) -> Session | None:
    path = SESSIONS_DIR / org_id / f"{session_id}.yaml"
    raw = _load_yaml(path)
    if not raw:
        return None
    return Session.from_dict(raw)


# --------------------------------------------------------------------------- #
# Overlay state (proposed vs current)                                          #
# --------------------------------------------------------------------------- #

def load_current_overlay(org_id: str) -> dict[str, Any]:
    """Return current org overlay, or the defaults overlay when the org is new."""
    org_overlay = OVERLAYS_ORG_DIR / org_id / "overlay.yaml"
    if org_overlay.exists():
        loaded = _load_yaml(org_overlay) or {}
        return loaded if isinstance(loaded, dict) else {}
    defaults = OVERLAYS_ORG_DEFAULTS / "overlay.yaml"
    if defaults.exists():
        loaded = _load_yaml(defaults) or {}
        return loaded if isinstance(loaded, dict) else {}
    return {}


def _set_by_dotted_path(root: dict[str, Any], dotted: str, value: Any) -> None:
    parts = dotted.split(".")
    cursor = root
    for p in parts[:-1]:
        if p not in cursor or not isinstance(cursor[p], dict):
            cursor[p] = {}
        cursor = cursor[p]
    cursor[parts[-1]] = value


def _get_by_dotted_path(root: dict[str, Any], dotted: str) -> Any:
    cursor: Any = root
    for p in dotted.split("."):
        if not isinstance(cursor, dict) or p not in cursor:
            return None
        cursor = cursor[p]
    return cursor


def _parse_target_ref(target_ref: str) -> tuple[str, str] | None:
    """Return (file, dotted_path) or None when the ref is malformed."""
    if "#" not in target_ref:
        return None
    file_part, key_part = target_ref.split("#", 1)
    return file_part, key_part


def build_proposed_overlay(
    session: Session,
    banks: dict[str, Bank],
    current_overlay: dict[str, Any],
) -> dict[str, Any]:
    """Apply answered, non-pending_doc questions onto a deep copy of current_overlay."""
    proposed = copy.deepcopy(current_overlay) if isinstance(current_overlay, dict) else {}
    for bank in banks.values():
        for q in bank.questions:
            answer = session.answers.get(q.id)
            if not answer:
                continue
            if answer.get("pending_doc"):
                continue
            if answer.get("skipped"):
                continue
            if q.target_overlay_ref is None:
                continue
            parsed = _parse_target_ref(q.target_overlay_ref)
            if parsed is None:
                continue
            _file, key_path = parsed
            _set_by_dotted_path(proposed, key_path, answer.get("value"))
    return proposed


# --------------------------------------------------------------------------- #
# Diff computation                                                             #
# --------------------------------------------------------------------------- #

@dataclass
class DiffEntry:
    overlay_key: str
    prior_value: Any
    proposed_value: Any
    interview_source: dict[str, str]
    approver_role: str | None
    approval_matrix_row: int | None
    rationale: str


def compute_diff(
    current: dict[str, Any],
    proposed: dict[str, Any],
    session: Session,
    banks: dict[str, Bank],
    approver_rules: dict[str, dict[str, Any]] | None = None,
) -> list[DiffEntry]:
    """
    Walk proposed keys and produce diff entries for added/modified keys.
    Each entry carries interview source metadata derived from the session's
    answer that populated that overlay key.
    """
    approver_rules = approver_rules or default_approver_rules()
    entries: list[DiffEntry] = []
    # Build reverse index: target_overlay_ref -> list of (bank_slug, question_id)
    # because multiple questions (for example COO and CFO reconcile questions) may
    # target the same overlay key. The first question with a usable answer wins;
    # ordering is deterministic by (bank_slug, question_id).
    target_to_questions: dict[str, list[tuple[str, str]]] = {}
    for bank in banks.values():
        for q in bank.questions:
            if q.target_overlay_ref:
                parsed = _parse_target_ref(q.target_overlay_ref)
                if parsed is None:
                    continue
                _, key_path = parsed
                target_to_questions.setdefault(key_path, []).append(
                    (q.bank_slug, q.id)
                )

    for key_path, sources in sorted(target_to_questions.items()):
        # Choose the first source that has a usable answer.
        chosen: tuple[str, str] | None = None
        for candidate in sorted(sources):
            bank_slug, question_id = candidate
            answer = session.answers.get(question_id)
            if answer and not answer.get("skipped") and not answer.get("pending_doc"):
                chosen = candidate
                break
        if chosen is None:
            continue
        bank_slug, question_id = chosen
        proposed_value = _get_by_dotted_path(proposed, key_path)
        prior_value = _get_by_dotted_path(current, key_path)
        if proposed_value == prior_value:
            continue
        rule = _match_approver_rule(key_path, approver_rules)
        entries.append(
            DiffEntry(
                overlay_key=key_path,
                prior_value=prior_value,
                proposed_value=proposed_value,
                interview_source={
                    "bank_slug": bank_slug,
                    "question_id": question_id,
                },
                approver_role=rule["approver_role"] if rule else None,
                approval_matrix_row=rule["approval_matrix_row"] if rule else None,
                rationale=rule["rationale_template"].format(
                    bank=bank_slug, qid=question_id
                ) if rule else (
                    f"From {bank_slug} interview question {question_id}."
                ),
            )
        )
    return entries


def default_approver_rules() -> dict[str, dict[str, Any]]:
    """Map overlay key prefixes to approver role and approval matrix row."""
    return {
        "approval_matrix.threshold_disbursement_1": {
            "approver_role": "coo_operations_leader",
            "approval_matrix_row": 6,
            "rationale_template": (
                "Approval matrix row 6 (financial disbursement tier 1) "
                "threshold; sourced from {bank} interview {qid}."
            ),
        },
        "approval_matrix.threshold_disbursement_2": {
            "approver_role": "coo_operations_leader",
            "approval_matrix_row": 7,
            "rationale_template": (
                "Approval matrix row 7 (financial disbursement tier 2) "
                "threshold; sourced from {bank} interview {qid}."
            ),
        },
        "approval_matrix.threshold_vendor_contract": {
            "approver_role": "portfolio_manager",
            "approval_matrix_row": 19,
            "rationale_template": (
                "Approval matrix row 19 (vendor contract signature) "
                "threshold; sourced from {bank} interview {qid}."
            ),
        },
        "approval_matrix.threshold_co_minor": {
            "approver_role": "coo_operations_leader",
            "approval_matrix_row": 10,
            "rationale_template": (
                "Approval matrix row 10 (change order minor) threshold; "
                "sourced from {bank} interview {qid}."
            ),
        },
        "approval_matrix.threshold_co_major": {
            "approver_role": "ceo_executive_leader",
            "approval_matrix_row": 11,
            "rationale_template": (
                "Approval matrix row 11 (change order major) threshold; "
                "sourced from {bank} interview {qid}."
            ),
        },
        "concession_policy": {
            "approver_role": "coo_operations_leader",
            "approval_matrix_row": 13,
            "rationale_template": (
                "Concession policy change; approval matrix row 13 applies. "
                "Sourced from {bank} interview {qid}."
            ),
        },
        "vendor_policy": {
            "approver_role": "portfolio_manager",
            "approval_matrix_row": 19,
            "rationale_template": (
                "Vendor policy change; approval matrix row 19 applies. "
                "Sourced from {bank} interview {qid}."
            ),
        },
    }


def _match_approver_rule(
    key_path: str, rules: dict[str, dict[str, Any]]
) -> dict[str, Any] | None:
    """Return the rule whose key is the longest prefix of key_path."""
    best: tuple[int, dict[str, Any]] | None = None
    for prefix, rule in rules.items():
        if key_path == prefix or key_path.startswith(prefix + "."):
            score = len(prefix)
            if best is None or score > best[0]:
                best = (score, rule)
    return best[1] if best else None


# --------------------------------------------------------------------------- #
# Queue append (missing docs, sign-offs)                                       #
# --------------------------------------------------------------------------- #

def load_queue(path: Path) -> dict[str, Any]:
    raw = _load_yaml(path) or {}
    if "entries" not in raw:
        raw["entries"] = []
    return raw


def save_queue(path: Path, queue: dict[str, Any]) -> None:
    _dump_yaml(path, queue)


def append_missing_doc(
    queue: dict[str, Any],
    *,
    doc_slug: str,
    doc_title: str,
    requested_from_role: str,
    priority: str,
    used_by_overlay_keys: list[str],
    substitute_behavior: str,
    org_id: str,
    session_id: str,
    notes: str = "",
) -> dict[str, Any]:
    entry = {
        "doc_slug": doc_slug,
        "doc_title": doc_title,
        "requested_from_role": requested_from_role,
        "requested_at": _now(),
        "priority": priority,
        "used_by_overlay_keys": list(used_by_overlay_keys),
        "substitute_behavior": substitute_behavior,
        "status": "open",
        "org_id": org_id,
        "session_id": session_id,
        "notes": notes,
    }
    queue.setdefault("entries", []).append(entry)
    return entry


def append_sign_off(
    queue: dict[str, Any],
    *,
    entry: DiffEntry,
    org_id: str,
    session_id: str,
    expires_in_days: int = 30,
) -> dict[str, Any]:
    now = _dt.datetime.now(_dt.timezone.utc)
    expires = now + _dt.timedelta(days=expires_in_days)
    record = {
        "queue_entry_id": uuid.uuid4().hex,
        "org_id": org_id,
        "session_id": session_id,
        "overlay_key": entry.overlay_key,
        "proposed_value": entry.proposed_value,
        "prior_value": entry.prior_value,
        "rationale": entry.rationale,
        "interview_source": entry.interview_source,
        "approver_role": entry.approver_role or "coo_operations_leader",
        "approval_matrix_row": entry.approval_matrix_row,
        "created_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "expires_at": expires.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "pending",
        "approver_note": None,
    }
    queue.setdefault("entries", []).append(record)
    return record


# --------------------------------------------------------------------------- #
# Completeness / confidence                                                    #
# --------------------------------------------------------------------------- #

def completeness_by_audience(
    session: Session, banks: dict[str, Bank]
) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for slug, bank in banks.items():
        total = len(bank.questions)
        answered = 0
        pending_doc = 0
        for q in bank.questions:
            a = session.answers.get(q.id)
            if not a:
                continue
            if a.get("skipped"):
                continue
            if a.get("pending_doc"):
                pending_doc += 1
                continue
            answered += 1
        denom = total - pending_doc if total > pending_doc else total
        score = (answered / denom) if denom else 0.0
        out[slug] = {
            "total": total,
            "answered": answered,
            "pending_doc": pending_doc,
            "score_excluding_pending": round(score, 4),
        }
    return out


# --------------------------------------------------------------------------- #
# Rendering helpers                                                            #
# --------------------------------------------------------------------------- #

WIDTH = 78  # default terminal width for box rendering


def clear_screen() -> None:
    if sys.stdout.isatty():
        sys.stdout.write("\x1b[2J\x1b[H")
        sys.stdout.flush()


def render_header(style: _AnsiStyle, title: str, subtitle: str = "") -> str:
    lines = [style.bold(title)]
    if subtitle:
        lines.append(style.dim(subtitle))
    return render_box(lines, WIDTH, double=True)


def render_question(
    style: _AnsiStyle,
    q: Question,
    progress: str,
    audience: str,
) -> str:
    header = style.bold(f"[{q.bank_slug} / {audience}] {q.id}")
    wrapped = _wrap_text(q.question_text, WIDTH - 4)
    body_lines = [header, "", *wrapped, ""]
    if q.purpose:
        body_lines.append(style.dim(f"why: {q.purpose}"))
    if q.choices:
        body_lines.append("")
        body_lines.append(style.cyan("choices:"))
        for idx, c in enumerate(q.choices, 1):
            body_lines.append(f"  {idx}. {c}")
    body_lines.append("")
    body_lines.append(style.dim(f"progress: {progress}"))
    body_lines.append(style.dim("[:b back] [:s skip] [:w where] [:p preview] [:q quit] [:h help]"))
    return render_box(body_lines, WIDTH)


def _wrap_text(text: str, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for w in words:
        if not current:
            current = w
        elif len(current) + 1 + len(w) <= width:
            current = current + " " + w
        else:
            lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


# --------------------------------------------------------------------------- #
# Answer validation                                                            #
# --------------------------------------------------------------------------- #

def validate_answer(q: Question, raw: str) -> tuple[bool, Any, str]:
    """Return (ok, parsed_value, error_message)."""
    s = raw.strip()
    if q.answer_type == "boolean":
        lowered = s.lower()
        if lowered in {"y", "yes", "true", "t", "1"}:
            return True, True, ""
        if lowered in {"n", "no", "false", "f", "0"}:
            return True, False, ""
        return False, None, "Enter yes/no (y/n)."
    if q.answer_type == "numeric":
        if s == "":
            return False, None, "Enter a number."
        try:
            return True, float(s) if "." in s else int(s), ""
        except ValueError:
            return False, None, "Not a valid number."
    if q.answer_type == "single_choice":
        if s.isdigit():
            idx = int(s)
            if 1 <= idx <= len(q.choices):
                return True, q.choices[idx - 1], ""
            return False, None, f"Choose 1..{len(q.choices)}."
        if s in q.choices:
            return True, s, ""
        return False, None, f"Unknown choice. Valid: {', '.join(q.choices)}."
    if q.answer_type == "multi_choice":
        if not s:
            return True, [], ""
        parts = [p.strip() for p in s.split(",") if p.strip()]
        selected: list[str] = []
        for p in parts:
            if p.isdigit():
                idx = int(p)
                if 1 <= idx <= len(q.choices):
                    selected.append(q.choices[idx - 1])
                else:
                    return False, None, f"Index {idx} out of range."
            elif p in q.choices:
                selected.append(p)
            else:
                return False, None, f"Unknown choice: {p}"
        return True, selected, ""
    if q.answer_type == "document_request":
        # The operator can reply with the path to a provided doc, or the word
        # "missing" (or free text explaining the doc is not in hand).
        return True, s or None, ""
    # free_text
    return True, s, ""


# --------------------------------------------------------------------------- #
# Interactive driver                                                           #
# --------------------------------------------------------------------------- #

HELP_TEXT = """\
Shortcuts:
  :b   back one question (navigates, does not delete prior answer)
  :s   skip this question (recorded as skipped)
  :w   show where this answer will land (target_overlay_ref)
  :p   render current proposed diff preview and stop interview
  :q   save and quit
  :h   this help
"""


def run_interactive(args: argparse.Namespace) -> int:
    """Main interactive entry point. Returns process exit code."""
    style = _AnsiStyle()
    banks = load_question_banks()
    if not banks:
        print(style.red("No question banks found under tailoring/question_banks/."))
        return 2
    doc_catalog = load_doc_catalog()

    session = _pick_session(args, banks, style)
    if session is None:
        return 0

    banks_in_order = [banks[s] for s in session.audiences_scheduled if s in banks]
    if not banks_in_order:
        print(style.red("Scheduled audiences do not match any loaded banks."))
        return 2

    # Main loop
    quit_requested = False
    preview_requested = False
    for bank in banks_in_order:
        if bank.bank_slug in session.audiences_completed:
            continue
        session.current_audience = bank.bank_slug

        # Build the question queue; include follow-ups dynamically.
        queue = [q.id for q in bank.questions]
        idx = 0
        # If resuming, start at current_question_id when it belongs to this bank.
        if session.current_question_id and session.current_question_id in queue:
            idx = queue.index(session.current_question_id)

        while idx < len(queue):
            qid = queue[idx]
            q = next((qq for qq in bank.questions if qq.id == qid), None)
            if q is None:
                idx += 1
                continue
            session.current_question_id = qid
            clear_screen()
            _render_screen(session, banks, bank, q, style)
            prompt = style.yellow(f"\nanswer [{q.answer_type}] > ")
            try:
                raw = input(prompt)
            except EOFError:
                raw = ":q"
            if raw == ":q":
                quit_requested = True
                break
            if raw == ":h":
                print(HELP_TEXT)
                input("press enter to continue ")
                continue
            if raw == ":b":
                idx = max(0, idx - 1)
                continue
            if raw == ":s":
                session.answers[q.id] = {
                    "value": None,
                    "skipped": True,
                    "answered_at": _now(),
                    "confidence": "low",
                }
                session.save()
                idx += 1
                continue
            if raw == ":w":
                print(style.cyan(f"target_overlay_ref: {q.target_overlay_ref}"))
                input("press enter to continue ")
                continue
            if raw == ":p":
                preview_requested = True
                break
            ok, value, err = validate_answer(q, raw)
            if not ok:
                print(style.red(f"  ! {err}"))
                input("press enter to retry ")
                continue
            pending_doc = False
            if q.answer_type == "document_request":
                doc_missing = _is_missing_response(raw)
                if doc_missing and q.missing_doc_triggers:
                    _trigger_missing_docs(
                        session=session,
                        q=q,
                        catalog=doc_catalog,
                        style=style,
                    )
                    pending_doc = True
            session.answers[q.id] = {
                "value": value,
                "skipped": False,
                "pending_doc": pending_doc,
                "answered_at": _now(),
                "confidence": _derive_confidence(q, value),
            }
            # Prepend follow-ups to remaining queue.
            for fid in q.follow_up_ids:
                if fid not in queue[idx + 1 :]:
                    queue.insert(idx + 1, fid)
            session.save()
            idx += 1

        if quit_requested or preview_requested:
            break
        session.audiences_completed.append(bank.bank_slug)
        session.current_question_id = None

    session.save()
    # Render preview and sign-off handling.
    _finalize(session, banks, style)
    return 0


def _is_missing_response(raw: str) -> bool:
    s = raw.strip().lower()
    return s in {"", "missing", "none", "n/a", "na", "no", "not yet", "tbd"}


def _derive_confidence(q: Question, value: Any) -> str:
    if value is None:
        return "low"
    if q.answer_type in {"single_choice", "multi_choice", "boolean"}:
        return "high"
    if q.answer_type == "numeric":
        return "medium"
    if q.answer_type == "document_request":
        return "medium"
    return "medium"


def _pick_session(
    args: argparse.Namespace, banks: dict[str, Bank], style: _AnsiStyle
) -> Session | None:
    # Resume if session-id passed and it exists.
    if args.session_id:
        existing = load_session_by_id(args.org_id, args.session_id)
        if existing:
            print(style.green(f"Resuming session {existing.session_id} for {existing.org_id}."))
            return existing
        print(style.yellow(
            f"Session {args.session_id} not found; starting new."
        ))
    # Auto-resume latest unless --new.
    if not args.new:
        latest = find_latest_session(args.org_id)
        if latest and not args.dry_run:
            print(style.green(
                f"Resuming latest session {latest.session_id} for {latest.org_id}."
            ))
            return latest
    # New session.
    audiences = args.audiences or list(banks.keys())
    audiences = [a for a in audiences if a in banks]
    if not audiences:
        print(style.red("No valid audiences; exiting."))
        return None
    session_id = args.session_id or new_session_id(
        audience=audiences[0] if audiences else None
    )
    session = Session(
        org_id=args.org_id,
        session_id=session_id,
        audiences_scheduled=audiences,
    )
    session.save()
    print(style.green(
        f"Created new session {session.session_id} for {session.org_id}."
    ))
    return session


def _render_screen(
    session: Session,
    banks: dict[str, Bank],
    bank: Bank,
    q: Question,
    style: _AnsiStyle,
) -> None:
    header = render_header(
        style,
        f"Tailoring Interview — {session.org_id}",
        f"session {session.session_id}  audience {bank.audience}",
    )
    completeness = completeness_by_audience(session, banks)
    stats = completeness.get(bank.bank_slug, {"answered": 0, "total": len(bank.questions)})
    progress = render_progress_bar(stats["answered"], stats["total"])
    question_box = render_question(style, q, progress, audience=bank.audience)
    print(header)
    print()
    print(question_box)


def _trigger_missing_docs(
    *,
    session: Session,
    q: Question,
    catalog: dict[str, dict[str, Any]],
    style: _AnsiStyle,
) -> None:
    queue = load_queue(MISSING_DOCS_QUEUE_PATH)
    for slug in q.missing_doc_triggers:
        doc = catalog.get(slug)
        if not doc:
            print(style.red(
                f"Doc catalog missing entry for slug '{slug}'. "
                f"Add it to tailoring/doc_catalog.yaml before continuing."
            ))
            continue
        if slug in session.missing_docs_opened:
            continue
        priority = _guess_priority(q, doc)
        append_missing_doc(
            queue,
            doc_slug=slug,
            doc_title=str(doc.get("doc_title", slug)),
            requested_from_role=_requested_from_role_for_bank(q.bank_slug),
            priority=priority,
            used_by_overlay_keys=list(doc.get("overlay_keys_filled") or []),
            substitute_behavior=_substitute_behavior_for(doc),
            org_id=session.org_id,
            session_id=session.session_id,
            notes=(
                f"Opened from question {q.id} in the {q.bank_slug} bank. "
                f"Target overlay key: {q.target_overlay_ref}."
            ),
        )
        session.missing_docs_opened.append(slug)
        print(style.yellow(
            f"  + missing_doc queued: {slug} ({priority}) for role "
            f"{_requested_from_role_for_bank(q.bank_slug)}"
        ))
    save_queue(MISSING_DOCS_QUEUE_PATH, queue)


def _guess_priority(q: Question, doc: dict[str, Any]) -> str:
    # Approval-matrix-related docs and org chart are p1 by default.
    slug = str(doc.get("doc_slug", ""))
    if slug in {"approval_matrix", "org_chart", "property_list"}:
        return "p1"
    if slug in {"budget_template", "forecast_template", "chart_of_accounts_mapping",
                "capex_approval_policy", "pma_template", "vendor_policy",
                "development_budget_template", "construction_draw_template"}:
        return "p2"
    return "p3"


def _requested_from_role_for_bank(bank_slug: str) -> str:
    mapping = {
        "coo": "coo_operations_leader",
        "cfo": "cfo_finance_leader",
        "regional_ops": "regional_manager",
        "asset_mgmt": "asset_manager",
        "development": "development_manager",
        "construction": "construction_manager",
        "reporting": "reporting_finance_ops_lead",
    }
    return mapping.get(bank_slug, "coo_operations_leader")


def _substitute_behavior_for(doc: dict[str, Any]) -> str:
    slug = str(doc.get("doc_slug", ""))
    if slug in {"approval_matrix", "org_chart"}:
        return "refuse"
    return "use_defaults"


# --------------------------------------------------------------------------- #
# Finalization — diff preview, sign-off queue, summary                         #
# --------------------------------------------------------------------------- #

def _finalize(
    session: Session, banks: dict[str, Bank], style: _AnsiStyle
) -> None:
    current = load_current_overlay(session.org_id)
    proposed = build_proposed_overlay(session, banks, current)
    diff = compute_diff(current, proposed, session, banks)
    if not diff:
        print(style.dim("No changes to propose; overlay matches current state."))
        _export_summary(session, banks, diff, preview_only=True)
        return
    print(style.bold("\nDiff preview\n"))
    for entry in diff:
        print(_render_diff_entry(entry, style))
        print()
    sign_off_queue = load_queue(SIGN_OFF_QUEUE_PATH)
    for entry in diff:
        record = append_sign_off(
            sign_off_queue,
            entry=entry,
            org_id=session.org_id,
            session_id=session.session_id,
        )
        session.sign_offs_opened.append(record["queue_entry_id"])
    save_queue(SIGN_OFF_QUEUE_PATH, sign_off_queue)
    session.save()
    _export_summary(session, banks, diff, preview_only=False)
    print(style.green(
        f"\n{len(diff)} sign-off queue entries opened. "
        f"Nothing was written to overlays/org/{session.org_id}/."
    ))


def _render_diff_entry(entry: DiffEntry, style: _AnsiStyle) -> str:
    header = style.bold(f"@@ {entry.overlay_key}")
    if entry.approval_matrix_row is not None:
        header += style.dim(f"  ~~ approval_matrix row {entry.approval_matrix_row}")
    prior = style.red(f"-  {entry.overlay_key}: {entry.prior_value!r}")
    proposed = style.green(f"+  {entry.overlay_key}: {entry.proposed_value!r}")
    meta = [
        f"   ^ approver_role: {entry.approver_role or 'unspecified'}",
        f"   ^ rationale: {entry.rationale}",
        f"   ^ source: {entry.interview_source}",
    ]
    return "\n".join([header, prior, proposed, *meta])


def _export_summary(
    session: Session,
    banks: dict[str, Bank],
    diff: list[DiffEntry],
    preview_only: bool,
) -> None:
    completeness = completeness_by_audience(session, banks)
    lines: list[str] = []
    lines.append(f"# Tailoring session summary — {session.org_id}")
    lines.append("")
    lines.append(f"- session_id: `{session.session_id}`")
    lines.append(f"- created_at: {session.created_at}")
    lines.append(f"- updated_at: {session.updated_at}")
    lines.append(f"- audiences_scheduled: {', '.join(session.audiences_scheduled)}")
    lines.append(f"- audiences_completed: {', '.join(session.audiences_completed) or '(none)'}")
    lines.append("")
    lines.append("## Completeness by audience")
    lines.append("")
    lines.append("| Audience | Total | Answered | Pending doc | Score |")
    lines.append("|---|---|---|---|---|")
    for slug, stats in completeness.items():
        lines.append(
            f"| {slug} | {stats['total']} | {stats['answered']} "
            f"| {stats['pending_doc']} | {stats['score_excluding_pending']:.0%} |"
        )
    lines.append("")
    lines.append("## Missing docs opened this session")
    lines.append("")
    if session.missing_docs_opened:
        for slug in session.missing_docs_opened:
            lines.append(f"- {slug}")
    else:
        lines.append("- (none)")
    lines.append("")
    lines.append("## Proposed diff")
    lines.append("")
    if not diff:
        lines.append("- (no changes)")
    else:
        lines.append("| Overlay key | Prior | Proposed | Approver | Row |")
        lines.append("|---|---|---|---|---|")
        for e in diff:
            lines.append(
                f"| `{e.overlay_key}` | `{e.prior_value!r}` | `{e.proposed_value!r}` "
                f"| {e.approver_role or '-'} | {e.approval_matrix_row or '-'} |"
            )
    lines.append("")
    if preview_only:
        lines.append("Preview only. No sign-off queue entries were opened in this render.")
    else:
        lines.append(
            "Sign-off queue entries were opened for each diff row. The commit of approved "
            "entries to `overlays/org/{org_id}/overlay.yaml` is handled by a separate tool."
        )
    lines.append("")
    path = session.summary_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# --------------------------------------------------------------------------- #
# CLI                                                                          #
# --------------------------------------------------------------------------- #

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Residential multifamily org-overlay tailoring TUI.",
    )
    parser.add_argument("--org-id", required=True, help="Operator org slug.")
    parser.add_argument("--session-id", help="Resume this session id.")
    parser.add_argument("--new", action="store_true", help="Force a new session.")
    parser.add_argument(
        "--audiences",
        nargs="*",
        help="Explicit audience slugs to cover; default is all.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Load banks and session only, do not prompt interactively.",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI color output.",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.no_color:
        os.environ["NO_COLOR"] = "1"
    if args.dry_run:
        return _dry_run(args)
    return run_interactive(args)


def _dry_run(args: argparse.Namespace) -> int:
    style = _AnsiStyle(enabled=False)
    banks = load_question_banks()
    catalog = load_doc_catalog()
    report = {
        "org_id": args.org_id,
        "banks_loaded": {slug: len(bank.questions) for slug, bank in banks.items()},
        "doc_catalog_entries": len(catalog),
        "current_overlay_keys": sorted(load_current_overlay(args.org_id).keys()),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
