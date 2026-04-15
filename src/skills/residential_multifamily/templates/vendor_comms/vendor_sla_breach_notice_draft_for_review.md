---
template_slug: vendor_sla_breach_notice_draft_for_review
title: Vendor SLA Breach Notice (for review)
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation, construction, development]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [property_manager, regional_manager, construction_manager, asset_manager]
  output_type: email_draft
legal_review_required: true
jurisdiction_sensitive: false
status: starter
references_used: []
produced_by: workflows/vendor_dispatch_sla_review
---

> **LEGAL REVIEW REQUIRED BEFORE SEND.** This draft may be cited in a vendor-contract dispute. Do not send until your operating counsel or designated legal reviewer has confirmed that the notice aligns with the executed vendor agreement, any cure-period requirements, and the owner's preferred remedies.

# Vendor SLA Breach Notice

To: {{vendor_contact_name}}, {{vendor_company}}
From: {{sender_name}}, {{sender_title}}, {{property_name}}
Date: {{notice_date}}
Subject: SLA breach — {{contract_reference}}

## Contract reference

- Agreement: {{agreement_name}} dated {{agreement_date}}
- Scope area: {{scope_area}}
- Applicable SLA: {{applicable_sla}}

## Observed breach(es)

| # | Date / event | SLA standard | Observed performance | Documented impact |
|---|---|---|---|---|
| 1 | {{breach_1_event}} | {{breach_1_std}} | {{breach_1_obs}} | {{breach_1_impact}} |
| 2 | {{breach_2_event}} | {{breach_2_std}} | {{breach_2_obs}} | {{breach_2_impact}} |
| 3 | {{breach_3_event}} | {{breach_3_std}} | {{breach_3_obs}} | {{breach_3_impact}} |

## Requested corrective action

- {{corrective_action_1}}
- {{corrective_action_2}}

## Cure period

Per the agreement, the cure period is {{cure_period}}. Please confirm receipt and provide a written corrective action plan by {{cure_plan_due}}.

## Escalation if not cured

If the breach is not cured by {{cure_deadline}}, we will consider further remedies under the agreement, including but not limited to {{possible_remedies}}.

Please contact {{sender_name}} at {{sender_contact}} with any questions.

{{sender_name}}
{{sender_title}}
{{property_name}}

---

> **LEGAL REVIEW CHECKPOINTS (before send):**
> - Contract alignment: does the cited SLA, cure period, and remedy language match the executed agreement?
> - Documentation: is the observed breach supported by system-of-record evidence (work orders, incident logs, communications)?
> - Tone: is the tone firm and factual without threat or defamation?
> - Forum / method of delivery: does the agreement require a specific delivery method?
> - Approval gate: contract-significant notices route per approval matrix row 19 (vendor contract signature / material contract actions).

*Template status: starter — draft only; not for send without review.*
