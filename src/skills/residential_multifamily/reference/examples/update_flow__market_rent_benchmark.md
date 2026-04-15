# Update Flow Walk-Through — `market_rent_benchmark`

Scenario: CoStar publishes aggregated submarket rent benchmarks on 2026-04-05. Unlike the property-level `rent_comp` flow, this flow ingests pre-aggregated submarket/unit-type benchmark rows directly.

## 1. Inbound → `reference/raw/market_rent_benchmark/2026/03/costar_submarket__2026-03-31.csv`

Row shape: one benchmark row per (market, submarket, segment, property_form, property_class, unit_type) combination with `sample_size_properties` and `trailing_3mo_change_pct`.

## 2. Validation

- Schema check against `reference/normalized/schemas/market_rent_benchmark.yaml`.
- Magnitude check: `trailing_3mo_change_pct` within -10% to +10%; beyond this routes to approval.
- Sample-size check: flag rows with `sample_size_properties < 5` as confidence `low`.

## 3. Normalization

Write to `reference/normalized/market_rents__<market>_mf.csv`. The normalized file is a single-market bundle; each row carries the submarket/unit-type scope.

## 4. Approval

Auto-approve rows within magnitude band and with sample size >= 5. Route outliers to `asset_manager` approval.

## 5. Change Log Entry

```yaml
change_log_id: chg_2026_04_05_0010
change_type: update
target_kind: reference_record
target_ref: reference/normalized/market_rents__charlotte_mf.csv#mrb-charlotte-southend-mm-garden-b1-20260331
old_value:
  value: 1895
new_value:
  value: 1935
source_name: "CoStar 2026-Q1 Charlotte submarket report (illustrative)"
source_type: costar
source_date: 2026-04-05
as_of_date: 2026-03-31
proposed_by: agent:market_rent_benchmark_agent
approved_by: human:mu_owner
proposed_at: 2026-04-05T14:30:00Z
approved_at: 2026-04-05T15:45:00Z
confidence: medium
reason_for_change: |
  Quarterly refresh. B1 garden benchmark in South End Charlotte shifted +2.1% QoQ.
affected_skills:
  - roles/property_manager
  - workflows/renewal_retention
  - workflows/rent_optimization
affected_overlays:
  - segments/middle_market
```

## 6. Derived Recomputation

`reference/derived/role_kpi_targets.csv` does not reuse market-level rent benchmarks directly, but the `workflows/rent_optimization` pack surfaces the new bands in its outputs.

## 7. Notifications

Logged impact on `workflows/rent_optimization`, `workflows/renewal_retention`, `roles/property_manager`, `roles/asset_manager`.

## 8. Archival

Prior rows moved to `reference/archives/market_rent_benchmark/2025/12/`.
