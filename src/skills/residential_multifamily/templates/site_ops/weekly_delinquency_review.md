---
template_slug: weekly_delinquency_review
title: Weekly Delinquency Review
applies_to:
  segment: [middle_market]
  form_factor: []
  lifecycle: [stabilized, lease_up, renovation]
  management_mode: [self_managed, third_party_managed]
  role: [property_manager, regional_manager, asset_manager]
  output_type: operating_review
legal_review_required: false
jurisdiction_sensitive: true
status: starter
references_used:
  - reference/normalized/delinquency_playbook_middle_market.csv
  - reference/normalized/collections_benchmarks__{region}_mf.csv
  - reference/normalized/approval_threshold_defaults.csv
produced_by: roles/property_manager, workflows/delinquency_collections
---

# Weekly Delinquency Review

**Property.** {{property_name}} ({{property_id}}) — {{market}} / {{submarket}}
**Week ending.** {{week_ending_date}}

## Confidence banner

- Playbook reference as-of: {{delinquency_playbook_as_of}} (status: {{delinquency_playbook_status}})
- Collections benchmark as-of: {{collections_benchmarks_as_of}} (status: {{collections_benchmarks_status}})
- Approval thresholds as-of: {{approval_thresholds_as_of}} (status: {{approval_thresholds_status}})

## Headline

- `delinquency_rate_30plus`: {{delinquency_rate_30plus}} (prior: {{delinquency_rate_30plus_prior}}, target: {{target_delinquency_rate_30plus}})
- `collections_rate` (T7): {{collections_rate_t7}} | (MTD): {{collections_rate_mtd}}
- `bad_debt_rate` (T12): {{bad_debt_rate_t12}}

## Aging bucket movement

| Bucket | Units prior week | Units this week | $ balance this week | Movement |
|---|---|---|---|---|
| 0 (current) | {{bucket_current_prior}} | {{bucket_current}} | {{bucket_current_balance}} | {{bucket_current_delta}} |
| 1-7 days | {{bucket_1_7_prior}} | {{bucket_1_7}} | {{bucket_1_7_balance}} | {{bucket_1_7_delta}} |
| 8-30 days | {{bucket_8_30_prior}} | {{bucket_8_30}} | {{bucket_8_30_balance}} | {{bucket_8_30_delta}} |
| 31-60 days | {{bucket_31_60_prior}} | {{bucket_31_60}} | {{bucket_31_60_balance}} | {{bucket_31_60_delta}} |
| 61-90 days | {{bucket_61_90_prior}} | {{bucket_61_90}} | {{bucket_61_90_balance}} | {{bucket_61_90_delta}} |
| 90+ days | {{bucket_90_plus_prior}} | {{bucket_90_plus}} | {{bucket_90_plus_balance}} | {{bucket_90_plus_delta}} |

## Stage-by-stage playbook status (middle-market)

| Stage (per playbook) | Residents in stage | Action due this week | Owner | Approval gate |
|---|---|---|---|---|
| Day 1-5: reminder + ledger validate | {{stage_day_1_5_count}} | {{stage_day_1_5_action}} | {{stage_day_1_5_owner}} | none |
| Day 6-15: plan offer + PM review | {{stage_day_6_15_count}} | {{stage_day_6_15_action}} | {{stage_day_6_15_owner}} | pay_or_quit_prep (if applicable) |
| Day 16+: eviction-track review | {{stage_day_16_plus_count}} | {{stage_day_16_plus_action}} | {{stage_day_16_plus_owner}} | approval_matrix row 2 |

## Payment plans

- Active plans: {{active_payment_plans}}
- Compliant: {{plans_compliant}} | In breach: {{plans_in_breach}}
- New plan requests this week: {{plan_requests_this_week}} | Non-standard (requires approval): {{non_standard_plan_requests}}

## Proposed communications (drafts)

- Portal delinquency draft: {{portal_draft_ref}} — flagged legal_review_required
- Pay-or-quit pre-read package: {{pay_or_quit_ref}} — gated (approval row 1)
- Payment-plan confirmation: {{payment_plan_comms_ref}}

## Escalations

- To regional / AM: {{escalations_to_regional_am}}
- To legal counsel: {{escalations_to_counsel}}

## Action items

| # | Action | Owner | Due | Approval gate |
|---|---|---|---|---|
| 1 | {{action_1}} | {{action_1_owner}} | {{action_1_due}} | {{action_1_gate}} |
| 2 | {{action_2}} | {{action_2_owner}} | {{action_2_due}} | {{action_2_gate}} |
| 3 | {{action_3}} | {{action_3_owner}} | {{action_3_due}} | {{action_3_gate}} |

---

*Template status: starter. Any resident-facing notice generated from this review inherits the legal-review requirement of its source template.*
