# Example — Monthly Asset Review (abridged)

**Prompt:** "Run the monthly asset review for Ashford Park. Include NOI variance, forecast accuracy, capex status, and the watchlist view."

**Inputs:** asset business plan; current-month actuals; prior-period forecast; debt schedule and covenants; capex tracker; renovation tracker (if applicable); TPM scorecard and oversight memo (if TPM).

**Output shape:** see `templates/monthly_asset_review_memo.md`.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- lifecycle_stage: stabilized
- management_mode: third_party_managed
- role: asset_manager
- market: Charlotte
- output_type: memo
- decision_severity: recommendation

## Expected packs loaded

- `roles/asset_manager/`
- `workflows/monthly_asset_review/`
- `workflows/debt_covenant_check/`
- `workflows/tpm_scorecard_review/` (if TPM asset)
- `overlays/segments/middle_market/`
- `overlays/form_factor/garden/`
- `overlays/lifecycle/stabilized/`
- `overlays/management_mode/third_party_managed/`

## Expected references

- `reference/normalized/market_rents__charlotte_mf.csv`
- `reference/normalized/cap_rate_benchmarks__charlotte_mf.csv`
- `reference/normalized/operating_expense_benchmarks__charlotte_mf.csv`
- `reference/derived/watchlist_scoring.yaml`
- `reference/derived/role_kpi_targets.csv`
- `reference/derived/same_store_set.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Gates potentially triggered

- Any deviation from approved business plan routes row 17.
- Any covenant-cushion breach risk routes row 14 via reporting_finance_ops_lead.
- Any capex reallocation above category cap routes (rows 8, 10, 11).

## Confidence banner pattern

```
References: market_rents@{as_of_date}, cap_rates@{as_of_date}, opex_benchmarks@{as_of_date},
watchlist_scoring@{as_of_date} (statuses per record). Operating data live; capex tracker as-of
run time; TPM scorecard for period just closed.
```
