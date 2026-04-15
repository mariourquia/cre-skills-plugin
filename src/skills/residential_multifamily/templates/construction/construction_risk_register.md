---
template_slug: construction_risk_register
title: Construction Risk Register
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [construction, renovation, development]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [construction_manager, development_manager, asset_manager]
  output_type: checklist
legal_review_required: false
jurisdiction_sensitive: false
status: starter
references_used: []
produced_by: workflows/schedule_risk_review, workflows/cost_to_complete_review
---

# Construction Risk Register

**Project.** {{project_name}} ({{project_id}})
**Property.** {{property_name}} ({{property_id}})
**Register owner.** {{register_owner}}
**Last updated.** {{last_updated}}

## Confidence note

- Register is qualitative; cost and schedule impacts reference the project SOV and contingency ledger in the project file.

## Scoring rubric

- Likelihood: L1 (rare) | L2 (unlikely) | L3 (possible) | L4 (likely) | L5 (near certain)
- Impact: I1 (trivial) | I2 (minor) | I3 (material) | I4 (significant) | I5 (project-threatening)
- Composite: L x I (1-25). Anything scoring >= 9 requires a named mitigation plan and re-review cadence.

## Register

| # | Risk | Category | L | I | Score | Trigger / early signal | Mitigation | Owner | Next review | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | {{risk_1}} | {{risk_1_cat}} | {{risk_1_L}} | {{risk_1_I}} | {{risk_1_score}} | {{risk_1_trigger}} | {{risk_1_mitigation}} | {{risk_1_owner}} | {{risk_1_review}} | {{risk_1_status}} |
| 2 | {{risk_2}} | {{risk_2_cat}} | {{risk_2_L}} | {{risk_2_I}} | {{risk_2_score}} | {{risk_2_trigger}} | {{risk_2_mitigation}} | {{risk_2_owner}} | {{risk_2_review}} | {{risk_2_status}} |
| 3 | {{risk_3}} | {{risk_3_cat}} | {{risk_3_L}} | {{risk_3_I}} | {{risk_3_score}} | {{risk_3_trigger}} | {{risk_3_mitigation}} | {{risk_3_owner}} | {{risk_3_review}} | {{risk_3_status}} |
| 4 | {{risk_4}} | {{risk_4_cat}} | {{risk_4_L}} | {{risk_4_I}} | {{risk_4_score}} | {{risk_4_trigger}} | {{risk_4_mitigation}} | {{risk_4_owner}} | {{risk_4_review}} | {{risk_4_status}} |
| 5 | {{risk_5}} | {{risk_5_cat}} | {{risk_5_L}} | {{risk_5_I}} | {{risk_5_score}} | {{risk_5_trigger}} | {{risk_5_mitigation}} | {{risk_5_owner}} | {{risk_5_review}} | {{risk_5_status}} |

### Category legend

- `schedule`, `cost`, `trade_buyout`, `design`, `unforeseen_site`, `weather`, `permitting`, `safety`, `vendor_performance`, `lender_funding`, `entitlements`, `resident_impact`.

## Active mitigations in progress

{{active_mitigations}}

## Risks promoted to issues

{{promoted_issues}}

## Escalations open

{{escalations_open}}

---

*Template status: starter.*
