# Update Flow Walk-Through — `occupancy_benchmark` (includes collections sub-file)

Scenario: peer-set refresh of collections benchmarks for the southeast middle-market garden cohort.

## 1. Inbound → `reference/raw/occupancy_benchmark/2026/03/peerset_collections__2026-03-31.csv`

One row per `(region, segment, property_form, lifecycle_stage, metric_slug)`; carries `band_low`, `band_high`, `peer_median`.

## 2. Validation

- Schema check against `reference/normalized/schemas/occupancy_benchmark.yaml`.
- `metric_slug` must match the canonical alias_registry entries.
- `peer_median` must lie inside `[band_low, band_high]`.

## 3. Normalization

Write to `reference/normalized/collections_benchmarks__southeast_mf.csv`. Each row is scoped by region plus segment plus form plus lifecycle plus metric_slug, ensuring no collision between, e.g., `physical_occupancy` stabilized vs. lease_up.

## 4. Approval

Auto-approve if peer_median shifts < 1 percentage point. Otherwise route to `asset_manager`. A delinquency or bad-debt jump of > 50 bps always routes for approval.

## 5. Change Log Entry

```yaml
change_log_id: chg_2026_03_05_0001
change_type: update
target_kind: reference_record
target_ref: reference/normalized/collections_benchmarks__southeast_mf.csv#ob-se-mm-garden-stab-delinq30-20260228
old_value:
  band_low: 0.012
  band_high: 0.030
  peer_median: 0.022
new_value:
  band_low: 0.015
  band_high: 0.035
  peer_median: 0.025
source_name: "Internal peer set trailing 3-month survey (illustrative)"
source_type: internal_record
source_date: 2026-03-05
as_of_date: 2026-02-28
proposed_by: agent:operations_benchmark_agent
approved_by: human:asset_manager_owner
proposed_at: 2026-03-05T09:00:00Z
approved_at: 2026-03-05T11:00:00Z
confidence: medium
reason_for_change: |
  Peer delinquency trend widened in early 2026 across the southeast middle-market cohort.
  Peer median 30+ delinquency up 30 bps; band widened accordingly.
affected_skills:
  - roles/property_manager
  - roles/asset_manager
  - workflows/delinquency_collections
  - workflows/operating_review
```

## 6. Derived Recomputation

`reference/derived/role_kpi_targets.csv` consumes these benchmark rows. The `role_kpi_derivation_agent` re-derives the property_manager stabilized targets and writes new rows with change_log pointers.

## 7. Notifications

Logged impact on all operating review outputs and the delinquency collections workflow.

## 8. Archival

Prior rows archived to `reference/archives/occupancy_benchmark/2026/01/`.
