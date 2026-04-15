---
template_slug: new_vendor_onboarding_checklist
title: New Vendor Onboarding Checklist
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation, construction, development]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [property_manager, regional_manager, construction_manager, asset_manager]
  output_type: checklist
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used:
  - reference/normalized/vendor_rate_cards__{market}.csv
produced_by: workflows/vendor_dispatch_sla_review
---

# New Vendor Onboarding Checklist

**Vendor.** {{vendor_company}}
**Primary contact.** {{vendor_contact_name}} | {{vendor_contact_email}} | {{vendor_contact_phone}}
**Scope area.** {{scope_area}}
**Onboarded at.** {{property_name}} / {{org_name}}
**Owner.** {{onboarding_owner}}

## Compliance and verification

- [ ] W-9 on file
- [ ] Business license verified (jurisdiction: {{jurisdiction}})
- [ ] Trade license verified (if applicable to scope): {{trade_license_ref}}
- [ ] Certificate of insurance on file (GL, auto, WC, umbrella as applicable): {{coi_ref}}
- [ ] Additional-insured endorsement verified where required: {{addl_insured_status}}
- [ ] OSHA / safety program documentation (for construction scope): {{safety_program_ref}}
- [ ] Drug and background testing protocol (if required by policy): {{screening_policy_ref}}
- [ ] Expiration tracker entered for all time-bound docs

## Commercial

- [ ] Rate card received and compared to `vendor_rate_cards` reference
- [ ] Master services agreement or work order template executed: {{msa_ref}}
- [ ] Standard SLAs documented per scope
- [ ] Payment terms confirmed
- [ ] Purchase-order / invoice process communicated

## Operational

- [ ] Access / key / gate code protocol agreed
- [ ] Escalation contact tree exchanged
- [ ] Hours of operation and after-hours contact documented
- [ ] On-property identification and badge issued (if required)
- [ ] Scope-of-work template reviewed

## Safety and fair-housing

- [ ] Safety orientation complete (hot-work, lock-out / tag-out, hazard comms as applicable)
- [ ] Fair-housing posture briefed (no differential treatment, no protected-class references in interactions)
- [ ] Resident-interaction conduct standards acknowledged

## Performance tracking

- [ ] Vendor record created in preferred-vendor list (status: {{vendor_status}})
- [ ] Initial KPIs set (response time, on-time rate, rework rate, cost variance)
- [ ] Probationary period defined: {{probation_length}}
- [ ] First scorecard review scheduled: {{first_review_date}}

## Sign-off

- Onboarding owner: {{onboarding_owner}}  (date: {{onboard_owner_signoff_date}})
- Approval: {{approver}}  (date: {{approver_signoff_date}})

---

*Template status: starter.*
