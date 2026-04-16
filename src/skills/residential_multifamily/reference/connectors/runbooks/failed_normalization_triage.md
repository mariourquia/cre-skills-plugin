# Runbook: Failed Normalization Triage

status_tag: reference

A normalization job failed loudly. Land-to-normalized promotion did not complete; downstream workflows are blocked.

## 1. Trigger

- Monitoring alert `normalization_failed` fires.
- An observability event of type `normalization_failed` is emitted (see `../monitoring/observability_events.yaml`).
- A scheduled normalization run exits non-zero; the raw landing remains in `reference/raw/<domain>/<YYYY>/<MM>/` but no corresponding entry appears in `reference/normalized/`.

## 2. Symptoms

- `reference/normalized/<entity>__<scope>.csv` was not updated for the expected window.
- `reconciliation_report.json` is missing or shows a `fail` status across multiple checks of severity blocker.
- Workflows that depend on the domain sit in `workflow_blocked` status.
- Exception queue fills with `dq_blocker` entries tagged to the affected domain.

## 3. Likely causes (ranked)

1. Schema drift that the adapter did not tolerate, handle under `source_schema_change.md`.
2. Identity-resolution failure (property, account, or vendor crosswalk missing), handle under `property_crosswalk_issue.md`, `unmapped_account_handling.md`, or the vendor-dedup path in the ap connector.
3. Mapping gap (unmapped enum, unit mismatch, null in a critical field the mapping assumed present).
4. Provenance failure (required provenance field missing on incoming rows; rejected at landing).
5. Adapter-side bug or partial outage.
6. Resource exhaustion (disk full, rate limit, timeout).

## 4. Immediate actions (minute-by-minute, numbered)

1. Pull the failing job's log and stack. Identify the first failed step: landing guard, provenance validation, contract validation, mapping, identity resolution, dedup, reconciliation.
2. If the job failed at the landing guard or provenance validation, the file is already in `reference/raw/<domain>/_rejected/<YYYY>/<MM>/`. Read the rejection reason and jump to the specialized runbook.
3. If the job failed at contract validation, confirm whether `schema.yaml` for the connector matches the incoming shape. If the shapes differ, switch to `source_schema_change.md`.
4. If the job failed at mapping, confirm `mapping.yaml` covers every raw field. Unmapped enums or missing transforms block the job. Apply the mapping fix per the schema-change playbook.
5. If the job failed at identity resolution, switch to `property_crosswalk_issue.md` (property-level) or `unmapped_account_handling.md` (gl). Vendor-dedup failures are handled inline under the ap connector's dedup rules.
6. If the job failed at dedup with `reject_on_conflict`, the source sent two records with the same primary key and a tie-breaker cannot choose, escalate to `data_owner` for the source to determine which record is authoritative.
7. If the job failed at reconciliation with a blocker, the landing is not promoted. Review the blocker check name, load the corresponding runbook or qa check definition under `../qa/`, and execute the remediation.
8. If the job partially succeeded (some entities promoted, others not), confirm the mapping's entity-level transactional boundary. The default is all-or-nothing per landing; check for operator overrides that allow partial success. If partial success is allowed, mark the failed entities only.
9. Retry the job. Connector tests, then a clean normalization pass, then reconciliation.
10. If retry still fails, quarantine the landing and escalate to `technical_owner` for an adapter-side fix.

## 5. Escalation path

- First responder: `on_call_ops`.
- `technical_owner` for adapter-side failures.
- `data_owner` for upstream content issues.
- `business_owner` for use-case-impacting decisions (hold vs proceed with known gap).
- Primary consumer audience (`finance_reporting`, `asset_mgmt`, `regional_ops`, `construction`, `compliance_risk`, or `site_ops`) for workflow prioritization when multiple teams are blocked.
- `compliance_risk` if a regulatory reporting deadline is at risk.
- `legal_counsel` for any rejection that exposes fair-housing-sensitive or legal-sensitive data (rare but not impossible).

## 6. Affected workflows

All workflows whose required inputs sit behind the failed normalization. The activation map (`../_core/workflow_activation_map.yaml`, planned) returns the authoritative list. Typical:

- pms failure: `monthly_property_operating_review`, `delinquency_collections`, `lead_to_lease_funnel_review`, `move_in_administration`, `move_out_administration`, `renewal_retention`, `unit_turn_make_ready`, `work_order_triage`, `vendor_dispatch_sla_review`.
- gl failure: `monthly_property_operating_review`, `monthly_asset_management_review`, `executive_operating_summary_generation`, `quarterly_portfolio_review`, `budget_build`, `reforecast`.
- construction failure: `draw_package_review`, `cost_to_complete_review`, `change_order_review`, `construction_meeting_prep_and_action_tracking`, `schedule_risk_review`, `capital_project_intake_and_prioritization`, `bid_leveling_procurement_review`, `capex_estimate_generation`.

## 7. Recovery steps

- Apply the root-cause fix (mapping, crosswalk, adapter patch, upstream correction).
- Replay the affected raw landing through normalization.
- Confirm reconciliation passes.
- Backfill any missed reconciliation windows.
- Clear the `workflow_blocked` flag and notify consumers.
- Record the incident in the subsystem change log per `_core/change_log_conventions.md`.

## 8. Verification steps

- `normalization_succeeded` event emitted for the affected window.
- Reconciliation blockers all green.
- Downstream workflow activation map recomputes; blocked workflows activate.
- Exception queue drains the relevant `dq_blocker` entries.
- No residual records in `reference/raw/<domain>/_rejected/` pending reprocessing.

## 9. Post-incident review hooks

- Log the incident in `_core/change_log_conventions.md` format.
- `data_owner` writes a brief root-cause note for the source's incident history.
- Recurring failures of the same type (same entity, same check) feed a quarterly adapter-reliability review.
- SLO impact logged to `../monitoring/slo_definitions.md` tracking.
- For any failure that touched fair-housing-sensitive fields (screening, demographic proxies), route to `fair_housing_sensitive_flag.md` for additional review.
