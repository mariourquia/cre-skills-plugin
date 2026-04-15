# Metrics used by portfolio_manager

All metrics are defined canonically in `_core/metrics.md`. This pack uses them; it does not
redefine them. Target bands and concentration thresholds are overlay- and
fund-document-driven.

| Slug | Why this role cares | Cadence |
|---|---|---|
| `noi` | Portfolio-rolled and per-asset consumption. | Monthly, T12 |
| `noi_margin` | Efficiency signal. | Monthly, T12 |
| `dscr` | Debt cushion per asset, watched portfolio-wide. | Monthly, T12 |
| `debt_yield` | Debt cushion / refi capacity. | Monthly, T12 |
| `budget_attainment` | Portfolio plan-vs-actual. | YTD |
| `forecast_accuracy` | Planning discipline across asset_managers. | T6 months |
| `asset_watchlist_score` | At-risk asset ranking. | As-of (weekly) |
| `capex_spend_vs_plan` | Capital plan execution portfolio-wide. | YTD |
| `renovation_yield_on_cost` | Program economics across renovation assets. | Quarterly |
| `stabilization_pace_vs_plan` | Lease-up cohort view. | Weekly |
| `same_store_noi_growth` | Portfolio cohort outcome. | T12 vs. prior T12 |
| `occupancy_by_market` | Market-level performance vs. benchmark. | Weekly, monthly |
| `delinquency_by_market` | Market-level risk view. | Weekly, monthly |
| `turn_cost_by_market` | Market-level ops cost signal. | T12 |
| `portfolio_concentration_market` | Concentration vs. target band. | Monthly, quarterly |
