# Example — Lead-to-Lease Funnel Review (abridged)

**Prompt:** "Run the weekly funnel review for Ashford Park; flag anything below band."

**Inputs:** CRM lead log (T30) + tour log + application log + lease log + rent roll snapshot + `reference/normalized/market_rents__charlotte_mf.csv` + `reference/derived/role_kpi_targets.csv`.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- lifecycle_stage: stabilized
- management_mode: third_party_managed
- role: property_manager
- market: Charlotte, submarket: South End
- output_type: kpi_review
- decision_severity: recommendation

## Expected packs loaded

- `workflows/lead_to_lease_funnel_review/`
- `overlays/segments/middle_market/`
- `overlays/form_factor/garden/`
- `overlays/lifecycle/stabilized/`
- `overlays/management_mode/third_party_managed/`

## Expected references

- `reference/normalized/market_rents__charlotte_mf.csv`
- `reference/normalized/concession_benchmarks__charlotte_mf.csv`
- `reference/normalized/occupancy_benchmarks__charlotte_mf.csv`
- `reference/derived/role_kpi_targets.csv`
- `reference/derived/funnel_conversion_benchmarks__middle_market.csv`

## Gates potentially triggered

- Fair-housing scan hit (row 3).
- Concession proposal above policy (row 13).

## Expected output shape

- Funnel KPI table with T7 and T30 comparisons against band.
- Binding-constraint finding with cited metric slugs.
- Fair-housing guardrail scan result.
- Action list with owners, due dates, approval gates.
- Confidence banner with reference `as_of_date` and `status` tags.

## Confidence banner pattern

```
References: funnel_conversion_benchmarks__middle_market@2026-03-31 (sample, replace with live),
market_rents__charlotte_mf@2026-03-31 (sample), role_kpi_targets@2026-03-31 (starter).
Data freshness: CRM live through 2026-04-12 08:00 local; rent roll snapshot 2026-04-12 08:00 local.
```
