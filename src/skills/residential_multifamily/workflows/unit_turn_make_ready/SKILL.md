---
name: Unit Turn and Make-Ready
slug: unit_turn_make_ready
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Turn cost libraries, target cycle times, and vendor rate cards drift with material and
  labor markets. Turn tiers (classic, light refresh, value-add interior) and the scope
  contents of each tier are overlay-driven.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [stabilized, renovation, lease_up, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [property_manager, maintenance_supervisor, regional_manager]
  output_types: [checklist, estimate, operating_review, kpi_review]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/normalized/unit_turn_cost_library__{market}.csv
    - reference/normalized/approved_vendor_list__{market}.csv
    - reference/normalized/vendor_rate_cards__{market}.csv
    - reference/normalized/turn_benchmarks__{market}.csv
    - reference/normalized/approval_threshold_defaults.csv
  writes: []
metrics_used:
  - make_ready_days
  - average_days_vacant
  - turnover_rate
  - turn_cost_by_market
  - repeat_work_order_rate
escalation_paths:
  - kind: disbursement_above_threshold
    to: regional_manager -> asset_manager (rows 6, 7)
  - kind: scope_change_safety
    to: maintenance_supervisor + property_manager + regional_manager (row 4)
  - kind: turn_cycle_breach
    to: maintenance_supervisor -> property_manager -> regional_manager
approvals_required:
  - disbursement_above_threshold
  - scope_change_safety
description: |
  Coordinates the unit turn from move-out handoff to ready-to-show. Selects the scope
  tier, produces the estimate, dispatches trades against the approved vendor list, tracks
  cycle time against benchmarks, and reconciles actuals against the turn cost library.
  Hands off to `workflows/move_in_administration` when the new resident is scheduled.
---

# Unit Turn and Make-Ready

## Workflow purpose

Minimize `make_ready_days` and `average_days_vacant` while hitting scope quality and budget. Produces the turn plan, dispatches the trades, tracks cycle time, and provides the reconciliation back to the turn cost library.

## Trigger conditions

- **Explicit:** "start turn on unit X", "turn pipeline review", "estimate turn cost for unit Y", "unit ready ETA".
- **Implicit:** `workflows/move_out_administration` writes a turn handoff record; a turn project exceeds target cycle time; materials delay detected.
- **Recurring:** weekly turn-pipeline review at property grain.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Turn handoff record | record | required | unit_id, scope tier, damages list |
| Turn cost library | csv | required | per-scope cost ranges by market |
| Approved vendor list | csv | required | by trade |
| Vendor rate cards | csv | required | for estimate |
| Turn benchmarks | csv | required | cycle-time targets |
| Renovation plan (if lifecycle=renovation) | record | optional | scope deltas |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Turn plan | `checklist` | scope, trades, order, durations |
| Turn estimate | `estimate` | by line item, cost range |
| Dispatch log | record | vendor assignments with ETAs |
| Turn pipeline snapshot | `kpi_review` | units in turn by stage, aging |
| Reconciliation | `memo` | actual vs. estimate vs. library |

## Required context

Asset_class, segment, form_factor, lifecycle_stage, management_mode, market.

## Process

1. **Select scope tier.** Pull from the handoff record: classic, light refresh, or value-add interior (renovation). Scope contents read from overlay.
2. **Produce estimate.** Apply turn cost library line items; reconcile against vendor rate cards. Flag any line item outside overlay tolerance.
3. **Cost gate.** If total estimate above threshold, open `approval_request` row 6 or 7 before procurement.
4. **Dispatch sequencing.** Order trades per overlay (demo, punch, paint, flooring, appliances, fixtures, deep clean, final inspection). Licensed-trade verification per `workflows/work_order_triage` gate.
5. **Cycle time tracking.** Compute target vs. actual per unit; breaches escalate to maintenance_supervisor -> property_manager -> regional.
6. **Scope changes (decision point).** Any safety-critical scope change triggers `approval_request` row 4. Any cost change above overlay variance triggers disbursement gate.
7. **Quality inspection.** Final inspection checklist per overlay; unit marked `ready` only when all items pass.
8. **Reconciliation.** Compare actual cost to estimate and to library; propose library updates via reference update flow if systematic drift.
9. **Handoff.** Write ready record; triggers `workflows/move_in_administration` if lease executed.
10. **Pipeline snapshot.** Weekly view: units in turn by stage, aging, breaches.
11. **Confidence banner.** Surface `as_of_date` and `status` for library and rate cards.

## Metrics used

`make_ready_days`, `average_days_vacant`, `turnover_rate`, `turn_cost_by_market`, `repeat_work_order_rate` (if post-turn defects trigger WOs).

## Reference files used

- `reference/normalized/unit_turn_cost_library__{market}.csv`
- `reference/normalized/approved_vendor_list__{market}.csv`
- `reference/normalized/vendor_rate_cards__{market}.csv`
- `reference/normalized/turn_benchmarks__{market}.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Escalation points

- Cycle-time breach: maintenance_supervisor -> property_manager -> regional.
- Safety-critical scope change: row 4.
- Cost above threshold: row 6 or 7.

## Required approvals

- Disbursement above threshold.
- Safety-critical scope deferral (row 4).

## Failure modes

1. Using last quarter's library. Fix: confidence banner surfaces freshness.
2. Dispatching without insurance check. Fix: handoff to `work_order_triage` gate.
3. Reading "ready" without inspection. Fix: ready record only on inspection pass.
4. Library not updated when actuals systematically drift. Fix: reconciliation step proposes update via reference flow.
5. Scope creep without approval. Fix: scope changes routed by kind.

## Edge cases

- **Renovation-tier turn on lease-up property:** scope reads from renovation overlay; pricing per renovation cost library.
- **Prior resident damage beyond schedule:** handoff flagged; turn cost delta covered by final ledger in `workflows/move_out_administration`.
- **Material lead-time issue:** schedule adjusts; PM notified; resident new-move-in communication handled via `workflows/move_in_administration`.
- **Abandoned unit with undisclosed damage:** PM + regional; scope expands; cost gate re-checked.

## Example invocations

1. "Start the classic turn on unit 101 at Ashford Park, vacate 2026-04-30."
2. "Review the turn pipeline for Willow Creek this week; flag any breaches."
3. "Estimate the value-add interior turn for unit 203 at Riverbend."

## Example outputs

### Output — Turn plan and estimate (abridged, unit 101 Ashford Park)

**Scope tier.** Classic turn per handoff record.

**Plan.** Demo, punch, paint, flooring, appliance check, deep clean, final inspection. Target cycle from overlay.

**Estimate.** Line items from library; total within band; no cost gate triggered.

**Dispatch.** Paint + flooring assigned to preferred vendors; licensure current; deep clean on-staff.

**Breach flags.** None at estimate stage.

**Reconciliation commitment.** Post-completion reconciliation will compare actual to estimate and to library; systematic drift proposes library update via reference flow.

**Confidence banner.** `unit_turn_cost_library__charlotte@2026-03-31, status=sample`. `turn_benchmarks__charlotte@2026-03-31, status=starter`.
