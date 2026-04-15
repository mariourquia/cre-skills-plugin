# Example — Owner Approval Routing (abridged)

**Prompt:** "Route this capex award for Ashford Park roof replacement."

**Inputs:** `ApprovalRequest` record (row 9, subject: bid award) + routing policy overlay + approver roster + related artifacts.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- management_mode: third_party_managed
- org_id: {org}
- approval_matrix_row: 9
- role: construction_manager / asset_manager
- output_type: checklist
- decision_severity: action_requires_approval

## Expected packs loaded

- `workflows/owner_approval_routing/`
- Invoked by any workflow that writes an `ApprovalRequest`.

## Expected references

- `reference/normalized/approval_threshold_defaults.csv`
- `reference/normalized/approval_routing_policy__{org}.yaml`
- `reference/derived/approval_audit_log.jsonl` (writes)

## Gates potentially triggered

- This pack is the gate plumbing; it does not itself require approval.

## Expected output shape

- Routing plan with ordered approvers and SLA.
- Approval packet bundle.
- Notification drafts per approver.
- Audit log entry (opened).
- Status updates as decisions arrive.

## Confidence banner pattern

```
References: approval_routing_policy__{org}@2026-03-31 (starter),
approval_threshold_defaults@2026-03-31 (starter).
```
