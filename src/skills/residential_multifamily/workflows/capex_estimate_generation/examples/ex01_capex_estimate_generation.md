# Example — Capex Estimate (abridged)

**Prompt:** "Estimate the roof replacement scope for Ashford Park."

**Inputs:** scope statement + library + labor/material refs + contingency.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- market: Charlotte
- role: estimator_preconstruction_lead
- output_type: estimate
- decision_severity: recommendation

## Expected packs loaded

- `workflows/capex_estimate_generation/`
- `overlays/segments/middle_market/`

## Expected references

- `reference/normalized/capex_line_items__roofing.csv`
- `reference/normalized/labor_rates__charlotte.csv`
- `reference/normalized/material_costs__southeast_residential.csv`
- `reference/normalized/construction_duration_assumptions__southeast.csv`
- `reference/derived/contingency_assumptions__{org}.csv`

## Gates potentially triggered

- None at estimate stage; downstream bid/change-order workflows carry gates.

## Expected output shape

- Line-item estimate with quantities, unit costs, extended totals.
- Assembly roll-up.
- Escalation at target execution date.
- Contingency applied per overlay.
- Risk memo.

## Confidence banner pattern

```
References: capex_line_items__roofing@2026-03-31 (starter), labor_rates__charlotte@2026-03-31 (sample),
material_costs__southeast_residential@2026-03-31 (sample), contingency_assumptions@2026-03-31 (starter).
```
