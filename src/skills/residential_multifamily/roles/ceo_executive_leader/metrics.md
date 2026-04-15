# Metrics used by ceo_executive_leader

All metrics are defined canonically in `_core/metrics.md`. This pack uses them; it does not
redefine them. The CEO consumes rollups.

| Slug | Why this role cares | Cadence |
|---|---|---|
| `same_store_noi_growth` | Headline portfolio performance cohort. | T12 vs. prior T12 |
| `budget_attainment` | Portfolio YTD plan-vs-actual. | YTD |
| `forecast_accuracy` | Planning discipline signal. | T6 months |
| `asset_watchlist_score` | Top-of-mind risk items consumed. | As-of |
| `noi` | Portfolio outcome consumed. | Monthly, T12 |
| `physical_occupancy` | Portfolio-weighted operating signal consumed. | Monthly |
| `leased_occupancy` | Forward pipeline consumed. | Monthly |
| `economic_occupancy` | Combined drag consumed. | Monthly |
| `delinquency_rate_30plus` | Portfolio risk signal consumed. | Monthly |
| `dscr` | Covenant cushion per loan consumed. | Monthly, T12 |
| `debt_yield` | Covenant cushion / refi capacity consumed. | Monthly, T12 |
| `service_level_adherence` | TPM SLA posture consumed. | T90 |
