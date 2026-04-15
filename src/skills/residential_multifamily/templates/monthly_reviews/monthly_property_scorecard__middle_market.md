---
template_slug: monthly_property_scorecard__middle_market
title: Monthly Property Scorecard (Middle-Market)
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [stabilized, lease_up, renovation]
  management_mode: [self_managed, third_party_managed]
  role: [property_manager, regional_manager, asset_manager]
  output_type: scorecard
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/derived/role_kpi_targets.csv
  - reference/normalized/market_rents__{market}_mf.csv
  - reference/normalized/concession_benchmarks__{market}_mf.csv
  - reference/normalized/collections_benchmarks__{region}_mf.csv
produced_by: roles/property_manager, workflows/monthly_property_operating_review
---

# Monthly Property Scorecard

**Property.** {{property_name}} ({{property_id}}) — {{market}} / {{submarket}}
**Period.** {{period_month}} ({{period_start}} to {{period_end}})
**Segment / form / stage / mode.** middle_market / {{form_factor}} / {{lifecycle_stage}} / {{management_mode}}

## Confidence banner

- KPI target source: {{role_kpi_targets_source}} (as-of: {{role_kpi_targets_as_of}}, status: {{role_kpi_targets_status}})
- Market rents as-of: {{market_rents_as_of}} (status: {{market_rents_status}})
- Collections benchmark as-of: {{collections_benchmarks_as_of}} (status: {{collections_benchmarks_status}})

## Scorecard — Property Operations family

| Metric | Actual | Prior month | Target band | Delta vs. target | Trend |
|---|---|---|---|---|---|
| `physical_occupancy` | {{physical_occupancy}} | {{physical_occupancy_prior}} | {{target_physical_occupancy}} | {{delta_physical_occupancy}} | {{trend_physical_occupancy}} |
| `leased_occupancy` | {{leased_occupancy}} | {{leased_occupancy_prior}} | {{target_leased_occupancy}} | {{delta_leased_occupancy}} | {{trend_leased_occupancy}} |
| `economic_occupancy` | {{economic_occupancy}} | {{economic_occupancy_prior}} | {{target_economic_occupancy}} | {{delta_economic_occupancy}} | {{trend_economic_occupancy}} |
| `notice_exposure` | {{notice_exposure}} | {{notice_exposure_prior}} | {{target_notice_exposure}} | {{delta_notice_exposure}} | {{trend_notice_exposure}} |
| `renewal_offer_rate` | {{renewal_offer_rate}} | {{renewal_offer_rate_prior}} | {{target_renewal_offer_rate}} | {{delta_renewal_offer_rate}} | {{trend_renewal_offer_rate}} |
| `renewal_acceptance_rate` | {{renewal_acceptance_rate}} | {{renewal_acceptance_rate_prior}} | {{target_renewal_acceptance_rate}} | {{delta_renewal_acceptance_rate}} | {{trend_renewal_acceptance_rate}} |
| `turnover_rate` (T12) | {{turnover_rate_t12}} | {{turnover_rate_t12_prior}} | {{target_turnover_rate}} | {{delta_turnover_rate}} | {{trend_turnover_rate}} |
| `make_ready_days` | {{make_ready_days}} | {{make_ready_days_prior}} | {{target_make_ready_days}} | {{delta_make_ready_days}} | {{trend_make_ready_days}} |
| `average_days_vacant` | {{average_days_vacant}} | {{average_days_vacant_prior}} | {{target_average_days_vacant}} | {{delta_average_days_vacant}} | {{trend_average_days_vacant}} |
| `work_order_aging` (P2 median) | {{wo_aging_p2_median}} | {{wo_aging_p2_median_prior}} | {{target_wo_aging_p2}} | {{delta_wo_aging_p2}} | {{trend_wo_aging_p2}} |
| `repeat_work_order_rate` | {{repeat_work_order_rate}} | {{repeat_work_order_rate_prior}} | {{target_repeat_work_order_rate}} | {{delta_repeat_work_order_rate}} | {{trend_repeat_work_order_rate}} |

