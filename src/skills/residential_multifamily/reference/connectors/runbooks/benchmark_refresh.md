# Runbook: Benchmark Refresh

status_tag: reference

Periodic refresh of market rent, concession, payroll, labor, materials, utility, vendor rate, capex cost library, and schedule duration benchmarks.

## 1. Trigger

- Calendar-scheduled refresh cycle per benchmark category (weekly for market rents, monthly for labor and utility, quarterly for capex cost library, annually for schedule durations and payroll bands, actual cadence per overlay).
- Benchmark provider publishes a new release.
- Reconciliation or variance analysis flags a benchmark as stale or drifted beyond tolerance.
- New overlay (segment, regulatory, org, market) requires a benchmark at a scope not currently in the reference system.

## 2. Symptoms

- `reference/derived/<benchmark>__<scope>.csv` has a `last_refreshed_at` older than cadence.
- Workflows that read the benchmark emit lower `confidence` scores.
- Variance narratives compare actuals against outdated targets.
- A tailoring session requests a benchmark that does not exist at the declared scope.

## 3. Likely causes (ranked)

1. Cadence window elapsed; refresh is due.
2. Provider released a new version; refresh is available.
3. Market conditions shifted materially and the monitor triggered an out-of-cycle refresh.
4. New scope (new market, new segment, new regulatory program) requires a fresh benchmark.
5. Data-quality incident upstream made the previous refresh unreliable and the benchmark has been held at the prior version pending correction.

## 4. Immediate actions (minute-by-minute, numbered)

1. Confirm which benchmark category is being refreshed: market_rent, concession_observation, occupancy_benchmark, payroll_benchmark, labor_benchmark, materials_benchmark, utility_benchmark, vendor_rate, capex_cost_library, schedule_duration_assumption.
2. Select the source(s) for the refresh. Map each source to a `source_id` in `source_registry.yaml`. For external subscriptions (for example, market_rent_comps_primary), confirm the source is `active`; for internal sources (for example, aggregated pms and gl data), confirm the upstream landings for the refresh window are complete.
3. Land sanitized sample(s) of the refreshed inputs under `reference/raw/<domain>/<YYYY>/<MM>/`. Validate all provenance fields per `INGESTION.md`.
4. Run the domain's normalization pipeline for the refresh window. Run all reconciliation checks; resolve blocker failures before proceeding.
5. Compute the derived benchmark using the canonical method documented in `_core/metrics.md` for metric-backed benchmarks, or the category's derivation note in `reference/derived/` for non-metric benchmarks.
6. Produce a refresh diff: compare the new `reference/derived/<benchmark>__<scope>.csv` to the prior version. Flag records whose delta exceeds the overlay's drift tolerance.
7. Assess confidence: tag the refreshed benchmark with a `confidence_band` (high, medium, low) based on source freshness, record count, and variance vs prior.
8. Open an approval gate for publication. Benchmarks that drive lender, investor, or board-facing outputs require `finance_reporting` sign-off; benchmarks that drive compensation or vendor-rate decisions require `executive` sign-off per `overlays/org/<org_id>/approval_matrix.yaml`.
9. On approval, publish the new version to `reference/derived/`. Emit a `benchmark_refresh_published` event (see `../monitoring/observability_events.yaml`).
10. Write a change log entry per `_core/change_log_conventions.md` naming: benchmark slug, scope, source(s), prior version, new version, confidence band, drift summary, approver.
11. Notify affected skill packs. Packs whose `reference_manifest.yaml` declares reads on the benchmark receive a freshness event; any workflow in flight at the time of the refresh reports whether it used the pre- or post-refresh version.

## 5. Escalation path

- First responder: `data_owner` for the benchmark source (or the benchmark-owner analyst role for aggregated sources).
- `business_owner` approves the use case.
- `finance_reporting` approves publication of finance-adjacent benchmarks.
- `compliance_risk` approves publication of regulatory-program benchmarks.
- `executive` approves publication of benchmarks driving compensation, vendor selection, or capital allocation.
- `asset_mgmt` reviews cross-portfolio drift.

## 6. Affected workflows

The refresh feeds any workflow that reads the benchmark. Examples:

- market_rent and concession_observation: `market_rent_refresh`, `rent_comp_intake`, `lead_to_lease_funnel_review`, `renewal_retention`, `lease_up_war_room` if invoked from a sibling skill pack.
- payroll and labor: `monthly_property_operating_review`, `budget_build`, `reforecast`, `third_party_manager_scorecard_review`.
- materials, vendor_rate, capex_cost_library: `capex_estimate_generation`, `bid_leveling_procurement_review`, `change_order_review`, `capital_project_intake_and_prioritization`, `cost_to_complete_review`.
- schedule_duration_assumption: `capex_estimate_generation`, `schedule_risk_review`, `capital_project_intake_and_prioritization`.
- utility: `monthly_property_operating_review`, `reforecast`.

## 7. Recovery steps

- If publication is blocked by a failed reconciliation, retain the prior version as the live benchmark. Do not publish the new version.
- If a published refresh is later identified as incorrect, follow `reference_rollback.md`.
- If drift exceeds a policy threshold and the new benchmark is directionally correct but wider than tolerance, publish with a `confidence_band: low` and flag downstream workflows to display a freshness advisory.

## 8. Verification steps

- `reference/derived/<benchmark>__<scope>.csv` has a fresh `last_refreshed_at`.
- Change log entry exists and is signed off.
- Approval artifact exists.
- Downstream workflow activation rechecks pass.
- Drift diff is archived for audit.

## 9. Post-incident review hooks

- Benchmark refresh events feed the monthly data-quality readout to `finance_reporting` and `asset_mgmt`.
- Quarterly cross-benchmark consistency review: `executive` and `finance_reporting` attend.
- Any benchmark whose drift exceeds an overlay threshold triggers a root-cause review with the owning analyst role.
- Regulatory-program benchmarks (for example, utility allowance schedule, rent limits, income limits) refresh through the regulatory overlay path; `compliance_risk` owns the review cadence.
