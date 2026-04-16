# Diff / Approval Preview — Tailoring

The canonical specification for what the tailoring skill shows an operator before applying an org overlay diff. This is the final gate between an answered interview and a committed `overlays/org/{org_id}/` write. Nothing gets committed without passing every check listed here.

This document is the formal spec; `PREVIEW_PROTOCOL.md` is the short-form convention doc already used by the TUI. Both stay in place — `PREVIEW_PROTOCOL.md` covers formatting conventions, this document covers the approval logic that governs whether a preview can progress to apply.

## Overview

The tailoring skill never writes to `overlays/org/{org_id}/` directly. When an audience session completes (or the operator explicitly ends the session), the skill produces a **preview bundle** that contains:

1. The proposed diff in YAML side-by-side form.
2. A canonical-definition reference list.
3. An unresolved-conflicts list (if any).
4. A sign-off matrix mapping each proposed change to an approval-matrix row number and approver role.
5. An approval-floor check result.

The preview bundle is committed to `tailoring/sessions/{org_id}/{session_id}__preview.yaml`. The human-readable version is rendered to `tailoring/sessions/{org_id}/{session_id}__summary.md`. Only after every sign-off queue entry linked to the preview reaches `approved` status may an external commit tool write the overlay. The tailoring skill itself never writes the overlay file.

## 1. Files to be created / updated / unchanged

Every preview opens with a file-action summary:

```
# preview header
org_id: acme_mf
session_id: 20260415_acme_exec_01
audiences_covered: [executive, finance_reporting]
preview_generated_at: 2026-04-15T14:22:00Z

files_to_create:
  - overlays/org/acme_mf/overlay.yaml
  - overlays/org/acme_mf/approval_matrix.yaml
files_to_update: []
files_unchanged:
  - overlays/org/acme_mf/reporting_cadences.yaml   # no answers touched it
```

`files_to_create` is used for new-org onboarding. `files_to_update` is used for refresh sessions on an existing org. `files_unchanged` is listed explicitly so the operator sees that an audience's answers really did not touch a given file (a common source of confusion).

## 2. Canonical definitions referenced

Every proposed overlay key that targets a canonical metric must cite the canonical slug. The preview lists each citation and confirms no redefinition is being attempted.

The following canonical-definition fields are **frozen** — an overlay may retarget a canonical metric's band, but never redefine:

- `numerator` — how the metric is computed in the top-line.
- `denominator` — the base the metric is expressed over.
- `rollup_rule` — how the metric aggregates across unit / property / portfolio.
- `filter_set` — which records are included (e.g., occupied vs all units).
- `unit_of_measure` — $/unit, %, days, ratio.
- `time_basis` — period, as-of, trailing, annualized.

Overlays may set or change: `target_band_low`, `target_band_high`, `alert_threshold`, `escalation_threshold`, `cadence`, `owner_role`, `display_label_alias`.

Preview example:

```
canonical_definitions_referenced:
  - metric_slug: economic_occupancy
    source: _core/metrics.md
    fields_retargeted:
      - target_band_low
      - target_band_high
    fields_frozen_ok: true
  - metric_slug: concession_ratio
    source: _core/metrics.md
    fields_retargeted:
      - alert_threshold
    fields_frozen_ok: true
```

If any proposed answer writes to a frozen field, the preview marks the entry `REDEFINITION_ATTEMPT` and refuses to progress. The answer is routed to `change_log.md` for canonical-core review rather than applied as an overlay.

## 3. Unresolved conflicts

When two audiences give conflicting answers that target the same overlay key, the preview surfaces both with their session IDs. The operator must reconcile before apply.

Example (the case the plan calls out explicitly):

```
unresolved_conflicts:
  - overlay_key: overlay.yaml#concession_policy.max_weeks_free
    conflict:
      - audience: executive
        session_id: 20260415_acme_exec_01
        answer: 2
        answered_by: coo_operations_leader
      - audience: asset_mgmt
        session_id: 20260415_acme_am_01
        answer: 4
        answered_by: asset_manager
    resolution_required: true
    resolution_policy: |
      Executive and asset_mgmt disagree on the concession ceiling. The operator
      must choose one of: (a) accept executive answer and record the override
      in the asset_mgmt session, (b) accept asset_mgmt answer and route a
      sign-off up to COO per approval matrix row 13, or (c) split by segment /
      form_factor / property via an explicit rule set.
```

Policy: conflicts between audiences do **not** auto-resolve. Executive does not automatically win; seniority-of-role tie-breaking would mask a real policy disagreement. The operator sees both and picks.

## 4. Sign-off required items

Every proposed change carries an approval-matrix row number. The row number resolves to an approver role via `_core/approval_matrix.md`. The preview lists each sign-off entry with its row and role:

