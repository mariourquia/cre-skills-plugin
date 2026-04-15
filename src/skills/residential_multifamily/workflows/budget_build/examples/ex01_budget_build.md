# Example — Annual Budget Build (abridged)

**Prompt:** "Build the 2027 budget for Ashford Park. Flag any assumption outside band."

**Inputs:** rent roll snapshot + T12 + budget history + assumption references.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- lifecycle_stage: stabilized
- management_mode: third_party_managed
- role: asset_manager
- market: Charlotte
- jurisdiction: Charlotte
- output_type: operating_review
- decision_severity: action_requires_approval

## Expected packs loaded

- `workflows/budget_build/`
- `workflows/capital_project_intake_and_prioritization/` (capex stub)
- `overlays/segments/middle_market/`
- `overlays/management_mode/third_party_managed/`

## Expected references

- `reference/normalized/payroll_assumptions__{org}.csv`
- `reference/normalized/insurance_tax_assumptions__charlotte.csv`
- `reference/normalized/utility_benchmarks__charlotte.csv`
- `reference/normalized/staffing_ratios__middle_market.csv`
- `reference/normalized/market_rents__charlotte_mf.csv`
- `reference/normalized/concession_benchmarks__charlotte_mf.csv`
- `reference/normalized/collections_benchmarks__southeast_mf.csv`
- `reference/normalized/unit_turn_cost_library__charlotte.csv`
- `reference/derived/budget_escalator_assumptions__charlotte.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Gates potentially triggered

- Final submission: row 14 (lender), 15 (LP/investor), or 16 (board/regulator).

## Expected output shape

- Revenue build table (monthly).
- Expense build table (monthly).
- NOI + NOI margin summary.
- Covenant view (DSCR, debt yield).
- Variance narrative vs. prior and T12.
- Sensitivity appendix.
- Owner-package draft.

## Confidence banner pattern

```
References: all assumption files surfaced with as_of_date and status.
Starter and sample tags flagged. Forecast calibration notes included.
```
