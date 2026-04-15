---
name: Monthly Property Operating Review
slug: monthly_property_operating_review
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Target bands, service standards, and KPI materiality thresholds are overlay-driven.
  Benchmarks drift with each reference refresh.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [stabilized, renovation, lease_up, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [property_manager, regional_manager, asset_manager]
  output_types: [operating_review, kpi_review, memo]
  decision_severity_max: recommendation
references:
  reads:
    - reference/derived/role_kpi_targets.csv
    - reference/normalized/market_rents__{market}_mf.csv
    - reference/normalized/concession_benchmarks__{market}_mf.csv
    - reference/normalized/collections_benchmarks__{region}_mf.csv
    - reference/normalized/approval_threshold_defaults.csv
  writes: []
metrics_used:
  - physical_occupancy
  - leased_occupancy
  - economic_occupancy
  - notice_exposure
  - renewal_offer_rate
  - renewal_acceptance_rate
  - blended_lease_trade_out
  - concession_rate
  - collections_rate
  - delinquency_rate_30plus
  - bad_debt_rate
  - make_ready_days
  - average_days_vacant
  - turnover_rate
  - open_work_orders
  - work_order_aging
  - repeat_work_order_rate
  - controllable_opex_per_unit
  - payroll_per_unit
  - rm_per_unit
  - utilities_per_unit
  - revenue_variance_to_budget
  - expense_variance_to_budget
escalation_paths:
  - kind: material_variance
    to: property_manager -> regional_manager -> asset_manager
  - kind: safety_p1_pattern
    to: maintenance_supervisor -> property_manager -> regional_manager
  - kind: fair_housing_flag
    to: approval_request(row 3)
approvals_required: []
description: |
  Monthly property scorecard and narrative. Synthesizes operating, leasing, collections,
  maintenance, and financial variance into a single review pack for the PM, regional,
  and AM. Invokes child workflows for funnel, delinquency, turn, and WO views.
---

# Monthly Property Operating Review

## Workflow purpose

Produce a single monthly review pack that covers the property's operating performance end to end: occupancy, revenue, collections, delinquency, leasing funnel, renewal, turn pipeline, maintenance, and variance to budget. Feeds the PM's monthly conversation with regional and AM.

## Trigger conditions

- **Explicit:** "monthly property scorecard", "monthly operating review", "March review for Ashford Park".
- **Implicit:** calendar month close; AM requests monthly pack.
- **Recurring:** monthly per property.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| T12 and current-month GL | table | required | |
| Rent roll snapshot | table | required | |
| Funnel inputs | table | required | via `workflows/lead_to_lease_funnel_review` |
| Delinquency inputs | table | required | via `workflows/delinquency_collections` |
| Turn pipeline inputs | table | required | via `workflows/unit_turn_make_ready` |
| WO log | table | required | via `workflows/work_order_triage` + `vendor_dispatch_sla_review` |
| Budget and reforecast | table | required | |
| Target bands | derived | required | |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Property scorecard | `kpi_review` | all primary KPIs with bands |
| Narrative memo | `memo` | drivers, variances, actions |
| Variance table | `kpi_review` | `revenue_variance_to_budget`, `expense_variance_to_budget` |
| Action list | `checklist` | owners, due dates, gates |
| Owner / AM submission draft | `operating_review` | |

## Required context

Asset_class, segment, form_factor, lifecycle_stage, management_mode, market.

## Process

1. **Pull core KPIs.** Compute every metric in `metrics_used` at the property grain as of month close.
2. **Band check.** Compare each KPI against overlay band; color-code within / below / above.
3. **Invoke child workflows** for narrative context:
   - `workflows/lead_to_lease_funnel_review` for leasing summary.
   - `workflows/delinquency_collections` for aging and gates.
   - `workflows/unit_turn_make_ready` for turn pipeline.
   - `workflows/vendor_dispatch_sla_review` for vendor SLA flags.
4. **Variance analysis.** Revenue and expense variance to budget + to reforecast. Material lines flagged per overlay.
5. **Controllable opex review.** `controllable_opex_per_unit` trend; `payroll_per_unit`, `rm_per_unit`, `utilities_per_unit` check.
6. **Action list.** Each action names an owner, due date, and approval gate if any.
7. **Owner / AM submission.** Compose per template; surface any `approval_request` already open from child workflows.
8. **Confidence banner.** Reference `as_of_date` and `status` tags.

## Metrics used

See frontmatter `metrics_used`.

## Reference files used

- `reference/derived/role_kpi_targets.csv`
- `reference/normalized/market_rents__{market}_mf.csv`
- `reference/normalized/concession_benchmarks__{market}_mf.csv`
- `reference/normalized/collections_benchmarks__{region}_mf.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Escalation points

- Material variance to budget or reforecast: PM -> regional -> AM.
- Pattern of P1s or breaches: maintenance_supervisor -> PM -> regional.
- Fair-housing flag surfaced in child workflows: row 3.

## Required approvals

None for the review pack itself (informational / recommendation severity). Any action inside a child workflow carries its own approval gate.

## Failure modes

1. Reporting occupancy without qualifier. Fix: always cite physical + leased + economic.
2. Narrative without cited metrics. Fix: every claim anchored to a slug.
3. Missing variance explanation. Fix: explanation required for any line above overlay materiality.
4. Sample-data as fact. Fix: confidence banner.

## Edge cases

- **First full month post-TCO:** narrative emphasizes lease-up pace and `stabilization_pace_vs_plan`.
- **Mid-renovation month:** narrative distinguishes classic and renovated lines.
- **TPM-managed:** the pack includes the TPM's submitted report and an oversight assessment (see `workflows/third_party_manager_scorecard_review`).

## Example invocations

1. "Build the March monthly review for Ashford Park. Flag anything off band."
2. "Produce the AM submission pack for Willow Creek April close."
3. "Monthly scorecard for the South End portfolio (three assets)."

## Example outputs

### Output — Monthly scorecard (abridged, Ashford Park, March 2026)

**Occupancy.** `physical_occupancy`, `leased_occupancy`, `economic_occupancy` all within band. `notice_exposure` within band.

**Leasing.** Funnel invoked; key flags surfaced.

**Renewal.** `renewal_offer_rate` at target; `renewal_acceptance_rate` within band; `blended_lease_trade_out` within overlay band.

**Collections.** `collections_rate` within band; `delinquency_rate_30plus` within band; `bad_debt_rate` within band. Two legal-notice approvals open from child workflow.

**Turn and WO.** `make_ready_days` within band; `open_work_orders` within band; `repeat_work_order_rate` within band; one vendor flagged for scorecard review.

**Financial variance.** `revenue_variance_to_budget` within overlay materiality. `expense_variance_to_budget`: utilities above materiality; driver explained.

**Action list.** Owners, dates, and gates enumerated.

**Confidence banner.** All references surfaced with `as_of_date` and `status`.