```
sign_offs_required:
  - change_id: chg_001
    overlay_key: overlay.yaml#approval_matrix.threshold_disbursement_1
    from_value: null
    to_value: 25000
    approval_matrix_row: 6
    approver_role: coo_operations_leader
    sign_off_queue_ref: sign_off_queue.yaml#entry_20260415_acme_exec_chg_001
  - change_id: chg_002
    overlay_key: overlay.yaml#concession_policy.max_weeks_free
    from_value: null
    to_value: 2
    approval_matrix_row: 13
    approver_role: coo_operations_leader
    sign_off_queue_ref: sign_off_queue.yaml#entry_20260415_acme_exec_chg_002
```

Change categories that always require sign-off (not exhaustive):

- `overlay.yaml#approval_matrix.*` → row 6–11 per threshold.
- `overlay.yaml#concession_policy.*` → row 13.
- `overlay.yaml#screening_policy.*` → row 13 + legal counsel.
- `overlay.yaml#vendor_policy.*` → row 19.
- `overlay.yaml#compliance_*` for regulatory programs → row 17 plus compliance officer.
- `overlay.yaml#disbursement_*` thresholds → row 6–7.
- `overlay.yaml#change_order_*` thresholds → row 10–11.

## 5. Approval-floor check

The preview computes, for every threshold in the proposed diff, whether the proposed value would drop the floor below the canonical minimum defined in `_core/approval_matrix.md`.

```
approval_floor_check:
  passed: true
  checks:
    - overlay_key: overlay.yaml#approval_matrix.threshold_disbursement_1
      proposed_value: 25000
      canonical_floor: 0       # canonical has no floor on tier 1 absolute value
      passed: true
    - overlay_key: overlay.yaml#approval_matrix.approvers_tier_1
      proposed_value: [property_manager, regional_manager]
      canonical_floor_approvers: [property_manager, regional_manager]
      passed: true
```

If any check fails, the preview refuses to progress and surfaces the specific row plus a recommended in-floor alternative. The operator cannot override the refusal from inside this skill — a floor change requires a change request against `_core/approval_matrix.md` via the change-log process.

## 6. Preview output format

Short YAML-style diff block (what the operator sees at the end of the preview):

```
--- overlays/org/acme_mf/overlay.yaml  (current: defaults)
+++ overlays/org/acme_mf/overlay.yaml  (proposed)
session_id: 20260415_acme_exec_01
@@ approval_matrix ~~ row 6 ~~ threshold_disbursement_1 ~~ approver: coo_operations_leader
- threshold_disbursement_1: null
+ threshold_disbursement_1: 25000
@@ concession_policy ~~ row 13 ~~ max_weeks_free ~~ approver: coo_operations_leader
- max_weeks_free: null
+ max_weeks_free: 2
@@ reporting ~~ row 14 ~~ lender_reporting_cadence ~~ approver: cfo_finance_leader
- lender_reporting_cadence: null
+ lender_reporting_cadence: monthly
```

Each `@@` block carries: section, approval-matrix row number, overlay key, approver role. The format is stable enough that downstream tooling can parse it.

## 7. REFUSE conditions

The preview must refuse to progress — output the refusal reason and stop — when any of the following are true:

1. A proposed change writes to a frozen canonical-definition field (`numerator`, `denominator`, `rollup_rule`, `filter_set`, `unit_of_measure`, `time_basis`).
2. A proposed change drops an approval floor below the canonical minimum defined in `_core/approval_matrix.md`.
3. A proposed change targets a file outside `overlays/org/{org_id}/` (for example, anything under `_core/`, `overlays/segments/`, `overlays/regulatory/`, `reference/`).
4. A proposed change cites an approval-matrix row number that does not exist in `_core/approval_matrix.md`.
5. A `missing_doc_triggers` entry cites a `doc_slug` not present in `tailoring/doc_catalog.yaml`.
6. A p1 missing document is unresolved and the dependent overlay keys are not marked `pending_doc` in the session state.
7. An unresolved conflict between audiences has not been reconciled by the operator.
8. The preview is missing any of the five sections (file action list, canonical citations, conflicts, sign-offs, floor check).

On refusal, the preview writes a `refusal_record` entry into the session file capturing the reason, the offending change_id, and the operator's options (typically: reopen the triggering audience, correct the answer, regenerate preview).

## Cross-references

- `PREVIEW_PROTOCOL.md` — short-form formatting conventions consumed by the TUI.
- `AUDIENCE_MAP.md` — the 8-audience model this preview reconciles across.
- `MISSING_DOC_MATRIX.md` — missing-doc lifecycle feeding `pending_doc` flags.
- `_core/approval_matrix.md` — the canonical floor checked by section 5.
- `_core/metrics.md` — the frozen canonical-definition fields checked by section 2.
- `sign_off_queue.yaml` — the queue that holds each required sign-off until approval.
