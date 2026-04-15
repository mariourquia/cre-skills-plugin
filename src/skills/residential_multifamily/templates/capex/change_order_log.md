---
template_slug: change_order_log
title: Change Order Log
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [construction, renovation, development]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [construction_manager, estimator_preconstruction_lead, asset_manager]
  output_type: checklist
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/normalized/approval_threshold_defaults.csv
  - reference/normalized/material_costs__{region}_residential.csv
  - reference/normalized/labor_rates__{market}_residential.csv
produced_by: workflows/change_order_review
---

# Change Order Log

**Project.** {{project_name}} ({{project_id}})
**Property.** {{property_name}} ({{property_id}})
**Contract value (base).** {{base_contract_value}}
**Log maintained by.** {{log_owner}}
**Last updated.** {{last_updated}}

## Confidence banner

- Approval thresholds as-of: {{approval_thresholds_as_of}} (status: {{approval_thresholds_status}})
- Material costs reference as-of: {{material_costs_as_of}} (status: {{material_costs_status}})

## Running totals

- Base contract: {{base_contract_value}}
- Approved CO dollars to date: {{approved_co_dollars}}
- Pending CO dollars: {{pending_co_dollars}}
- `change_orders_pct_of_contract`: {{co_pct_of_contract}}
- Contingency original: {{contingency_original}}
- `contingency_remaining`: {{contingency_remaining}}

## Log

| CO # | Date raised | Description | Category | Cost impact | Schedule impact (days) | Origin | Status | Approver required | Decision date | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| {{co_1}} | {{co_1_date}} | {{co_1_desc}} | {{co_1_cat}} | {{co_1_cost}} | {{co_1_days}} | {{co_1_origin}} | {{co_1_status}} | {{co_1_approver}} | {{co_1_decision_date}} | {{co_1_notes}} |
| {{co_2}} | {{co_2_date}} | {{co_2_desc}} | {{co_2_cat}} | {{co_2_cost}} | {{co_2_days}} | {{co_2_origin}} | {{co_2_status}} | {{co_2_approver}} | {{co_2_decision_date}} | {{co_2_notes}} |
| {{co_3}} | {{co_3_date}} | {{co_3_desc}} | {{co_3_cat}} | {{co_3_cost}} | {{co_3_days}} | {{co_3_origin}} | {{co_3_status}} | {{co_3_approver}} | {{co_3_decision_date}} | {{co_3_notes}} |

### Category legend

- `scope_add`: Owner-directed scope expansion.
- `scope_delete`: Owner-directed scope reduction.
- `design_clarification`: No scope change; cost or schedule impact from clarified design.
- `unforeseen_condition`: Latent condition discovered during work.
- `market_swing`: Material or labor price movement within allowed pricing mechanism.
- `schedule_accel`: Acceleration directed by owner or required by contract.
- `regulatory`: Code or jurisdictional requirement.

### Status legend

- `draft`: Raised but not priced.
- `priced`: Cost impact quantified; awaiting owner review.
- `pending_approval`: Routed for owner approval per approval matrix.
- `approved`: Approved and incorporated.
- `rejected`: Declined; original scope stands.
- `void`: Withdrawn.

## Approval matrix reference

- Minor CO tier (per approval matrix row 10): threshold token `threshold_co_minor`
- Major CO tier (per approval matrix row 11): threshold token `threshold_co_major`
- Both resolve from: {{approval_thresholds_source}}

## Watch-outs

{{watch_outs_narrative}}

---

*Template status: starter.*
