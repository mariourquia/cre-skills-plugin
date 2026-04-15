---
name: Change Order Review
slug: change_order_review
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Change order threshold bands (minor / major), contingency rules, and scope-change
  approval paths are overlay-driven.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [renovation, construction, recap_support, lease_up, stabilized, development]
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
    - reference/normalized/approval_threshold_defaults.csv
  writes: []
metrics_used:
  - change_orders_pct_of_contract
  - contingency_remaining
  - contingency_burn_rate
  - cost_to_complete
  - schedule_variance_days
escalation_paths:
  - kind: change_order_minor
    to: construction_manager + asset_manager -> approval_request(row 10)
  - kind: change_order_major
    to: construction_manager + asset_manager + executive -> approval_request(row 11)
  - kind: safety_scope_change
    to: maintenance_supervisor + property_manager + regional_manager (row 4 if applicable)
approvals_required:
  - change_order_minor
  - change_order_major
description: |
  Reviews each proposed change order: validates scope basis, re-estimates cost, checks
  schedule impact, evaluates against contingency, recommends approval or rejection, and
  routes to the correct approval row by dollar threshold. Tracks `change_orders_pct_of_contract`
  and `contingency_burn_rate`.
---

# Change Order Review

## Workflow purpose

Convert a change order request into an informed decision with a cost, schedule, and contingency view. Route to the correct approval row. Keep the change-order trail clean for draw review and cost-to-complete.

## Trigger conditions

- **Explicit:** "review change order", "CO evaluation", "PCO review".
- **Implicit:** GC submits a PCO; owner requests scope change; RFI produces a cost impact.
- **Recurring:** as each CO arrives.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| CO package | doc | required | narrative, line items, schedule |
| Original scope and contract | doc | required | basis |
| Prior COs | table | required | cumulative view |
| Estimator baseline | estimate | required | for re-estimate |
| Schedule record | record | required | for impact |
| Contingency status | derived | required | `contingency_remaining`, burn rate |

## Outputs

| Output | Type | Shape |
|---|---|---|
| CO review memo | `memo` | scope, cost, schedule, contingency impact, recommendation |
| Updated contract value | record | with CO pending or approved state |
| Updated schedule | record | milestone impacts |
| Approval request | request | row 10 or 11 |

## Required context

Asset_class, segment, form_factor, market, project.

## Process

1. **Scope validation.** Compare CO narrative to original contract and current scope; identify whether the change is scope add, deduct, credit, or clarification.
2. **Re-estimate.** Apply library, labor, and material references; compare to GC's proposed cost.
3. **Schedule impact.** Evaluate milestone impacts; compute `schedule_variance_days` delta.
4. **Contingency impact.** Compute `contingency_remaining` and `contingency_burn_rate` after CO. If burn exceeds overlay band, flag.
5. **Decision recommendation.** Approve / negotiate / reject based on scope rationale and cost variance.
6. **Approval routing.** Row 10 for minor; row 11 for major. Thresholds overlay-driven.
7. **Safety-critical scope change.** If change defers or modifies life-safety scope, row 4 also applies.
8. **Documentation.** Update contract register, schedule register, change-order log.
9. **Confidence banner.** References surfaced.

## Metrics used

`change_orders_pct_of_contract`, `contingency_remaining`, `contingency_burn_rate`, `cost_to_complete`, `schedule_variance_days`.

## Reference files used

- `reference/normalized/capex_line_items__{scope}.csv`
- `reference/normalized/labor_rates__{market}.csv`
- `reference/normalized/material_costs__{region}_residential.csv`
- `reference/derived/contingency_assumptions__{org}.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Escalation points

- Minor CO: row 10.
- Major CO: row 11.
- Safety-scope deferral: row 4.

## Required approvals

- Minor change order (row 10).
- Major change order (row 11).

## Failure modes

1. Approving without re-estimate. Fix: re-estimate mandatory.
2. Missing schedule impact. Fix: schedule impact mandatory.
3. Approving without contingency view. Fix: contingency impact mandatory.
4. Treating scope clarification as added cost. Fix: scope validation classifies.
5. Safety-scope deferral silent. Fix: row 4 gate.

## Edge cases

- **Owner-initiated change:** track separately; may be funded outside project budget per overlay.
- **Differing site condition:** overlay may require third-party verification before approval.
- **Credit CO:** ensure credit flows to owner; not netted silently.
- **Chain of COs from one RFI:** aggregate for approval level.

## Example invocations

1. "Review the PCO submitted for Ashford Park amenity refresh."
2. "CO log for the Willow Creek renovation program — anything trending hot?"
3. "Evaluate this scope change request on Riverbend construction."

## Example outputs

### Output — CO review (abridged, amenity refresh PCO)

**Scope.** Scope add per owner direction; library mapping present.

**Re-estimate.** Cost within overlay range of GC proposal; negotiation lever identified in one line.

**Schedule.** No critical path impact; `schedule_variance_days` unchanged.

**Contingency.** `contingency_remaining` after CO within overlay band; `contingency_burn_rate` within tolerance.

**Recommendation.** Approve at negotiated line adjustment; `approval_request` row 10 opened.

**Confidence banner.** `capex_line_items__amenity@2026-03-31, status=starter`. `contingency_assumptions@2026-03-31, status=starter`.
