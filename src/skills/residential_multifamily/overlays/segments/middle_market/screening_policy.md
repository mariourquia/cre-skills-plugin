# Middle-Market Screening Policy Posture

This file describes the middle-market overlay's posture on screening. It is not a
policy; operators carry their own documented policies, which are loaded via the org
overlay. This file states what the segment overlay expects to see in that org
policy and how the overlay binds to the canonical screening guardrails.

## Segment posture

- Screening criteria are documented in a policy artifact loaded at the org overlay
  level. Ad-hoc criteria are prohibited per `_core/guardrails.md#screening`.
- Income and credit thresholds come from the org's documented policy, not from
  skill prose or this overlay. The overlay references the org policy by slug.
- Criminal history is handled through the operator's documented individualized-
  assessment process, aligned with HUD 2016 guidance and local ordinances. Blanket
  bans are prohibited.
- Source-of-income considerations follow local law. Where source-of-income is a
  protected class, the overlay binds to the jurisdiction's requirement rather than
  any default.
- Reasonable accommodation and reasonable modification requests are human-decided
  and never autonomously denied, fee-gated above policy, or treated as optional.

## What the overlay binds to

The overlay's `screening_policy` override points at
`overlays/segments/middle_market/screening_policy.md#policy_posture`, which in turn
points at `_core/guardrails.md#screening`. The org overlay provides the actual
policy document in `overlays/org/<org_id>/screening_policy/`.

## Application conversion expectation

Because middle-market screening is strict-but-documented, the segment's
`application_conversion` target band (in
`reference/derived/role_kpi_targets.csv#row_mm_application_conversion`) is
calibrated to this posture. Sustained conversion below band triggers a review of
the funnel; above-band may indicate a screening gap that requires org-side review.

## What this overlay will not do

This overlay will not:

- Produce screening criteria outside the documented policy.
- Infer protected-class attributes from applicant data.
- Apply a concession or screening exception outside the documented process.
- Recommend an ad-hoc override to screening.

Per guardrails, the system surfaces policy refusals and the approved path.
