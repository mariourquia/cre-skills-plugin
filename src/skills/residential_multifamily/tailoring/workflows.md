# Workflows — tailoring

The tailoring pack is invoked directly by the router; it does not invoke role or workflow packs. The interview flow itself is a workflow and is documented in depth in `INTERVIEW_FLOW.md`. This file lists the workflow entry points and their trigger conditions.

| Workflow | Cadence | Trigger |
|---|---|---|
| `new_org_onboarding` | once per new org | router detects `org_id` with no overlay under `overlays/org/{org_id}/` |
| `refresh_audience` | ad hoc | leadership change; new fund vehicle; new segment; management-mode shift |
| `process_missing_docs_queue` | on demand | user-initiated; or automation detects p1 queue entry blocking output |
| `resume_session` | ad hoc | session file exists under `tailoring/sessions/{org_id}/` |
| `render_diff_preview` | end of interview | audience complete or user ends session |
| `open_sign_off_queue_entry` | per proposed change | diff contains a change that routes through approval_matrix |
| `export_summary` | end of session | always, after diff preview |

## Workflow process — new_org_onboarding

1. Accept `org_id`. Confirm it does not have an overlay under `overlays/org/{org_id}/`.
2. Bootstrap session state from `overlays/org/_defaults/` and an empty answer set.
3. Select audiences to cover; sequence them.
4. Run each audience's question bank in order.
5. Detect missing docs; add to `missing_docs_queue.yaml`.
6. At audience end, render diff preview.
7. Open sign-off queue entries.
8. Export session summary.

## Workflow process — refresh_audience

1. Accept `org_id` and target audience slug.
2. Load existing `overlays/org/{org_id}/overlay.yaml`. If absent, fall back to `new_org_onboarding`.
3. Run only the specified audience's question bank. Pre-fill answers from the existing overlay.
4. For any pre-filled answer the interviewer re-answers, track it as an update proposal.
5. Render diff preview scoped to updated keys only.
6. Open sign-off entries.
7. Export summary.

## Workflow process — process_missing_docs_queue

1. Load `missing_docs_queue.yaml`; filter to entries with `status: open` or `status: received`.
2. For each `received` entry, offer to parse. If `doc_catalog.yaml` declares an `ingest_handler` of `automated_parse`, run it; otherwise prompt the user to walk through the document.
3. Update dependent overlay keys with `pending_doc` removed.
4. Render diff preview scoped to updated keys.
5. Open sign-off entries.
6. Mark queue entries `parsed` or `closed` as appropriate.

## Edge cases

- **Two sessions open simultaneously for the same org.** The session files are distinct; conflict is resolved at sign-off time by the external commit tool, not here.
- **User answers a question with "not applicable" or "unknown".** The answer is recorded; the target overlay key is left at the default (if any) and flagged `low_confidence`.
- **Answer implies a policy that the approval matrix forbids.** The skill refuses, explains which floor is binding, and offers alternatives inside the floor.
- **Question bank has been updated since last session.** On resume, new questions are prepended to the remaining queue with a "new since last session" marker.

## Failure modes

1. **Question bank YAML malformed.** The TUI validates schema on load; a malformed bank blocks the interview and surfaces the offending entry.
2. **Missing doc catalog entry.** If a question's `missing_doc_triggers` references a `doc_slug` not in `doc_catalog.yaml`, the TUI refuses the trigger and surfaces the catalog gap.
3. **Session resume with altered target_overlay_ref.** If a question's target path has moved, the TUI surfaces the mismatch and asks the user to re-answer.
4. **Sign-off approver role unavailable.** The sign-off queue entry still opens; the external approver notification flow is not part of this pack.
