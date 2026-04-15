# Example — Renewal and Retention Plan (abridged)

**Prompt:** "Build the June renewal plan for Ashford Park. 28 leases expiring. Stay inside policy on concessions."

**Inputs:** expiring-lease list + rent roll snapshot + `reference/normalized/market_rents__charlotte_mf.csv` + concession overlay + `reference/derived/renewal_uplift_bands__middle_market.csv`.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- lifecycle_stage: stabilized
- management_mode: third_party_managed
- role: property_manager
- market: Charlotte, submarket: South End
- output_type: memo
- decision_severity: action_requires_approval

## Expected packs loaded

- `workflows/renewal_retention/`
- `overlays/segments/middle_market/`
- `overlays/form_factor/garden/`
- `overlays/lifecycle/stabilized/`
- `overlays/management_mode/third_party_managed/`

## Expected references

- `reference/normalized/market_rents__charlotte_mf.csv`
- `reference/normalized/concession_benchmarks__charlotte_mf.csv`
- `reference/derived/renewal_uplift_bands__middle_market.csv`
- `reference/derived/role_kpi_targets.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Gates potentially triggered

- Concession above policy or offer outside uplift band -> `approval_request` row 13.
- Non-renewal notice (jurisdiction overlay conditional) -> `approval_request` row 1.
- Fair-housing disparity signal -> `approval_request` row 3.

## Expected output shape

- Renewal segmentation table with tiers, prior effective rent, market rent, proposed offer, band flag.
- Renewal strategy memo with blended uplift sensitivity.
- Draft resident communication set (portal + email variants) with `draft_for_review` banner.
- Approval request bundle listing any offer outside policy.
- Acceptance tracker checklist with follow-up cadence.

## Confidence banner pattern

```
References: market_rents__charlotte_mf@2026-03-31 (sample), renewal_uplift_bands__middle_market@2026-03-31 (starter),
approval_threshold_defaults@2026-03-31 (starter).
Data freshness: rent roll snapshot 2026-04-12 08:00 local; expiring-lease list live.
```
