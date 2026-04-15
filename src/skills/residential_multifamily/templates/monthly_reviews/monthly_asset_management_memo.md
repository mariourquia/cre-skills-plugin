---
template_slug: monthly_asset_management_memo
title: Monthly Asset Management Memo
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [asset_manager, portfolio_manager]
  output_type: memo
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/derived/role_kpi_targets.csv
  - reference/normalized/market_rents__{market}_mf.csv
  - reference/normalized/tpm_scorecard_weights.csv
produced_by: roles/asset_manager, workflows/monthly_asset_management_review
---

# Monthly Asset Management Memo

**Property.** {{property_name}} ({{property_id}}) — {{market}} / {{submarket}}
**Period.** {{period_month}}
**Prepared by.** {{prepared_by}} (asset_manager)

## Headline

{{headline_statement}}

## Confidence banner

- KPI target source: {{role_kpi_targets_source}} (status: {{role_kpi_targets_status}})
- Market rents as-of: {{market_rents_as_of}} (status: {{market_rents_status}})
- TPM scorecard weights as-of: {{tpm_scorecard_weights_as_of}} (status: {{tpm_scorecard_weights_status}})

## Plan-vs-actual snapshot

| Metric | Plan (UW / budget) | Actual | Delta | Assessment |
|---|---|---|---|---|
| `physical_occupancy` | {{plan_physical_occupancy}} | {{actual_physical_occupancy}} | {{delta_physical_occupancy}} | {{assessment_physical_occupancy}} |
| `economic_occupancy` | {{plan_economic_occupancy}} | {{actual_economic_occupancy}} | {{delta_economic_occupancy}} | {{assessment_economic_occupancy}} |
| `delinquency_rate_30plus` | {{plan_delinquency_rate_30plus}} | {{actual_delinquency_rate_30plus}} | {{delta_delinquency_rate_30plus}} | {{assessment_delinquency_rate_30plus}} |
| `blended_lease_trade_out` | {{plan_blended_trade_out}} | {{actual_blended_trade_out}} | {{delta_blended_trade_out}} | {{assessment_blended_trade_out}} |
| `controllable_opex_per_unit` (T12) | {{plan_controllable_opex_per_unit}} | {{actual_controllable_opex_per_unit}} | {{delta_controllable_opex_per_unit}} | {{assessment_controllable_opex_per_unit}} |
| `noi` (MTD / YTD) | {{plan_noi}} | {{actual_noi}} | {{delta_noi}} | {{assessment_noi}} |

## TPM performance (if applicable)

| Dimension | Score | Weight | Weighted score | Commentary |
|---|---|---|---|---|
| `report_timeliness` | {{tpm_report_timeliness_score}} | {{weight_report_timeliness}} | {{weighted_report_timeliness}} | {{note_report_timeliness}} |
| `kpi_completeness` | {{tpm_kpi_completeness_score}} | {{weight_kpi_completeness}} | {{weighted_kpi_completeness}} | {{note_kpi_completeness}} |
| `budget_adherence` | {{tpm_budget_adherence_score}} | {{weight_budget_adherence}} | {{weighted_budget_adherence}} | {{note_budget_adherence}} |
| `service_level_adherence` | {{tpm_sla_adherence_score}} | {{weight_sla_adherence}} | {{weighted_sla_adherence}} | {{note_sla_adherence}} |
| `staffing_vacancy_rate_tpm` | {{tpm_staffing_vacancy_score}} | {{weight_staffing_vacancy}} | {{weighted_staffing_vacancy}} | {{note_staffing_vacancy}} |
| `approval_response_time_tpm` | {{tpm_approval_response_score}} | {{weight_approval_response}} | {{weighted_approval_response}} | {{note_approval_response}} |
| `audit_issue_count_and_severity` | {{tpm_audit_issues_score}} | {{weight_audit_issues}} | {{weighted_audit_issues}} | {{note_audit_issues}} |

**Composite TPM score.** {{tpm_composite_score}}

## Watchlist assessment

- Status: {{watchlist_status}}
- Drivers: {{watchlist_drivers}}
- Corrective actions and timelines: {{watchlist_corrective_actions}}

## Asset-plan reaffirmation

- Hold / sell / refi recommendation: {{hold_sell_refi_recommendation}}
- Drivers of recommendation: {{recommendation_drivers}}

## Decisions requested

| # | Decision | Required by | Approval path |
|---|---|---|---|
| 1 | {{decision_1}} | {{decision_1_by}} | {{decision_1_path}} |
| 2 | {{decision_2}} | {{decision_2_by}} | {{decision_2_path}} |

---

*Template status: starter. Any recommendation marked `final` to lenders or LPs requires approval per approval matrix.*
