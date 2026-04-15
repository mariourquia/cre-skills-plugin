---
template_slug: rent_comp_intake_form
title: Rent Comp Intake Form
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [property_manager, leasing_manager, regional_manager, asset_manager]
  output_type: checklist
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/normalized/schemas/rent_comp.yaml
produced_by: workflows/rent_comp_intake
---

# Rent Comp Intake Form

**Subject property.** {{subject_property_name}} ({{subject_property_id}})
**Market / submarket.** {{market}} / {{submarket}}
**Surveyed by.** {{surveyed_by}}
**Survey date.** {{survey_date}}
**Survey method.** {{survey_method}}  (shop | call | online | subscription | colleague)

## Confidence banner

- Per-row confidence assessed per comp.
- All rows stamped `as_of_date` = survey date unless source indicates otherwise.

## Comp row

- Comp property name: {{comp_property_name}}
- Comp property address: {{comp_property_address}}
- Market / submarket: {{comp_market}} / {{comp_submarket}}
- Year built / renovated: {{comp_year_built}} / {{comp_year_renovated}}
- Unit count (approx): {{comp_unit_count}}
- Form factor: {{comp_form_factor}}
- Class (operator-judged): {{comp_class}}
- Unit type observed: {{unit_type}}  (e.g., 1BR/1BA, 2BR/2BA)
- SF observed: {{sf_observed}}
- Asking rent (quoted): {{asking_rent}}
- Concession offered (if any): {{concession_offered}}
- Effective rent computed: {{effective_rent}}
- Lease term offered: {{lease_term_offered}}
- Move-in date availability: {{move_in_availability}}
- Amenities highlighted: {{amenities_highlighted}}
- Unit finish level observed: {{finish_level}}
- Appliance package observed: {{appliance_package}}
- Parking type / cost: {{parking}}
- Pet policy / fees: {{pet_policy}}
- RUBS / utility treatment: {{rubs_or_utility}}
- Source of info: {{source_of_info}}
- Source date: {{source_date}}
- Confidence: {{confidence}}  (low | medium | high | verified)
- Status: {{record_status}}  (draft | proposed | approved | sample)
- Proposed by: {{proposed_by}}
- Notes: {{notes}}

## Quality gates

- [ ] Unit type explicitly recorded
- [ ] SF captured (not 'about' / range-only)
- [ ] Concession recorded separately from asking rent
- [ ] Effective rent computed with documented method
- [ ] Source and source date recorded
- [ ] Confidence assigned
- [ ] Status explicitly set
- [ ] Fair-housing neutrality: no protected-class references in notes

## Next steps

- [ ] Record written to `reference/raw/` with intake id
- [ ] Scheduled for normalization into `reference/normalized/market_rents__{market}_mf.csv`
- [ ] Change log entry queued

---

*Template status: starter.*
