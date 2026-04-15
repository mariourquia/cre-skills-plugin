# Example — Change Order Review (abridged)

**Prompt:** "Review the PCO submitted for Ashford Park amenity refresh."

**Inputs:** CO package + original contract + prior COs + estimator baseline + schedule record + contingency status.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- market: Charlotte
- role: construction_manager
- project_id: amenity_refresh_ashford_park_2026
- output_type: memo
- decision_severity: action_requires_approval

## Expected packs loaded

- `workflows/change_order_review/`
- `workflows/capex_estimate_generation/` (re-estimate)
- `overlays/segments/middle_market/`

## Expected references

- `reference/normalized/capex_line_items__amenity.csv`
- `reference/normalized/labor_rates__charlotte.csv`
- `reference/normalized/material_costs__southeast_residential.csv`
- `reference/derived/contingency_assumptions__{org}.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Gates potentially triggered

- Minor CO: row 10.
- Major CO: row 11.
- Safety-scope deferral: row 4.

## Expected output shape

- CO review memo with scope, cost, schedule, contingency impact.
- Updated contract value and schedule record.
- Approval request with correct row based on dollar.

## Confidence banner pattern

```
References: capex_line_items__amenity@2026-03-31 (starter),
contingency_assumptions@2026-03-31 (starter).
```
