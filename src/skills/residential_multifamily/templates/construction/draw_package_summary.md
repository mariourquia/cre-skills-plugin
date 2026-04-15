---
template_slug: draw_package_summary
title: Draw Package Summary
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [construction, renovation, development]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [construction_manager, development_manager, asset_manager, reporting_finance_ops_lead]
  output_type: memo
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/normalized/approval_threshold_defaults.csv
produced_by: workflows/draw_package_review
---

# Draw Package Summary

**Project.** {{project_name}} ({{project_id}})
**Property.** {{property_name}} ({{property_id}})
**Draw number.** {{draw_number}}
**Draw period.** {{draw_period_start}} to {{draw_period_end}}
**Prepared by.** {{prepared_by}}

## Confidence banner

- Approval thresholds as-of: {{approval_thresholds_as_of}} (status: {{approval_thresholds_status}})
- Schedule-of-values version: {{sov_version}}  (as-of: {{sov_as_of}})

## Draw totals

- Period draw amount: {{period_draw_amount}}
- Cumulative draws to date: {{cumulative_draws}}
- Contract + approved COs total: {{contract_plus_cos}}
- % complete (cost-loaded schedule): {{pct_complete_cost}}
- % complete (physical estimate): {{pct_complete_physical}}
- `draw_cycle_time` (request-to-funding, prior draw): {{draw_cycle_time}}

## Line-item summary (CSI divisions)

| Division | Scheduled value | Prior billed | This period billed | Stored materials | Total completed | % complete | Retainage |
|---|---|---|---|---|---|---|---|
| {{div_1}} | {{div_1_sv}} | {{div_1_prior}} | {{div_1_this}} | {{div_1_stored}} | {{div_1_total}} | {{div_1_pct}} | {{div_1_retain}} |
| {{div_2}} | {{div_2_sv}} | {{div_2_prior}} | {{div_2_this}} | {{div_2_stored}} | {{div_2_total}} | {{div_2_pct}} | {{div_2_retain}} |
| {{div_3}} | {{div_3_sv}} | {{div_3_prior}} | {{div_3_this}} | {{div_3_stored}} | {{div_3_total}} | {{div_3_pct}} | {{div_3_retain}} |

## Retainage

- Retainage withheld: {{retainage_withheld}}
- Retainage release requested this draw: {{retainage_release_requested}}
- Retainage release approval gate: {{retainage_release_gate}}

## Lien waivers / compliance

- Conditional waivers collected (GC + subs): {{conditional_waivers_collected}}
- Unconditional waivers collected (prior period): {{unconditional_waivers_collected}}
- Missing waivers: {{missing_waivers}}
- Stored materials documentation: {{stored_materials_docs}}

## Change orders included

{{cos_included_summary}}

## Issues / holds

{{issues_holds_narrative}}

## Approval path

- Internal approval tier: {{internal_tier}}  (per approval matrix row 6 / 7 as applicable)
- Lender approval required: {{lender_approval_required}}
- Required approvers: {{required_approvers}}

## Forward-look

- Next draw anticipated amount: {{next_draw_estimate}}
- Milestone / completion forecast impact: {{milestone_impact}}

---

*Template status: starter.*
