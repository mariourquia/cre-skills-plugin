---
name: Cost-to-Complete Review
slug: cost_to_complete_review
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Labor, material, and escalation references drift; CTC quality depends on freshness.
  Overlay governs materiality of CTC variance and triggers for executive review.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [development, construction, renovation]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [construction_manager, estimator_preconstruction_lead, asset_manager, development_manager]
  output_types: [memo, kpi_review, estimate]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/normalized/capex_line_items__{scope}.csv
    - reference/normalized/labor_rates__{market}.csv
    - reference/normalized/material_costs__{region}_residential.csv
    - reference/derived/contingency_assumptions__{org}.csv
    - reference/normalized/construction_duration_assumptions__{region}.csv
    - reference/normalized/approval_threshold_defaults.csv
  writes: []
metrics_used:
  - cost_to_complete
  - contingency_remaining
  - contingency_burn_rate
  - change_orders_pct_of_contract
  - schedule_variance_days
escalation_paths:
  - kind: ctc_variance_above_threshold
    to: construction_manager -> asset_manager -> executive
  - kind: contingency_exhaustion_risk
    to: construction_manager + asset_manager -> approval_request per overlay
approvals_required:
  - budget_reallocation_above_threshold
description: |
  Recomputes cost-to-complete from current actuals plus remaining scope plus overlay-derived
  escalation and contingency. Compares against prior CTC and the underwriting baseline.
  Identifies the driver (labor, material, scope, duration) and recommends remediation
  (re-estimate, scope trim, re-bid, contingency pull).
---

# Cost-to-Complete Review

## Workflow purpose

Build an accurate, transparent cost-to-complete at any point in the project. Trigger remediation when CTC deviates from plan.

## Trigger conditions

- **Explicit:** "run CTC", "cost-to-complete refresh", "pressure-test the remaining budget".
- **Implicit:** `workflows/draw_package_review` finds CTC drift; `workflows/change_order_review` produces material cost delta; milestone slippage from schedule.
- **Recurring:** monthly per active project; re-run when a CO is reviewed.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Cost-to-date | record | required | from draw or GL |
| Approved COs | table | required | |
| Pending COs | table | required | scenario view |
| Remaining scope | table | required | assemblies, percent complete |
| Schedule update | record | required | for duration-based escalation |
| Prior CTC | record | required | for delta |
| Estimator baseline | estimate | required | |

## Outputs

| Output | Type | Shape |
|---|---|---|
| CTC refresh | `kpi_review` | per trade, per project |
| Driver decomposition | table | labor / material / scope / duration |
| Contingency posture | `kpi_review` | remaining vs. plan |
| Scenario set | table | base / upside / downside |
| Recommendation memo | `memo` | remediation and approval path |

## Required context

Asset_class, segment, form_factor, market, project.

## Process

1. **Inherit cost to date.** From most recent draw or GL.
2. **Compute remaining cost.** Remaining scope x unit costs from library; market-adjust via labor/material references; apply escalation per overlay to expected execution dates per schedule.
3. **Apply contingency.** Remaining scope contingency per overlay.
4. **Delta vs. prior CTC.** Attribute to labor, material, scope, duration, CO.
5. **Scenario set.** Base, upside (favorable buyouts, scope value engineering), downside (labor shortage, material spike, additional COs).
6. **Recommendation.** If CTC within overlay, monitor. If above threshold, recommend remediation: re-estimate, scope trim, re-bid, contingency pull. Any budget reallocation above threshold opens approval.
7. **Confidence banner.** References surfaced.

## Metrics used

`cost_to_complete`, `contingency_remaining`, `contingency_burn_rate`, `change_orders_pct_of_contract`, `schedule_variance_days`.

## Reference files used

- `reference/normalized/capex_line_items__{scope}.csv`
- `reference/normalized/labor_rates__{market}.csv`
- `reference/normalized/material_costs__{region}_residential.csv`
- `reference/derived/contingency_assumptions__{org}.csv`
- `reference/normalized/construction_duration_assumptions__{region}.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Escalation points

- CTC variance above overlay threshold: CM -> AM -> executive.
- Contingency exhaustion risk: CM + AM approval request per overlay.
- Budget reallocation above threshold: approval row per overlay.

## Required approvals

- Budget reallocation above threshold.

## Failure modes

1. CTC without escalation. Fix: overlay escalator applied by execution date.
2. CTC without scenario set. Fix: scenario set mandatory.
3. Silent contingency pull. Fix: contingency posture explicit.
4. Ignoring pending COs. Fix: scenario view includes pending.
5. Sample library used as authoritative. Fix: confidence banner surfaces status.

## Edge cases

- **Late-stage value engineering:** scope trim may offset CTC drift; document VE basis.
- **Trade buyout mid-project:** favorable or unfavorable buyout feeds CTC; `trade_buyout_variance` referenced.
- **Force-majeure delay:** duration escalation significant; surface clearly.
- **Multiple stacked COs:** aggregate effect on CTC; stacked approval path.

## Example invocations

1. "Run the April CTC for Willow Creek."
2. "Pressure-test CTC on the South End renovation."
3. "Compare CTC to underwriting baseline for Riverbend."

## Example outputs

### Output — CTC refresh (abridged, Willow Creek April)

**Cost to date.** Inherited.

**Remaining cost.** Market-adjusted, escalated.

**Contingency.** Applied per overlay; remaining within band.

**Delta vs. prior CTC.** Attributed: material drift on two line items; labor hours above baseline on one.

**Scenario set.** Base within overlay. Downside approaches contingency exhaustion if labor shortage persists.

**Recommendation.** Monitor; re-estimate two line items at next draw; no reallocation needed.

**Confidence banner.** `capex_line_items@2026-03-31 (starter)`, `labor_rates__charlotte@2026-03-31 (sample)`, `material_costs__southeast_residential@2026-03-31 (sample)`.
