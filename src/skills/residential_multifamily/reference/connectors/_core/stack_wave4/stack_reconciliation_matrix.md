# Stack Reconciliation Matrix — Wave 4

Status: wave_4_authoritative
Cross-references: per-adapter `reconciliation_checks.yaml`, per-adapter `reconciliation_rules.md`.

This matrix is the operator-facing summary of every cross-system reconciliation
the wave-4 stack runs. Tolerances cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`;
no numeric thresholds are hardcoded here.

| check_id | Sources | Tolerance Ref | Frequency | Severity | Affected Workflows | Remediation Runbook |
|---|---|---|---|---|---|---|
| recon_af_units_vs_assumptions | appfolio | unit_count_band | daily | blocker | monthly_property_operating_review | property_crosswalk_issue.md |
| recon_af_collections_vs_intacct_revenue | appfolio + intacct | revenue_basis_band | monthly | warning | monthly_property_operating_review, monthly_asset_management_review | unmapped_account_handling.md |
| recon_af_property_list_vs_intacct_dim | appfolio + intacct | n/a (presence check) | weekly | blocker | monthly_property_operating_review | property_crosswalk_issue.md |
| recon_pc_costs_vs_intacct_capex | procore + intacct | capex_posting_band | weekly | blocker | cost_to_complete_review, draw_package_review | procore_common_issues.md::cost_posting_lag |
| recon_dp_approved_vs_setup | dealpath + appfolio + intacct + procore | handoff_lag_band | weekly | warning → blocker (after lag) | acquisition_handoff, post_ic_property_setup | dealpath_common_issues.md::closed_deal_no_setup |
| recon_excel_freshness_vs_use | excel + workflow_clock | staleness_band | daily | warning → blocker (after staleness) | market_rent_refresh, renewal_retention, budget_build | benchmark_refresh.md |
| recon_vendor_three_way | appfolio + intacct + procore | identity_match_band | weekly | warning | vendor_dispatch_sla_review, change_order_review, owner_approval_routing | vendor_crosswalk_mismatch.md |
| recon_market_tag_consistency | excel + appfolio | submarket_tag_band | weekly | warning | market_rent_refresh, renewal_retention | benchmark_refresh.md::submarket_drift |
| recon_staffing_benchmark_vs_actual | excel + hr_payroll + intacct | staffing_drift_band | monthly | warning | budget_build, monthly_property_operating_review | benchmark_refresh.md::staffing_drift |
| recon_labor_rate_vs_payroll | excel + hr_payroll + intacct | labor_rate_drift_band | quarterly | warning | budget_build, capex_estimate_generation | benchmark_refresh.md::labor_drift |
| recon_pc_co_pending_vs_posted | procore + intacct | co_posting_lag_band | weekly | warning → blocker | change_order_review, draw_package_review | procore_common_issues.md::co_posting_lag |
| recon_pc_draw_vs_posted | procore + intacct | draw_posting_lag_band | weekly | warning → blocker | draw_package_review | procore_common_issues.md::draw_posting_lag |
| recon_dp_dev_to_pc | dealpath + procore | dev_handoff_lag | weekly | warning → blocker | capital_project_intake_and_prioritization | dealpath_common_issues.md::dev_handoff |
| recon_pc_to_af_at_delivery | procore + appfolio | delivery_handoff_band | event-driven | blocker | lease_up_first_period | procore_common_issues.md::delivery_handoff |
| recon_intacct_unmapped_account | intacct | n/a (presence) | daily | blocker | monthly_property_operating_review, monthly_asset_management_review, reforecast | unmapped_account_handling.md |
| recon_capex_to_opex_misclass | intacct | account_class_band | monthly | warning | monthly_asset_management_review, capex_spend_vs_plan | sage_intacct_common_issues.md::capex_opex_misclass |
| recon_manual_journal_property_attribution | intacct | n/a (presence) | weekly | warning → blocker (close period) | monthly_property_operating_review | sage_intacct_common_issues.md::manual_journal_attrib |
| recon_appfolio_eviction_vs_legal | appfolio + manual | n/a (cross-ref) | weekly | warning | delinquency_collections | appfolio_common_issues.md::eviction_status |
| recon_excel_rent_comp_outliers | excel | comp_outlier_band | weekly | warning | market_rent_refresh | excel_market_survey_common_issues.md::outliers |
| recon_excel_luxury_contamination | excel | segment_match_band | weekly | warning | market_rent_refresh, renewal_retention | excel_market_survey_common_issues.md::segment_mismatch |
| recon_tpm_file_submission_lag | manual + appfolio | tpm_submission_band | weekly | warning → blocker | third_party_manager_scorecard_review | manual_sources_common_issues.md::tpm_lag |

## Cross-system anti-patterns guarded against

- Two systems each updating the same field in close succession (race condition; resolved by `posting_period_close_wins`).
- Vendor records auto-created in three systems with slightly different names (resolved by `vendor_three_way` weekly recon + `vendor_crosswalk_mismatch.md`).
- Excel benchmark file refreshed by analyst but workflow still consuming stale version (resolved by `excel_freshness_vs_use` daily recon).
- Procore CO approved but Intacct not yet posted, then snapshot captured for executive summary (resolved by `co_pending_vs_posted` weekly recon + flagged in handoff payload).

## Confidence model

Each reconciliation outcome contributes to the workflow's `effective_confidence`:

- `pass` (within `silent_audit` band) → no impact
- `pass_with_drift` (within `confidence_reduced` band) → degrade to `medium` if `high`
- `fail` (outside `blocker` band) → block workflow per `workflow_activation_map.yaml::blocking_issues`

The `effective_confidence` is annotated in every workflow output. Operators
cannot suppress it; only `manual_override_approval.md` can release a blocked
workflow, and the override carries `audit_trail.md` requirements.
