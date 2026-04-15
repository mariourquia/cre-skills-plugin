---
template_slug: vendor_bid_leveling_template
title: Vendor Bid Leveling Template
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, renovation, construction, development]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [construction_manager, estimator_preconstruction_lead, property_manager, regional_manager, asset_manager]
  output_type: estimate
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/normalized/material_costs__{region}_residential.csv
  - reference/normalized/labor_rates__{market}_residential.csv
  - reference/normalized/capex_line_items__{market}_mf.csv
  - reference/normalized/vendor_rate_cards__{market}.csv
produced_by: workflows/bid_leveling_procurement_review
---

# Vendor Bid Leveling

**Project.** {{project_name}} ({{project_id}})
**Property.** {{property_name}} ({{property_id}})
**Bid leveling prepared by.** {{prepared_by}}
**Bid due date / open date.** {{bid_open_date}}

## Confidence banner

- Material costs reference as-of: {{material_costs_as_of}} (status: {{material_costs_status}})
- Labor rates reference as-of: {{labor_rates_as_of}} (status: {{labor_rates_status}})
- Vendor rate card as-of: {{vendor_rate_cards_as_of}} (status: {{vendor_rate_cards_status}})

## Scope baseline

- Scope reference: {{scope_reference_doc}}
- Plans / spec version: {{plans_spec_version}}
- Alternates requested: {{alternates_requested}}

## Bidders

| Bidder | Qualification status | Insurance verified | License verified | Prior performance |
|---|---|---|---|---|
| {{bidder_1}} | {{bidder_1_qual}} | {{bidder_1_ins}} | {{bidder_1_lic}} | {{bidder_1_perf}} |
| {{bidder_2}} | {{bidder_2_qual}} | {{bidder_2_ins}} | {{bidder_2_lic}} | {{bidder_2_perf}} |
| {{bidder_3}} | {{bidder_3_qual}} | {{bidder_3_ins}} | {{bidder_3_lic}} | {{bidder_3_perf}} |

## Leveled comparison — base scope

| CSI division / line | Unit | Qty | Ref unit cost | Bidder 1 | Bidder 2 | Bidder 3 | Notes |
|---|---|---|---|---|---|---|---|
| {{div_1}} | {{unit_1}} | {{qty_1}} | {{ref_unit_cost_1}} | {{b1_line_1}} | {{b2_line_1}} | {{b3_line_1}} | {{notes_1}} |
| {{div_2}} | {{unit_2}} | {{qty_2}} | {{ref_unit_cost_2}} | {{b1_line_2}} | {{b2_line_2}} | {{b3_line_2}} | {{notes_2}} |
| {{div_3}} | {{unit_3}} | {{qty_3}} | {{ref_unit_cost_3}} | {{b1_line_3}} | {{b2_line_3}} | {{b3_line_3}} | {{notes_3}} |

**Base scope totals.** B1: {{b1_base_total}} | B2: {{b2_base_total}} | B3: {{b3_base_total}}

## Scope gaps / exclusions

| Gap / exclusion | Bidder | Resolution (include as alternate, carry in contingency, re-bid) |
|---|---|---|
| {{gap_1}} | {{gap_1_bidder}} | {{gap_1_resolution}} |
| {{gap_2}} | {{gap_2_bidder}} | {{gap_2_resolution}} |

## Alternates

| Alternate | B1 | B2 | B3 | Recommend accept? |
|---|---|---|---|---|
| {{alt_1}} | {{b1_alt_1}} | {{b2_alt_1}} | {{b3_alt_1}} | {{alt_1_recommend}} |
| {{alt_2}} | {{b1_alt_2}} | {{b2_alt_2}} | {{b3_alt_2}} | {{alt_2_recommend}} |

## Qualitative factors

| Factor | Bidder 1 | Bidder 2 | Bidder 3 |
|---|---|---|---|
| Schedule confidence | {{b1_sched}} | {{b2_sched}} | {{b3_sched}} |
| Mobilization plan | {{b1_mob}} | {{b2_mob}} | {{b3_mob}} |
| Subs and key personnel | {{b1_subs}} | {{b2_subs}} | {{b3_subs}} |
| Warranty terms | {{b1_warr}} | {{b2_warr}} | {{b3_warr}} |
| Owner-preferred | {{b1_pref}} | {{b2_pref}} | {{b3_pref}} |

## Recommendation

- Recommended bidder: {{recommended_bidder}}
- Awarded scope total: {{awarded_total}}
- Contingency recommendation: {{recommended_contingency}}
- Award gate: {{award_gate}} (per approval matrix row 8 / 9 as applicable)

## Risks and watch-outs

{{risks_narrative}}

---

*Template status: starter.*
