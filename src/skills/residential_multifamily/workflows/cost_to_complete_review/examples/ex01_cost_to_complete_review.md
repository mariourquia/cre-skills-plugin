# Example — Cost-to-Complete Review (abridged)

**Prompt:** "Run the April CTC for Willow Creek."

**Inputs:** cost-to-date + approved COs + pending COs + remaining scope + schedule + prior CTC + estimator baseline.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: suburban_mid_rise
- market: Charlotte
- project_id: willow_creek_construction
- role: construction_manager
- output_type: kpi_review
- decision_severity: action_requires_approval

## Expected packs loaded

- `workflows/cost_to_complete_review/`
- `workflows/capex_estimate_generation/` (re-estimate inputs)
- `overlays/segments/middle_market/`
- `overlays/lifecycle/construction/`

## Expected references

- `reference/normalized/capex_line_items__{scope}.csv`
- `reference/normalized/labor_rates__charlotte.csv`
- `reference/normalized/material_costs__southeast_residential.csv`
- `reference/derived/contingency_assumptions__{org}.csv`
- `reference/normalized/construction_duration_assumptions__southeast.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Gates potentially triggered

- Budget reallocation above threshold: approval row per overlay.
- Contingency exhaustion risk: approval request per overlay.
- CTC variance above threshold escalates to executive.

## Expected output shape

- CTC refresh table per trade.
- Driver decomposition (labor / material / scope / duration).
- Contingency posture view.
- Scenario set (base / upside / downside).
- Recommendation memo.

## Confidence banner pattern

```
References: capex_line_items@2026-03-31 (starter),
labor_rates__charlotte@2026-03-31 (sample),
material_costs__southeast_residential@2026-03-31 (sample),
contingency_assumptions@2026-03-31 (starter).
```
