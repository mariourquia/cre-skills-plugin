# Example — Market Rent Refresh (abridged)

**Prompt:** "Refresh Charlotte market rents; staleness threshold crossed."

**Inputs:** current benchmarks + shop list + overlay staleness threshold.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- market: Charlotte, submarket: South End
- role: leasing_manager
- output_type: checklist
- decision_severity: recommendation

## Expected packs loaded

- `workflows/market_rent_refresh/`
- `workflows/rent_comp_intake/` (downstream handoff)
- `overlays/segments/middle_market/`

## Expected references

- `reference/normalized/market_rents__charlotte_mf.csv`
- `reference/normalized/concession_benchmarks__charlotte_mf.csv`
- `reference/normalized/comp_normalization_rules__middle_market.yaml`

## Gates potentially triggered

- Downstream (in `rent_comp_intake`): magnitude delta gate per reference update flow.

## Expected output shape

- Freshness status per benchmark.
- Refresh plan checklist (shop list, dates, owners).
- Current-state memo (market trend).
- Bundle handoff record to `rent_comp_intake`.

## Confidence banner pattern

```
References: market_rents__charlotte_mf@2026-03-31 (stale per overlay, status=sample),
concession_benchmarks__charlotte_mf@2026-03-31 (sample),
comp_normalization_rules__middle_market@2026-03-31 (starter).
```
