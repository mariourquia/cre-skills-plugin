---
template_slug: executive_weekly_operating_summary
title: Executive Weekly Operating Summary
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [coo_operations_leader, cfo_finance_leader, ceo_executive_leader, director_of_operations, portfolio_manager]
  output_type: operating_review
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/derived/role_kpi_targets.csv
  - reference/normalized/market_rents__{market}_mf.csv
produced_by: workflows/executive_operating_summary_generation
---

# Executive Weekly Operating Summary

**Portfolio / fund.** {{portfolio_name}}
**Week ending.** {{week_ending_date}}
**Prepared by.** {{prepared_by}}

## Confidence banner

- KPI target source: {{role_kpi_targets_source}} (status: {{role_kpi_targets_status}})
- Market references as-of: {{market_references_as_of}} (status: {{market_references_status}})

## One-paragraph headline

{{headline_paragraph}}

## Portfolio KPIs (weighted)

| Metric | This week | Prior week | 4-week trend | Portfolio target | Flag |
|---|---|---|---|---|---|
| Weighted `physical_occupancy` | {{weighted_physical_occupancy}} | {{weighted_physical_occupancy_prior}} | {{weighted_physical_occupancy_trend}} | {{target_weighted_physical_occupancy}} | {{flag_physical_occupancy}} |
| Weighted `leased_occupancy` | {{weighted_leased_occupancy}} | {{weighted_leased_occupancy_prior}} | {{weighted_leased_occupancy_trend}} | {{target_weighted_leased_occupancy}} | {{flag_leased_occupancy}} |
| Weighted `delinquency_rate_30plus` | {{weighted_delinquency_30plus}} | {{weighted_delinquency_30plus_prior}} | {{weighted_delinquency_30plus_trend}} | {{target_weighted_delinquency}} | {{flag_delinquency}} |
| Weighted `blended_lease_trade_out` | {{weighted_blended_trade_out}} | {{weighted_blended_trade_out_prior}} | {{weighted_blended_trade_out_trend}} | {{target_weighted_blended_trade_out}} | {{flag_blended_trade_out}} |
| Portfolio `budget_attainment` (MTD) | {{budget_attainment_mtd}} | {{budget_attainment_mtd_prior}} | {{budget_attainment_mtd_trend}} | {{target_budget_attainment}} | {{flag_budget_attainment}} |

## Red / amber / green heatmap (properties)

| Property | Market | Status | Drivers | Actions in flight |
|---|---|---|---|---|
| {{prop_1}} | {{prop_1_market}} | {{prop_1_status}} | {{prop_1_drivers}} | {{prop_1_actions}} |
| {{prop_2}} | {{prop_2_market}} | {{prop_2_status}} | {{prop_2_drivers}} | {{prop_2_actions}} |
| {{prop_3}} | {{prop_3_market}} | {{prop_3_status}} | {{prop_3_drivers}} | {{prop_3_actions}} |
| {{prop_4}} | {{prop_4_market}} | {{prop_4_status}} | {{prop_4_drivers}} | {{prop_4_actions}} |

## Watchlist changes

- Added: {{watchlist_added}}
- Removed: {{watchlist_removed}}
- Still on: {{watchlist_still_on}}

## Top 5 open items for executive attention

| # | Item | Owner | Due | Approval gate |
|---|---|---|---|---|
| 1 | {{exec_item_1}} | {{exec_item_1_owner}} | {{exec_item_1_due}} | {{exec_item_1_gate}} |
| 2 | {{exec_item_2}} | {{exec_item_2_owner}} | {{exec_item_2_due}} | {{exec_item_2_gate}} |
| 3 | {{exec_item_3}} | {{exec_item_3_owner}} | {{exec_item_3_due}} | {{exec_item_3_gate}} |
| 4 | {{exec_item_4}} | {{exec_item_4_owner}} | {{exec_item_4_due}} | {{exec_item_4_gate}} |
| 5 | {{exec_item_5}} | {{exec_item_5_owner}} | {{exec_item_5_due}} | {{exec_item_5_gate}} |

## Cross-portfolio themes

{{cross_portfolio_themes}}

## Capital and development headlines

{{capital_dev_headlines}}

## Risks and watch-outs

{{risks_watchouts}}

---

*Template status: starter.*
