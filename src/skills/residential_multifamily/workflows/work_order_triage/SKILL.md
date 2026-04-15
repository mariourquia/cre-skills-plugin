---
name: Work Order Triage
slug: work_order_triage
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Priority bands (P1/P2/P3/P4) and acknowledgment and completion SLAs are overlay-driven.
  Licensed-trade thresholds vary by jurisdiction. Vendor preferred-list membership and
  insurance/licensure freshness come from reference files and can go stale.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [stabilized, renovation, lease_up, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [property_manager, assistant_property_manager, maintenance_supervisor]
  output_types: [checklist, kpi_review, email_draft]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/normalized/work_order_priority_playbook__middle_market.csv
    - reference/normalized/approved_vendor_list__{market}.csv
    - reference/normalized/vendor_rate_cards__{market}.csv
    - reference/normalized/approval_threshold_defaults.csv
  writes: []
metrics_used:
  - open_work_orders
  - work_order_aging
  - repeat_work_order_rate
escalation_paths:
  - kind: safety_p1
    to: maintenance_supervisor -> property_manager -> regional_manager
  - kind: licensed_trade_required
    to: maintenance_supervisor -> property_manager (vendor verification mandatory)
  - kind: disbursement_above_threshold
    to: regional_manager -> asset_manager (rows 6, 7)
  - kind: vendor_contract_signature
    to: asset_manager -> legal (row 19)
approvals_required:
  - disbursement_above_threshold
  - vendor_contract_signature
description: |
  Classifies every incoming work order by urgency and category, assigns the right vendor
  or tech from the approved list, computes estimated cost and routes above-threshold
  disbursements for approval, verifies licensure and insurance for any licensed trade,
  and tracks the order through completion. Life-safety items are P1 and are never
  autonomously deferred.
---

# Work Order Triage

## Workflow purpose

Convert an incoming work order into an actioned task with the right priority, the right vendor or tech, the right cost expectation, and the right approvals. Enforce life-safety SLAs, license and insurance verification, and vendor-rotation discipline.

## Trigger conditions

- **Explicit:** "triage work orders", "priority this WO", "daily WO review", "assign vendor to WO X".
- **Implicit:** new WorkOrder created; P1 item reaches acknowledgment SLA boundary; aging bucket transition; repeat WO detected for same unit + category.
- **Recurring:** daily P1 screen; weekly backlog review.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| WorkOrder record(s) | table | required | description, reported_ts, unit_id, category |
| Priority playbook overlay | csv | required | P1–P4 definitions and SLA bands |
| Approved vendor list | csv | required | by market, by trade |
| Vendor rate cards | csv | required | cost estimate |
| Insurance/licensure status | table | required | vendor cert tracking |
| Property staff availability | table | optional | tech capacity |
| Prior WO history for unit | table | optional | informs repeat detection |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Priority assignment per WO | field | P1/P2/P3/P4 |
| Dispatch record | record | vendor or tech, ETA, cost estimate |
| Resident communication (if needed) | `email_draft` | entry notice or scheduling |
| Approval request (if above threshold) | request | row 6 or 7 |
| Triage queue snapshot | `kpi_review` | counts by priority, aging by priority |

## Required context

Asset_class, segment, form_factor, management_mode, market. Jurisdiction required if entry-notice communication will be drafted.

## Process

1. **Classify each WO.** Apply the priority playbook: P1 life-safety (gas leak, live electrical exposure, fire/smoke, no heat in cold season, no AC in hot season per overlay, flooding, lockout after hours per overlay, child-safety hazard); P2 habitability (major appliance, plumbing non-emergency, security); P3 comfort; P4 cosmetic.
2. **Confirm category and trade.** Map category to trade (plumbing, electrical, HVAC, appliance, general, landscaping, pest). Flag licensed-trade requirement per overlay.
3. **Licensed-trade verification (gate).** If the trade requires a license, verify the vendor's license and insurance are current. Stale or missing = refuse dispatch; escalate to maintenance_supervisor. The system does not mark any vendor preferred with stale licensure data.
4. **Vendor or tech selection.** Prefer on-staff tech if capacity and skill match; otherwise select from approved vendor list with rotation discipline. Pull cost estimate from rate card.
5. **Cost gate (decision point).** If estimated cost above disbursement thresholds (row 6 or 7), open `approval_request` before dispatch. Contract signature triggers row 19.
6. **Entry-notice communication (if required).** Draft resident entry notice per jurisdiction overlay; `legal_review_required` if jurisdiction treats as statutory.
7. **Dispatch.** Record ETA. P1 acknowledgment SLA is hard; miss escalates automatically.
8. **Track to completion.** Update status; on close, compute whether WO is a repeat (same unit + category within 30 days); flag vendor if `repeat_work_order_rate` exceeds overlay threshold.
9. **Daily queue snapshot.** Counts by priority; aging distribution; vendor performance summary.
10. **Confidence banner.** Surface reference `as_of_date` and `status`; surface vendor certification freshness.

## Metrics used

`open_work_orders`, `work_order_aging`, `repeat_work_order_rate`.

## Reference files used

- `reference/normalized/work_order_priority_playbook__middle_market.csv`
- `reference/normalized/approved_vendor_list__{market}.csv`
- `reference/normalized/vendor_rate_cards__{market}.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Escalation points

- P1 SLA breach: maintenance_supervisor -> property_manager -> regional_manager.
- Licensed-trade verification failure: maintenance_supervisor -> property_manager; vendor not dispatched.
- Disbursement above threshold: regional_manager -> asset_manager (row 6 or 7).
- Safety-critical scope change: maintenance_supervisor + property_manager + regional_manager (row 4).

## Required approvals

- Disbursement above threshold (row 6 or 7).
- Vendor contract signature (row 19).
- Safety-critical scope deferral (row 4).

## Failure modes

1. Auto-deferring a life-safety item. Fix: P1 never deferred without approval matrix row 4.
2. Dispatching to an out-of-cert vendor. Fix: licensure/insurance verification is a gate.
3. Treating all WOs equally. Fix: priority playbook governs.
4. Silent repeat patterns. Fix: repeat flag opens vendor scorecard review via `workflows/vendor_dispatch_sla_review`.
5. Sending entry notice without jurisdiction rules. Fix: overlay required; missing -> refuse entry-notice draft.

## Edge cases

- **After-hours emergency:** P1 on-call rotation per overlay; if on-call unassigned, escalation path fires immediately.
- **Resident refuses entry:** workflow documents refusal; entry notice tracked; legal counsel if blocking a safety issue.
- **Multiple units same issue:** batch dispatch; root-cause investigation flagged.
- **Warranty-covered:** route to warranty vendor; do not pay; flag if warranty expired.
- **Resident-caused damage:** WO still completed; chargeback captured and routed through ledger via `workflows/move_out_administration` or lease-violation process.

## Example invocations

1. "Triage the daily work-order queue for Ashford Park."
2. "WO 1842 reports a gas smell — handle."
3. "What does the WO backlog look like for Willow Creek this week?"

## Example outputs

### Output — Daily WO triage snapshot (abridged, Ashford Park)

**Queue.** P1 x 0, P2 x 4, P3 x 14, P4 x 5. `open_work_orders` within band.

**P1 status.** None open. Trailing week P1s acknowledged within SLA.

**Dispatch this cycle.**

- 2 P2 plumbing: dispatched to preferred vendor, licenses current; cost within threshold; no gate.
- 1 P2 HVAC: dispatched to preferred vendor, licenses current; estimated cost above threshold; `approval_request` row 6 opened.
- 1 P2 appliance: on-staff tech assigned.
- 2 P3: scheduled for next week.

**Repeat flags.** One P3 in unit 204 is second in 21 days for same category; vendor flagged for scorecard review via `workflows/vendor_dispatch_sla_review`.

**Entry notices.** 3 drafted per Charlotte overlay, `legal_review_required` banner; PM to confirm send.

**Confidence banner.** `approved_vendor_list__charlotte@2026-04-01, status=starter`. `vendor_rate_cards__charlotte@2026-04-01, status=sample`. Vendor license check freshness surfaced per vendor.
