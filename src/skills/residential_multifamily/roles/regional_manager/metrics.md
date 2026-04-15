# Metrics used by regional_manager

All metrics are defined canonically in `_core/metrics.md`. This pack uses them; it does not
redefine them. Target bands are overlay-driven.

| Slug | Why this role cares | Cadence |
|---|---|---|
| `physical_occupancy` | Headline operating signal across the region. | Weekly, monthly |
| `leased_occupancy` | Forward-looking occupancy; drives CAP triggers. | Weekly |
| `economic_occupancy` | Captures vacancy + concession + delinquency drag. | Monthly |
| `notice_exposure` | Near-term vacancy risk region-wide. | Weekly |
| `renewal_offer_rate` | Process discipline across all sites (100% target). | Weekly |
| `renewal_acceptance_rate` | Retention outcome. | Monthly |
| `blended_lease_trade_out` | Region-level rent growth. | Monthly |
| `concession_rate` | Pricing discipline and fair-housing pattern check. | Monthly |
| `delinquency_rate_30plus` | Financial risk and legal-notice exposure. | Weekly |
| `collections_rate` | Revenue capture discipline. | Weekly, monthly |
| `bad_debt_rate` | Write-off discipline. | Monthly, T12 |
| `make_ready_days` | Turn productivity. | Weekly |
| `turnover_rate` | Operating stability. | Monthly, T12 |
| `repeat_work_order_rate` | Vendor and quality signal. | Monthly |
| `payroll_per_unit` | Site labor efficiency across region. | Monthly, T12 |
| `rm_per_unit` | Repairs discipline. | Monthly, T12 |
| `controllable_opex_per_unit` | Primary opex dial for region. | Monthly, T12 |
| `revenue_variance_to_budget` | Revenue accountability at site level. | Monthly |
| `expense_variance_to_budget` | Expense accountability at site level. | Monthly |
| `noi` | Outcome measure for the region. | Monthly, T12 |
| `budget_attainment` | Headline accountability vs. plan. | YTD |
| `forecast_accuracy` | Discipline of site-level forecasting. | T6 months |
| `asset_watchlist_score` | Composite risk view per property. | As-of |
