---
template_slug: capex_request_memo
title: Capex Request Memo
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [property_manager, regional_manager, asset_manager, construction_manager]
  output_type: memo
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/normalized/capex_line_items__{market}_mf.csv
  - reference/normalized/material_costs__{region}_residential.csv
  - reference/normalized/labor_rates__{market}_residential.csv
  - reference/normalized/approval_threshold_defaults.csv
produced_by: workflows/capital_project_intake_and_prioritization
---

# Capex Request Memo

**Property.** {{property_name}} ({{property_id}}) — {{market}} / {{submarket}}
**Requested by.** {{requested_by}} ({{role}})
**Request date.** {{request_date}}
**Project.** {{project_name}}

## Confidence banner

- Capex line-item library as-of: {{capex_line_items_as_of}} (status: {{capex_line_items_status}})
- Material costs as-of: {{material_costs_as_of}} (status: {{material_costs_status}})
- Labor rates as-of: {{labor_rates_as_of}} (status: {{labor_rates_status}})
- Approval thresholds as-of: {{approval_thresholds_as_of}} (status: {{approval_thresholds_status}})

## Classification

- Category: {{capex_category}}  (life_safety | deferred_maintenance | replacement | value_add | other)
- Priority: {{priority}}  (urgent | this_year | next_12 | opportunistic)
- Life-safety: {{life_safety_flag}}  (yes | no)

## Scope

{{scope_narrative}}

## Quantitative summary

| Line | Quantity | Unit cost (ref) | Extended | Contingency | Total |
|---|---|---|---|---|---|
| {{line_1}} | {{qty_1}} | {{unit_cost_1}} | {{ext_1}} | {{cont_1}} | {{total_1}} |
| {{line_2}} | {{qty_2}} | {{unit_cost_2}} | {{ext_2}} | {{cont_2}} | {{total_2}} |
| {{line_3}} | {{qty_3}} | {{unit_cost_3}} | {{ext_3}} | {{cont_3}} | {{total_3}} |

**Total ask.** {{total_ask}}
**Contingency included.** {{contingency_amount}} ({{contingency_pct}})

## Justification

- Return / value lever: {{value_lever_narrative}}
- If value-add, `renovation_yield_on_cost` expectation (with reference): {{yoc_expectation}}
- If deferred-maintenance, downstream risk if deferred: {{downstream_risk}}
- If life-safety, citation and deadline: {{life_safety_citation}}

## Alternatives considered

- {{alternative_1}}
- {{alternative_2}}

## Schedule

- Target start: {{target_start}}
- Target completion: {{target_completion}}
- Resident-impact plan: {{resident_impact_plan}}

## Procurement plan

- Bidders: {{bidders_planned}}
- Bid leveling planned: {{bid_leveling_planned}}  (reference: `vendor_bid_leveling_template.md`)
- Contract type: {{contract_type}}  (lump_sum | cost_plus | gmp | unit_price)

## Approval path

- Threshold tier: {{threshold_tier}}  (per approval matrix)
- Required approvers: {{required_approvers}}
- Gate citations: {{approval_matrix_rows}}

## Funding source

- Reserves / operating / capital call: {{funding_source}}
- Impact on DSCR / debt yield: {{debt_impact}}

---

*Template status: starter. Every dollar resolves to a reference layer citation; no hardcoded unit costs live in this memo template.*
