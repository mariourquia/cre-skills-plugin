# Runbook: Exception Queue Review

status_tag: reference

The daily and weekly review cycle for the integration-layer exception queue.

## 1. Trigger

- Daily review: a scheduled calendar event at the start of each business day.
- Weekly review: a scheduled calendar event at the start of each business week.
- Ad hoc: when an alert routed to the queue indicates a dwell-time SLA is about to expire.

## 2. Symptoms

- Non-empty exception queue. Every connector emits exceptions of the categories enumerated in `_core/exception_taxonomy.md` (planned): `dq_blocker`, `dq_warning`, `reconciliation_mismatch`, `identity_unresolved`, `schema_drift`, `stale_source`, `mapping_override_pending`, `approval_override_pending`, `manual_correction_required`, `policy_violation`, `fair_housing_sensitive`, `legal_sensitive`.
- Items in the queue either carry an owner or are unassigned.
- Aging items (dwell-time exceeded) carry an escalation flag.

## 3. Likely causes (ranked)

1. Normal operational volume, connectors are emitting exceptions at their steady-state rate and the queue needs routine triage.
2. Incident cluster, a single upstream event produced many exceptions simultaneously (handle via the originating incident's runbook).
3. Volume spike from a benchmark refresh or cutover.
4. Queue neglect, the queue was not reviewed in a prior cycle and aging items require prioritized closeout.

## 4. Immediate actions (minute-by-minute, numbered)

1. Open the queue. Filter to "open" or "in progress" items.
2. For each item, confirm severity: `info`, `warning`, or `critical`. Severity is set by the alert policy in `../monitoring/alert_policies.yaml`; reviewers may raise severity but never lower it without the source alert policy's review.
3. For each item, confirm routing audience: one of the 8 canonical audiences from `tailoring/AUDIENCE_MAP.md` plus on-call functional roles. Routing is set by `../monitoring/exception_routing.yaml`.
4. Assign an owner for every item that does not yet have one. Owner is a named role (for example, `data_owner` for the source, `compliance_officer` for regulatory exceptions), not a person.
5. Check dwell time. Any item whose dwell time exceeds the SLA in `exception_routing.yaml` is escalated one level up the chain immediately.
6. Triage:
   - `dq_blocker`: switch to `failed_normalization_triage.md` if not already active.
   - `dq_warning`: schedule a fix by end-of-week; log in the queue.
   - `reconciliation_mismatch`: switch to the specific qa check's remediation runbook (see `../qa/`).
   - `identity_unresolved`: switch to `property_crosswalk_issue.md` or `unmapped_account_handling.md`.
   - `schema_drift`: switch to `source_schema_change.md`.
   - `stale_source`: switch to `missing_file_handling.md` or `stale_feed_handling.md`.
   - `mapping_override_pending`: switch to `manual_override_approval.md`.
   - `approval_override_pending`: confirm an `ApprovalRequest` exists; if not, open one per `_core/approval_matrix.md`.
   - `manual_correction_required`: coordinate with the upstream `data_owner` for the source.
   - `policy_violation`: switch to `financial_control_gate_breach.md`.
   - `fair_housing_sensitive` or `legal_sensitive`: switch to `fair_housing_sensitive_flag.md` immediately, regardless of dwell time.
7. Close items whose remediation is complete. A closeout requires: remediation documented, verification complete, root-cause tagged.
8. Summarize the queue's current state: open count by severity, aging items, new items since last review.

## 5. Escalation path

- Daily review is run by `on_call_ops`.
- Weekly review is owned by the integration-layer operations lead and attended by at least one representative from `finance_reporting`, `asset_mgmt`, and `regional_ops`.
- `compliance_risk` attends weekly when any fair-housing or regulatory exceptions are in the queue.
- `executive` is briefed monthly with the roll-up (see `../rollout/post_launch_monitoring_cadence.md`).
- Any item aged beyond the next-higher severity's SLA is auto-escalated to that severity's default routing chain.

## 6. Affected workflows

Every workflow indirectly depends on the queue staying bounded. A persistently aging queue signals a systemic data-quality problem that will eventually block:

- `monthly_property_operating_review`
- `monthly_asset_management_review`
- `executive_operating_summary_generation`
- `quarterly_portfolio_review`
- Every workflow that reads from a domain with open `dq_blocker` items.

## 7. Recovery steps

- When queue size or aging counts breach the SLO in `../monitoring/slo_definitions.md`, pause non-essential ingest to stabilize and focus on drain-down.
- If a root cause is detected across many items (schema drift, new account code pattern), apply the root-cause fix once and close the cluster in bulk rather than item-by-item.
- After a spike, document in a weekly readout; if the spike repeats, escalate to a structural review.

## 8. Verification steps

- No item aged beyond its SLA at the end of the review.
- Severity bands reflect current state (nothing silently demoted).
- Closed items carry documented remediation and verification notes.
- Queue metrics feed the weekly readout (open count, closed count, average dwell, max dwell).
- Exception counts by category are persisted to the observability stream per `observability_events.yaml`.

## 9. Post-incident review hooks

- Weekly readout: owner types, volume by category, time-to-close distribution, aging items, incidents opened, incidents closed.
- Monthly roll-up: feed `executive` monthly operations review with qualitative bands.
- Quarterly review: identify chronic sources (same exception repeating) and feed the `cutover_manual_to_system.md` or `connector_deprecation.md` candidacy lists.
- Annual review: the exception taxonomy itself is reviewed for completeness; new categories are added through the subsystem change log per `_core/change_log_conventions.md`.
