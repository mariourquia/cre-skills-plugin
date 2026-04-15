---
template_slug: owner_approval_routing_checklist
title: Owner Approval Routing Checklist
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation, construction, development]
  management_mode: [third_party_managed, owner_oversight]
  role: [third_party_manager_oversight_lead, asset_manager, portfolio_manager]
  output_type: checklist
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/normalized/approval_threshold_defaults.csv
produced_by: workflows/owner_approval_routing
---

# Owner Approval Routing Checklist

**Property.** {{property_name}} ({{property_id}})
**Routing request opened by.** {{opened_by}}
**Request date.** {{request_date}}
**Approval-request ID.** {{approval_request_id}}

## Confidence banner

- Approval thresholds as-of: {{approval_thresholds_as_of}} (status: {{approval_thresholds_status}})
- Org overlay approver map version: {{org_overlay_version}}

## Classification

- Request category: {{request_category}}  (e.g., `vendor_award`, `capex_over_threshold`, `lease_deviation`, `concession_over_policy`, `non_standard_payment_plan`, `final_lender_submission`)
- Approval-matrix row: {{approval_matrix_row}}
- Decision severity: {{decision_severity}}  (recommendation | action_requires_approval)
- Material dollar amount: {{dollar_amount}}
- Tier mapped: {{tier_mapped}}  (tier_1 | tier_2 | tier_3 — resolved from threshold reference)

## Supporting documents

- [ ] Memo or request document attached: {{memo_ref}}
- [ ] Reference citations inline (unit cost, market rent, etc.): {{reference_citations}}
- [ ] Alternatives considered documented: {{alternatives_ref}}
- [ ] Risk register / watch-outs: {{risk_register_ref}}
- [ ] PM / AM / regional pre-endorsement: {{preendorsement_status}}

## Approver chain (resolved)

| # | Role | Name | Action required | SLA |
|---|---|---|---|---|
| 1 | {{approver_1_role}} | {{approver_1_name}} | {{approver_1_action}} | {{approver_1_sla}} |
| 2 | {{approver_2_role}} | {{approver_2_name}} | {{approver_2_action}} | {{approver_2_sla}} |
| 3 | {{approver_3_role}} | {{approver_3_name}} | {{approver_3_action}} | {{approver_3_sla}} |

## Status

- Current step: {{current_step}}
- Time in current step: {{time_in_step}}
- `approval_response_time_tpm` for this request: {{approval_response_time}}

## Outcome

- Decision: {{decision}}  (approved | approved_with_conditions | denied | withdrawn)
- Conditions (if any): {{conditions}}
- Effective date: {{effective_date}}
- Audit-log entry reference: {{audit_log_entry}}

---

*Template status: starter.*
