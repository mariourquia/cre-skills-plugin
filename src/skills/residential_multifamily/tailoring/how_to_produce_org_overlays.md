# How to produce org overlays

The tailoring skill does not write directly to `overlays/org/{org_id}/`. Overlay production is a three-step flow, each with explicit boundaries.

## Step 1 — Read the starting template

The tailoring skill reads `overlays/org/_defaults/` as the starting template for any new organization. The defaults are canonical starters — placeholders in most fields, plus the canonical structure expected by `_core/schemas/overlay_manifest.yaml`. The defaults are not policy; they are the shape of an overlay with its required keys enumerated and its placeholders explicit.

## Step 2 — Produce a diff from the interview

Running the interview (see `SKILL.md` and `INTERVIEW_FLOW.md`) produces answers that populate proposed overlay keys. The TUI computes a diff between:

- **Current state.** The existing `overlays/org/{org_id}/overlay.yaml`, or `overlays/org/_defaults/overlay.yaml` for a new org.
- **Proposed state.** The session's proposed overlay keys, excluding any key flagged `pending_doc`.

The diff is rendered per `PREVIEW_PROTOCOL.md` and displayed to the operator. No file under `overlays/org/{org_id}/` is mutated by this step.

## Step 3 — Sign-off queue mediates the write

Each `added` or `modified` diff entry opens a `sign_off_queue.yaml` entry with an `approver_role` that matches the approval matrix row for the change. Approvers use an external tool to review and mark entries `approved` or `rejected`.

Only after a sign-off queue entry is in `approved` status may a commit tool (outside the tailoring pack) apply the change to `overlays/org/{org_id}/overlay.yaml`, writing a corresponding change log entry. The tailoring pack's contract ends at the sign-off queue.

## What is never mutated

- `_core/` — canonical core. Never mutated by the tailoring pack or by any overlay-writing tool. Changes to canonical concepts go through `_core/change_log_conventions.md`.
- `overlays/org/_defaults/` — the starting template. Never mutated by the tailoring pack. Changes to defaults require a core-level change log entry.

## What the operator gets out

After a successful interview and sign-off, the operator has:

- `overlays/org/{org_id}/overlay.yaml` — a complete organizational overlay conforming to the overlay manifest schema, with overrides traceable to interview answers.
- `overlays/org/{org_id}/change_log.md` — a per-org change log that captures every approved sign-off entry with approver, date, and rationale.
- `tailoring/sessions/{org_id}/*.yaml` — session transcripts (operator-private by default; not committed).
- `tailoring/missing_docs_queue.yaml` — cross-session record of outstanding document requests for this org.

## Worked flow for a new org

```
user: "Onboard Acme Multifamily as a new operator."
tailoring TUI:
  1. Accepts org_id=acme_mf.
  2. Detects no overlays/org/acme_mf/ directory.
  3. Bootstraps session state from overlays/org/_defaults/overlay.yaml.
  4. Runs COO audience (30 questions).
     - Operator answers 22 of 30; 3 trigger missing_doc entries; 5 skipped.
  5. Renders diff preview: 14 added keys, 0 modified.
  6. Opens 14 sign-off queue entries; approver_role=coo_operations_leader for 11,
     portfolio_manager for 2, legal_counsel for 1 (approval floor crossing).
  7. Writes session summary to tailoring/sessions/acme_mf/20260415_acme_coo_01__summary.md.
approver:
  1. Opens sign_off_queue.yaml; marks 13 entries approved, 1 rejected.
external commit tool:
  1. Reads approved sign-off entries.
  2. Creates overlays/org/acme_mf/overlay.yaml with the 13 approved keys.
  3. Writes overlays/org/acme_mf/change_log.md with 13 entries.
tailoring TUI (next session):
  1. Shows rejected entry and remaining missing_docs_queue items.
  2. Operator continues with regional_ops audience.
```

## When to re-interview

- Leadership change (new COO, CFO, CEO) — refresh that audience.
- New fund vehicle — refresh CFO and asset_mgmt.
- New segment (operator adds luxury properties) — refresh COO and asset_mgmt.
- Management-mode shift (self-managed to third-party-managed) — refresh COO and asset_mgmt.
- Every 12 months — refresh COO and CFO.
- Every 24 months — refresh asset_mgmt, development, construction, reporting.

These cadences live in `overlays/org/{org_id}/overlay.yaml` under `tailoring.refresh_cadences` once the initial interview is complete. Until then, the defaults apply.
