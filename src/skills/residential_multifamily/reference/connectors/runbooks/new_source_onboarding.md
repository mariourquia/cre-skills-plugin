# Runbook: New Source Onboarding

status_tag: reference

Covers bringing a new upstream source system into the subsystem: discovery through go-live. Applies to any domain (pms, gl, crm, ap, market_data, construction, hr_payroll, manual_uploads).

## 1. Trigger

- An operator, overlay sign-off, or org tailoring interview has declared a new inbound source.
- The source is not yet listed in `source_registry/source_registry.yaml`.
- A `planned` record will be inserted as the first concrete step.

Common triggers:

- New fund or portfolio onboarding introduces a previously absent domain.
- An existing operator migrates from a spreadsheet process to a system feed.
- A regulatory overlay requires a dedicated compliance-intake source.
- A market data or reference benchmark provider is added.

## 2. Symptoms

- Tailoring session writes a new row into `tailoring/missing_docs_queue.yaml` or `tailoring/sign_off_queue.yaml` naming an unrecognized source.
- Executive or `finance_reporting` audience asks for a metric that the subsystem cannot currently activate because the minimum viable data package is incomplete (see `../rollout/minimum_viable_data.md`).
- Reconciliation report shows orphan records whose `source_name` does not resolve to a registry entry.

## 3. Likely causes (ranked)

1. Legitimate new source declared through tailoring or sign-off.
2. New source declared informally (email, meeting) without flowing through tailoring, root cause is missing intake governance.
3. An existing source renamed but the registry was not updated, this is actually `source_schema_change.md`, not this runbook.
4. Test artifact or development fixture leaking a `source_name` that does not belong in production, treat as data leak, not onboarding.

## 4. Immediate actions (minute-by-minute, numbered)

1. Confirm the source is net-new. Grep `source_registry.yaml` for every plausible `source_id` and any vendor-family hint. If an existing entry matches, stop and switch to the appropriate runbook (`source_schema_change.md`, `cutover_manual_to_system.md`, or `connector_deprecation.md`).
2. Identify the owning domain (pms, gl, crm, ap, market_data, construction, hr_payroll, manual_uploads). If it does not fit an existing domain, halt and escalate, a new domain is a subsystem-wide change, not a connector onboarding.
3. Draft a `planned` entry in `source_registry.yaml` using `source_registry.schema.yaml`. Fill all required fields: `source_id`, `source_name`, `source_domain`, `vendor_family`, `ingestion_mode`, `environment`, `cadence`, `data_owner`, `business_owner`, `technical_owner`, `credential_method`, `object_coverage`, `expected_latency_minutes`, `pii_classification`, `financial_sensitivity`, `legal_sensitivity`, `status: planned`, `rollout_wave`.
4. Confirm the owning domain's connector exists under `../../<domain>/`. If the connector does not yet exist (hr_payroll, manual_uploads), escalate; this runbook cannot proceed until the connector contract is authored.
5. Acquire a sanitized sample of the source output. Land it under `reference/raw/<domain>/_samples/<source>__<as_of>.jsonl` tagged with `status_tag: sample`. Confirm all required provenance fields are present per `INGESTION.md`.
6. Author (or extend) `mapping.yaml` in the connector directory to cover every raw field in the sample. Any source field without a canonical target is marked `optional_source: true` or escalated.
7. Author or extend domain reconciliation checks in `reconciliation_checks.yaml`, referencing the shared checks under `qa/`.
8. Kick off a pilot load into `reference/normalized/<entity>__<scope>.csv` in a non-production environment. Capture the `reconciliation_report.json`.
9. Review blocker failures. Resolve or escalate each. Warnings are triaged per `exception_queue_review.md`.
10. Transition `status: planned` to `status: stubbed` in the registry once the sample passes the connector's reconciliation checks.
11. Stand up the live adapter (out-of-scope artifact, owned by `technical_owner`). Land at least one production file; re-run reconciliation.
12. Transition `status: stubbed` to `status: active` once the initial reconciliation window passes. Set `last_validated_at`.
13. Update `../rollout/go_live_checklist.md` items that reference this source.

## 5. Escalation path

- `data_owner` and `technical_owner` named on the registry entry own the work.
- `business_owner` approves the use case.
- For a new domain (not just a new source), escalate to `executive` and `finance_reporting` audiences; a new domain changes the subsystem scope and may require an overlay sign-off.
- For sources with `pii_classification: restricted` or `legal_sensitivity: restricted` or `legal_sensitivity: high`, loop in `compliance_risk` before the stubbed-to-active transition.
- For sources feeding regulatory-program workflows, loop in `compliance_risk` at step 3.

## 6. Affected workflows

Onboarding a source touches every workflow that depends on that domain. Reference the machine-readable `../_core/workflow_activation_map.yaml` (planned) for the full dependency set. Typical activation deltas:

- pms source: `monthly_property_operating_review`, `lead_to_lease_funnel_review`, `move_in_administration`, `move_out_administration`, `renewal_retention`, `delinquency_collections`, `work_order_triage`, `unit_turn_make_ready`, `vendor_dispatch_sla_review`.
- gl source: `budget_build`, `reforecast`, `monthly_property_operating_review`, `monthly_asset_management_review`, `executive_operating_summary_generation`, `quarterly_portfolio_review`.
- crm source: `lead_to_lease_funnel_review`.
- ap source: `delinquency_collections` (vendor side), `bid_leveling_procurement_review`, `vendor_dispatch_sla_review`.
- market_data source: `market_rent_refresh`, `rent_comp_intake`.
- construction source: `capex_estimate_generation`, `bid_leveling_procurement_review`, `change_order_review`, `draw_package_review`, `construction_meeting_prep_and_action_tracking`, `cost_to_complete_review`, `schedule_risk_review`, `capital_project_intake_and_prioritization`.
- hr_payroll source: `third_party_manager_scorecard_review`, staffing sections of `monthly_property_operating_review`.
- manual_uploads source: may feed any of the above depending on `object_coverage`.

## 7. Recovery steps

- If onboarding is aborted mid-flight, leave the registry entry at `status: planned` with a `notes` explanation. Do not delete; the record documents the decision.
- Remove any sanitized samples from `reference/raw/<domain>/_samples/` if they are no longer needed, but never remove them while any normalized record still cites them.
- Re-run the subsystem-wide `tests/test_connector_contracts.py` to confirm no contract drift was introduced.

## 8. Verification steps

- `source_registry.yaml` carries the new entry; `tests/test_source_registry.py` (planned) passes.
- Sample file passes all connector reconciliation checks.
- Normalized output for the sample exists and is queryable.
- At least one downstream workflow activation map recomputes correctly (spot-check via `workflow_activation_map.yaml`).
- For a production cutover, the first scheduled landing in production passes reconciliation and the registry flips to `status: active`.

## 9. Post-incident review hooks

- An onboarding event is logged to the subsystem change log per `_core/change_log_conventions.md`.
- The `data_owner` reviews the first thirty days of reconciliation reports and summarizes to `finance_reporting` and, for regulated sources, `compliance_risk`.
- Cadence: the `executive` monthly operations review includes any source that transitioned state in the prior month.
- Recurring onboarding failures (e.g., same step fails across multiple sources) feed a quarterly retrospective on intake governance.
