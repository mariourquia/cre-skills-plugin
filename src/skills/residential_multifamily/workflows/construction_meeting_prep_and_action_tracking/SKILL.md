---
name: Construction Meeting Prep and Action Tracking
slug: construction_meeting_prep_and_action_tracking
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Meeting cadence and attendee sets are overlay-driven. Action-item taxonomy drifts with
  program structure.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [development, construction, renovation]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [construction_manager, estimator_preconstruction_lead, development_manager, asset_manager]
  output_types: [checklist, memo, email_draft]
  decision_severity_max: recommendation
references:
  reads:
    - reference/normalized/approval_threshold_defaults.csv
  writes: []
metrics_used:
  - schedule_variance_days
  - milestone_slippage_rate
  - change_orders_pct_of_contract
  - cost_to_complete
  - punchlist_closeout_rate
escalation_paths:
  - kind: stale_action_item
    to: construction_manager -> asset_manager
approvals_required: []
description: |
  Prepares weekly or biweekly construction-meeting packets (agenda, data summary, RFI and
  submittal log, COs, schedule status, safety) and tracks action items with owners and
  due dates. Closes the loop by updating status and surfacing stale items.
---

# Construction Meeting Prep and Action Tracking

## Workflow purpose

Reduce meeting time; increase meeting clarity. Produce the agenda, the data pack, and a clean action-item ledger. Follow up reliably.

## Trigger conditions

- **Explicit:** "build the construction meeting pack", "agenda for OAC", "action item update".
- **Implicit:** scheduled meeting date approaching; open action items aging; new RFI or submittal.
- **Recurring:** weekly or biweekly per overlay.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Prior meeting action items | table | required | open and closed |
| Current schedule state | record | required | |
| RFI and submittal log | table | required | |
| Open CO log | table | required | |
| Safety log | table | required | |
| Budget and CTC summary | record | required | |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Meeting agenda | `checklist` | topics, owner, time box |
| Data pack | `memo` | KPIs, schedule, budget, RFI, CO, safety |
| Action-item ledger update | table | status, owner, due date |
| Action-item reminders | `email_draft` | for stale items |

## Required context

Asset_class, segment, form_factor, market, project.

## Process

1. **Agenda compose.** From overlay template + open items.
2. **Data pack compose.** KPI rollup, schedule, budget, RFI, CO, safety.
3. **Action-item review.** Close completed; age open; identify stale (past due).
4. **Reminder drafts.** For each stale item, draft a reminder with owner and due-date nudge.
5. **Meeting follow-up.** Post-meeting capture of new items and decisions.
6. **Confidence banner.** References surfaced.

## Metrics used

`schedule_variance_days`, `milestone_slippage_rate`, `change_orders_pct_of_contract`, `cost_to_complete`, `punchlist_closeout_rate`.

## Reference files used

- `reference/normalized/approval_threshold_defaults.csv`

## Escalation points

- Stale action item: CM -> AM.

## Required approvals

None by default; any decisions captured in meeting minutes that trigger approvals (e.g., scope change) route through relevant workflow.

## Failure modes

1. Meeting without action-item ledger. Fix: ledger is the backbone.
2. Stale items never surfaced. Fix: aging view mandatory.
3. Minutes without decisions captured. Fix: decisions separate from discussion in the data pack template.

## Edge cases

- **Absent owner for a critical item:** escalate to next level in overlay.
- **Item crossing multiple trades:** cross-reference in ledger.
- **Cancelled meeting:** action-item cadence continues; asynchronous updates recorded.

## Example invocations

1. "Build the OAC pack for Willow Creek this Wednesday."
2. "Stale action items across Riverbend construction."
3. "Update the action ledger after Thursday's meeting."

## Example outputs

### Output — OAC meeting pack (abridged, Willow Creek)

**Agenda.** Safety, schedule, RFIs, submittals, COs, budget / CTC, punch, action items.

**Data pack.** KPI snapshot; `schedule_variance_days` and `milestone_slippage_rate` within band; RFI and submittal log counts; CO log with rows 10/11 status; safety log clean; CTC within overlay.

**Action-item ledger.** Closed 6 items; opened 3; aged 2 stale; reminder drafts prepared.

**Confidence banner.** `approval_threshold_defaults@2026-03-31 (starter)`.
