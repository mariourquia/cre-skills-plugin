# Metrics used by director_of_operations

All metrics are defined canonically in `_core/metrics.md`. This pack uses them; it does not
redefine them. Target bands are overlay-driven.

| Slug | Why this role cares | Cadence |
|---|---|---|
| `physical_occupancy` | Primary ops signal at region/portfolio weight. | Weekly, monthly |
| `leased_occupancy` | Forward pipeline at region/portfolio weight. | Weekly |
| `economic_occupancy` | Combined vacancy + concession + delinquency drag. | Monthly |
| `renewal_offer_rate` | Process discipline (100% target everywhere). | Weekly |
| `renewal_acceptance_rate` | Retention outcome. | Monthly |
| `blended_lease_trade_out` | Rent-growth performance. | Monthly |
| `concession_rate` | Pricing-discipline signal. | Monthly |
| `delinquency_rate_30plus` | Financial risk across regions. | Weekly |
| `collections_rate` | Revenue capture. | Weekly, monthly |
| `bad_debt_rate` | Write-off discipline. | Monthly, T12 |
| `make_ready_days` | Turn productivity. | Weekly |
| `turnover_rate` | Operating stability. | Monthly, T12 |
| `repeat_work_order_rate` | Quality / vendor signal. | Monthly |
| `payroll_per_unit` | Labor efficiency. | Monthly, T12 |
| `rm_per_unit` | Repairs discipline. | Monthly, T12 |
| `controllable_opex_per_unit` | Region-level controllables. | Monthly, T12 |
| `revenue_variance_to_budget` | Revenue accountability. | Monthly |
| `expense_variance_to_budget` | Expense accountability. | Monthly |
| `noi` | Outcome measure at region/portfolio. | Monthly, T12 |
| `budget_attainment` | YTD plan vs. actual. | YTD |
| `forecast_accuracy` | Forecasting discipline. | T6 months |
| `asset_watchlist_score` | Risk view per property, consumed at director level. | As-of |
| `same_store_noi_growth` | Portfolio-wide same-store performance. | T12 vs. prior T12 |
