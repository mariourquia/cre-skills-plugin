# Runbook: Manual Override Approval

status_tag: reference

A human override of an auto-resolution (property mapping, vendor dedup, account mapping, enum decision, or approval decision) needs to be proposed, approved, and logged.

## 1. Trigger

- Exception of category `mapping_override_pending` or `approval_override_pending` in the queue.
- Auto-resolution produced an output a human disagrees with and wants to supersede.
- A one-time-only exception to a contract (for example, accept a record with a missing optional field that the current mapping rejects, or map an unmapped account to a canonical account temporarily while a permanent crosswalk update is drafted).

## 2. Symptoms

- A proposed override is drafted in the mapping override log (schema: `_core/mapping_override_log.schema.yaml`, planned).
- The affected workflow is held pending resolution.
- An `ApprovalRequest` is referenced but not yet approved.

## 3. Likely causes (ranked)

1. Legitimate edge case the canonical contract does not yet cover.
2. Short-term expedient while a permanent fix is in flight (crosswalk update, schema fix).
3. Business-decision override that legitimately supersedes the default (for example, an asset transfer that changes ownership mid-cycle).
4. Incorrect override proposed, reviewer must reject.
5. Repeated override pattern that signals the contract should be updated rather than overridden.

## 4. Immediate actions (minute-by-minute, numbered)

1. Validate the override request. Required fields: `override_type`, `target_object_type`, `target_object_id`, `justification`, `effective_start`, `effective_end`, `proposed_by`, `approver_audience`.
2. Confirm the override does not cross an approval floor in `_core/approval_matrix.md`. If it does, the action is gated and requires an `ApprovalRequest` matched to the gate (not just a mapping-override log entry). Common gates to check:
   - Row 13: lease deviation, concession above policy, non-standard payment plan.
   - Row 8: contract award above procurement threshold.
   - Row 10 or 11: change order above threshold.
   - Row 20: ontology, canonical metric, alias registry, routing core change.
3. Route to the approver(s). Approvers are defined by the override's `approver_audience`, one or more of the 8 canonical audiences plus functional roles (`legal_counsel`, `compliance_officer`).
4. Require an effective-window. Overrides never run open-ended; `effective_end` is mandatory, even if far in the future. A planned permanent fix should have a short window and cite the permanent-fix ticket.
5. Require a rollback plan. The override entry must describe how to revert: what prior value to restore, what recompute is needed, what consumers to notify.
6. Apply the override only after the approval lands. Emit a `manual_override_applied` event (see `../monitoring/observability_events.yaml`) with the full override payload (minus any sensitive data).
7. Log the override to `mapping_override_log` (or the analogous log for the affected domain). Tests (`tests/test_mapping_override_log.py`, planned) enforce log consistency.
8. Set a reminder to review the override at the effective-end date; if the override is about to expire without a permanent fix, either renew (with a new approval) or let it expire and handle fallout.

## 5. Escalation path

- Proposer: the role that identified the exception (often `data_owner` or `on_call_ops`).
- Reviewer: the canonical audience relevant to the override type:
  - property_mapping override: `asset_mgmt` and `regional_ops`.
  - vendor_dedup override: `finance_reporting` and `construction` (if capex) or `regional_ops` (if operational).
  - account_mapping override: `finance_reporting`.
  - enum_mapping override: `data_owner` of the affected source.
  - approval_override: the approvers listed in the matching `approval_matrix.md` row.
- `compliance_risk` reviews any override touching regulatory-program data or fair-housing-sensitive fields.
- `legal_counsel` reviews any override that could affect contractual or legal obligations (leases, vendor agreements, draw requests).

## 6. Affected workflows

Depends on the override type. Examples:

- Property mapping override: every property-scoped workflow.
- Vendor dedup override: `bid_leveling_procurement_review`, `vendor_dispatch_sla_review`, ap-driven slices of `monthly_property_operating_review`.
- Account mapping override: every gl-consuming workflow.
- Approval override: the workflow the approval was gating.

## 7. Recovery steps

- When the permanent fix lands (crosswalk update, schema fix, contract revision), the override is superseded. Retire the override by recording its end in the log and removing its runtime effect.
- For rejected overrides, the log retains the rejection reason. The original exception remains open and the fix must come through another path.
- For expired overrides, the system reverts to the canonical behavior automatically; if doing so causes a regression, reopen the exception and re-apply via a new override request.

## 8. Verification steps

- Mapping override log has a complete entry with all required fields.
- Approval artifact exists and matches.
- Observability event `manual_override_applied` was emitted.
- Affected workflow runs cleanly after the override is applied.
- No downstream test (`tests/test_mapping_override_log.py`, `tests/test_connector_contracts.py`, `tests/test_boundary_rules.py`) flags drift.

## 9. Post-incident review hooks

- `finance_reporting` and `asset_mgmt` review open overrides monthly; overrides approaching their effective-end are promoted for resolution.
- Chronic override patterns (same type, same target class) prompt a contract-update review; the correct fix is usually to extend the canonical contract, not to keep overriding.
- Any override that touched fair-housing-sensitive or legal-sensitive fields also feeds the next `compliance_risk` review.
- Approval-override artifacts are retained per the retention period declared in `overlays/org/<org_id>/approval_matrix.yaml` (or the canonical default if none is set).
