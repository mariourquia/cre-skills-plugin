# Update Flow Walk-Through — `staffing_model`

Scenario: annual staffing-norms refresh. HR circulates new ratios for middle-market garden based on observed workloads across the managed portfolio over the trailing twelve months.

## 1. Inbound → `reference/raw/staffing_model/2026/03/internal_staffing__2026-03-31.csv`

Row shape: one row per `(segment, property_form, management_mode, role_slug, property_size_band)` with `fte_count` and derived `units_per_fte`.

## 2. Validation

- Schema check against `reference/normalized/schemas/staffing_model.yaml`.
- `fte_count` must be > 0 and typically <= 6 for a single role at a single property.
- `role_slug` must match the role_slug enumeration used across the pack roles directory.

## 3. Normalization

Write to `reference/normalized/staffing_ratios__middle_market.csv`. Rows carry `prior_reference_id` when superseding.

## 4. Approval

Ratio changes within +/- 0.25 FTE at any size band auto-approve. Larger shifts route to `director_of_operations` approval because they move payroll assumptions.

## 5. Change Log Entry

```yaml
change_log_id: chg_2026_03_05_0005
change_type: update
target_kind: reference_record
target_ref: reference/normalized/staffing_ratios__middle_market.csv#sm-mm-garden-3pm-leasing-300399
old_value:
  fte_count: 2
  units_per_fte: 175
new_value:
  fte_count: 2.5
  units_per_fte: 140
source_name: "Internal staffing review 2026-Q1 (illustrative)"
source_type: internal_record
source_date: 2026-03-05
as_of_date: 2026-02-28
proposed_by: agent:staffing_model_agent
approved_by: human:director_of_operations
proposed_at: 2026-03-05T12:00:00Z
approved_at: 2026-03-06T09:00:00Z
confidence: medium
reason_for_change: |
  Observed tour and lead volume for 300-399 unit garden communities supported adding
  a half-FTE leasing agent. Ratio moves to 2.5 FTE / 140 units per FTE.
affected_skills:
  - roles/property_manager
  - roles/regional_manager
  - roles/leasing_manager
  - workflows/annual_budget
```

## 6. Derived Recomputation

`reference/normalized/payroll_assumptions__southeast_middle_market.csv` is consumed alongside staffing in the annual budget workflow. No automatic derived row rewrite, but the annual budget pipeline is flagged as needing re-run on next schedule.

## 7. Notifications

Logged impact on annual budgeting, regional manager oversight, and leasing operations.

## 8. Archival

Prior rows archived to `reference/archives/staffing_model/2025/12/`.
