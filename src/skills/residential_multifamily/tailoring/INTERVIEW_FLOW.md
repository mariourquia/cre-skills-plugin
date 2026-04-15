# Interview Flow

This document describes how the terminal UI sequences audiences, branches on answers, handles partial completion, resumes across sessions, and persists state.

## Session lifecycle

A session is the unit of interview work. Each session is identified by:

- `org_id` — the organization the overlay is for.
- `session_id` — time-based slug plus audience hint, for example `20260415_acme_coo_01`. The TUI generates this automatically on new sessions.

Session state is persisted to `tailoring/sessions/{org_id}/{session_id}.yaml`. This directory is listed in `.gitignore`; session files are operator-private by default and are not committed. If an organization wants to retain session state under version control, the `.gitignore` entry must be removed deliberately in a separate commit.

## Session state file shape

```yaml
org_id: acme_mf
session_id: 20260415_acme_coo_01
created_at: 2026-04-15T16:00:00Z
updated_at: 2026-04-15T17:32:10Z
audiences_scheduled: [coo]
audiences_completed: []
current_audience: coo
current_question_id: coo_007
answers:
  coo_001:
    value: self_managed
    answered_at: 2026-04-15T16:02:15Z
    confidence: high
  coo_002:
    value: "n/a - all self-managed"
    answered_at: 2026-04-15T16:02:30Z
    confidence: high
pending_doc_keys:
  - overlay.yaml#org_chart_ref
missing_docs_opened:
  - org_chart
sign_offs_opened: []
completeness_by_audience:
  coo:
    total: 30
    answered: 7
    pending_doc: 1
    score_excluding_pending: 0.23
notes: |
  Operator paused after coo_007; will resume same day with regional after lunch.
```

## Audience sequencing

When a session is started, the user selects one or more audiences. The TUI sequences them in the order selected. Within an audience, the TUI runs questions in bank-declared order. A question may declare `follow_up_ids`; when a matching answer is given, those follow-ups are prepended to the remaining queue.

Default sequencing recommendation (not enforced):

1. COO — sets approval matrix, service standards, staffing, and portfolio segmentation.
2. CFO — sets finance, reporting calendar, investor reporting.
3. Regional Ops — sets regional cadences and staffing detail.
4. Asset Mgmt — sets watchlist, capex policy, sell/hold/refi triggers.
5. Development — sets dev criteria and pro forma norms.
6. Construction — sets draw, change order authority, contract norms.
7. Reporting — sets platform and automation current state.

The operator may re-order freely; the TUI does not force a sequence.

## Branching on answers

Branches come in three flavors:

- **Follow-up questions.** A question's `follow_up_ids` list; triggered when the answer is non-empty. Branches that depend on specific values should be encoded as separate follow-ups whose `purpose` field explains the condition; the TUI surfaces the follow-up and the operator may skip if inapplicable.
- **Doc triggers.** A question's `missing_doc_triggers`; triggered when the answer is a `document_request` or when the operator explicitly indicates a document is not in hand.
- **Skip rules.** Every question is skippable. A skip is recorded as `answer.value = null`, `answer.skipped = true`. Skipped questions count against completeness unless the session is marked `partial` explicitly.

## Partial completion and resume

The session is saved after every answer. If the TUI is closed, the operator resumes with `python3 tools/tailoring_tui.py --org-id {org_id} --session-id {session_id}`. On resume:

1. The TUI loads the session YAML.
2. The TUI checks for question-bank version drift. If the bank version differs from the version recorded at session start, new questions are appended to the remaining queue and marked "added since last session".
3. The TUI rewinds to the `current_question_id`.
4. The operator continues.

Resuming without specifying `--session-id` re-opens the most recent session file in `tailoring/sessions/{org_id}/`. If the operator wants a fresh session, they pass `--new`.

## Navigation

At any prompt the operator may:

- `:b` — back one question (does not undo the last answer unless explicitly requested).
- `:s` — skip this question.
- `:q` — save and quit.
- `:w` — show "where this answer will go" (target_overlay_ref).
- `:p` — preview the current proposed diff.
- `:h` — inline help.

## Diff preview and sign-off at end of audience

When an audience is fully answered (or the operator invokes `:p`), the TUI:

1. Computes the diff per `PREVIEW_PROTOCOL.md`.
2. Renders the diff.
3. Asks the operator to confirm. On confirm, the TUI opens sign-off queue entries and writes a session summary.
4. On reject, the TUI returns to the interview; answers are not deleted.

## Cross-session missing-docs queue

`missing_docs_queue.yaml` is cross-session. A p1 entry opened during the COO interview in one session will still be there when the reporting lead starts their interview in a later session. The TUI surfaces existing queue entries at session start so the operator knows what is outstanding.

## Persistence rules

- Answers are written to disk on every change.
- The diff preview triggers a re-save before rendering.
- Sign-off queue entries are flushed on every audience completion, not only at session end.
- Session summary is re-written on every diff preview; the last render wins.

## Graceful degradation

The TUI degrades if stdout is not a TTY:

- Borders and ANSI color escape codes are suppressed.
- Input is read line-by-line from stdin with no raw-mode control codes.
- `:` shortcuts still work but are announced explicitly at each prompt.

This makes the TUI runnable under CI or non-interactive inspection (for example, piping answers from a test fixture).

## Error handling

- Malformed question bank YAML: the TUI reports the offending file and question, and refuses to start the session.
- Missing `doc_slug` in doc catalog: the TUI reports the gap and asks the operator to add it to the catalog before continuing.
- Session file corruption: the TUI backs up the file to `{session_id}.yaml.corrupt_{timestamp}` and starts a new session. No data is lost silently.
