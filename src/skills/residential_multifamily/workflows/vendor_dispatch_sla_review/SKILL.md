---
name: Vendor Dispatch and SLA Review
slug: vendor_dispatch_sla_review
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Vendor scorecard thresholds, SLA bands, and rotation discipline rules are overlay-driven.
  Vendor insurance and licensure tracking depends on the reference being current; stale
  vendor certs must surface at review.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [stabilized, renovation, lease_up, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [property_manager, maintenance_supervisor, regional_manager, asset_manager]
  output_types: [scorecard, kpi_review, memo]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/normalized/approved_vendor_list__{market}.csv
    - reference/normalized/vendor_rate_cards__{market}.csv
    - reference/normalized/vendor_sla_policy__{org}.yaml
    - reference/normalized/approval_threshold_defaults.csv
  writes: []
metrics_used:
  - repeat_work_order_rate
  - work_order_aging
  - open_work_orders
escalation_paths:
  - kind: vendor_cert_expired
    to: property_manager -> regional_manager (preferred status removed)
  - kind: vendor_contract_signature
    to: asset_manager -> legal (row 19)
  - kind: performance_dispute
    to: regional_manager -> asset_manager
approvals_required:
  - vendor_contract_signature
  - vendor_preferred_list_change
description: |
  Weekly and quarterly review of dispatch SLA adherence and vendor performance. Produces
  a vendor scorecard per market and trade, flags underperformers, verifies insurance and
  licensure freshness, and proposes rotation actions. Vendor contract changes are routed
  for approval.
---

# Vendor Dispatch and SLA Review

## Workflow purpose

Keep the approved vendor list accurate, the SLAs enforced, and underperformers rotated out. Produces the scorecard and the rotation proposal; does not unilaterally change preferred-list membership.

## Trigger conditions

- **Explicit:** "vendor scorecard", "SLA review", "review dispatch", "rotate vendor".
- **Implicit:** `repeat_work_order_rate` above overlay threshold for a vendor; vendor license or insurance expiry within overlay window; SLA breach pattern.
- **Recurring:** weekly property-level SLA check; quarterly portfolio-level vendor scorecard.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| WorkOrder log (T90) | table | required | dispatch_ts, completed_ts, vendor_id |
| Vendor list + certs | table | required | insurance, license dates |
| Vendor rate cards | csv | required | for pricing discipline view |
| SLA policy overlay | yaml | required | SLAs by priority and trade |
| Repeat WO history | derived | required | input to scorecard |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Vendor scorecard | `scorecard` | per vendor: SLA adherence, repeat rate, cost discipline, cert freshness |
| Flagged underperformers | list | rationale, proposed action, approval gate |
| Cert-refresh requests | `checklist` | vendor, cert type, expiry date |
| Rotation proposal | `memo` | add/remove/suspend proposals |

## Required context

Asset_class, segment, management_mode, market.

## Process

1. **Pull dispatch data.** Join WOs to vendors; compute per-vendor SLA adherence, `repeat_work_order_rate`, cost-vs-rate-card variance.
2. **Scorecard compute.** Score per overlay rubric: SLA, repeat, quality (callbacks), cost discipline, cert freshness.
3. **Cert freshness gate.** Vendors with expired certs lose preferred status immediately; dispatches are refused by `workflows/work_order_triage` until cert refresh.
4. **Underperformer identification.** Vendors below overlay thresholds flagged; proposed actions (coach, suspend, rotate out) per rubric.
5. **Rotation proposal.** Additions and removals to the preferred list require `approval_request` row 19 for contract changes; list changes without contract impact route to asset_manager for approval per overlay.
6. **Cost discipline check.** Variance of actual cost to rate card above overlay threshold flags for re-negotiation.
7. **Communication drafts.** Vendor-facing drafts `draft_for_review`; scorecard-share drafts for routine updates.
8. **Confidence banner.** Reference `as_of_date` and cert-freshness dates surfaced.

## Metrics used

`repeat_work_order_rate`, `work_order_aging`, `open_work_orders`.

## Reference files used

- `reference/normalized/approved_vendor_list__{market}.csv`
- `reference/normalized/vendor_rate_cards__{market}.csv`
- `reference/normalized/vendor_sla_policy__{org}.yaml`
- `reference/normalized/approval_threshold_defaults.csv`

## Escalation points

- Expired cert: PM -> regional; preferred status removed.
- Vendor contract change: `approval_request` row 19.
- Performance dispute: regional -> asset_manager.

## Required approvals

- Vendor contract signature (row 19).
- Preferred-list changes per overlay.

## Failure modes

1. Keeping a preferred vendor with stale certs. Fix: automatic removal on expiry.
2. Scoring on SLA only, missing repeat rate. Fix: rubric includes both.
3. Over-reliance on one vendor. Fix: concentration flag per trade.
4. Silent rate-card drift. Fix: cost discipline check surfaces variance.

## Edge cases

- **Single-source trade market:** overlay flags; scorecard widened to capture context; PM proposes sourcing.
- **Seasonal vendor:** scorecard annualized; SLA adjusted per overlay seasonal adjustment.
- **Emergency sub:** allowed outside preferred list for P1; cert check still required; dispatch recorded as exception.

## Example invocations

1. "Run the weekly SLA review for Ashford Park."
2. "Build the quarterly vendor scorecard for the Charlotte portfolio."
3. "Vendor X has three repeat WOs this month. Recommend next step."

## Example outputs

### Output — Weekly vendor SLA snapshot (abridged, Ashford Park)

**SLA adherence.** Most vendors above SLA band; one plumbing vendor below SLA on P2; flagged for coaching.

**Repeat rate.** One HVAC vendor above overlay threshold; scorecard flag; proposed action: coach + re-bid.

**Cert freshness.** One vendor insurance expiring within overlay window; cert-refresh request drafted.

**Cost discipline.** One vendor consistently above rate card; re-negotiation proposed.

**Rotation proposal.** No removals this week. One suspension candidate under review for quarterly.

**Approvals opened.** None for contract changes this week; queued for quarterly.

**Confidence banner.** `approved_vendor_list__charlotte@2026-04-01, status=starter`. `vendor_sla_policy@2026-03-31, status=starter`.
