---
template_slug: market_survey_summary
title: Market Survey Summary
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [property_manager, leasing_manager, regional_manager, asset_manager]
  output_type: memo
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/normalized/market_rents__{market}_mf.csv
  - reference/normalized/concession_benchmarks__{market}_mf.csv
  - reference/normalized/occupancy_benchmarks__{market}_mf.csv
produced_by: workflows/market_rent_refresh, workflows/rent_comp_intake
---

# Market Survey Summary

**Subject property.** {{subject_property_name}} ({{subject_property_id}})
**Market / submarket.** {{market}} / {{submarket}}
**Survey window.** {{survey_window_start}} to {{survey_window_end}}
**Prepared by.** {{prepared_by}}

## Confidence banner

- Market rents reference as-of: {{market_rents_as_of}} (status: {{market_rents_status}})
- Concession benchmark as-of: {{concession_benchmarks_as_of}} (status: {{concession_benchmarks_status}})
- Occupancy benchmark as-of: {{occupancy_benchmarks_as_of}} (status: {{occupancy_benchmarks_status}})

## Comp roster

| Comp | Year built / reno | Class | # units | 1BR eff rent | 2BR eff rent | Concessions posture |
|---|---|---|---|---|---|---|
| {{comp_1}} | {{comp_1_yb}} | {{comp_1_class}} | {{comp_1_units}} | {{comp_1_1br_eff}} | {{comp_1_2br_eff}} | {{comp_1_concession}} |
| {{comp_2}} | {{comp_2_yb}} | {{comp_2_class}} | {{comp_2_units}} | {{comp_2_1br_eff}} | {{comp_2_2br_eff}} | {{comp_2_concession}} |
| {{comp_3}} | {{comp_3_yb}} | {{comp_3_class}} | {{comp_3_units}} | {{comp_3_1br_eff}} | {{comp_3_2br_eff}} | {{comp_3_concession}} |
| {{comp_4}} | {{comp_4_yb}} | {{comp_4_class}} | {{comp_4_units}} | {{comp_4_1br_eff}} | {{comp_4_2br_eff}} | {{comp_4_concession}} |

## Subject-to-comp summary

| Unit type | Subject asking | Subject effective | Comp median effective | `market_to_lease_gap` implication |
|---|---|---|---|---|
| 1BR | {{subject_1br_ask}} | {{subject_1br_eff}} | {{comp_1br_median_eff}} | {{gap_1br}} |
| 2BR | {{subject_2br_ask}} | {{subject_2br_eff}} | {{comp_2br_median_eff}} | {{gap_2br}} |
| 3BR (if applicable) | {{subject_3br_ask}} | {{subject_3br_eff}} | {{comp_3br_median_eff}} | {{gap_3br}} |

## Concession landscape

- Most common concession form observed: {{concession_form}}
- Directional move vs. prior survey: {{concession_direction}}

## Supply / demand signals

- Deliveries within {{radius}}: {{deliveries_count}}
- Lease-up assets in radius: {{lease_up_assets}}
- Observed concessions at lease-up assets: {{lease_up_concessions}}
- Employer / demographic signals: {{employer_demo_signals}}

## Implications for subject

- Pricing: {{pricing_implication}}
- Concessions: {{concession_implication}}
- Renewals: {{renewal_implication}}
- Capex / amenity gaps: {{capex_amenity_gaps}}

## Recommended actions

{{recommended_actions}}

## Provenance

- Input intake forms processed: {{intake_forms_processed}}
- Records proposed for `reference/normalized/market_rents__{market}_mf.csv`: {{records_proposed}}
- Change log entries queued: {{change_log_entries_queued}}

---

*Template status: starter.*
