# CRM Reconciliation Rules

Narrative describing how reconciliation in the CRM domain works.

## Reconciliation scope

The CRM captures prospect and resident communication, campaign attribution, service requests, and agent follow-ups. It reconciles with:

- The PMS lead, tour, application, and lease records (for funnel linkage).
- The PMS resident_account records (for resident communication targeting).
- Campaign spend records (for cost-per-lead and cost-per-lease attribution).

The CRM is NOT the system of record for funnel stage: the PMS is. The CRM is the system of record for the touches that drive stage transitions.

## Totals that must agree

### Lead counts (CRM leads versus PMS leads)

For each property_id and window, the count of distinct lead_ids referenced in CRM lead_interactions equals the count of pms.lead rows for that property and window, within the candidate-duplicate allowance. Tolerance is the duplicate-surfacing window declared in `lead_dedup_rules.yaml`.

### Interaction-to-lead attachment

For each lead_id, the count of lead_interactions linked to it equals the sum of inbound + outbound interactions observed across all channels. Any orphan lead_id in interactions (lead_id not in pms.lead) is flagged; historical orphans after merge carry a merged_into pointer.

### Campaign attribution

For each campaign_source with spend_cents IS NOT NULL, the count of pms.lead.source_channel = campaign_id matches the count of distinct contacts that arrived via the campaign's tracked channels. Tolerance is the attribution-window mismatch declared in `campaign_registry.yaml`.

### Follow-up task aging

For each open follow_up_task, the age against due_date matches the SLA declared in `workflows/lead_to_lease_funnel_review/`. Tolerance is the grace window declared in the workflow manifest.

## Tolerances

| Reconciliation | Absolute tolerance | Relative tolerance |
|---|---|---|
| Lead counts CRM vs PMS | referenced from lead_dedup_rules.yaml | 0 |
| Interaction-to-lead attachment | 0 | 0 |
| Campaign attribution | referenced from campaign_registry.yaml | 0 |
| Follow-up task aging | referenced from workflow manifest | 0 |

All non-zero tolerance values live in referenced configuration.

## Escalation triggers

- A blocker failure on protected-class scan escalates to the compliance_risk audience immediately; the landing holds until sanitized.
- Merged-lead survivorship blocker failures escalate to the site_ops and asset_mgmt audiences because funnel attribution is load-bearing for leasing performance reviews.
- Campaign attribution warnings with spend but no inquiries escalate to the leasing_strategy audience (cost-per-lead implications).

## Cross-domain reconciliation dependencies

CRM reconciliation failures on lead-attachment and stale-pipeline warnings feed directly into the `lead_to_lease_funnel_review` workflow. A blocker in CRM holds the funnel review for the affected property until reconciled. Stale-pipeline warnings, when they accumulate across multiple landings, escalate to the leasing_strategy audience.
