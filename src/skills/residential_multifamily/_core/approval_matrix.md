# Approval Matrix

The default autonomy policy for this subsystem. Overlays may tighten thresholds (lower dollar limits, add approvers) but may not loosen them below the canonical floor. Organization-specific thresholds live in `overlays/org/<org_id>/approval_matrix.yaml`.

## Autonomy floor (always automated unless overlaid otherwise)

The subsystem may draft, analyze, summarize, monitor, route, and recommend without approval for the following categories:

- Operational dashboards, KPI reviews, variance narratives (marked `informational` or `recommendation`).
- Draft resident communications marked `draft_for_review` (not sent until a human or approved automation routes them).
- Draft vendor communications marked `draft_for_review`.
- Draft owner and LP reporting marked `draft_for_review`.
- Internal task creation, scheduling, and routing.
- Reference-data ingest proposals (proposed status; approval still required before `approved` status).
- Internal meeting prep, agenda creation, and action-item synthesis.

## Gated actions (require an approval_request in approved status)

| # | Action | Minimum approvers | Notes |
|---|---|---|---|
| 1 | Serve a legal notice (pay-or-quit, cure-or-quit, non-renewal of a lease) | property_manager + regional_manager (or overlay-defined owner rep) | Jurisdiction-specific review also required; see guardrails.md. |
| 2 | File for eviction | property_manager + regional_manager + legal counsel sign-off | `legal_flag=true` in `DelinquencyCase`. |
| 3 | Tenant dispute with legal exposure (e.g., fair housing complaint, retaliation claim) | regional_manager + legal counsel | Route to legal, do not draft public-facing response without counsel. |
| 4 | Safety-critical maintenance decision (scope change, life-safety deferral, evacuation) | maintenance_supervisor + property_manager + regional_manager | For life-safety scope defer, add owner rep. |
| 5 | Licensed engineering or code-compliance judgment | licensed engineer or authorized compliance officer | System may summarize, not decide. |
| 6 | Financial disbursement >= $threshold_disbursement_1 but < $threshold_disbursement_2 | property_manager + regional_manager | Default threshold values in `overlays/org/_defaults/thresholds.yaml`. |
| 7 | Financial disbursement >= $threshold_disbursement_2 | property_manager + regional_manager + asset_manager | |
| 8 | Contract award or material procurement >= $threshold_procurement | regional_manager + asset_manager | |
| 9 | Bid award regardless of dollar (for construction or capex) | construction_manager + asset_manager; for >= $threshold_bid_major, add development or executive | |
| 10 | Change order >= $threshold_co_minor | construction_manager + asset_manager | Escalates with dollar size. |
| 11 | Change order >= $threshold_co_major | construction_manager + asset_manager + executive (COO or CEO per overlay) | |
| 12 | Draw request submission | construction_manager + asset_manager | Lender-facing; marked `final`. |
| 13 | Lease deviation, concession > concession_policy_max, non-standard payment plan | property_manager + regional_manager | Fair-housing review required if pattern. |
| 14 | Lender-facing submission marked `final` | asset_manager + finance/reporting lead | |
| 15 | Investor-facing submission marked `final` | asset_manager or portfolio_manager + executive | |
| 16 | Board-, lender-, or investor-facing final report submission | executive + finance/reporting lead | |
| 17 | Any action explicitly marked `human_approval_required` by a policy overlay | per overlay | |
| 18 | Hiring / termination / discipline action at a site | regional_manager + HR | System may prepare; must not decide. |
| 19 | PMA amendment, vendor agreement signature, or any contract binding the owner | asset_manager or portfolio_manager + legal | |
| 20 | Assumption change in ontology, canonical metric contract, alias registry, or routing core | system maintainer + designated reviewer | Handled via change_log_conventions.md. |

## Severity-to-gate mapping (used by the router)

| Decision severity | Routing behavior |
|---|---|
| `informational` | Automated. No gate. |
| `recommendation` | Automated draft. Human reads. No gate unless action is invoked. |
| `action_routable` | Automated execution permitted if all overlays' policies allow. |
| `action_requires_approval` | System must locate an approved `approval_request` linked to the action; otherwise refuse and open a new `ApprovalRequest`. |

## Threshold conventions

All dollar thresholds live in overlays, not in this document. Defaults for a new organization onboarded via the tailoring skill are placed in `overlays/org/<org_id>/approval_matrix.yaml` based on the tailoring interview. A reference defaults file lives at `reference/normalized/approval_threshold_defaults.csv` (status=starter, editable).

## Escalation to executive review

The following automatically escalate to executive review regardless of dollar:

- Any action tagged with `fair_housing_risk` or `policy_discrimination_risk`.
- Any action touching child safety (e.g., lead paint disclosure exceptions, pool safety).
- Any action that would be visible to LPs, lenders, regulators, or the press.
- Any deviation from a policy that has been reviewed by legal within the last 12 months.

## Canonical status vocabulary

The approval lifecycle has exactly ONE canonical vocabulary. Both the
`approval_request.status` field (in `_core/schemas/approval_request.yaml`) and
the audit log `outcome` field use the same enum:

```
pending, approved, approved_with_conditions, denied, expired, withdrawn
```

Legacy vocabulary (`opened`, `executed`, `cancelled`) is retired.

- `opened` was an informal label for newly created requests. It maps to `pending`.
- `executed` was an informal label for "approval has been used to gate an
  action." This is now a distinct log event (see "Execution audit", below)
  and NOT an approval status. An approval_request remains `approved`
  throughout its lifetime; the action it authorizes is logged separately.
- `cancelled` maps to `withdrawn` (the requester abandoned the request).

## Stale-approval guard (subject_object_version_hash)

Approvals are bound to a specific version of the subject artifact via
`subject_object_version_hash` (SHA-256 of the canonical JSON serialization
of the artifact at the time the approval was requested). When a gated
action is executed, the runtime:

1. recomputes the content hash of the artifact referenced by
   `subject_object_type` + `subject_object_id`;
2. compares against the approval_request's `subject_object_version_hash`;
3. refuses the action if they do not match, and opens a new approval_request
   for the new artifact version.

This closes the silent-reuse hole where an artifact (e.g. a change order or
capex project) could be mutated after approval and before execution.

## Logging

Every gated action attempt produces an entry in the subsystem's
`approval_audit_log.jsonl` (schema below), regardless of outcome. Tests
verify tail consistency (no dangling `pending`, no actions executed without
matching `approved` entry whose version hash matches the artifact hash at
execution time).

```yaml
# approval_audit_log entry shape
timestamp: 2026-04-15T14:23:05Z
action_id: <ulid>
event: [request_created | decision_recorded | execution_attempted | execution_completed | request_expired]
subject_object_type: <see approval_request schema>
subject_object_id: <string>
subject_object_version_hash: <sha256 hex digest>   # required on decision_recorded and execution_attempt
actor: <agent or human id>
gate_category: <row # from table above>
approval_request_status: [pending | approved | approved_with_conditions | denied | expired | withdrawn]
approval_request_id: <ulid>
execution_outcome: [authorized | refused_stale_hash | refused_missing_approval | refused_other]  # only on execution_attempt / execution_completed
notes: <optional>
```
