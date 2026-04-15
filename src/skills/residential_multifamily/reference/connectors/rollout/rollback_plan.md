# Rollback Plan

status_tag: reference

Per-wave rollback protocol for the integration layer.

## Rollback principles

1. Raw files are immutable. Never delete raw files to "clean up" after a rollback. They document what was received; reprocessing goes through normalization, not through the raw layer.
2. Normalized files are re-derivable. A rollback can delete or supersede normalized files as long as the originating raw files remain and the mapping is correct.
3. Derived files can be re-computed. Rollbacks restore prior derived snapshots and then recompute as the inputs stabilize.
4. Approvals are append-only. A rollback never deletes an `approval_audit_log.jsonl` entry; it opens a new entry describing the rollback.
5. Rollbacks are announced, not hidden. Affected audiences receive explicit notification.

## Wave-specific rollback

### Wave 0 rollback

Affected assets: `source_registry/source_registry.yaml` entries, `master_data/` crosswalks.

Rollback steps:

1. Revert disputed registry entries to `status: planned` or remove them if they were never committed upstream.
2. Restore crosswalk snapshots to the pre-Wave-0 state.
3. Re-run `tests/test_boundary_rules.py`, `tests/test_connector_contracts.py`, and any planned master-data tests.
4. Notify `asset_mgmt`, `finance_reporting`, and `compliance_risk`.
5. Log per `_core/change_log_conventions.md`.

### Wave 1 rollback

Affected assets: pms, gl, market_data source status, normalized outputs, Wave-1 workflow activation.

Rollback steps:

1. Transition affected sources from `status: active` to `status: stubbed`. Do not retire them.
2. Hold new landings. The adapter may continue pulling; the integration layer stops promoting to normalized until the issue is resolved.
3. Restore `reference/normalized/` snapshots for the affected entities. Raw files remain in place.
4. Recompute derived benchmarks based on the restored normalized state.
5. Flag Wave-1 workflows as degraded. Consumers are notified via the primary consumer audience channel per `../monitoring/alert_channel_design.md`.
6. `finance_reporting` and `asset_mgmt` sign off on the rollback scope.
7. Log per `_core/change_log_conventions.md`.

### Wave 2 rollback

Affected assets: ap, crm, hr_payroll source status.

Rollback steps mirror Wave 1. Additional considerations:

- hr_payroll rollback requires `compliance_risk` sign-off because PII sensitivity is high.
- crm rollback may impact fair-housing-sensitive leasing-funnel data; if so, also trigger `../runbooks/fair_housing_sensitive_flag.md` containment protocol.

### Wave 3 rollback

Affected assets: construction, manual_uploads source status; construction workflows (`draw_package_review`, `change_order_review`, etc.).

Rollback steps mirror Wave 1. Additional considerations:

- Any in-flight `ApprovalRequest` for draw or bid award is paused; approvers notified.
- Lien-waiver attestations remain valid; the rollback does not invalidate legal documents. Only the automation state rolls back.
- Construction-specific reconciliation (commitment + CO + draw) is rerun after rollback stabilization.

### Wave 4 rollback

Affected assets: full workflow activation; executive and owner reporting; monitoring dashboards.

Rollback steps:

1. Revert to the partial activation state of the prior stable wave. Workflows outside the prior wave's scope are flagged degraded.
2. Pause executive and owner reporting for the affected scope.
3. Monitor exception volume, workflow activation rate, and SLO bands for a stability window before considering re-expansion.
4. `executive` sign-off required; a Wave-4 rollback is visible to the top of the organization.
5. Log per `_core/change_log_conventions.md`.

## Rollback triggers

A rollback is triggered (not just considered) when any of the following conditions hold:

- Two consecutive reconciliation cycles fail blockers on sources activated in the wave.
- A fair-housing-sensitive incident surfaced during the wave and containment was required.
- A legal-sensitive leak surfaced during the wave.
- An approval-gate breach attempt occurred that was not contained by the canonical controls (should not happen; if it does, the rollback is immediate).
- SLO bands breach "at risk" in multiple categories simultaneously within the wave's scope.
- The wave's primary consumer audience formally declines the wave's outputs due to confidence or accuracy concerns.

## Rollback communication

1. Announce the rollback to affected audiences through the appropriate channel per `../monitoring/alert_channel_design.md`.
2. Include: what rolled back, why, how long the rollback is expected to hold, what workflows are degraded, and who to contact for immediate questions.
3. Do not dilute the message. The audience needs an accurate picture, not reassurance.
4. Follow up with a written retro within the cadence in `post_launch_monitoring_cadence.md`.

## Rollback-recovery path

A rolled-back wave returns to activated state only when:

- The root cause is identified and fixed.
- The fix has been validated against the same pilot properties that originally validated the wave.
- Consumer audiences have re-signed-off.
- The next go-live checklist is executed freshly, not simply "continued from where we left off."

## Non-rollback alternatives

Before a full rollback, consider:

- **Partial degradation**: flag only the affected subset of sources or workflows as degraded, not the entire wave. Use when the issue is scoped.
- **Tolerance tightening**: if the issue is a reconciliation tolerance mismatch, adjust the tolerance (with approval) rather than rolling back the whole wave.
- **Override with full audit**: apply a mapping override per `../runbooks/manual_override_approval.md` if the issue is a narrow edge case. Never use override as a substitute for fixing a structural problem.

## Do-not-rollback cases

- Fair-housing and legal-sensitive incidents do not roll back; they contain and escalate per their runbooks. Rolling back discards audit evidence.
- Approval-audit-log entries do not roll back; the log is append-only.
- Source registry entries in `status: deprecated` after a completed deprecation do not revert automatically; a reverse deprecation requires `executive` approval and a new registry entry.

## Post-rollback review

Every rollback produces:

- A retro attended by `on_call_ops`, `data_owner`, `business_owner`, primary consumer audience, `finance_reporting`, and the responsible technical role.
- A written post-mortem logged per `_core/change_log_conventions.md`.
- A corrective-action list with owners and target dates.
- An update to runbooks, monitoring, or rollout documentation where the rollback revealed a gap.
