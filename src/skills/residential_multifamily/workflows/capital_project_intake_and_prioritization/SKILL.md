---
name: Capital Project Intake and Prioritization
slug: capital_project_intake_and_prioritization
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Capex line-item libraries, labor rates, escalation assumptions, and replacement cost
  benchmarks drift. Prioritization rubric weights live in overlays. Life-safety
  classifications come from jurisdiction overlays.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [stabilized, renovation, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [property_manager, regional_manager, asset_manager, construction_manager, estimator_preconstruction_lead]
  output_types: [memo, checklist, estimate, kpi_review]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/normalized/capex_line_items__{scope}.csv
    - reference/normalized/labor_rates__{market}.csv
    - reference/normalized/material_costs__{region}_residential.csv
    - reference/normalized/capex_priority_rubric__{org}.yaml
    - reference/normalized/approval_threshold_defaults.csv
  writes: []
metrics_used:
  - capex_spend_vs_plan
  - renovation_yield_on_cost
  - repeat_work_order_rate
  - controllable_opex_per_unit
escalation_paths:
  - kind: life_safety_prioritization
    to: maintenance_supervisor + property_manager + regional_manager -> approval_request(row 4)
  - kind: bid_award
    to: construction_manager + asset_manager -> approval_request(row 9)
  - kind: capex_program_change
    to: asset_manager + portfolio_manager -> approval_request(rows 8-11 per dollar)
approvals_required:
  - capex_program_change
  - life_safety_prioritization
description: |
  Intake for capital project ideas from any source (PM, regional, AM, engineering, capex
  plan cycle). Scores each project against the overlay's priority rubric (life safety,
  deferred maintenance, renovation yield, risk mitigation, regulatory). Produces the
  prioritized backlog and flags gated decisions.
---

# Capital Project Intake and Prioritization

## Workflow purpose

Convert raw capex ideas and deferred-maintenance flags into a ranked, costed, approvable backlog. Ensures life-safety items never lose priority; routes scope deferrals for approval.

## Trigger conditions

- **Explicit:** "capex intake", "prioritize capex", "capex backlog", "year-end capex plan".
- **Implicit:** `workflows/monthly_property_operating_review` surfaces deferred maintenance; `workflows/work_order_triage` finds a repeat pattern; insurance claim or inspection produces a scope.
- **Recurring:** quarterly intake; annual plan build pre-budget.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Intake items | list | required | description, source, unit, scope |
| Capex line-item library | csv | required | cost ranges |
| Labor and material references | csv | required | market-specific |
| Priority rubric overlay | yaml | required | life safety weight etc. |
| Existing capex plan | record | required | conflict detection |
| Renovation program tracker | record | optional | for yield context |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Prioritized backlog | `kpi_review` | per-item score, cost, priority, life-safety flag |
| Estimate per item | `estimate` | line items from library |
| Backlog memo | `memo` | narrative + recommended sequence |
| Approval request list | list | for items that require approval |

## Required context

Asset_class, segment, form_factor, lifecycle_stage, management_mode, market.

## Process

1. **Intake normalization.** Each item normalized to (description, unit, scope tier, driver, source).
2. **Life-safety flag.** Any item tagged life-safety cannot be deprioritized without `approval_request` row 4.
3. **Estimate.** Apply library; adjust for market via labor/material references.
4. **Score.** Per overlay rubric: life safety, deferred maintenance, renovation yield, risk mitigation, regulatory compliance, residual value.
5. **Sequence.** Produce prioritized backlog with scheduling constraints (seasonality, tenant impact).
6. **Gated items.** Any life-safety deferral, any program change above threshold: open approval rows 4 / 8-11.
7. **Feed budget / reforecast.** Output feeds `workflows/budget_build` and `workflows/reforecast`.
8. **Confidence banner.** References cited.

## Metrics used

`capex_spend_vs_plan`, `renovation_yield_on_cost`, `repeat_work_order_rate`, `controllable_opex_per_unit`.

## Reference files used

- `reference/normalized/capex_line_items__{scope}.csv`
- `reference/normalized/labor_rates__{market}.csv`
- `reference/normalized/material_costs__{region}_residential.csv`
- `reference/normalized/capex_priority_rubric__{org}.yaml`
- `reference/normalized/approval_threshold_defaults.csv`

## Escalation points

- Life-safety deferral: row 4.
- Program change above threshold: rows 8-11.
- Bid award associated with a project: row 9.

## Required approvals

- Life-safety scope deferral (row 4).
- Capex program change above threshold.

## Failure modes

1. Silent life-safety deprioritization. Fix: row 4 gate automatic.
2. Library not market-adjusted. Fix: labor/material references required.
3. Estimate without scope tier. Fix: tier required.
4. Prioritization without rubric. Fix: overlay rubric governs.

## Edge cases

- **Insurance claim scope:** treat as capex intake if above reserve; flag insurance coordination.
- **Regulatory deadline (e.g., code compliance):** auto-priority boost.
- **Tenant-impact scope:** scheduling constraint; include tenant communication via `workflows/move_in_administration` or notice.
- **Renovation in progress with change order backlog:** coordinate via `workflows/change_order_review`.

## Example invocations

1. "Quarterly capex intake for Ashford Park; prioritize backlog."
2. "What's the life-safety queue across the portfolio?"
3. "Build the 2027 capex plan input for Willow Creek."

## Example outputs

### Output — Prioritized capex backlog (abridged, Ashford Park)

**Backlog.** Per-item score, cost range, priority, life-safety flag. Top items: roof repairs (life safety), parking lot resurfacing (deferred maintenance), unit renovation cohort (yield).

**Sequence.** Proposed order with seasonal constraints.

**Approvals.** Two items above overlay threshold: rows 8-11 opened for program decisions.

**Confidence banner.** `capex_line_items__value_add@2026-03-31, status=starter`. `labor_rates__charlotte@2026-03-31, status=sample`. `capex_priority_rubric@2026-03-31, status=starter`.