## Scorecard — Revenue and financial

| Metric | Actual | Prior month | Target band | Delta vs. target |
|---|---|---|---|---|
| `delinquency_rate_30plus` | {{delinquency_rate_30plus}} | {{delinquency_rate_30plus_prior}} | {{target_delinquency_rate_30plus}} | {{delta_delinquency_rate_30plus}} |
| `collections_rate` | {{collections_rate}} | {{collections_rate_prior}} | {{target_collections_rate}} | {{delta_collections_rate}} |
| `bad_debt_rate` (T12) | {{bad_debt_rate_t12}} | {{bad_debt_rate_t12_prior}} | {{target_bad_debt_rate}} | {{delta_bad_debt_rate}} |
| `concession_rate` | {{concession_rate}} | {{concession_rate_prior}} | {{target_concession_rate}} | {{delta_concession_rate}} |
| `rent_growth_new_lease` | {{rent_growth_new_lease}} | {{rent_growth_new_lease_prior}} | {{target_rent_growth_new_lease}} | {{delta_rent_growth_new_lease}} |
| `rent_growth_renewal` | {{rent_growth_renewal}} | {{rent_growth_renewal_prior}} | {{target_rent_growth_renewal}} | {{delta_rent_growth_renewal}} |
| `blended_lease_trade_out` | {{blended_lease_trade_out}} | {{blended_lease_trade_out_prior}} | {{target_blended_lease_trade_out}} | {{delta_blended_lease_trade_out}} |
| `controllable_opex_per_unit` (MTD) | {{controllable_opex_per_unit_mtd}} | {{controllable_opex_per_unit_mtd_prior}} | {{target_controllable_opex_per_unit}} | {{delta_controllable_opex_per_unit}} |
| `payroll_per_unit` (MTD) | {{payroll_per_unit_mtd}} | {{payroll_per_unit_mtd_prior}} | {{target_payroll_per_unit}} | {{delta_payroll_per_unit}} |
| `rm_per_unit` (MTD) | {{rm_per_unit_mtd}} | {{rm_per_unit_mtd_prior}} | {{target_rm_per_unit}} | {{delta_rm_per_unit}} |
| `utilities_per_unit` (MTD) | {{utilities_per_unit_mtd}} | {{utilities_per_unit_mtd_prior}} | {{target_utilities_per_unit}} | {{delta_utilities_per_unit}} |
| `noi` (MTD) | {{noi_mtd}} | {{noi_mtd_prior}} | {{target_noi_budget}} | {{delta_noi_budget}} |
| `noi_margin` | {{noi_margin}} | {{noi_margin_prior}} | {{target_noi_margin}} | {{delta_noi_margin}} |

## Rollup scoring

| Dimension | Score (1-5) | Commentary |
|---|---|---|
| Occupancy and leasing | {{score_occupancy_leasing}} | {{note_occupancy_leasing}} |
| Retention and renewals | {{score_retention}} | {{note_retention}} |
| Collections and delinquency | {{score_collections}} | {{note_collections}} |
| Turn and make-ready | {{score_turn}} | {{note_turn}} |
| Maintenance and service | {{score_maintenance}} | {{note_maintenance}} |
| Controllable opex | {{score_opex}} | {{note_opex}} |
| Resident experience (qualitative) | {{score_resident_experience}} | {{note_resident_experience}} |
| Overall | {{score_overall}} | {{note_overall}} |

## Watchlist status

- Currently on watchlist: {{on_watchlist}}
- Watchlist drivers: {{watchlist_drivers}}
- Watchlist exit criteria: {{watchlist_exit_criteria}}

---

*Template status: starter. Scores and target bands load from the reference layer; any sample-tagged source is surfaced in the confidence banner.*
