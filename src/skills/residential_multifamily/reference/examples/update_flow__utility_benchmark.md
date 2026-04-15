# Update Flow Walk-Through — `utility_benchmark`

Scenario: Duke Energy common-area electric rate tariff change lifts the master-metered common-area electric benchmark from $14/unit/month to $15/unit/month for southeast garden.

## 1. Inbound → `reference/raw/utility_benchmark/2026/03/internal_norms__2026-03-31.csv`

Row shape: `(region, segment, property_form, utility_slug, metering_basis, rubs_recovery_pct, gross_owner_paid, net_owner_paid, unit)`.

## 2. Validation

- Schema check against `reference/normalized/schemas/utility_benchmark.yaml`.
- `rubs_recovery_pct` in [0,1].
- `net_owner_paid <= gross_owner_paid`.

## 3. Normalization

Write to `reference/normalized/utility_benchmarks__southeast_mf.csv`.

## 4. Approval

Auto-approve if delta < 10%. Larger deltas route to `asset_manager`.

## 5. Change Log Entry

```yaml
change_log_id: chg_2026_03_25_0001
change_type: update
target_kind: reference_record
target_ref: reference/normalized/utility_benchmarks__southeast_mf.csv#ub-se-mm-garden-elec-common
old_value:
  gross_owner_paid: 14
  net_owner_paid: 14
new_value:
  gross_owner_paid: 15
  net_owner_paid: 15
source_name: "Internal utility norms refresh 2026-Q1 (illustrative)"
source_type: internal_record
source_date: 2026-03-25
as_of_date: 2026-02-28
proposed_by: agent:utility_benchmark_agent
approved_by: human:asset_manager_owner
proposed_at: 2026-03-25T09:00:00Z
approved_at: 2026-03-25T12:00:00Z
confidence: medium
reason_for_change: |
  Duke Energy common-area electric tariff adjustment lifts benchmark by ~7%.
affected_skills:
  - workflows/annual_budget
  - workflows/operating_review
  - roles/asset_manager
```

## 6. Derived Recomputation

None; annual budget picks up on next run.

## 7. Notifications

Logged impact on annual budget, operating review, asset manager.

## 8. Archival

Prior row archived to `reference/archives/utility_benchmark/2026/01/`.
