---
template_slug: renewal_offer_draft_for_review
title: Renewal Offer Draft (for review)
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, renovation]
  management_mode: [self_managed, third_party_managed]
  role: [property_manager, leasing_manager]
  output_type: email_draft
legal_review_required: true
jurisdiction_sensitive: true
status: starter
references_used:
  - reference/normalized/market_rents__{market}_mf.csv
  - reference/normalized/concession_benchmarks__{market}_mf.csv
produced_by: roles/property_manager, workflows/renewal_retention
---

> **LEGAL REVIEW REQUIRED BEFORE SEND.** This draft may constitute a statutory rent-increase or non-renewal notice in some jurisdictions. Do not send until your operating counsel or designated legal reviewer has confirmed form, notice period, delivery method, and jurisdiction-specific requirements.

# Renewal Offer

Subject: Renewing your lease at {{property_name}}, {{resident_first_name}}.

Hi {{resident_first_name}},

Your current lease at {{property_name}}, Unit {{unit_number}}, ends on {{current_lease_end_date}}. We would like you to stay. Below are renewal options for your review.

## Renewal options

| Option | Term | New monthly rent | Effective date | Notes |
|---|---|---|---|---|
| {{option_1_label}} | {{option_1_term}} | {{option_1_rent}} | {{option_1_effective}} | {{option_1_notes}} |
| {{option_2_label}} | {{option_2_term}} | {{option_2_rent}} | {{option_2_effective}} | {{option_2_notes}} |
| {{option_3_label}} | {{option_3_term}} | {{option_3_rent}} | {{option_3_effective}} | {{option_3_notes}} |

*Current monthly rent: {{current_monthly_rent}}.*

## How to accept

- Reply to this email with your preferred option, or
- Log into your portal at {{portal_link}} and select a renewal option there, or
- Stop by the office during {{office_hours}}.

## Response window

Please respond by {{response_deadline}} so we can prepare the renewal paperwork in time. If we do not hear from you by {{response_deadline}}, we will follow up.

## Questions?

Your team is here:
- Office: {{office_phone}} | {{office_email}}
- Office hours: {{office_hours}}

Thanks for being part of our community.

{{leasing_team_name}}
{{property_name}}

---

> **LEGAL REVIEW CHECKPOINTS (before send):**
> - Jurisdiction: does local / state law treat this communication as a statutory notice?
> - Notice period: does the proposed rent change satisfy jurisdiction-specific minimums?
> - Delivery method: does local law require certified mail, posting, or any particular format?
> - Content: does the draft comply with fair-housing marketing guidance? Does it avoid preference signaling? Does it avoid protected-class references?
> - Operator policy: does the offer stay inside the concession policy overlay and the renewal strategy band? Any exception requires approval per approval matrix row 13.
> - Rent-regulated units (if applicable): does the increase comply with applicable caps / notice rules?

*Template status: starter — draft only; not for send without review.*
