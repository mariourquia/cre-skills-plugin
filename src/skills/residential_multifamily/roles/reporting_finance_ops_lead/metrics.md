# Metrics used by reporting_finance_ops_lead

All metrics are defined canonically in `_core/metrics.md`. This pack uses them; it does not
redefine them. Target bands are policy- and overlay-driven.

| Slug | Why this role cares | Cadence |
|---|---|---|
| `noi` | Headline finance output at property / portfolio. | Monthly, T12 |
| `noi_margin` | Efficiency signal. | Monthly, T12 |
| `dscr` | Covenant cushion per loan. | Monthly, T12 |
| `debt_yield` | Covenant cushion / refi capacity. | Monthly, T12 |
| `revenue_variance_to_budget` | Property-level revenue accountability. | Monthly |
| `expense_variance_to_budget` | Property-level expense accountability. | Monthly |
| `budget_attainment` | YTD plan vs. actual; published to history. | YTD |
| `forecast_accuracy` | Measured monthly; published to history reference (write). | T6 months |
| `capex_spend_vs_plan` | Capex pacing vs. plan. | YTD |
| `same_store_noi_growth` | Cohort view for portfolio and investor packages. | T12 vs. prior T12 |
| `asset_watchlist_score` | Consumed for watchlist pack. | As-of |
| `report_timeliness` | Closes calendar adherence. | Monthly (T6 rolling) |
| `kpi_completeness` | Owner-report completeness. | Monthly |
| `variance_explanation_completeness` | Narrative completeness. | Monthly |
| `draw_cycle_time` | Process KPI for projects with draws. | T90 |
| `cost_to_complete` | Forward dev / reno budget view. | Monthly |
