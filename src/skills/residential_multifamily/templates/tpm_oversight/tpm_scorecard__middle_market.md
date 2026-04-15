---
template_slug: tpm_scorecard__middle_market
title: Third-Party Manager Scorecard (Middle-Market)
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation]
  management_mode: [third_party_managed, owner_oversight]
  role: [third_party_manager_oversight_lead, asset_manager, portfolio_manager, coo_operations_leader]
  output_type: scorecard
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/normalized/tpm_scorecard_weights.csv
  - reference/derived/role_kpi_targets.csv
produced_by: workflows/third_party_manager_scorecard_review
---

# Third-Party Manager Scorecard

**Property.** {{property_name}} ({{property_id}})
**TPM.** {{tpm_name}}
**Scorecard period.** {{scorecard_period}}
**Prepared by.** {{prepared_by}}

## Confidence banner

- Scorecard weight reference as-of: {{tpm_scorecard_weights_as_of}} (status: {{tpm_scorecard_weights_status}})
- KPI target source: {{role_kpi_targets_source}} (status: {{role_kpi_targets_status}})

## Dimension scores

| Dimension (metric) | Score (1-5) | Weight | Weighted | Commentary |
|---|---|---|---|---|
| `report_timeliness` | {{score_report_timeliness}} | {{weight_report_timeliness}} | {{weighted_report_timeliness}} | {{note_report_timeliness}} |
| `kpi_completeness` | {{score_kpi_completeness}} | {{weight_kpi_completeness}} | {{weighted_kpi_completeness}} | {{note_kpi_completeness}} |
| `variance_explanation_completeness` | {{score_variance_explanation}} | {{weight_variance_explanation}} | {{weighted_variance_explanation}} | {{note_variance_explanation}} |
| `budget_adherence` | {{score_budget_adherence}} | {{weight_budget_adherence}} | {{weighted_budget_adherence}} | {{note_budget_adherence}} |
| `staffing_vacancy_rate_tpm` | {{score_staffing_vacancy}} | {{weight_staffing_vacancy}} | {{weighted_staffing_vacancy}} | {{note_staffing_vacancy}} |
| `tpm_collections_performance` | {{score_collections}} | {{weight_collections}} | {{weighted_collections}} | {{note_collections}} |
| `tpm_turn_performance` | {{score_turn}} | {{weight_turn}} | {{weighted_turn}} | {{note_turn}} |
| `service_level_adherence` | {{score_sla}} | {{weight_sla}} | {{weighted_sla}} | {{note_sla}} |
| `approval_response_time_tpm` | {{score_approval_response}} | {{weight_approval_response}} | {{weighted_approval_response}} | {{note_approval_response}} |
| `audit_issue_count_and_severity` | {{score_audit}} | {{weight_audit}} | {{weighted_audit}} | {{note_audit}} |

**Composite score.** {{composite_score}}
**Prior period composite.** {{composite_score_prior}}
**Trend.** {{trend}}

## Observed gaps

{{observed_gaps_narrative}}

## Corrective actions

| # | Action | Owner (TPM / owner-side) | Due | Approval gate |
|---|---|---|---|---|
| 1 | {{correct_1}} | {{correct_1_owner}} | {{correct_1_due}} | {{correct_1_gate}} |
| 2 | {{correct_2}} | {{correct_2_owner}} | {{correct_2_due}} | {{correct_2_gate}} |

## Contract / escalation posture

- Contract-renewal trigger points: {{contract_trigger_points}}
- Escalation threshold crossed?: {{escalation_threshold_crossed}}
- Rebid under consideration?: {{rebid_consideration}}

---

*Template status: starter.*
