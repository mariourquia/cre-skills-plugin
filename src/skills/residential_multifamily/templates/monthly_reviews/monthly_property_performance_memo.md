---
template_slug: monthly_property_performance_memo
title: Monthly Property Performance Memo
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation]
  management_mode: [self_managed, third_party_managed]
  role: [property_manager, regional_manager, asset_manager]
  output_type: memo
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/derived/role_kpi_targets.csv
  - reference/normalized/market_rents__{market}_mf.csv
produced_by: roles/property_manager, workflows/monthly_property_operating_review
---

# Monthly Property Performance Memo

**Property.** {{property_name}} ({{property_id}}) — {{market}} / {{submarket}}
**Period.** {{period_month}}
**Prepared by.** {{prepared_by}} ({{role}})

## Headline

{{headline_statement}}

## Confidence banner

- KPI target source: {{role_kpi_targets_source}} (status: {{role_kpi_targets_status}})
- Market rents as-of: {{market_rents_as_of}} (status: {{market_rents_status}})

## What went right

{{what_went_right_narrative}}

## What went wrong

{{what_went_wrong_narrative}}

## Variance drivers (vs. budget)

| P&L line | Budget | Actual | Variance | Driver |
|---|---|---|---|---|
| Base rent | {{base_rent_budget}} | {{base_rent_actual}} | {{base_rent_variance}} | {{base_rent_driver}} |
| Vacancy / loss | {{vacancy_budget}} | {{vacancy_actual}} | {{vacancy_variance}} | {{vacancy_driver}} |
| Concessions | {{concessions_budget}} | {{concessions_actual}} | {{concessions_variance}} | {{concessions_driver}} |
| Delinquency / bad debt | {{delinq_budget}} | {{delinq_actual}} | {{delinq_variance}} | {{delinq_driver}} |
| Other income | {{other_income_budget}} | {{other_income_actual}} | {{other_income_variance}} | {{other_income_driver}} |
| Payroll | {{payroll_budget}} | {{payroll_actual}} | {{payroll_variance}} | {{payroll_driver}} |
| R&M | {{rm_budget}} | {{rm_actual}} | {{rm_variance}} | {{rm_driver}} |
| Utilities | {{utilities_budget}} | {{utilities_actual}} | {{utilities_variance}} | {{utilities_driver}} |
| Insurance / tax | {{ins_tax_budget}} | {{ins_tax_actual}} | {{ins_tax_variance}} | {{ins_tax_driver}} |
| NOI | {{noi_budget}} | {{noi_actual}} | {{noi_variance}} | {{noi_driver}} |

## Forward view — next 30 / 60 / 90

- Next 30: {{next_30_outlook}}
- Next 60: {{next_60_outlook}}
- Next 90: {{next_90_outlook}}

## Ask / escalations

- Owner decisions requested: {{owner_decisions_requested}}
- Regional decisions requested: {{regional_decisions_requested}}
- Approval requests opened or pending: {{approval_requests_open}}

---

*Template status: starter.*
