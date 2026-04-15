# Example — Monthly Development Status (abridged)

**Prompt:** "Build the monthly development status for Harbor Point. Include cost-to-complete, contingency burn, schedule variance, and change orders."

**Inputs:** project budget (approved); schedule (baseline + current); GC cost report; change-order log; draw schedule; entitlement tracker.

**Output shape:** see `templates/monthly_development_status.md`.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: suburban_mid_rise
- lifecycle_stage: construction
- role: development_manager
- output_type: operating_review
- decision_severity: recommendation

## Expected packs loaded

- `roles/development_manager/`
- `workflows/monthly_development_status/`
- `workflows/change_order_review/` (if open CO in period)
- `overlays/segments/middle_market/`
- `overlays/form_factor/suburban_mid_rise/`
- `overlays/lifecycle/construction/`

## Expected references

- `reference/normalized/material_costs__{region}_residential.csv`
- `reference/normalized/labor_rates__{market}_residential.csv`
- `reference/normalized/dev_budget_benchmarks__middle_market_suburban_mid_rise.csv`
- `reference/normalized/soft_cost_benchmarks__middle_market.csv`
- `reference/normalized/cost_escalation_assumptions__{region}.csv`
- `reference/normalized/contingency_policy__middle_market.csv`

## Gates potentially triggered

- Any major change order routes row 11.
- Any contingency draw above policy routes row 8.
- Any business-plan deviation routes row 17.
- Any lender-facing final routes row 14.

## Confidence banner pattern

```
References: material_costs@{as_of_date, region}, labor_rates@{as_of_date, market},
dev_budget_benchmarks@{as_of_date}, cost_escalation@{as_of_date}, contingency_policy@{as_of_date}
(statuses per record). GC cost report as of {report_date}. Schedule current as of
{tracker_date}.
```
