# Example — Weekly Site Ops Review (abridged)

**Prompt:** "Build this week's site ops review for Ashford Park."

**Inputs:** property master + rent roll snapshot + T7 funnel + T7 delinquency + open WOs + turn pipeline.

**Output shape:** see `templates/weekly_site_ops_review__middle_market.md`.

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

- `roles/property_manager/`
- `workflows/lead_to_lease_funnel_review/` (invoked within)
- `workflows/delinquency_collections/` (invoked within)
- `workflows/work_order_triage/` (invoked within)
- `workflows/unit_turn_make_ready/` (invoked within)
- `overlays/segments/middle_market/`
- `overlays/form_factor/garden/`
- `overlays/lifecycle/stabilized/`
- `overlays/management_mode/third_party_managed/`

## Expected references

- `reference/normalized/market_rents__charlotte_mf.csv`
- `reference/normalized/concession_benchmarks__charlotte_mf.csv`
- `reference/normalized/collections_benchmarks__southeast_mf.csv`
- `reference/derived/role_kpi_targets.csv`
- `overlays/segments/middle_market/service_standards.md`

## Gates potentially triggered

- Delinquency aging transitions that would trigger legal notice (approval matrix row 1).
- Any proposed concession > policy limit (row 13).

## Confidence banner pattern

```
References: market_rents@2026-03-31 (sample, replace with live), concessions@2026-03-31 (sample, replace with live), collections_benchmarks@2026-02-28 (starter, operator overlay pending).
Data freshness: rent roll snapshot at 2026-04-12 08:00 local; funnel data live CRM; WO data live.
```
