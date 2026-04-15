# Metrics used by coo_operations_leader

All metrics are defined canonically in `_core/metrics.md`. This pack uses them; it does not
redefine them. The COO consumes rollups and does not author site- or asset-level metrics.

| Slug | Why this role cares | Cadence |
|---|---|---|
| `same_store_noi_growth` | Portfolio cohort outcome consumed. | T12 vs. prior T12 |
| `budget_attainment` | Portfolio plan-vs-actual consumed. | YTD |
| `forecast_accuracy` | Planning discipline across ops / asset teams. | T6 months |
| `asset_watchlist_score` | Top-of-mind risk items. | As-of (weekly) |
| `physical_occupancy` | Region-weighted consumed. | Weekly, monthly |
| `leased_occupancy` | Region-weighted consumed. | Weekly |
| `economic_occupancy` | Region-weighted consumed. | Monthly |
| `delinquency_rate_30plus` | Region-weighted consumed. | Weekly |
| `make_ready_days` | Ops productivity signal consumed. | Weekly |
| `turnover_rate` | Operating stability consumed. | Monthly, T12 |
| `payroll_per_unit` | Labor efficiency consumed. | Monthly, T12 |
| `controllable_opex_per_unit` | Portfolio controllables consumed. | Monthly, T12 |
| `noi` | Outcome consumed at portfolio. | Monthly, T12 |
| `service_level_adherence` | TPM SLA health consumed. | T90 |
| `report_timeliness` | TPM and internal reporting consumed. | Monthly (T6 rolling) |
| `kpi_completeness` | Reporting completeness consumed. | Monthly |
| `variance_explanation_completeness` | Narrative completeness consumed. | Monthly |
