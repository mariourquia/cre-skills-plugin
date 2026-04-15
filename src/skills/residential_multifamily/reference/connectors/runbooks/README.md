# Runbooks, Integration Layer Operations

status_tag: reference

Operational playbooks for the integration layer of the residential multifamily subsystem. Each runbook assumes the reader is the current on-call operator, familiar with `INGESTION.md`, `source_registry/`, `qa/`, and `_core/exception_taxonomy.md` (planned file referenced from `_core/README.md`).

## How these runbooks fit together

- A monitoring alert (see `../monitoring/alert_policies.yaml`) fires.
- The alert carries an `alert_id`, an `exception_taxonomy` category, a severity, and a default routing audience (from `../monitoring/exception_routing.yaml`).
- The alert references a `related_runbook` by filename. The on-call opens that runbook and follows it top to bottom.
- The runbook cites workflow slugs from `../../workflows/` (all 27 are canonical) and audience slugs from `../../tailoring/AUDIENCE_MAP.md` (8 audiences).
- Approval-gated actions never bypass `_core/approval_matrix.md`. If a runbook step crosses an approval floor it halts and opens an `ApprovalRequest`.

## Canonical structure

Every runbook in this directory has the following nine sections:

1. Trigger
2. Symptoms
3. Likely causes (ranked)
4. Immediate actions (minute-by-minute, numbered)
5. Escalation path
6. Affected workflows
7. Recovery steps
8. Verification steps
9. Post-incident review hooks

Deviations fail `tests/test_runbook_structure.py` (planned; tracked in the subsystem test harness).

## Runbook index

| # | File | Purpose |
|---|---|---|
| 1 | `new_source_onboarding.md` | Bring a new source system into the subsystem: discovery, contract, sample, mapping, dq, pilot, go-live gate, registry update. |
| 2 | `source_schema_change.md` | Vendor adds, renames, or removes a field: detection, impact, decide to tolerate, remap, or escalate. |
| 3 | `missing_file_handling.md` | Expected file did not arrive: cadence check, contact, stale-feed escalation, fallback, backfill. |
| 4 | `stale_feed_handling.md` | File arrived on cadence but `as_of` is stale: diagnosis, confidence downgrade, communication. |
| 5 | `property_crosswalk_issue.md` | Unrecognized property code, duplicate, or rename: crosswalk resolution with survivorship rule. |
| 6 | `unmapped_account_handling.md` | GL account not in `account_crosswalk.yaml`: unmapped bucket, approval, re-ingest. |
| 7 | `benchmark_refresh.md` | Periodic refresh of rent, concession, payroll, labor, materials, utility, vendor, capex, schedule benchmarks. |
| 8 | `failed_normalization_triage.md` | Normalization job fails loudly: log inspection, contract validation, mapping check, retry policy. |
| 9 | `exception_queue_review.md` | Daily / weekly queue review: triage, assign owner, dwell-time SLA, closeout. |
| 10 | `manual_override_approval.md` | Human override of auto-resolution: request, approver, justification, effective window, rollback. |
| 11 | `cutover_manual_to_system.md` | Move a feed from manual drop to direct integration: parallel run, reconciliation, cutover gate. |
| 12 | `connector_deprecation.md` | Sunset a connector: announcement, replacement, dual-run, cutoff, archive retention. |
| 13 | `fair_housing_sensitive_flag.md` | Fair-housing-sensitive exception: containment, halt dependent workflows, legal escalation, audit log. |
| 14 | `financial_control_gate_breach.md` | Automation about to act beyond approval floor: halt, open ApprovalRequest, notify approvers. |
| 15 | `schema_drift_escalation.md` | Upstream schema changes break downstream workflow: detection, mitigation, degraded-mode operation. |
| 16 | `reference_rollback.md` | Roll back a bad benchmark / reference update: identify, restore prior, re-publish, change log, notify. |

## Cross-references to the exception taxonomy

Each runbook is triggered by one or more categories in `_core/exception_taxonomy.md` (planned). The mapping:

| Exception category | Runbooks |
|---|---|
| `dq_blocker` | `failed_normalization_triage.md`, `exception_queue_review.md` |
| `dq_warning` | `exception_queue_review.md` |
| `reconciliation_mismatch` | `failed_normalization_triage.md`, `exception_queue_review.md` |
| `identity_unresolved` | `property_crosswalk_issue.md`, `unmapped_account_handling.md` |
| `schema_drift` | `source_schema_change.md`, `schema_drift_escalation.md` |
| `stale_source` | `missing_file_handling.md`, `stale_feed_handling.md` |
| `mapping_override_pending` | `manual_override_approval.md` |
| `approval_override_pending` | `manual_override_approval.md`, `financial_control_gate_breach.md` |
| `manual_correction_required` | `exception_queue_review.md`, `manual_override_approval.md` |
| `policy_violation` | `financial_control_gate_breach.md` |
| `fair_housing_sensitive` | `fair_housing_sensitive_flag.md` |
| `legal_sensitive` | `fair_housing_sensitive_flag.md`, `financial_control_gate_breach.md` |

## Escalation audiences

All runbooks reference the 8 canonical audience slugs in `tailoring/AUDIENCE_MAP.md`:

- `executive`
- `regional_ops`
- `asset_mgmt`
- `finance_reporting`
- `development`
- `construction`
- `compliance_risk`
- `site_ops`

Plus the functional roles on-call operators may route to: `on_call_ops`, `legal_counsel`, `data_platform_team`, `finance_systems_team`, `hr_systems_team`. These are roles, not people.

## Approval floor reminder

A runbook never lowers an approval floor. If a step crosses one of the gated actions in `_core/approval_matrix.md`, the step stops and opens an `ApprovalRequest`. This applies to eviction, concession above policy, vendor award, draw disbursement, final investor submission, policy changes, and the other entries on that list.

## No numbers in prose

Dollar thresholds and percent targets live in `overlays/org/<org_id>/approval_matrix.yaml` and in `reference/derived/`. Runbook prose cites them by name, never by value.
