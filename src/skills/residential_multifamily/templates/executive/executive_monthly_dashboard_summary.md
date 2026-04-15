---
template_slug: executive_monthly_dashboard_summary
title: Executive Monthly Dashboard Summary
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [coo_operations_leader, cfo_finance_leader, ceo_executive_leader]
  output_type: dashboard
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/derived/role_kpi_targets.csv
  - reference/normalized/market_rents__{market}_mf.csv
produced_by: workflows/executive_operating_summary_generation, workflows/monthly_asset_management_review
---

# Executive Monthly Dashboard Summary

**Portfolio / fund.** {{portfolio_name}}
**Period.** {{period_month}}
**Prepared by.** {{prepared_by}}

## Confidence banner

- KPI target source: {{role_kpi_targets_source}} (status: {{role_kpi_targets_status}})
- Market rents as-of: {{market_rents_as_of}} (status: {{market_rents_status}})

## Portfolio panel

| Dimension | MTD | YTD | Prior year same period | Target / plan |
|---|---|---|---|---|
| Revenue | {{rev_mtd}} | {{rev_ytd}} | {{rev_py}} | {{rev_target}} |
| Total opex | {{opex_mtd}} | {{opex_ytd}} | {{opex_py}} | {{opex_target}} |
| NOI | {{noi_mtd}} | {{noi_ytd}} | {{noi_py}} | {{noi_target}} |
| `same_store_noi_growth` | {{ss_noi_growth}} | {{ss_noi_growth_ytd}} | {{ss_noi_growth_py}} | {{ss_noi_growth_target}} |
| Weighted `physical_occupancy` | {{weighted_physical_occupancy}} | {{weighted_physical_occupancy_ytd}} | {{weighted_physical_occupancy_py}} | {{target_weighted_physical_occupancy}} |
| Weighted `economic_occupancy` | {{weighted_economic_occupancy}} | {{weighted_economic_occupancy_ytd}} | {{weighted_economic_occupancy_py}} | {{target_weighted_economic_occupancy}} |
| Weighted `delinquency_rate_30plus` | {{weighted_delinquency_30plus}} | {{weighted_delinquency_30plus_ytd}} | {{weighted_delinquency_30plus_py}} | {{target_weighted_delinquency}} |
| Portfolio `budget_attainment` | {{budget_attainment}} | {{budget_attainment_ytd}} | {{budget_attainment_py}} | {{target_budget_attainment}} |
| `capex_spend_vs_plan` | {{capex_spend_vs_plan}} | {{capex_spend_vs_plan_ytd}} | {{capex_spend_vs_plan_py}} | {{target_capex_spend_vs_plan}} |

## Market / segment cuts

| Cut | Weight (units) | Occupancy | Delinquency | Trade-out | NOI variance |
|---|---|---|---|---|---|
| {{cut_1}} | {{cut_1_weight}} | {{cut_1_occ}} | {{cut_1_delinq}} | {{cut_1_trade}} | {{cut_1_noi_var}} |
| {{cut_2}} | {{cut_2_weight}} | {{cut_2_occ}} | {{cut_2_delinq}} | {{cut_2_trade}} | {{cut_2_noi_var}} |
| {{cut_3}} | {{cut_3_weight}} | {{cut_3_occ}} | {{cut_3_delinq}} | {{cut_3_trade}} | {{cut_3_noi_var}} |

## Balance sheet and liquidity

- Cash on hand: {{cash_on_hand}}
- Reserves (portfolio): {{reserves_portfolio}}
- Upcoming debt maturities (next 12): {{debt_maturities_next_12}}
- DSCR weighted average: {{weighted_dscr}}
- Debt yield weighted average: {{weighted_debt_yield}}

## Capital deployment

- Acquisitions under evaluation: {{acquisitions_under_eval}}
- Dispositions in process: {{dispositions_in_process}}
- Development pipeline value: {{dev_pipeline_value}}
- Refi candidates next 12 months: {{refi_candidates}}

## Operating themes this month

{{operating_themes}}

## Risks elevated to executive

{{executive_risks}}

## Decisions requested this month

{{decisions_requested_this_month}}

---

*Template status: starter.*
