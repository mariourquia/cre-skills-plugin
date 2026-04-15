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

## Logging

Every gated action attempt produces an entry in the subsystem's `approval_audit_log.jsonl` (schema below), regardless of outcome. Tests verify tail consistency (no dangling `pending`, no actions executed without matching `approved` entry).

```yaml
# approval_audit_log entry shape
timestamp: 2026-04-15T14:23:05Z
action_id: <ulid>
subject_object_type: <see approval_request schema>
subject_object_id: <string>
actor: <agent or human id>
gate_category: <row # from table above>
outcome: [opened | approved | denied | executed | cancelled | expired]
approval_request_id: <ulid>
notes: <optional>
```
