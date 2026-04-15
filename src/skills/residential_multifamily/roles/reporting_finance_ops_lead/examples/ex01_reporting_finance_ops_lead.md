# Example — Month-End Close + Variance Pack (abridged)

**Prompt:** "Close March 2026 for the Southeast region. Produce the variance pack, covenant cushion memos, and lender QA sign-offs."

**Inputs:** GLs (per property, consolidated); rent rolls; budget / forecast; debt and covenant schedules; variance materiality policy; close calendar.

**Output shape:** `templates/monthly_close_binder.md` + `templates/variance_reporting_pack__middle_market.md` + `templates/covenant_cushion_memo.md`.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- role: reporting_finance_ops_lead
- output_type: operating_review + memo
- decision_severity: recommendation (for AM / CFO sign-off)

## Expected packs loaded

- `roles/reporting_finance_ops_lead/`
- `workflows/month_end_close/`
- `workflows/variance_reporting_pack/`
- `workflows/covenant_cushion_memo/`
- `workflows/lender_compliance_package/`
- `workflows/forecast_accuracy_measurement/`
- `overlays/segments/middle_market/`

## Expected references

- `reference/normalized/chart_of_accounts__middle_market.csv`
- `reference/normalized/close_calendar__portfolio.csv`
- `reference/normalized/covenant_calculation_library.csv`
- `reference/normalized/variance_materiality_policy.csv`
- `reference/derived/same_store_set.csv`

## Gates potentially triggered

- Any covenant cushion breach risk escalates row 14 to cfo_finance_leader.
- Any material variance indicating plan deviation routes row 17 via asset_manager.
- Any finance-domain reference update is logged per row 20.
- Any lender-facing final routes row 14.

## Confidence banner pattern

```
References: chart_of_accounts@{as_of_date}, close_calendar@{as_of_date},
covenant_calculation_library@{as_of_date, per loan}, variance_materiality_policy@{as_of_date},
same_store_set@{as_of_date} (statuses per record). GLs as of close snapshot.
```
