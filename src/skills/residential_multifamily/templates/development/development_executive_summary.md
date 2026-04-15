---
template_slug: development_executive_summary
title: Development Executive Summary
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [development, construction]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [development_manager, asset_manager, portfolio_manager, coo_operations_leader, ceo_executive_leader]
  output_type: memo
legal_review_required: false
jurisdiction_sensitive: true
status: starter
references_used: []
produced_by: workflows/capital_project_intake_and_prioritization
---

# Development Executive Summary

**Project.** {{project_name}} ({{project_id}})
**Site address.** {{site_address}}
**Jurisdiction.** {{jurisdiction}}
**Period covered.** {{period_covered}}
**Prepared by.** {{prepared_by}}

## Confidence banner

- Schedule confidence: {{schedule_confidence}}
- Cost confidence: {{cost_confidence}}
- Permitting confidence: {{permitting_confidence}}
- Lease-up confidence: {{lease_up_confidence}}

## Headline

{{headline_statement}}

## Deal snapshot

- Program: {{unit_count}} units | {{nrsf_total}} NRSF | {{form_factor}} | {{stories}} stories
- Target segment: middle_market
- Land basis: {{land_basis_source}}
- Total development cost (TDC): {{tdc_source}}
- `dev_cost_per_unit`: {{dev_cost_per_unit}}  (source: {{dev_cost_per_unit_source}})
- `dev_cost_per_nrsf`: {{dev_cost_per_nrsf}}  (source: {{dev_cost_per_nrsf_source}})
- Target stabilized NOI: {{target_stabilized_noi_source}}
- Target YoC: {{target_yoc_source}}

## Schedule summary

- Groundbreaking (actual or forecast): {{ntp_date}}
- Substantial completion forecast: {{sc_forecast}}
- Stabilization forecast: {{stab_forecast}}
- `schedule_variance_days` vs. baseline: {{schedule_variance_days}}

## Cost summary

- Contract value (current): {{contract_value_current}}
- Approved COs to date: {{approved_cos}}
- Pending COs: {{pending_cos}}
- `cost_to_complete`: {{cost_to_complete}}
- Contingency used: {{contingency_used}}
- `contingency_remaining`: {{contingency_remaining}}
- `contingency_burn_rate` vs. % complete: {{contingency_burn_vs_pct}}

## Lease-up posture (if in construction / pre-TCO)

- Pre-lease campaign start: {{prelease_start}}
- `lease_up_pace_post_delivery` target: {{lease_up_pace_target}}
- Market rent assumption: {{market_rent_assumption}}  (source: {{market_rent_source}})

## Risks elevated to executive attention

{{executive_risks_narrative}}

## Decisions requested from executive

| # | Decision | Needed by | Approval path |
|---|---|---|---|
| 1 | {{exec_decision_1}} | {{exec_decision_1_by}} | {{exec_decision_1_path}} |
| 2 | {{exec_decision_2}} | {{exec_decision_2_by}} | {{exec_decision_2_path}} |

## Forward-look

- Next 30: {{next_30_outlook}}
- Next 90: {{next_90_outlook}}
- Key milestones in next 90: {{next_90_milestones}}

---

*Template status: starter.*
