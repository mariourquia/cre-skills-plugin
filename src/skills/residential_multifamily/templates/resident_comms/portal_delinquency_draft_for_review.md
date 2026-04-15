---
template_slug: portal_delinquency_draft_for_review
title: Portal Delinquency Draft (for review)
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation]
  management_mode: [self_managed, third_party_managed]
  role: [property_manager, assistant_property_manager, leasing_manager]
  output_type: email_draft
legal_review_required: true
jurisdiction_sensitive: true
status: starter
references_used:
  - reference/normalized/delinquency_playbook_middle_market.csv
produced_by: roles/property_manager, workflows/delinquency_collections
---

> **LEGAL REVIEW REQUIRED BEFORE SEND.** This draft may approach — or constitute — a statutory pay-or-quit or delinquency notice depending on jurisdiction. Do not send until your operating counsel or designated legal reviewer has confirmed tone, form, notice period, delivery method, and jurisdiction-specific requirements. Absolutely no eviction-related language is to be added or sent autonomously.

# Portal Message — Account Update

Subject: Let's get your account up to date.

Hi {{resident_first_name}},

We want to help resolve the balance currently open on your account. Below is a summary and your options for bringing the account current.

## Account snapshot

- Unit: {{unit_number}}
- Current balance: {{current_balance}}
- Last payment received: {{last_payment_date}} ({{last_payment_amount}})
- Days past due: {{days_past_due}}

## Options

1. **Pay in full.** Pay the current balance through the portal: {{portal_link}}.
2. **Payment plan (standard).** Contact the office to set up a standard plan that fits your situation.
3. **Stop by.** We would rather talk than write. Office hours: {{office_hours}}. Office: {{office_phone}}.

## What happens next

If we do not hear from you by {{followup_date}}, we will reach out again. We want to keep you in the community.

## Resources

- Rental assistance programs in your area: {{rental_assistance_resources}}
- Our office is happy to walk you through options.

Thanks,
{{leasing_team_name}}
{{property_name}}

---

> **LEGAL REVIEW CHECKPOINTS (before send):**
> - Jurisdiction: does this message cross into a statutory notice under local / state law?
> - Tone: is the language free of threats, misrepresentation, or unlawful fee references?
> - FDCPA / state debt-collection rules: are all disclosures correct where applicable?
> - Ledger accuracy: has the balance been validated against the rent roll and GL?
> - Fair housing: is the message uniformly templated and free of preference / protected-class references?
> - Escalation gates: any pay-or-quit notice, late-fee waiver, non-standard payment plan, or lease-default step routes per approval matrix rows 1 / 13.

*Template status: starter — draft only; not for send without review.*
