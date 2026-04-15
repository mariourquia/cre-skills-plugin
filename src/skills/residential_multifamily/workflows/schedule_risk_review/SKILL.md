---
name: Schedule Risk Review
slug: schedule_risk_review
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Duration assumptions by trade and market drift. Overlay governs materiality thresholds
  on schedule variance. Lease-up and construction stabilization interlocks change with
  market conditions.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [development, construction, renovation, lease_up]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [construction_manager, development_manager, asset_manager, estimator_preconstruction_lead]
  output_types: [memo, kpi_review]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/normalized/construction_duration_assumptions__{region}.csv
    - reference/normalized/approval_threshold_defaults.csv
  writes: []
metrics_used:
  - schedule_variance_days
  - milestone_slippage_rate
  - punchlist_closeout_rate
  - lease_up_pace_post_delivery
  - stabilization_pace_vs_plan
escalation_paths:
  - kind: schedule_slip_above_threshold
    to: construction_manager -> asset_manager -> executive
  - kind: critical_path_disruption
    to: construction_manager + asset_manager -> approval_request per overlay
approvals_required:
  - schedule_rebaseline
description: |
  Reviews current schedule against baseline, identifies critical-path risks, recomputes
  completion and stabilization probability, and routes a rebaseline proposal when
  warranted. Integrates with `workflows/cost_to_complete_review` and
  `workflows/draw_package_review` for financial consequences.
---

# Schedule Risk Review

## Workflow purpose

Keep the project schedule honest. Measure slip, name the cause, quantify the cost and lease-up downstream impact, and route any rebaseline.

## Trigger conditions

- **Explicit:** "run schedule risk", "what's the slip", "rebaseline proposal".
- **Implicit:** milestone slipped vs. baseline; critical-path disruption; weather delay beyond overlay tolerance; lease-up pace approaching stabilization deadline.
- **Recurring:** monthly per active project.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Current schedule | record | required | |
| Baseline schedule | record | required | |
| Milestone record | table | required | baseline vs. current forecast |
| Critical-path disruption log | log | optional | |
| Duration assumption overlay | csv | required | |
| Lease-up plan (if applicable) | record | optional | |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Schedule delta view | `kpi_review` | `schedule_variance_days`, `milestone_slippage_rate` |
| Critical-path memo | `memo` | cause, cost impact, lease-up impact |
| Rebaseline proposal | `memo` | with approval path |
| Lease-up delivery scenario | `kpi_review` | `lease_up_pace_post_delivery` / `stabilization_pace_vs_plan` |

## Required context

Asset_class, segment, form_factor, market, project.

## Process

1. **Compute schedule delta.** `schedule_variance_days` and `milestone_slippage_rate`.
2. **Classify cause.** Trade delay, material lead time, permit, weather, design, labor, owner decision.
3. **Critical-path analysis.** Determine whether slip is on critical path.
4. **Cost consequence.** Link to `workflows/cost_to_complete_review` (escalation, labor, carry cost).
5. **Lease-up consequence (if applicable).** Link to `lease_up_pace_post_delivery` and `stabilization_pace_vs_plan`.
6. **Rebaseline recommendation.** If slip exceeds overlay threshold, recommend rebaseline; opens `approval_request` per overlay.
7. **Confidence banner.** References surfaced.

## Metrics used

`schedule_variance_days`, `milestone_slippage_rate`, `punchlist_closeout_rate`, `lease_up_pace_post_delivery`, `stabilization_pace_vs_plan`.

## Reference files used

- `reference/normalized/construction_duration_assumptions__{region}.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Escalation points

- Slip above overlay: CM -> AM -> executive.
- Critical-path disruption: CM + AM approval per overlay.

## Required approvals

- Schedule rebaseline.

## Failure modes

1. Slip view without critical-path analysis. Fix: step is mandatory.
2. Missing cost consequence link. Fix: invokes CTC review.
3. Silent rebaseline. Fix: rebaseline is an approval.
4. Lease-up impact ignored. Fix: lease-up scenario mandatory when applicable.

## Edge cases

- **Permit delay at start:** cascading; document clearly.
- **Weather seasonality:** overlay governs expected delays; variance beyond overlay is the flag.
- **Owner-driven delay (design changes):** attribute to owner; cost exposure view distinct.
- **Subcontractor default mid-project:** significant rebaseline likely; escalate.

## Example invocations

1. "Run schedule risk review for Willow Creek."
2. "What's the critical-path slip on the South End renovation?"
3. "Lease-up impact if framing slips 30 days on Riverbend."

## Example outputs

### Output — Schedule risk (abridged, Willow Creek April)

**Slip.** `schedule_variance_days` within overlay band; `milestone_slippage_rate` within band.

**Cause.** One trade's material lead time on one milestone; non-critical path.

**Cost.** Minor carrying cost; CTC review to confirm.

**Lease-up.** No material change to expected TCO.

**Rebaseline.** Not recommended.

**Confidence banner.** `construction_duration_assumptions__southeast@2026-03-31 (starter)`.
