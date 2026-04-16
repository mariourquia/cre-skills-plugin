# Runbook: Missing File Handling

status_tag: reference

An expected manual or scheduled file did not arrive within its cadence window.

## 1. Trigger

- Monitoring alert `missing_file_after_cadence` fires for a source in `source_registry.yaml`.
- The alert condition is computed from the source's declared `cadence` and `expected_latency_minutes`.
- Applies to any ingestion mode: `api`, `sftp`, `scheduled_export`, `shared_drive`, `email_drop`, `file_drop`, `manual_upload`.

## 2. Symptoms

- No raw file landed under `reference/raw/<domain>/<YYYY>/<MM>/` within the expected window.
- Reconciliation check `date_coverage` reports a gap relative to the prior period.
- Downstream workflows waiting on the feed either block (for blocking dependencies) or run in degraded mode (for soft dependencies; see `../rollout/minimum_viable_data.md`).
- The registry entry's `last_validated_at` timestamp is older than the cadence would allow.

## 3. Likely causes (ranked)

1. Upstream source system scheduled export did not run (cron misconfiguration, credential expiry, outage).
2. Manual sender forgot or is delayed (holiday, handoff, illness).
3. Transport issue (sftp credentials expired, api token rotated, email intake mailbox full, shared drive quota).
4. File landed but with wrong filename convention; the landing guard rejected it, in that case the file is actually in `_rejected/` and this is a `failed_normalization_triage.md` case.
5. Calendar event (e.g., end-of-quarter close) that legitimately pushes cadence.

## 4. Immediate actions (minute-by-minute, numbered)

1. Confirm the file is genuinely missing. Inspect `reference/raw/<domain>/<YYYY>/<MM>/` and `reference/raw/<domain>/_rejected/<YYYY>/<MM>/`. If rejected, switch to `failed_normalization_triage.md`.
2. Check the registry entry. Note `data_owner`, `business_owner`, `technical_owner`, `ingestion_mode`, `cadence`, `expected_latency_minutes`, and `notes` for known cadence caveats.
3. For `api` or `scheduled_export` sources: ping `technical_owner` to verify the upstream job ran. Check for credential expiry (`credential_method` hints which secret store to query, placeholder only; live secrets live in the operator environment, not this repo).
4. For `sftp`, `email_drop`, `shared_drive`, `manual_upload`: ping `data_owner` and `business_owner`. If the file has a human sender, contact the sender through the operator's normal channel (see `../monitoring/alert_channel_design.md`).
5. Set a dwell-time timer matching the severity in `../monitoring/exception_routing.yaml`. If the timer expires, escalate to the next audience in the escalation chain.
6. For dependent workflows, consult `../rollout/minimum_viable_data.md`. If the workflow can run in manual-files-only mode or with a fallback source, flag the workflow as degraded and communicate to consumers; do not hide the gap.
7. If a regulatory-reporting deadline is impacted, loop in `compliance_risk` immediately, not at the end of the dwell timer.
8. Once the file arrives, execute the backfill plan below.

## 5. Escalation path

- First responder: `on_call_ops`.
- Step one: `data_owner` + `technical_owner` for the source.
- Step two: `business_owner`.
- Step three: the primary consumer audience, typically `finance_reporting` for gl and ap, `asset_mgmt` for pms and construction, `regional_ops` for site-adjacent pms, `compliance_risk` for regulatory intake.
- Step four: `executive` if the miss threatens a board, lender, investor, or regulator deadline.
- Fair-housing-sensitive data never takes the slow path; it escalates directly to `compliance_risk` and `legal_counsel` on first detection.

## 6. Affected workflows

Depends on the source. Consult `workflow_activation_map.yaml` (planned) for the authoritative mapping. Common dependencies:

- Daily gl file missing: `monthly_property_operating_review`, `reforecast`, `budget_build` cannot run in full detail until file arrives.
- Weekly market_data file missing: `market_rent_refresh`, `rent_comp_intake` run against stale comps; confidence downgraded.
- Quarterly manual budget drop missing: `budget_build`, `reforecast`, `quarterly_portfolio_review` blocked for the affected properties.
- Monthly construction file missing: `draw_package_review`, `cost_to_complete_review`, `construction_meeting_prep_and_action_tracking` degrade until arrival.
- hr_payroll file missing: staffing sections of `monthly_property_operating_review` and `third_party_manager_scorecard_review` blank until arrival.

## 7. Recovery steps

- When the file arrives, land it under the normal convention. Do not backdate the filename to paper over the gap, use the actual arrival `as_of`.
- Run normalization and reconciliation. Expect a larger-than-usual record set on the first post-gap landing; `date_coverage` should flip from fail to pass.
- Recompute derived benchmarks that depend on the domain.
- Retrigger any workflow that was blocked or degraded. Confirm it now activates cleanly.
- Update the registry entry's `last_validated_at`.

## 8. Verification steps

- `date_coverage` check passes for the affected entity.
- `record_count` reconciliation is within tolerance.
- Downstream workflow activation returns to non-degraded.
- No residual exception of category `stale_source` remains in the queue for this source.

## 9. Post-incident review hooks

- Log the miss to the source's incident history (tracked in the registry's `notes` or an adjacent incident log, depending on the operator's tooling).
- If the miss is recurring for this source (same sender, same interval), escalate to `../monitoring/slo_definitions.md` as a chronic-miss pattern and consider moving the source up the `cutover_manual_to_system.md` priority list.
- `executive` monthly operations review includes any source that missed cadence in the prior month with a qualitative status band.
- For a miss that caused a regulatory deadline impact, `compliance_risk` owns the corrective-action summary and files it per the regulatory overlay's documentation requirements.
