# Example — Monthly Property Operating Review (abridged)

**Prompt:** "Build the March monthly review for Ashford Park. Flag anything off band."

**Inputs:** month-end GL + rent roll + child workflow inputs + target bands.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- lifecycle_stage: stabilized
- management_mode: third_party_managed
- role: property_manager
- market: Charlotte
- output_type: operating_review
- decision_severity: recommendation

## Expected packs loaded

- `workflows/monthly_property_operating_review/`
- `workflows/lead_to_lease_funnel_review/`
- `workflows/delinquency_collections/`
- `workflows/unit_turn_make_ready/`
- `workflows/vendor_dispatch_sla_review/`
- `overlays/segments/middle_market/`
- `overlays/management_mode/third_party_managed/`

## Expected references

- `reference/derived/role_kpi_targets.csv`
- `reference/normalized/market_rents__charlotte_mf.csv`
- `reference/normalized/concession_benchmarks__charlotte_mf.csv`
- `reference/normalized/collections_benchmarks__southeast_mf.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Gates potentially triggered

- Fair-housing row 3 from child workflow.
- Legal-notice / eviction rows from child workflow.
- Concession row 13 from child workflow.

## Expected output shape

- Property scorecard across occupancy, leasing, renewal, collections, turn, WO, financial variance.
- Narrative memo with cited slugs.
- Action list with owners, dates, gates.
- Owner / AM submission draft.

## Confidence banner pattern

```
References: role_kpi_targets@2026-03-31 (starter), market_rents@2026-03-31 (sample),
concession_benchmarks@2026-03-31 (sample), collections_benchmarks@2026-02-28 (starter).
```
