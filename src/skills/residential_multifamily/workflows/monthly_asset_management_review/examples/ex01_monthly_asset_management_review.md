# Example — Monthly Asset Management Review (abridged)

**Prompt:** "Run the monthly AM review for the South End portfolio. Include covenant cushion, watchlist, and same-store rollup."

**Inputs:** closed property reviews per asset + per-asset T12 + reforecast + per-loan covenant definitions + capex plan/actuals + watchlist scoring + same-store set.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden / suburban_mid_rise (varies by asset)
- lifecycle_stage: stabilized / renovation
- management_mode: third_party_managed
- role: asset_manager
- market: Charlotte, submarket: South End
- output_type: operating_review
- decision_severity: action_requires_approval

## Expected packs loaded

- `workflows/monthly_asset_management_review/`
- `workflows/monthly_property_operating_review/` (per asset)
- `workflows/third_party_manager_scorecard_review/` (per TPM asset)
- `workflows/reforecast/` (if reforecast window)
- `workflows/capital_project_intake_and_prioritization/` (if capex deviations)
- `workflows/cost_to_complete_review/` (if applicable)
- `workflows/change_order_review/` (if applicable)
- `overlays/segments/middle_market/`
- `overlays/management_mode/owner_oversight/`
- `overlays/management_mode/third_party_managed/`

## Expected references

- `reference/derived/role_kpi_targets.csv`
- `reference/normalized/watchlist_scoring.yaml`
- `reference/normalized/covenant_definitions__{loan}.yaml` (per loan)
- `reference/normalized/market_rents__charlotte_mf.csv`
- `reference/normalized/concession_benchmarks__charlotte_mf.csv`
- `reference/normalized/occupancy_benchmarks__charlotte_mf.csv`
- `reference/normalized/collections_benchmarks__southeast_mf.csv`
- `reference/derived/same_store_set__{org}.yaml`
- `reference/normalized/approval_threshold_defaults.csv`

## Gates potentially triggered

- Covenant warning escalation -> CFO path.
- Watchlist escalation -> executive path.
- Capex plan deviation above threshold -> rows 8-11.
- Lender compliance submission -> row 14.
- Investor / board submission -> rows 15 / 16.
- Fair-housing flag echo -> row 3 (verified).

## Expected output shape

- Per-asset AM review (KPI, variance, covenants, capex, watchlist, AM agenda).
- Portfolio rollup (same-store, concentration, watchlist distribution, covenant posture).
- Covenant cushion runway tables.
- Approval request bundle.
- Lender compliance scaffold (if due).
- Investor / LP draft (if due).

## Confidence banner pattern

```
References: watchlist_scoring@2026-03-31 (starter), covenant_definitions__loan_X@2026-01-15 (sample, loan doc overlay pending),
role_kpi_targets@2026-03-31 (starter), same_store_set@2026-03-31 (starter),
market_rents__charlotte_mf@2026-03-31 (sample), concession_benchmarks__charlotte_mf@2026-03-31 (sample).
```
