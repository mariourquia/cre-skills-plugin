---
name: Owner Approval Routing
slug: owner_approval_routing
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Approval thresholds live in org overlays; the canonical approval matrix rows are stable.
  Routing behavior for each row depends on the overlay; no dollar constants live in skill
  prose.
applies_to:
  segment: [middle_market, affordable, luxury]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise, high_rise]
  lifecycle: [development, construction, lease_up, stabilized, renovation, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [property_manager, regional_manager, asset_manager, portfolio_manager, third_party_manager_oversight_lead, construction_manager, development_manager, coo_operations_leader, cfo_finance_leader, ceo_executive_leader, reporting_finance_ops_lead]
  output_types: [checklist, memo, email_draft]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/normalized/approval_threshold_defaults.csv
    - reference/normalized/approval_routing_policy__{org}.yaml
  writes:
    - reference/derived/approval_audit_log.jsonl
metrics_used:
  - approval_response_time_tpm
escalation_paths:
  - kind: approval_sla_breach
    to: next-level approver per overlay
approvals_required: []
description: |
  The plumbing for every gated action. Takes a pending `ApprovalRequest` and routes it to
  the correct approvers per the approval matrix row and org overlay, tracks SLA, and
  records the outcome to the approval audit log. Invoked by any workflow that opens an
  approval request. Never decides on behalf of humans; composes and routes.
---

# Owner Approval Routing

## Workflow purpose

Deliver approval requests to the right approvers, in the right order, with the right package, and with an enforced SLA. Produce a complete audit trail. Every gated action in the subsystem depends on this workflow; its job is to make approvals a simple, reliable plumbing layer.

## Trigger conditions

- **Explicit:** "route this approval", "open approval request for X", "approval status update".
- **Implicit:** any workflow writes an `ApprovalRequest` record.
- **Recurring:** continuous; SLA screen runs daily.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| `ApprovalRequest` record | record | required | includes matrix row, subject, actor, proposed action |
| Approval routing policy overlay | yaml | required | per-org overrides to matrix defaults |
| Approver roster | yaml | required | org contacts per role |
| Related artifacts | package | required | memos, drafts, estimates |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Routing plan | `checklist` | approvers in order, SLA, deadlines |
| Approval packet | bundle | all artifacts a human needs |
| Approver notifications | `email_draft` | `draft_for_review` initially; sent once automated send is overlay-permitted |
| Audit log entry | jsonl | append to `reference/derived/approval_audit_log.jsonl` |
| Status updates | record | open, approved, denied, cancelled, expired |

## Required context

Asset_class, segment, org, matrix row, subject object type. Additional axes depend on the action.

## Process

1. **Receive `ApprovalRequest`.** Validate fields against schema; reject incomplete.
2. **Resolve row and approvers.** Read `approval_matrix.md` row + `approval_routing_policy__{org}.yaml` overrides; compose ordered approver list.
3. **Assemble packet.** Include all linked artifacts from the opening workflow.
4. **Notify.** Draft messages to approvers; tone per overlay; sending behavior per overlay (typically `draft_for_review` for human send; overlay may permit auto-send to internal approvers).
5. **Track.** On each approver's decision, record in the audit log. Cumulative status computed.
6. **SLA screen.** Daily sweep for approvals past SLA; route escalation per overlay.
7. **Final outcome.** On approval completion, release the gated action in the originating workflow. On denial, update `ApprovalRequest` status and notify the opener.
8. **Audit log append.** Every transition writes one entry.
9. **Confidence banner.** Overlay `as_of_date` and `status` surfaced.

## Metrics used

`approval_response_time_tpm` (where applicable). Generic response time metrics derived from the audit log.

## Reference files used

- `reference/normalized/approval_threshold_defaults.csv`
- `reference/normalized/approval_routing_policy__{org}.yaml`
- `reference/derived/approval_audit_log.jsonl` (writes)

## Escalation points

- Approval SLA breach: next-level approver per overlay; if still stalled, executive escalation.

## Required approvals

None for the routing itself. The workflow is the routing layer.

## Failure modes

1. Routing without overlay. Fix: org routing overlay required.
2. Missing audit log entry. Fix: every transition writes one.
3. Auto-sending external notifications without overlay permission. Fix: default to `draft_for_review`.
4. Releasing gated action before final approval. Fix: final outcome gate explicit.
5. Losing artifacts between steps. Fix: packet is a bundle, not a reference chain.

## Edge cases

- **Approver on vacation / unavailable:** overlay designates alternate; routing skips to next per overlay policy.
- **Conditional approvals (e.g., approved pending clarification):** request remains open with the condition; condition-close step required.
- **Parallel approvers (any-of vs. all-of):** overlay governs; matrix row default applies.
- **Retroactive approval attempt:** the workflow refuses; retroactive approval is not a valid state.
- **Amended request mid-review:** amendment creates new request linked to prior; approvers re-acknowledge.

## Example invocations

1. "Route this capex award for Ashford Park roof replacement."
2. "Status update on all open row 14 approvals for the South End portfolio."
3. "Renewal concession above policy for 3 leases at Willow Creek — route."

## Example outputs

### Output — Routing plan (abridged)

**Request.** Row 9 bid award for Ashford Park roof replacement.

**Approvers.** Construction_manager -> asset_manager (minimum per matrix + overlay).

**Packet.** Level sheet, recommended award memo, scope clarification closure status, vendor verification status.

**Notifications.** Draft messages produced; `draft_for_review`; overlay permits auto-send to internal approvers on PM confirmation.

**SLA.** Overlay-defined window.

**Audit log.** Opened-entry appended.

**Confidence banner.** `approval_routing_policy__{org}@2026-03-31, status=starter`. `approval_threshold_defaults@2026-03-31, status=starter`.
