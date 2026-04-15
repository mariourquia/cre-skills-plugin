# Runbook: Cutover, Manual to System

status_tag: reference

Move a data feed from a manual file drop (email, shared drive, spreadsheet) to a direct system integration (api, sftp, scheduled_export).

## 1. Trigger

- Cutover is scheduled based on chronic manual-source incidents, new system availability, or a tailoring session outcome.
- A manual source in `source_registry.yaml` is paired with a replacement `planned` source of a different `ingestion_mode` in the same domain.
- `executive` or `finance_reporting` audience signs off on the cutover as part of a wave-based rollout (see `../rollout/rollout_waves.md`).

## 2. Symptoms

- The manual source has a history of `stale_feed_handling.md` or `missing_file_handling.md` incidents.
- The replacement system has passed new-source onboarding and is in `status: stubbed` or recently transitioned `status: active`.
- Downstream consumers report they need fresher data than manual cadence allows.

## 3. Likely causes (ranked)

1. Operator completed an integration project and the system source is now available.
2. Chronic manual-source incidents crossed a threshold requiring change.
3. Third-party operator or manager migrated to a direct feed.
4. Regulatory-program requirement forced a shift (for example, automated REAC reporting replaces a manual email).
5. Consolidation: two manual sources converge to a single system.

## 4. Immediate actions (minute-by-minute, numbered)

1. Confirm the replacement source is `status: active` with a clean reconciliation history across a full cadence window (for example, one month for daily feeds, one quarter for quarterly feeds).
2. Establish the parallel-run period. Both sources land simultaneously under their respective `source_id` paths. Lengths are overlay-defined; typical bands: short for high-frequency sources, longer for quarterly or annual sources.
3. For every parallel-run period, run a reconciliation diff: for each canonical object, compare the manual and system versions. Track deltas in a cutover comparison log.
4. Classify deltas:
   - Tie (manual and system match): no action.
   - System more complete or fresher: expected; document.
   - Manual more complete or fresher: investigate; the system source may have a gap the manual process covers.
   - Divergent business meaning: halt cutover; the system source is not a like-for-like replacement.
5. Confidence comparison: produce a side-by-side `confidence_band` for each source over the parallel-run window. The system source should reach equal or higher confidence for a sustained window before cutover proceeds.
6. Gate the cutover. Required sign-offs: `data_owner`, `business_owner`, primary consumer audience, and `finance_reporting` if the source feeds finance-adjacent outputs. Regulatory sources also require `compliance_risk`. See `../rollout/cutover_procedures.md` for the general cutover gate.
7. On cutover date, transition the manual source to `status: deprecated`. The system source becomes the primary source for all declared `object_coverage` it covers.
8. Repoint `master_data/` crosswalks that reference the manual source's `source_id` to the system source's `source_id`.
9. Retain a deprecation note on the manual source's registry entry naming the replacement and the cutover date.
10. Decommission the manual landing path (turn off the email intake, close the shared-drive folder, retire the sftp credentials) only after a stability window post-cutover (typically matching the parallel-run length).
11. Update `../rollout/go_live_checklist.md` if the cutover closes a wave milestone.

## 5. Escalation path

- `data_owner` and `business_owner` own the cutover plan.
- `technical_owner` owns adapter readiness for the system source.
- Primary consumer audience (`finance_reporting`, `asset_mgmt`, `regional_ops`, `construction`, `compliance_risk`, `site_ops`) signs off on acceptable confidence and freshness.
- `executive` signs off on cutovers that touch executive-facing reporting.
- `compliance_risk` signs off on regulatory-program cutovers.
- Any blocker discovered during parallel run escalates to halt; cutover does not proceed until resolved.

## 6. Affected workflows

All workflows that read the affected domain. A partial list based on `object_coverage`:

- Manual budget drop to gl cutover: `budget_build`, `reforecast`, `monthly_property_operating_review`, `monthly_asset_management_review`, `quarterly_portfolio_review`.
- Manual operator-portal drop to pms api cutover: `monthly_property_operating_review`, `delinquency_collections`, `renewal_retention`, `lead_to_lease_funnel_review`, `work_order_triage`, `unit_turn_make_ready`.
- Manual utility drop to ap api cutover: `monthly_property_operating_review` utility section.
- Manual COI email to vendor-compliance system cutover: `vendor_dispatch_sla_review` (insurance block), `bid_leveling_procurement_review` (vendor screening).

## 7. Recovery steps

- If the cutover introduces a regression, trigger `schema_drift_escalation.md` or the appropriate runbook for the specific failure. If the regression is severe, roll back to the manual source as the interim primary and reopen the parallel run.
- Backfill any data the system source missed during the initial landing window.
- Recompute derived benchmarks after cutover and confirm no step change.

## 8. Verification steps

- Cutover comparison log shows zero divergent-meaning deltas and confidence at or above the manual baseline for the required stability window.
- The manual source is `deprecated` in the registry.
- Every crosswalk reference to the manual source is repointed.
- Downstream workflows run cleanly on the system source only.
- Reconciliation reports for the first period post-cutover are green.

## 9. Post-incident review hooks

- Cutover event logged to the subsystem change log per `_core/change_log_conventions.md`.
- Post-cutover retrospective attended by `data_owner`, `business_owner`, `technical_owner`, and primary consumer audiences.
- Any residual gap discovered post-cutover feeds `../rollout/post_launch_monitoring_cadence.md` follow-up items.
- If the cutover improved SLOs tracked in `../monitoring/slo_definitions.md`, capture the delta for the next quarterly portfolio review.
- If the cutover degraded any SLO, open a corrective-action plan and include in the next monthly readout.
