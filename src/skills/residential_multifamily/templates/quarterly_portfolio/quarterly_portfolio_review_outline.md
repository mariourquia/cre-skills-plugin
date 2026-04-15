---
template_slug: quarterly_portfolio_review_outline
title: Quarterly Portfolio Review Outline
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [portfolio_manager, asset_manager, director_of_operations, coo_operations_leader]
  output_type: operating_review
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/derived/role_kpi_targets.csv
  - reference/normalized/market_rents__{market}_mf.csv
  - reference/normalized/occupancy_benchmarks__{market}_mf.csv
produced_by: roles/portfolio_manager, workflows/quarterly_portfolio_review
---

# Quarterly Portfolio Review

**Portfolio / fund.** {{portfolio_name}}
**Quarter.** {{quarter}} ({{quarter_start}} to {{quarter_end}})
**Prepared by.** {{prepared_by}}

## Confidence banner

- KPI target source: {{role_kpi_targets_source}} (status: {{role_kpi_targets_status}})
- Market references as-of: {{market_references_as_of}} (status: {{market_references_status}})

## Portfolio headline

| Metric | Q value | Prior Q | YoY | Portfolio target |
|---|---|---|---|---|
| `same_store_noi_growth` | {{ss_noi_growth}} | {{ss_noi_growth_prior_q}} | {{ss_noi_growth_yoy}} | {{target_ss_noi_growth}} |
| Weighted `physical_occupancy` | {{weighted_physical_occupancy}} | {{weighted_physical_occupancy_prior_q}} | {{weighted_physical_occupancy_yoy}} | {{target_weighted_physical_occupancy}} |
| Weighted `economic_occupancy` | {{weighted_economic_occupancy}} | {{weighted_economic_occupancy_prior_q}} | {{weighted_economic_occupancy_yoy}} | {{target_weighted_economic_occupancy}} |
| Weighted `delinquency_rate_30plus` | {{weighted_delinquency_30plus}} | {{weighted_delinquency_30plus_prior_q}} | {{weighted_delinquency_30plus_yoy}} | {{target_weighted_delinquency}} |
| Weighted `blended_lease_trade_out` | {{weighted_blended_trade_out}} | {{weighted_blended_trade_out_prior_q}} | {{weighted_blended_trade_out_yoy}} | {{target_weighted_blended_trade_out}} |
| Portfolio `budget_attainment` | {{budget_attainment}} | {{budget_attainment_prior_q}} | {{budget_attainment_yoy}} | {{target_budget_attainment}} |

## Market cuts

| Market | # props | # units | Weight (units) | Occ. | Delinq. | Trade-out | NOI var. |
|---|---|---|---|---|---|---|---|
| {{market_1}} | {{market_1_props}} | {{market_1_units}} | {{market_1_weight}} | {{market_1_occ}} | {{market_1_delinq}} | {{market_1_trade_out}} | {{market_1_noi_var}} |
| {{market_2}} | {{market_2_props}} | {{market_2_units}} | {{market_2_weight}} | {{market_2_occ}} | {{market_2_delinq}} | {{market_2_trade_out}} | {{market_2_noi_var}} |
| {{market_3}} | {{market_3_props}} | {{market_3_units}} | {{market_3_weight}} | {{market_3_occ}} | {{market_3_delinq}} | {{market_3_trade_out}} | {{market_3_noi_var}} |

- Portfolio concentration flags: {{concentration_flags}}

## Watchlist

| Property | Reason on watchlist | Weeks on watchlist | Corrective actions | Exit criteria |
|---|---|---|---|---|
| {{watchlist_property_1}} | {{watchlist_reason_1}} | {{watchlist_weeks_1}} | {{watchlist_actions_1}} | {{watchlist_exit_1}} |
| {{watchlist_property_2}} | {{watchlist_reason_2}} | {{watchlist_weeks_2}} | {{watchlist_actions_2}} | {{watchlist_exit_2}} |

## Lease expirations and rollover

- Q+1 expirations (units): {{expirations_q_plus_1}}
- Q+2 expirations (units): {{expirations_q_plus_2}}
- Concentration in single market / floor plan: {{expiration_concentrations}}

## Capital projects (portfolio roll-up)

- Active projects: {{active_capex_projects}}
- Total committed: {{total_committed_capex}}
- `capex_spend_vs_plan`: {{capex_spend_vs_plan}}
- Projects tracking red: {{red_projects}}

## Cycle snapshot cross-reference

See companion `quarterly_market_cycle_snapshot.md` for the market-cycle context underlying these numbers.

## Decisions requested

{{decisions_requested}}

---

*Template status: starter.*
