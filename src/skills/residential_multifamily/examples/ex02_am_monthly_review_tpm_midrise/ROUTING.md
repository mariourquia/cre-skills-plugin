# Example 02 — ROUTING

## Matched rules

- `r002_asset_manager_monthly_review` (primary)
- `r003_tpm_oversight_weekly` (secondary pack load because owner-side asker in `owner_oversight` mode)
- `r009_direct_workflow` — workflow `monthly_asset_management_review` and nested `third_party_manager_scorecard_review`

## Axis resolution

| Axis | Resolved to | Source |
|---|---|---|
| `asset_class` | `residential_multifamily` | default |
| `segment` | `middle_market` | property master |
| `form_factor` | `urban_mid_rise` | property master |
| `lifecycle_stage` | `stabilized` | property master |
| `management_mode` | `third_party_managed` + `owner_oversight` loaded (asker side) | property master + session role |
| `role` | `asset_manager` | session context |
| `workflow` | `monthly_asset_management_review` | inferred |
| `market` | `Nashville` | property master |
| `submarket` | `The Gulch` | property master |
| `output_type` | `operating_review` (with embedded `scorecard` and `memo`) | request text |
| `decision_severity` | `recommendation` | internal IC review; not `final` external |
| `org_id` | `examples_org` | session context |

## Packs loaded

- Role pack: `roles/asset_manager/` (primary).
- Role pack: `roles/third_party_manager_oversight_lead/` (loaded secondary; mode is `owner_oversight`).
- Workflow pack: `workflows/monthly_asset_management_review/`.
- Workflow pack: `workflows/third_party_manager_scorecard_review/` (invoked inside the AM review).
- Segment overlay: `overlays/segments/middle_market/`.
- Form-factor overlay: `overlays/form_factor/urban_mid_rise/`.
- Lifecycle overlay: `overlays/lifecycle/stabilized/`.
- Management-mode overlays: `overlays/management_mode/third_party_managed/` + `overlays/management_mode/owner_oversight/`.
- Org overlay: `overlays/org/examples_org/`.

## References loaded

| Path | Category | as-of | Status | Fallback |
|---|---|---|---|---|
| `reference/normalized/market_rents__nashville_mf.csv` | market_rent_benchmark | 2026-03-31 | sample | ask_user |
| `reference/normalized/concession_benchmarks__nashville_mf.csv` | concession_benchmark | 2026-03-31 | sample | use_prior_period |
| `reference/normalized/collections_benchmarks__southeast_mf.csv` | occupancy_benchmark | 2026-03-31 | sample | use_portfolio_average |
| `reference/normalized/tpm_scorecard_weights.csv` | approval_threshold_policy | 2026-01-01 | starter | refuse |
| `reference/derived/role_kpi_targets.csv` | occupancy_benchmark | 2026-01-15 | starter | refuse |

## Metrics engaged

- `physical_occupancy`, `leased_occupancy`, `economic_occupancy`
- `notice_exposure`, `renewal_acceptance_rate`
- `delinquency_rate_30plus`, `collections_rate`, `bad_debt_rate`
- `blended_lease_trade_out`, `rent_growth_new_lease`, `rent_growth_renewal`
- `controllable_opex_per_unit`, `payroll_per_unit`, `rm_per_unit`, `utilities_per_unit`
- `noi`, `noi_margin`, `budget_attainment`
- `report_timeliness`, `kpi_completeness`, `variance_explanation_completeness`, `budget_adherence`, `staffing_vacancy_rate_tpm`, `tpm_collections_performance`, `tpm_turn_performance`, `service_level_adherence`, `approval_response_time_tpm`, `audit_issue_count_and_severity`
- `asset_watchlist_score`

## Gates surfaced

- No gated actions opened by the review itself (internal IC read).
- If AM requests a `final` LP / lender-facing version: row 20 `final_external_submission` routes.
- Any TPM contract change or vendor amendment triggered by review: row 19.

## Templates selected

- `templates/monthly_reviews/monthly_asset_management_memo.md` (top-level memo).
- `templates/monthly_reviews/monthly_property_scorecard__middle_market.md` (plan-vs-actual backbone).
- `templates/tpm_oversight/tpm_scorecard__middle_market.md` (TPM performance).
- `templates/tpm_oversight/tpm_audit_issue_log.md` (observed gaps).
- `templates/budget_forecast/variance_commentary_template.md` (referenced for narrative discipline).

## Output shape

- Variance narrative by P&L line with TPM-provided explanations and owner-side assessment of completeness (`variance_explanation_completeness` is itself surfaced).
- TPM composite scorecard score with dimension scores and weight resolution.
- Watchlist assessment with drivers and exit criteria.
- Action list for the AM's next TPM meeting + decisions requested.
- Confidence banner surfacing sample / starter reference status.
