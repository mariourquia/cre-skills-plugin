---
template_slug: daily_site_priority_list
title: Daily Site Priority List
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation]
  management_mode: [self_managed, third_party_managed]
  role: [property_manager, assistant_property_manager]
  output_type: checklist
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/derived/role_kpi_targets.csv
produced_by: roles/property_manager
---

# Daily Site Priority List

**Property.** {{property_name}} ({{property_id}})
**Date.** {{date}}
**Prepared by.** {{prepared_by}}

## Overnight / safety

- P1 work orders acknowledged and owner-assigned: {{p1_ack_status}}
- Life-safety incidents or alarms: {{life_safety_incidents}}
- After-hours resident issues logged: {{after_hours_issues}}

## Funnel (last 24h)

- New leads: {{leads_24h}} | First-touch SLA misses: {{first_touch_sla_misses}}
- Tours booked today: {{tours_today}} | Tours completed yesterday: {{tours_yesterday}}
- Applications received: {{apps_received_24h}} | Screening queue depth: {{screening_queue}}

## Move-ins / move-outs

- Move-ins today: {{move_ins_today}}
- Move-outs today: {{move_outs_today}}
- Move-in readiness gaps (units not ready for an in-flight move-in): {{move_in_readiness_gaps}}

## Collections

- Auto-pay failures overnight: {{autopay_failures}}
- Residents crossing aging buckets today: {{aging_bucket_crossings}}
- Payment plans expiring today: {{payment_plans_expiring}}

## Turn

- Units moving stage today (to in-turn / punchlist / ready): {{turn_stage_transitions}}
- Vendor schedule for today: {{turn_vendor_schedule}}

## Walk

- Curb appeal check: {{curb_appeal_status}}
- Amenity / common area check: {{amenity_status}}
- Trash / landscaping: {{trash_landscaping_status}}

## Top 3 priorities for today

1. {{priority_1}} — owner: {{priority_1_owner}} — gate: {{priority_1_gate}}
2. {{priority_2}} — owner: {{priority_2_owner}} — gate: {{priority_2_gate}}
3. {{priority_3}} — owner: {{priority_3_owner}} — gate: {{priority_3_gate}}

---

*Template status: starter.*
