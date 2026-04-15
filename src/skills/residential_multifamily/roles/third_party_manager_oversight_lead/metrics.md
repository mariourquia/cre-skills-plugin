# Metrics used by third_party_manager_oversight_lead

All metrics are defined canonically in `_core/metrics.md`. This pack uses them; it does not
redefine them. Target bands are PMA- and overlay-driven.

| Slug | Why this role cares | Cadence |
|---|---|---|
| `report_timeliness` | PMA reporting SLA adherence. | Monthly (T6 rolling) |
| `kpi_completeness` | Owner-report completeness check. | Monthly |
| `variance_explanation_completeness` | Ownership of explanations on variances. | Monthly |
| `budget_adherence_tpm` | TPM plan-vs-actual at line level. | YTD |
| `staffing_vacancy_rate_tpm` | TPM staffing execution. | As-of |
| `tpm_collections_performance` | Market-relative collections. | Monthly |
| `tpm_turn_performance` | Market-relative turn speed. | T90 |
| `service_level_adherence` | SLA catalog compliance. | T90 |
| `approval_response_time_tpm` | Owner-side process; process signal owned jointly. | T90 |
| `audit_issue_count_and_severity` | Open audit finding posture. | As-of |
| `physical_occupancy` | Headline op signal consumed from TPM. | Weekly |
| `leased_occupancy` | Forward pipeline consumed from TPM. | Weekly |
| `economic_occupancy` | Combined drag consumed from TPM. | Monthly |
| `renewal_acceptance_rate` | Retention outcome consumed. | Monthly |
| `blended_lease_trade_out` | Rent-growth consumed. | Monthly |
| `delinquency_rate_30plus` | Risk signal consumed. | Weekly |
| `collections_rate` | Cash capture consumed. | Monthly |
| `make_ready_days` | Turn productivity consumed. | Weekly |
| `repeat_work_order_rate` | Quality signal consumed. | Monthly |
| `revenue_variance_to_budget` | Revenue accountability consumed. | Monthly |
| `expense_variance_to_budget` | Expense accountability consumed. | Monthly |
| `noi` | Outcome consumed. | Monthly, T12 |
| `budget_attainment` | YTD vs. plan consumed. | YTD |
| `forecast_accuracy` | Planning discipline consumed. | T6 months |
| `asset_watchlist_score` | Risk view consumed. | As-of (weekly) |
