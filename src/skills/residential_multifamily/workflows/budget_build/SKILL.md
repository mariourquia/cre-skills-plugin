---
name: Annual Budget Build
slug: budget_build
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Payroll assumptions, insurance and tax assumptions, utility benchmarks, material and
  labor escalators, concession and rent-growth assumptions, and staffing ratios all drift.
  All assumption values come from reference libraries; this pack does not embed numbers.
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
    - reference/normalized/staffing_ratios__middle_market.csv
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
  - economic_occupancy
  - physical_occupancy
  - leased_occupancy
  - collections_rate
  - bad_debt_rate
  - concession_rate
  - rent_growth_renewal
  - rent_growth_new_lease
  - blended_lease_trade_out
  - payroll_per_unit
  - rm_per_unit
  - utilities_per_unit
  - controllable_opex_per_unit
  - dscr
  - debt_yield
escalation_paths:
  - kind: budget_final_submission
    to: asset_manager -> finance/reporting lead -> approval_request(row 14 for lender submission)
  - kind: owner_submission
    to: asset_manager -> executive -> approval_request(row 15 or 16)
approvals_required:
  - final_budget_submission
description: |
  Builds the annual operating budget from property-level bottoms-up plus portfolio-level
  assumptions. Revenue build from rent roll + market reference + renewal policy; expense
  build from assumption libraries + staffing ratios + benchmarks. Produces variance
  narrative against prior year and T12, stress-test sensitivities, and a draft owner
  package. Final submission is gated.
---

# Annual Budget Build

## Workflow purpose

Produce a defensible annual operating budget for a property, with every dollar traced to a reference. Revenue derives from rent roll roll-forward + overlay market assumptions + renewal policy. Expense derives from assumption libraries and staffing ratios. The output is a budget package plus a narrative that can withstand asset-management and lender review.

## Trigger conditions

- **Explicit:** "build 2027 budget", "budget build for property X", "annual operating budget", "start budget cycle".
- **Implicit:** calendar approach of budget season per org overlay; prior budget superseded.
- **Recurring:** annual per property, on the org's budget calendar.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Rent roll snapshot | table | required | for revenue roll-forward |
| T12 operating statement | table | required | base for expense build |
| Budget history (prior 2 years) | table | required | for trend analysis |
| Market rent reference | csv | required | |
| Concession benchmark | csv | required | |
| Collections benchmark | csv | required | |
| Payroll assumptions | csv | required | |
| Insurance/tax assumptions | csv | required | |
| Utility benchmarks | csv | required | |
| Turn cost library | csv | required | |
| Staffing ratios | csv | required | |
| Budget escalator assumptions | csv | required | per market |
| Renewal uplift bands | csv | required | |
| Debt schedule | record | required | for DSCR/DY view |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Revenue build | table | by line item, monthly |
| Expense build | table | by line item, monthly |
| Capex plan stub | list | referenced, produced by `capital_project_intake_and_prioritization` |
| NOI + NOI margin summary | `kpi_review` | prior, T12, budget; variance |
| Covenant view | `kpi_review` | `dscr`, `debt_yield` on budgeted NOI |
| Budget narrative | `memo` | drivers and assumptions, sensitivities |
| Owner package draft | `operating_review` | assembled budget package |

## Required context

Asset_class, segment, form_factor, lifecycle_stage, management_mode, market, jurisdiction.

## Process

1. **Revenue build.**
   - Start with rent roll. Roll forward each lease through its term; on roll, apply renewal uplift band for renewals and market trend for new leases. Reflect concession policy.
   - Compute GPR, vacancy loss (from target `physical_occupancy` band), concessions, bad debt (from `collections_rate` and `bad_debt_rate` assumptions), other income (from T12 trend + overlay).
   - Produce `economic_occupancy` view.
2. **Expense build.**
   - Payroll: staffing ratios x salary bands + burden rate from payroll assumptions. Compute `payroll_per_unit`.
   - R&M and contract services: T12 base + overlay escalators + known scope changes; `rm_per_unit`.
   - Utilities: benchmark x seasonality curve; apply RUBS recovery per overlay. `utilities_per_unit`.
   - Insurance and property tax: assumption library; tax may require a separate appeal/reassessment view.
   - Management fee: per PMA if third_party_managed.
   - Marketing: overlay ratio.
   - Turnover expense: turn cost library x projected turn count from target `turnover_rate`.
