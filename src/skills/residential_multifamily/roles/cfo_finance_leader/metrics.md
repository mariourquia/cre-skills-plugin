# Metrics used by cfo_finance_leader

All metrics are defined canonically in `_core/metrics.md`. This pack uses them; it does not
redefine them. The CFO consumes rollups and does not author day-to-day metrics.

| Slug | Why this role cares | Cadence |
|---|---|---|
| `noi` | Portfolio outcome consumed. | Monthly, T12 |
| `noi_margin` | Efficiency signal consumed. | Monthly, T12 |
| `dscr` | Covenant cushion per loan. | Monthly, T12 |
| `debt_yield` | Covenant cushion / refi capacity. | Monthly, T12 |
| `revenue_variance_to_budget` | Property / portfolio revenue accountability consumed. | Monthly |
| `expense_variance_to_budget` | Property / portfolio expense accountability consumed. | Monthly |
| `budget_attainment` | Portfolio YTD plan-vs-actual. | YTD |
| `forecast_accuracy` | Planning discipline consumed. | T6 months |
| `capex_spend_vs_plan` | Capital pacing consumed. | YTD |
| `same_store_noi_growth` | Cohort performance consumed. | T12 vs. prior T12 |
| `asset_watchlist_score` | Risk posture consumed. | As-of |
| `report_timeliness` | Reporting discipline consumed. | Monthly (T6 rolling) |
| `kpi_completeness` | Reporting completeness consumed. | Monthly |
| `variance_explanation_completeness` | Narrative completeness consumed. | Monthly |
| `cost_to_complete` | Dev / reno budget forward view consumed. | Monthly |
| `draw_cycle_time` | Treasury / process signal consumed. | T90 |
