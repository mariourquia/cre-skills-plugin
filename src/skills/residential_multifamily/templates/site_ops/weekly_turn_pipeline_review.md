---
template_slug: weekly_turn_pipeline_review
title: Weekly Turn Pipeline Review
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation]
  management_mode: [self_managed, third_party_managed]
  role: [property_manager, regional_manager]
  output_type: operating_review
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/normalized/unit_turn_cost_library__middle_market.csv
  - reference/normalized/labor_rates__{market}_residential.csv
  - reference/derived/role_kpi_targets.csv
produced_by: roles/property_manager, workflows/unit_turn_make_ready
---

# Weekly Turn Pipeline Review

**Property.** {{property_name}} ({{property_id}})
**Week ending.** {{week_ending_date}}

## Confidence banner

- Turn cost library as-of: {{turn_cost_library_as_of}} (status: {{turn_cost_library_status}})
- Labor rates reference as-of: {{labor_rates_as_of}} (status: {{labor_rates_status}})

## Headline

- `make_ready_days` median (T30): {{make_ready_days_median_t30}} (target: {{target_make_ready_days}})
- Units in active turn: {{units_in_turn}}
- Units ready and unrented: {{units_ready_unrented}}
- `average_days_vacant` (T30): {{average_days_vacant_t30}} (target: {{target_average_days_vacant}})

## Stage table

| Unit | Stage | Days in stage | Target | Root cause if aged | Scope (classic / value_add) | Est. cost |
|---|---|---|---|---|---|---|
| {{unit_1}} | {{stage_1}} | {{days_in_stage_1}} | {{target_stage_1}} | {{root_cause_1}} | {{scope_1}} | {{est_cost_1}} |
| {{unit_2}} | {{stage_2}} | {{days_in_stage_2}} | {{target_stage_2}} | {{root_cause_2}} | {{scope_2}} | {{est_cost_2}} |
| {{unit_3}} | {{stage_3}} | {{days_in_stage_3}} | {{target_stage_3}} | {{root_cause_3}} | {{scope_3}} | {{est_cost_3}} |

## Vendor performance

| Vendor | Units in flight | On-time rate | Rework count | Scorecard notes |
|---|---|---|---|---|
| {{vendor_1}} | {{vendor_1_in_flight}} | {{vendor_1_on_time}} | {{vendor_1_rework}} | {{vendor_1_notes}} |
| {{vendor_2}} | {{vendor_2_in_flight}} | {{vendor_2_on_time}} | {{vendor_2_rework}} | {{vendor_2_notes}} |

## Bottlenecks

- Flooring / material delays: {{flooring_delays}}
- Appliance / cabinet delays: {{appliance_delays}}
- Inspection / punch backlog: {{inspection_backlog}}
- Vendor capacity constraints: {{vendor_capacity_issues}}

## Action items

| # | Action | Owner | Due | Approval gate |
|---|---|---|---|---|
| 1 | {{action_1}} | {{action_1_owner}} | {{action_1_due}} | {{action_1_gate}} |
| 2 | {{action_2}} | {{action_2_owner}} | {{action_2_due}} | {{action_2_gate}} |
| 3 | {{action_3}} | {{action_3_owner}} | {{action_3_due}} | {{action_3_gate}} |

---

*Template status: starter.*
