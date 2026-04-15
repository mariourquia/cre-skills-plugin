# Example — Schematic-Stage Estimate with Conceptual Reconciliation (abridged)

**Prompt:** "Build a schematic-stage estimate for Harbor Point at the proposed unit count and GSF. Include reconciliation with the conceptual estimate."

**Inputs:** schematic package (plans, area take-offs, program); prior conceptual estimate; scope class = SF-based / unit-based hybrid (dev ground-up).

**Output shape:** see `templates/estimate__schematic.md` + `templates/estimate_reconciliation_memo.md`.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: suburban_mid_rise
- lifecycle_stage: development
- role: estimator_preconstruction_lead
- output_type: estimate
- decision_severity: recommendation

## Expected packs loaded

- `roles/estimator_preconstruction_lead/`
- `workflows/preconstruction_estimate_cycle/`
- `overlays/segments/middle_market/`
- `overlays/form_factor/suburban_mid_rise/`
- `overlays/lifecycle/development/`

## Expected references

- `reference/normalized/dev_budget_benchmarks__middle_market_suburban_mid_rise.csv`
- `reference/normalized/material_costs__{region}_residential.csv`
- `reference/normalized/labor_rates__{market}_residential.csv`
- `reference/normalized/productivity_norms__{region}_residential.csv`
- `reference/normalized/assembly_cost_library__middle_market_suburban_mid_rise.csv`
- `reference/normalized/cost_escalation_assumptions__{region}.csv`
- `reference/normalized/contingency_policy__middle_market.csv`
- `reference/normalized/soft_cost_benchmarks__middle_market.csv`

## Gates potentially triggered

- None directly by the estimator. Any estimate reconciliation gap material to underwriting
  is surfaced to development_manager with a reconciliation memo; that routes row 17 via
  asset_manager if a plan deviation is indicated.

## Confidence banner pattern

```
Schematic-stage estimate. Confidence band: schematic. References:
dev_budget_benchmarks@{as_of_date}, material_costs@{as_of_date, region},
labor_rates@{as_of_date, market}, assembly_cost_library@{as_of_date},
cost_escalation@{as_of_date}, contingency_policy@{as_of_date},
soft_cost_benchmarks@{as_of_date} (statuses per record). Stage assignment requires
DD before GMP negotiation.
```
