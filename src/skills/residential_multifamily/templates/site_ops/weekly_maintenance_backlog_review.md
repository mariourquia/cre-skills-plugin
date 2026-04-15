---
template_slug: weekly_maintenance_backlog_review
title: Weekly Maintenance Backlog Review
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation]
  management_mode: [self_managed, third_party_managed]
  role: [property_manager, maintenance_supervisor, regional_manager]
  output_type: operating_review
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/derived/role_kpi_targets.csv
  - reference/normalized/staffing_ratios__middle_market.csv
  - reference/normalized/vendor_rate_cards__{market}.csv
produced_by: roles/property_manager, workflows/work_order_triage
---

# Weekly Maintenance Backlog Review

**Property.** {{property_name}} ({{property_id}})
**Week ending.** {{week_ending_date}}

## Confidence banner

- KPI target source as-of: {{role_kpi_targets_as_of}} (status: {{role_kpi_targets_status}})
- Staffing ratios as-of: {{staffing_ratios_as_of}} (status: {{staffing_ratios_status}})
- Vendor rate card as-of: {{vendor_rate_cards_as_of}} (status: {{vendor_rate_cards_status}})

## Headline

- `open_work_orders`: {{open_work_orders}} (prior: {{open_work_orders_prior}}, target band: {{target_open_work_orders}})
- `repeat_work_order_rate` (T30): {{repeat_work_order_rate}} (target: {{target_repeat_work_order_rate}})

## Priority breakdown

| Priority | Open | Acknowledged | In progress | Aged past SLA | SLA band |
|---|---|---|---|---|---|
| P1 (life safety) | {{p1_open}} | {{p1_ack}} | {{p1_in_progress}} | {{p1_aged}} | {{sla_p1}} |
| P2 (urgent) | {{p2_open}} | {{p2_ack}} | {{p2_in_progress}} | {{p2_aged}} | {{sla_p2}} |
| P3 (standard) | {{p3_open}} | {{p3_ack}} | {{p3_in_progress}} | {{p3_aged}} | {{sla_p3}} |
| P4 (planned) | {{p4_open}} | {{p4_ack}} | {{p4_in_progress}} | {{p4_aged}} | {{sla_p4}} |

## Repeat / rework

- Open repeat work orders (same unit, same symptom within 30 days): {{repeat_wo_count}}
- Unit clusters: {{repeat_wo_unit_clusters}}
- Vendor clusters: {{repeat_wo_vendor_clusters}}

## PM plan vs. actual

- Tasks scheduled this week: {{pm_scheduled}}
- Completed on schedule: {{pm_completed_on_schedule}}
- Deferred (with reason): {{pm_deferred}}

## Parts / vendor constraints

- Parts on order (top 5): {{parts_on_order_top_5}}
- Vendor dispatches scheduled next 7d: {{vendor_dispatches_next_7}}
- License / insurance gaps blocking dispatch: {{license_gaps}}

## Staffing

- Maintenance staff on duty: {{maint_staff_on_duty}}
- Open positions: {{maint_open_positions}}
- Overtime hours T7: {{maint_ot_t7}}

## Action items

| # | Action | Owner | Due | Approval gate |
|---|---|---|---|---|
| 1 | {{action_1}} | {{action_1_owner}} | {{action_1_due}} | {{action_1_gate}} |
| 2 | {{action_2}} | {{action_2_owner}} | {{action_2_due}} | {{action_2_gate}} |
| 3 | {{action_3}} | {{action_3_owner}} | {{action_3_due}} | {{action_3_gate}} |

---

*Template status: starter.*
