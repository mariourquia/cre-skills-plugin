---
name: Reforecast
slug: reforecast
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Same assumptions as budget_build. Reforecast inherits live actuals through the asof
  month and preserves forward-looking assumptions unless overlay cites a change basis.
  Forecast accuracy is a trailing-6-month metric; drift informs assumption recalibration.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [stabilized, renovation, lease_up, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [property_manager, regional_manager, asset_manager, reporting_finance_ops_lead]
  output_types: [operating_review, memo, kpi_review]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/normalized/payroll_assumptions__{org}.csv
    - reference/normalized/insurance_tax_assumptions__{market}.csv
    - reference/normalized/utility_benchmarks__{market}.csv
    - reference/normalized/market_rents__{market}_mf.csv
    - reference/normalized/concession_benchmarks__{market}_mf.csv
    - reference/normalized/collections_benchmarks__{region}_mf.csv
    - reference/normalized/unit_turn_cost_library__{market}.csv
    - reference/derived/budget_escalator_assumptions__{market}.csv
    - reference/normalized/approval_threshold_defaults.csv
  writes: []
metrics_used:
  - noi
  - noi_margin
  - forecast_accuracy
  - revenue_variance_to_budget
  - expense_variance_to_budget
  - economic_occupancy
  - collections_rate
  - bad_debt_rate
  - concession_rate
  - dscr
  - debt_yield
  - budget_attainment
escalation_paths:
  - kind: forecast_final_submission
    to: asset_manager -> finance/reporting lead -> approval_request(row 14 for lender)
  - kind: owner_submission
    to: asset_manager -> executive -> approval_request(row 15 or 16)
approvals_required:
  - final_forecast_submission
description: |
  Produces a reforecast that inherits actuals through the as-of month, preserves or revises
  forward-looking assumptions with citation, and surfaces the delta vs. budget and vs.
  prior forecast. Includes forecast-accuracy calibration and NOI sensitivity.
---

# Reforecast

## Workflow purpose

Take the latest actuals, combine with forward assumptions, and produce a reforecast that shows how year-end is likely to land vs. budget and prior forecast. Preserve assumption trail. Cite every revision.

## Trigger conditions

- **Explicit:** "reforecast Q2", "update forecast", "year-end landing", "roll forecast through December".
- **Implicit:** as-of month closes; material variance vs. prior forecast; market-side event (rent comp update, insurance renewal, tax reassessment).
- **Recurring:** per org overlay calendar (often monthly or quarterly).

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Actuals through asof | table | required | GL closed through month |
| Prior forecast | table | required | for delta tracking |
| Budget | table | required | anchor |
| Rent roll snapshot | table | required | for forward revenue |
| Assumption references | csv / yaml | required | all budget_build refs |
| Change basis notes | memo | optional | any revision > overlay materiality |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Reforecast by line item | table | monthly through year end |
| NOI + margin + covenant view | `kpi_review` | budget vs. prior forecast vs. new forecast |
| Delta commentary | `memo` | revisions and basis |
| Forecast accuracy view | `kpi_review` | `forecast_accuracy` trailing 6 |
| Owner submission draft | `operating_review` | if applicable |

## Required context

Asset_class, segment, form_factor, lifecycle_stage, management_mode, market.

## Process

1. **Snapshot actuals through asof.** Confirm GL close; flag any open items.
2. **Compute variance to budget (MTD, YTD, RTG).** `revenue_variance_to_budget`, `expense_variance_to_budget`. Classify drivers.
3. **Forward revenue.** Roll forward leases; apply current market reference and concession posture; revise if actuals show drift.
4. **Forward expense.** Apply escalators and assumptions; any revision cites basis (overlay update, re-bid, known scope change).
5. **Recompute NOI, margin, DSCR, DY.**
6. **Forecast accuracy calibration.** Compute trailing `forecast_accuracy`; surface systematic bias.
7. **Sensitivity.** Overlay stress cases on forward months.
8. **Comparison table.** Budget vs. prior forecast vs. new forecast.
9. **Submission path.** Owner or lender final submission opens `approval_request` row 14 / 15 / 16.
10. **Confidence banner.** All reference `as_of_date` and `status` tags surfaced.

## Metrics used

`noi`, `noi_margin`, `forecast_accuracy`, `revenue_variance_to_budget`, `expense_variance_to_budget`, `economic_occupancy`, `collections_rate`, `bad_debt_rate`, `concession_rate`, `dscr`, `debt_yield`, `budget_attainment`.

## Reference files used

Same as `budget_build` (assumption inheritance).

## Escalation points

- Final submission: row 14 (lender), 15 / 16 (LP / board).
- Assumption revision above overlay materiality: asset_manager sign-off.

## Required approvals

- Final forecast submission (row 14 / 15 / 16).

## Failure modes

1. Silent assumption change. Fix: every revision cites basis; change basis memo required above materiality.
2. Not recalibrating when `forecast_accuracy` shows bias. Fix: calibration is a step.
3. Forward revenue built on stale market reference. Fix: surface staleness; if > overlay threshold, refresh first via `workflows/market_rent_refresh`.
4. Submitting final to lender without approval. Fix: row 14 gate.

## Edge cases

- **Property mid-renovation:** split classic and renovated unit lines; distinct assumptions.
- **Debt refi during remaining year:** sensitivity on DSCR / DY post-refi; flag timing uncertainty.
- **Insurance renewal pending:** hold assumption at current rate with sensitivity; cite pending renewal.
- **Tax reassessment filed:** show appeal scenario alongside base.
- **Lease-up still active:** stabilization pace remains anchor; reforecast tied to `stabilization_pace_vs_plan`.

## Example invocations

1. "Reforecast Ashford Park through year end using March actuals."
2. "How is Willow Creek landing vs. budget this year?"
3. "Build the quarterly reforecast for the South End portfolio."

## Example outputs

### Output — Reforecast summary (abridged, Ashford Park, asof 2026-03)

**Actuals through March.** Revenue within band vs. budget; expenses showing utilities drift per seasonal pattern.

**Forward revenue.** Roll-forward applied; market reference refreshed 2026-03-31; concessions tracking overlay.

**Forward expense.** Utilities assumption revised with basis memo; insurance held at current rate pending renewal.

**Year-end landing.** NOI within band of budget; `noi_margin` within overlay target; `dscr` and `debt_yield` meet covenants.

**Forecast accuracy.** Trailing 6 months within overlay band.

**Submission.** Owner draft prepared; `approval_request` row 15 opened.

**Confidence banner.** Assumption references carry `as_of_date` and `status`. Change basis memo attached for utilities revision.
