# Runbook: Stale Feed Handling

status_tag: reference

The feed arrives on cadence but the `as_of` date of the records is older than the cadence would imply.

## 1. Trigger

- Monitoring alert `stale_as_of` fires: the landed file's `source_date` or per-record `as_of_date` is older than cadence plus tolerance, even though the file itself is on time.
- `date_coverage` reconciliation check reports a forward-coverage gap despite a file landing.
- A downstream consumer notices a metric that did not move when it should have.

## 2. Symptoms

- Record count is normal; `as_of` is old.
- `last_validated_at` in `source_registry.yaml` is fresh, masking the real staleness.
- Derived benchmarks appear unchanged over a window where upstream conditions should have moved them (for example, market_data rent comps unchanged across two refreshes).
- Workflow outputs carry a `data_freshness_confidence` score lower than target.

## 3. Likely causes (ranked)

1. Upstream system exported a cached snapshot instead of the latest state (common with nightly exports that pin an earlier close).
2. Upstream source is live but its own ingest is stale (market_data provider's underlying scrape is behind schedule).
3. Manual sender pulled the wrong file or resent a prior file.
4. A mid-month re-extract happened but the file is correctly older than the current cutoff, in that case the file is legitimate, and staleness is by design.
5. Time-zone bug in the extractor that labels a fresh file with a stale date.

## 4. Immediate actions (minute-by-minute, numbered)

1. Inspect the incoming file's header, provenance, and `extracted_at`. Compare to `source_date` and per-record `as_of_date`. Confirm the staleness is in the data, not in the filename.
2. Confirm the source is not legitimately mid-cycle (month-end close windows, market-data provider publication schedule).
3. Contact `technical_owner` to verify the upstream job pulled the latest state. If the upstream system supports a "latest-only" flag, confirm it was honored.
4. Contact `business_owner` for manual sources to confirm the correct file was sent.
5. Downgrade the confidence attached to the affected normalized entity. Emit a `confidence_downgrade` event to the observability stream (see `../monitoring/observability_events.yaml`).
6. For each dependent workflow, evaluate whether the staleness crosses the workflow's minimum freshness requirement (`../rollout/minimum_viable_data.md`). If it does, set the workflow to degraded mode; notify the primary audience.
7. If the staleness is a one-off artifact (time-zone bug, wrong file sent), correct and re-land the file; run normalization fresh.
8. If the staleness is chronic (same source stales every cycle), treat it as an SLO breach under `../monitoring/slo_definitions.md` and escalate to the `data_owner` for a structural fix.

## 5. Escalation path

- First responder: `on_call_ops`.
- `technical_owner` validates the extractor.
- `data_owner` owns the staleness classification.
- `business_owner` decides whether to accept the stale data or block.
- Primary consumer audience decides whether to rerun dependent workflows in degraded mode or wait for refresh.
- `compliance_risk` escalation for regulatory sources where staleness could compromise a filing deadline.

## 6. Affected workflows

Workflow impact mirrors `missing_file_handling.md`, but the failure mode is "works with low-confidence inputs" rather than "does not run." Examples:

- gl stale: variance narratives in `monthly_property_operating_review` and `monthly_asset_management_review` read correct numbers for the stale period but not the current period.
- market_data stale: `market_rent_refresh`, `rent_comp_intake` produce results with a flagged confidence band.
- crm stale: `lead_to_lease_funnel_review` undercounts recent activity.
- construction stale: `cost_to_complete_review`, `draw_package_review` run against an older picture; flag risk of approval-gate drift.

## 7. Recovery steps

- Re-pull or re-request the source in the correct freshness window.
- Reprocess the raw file(s); recompute derived benchmarks.
- Clear the `confidence_downgrade` flag once the fresh file lands and reconciles.
- Notify consumers of the correction; if a workflow ran and emitted outputs in degraded mode, note which outputs now supersede.

## 8. Verification steps

- `as_of` of the latest landing is within cadence tolerance.
- `date_coverage` check passes forward-coverage as well as gap-coverage.
- `data_freshness_confidence` returns to target band.
- Re-run dependent workflows; confirm they exit degraded mode.

## 9. Post-incident review hooks

- Log the event in the source's incident history.
- If recurring, the pattern feeds `../monitoring/slo_definitions.md` breach tracking and a `cutover_manual_to_system.md` candidacy review for manual sources.
- `finance_reporting` and `asset_mgmt` audiences review staleness patterns as part of monthly data-quality readouts.
- `compliance_risk` reviews any staleness that touched a regulatory input, regardless of whether a filing was missed.
