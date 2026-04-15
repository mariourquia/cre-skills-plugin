---
template_slug: variance_commentary_template
title: Variance Commentary Template
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [property_manager, regional_manager, asset_manager, reporting_finance_ops_lead]
  output_type: memo
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/derived/role_kpi_targets.csv
produced_by: roles/reporting_finance_ops_lead, workflows/monthly_property_operating_review
---

# Variance Commentary

**Property.** {{property_name}} ({{property_id}})
**Period.** {{period_month}}
**Prepared by.** {{prepared_by}}
**Materiality threshold.** {{materiality_threshold_source}}  (source: {{materiality_source_ref}})

## Confidence banner

- KPI target source: {{role_kpi_targets_source}} (status: {{role_kpi_targets_status}})

## Revenue variances (vs. budget)

| Line | Budget | Actual | Variance | Above materiality? | Classification | Root cause | One-time? | Corrective / forward action |
|---|---|---|---|---|---|---|---|---|
| Base rent | {{base_rent_budget}} | {{base_rent_actual}} | {{base_rent_var}} | {{base_rent_material}} | {{base_rent_class}} | {{base_rent_root}} | {{base_rent_onetime}} | {{base_rent_action}} |
| Vacancy / loss | {{vacancy_budget}} | {{vacancy_actual}} | {{vacancy_var}} | {{vacancy_material}} | {{vacancy_class}} | {{vacancy_root}} | {{vacancy_onetime}} | {{vacancy_action}} |
| Concessions | {{concessions_budget}} | {{concessions_actual}} | {{concessions_var}} | {{concessions_material}} | {{concessions_class}} | {{concessions_root}} | {{concessions_onetime}} | {{concessions_action}} |
| Delinquency / bad debt | {{delinq_budget}} | {{delinq_actual}} | {{delinq_var}} | {{delinq_material}} | {{delinq_class}} | {{delinq_root}} | {{delinq_onetime}} | {{delinq_action}} |
| Other income | {{other_budget}} | {{other_actual}} | {{other_var}} | {{other_material}} | {{other_class}} | {{other_root}} | {{other_onetime}} | {{other_action}} |

## Opex variances (vs. budget)

| Line | Budget | Actual | Variance | Above materiality? | Classification | Root cause | One-time? | Corrective / forward action |
|---|---|---|---|---|---|---|---|---|
| Payroll | {{payroll_budget}} | {{payroll_actual}} | {{payroll_var}} | {{payroll_material}} | {{payroll_class}} | {{payroll_root}} | {{payroll_onetime}} | {{payroll_action}} |
| R&M | {{rm_budget}} | {{rm_actual}} | {{rm_var}} | {{rm_material}} | {{rm_class}} | {{rm_root}} | {{rm_onetime}} | {{rm_action}} |
| Turn | {{turn_budget}} | {{turn_actual}} | {{turn_var}} | {{turn_material}} | {{turn_class}} | {{turn_root}} | {{turn_onetime}} | {{turn_action}} |
| Utilities | {{util_budget}} | {{util_actual}} | {{util_var}} | {{util_material}} | {{util_class}} | {{util_root}} | {{util_onetime}} | {{util_action}} |
| Insurance | {{ins_budget}} | {{ins_actual}} | {{ins_var}} | {{ins_material}} | {{ins_class}} | {{ins_root}} | {{ins_onetime}} | {{ins_action}} |
| Real-estate tax | {{tax_budget}} | {{tax_actual}} | {{tax_var}} | {{tax_material}} | {{tax_class}} | {{tax_root}} | {{tax_onetime}} | {{tax_action}} |
| Marketing | {{mkt_budget}} | {{mkt_actual}} | {{mkt_var}} | {{mkt_material}} | {{mkt_class}} | {{mkt_root}} | {{mkt_onetime}} | {{mkt_action}} |
| Admin | {{admin_budget}} | {{admin_actual}} | {{admin_var}} | {{admin_material}} | {{admin_class}} | {{admin_root}} | {{admin_onetime}} | {{admin_action}} |

## Classification rubric (reminder)

- **Timing.** Temporary phasing; trues up over subsequent months.
- **Pricing / volume.** Change in market rent, concession, or volume (leases, turns, work orders).
- **Contracted.** Known contract escalation or renewal adjustment.
- **External.** Tax, insurance, utility rate, or regulatory change.
- **Operational.** Controllable execution signal — the PM owns the corrective action.
- **Structural.** Persistent, not reversible without plan change; escalate to AM / portfolio.

## Overall NOI variance

- NOI variance: {{noi_variance}}
- % of budget NOI: {{noi_variance_pct}}
- YTD implication for `budget_attainment`: {{ytd_budget_attainment_implication}}

## Summary

{{summary_narrative}}

---

*Template status: starter. Materiality thresholds and classification rubric live in the org overlay; this template links to them, does not embed them.*
