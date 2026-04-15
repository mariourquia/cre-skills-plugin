# Metrics used by asset_manager

All metrics are defined canonically in `_core/metrics.md`. This pack uses them; it does not
redefine them. Target bands are overlay-driven.

| Slug | Why this role cares | Cadence |
|---|---|---|
| `physical_occupancy` | Operating signal against plan. | Weekly, monthly |
| `leased_occupancy` | Forward-pipeline against plan. | Weekly |
| `economic_occupancy` | Combined drag vs. plan. | Monthly |
| `renewal_acceptance_rate` | Retention outcome vs. underwrite. | Monthly |
| `blended_lease_trade_out` | Rent-growth vs. plan. | Monthly |
| `concession_rate` | Pricing / fair-housing pattern. | Monthly |
| `delinquency_rate_30plus` | Financial risk / cashflow. | Weekly |
| `collections_rate` | Cash capture. | Monthly |
| `bad_debt_rate` | Write-off drag. | Monthly, T12 |
| `make_ready_days` | Turn productivity → revenue-days. | Weekly |
| `turnover_rate` | Operating stability / cost driver. | Monthly, T12 |
| `payroll_per_unit` | Labor efficiency vs. benchmark. | Monthly, T12 |
| `rm_per_unit` | R&M vs. benchmark. | Monthly, T12 |
| `controllable_opex_per_unit` | Controllables vs. plan. | Monthly, T12 |
| `revenue_variance_to_budget` | Revenue accountability. | Monthly |
| `expense_variance_to_budget` | Expense accountability. | Monthly |
| `noi` | Headline asset outcome. | Monthly, T12 |
| `noi_margin` | Efficiency signal. | Monthly, T12 |
| `dscr` | Debt cushion. | Monthly, T12 |
| `debt_yield` | Debt cushion, refi capacity. | Monthly, T12 |
| `capex_spend_vs_plan` | Capital plan execution. | YTD |
| `renovation_yield_on_cost` | Program economics vs. underwrite. | Quarterly (if applicable) |
| `stabilization_pace_vs_plan` | Lease-up outcome vs. plan. | Weekly (if in lease_up) |
| `renewal_rent_delta_dollars` | Dollars captured per retained lease. | Monthly |
| `forecast_accuracy` | Planning discipline. | T6 months |
| `budget_attainment` | YTD plan vs. actual. | YTD |
| `asset_watchlist_score` | Composite risk; watchlist trigger. | As-of (weekly) |
| `same_store_noi_growth` | Portfolio cohort context. | T12 vs. prior T12 |
