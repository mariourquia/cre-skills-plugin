# Example — Monthly Portfolio Review (abridged)

**Prompt:** "Build the monthly portfolio review for Q1 2026 with same-store cohort, debt ladder, and watchlist movement."

**Inputs:** all AM monthly asset reviews; debt schedule by asset; covenant schedule; same-store cohort definition; concentration targets.

**Output shape:** see `templates/monthly_portfolio_review.md`.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- role: portfolio_manager
- output_type: operating_review
- decision_severity: recommendation

## Expected packs loaded

- `roles/portfolio_manager/`
- `workflows/monthly_portfolio_review/`
- `workflows/debt_covenant_check/`
- `workflows/concentration_monitoring/`
- `overlays/segments/middle_market/`

## Expected references

- `reference/normalized/cap_rate_benchmarks__{market}_mf.csv`
- `reference/normalized/debt_rate_reference__{product}.csv`
- `reference/derived/same_store_set.csv`
- `reference/normalized/watchlist_scoring.yaml`
- `reference/derived/portfolio_concentration_targets.csv`
- `reference/derived/role_kpi_targets.csv`

## Gates potentially triggered

- Any disposition / acquisition / recap recommendation routes row 15 / 16 via executive leadership.
- Any material concentration shift routes row 17.
- Any lender- or investor-facing final routes row 14 / 15 / 16.

## Confidence banner pattern

```
References: cap_rate_benchmarks@{as_of_date}, debt_rate_reference@{as_of_date},
same_store_set@{as_of_date}, watchlist_scoring@{as_of_date}, concentration_targets@{as_of_date}
(statuses per record). Asset inputs per each monthly_asset_review for the period.
```
