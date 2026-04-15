# Middle-Market Resident Communication Tone

The middle-market communication voice is friendly, professional, and plain-language.
Residents should feel respected, informed, and never talked down to. Legal or
clinical language is reserved for notices that legally require it; everyday
communication reads like a well-run workplace.

## Tone profile

- Plain language at a general reading level. Avoid industry jargon (no "NTV,"
  "rollover," "LTL," "trade-out" in resident-facing copy).
- Warm but efficient. Acknowledge the resident, state the action or information,
  close with a clear next step.
- First-person plural ("we"). Residents address a team, not a system.
- No slang, no emojis in operational communications. Amenity-event or holiday
  messages may carry a lighter register per the property's brand guide.

## Forbidden patterns

Per `_core/guardrails.md#fair_housing`, communication never:

- Signals preference or limitation on a protected basis. Copy scans flag phrases
  like "great for young professionals," "perfect for families," "quiet community"
  where "quiet" implies a protected-class limitation, and so on.
- References a resident's protected attributes, even to compliment.
- Suggests a resident pursue or forgo a reasonable accommodation.

## Legal-notice exception

Notices that constitute legal communication under a jurisdiction's law (rent
increase, non-renewal, entry, pay-or-quit) carry a `legal_review_required` banner in
their YAML frontmatter and are reviewed by a human before send. The tone of a legal
notice is correct and complete first; the friendly framing comes via a companion
resident-facing message that does not substitute for the notice itself.

## Channel posture

Default channel is the resident's documented preferred channel (email, portal,
text, phone). No channel preference is assumed from resident attributes. Urgent
safety matters escalate to phone plus door-knock regardless of preference.

## QA

Outbound drafts are scanned for forbidden patterns, for reading level, and for
channel-appropriate length before they route to a human for send or to an
action_routable automation under policy.
