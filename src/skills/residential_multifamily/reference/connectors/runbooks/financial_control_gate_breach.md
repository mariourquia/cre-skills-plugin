# Runbook: Financial Control Gate Breach

status_tag: reference

The integration layer detects that automation is about to act beyond the approval floor documented in `_core/approval_matrix.md`. Examples: concession above policy, vendor award without approval, draw disbursement without lien waivers, change order above threshold without required approvers, final lender or investor submission without finance sign-off.

## 1. Trigger

- Exception of category `policy_violation` in the queue.
- Alert `approval_gate_breach_imminent` fires.
- A workflow attempts to execute an action flagged `action_requires_approval` without a matching approved `ApprovalRequest`.
- A change-order, bid-award, or draw-release artifact is ready to submit and the system cannot locate the required approvals.

## 2. Symptoms

- Workflow execution halts with an `approval_required` status.
- `approval_audit_log.jsonl` shows an `opened` entry with no matching `approved` entry for a gated action.
- Operator or agent attempts to override the block.
- `draw_package_review`, `bid_leveling_procurement_review`, `change_order_review`, or any investor or lender submission workflow surfaces the breach as a blocker.

## 3. Likely causes (ranked)

1. Legitimate pending approval, the `ApprovalRequest` exists but is not yet in `approved` status.
2. Approval was previously granted but scope expanded; the new scope exceeds the prior approval.
3. Policy overlay change tightened thresholds and an in-flight action is now gated where it previously was not.
4. Automation edge case, the action was auto-classified as `action_routable` but should have been `action_requires_approval` under current policy.
5. Explicit override attempt by a human or agent without authority.

## 4. Immediate actions (minute-by-minute, numbered)

1. Halt the action. Do not allow execution. The subsystem router's default behavior is to refuse; this runbook describes what to do after the refusal.
2. Identify the gate. Read `_core/approval_matrix.md` and determine which row applies (concession deviation, vendor award, change order, draw, final lender/investor submission, policy change, etc.).
3. Check for an existing `ApprovalRequest`:
   - If one exists in `pending` status with matching scope, escalate to the approver audience to complete the decision.
   - If one exists but was `denied`, `expired`, or `cancelled`, the action cannot proceed; open a new request only if facts have changed.
   - If none exists, open a new `ApprovalRequest` per `_core/schemas/approval_request.yaml`.
4. Notify approvers. Route to the audience(s) and roles named in the matching row. Common mappings:
   - Row 6 and 7 (financial disbursement): `property_manager`, `regional_manager`, and above by threshold.
   - Row 8 (contract award or material procurement): `regional_manager` and `asset_manager`.
   - Row 9 (bid award): `construction_manager` and `asset_manager`; development or executive for major bids.
   - Row 10 and 11 (change order): `construction_manager`, `asset_manager`, and executive by threshold.
   - Row 12 (draw request submission): `construction_manager` and `asset_manager`.
   - Row 13 (lease deviation or concession): `property_manager` and `regional_manager`; fair-housing review required if patterned.
   - Row 14 and 15 (lender- or investor-facing final): `asset_manager`, `finance_reporting` lead, and executive per row.
   - Row 20 (canonical data change): system maintainer and designated reviewer.
5. Attach the full action context to the request: target object, scope, magnitude classification (bands, not numbers in prose; numbers live in the overlay), justification.
6. Set a dwell-time SLA matching the severity of the action's consequence (see `../monitoring/exception_routing.yaml`).
7. If the action is in a regulatory-reporting path and the delay threatens a filing deadline, escalate to `compliance_risk` and consider whether an interim, less-scoped action can satisfy the deadline without crossing the gate.
8. Document the breach in `approval_audit_log.jsonl`: entries for `opened`, `approved` or `denied` (when decision lands), and `executed` (only if approved and carried out).

## 5. Escalation path

- Follow `_core/approval_matrix.md` exactly. Do not substitute roles unless the overlay explicitly names a substitute.
- Fair-housing-sensitive actions additionally route via `fair_housing_sensitive_flag.md`.
- Investor-, lender-, regulator-, or board-facing actions escalate to `executive` automatically.
- `legal_counsel` reviews any action with legal exposure (eviction, contract binding the owner, regulatory filing).
- `finance_reporting` must sign off on financial disbursements, draws, and lender or investor submissions.
- Any attempt to override without an approved request is logged as an exception and reviewed.

## 6. Affected workflows

The halted workflow and its downstream consumers. Specifically, the workflows most likely to hit this runbook:

- `draw_package_review` (draw release, lien waivers).
- `bid_leveling_procurement_review` (bid award above threshold).
- `change_order_review` (CO above threshold).
- `renewal_retention` or `lead_to_lease_funnel_review` (concession above policy).
- `delinquency_collections` (non-standard payment plan).
- `owner_approval_routing` (the routing workflow itself).
- `quarterly_portfolio_review`, `executive_operating_summary_generation` (final investor or board output).
- `monthly_asset_management_review` (final lender output).
- `vendor_dispatch_sla_review` (vendor dispatch above authority).

## 7. Recovery steps

- When approval lands, resume the action. Log the `approved` and `executed` entries.
- When approval is denied, notify the workflow owner. Do not retry the action without a new request or a material change in circumstances.
- If the gate fired because of an overlay change and the overlay needs revision, handle via the overlay change process, not by weakening the gate.
- If the gate fired because of an automation edge case (misclassification), open a contract-update proposal to correct the classification; apply a manual override only per `manual_override_approval.md`.

## 8. Verification steps

- `approval_audit_log.jsonl` tail is consistent: no dangling `pending`, no `executed` without a matching `approved`.
- The action, if executed, matches the scope approved.
- Downstream workflow resumes cleanly.
- No secondary breaches were triggered.
- Exception queue entries for the breach are closed with remediation notes.

## 9. Post-incident review hooks

- Every breach attempt is reviewed by `finance_reporting` and `asset_mgmt` at the weekly readout.
- Patterns of recurring breaches at a gate feed a structural review, either threshold calibration (overlay adjustment) or automation-side classification correction.
- Executive-facing breach counts feed `executive` monthly operations review.
- `compliance_risk` reviews any breach involving regulatory filings or fair-housing-sensitive actions.
- `legal_counsel` reviews any breach involving contracts binding the owner, evictions, or disputes.
