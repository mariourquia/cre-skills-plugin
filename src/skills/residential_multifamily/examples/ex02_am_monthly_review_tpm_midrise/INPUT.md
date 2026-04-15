# Example 02 — INPUT

## User prompt

> "Pull me the monthly AM review for Liberty Apartments for March. We are behind on budget. I want to see what happened, a TPM scorecard read, and what the TPM is doing about it. Flag watchlist status. I will be presenting to the IC on Monday."

## Session context

- asker.role: `asset_manager`
- asker.org_id: `examples_org`
- property lookup: `property_id = liberty_apartments_nashville_01`
- property master: `property_name=Liberty Apartments`, `segment=middle_market`, `form_factor=urban_mid_rise`, `lifecycle_stage=stabilized`, `management_mode=third_party_managed` (with `owner_oversight` loaded owner-side), `market=Nashville`, `submarket=The Gulch`, `unit_count_rentable=212`.
- Period: March 2026 close.
- T-12 and budget attached via the internal data room.
- TPM: `tpm_name=Acme MF Management`.

## Known data points

- `physical_occupancy` March month-end: 92.1% (plan 94.0%).
- `economic_occupancy` MTD: 88.4% (plan 90.5%).
- `delinquency_rate_30plus`: 5.9% (plan 4.0%).
- `blended_lease_trade_out` MTD: +1.2% (plan +3.0%).
- `controllable_opex_per_unit` T12: above plan by $31.
- NOI MTD variance to budget: -6.8%.
- TPM submitted monthly report on 2026-04-09 (target: 10th business day, late by 1 business day).
- KPI completeness on submission: 85% (target: 100%). Variance commentary completeness: 70%.

## Reference availability snapshot

- `reference/normalized/market_rents__nashville_mf.csv` — present, status: sample, as_of 2026-03-31.
- `reference/normalized/concession_benchmarks__nashville_mf.csv` — present, status: sample, as_of 2026-03-31.
- `reference/normalized/collections_benchmarks__southeast_mf.csv` — present, status: sample, as_of 2026-03-31.
- `reference/normalized/tpm_scorecard_weights.csv` — present, status: starter, as_of 2026-01-01.
- `reference/derived/role_kpi_targets.csv` — present, status: starter, as_of 2026-01-15.

## Decision / autonomy context

- decision_severity expected: `recommendation`.
- Gated actions likely: none this month (internal review); if IC requests a `final` LP/lender-facing version, that routes per approval matrix.
