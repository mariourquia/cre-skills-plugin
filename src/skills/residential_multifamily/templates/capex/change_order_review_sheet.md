---
template_slug: change_order_review_sheet
title: Change Order Review Sheet
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [construction, renovation, development]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [construction_manager, estimator_preconstruction_lead, asset_manager]
  output_type: memo
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/normalized/approval_threshold_defaults.csv
  - reference/normalized/material_costs__{region}_residential.csv
  - reference/normalized/labor_rates__{market}_residential.csv
produced_by: workflows/change_order_review
---

# Change Order Review Sheet

**Project.** {{project_name}} ({{project_id}})
**CO number.** {{co_number}}
**CO title.** {{co_title}}
**Raised by.** {{raised_by}}
**Date raised.** {{date_raised}}

## Confidence banner

- Material costs as-of: {{material_costs_as_of}} (status: {{material_costs_status}})
- Labor rates as-of: {{labor_rates_as_of}} (status: {{labor_rates_status}})
- Approval thresholds as-of: {{approval_thresholds_as_of}} (status: {{approval_thresholds_status}})

## Description and category

- Description: {{co_description}}
- Category: {{co_category}}  (scope_add | scope_delete | design_clarification | unforeseen_condition | market_swing | schedule_accel | regulatory)
- Origin: {{co_origin}}  (owner | design | GC | subcontractor | inspector | resident)

## Scope details

{{scope_detail_narrative}}

## Pricing breakdown

| Line | Unit | Qty | Ref unit cost | GC priced | Variance to ref | Notes |
|---|---|---|---|---|---|---|
| {{line_1}} | {{unit_1}} | {{qty_1}} | {{ref_unit_cost_1}} | {{gc_price_1}} | {{var_1}} | {{notes_1}} |
| {{line_2}} | {{unit_2}} | {{qty_2}} | {{ref_unit_cost_2}} | {{gc_price_2}} | {{var_2}} | {{notes_2}} |
| {{line_3}} | {{unit_3}} | {{qty_3}} | {{ref_unit_cost_3}} | {{gc_price_3}} | {{var_3}} | {{notes_3}} |

- GC overhead / profit applied: {{gc_op_applied}}
- GC bond / insurance applied: {{bond_ins_applied}}

**Total cost impact.** {{total_cost_impact}}
**Schedule impact (days).** {{schedule_impact_days}}

## Trade-buyout context (if applicable)

- `trade_buyout_variance` to date for this trade: {{trade_buyout_variance}}
- Buyout reference source: {{buyout_source}}

## Options

| Option | Cost | Schedule | Risk | Approval gate |
|---|---|---|---|---|
| Absorb in contingency | {{opt_absorb_cost}} | {{opt_absorb_schedule}} | {{opt_absorb_risk}} | {{opt_absorb_gate}} |
| Approve change order | {{opt_co_cost}} | {{opt_co_schedule}} | {{opt_co_risk}} | {{opt_co_gate}} |
| Rebid scope | {{opt_rebid_cost}} | {{opt_rebid_schedule}} | {{opt_rebid_risk}} | {{opt_rebid_gate}} |
| Descope / reject | {{opt_reject_cost}} | {{opt_reject_schedule}} | {{opt_reject_risk}} | {{opt_reject_gate}} |

## Recommendation

{{recommendation_narrative}}

## Approval path

- Threshold tier: {{threshold_tier}} (minor | major — per approval matrix rows 10/11)
- Required approvers: {{required_approvers}}
- Gate citations: {{approval_matrix_rows}}

## Confidence

{{confidence_note}}

---

*Template status: starter. Any CO crossing the major tier routes automatically to executive-level approval per approval matrix.*
