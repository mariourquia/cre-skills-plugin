# Example — Quarterly Portfolio Review (abridged)

**Prompt:** "Run the Q2 2026 portfolio review; include watchlist movers and concentration."

**Inputs:** 3 months of AM reviews + same-store set + market references + watchlist config + fund debt schedule.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- management_mode: third_party_managed + self_managed mix
- role: portfolio_manager
- output_type: operating_review
- decision_severity: action_requires_approval

## Expected packs loaded

- `workflows/quarterly_portfolio_review/`
- `workflows/monthly_asset_management_review/` (3 months per asset)
- `workflows/market_rent_refresh/` (trend commentary)
- `overlays/segments/middle_market/`

## Expected references

- `reference/derived/role_kpi_targets.csv`
- `reference/normalized/watchlist_scoring.yaml`
- `reference/derived/same_store_set__{org}.yaml`
- `reference/normalized/occupancy_benchmarks__{market}_mf.csv`
- `reference/normalized/collections_benchmarks__{region}_mf.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Gates potentially triggered

- Board submission -> row 16.
- LP quarterly submission -> row 15.

## Expected output shape

- Portfolio KPI dashboard.
- Same-store trend with quarterly sparkline.
- Concentration and watchlist distribution.
- Fund-level covenant posture.
- Capex and renovation program summary.
- Board packet and LP draft.

## Confidence banner pattern

```
References: watchlist_scoring@2026-03-31 (starter), same_store_set@2026-03-31 (starter),
role_kpi_targets@2026-03-31 (starter).
```
