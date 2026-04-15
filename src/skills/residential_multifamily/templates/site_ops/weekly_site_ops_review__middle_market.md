---
template_slug: weekly_site_ops_review__middle_market
title: Weekly Site Operations Review (Middle-Market)
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [stabilized, renovation, lease_up]
  management_mode: [self_managed, third_party_managed]
  role: [property_manager]
  output_type: operating_review
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/derived/role_kpi_targets.csv
  - reference/normalized/market_rents__{market}_mf.csv
  - reference/normalized/concession_benchmarks__{market}_mf.csv
  - reference/normalized/collections_benchmarks__{region}_mf.csv
produced_by: roles/property_manager
---

# Weekly Site Operations Review

**Property.** {{property_name}} ({{property_id}}) — {{market}} / {{submarket}}
**Week ending.** {{week_ending_date}}
**Prepared by.** {{prepared_by}} ({{role}})
**Segment / form / stage / mode.** middle_market / {{form_factor}} / {{lifecycle_stage}} / {{management_mode}}

## Confidence banner

- Rent reference as-of: {{market_rents_as_of}} (status: {{market_rents_status}})
- Concession reference as-of: {{concession_benchmarks_as_of}} (status: {{concession_benchmarks_status}})
- Collections benchmark as-of: {{collections_benchmarks_as_of}} (status: {{collections_benchmarks_status}})
- KPI target source: {{role_kpi_targets_source}} (status: {{role_kpi_targets_status}})

## Leasing funnel (T7)

| Metric | This week | Prior week | Target band (middle_market) | Delta vs. target |
|---|---|---|---|---|
| `lead_response_time` (median) | {{lead_response_time_median}} | {{lead_response_time_median_prior}} | {{target_lead_response_time}} | {{delta_lead_response_time}} |
| `tour_conversion` | {{tour_conversion}} | {{tour_conversion_prior}} | {{target_tour_conversion}} | {{delta_tour_conversion}} |
| `application_conversion` | {{application_conversion}} | {{application_conversion_prior}} | {{target_application_conversion}} | {{delta_application_conversion}} |
| `approval_rate` | {{approval_rate}} | {{approval_rate_prior}} | {{target_approval_rate}} | {{delta_approval_rate}} |
| `move_in_conversion` | {{move_in_conversion}} | {{move_in_conversion_prior}} | {{target_move_in_conversion}} | {{delta_move_in_conversion}} |

**Commentary.** {{funnel_commentary}}

## Occupancy and exposure

| Metric | Value | Target band | Notes |
|---|---|---|---|
| `physical_occupancy` | {{physical_occupancy}} | {{target_physical_occupancy}} | {{note_physical_occupancy}} |
| `leased_occupancy` | {{leased_occupancy}} | {{target_leased_occupancy}} | {{note_leased_occupancy}} |
| `preleased_occupancy` | {{preleased_occupancy}} | {{target_preleased_occupancy}} | {{note_preleased_occupancy}} |
| `notice_exposure` | {{notice_exposure}} | {{target_notice_exposure}} | {{note_notice_exposure}} |
| `market_to_lease_gap` | {{market_to_lease_gap}} | {{target_market_to_lease_gap}} | {{note_market_to_lease_gap}} |

## Renewals

- `renewal_offer_rate`: {{renewal_offer_rate}} (target: {{target_renewal_offer_rate}})
- Outstanding offers: {{offers_outstanding}} of {{offers_in_window}}
- Gaps (expiring leases without offer): {{renewal_offer_gaps}}

## Delinquency

- `delinquency_rate_30plus`: {{delinquency_rate_30plus}} (prior: {{delinquency_rate_30plus_prior}}, target: {{target_delinquency_rate_30plus}})
- Movement: {{delinquency_bucket_movement_summary}}
- Open payment plans: {{open_payment_plans}}
- Items flagged for escalation: {{delinquency_escalations}}

## Turn pipeline

| Stage | Count | Median days in stage | Target | Aged beyond target |
|---|---|---|---|---|
| Noticed — not yet vacated | {{turn_stage_notice}} | {{turn_stage_notice_median}} | {{turn_stage_notice_target}} | {{turn_stage_notice_aged}} |
| Vacated — pre-scope | {{turn_stage_prescope}} | {{turn_stage_prescope_median}} | {{turn_stage_prescope_target}} | {{turn_stage_prescope_aged}} |
| In turn | {{turn_stage_inturn}} | {{turn_stage_inturn_median}} | {{turn_stage_inturn_target}} | {{turn_stage_inturn_aged}} |
| Punchlist / QC | {{turn_stage_punchlist}} | {{turn_stage_punchlist_median}} | {{turn_stage_punchlist_target}} | {{turn_stage_punchlist_aged}} |
| Ready | {{turn_stage_ready}} | {{turn_stage_ready_median}} | {{turn_stage_ready_target}} | {{turn_stage_ready_aged}} |

**Headline.** `make_ready_days` median {{make_ready_days_median}} (target: {{target_make_ready_days}}).

## Maintenance backlog

- `open_work_orders`: {{open_work_orders}} (prior: {{open_work_orders_prior}})
- P1 open: {{p1_open}}  |  P1 aged past SLA: {{p1_aged_past_sla}}
- P2 aging beyond target: {{p2_aged_past_sla}}
- `repeat_work_order_rate`: {{repeat_work_order_rate}} (target: {{target_repeat_work_order_rate}})

## Staffing and vendor flags

- Open site staffing positions: {{open_staffing_positions}}
- Vendor incidents this week: {{vendor_incidents}}
- Preferred-vendor coverage gaps: {{vendor_coverage_gaps}}

## Action items

| # | Action | Owner | Due | Approval gate | Confidence |
|---|---|---|---|---|---|
| 1 | {{action_1}} | {{action_1_owner}} | {{action_1_due}} | {{action_1_gate}} | {{action_1_confidence}} |
| 2 | {{action_2}} | {{action_2_owner}} | {{action_2_due}} | {{action_2_gate}} | {{action_2_confidence}} |
| 3 | {{action_3}} | {{action_3_owner}} | {{action_3_due}} | {{action_3_gate}} | {{action_3_confidence}} |

## Approval requests opened this week

{{approval_requests_opened}}

## Escalations routed

{{escalations_routed}}

---

*Template status: starter. Numeric bands load from reference layer; any sample-tagged references are surfaced in the confidence banner above.*
