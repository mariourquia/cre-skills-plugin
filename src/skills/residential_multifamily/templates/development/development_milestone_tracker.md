---
template_slug: development_milestone_tracker
title: Development Milestone Tracker
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [development, construction]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [development_manager, construction_manager, asset_manager]
  output_type: checklist
legal_review_required: false
jurisdiction_sensitive: true
status: starter
references_used: []
produced_by: workflows/capital_project_intake_and_prioritization, workflows/schedule_risk_review
---

# Development Milestone Tracker

**Project.** {{project_name}} ({{project_id}})
**Site address.** {{site_address}}
**Jurisdiction.** {{jurisdiction}}
**Tracker owner.** {{tracker_owner}}
**Last updated.** {{last_updated}}

## Confidence note

- Schedule confidence: {{schedule_confidence}}  (low | medium | high | verified)
- Permitting jurisdiction risk: {{permitting_risk}}

## Milestones

| # | Milestone | Planned date | Forecast date | Actual date | Status | Blocking items | Owner |
|---|---|---|---|---|---|---|---|
| 1 | Site control (PSA executed) | {{site_control_planned}} | {{site_control_forecast}} | {{site_control_actual}} | {{site_control_status}} | {{site_control_blockers}} | {{site_control_owner}} |
| 2 | Feasibility complete | {{feasibility_planned}} | {{feasibility_forecast}} | {{feasibility_actual}} | {{feasibility_status}} | {{feasibility_blockers}} | {{feasibility_owner}} |
| 3 | Zoning / entitlement approved | {{entitlement_planned}} | {{entitlement_forecast}} | {{entitlement_actual}} | {{entitlement_status}} | {{entitlement_blockers}} | {{entitlement_owner}} |
| 4 | Design development complete | {{dd_planned}} | {{dd_forecast}} | {{dd_actual}} | {{dd_status}} | {{dd_blockers}} | {{dd_owner}} |
| 5 | Construction documents complete | {{cd_planned}} | {{cd_forecast}} | {{cd_actual}} | {{cd_status}} | {{cd_blockers}} | {{cd_owner}} |
| 6 | GMP / hard bid close | {{gmp_planned}} | {{gmp_forecast}} | {{gmp_actual}} | {{gmp_status}} | {{gmp_blockers}} | {{gmp_owner}} |
| 7 | Permit issued | {{permit_planned}} | {{permit_forecast}} | {{permit_actual}} | {{permit_status}} | {{permit_blockers}} | {{permit_owner}} |
| 8 | Equity closing | {{equity_planned}} | {{equity_forecast}} | {{equity_actual}} | {{equity_status}} | {{equity_blockers}} | {{equity_owner}} |
| 9 | Construction loan closing | {{loan_planned}} | {{loan_forecast}} | {{loan_actual}} | {{loan_status}} | {{loan_blockers}} | {{loan_owner}} |
| 10 | Groundbreaking / NTP | {{ntp_planned}} | {{ntp_forecast}} | {{ntp_actual}} | {{ntp_status}} | {{ntp_blockers}} | {{ntp_owner}} |
| 11 | Topping out | {{topping_planned}} | {{topping_forecast}} | {{topping_actual}} | {{topping_status}} | {{topping_blockers}} | {{topping_owner}} |
| 12 | Temporary CO (TCO) / first delivery | {{tco_planned}} | {{tco_forecast}} | {{tco_actual}} | {{tco_status}} | {{tco_blockers}} | {{tco_owner}} |
| 13 | Substantial completion | {{sc_planned}} | {{sc_forecast}} | {{sc_actual}} | {{sc_status}} | {{sc_blockers}} | {{sc_owner}} |
| 14 | Final CO | {{co_planned}} | {{co_forecast}} | {{co_actual}} | {{co_status}} | {{co_blockers}} | {{co_owner}} |
| 15 | Stabilization | {{stab_planned}} | {{stab_forecast}} | {{stab_actual}} | {{stab_status}} | {{stab_blockers}} | {{stab_owner}} |

## Slippage summary

- `milestone_slippage_rate` (cumulative): {{milestone_slippage_rate}}
- Largest slippage driver: {{largest_slippage_driver}}
- Impact on stabilization: {{stabilization_impact}}

## Critical path

{{critical_path_narrative}}

## Decisions due

| # | Decision | Due | Approval path |
|---|---|---|---|
| 1 | {{decision_1}} | {{decision_1_due}} | {{decision_1_path}} |
| 2 | {{decision_2}} | {{decision_2_due}} | {{decision_2_path}} |

---

*Template status: starter. Jurisdiction-sensitive: entitlement, permit, and CO rows depend on local process.*
