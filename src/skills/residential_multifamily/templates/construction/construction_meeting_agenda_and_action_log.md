---
template_slug: construction_meeting_agenda_and_action_log
title: Construction Meeting Agenda and Action Log
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [construction, renovation, development]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [construction_manager, estimator_preconstruction_lead, development_manager, asset_manager]
  output_type: checklist
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used: []
produced_by: workflows/construction_meeting_prep
---

# Construction Meeting Agenda and Action Log

**Project.** {{project_name}} ({{project_id}})
**Property.** {{property_name}} ({{property_id}})
**Meeting type.** {{meeting_type}}  (weekly OAC | pre-construction | milestone review | other)
**Date / time.** {{meeting_datetime}}
**Chair.** {{meeting_chair}}
**Attendees.** {{attendees}}

## Safety moment

{{safety_moment}}

## Schedule

- Planned substantial completion: {{planned_sc_date}}
- Current forecast substantial completion: {{forecast_sc_date}}
- `schedule_variance_days` vs. baseline: {{schedule_variance_days}}
- Critical path items at risk: {{critical_path_risks}}

## Milestones this period

| Milestone | Planned | Actual / forecast | Status | Notes |
|---|---|---|---|---|
| {{milestone_1}} | {{milestone_1_planned}} | {{milestone_1_actual}} | {{milestone_1_status}} | {{milestone_1_notes}} |
| {{milestone_2}} | {{milestone_2_planned}} | {{milestone_2_actual}} | {{milestone_2_status}} | {{milestone_2_notes}} |
| {{milestone_3}} | {{milestone_3_planned}} | {{milestone_3_actual}} | {{milestone_3_status}} | {{milestone_3_notes}} |

## Cost / budget

- Contract value (current): {{contract_value_current}}
- Approved COs to date: {{approved_cos}}
- Pending COs: {{pending_cos}}
- `cost_to_complete`: {{cost_to_complete}}
- `contingency_remaining`: {{contingency_remaining}}
- Buyout variance to date: {{trade_buyout_variance}}

## RFIs

- Open RFIs: {{open_rfis}}
- Aged RFIs (past SLA): {{aged_rfis}}
- Top RFIs blocking progress: {{top_rfis}}

## Submittals

- Open submittals: {{open_submittals}}
- Aged submittals: {{aged_submittals}}
- Top submittals blocking procurement: {{top_submittals}}

## Change orders

- New CO proposals this period: {{new_co_proposals}}
- Pending owner approval: {{pending_owner_co}}
- Disputed items: {{disputed_items}}

## Inspections / quality

- Inspections completed this period: {{inspections_completed}}
- Deficiencies open: {{deficiencies_open}}
- Quality concerns logged: {{quality_concerns}}

## Safety / incidents

- Incidents in period: {{incidents_in_period}}
- Near misses logged: {{near_misses}}
- Corrective actions open: {{safety_corrective_actions}}

## Action log

| # | Action | Owner | Due | Status | Approval gate |
|---|---|---|---|---|---|
| 1 | {{action_1}} | {{action_1_owner}} | {{action_1_due}} | {{action_1_status}} | {{action_1_gate}} |
| 2 | {{action_2}} | {{action_2_owner}} | {{action_2_due}} | {{action_2_status}} | {{action_2_gate}} |
| 3 | {{action_3}} | {{action_3_owner}} | {{action_3_due}} | {{action_3_status}} | {{action_3_gate}} |
| 4 | {{action_4}} | {{action_4_owner}} | {{action_4_due}} | {{action_4_status}} | {{action_4_gate}} |

## Escalations

{{escalations_narrative}}

## Next meeting

- Date: {{next_meeting_date}}
- Focus: {{next_meeting_focus}}

---

*Template status: starter.*
