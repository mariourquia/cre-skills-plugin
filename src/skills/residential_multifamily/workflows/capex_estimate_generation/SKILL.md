---
name: Capex Estimate Generation
slug: capex_estimate_generation
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Line-item library unit costs, labor rates, and material costs drift with market cycles.
  Contingency assumptions and escalation factors are overlay-driven. Assembly costs (e.g.,
  unit turn scope tiers, common-area refreshes) live in reference libraries.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [stabilized, renovation, lease_up, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [estimator_preconstruction_lead, construction_manager, asset_manager, development_manager]
  output_types: [estimate, memo]
  decision_severity_max: recommendation
references:
  reads:
    - reference/normalized/capex_line_items__{scope}.csv
    - reference/normalized/labor_rates__{market}.csv
    - reference/normalized/material_costs__{region}_residential.csv
    - reference/normalized/construction_duration_assumptions__{region}.csv
    - reference/derived/contingency_assumptions__{org}.csv
  writes: []
metrics_used:
  - dev_cost_per_unit
  - dev_cost_per_gsf
  - dev_cost_per_nrsf
  - renovation_yield_on_cost
  - capex_spend_vs_plan
escalation_paths:
  - kind: estimate_magnitude_outside_band
    to: estimator_preconstruction_lead -> construction_manager -> asset_manager
approvals_required: []
description: |
  Produces line-item capex estimates for a defined scope using the capex library, labor
  rates, material costs, and overlay contingency and escalation. Output is a structured
  estimate suitable for bid leveling, prioritization, or budget inclusion.
---

# Capex Estimate Generation

## Workflow purpose

Turn a scope statement into a structured, line-item estimate tied to the capex library. Output feeds `workflows/capital_project_intake_and_prioritization`, `workflows/bid_leveling_procurement_review`, and `workflows/budget_build`.

## Trigger conditions

- **Explicit:** "estimate this capex scope", "unit turn tier estimate", "amenity refresh estimate", "roof replacement estimate".
- **Implicit:** `workflows/capital_project_intake_and_prioritization` requests estimate; bid package prep; draw-review estimate scrub.
- **Recurring:** on demand.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Scope statement | memo | required | assembly / line-item references |
| Capex library | csv | required | |
| Labor rates | csv | required | market-specific |
| Material costs | csv | required | region-specific |
| Duration assumptions | csv | required | for phasing |
| Contingency assumptions | csv | required | overlay |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Line-item estimate | `estimate` | qty, unit_cost, extended, source |
| Summary roll-up | table | by assembly and project |
| Escalation view | table | at estimated execution date |
| Estimate memo | `memo` | assumptions, confidence, risk |

## Required context

Asset_class, segment, form_factor, lifecycle_stage, market.

## Process

1. **Scope decomposition.** Break scope into assemblies and line items; map to library.
2. **Quantity take-off.** Compute quantities per scope; include allowances per overlay.
3. **Unit cost application.** Apply library unit costs; adjust for labor and material references.
4. **Escalation.** Apply overlay escalator to target execution date.
5. **Contingency.** Apply overlay contingency by scope tier.
6. **Assembly roll-up.** Aggregate to assembly, project, and per-unit / per-sf.
7. **Risk memo.** Note assumption confidence, market sensitivities, schedule risks.
8. **Confidence banner.** References surfaced with `as_of_date` and `status`.

## Metrics used

`dev_cost_per_unit`, `dev_cost_per_gsf`, `dev_cost_per_nrsf`, `renovation_yield_on_cost` (if yield is asked), `capex_spend_vs_plan` (feeder).

## Reference files used

- `reference/normalized/capex_line_items__{scope}.csv`
- `reference/normalized/labor_rates__{market}.csv`
- `reference/normalized/material_costs__{region}_residential.csv`
- `reference/normalized/construction_duration_assumptions__{region}.csv`
- `reference/derived/contingency_assumptions__{org}.csv`

## Escalation points

- Estimate magnitude outside overlay band: estimator -> construction_manager -> asset_manager.

## Required approvals

None for the estimate itself (recommendation severity). Downstream approvals live in `workflows/bid_leveling_procurement_review`, `workflows/change_order_review`, etc.

## Failure modes

1. Library without market adjustment. Fix: labor/material references mandatory.
2. No contingency. Fix: overlay contingency mandatory.
3. No escalation. Fix: escalator applied to target execution date.
4. Estimate without risk memo. Fix: risk memo mandatory.

## Edge cases

- **Custom scope (no library assembly):** new line items flagged; note confidence low; propose library update via reference flow if systematic.
- **Tenant-impact scope:** add tenant communication allowance per overlay.
- **Licensed trade with limited local market:** surface market-specific risk.
- **Phased scope crossing fiscal years:** escalate by phase.

## Example invocations

1. "Estimate the roof replacement scope for Ashford Park."
2. "Build the estimate for the Willow Creek unit renovation tier 2."
3. "Amenity refresh estimate for the South End portfolio common areas."

## Example outputs

### Output — Capex estimate (abridged, roof replacement Ashford Park)

**Scope.** Roof replacement per scope statement; decomposed to tear-off, underlayment, shingles, flashing, cleanup.

**Line items.** Quantities and unit costs from library; adjusted for labor market.

**Roll-up.** Per-assembly and per-unit totals.

**Escalation.** Applied to target execution date.

**Contingency.** Applied per overlay tier.

**Risk memo.** Material-cost volatility noted; labor availability confidence medium.

**Confidence banner.** `capex_line_items__roofing@2026-03-31, status=starter`. `labor_rates__charlotte@2026-03-31, status=sample`. `contingency_assumptions@2026-03-31, status=starter`.
