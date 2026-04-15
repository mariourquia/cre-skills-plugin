---
template_slug: monthly_owner_report__middle_market
title: Monthly Owner Report (Middle-Market)
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation]
  management_mode: [self_managed, third_party_managed]
  role: [property_manager, regional_manager, asset_manager, third_party_manager_oversight_lead]
  output_type: operating_review
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/derived/role_kpi_targets.csv
  - reference/normalized/market_rents__{market}_mf.csv
produced_by: roles/property_manager, workflows/monthly_property_operating_review
---

# Monthly Owner Report

**Property.** {{property_name}} ({{property_id}})
**Owner entity.** {{owner_entity}}
**Period.** {{period_month}}
**Prepared by.** {{prepared_by}}

## Executive summary

{{executive_summary}}

## Confidence banner

- KPI target source: {{role_kpi_targets_source}} (status: {{role_kpi_targets_status}})
- Market rents as-of: {{market_rents_as_of}} (status: {{market_rents_status}})

## Operating summary

- `physical_occupancy` (month-end): {{physical_occupancy}}
- `leased_occupancy` (month-end): {{leased_occupancy}}
- `economic_occupancy` (MTD): {{economic_occupancy}}
- `delinquency_rate_30plus`: {{delinquency_rate_30plus}}
- `blended_lease_trade_out` (MTD): {{blended_lease_trade_out}}

## Financial summary

| Line | Month actual | Month budget | Variance | YTD actual | YTD budget | YTD variance |
|---|---|---|---|---|---|---|
| Total revenue | {{rev_actual}} | {{rev_budget}} | {{rev_var}} | {{ytd_rev_actual}} | {{ytd_rev_budget}} | {{ytd_rev_var}} |
| Total opex | {{opex_actual}} | {{opex_budget}} | {{opex_var}} | {{ytd_opex_actual}} | {{ytd_opex_budget}} | {{ytd_opex_var}} |
| NOI | {{noi_actual}} | {{noi_budget}} | {{noi_var}} | {{ytd_noi_actual}} | {{ytd_noi_budget}} | {{ytd_noi_var}} |
| Capex spend | {{capex_actual}} | {{capex_budget}} | {{capex_var}} | {{ytd_capex_actual}} | {{ytd_capex_budget}} | {{ytd_capex_var}} |

## Variance commentary

{{variance_narrative}}

## Leasing and renewals

- New leases signed: {{new_leases}}
- Renewals signed: {{renewals_signed}}
- `rent_growth_new_lease`: {{rent_growth_new_lease}}
- `rent_growth_renewal`: {{rent_growth_renewal}}

## Maintenance and turn

- Turns completed: {{turns_completed}}
- `make_ready_days` median: {{make_ready_days_median}}
- `open_work_orders` month-end: {{open_work_orders_month_end}}

## Capital projects

| Project | Budget | Spend MTD | Spend YTD | % complete | Status |
|---|---|---|---|---|---|
| {{capex_project_1}} | {{capex_project_1_budget}} | {{capex_project_1_mtd}} | {{capex_project_1_ytd}} | {{capex_project_1_pct}} | {{capex_project_1_status}} |
| {{capex_project_2}} | {{capex_project_2_budget}} | {{capex_project_2_mtd}} | {{capex_project_2_ytd}} | {{capex_project_2_pct}} | {{capex_project_2_status}} |

## Items for owner decision

{{owner_decision_items}}

## Distributions (if applicable)

- Declared: {{declared_distributions}}
- Paid in period: {{paid_distributions}}
- Reserves balance: {{reserves_balance}}

---

*Template status: starter. Any submission tagged `final` to lender or LP requires approval per approval matrix.*
