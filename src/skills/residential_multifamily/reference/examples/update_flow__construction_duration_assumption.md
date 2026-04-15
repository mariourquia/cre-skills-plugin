# Update Flow Walk-Through — `construction_duration_assumption`

Scenario: observed framing duration on the trailing three 200-299 unit garden projects averages 7 months instead of the 6-month planning norm. Update the reference accordingly.

## 1. Inbound → `reference/raw/construction_duration_assumption/2026/03/internal_norms__2026-03-31.csv`

Row shape: `(segment, property_form, project_size_band, milestone_slug, milestone_category, duration, unit)`.

## 2. Validation

- Schema check against `reference/normalized/schemas/construction_duration_assumption.yaml`.
- `unit` in `[days, weeks, months]`.
- Plausibility band per milestone_category.

## 3. Normalization

Write to `reference/normalized/construction_duration_assumptions__middle_market.csv`.

## 4. Approval

Any change >= 1 month in any milestone routes to `construction_manager` approval.

## 5. Change Log Entry

```yaml
change_log_id: chg_2026_03_24_0001
change_type: update
target_kind: reference_record
target_ref: reference/normalized/construction_duration_assumptions__middle_market.csv#cda-se-mm-garden-200-framing
old_value:
  value: 6
new_value:
  value: 7
source_name: "Internal schedule norms refresh 2026-Q1 (illustrative)"
source_type: internal_record
source_date: 2026-03-24
as_of_date: 2026-02-28
proposed_by: agent:construction_duration_agent
approved_by: human:construction_manager_owner
proposed_at: 2026-03-24T10:00:00Z
approved_at: 2026-03-24T15:00:00Z
confidence: medium
reason_for_change: |
  Observed framing duration on trailing three garden 200-299 unit projects averaged 7 months;
  update planning norm to match observed pace.
affected_skills:
  - workflows/dev_proforma
  - workflows/construction_schedule
  - roles/construction_manager
  - roles/development_manager
```

## 6. Derived Recomputation

None automatic; construction schedule template picks up on next run.

## 7. Notifications

Logged impact on dev pro forma, construction schedule, construction manager.

## 8. Archival

Prior row archived to `reference/archives/construction_duration_assumption/2026/01/`.
