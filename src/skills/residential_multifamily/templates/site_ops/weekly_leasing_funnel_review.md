---
template_slug: weekly_leasing_funnel_review
title: Weekly Leasing Funnel Review
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation]
  management_mode: [self_managed, third_party_managed]
  role: [property_manager, leasing_manager, regional_manager]
  output_type: kpi_review
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/derived/funnel_conversion_benchmarks__middle_market.csv
  - reference/normalized/market_rents__{market}_mf.csv
  - reference/normalized/concession_benchmarks__{market}_mf.csv
  - reference/derived/role_kpi_targets.csv
produced_by: roles/property_manager, workflows/lead_to_lease_funnel_review
---

# Weekly Leasing Funnel Review

**Property.** {{property_name}} ({{property_id}})
**Week ending.** {{week_ending_date}}

## Confidence banner

- Funnel benchmark as-of: {{funnel_benchmarks_as_of}} (status: {{funnel_benchmarks_status}})
- Market rents as-of: {{market_rents_as_of}} (status: {{market_rents_status}})
- Concession benchmarks as-of: {{concession_benchmarks_as_of}} (status: {{concession_benchmarks_status}})

## Funnel stages (T7 and T30)

| Stage | T7 count | T7 conversion | T30 count | T30 conversion | Target band |
|---|---|---|---|---|---|
| Leads | {{leads_t7}} | — | {{leads_t30}} | — | — |
| Contacted within SLA | {{contacted_t7}} | {{lead_response_t7}} | {{contacted_t30}} | {{lead_response_t30}} | {{target_lead_response_time}} |
| Tours scheduled | {{tours_sched_t7}} | — | {{tours_sched_t30}} | — | — |
| Tours completed | {{tours_comp_t7}} | {{tour_conversion_t7}} | {{tours_comp_t30}} | {{tour_conversion_t30}} | {{target_tour_conversion}} |
| Applications | {{apps_t7}} | {{application_conversion_t7}} | {{apps_t30}} | {{application_conversion_t30}} | {{target_application_conversion}} |
| Approved | {{approved_t7}} | {{approval_rate_t7}} | {{approved_t30}} | {{approval_rate_t30}} | {{target_approval_rate}} |
| Moved-in | {{mi_t7}} | {{move_in_conversion_t7}} | {{mi_t30}} | {{move_in_conversion_t30}} | {{target_move_in_conversion}} |

## Lead source mix (T30)

| Source | Leads | Apps | Move-ins | Cost (if paid source) |
|---|---|---|---|---|
| {{source_1}} | {{source_1_leads}} | {{source_1_apps}} | {{source_1_mi}} | {{source_1_cost}} |
| {{source_2}} | {{source_2_leads}} | {{source_2_apps}} | {{source_2_mi}} | {{source_2_cost}} |
| {{source_3}} | {{source_3_leads}} | {{source_3_apps}} | {{source_3_mi}} | {{source_3_cost}} |

## Concessions and pricing

- `concession_rate` (T30 new-lease): {{concession_rate_new_lease}} (target: {{target_concession_rate}})
- `market_to_lease_gap` (portfolio-weighted): {{market_to_lease_gap}}
- Units priced at or above market: {{units_at_or_above_market}}
- Units priced below market: {{units_below_market}}

## Screening flags

- Applications declined for documented policy reasons: {{declines_policy}}
- Applications routed for individualized assessment: {{individualized_assessment_count}}
- Fair-housing flags: {{fair_housing_flags}} (every flag routes approval matrix row 3)

## Diagnostics

- Top funnel friction: {{top_funnel_friction}}
- Mid-funnel friction: {{mid_funnel_friction}}
- Bottom funnel friction: {{bottom_funnel_friction}}

## Action items

| # | Action | Owner | Due | Approval gate |
|---|---|---|---|---|
| 1 | {{action_1}} | {{action_1_owner}} | {{action_1_due}} | {{action_1_gate}} |
| 2 | {{action_2}} | {{action_2_owner}} | {{action_2_due}} | {{action_2_gate}} |
| 3 | {{action_3}} | {{action_3_owner}} | {{action_3_due}} | {{action_3_gate}} |

---

*Template status: starter. All fair-housing flags route approval-required; no autonomous resident response.*