3. **Capex plan stub.** Pull from `workflows/capital_project_intake_and_prioritization`; budget reflects cash flow timing, not P&L.
4. **NOI, NOI margin, DSCR, DY.** Compute on budget numbers; compare prior and T12.
5. **Variance narrative.** For each material line, explain driver (volume, price, mix, assumption change).
6. **Sensitivity cases.** Run overlay stress cases: occupancy down X, trade-out down Y, insurance up Z; show NOI impact.
7. **Calibration check.** Forecast accuracy on prior budget: where was the operator off; adjust current assumptions where pattern is explained.
8. **Owner package.** Assemble per template; draft narrative; prepare sensitivity appendix.
9. **Approval.** Final owner/lender submission opens `approval_request` row 14 (lender) or row 15 / 16 (investor).
10. **Confidence banner.** Reference `as_of_date` and `status` tags for every assumption.

## Metrics used

`noi`, `noi_margin`, `economic_occupancy`, `physical_occupancy`, `leased_occupancy`, `collections_rate`, `bad_debt_rate`, `concession_rate`, `rent_growth_renewal`, `rent_growth_new_lease`, `blended_lease_trade_out`, `payroll_per_unit`, `rm_per_unit`, `utilities_per_unit`, `controllable_opex_per_unit`, `dscr`, `debt_yield`.

## Reference files used

- `reference/normalized/payroll_assumptions__{org}.csv`
- `reference/normalized/insurance_tax_assumptions__{market}.csv`
- `reference/normalized/utility_benchmarks__{market}.csv`
- `reference/normalized/staffing_ratios__middle_market.csv`
- `reference/normalized/market_rents__{market}_mf.csv`
- `reference/normalized/concession_benchmarks__{market}_mf.csv`
- `reference/normalized/collections_benchmarks__{region}_mf.csv`
- `reference/normalized/unit_turn_cost_library__{market}.csv`
- `reference/derived/budget_escalator_assumptions__{market}.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Escalation points

- Final submission to lender: `approval_request` row 14.
- Final submission to owner/LP: row 15 or 16.
- Assumptions outside overlay bands: asset_manager sign-off before finalization.

## Required approvals

- Final budget submission (row 14 / 15 / 16 per recipient).

## Failure modes

1. Rent growth without a market reference. Fix: market reference required.
2. Payroll built from headcount without ratios. Fix: ratios overlay governs.
3. No sensitivity. Fix: sensitivity pass is mandatory.
4. Ignoring prior forecast accuracy. Fix: calibration check is a required step.
5. Final submission without approval. Fix: row 14/15/16 gate.

## Edge cases

- **Lease-up property:** revenue build uses lease-up curve; utility baseline distinct.
- **Renovation program in-flight:** distinguish classic and renovated unit rent lines.
- **Tax reassessment pending:** sensitivity case on tax; reference the appeal assumption.
- **Debt maturity during budget year:** show refi sensitivity on DSCR.
- **New construction in sister property:** supply/demand note in narrative; not in revenue build directly.

## Example invocations

1. "Build the 2027 budget for Ashford Park. Use current assumptions and flag any outside band."
2. "Run sensitivities on the draft 2027 budget for Willow Creek."
3. "Produce the owner budget package for the South End portfolio."

## Example outputs

### Output — 2027 budget summary (abridged, Ashford Park)

**Revenue.** GPR from roll-forward; vacancy loss to target; concessions per overlay; other income per T12 + overlay; `economic_occupancy` within band.

**Expense.** Payroll from ratios; R&M per overlay escalator; utilities per benchmark with RUBS; insurance/tax per overlay.

**NOI.** Computed; `noi_margin` within overlay band.

**Covenant view.** `dscr` on budget NOI against loan requirement; `debt_yield` above floor.

**Sensitivities.** Overlay stress cases produce NOI impact table.

**Calibration.** Prior budget forecast accuracy noted; adjustments made to utilities assumption per pattern.

**Submission.** Owner package drafted; `approval_request` row 15 opened for owner final submission.

**Confidence banner.** All assumption references carry `as_of_date` and `status`. Sample / starter references surfaced with tag.
