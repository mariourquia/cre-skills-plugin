# Update Flow Walk-Through — `payroll_assumption`

Scenario: mid-year payroll survey update. Southeast market wage pressure on maintenance techs pushes hourly_mid from $24/hr to $26/hr.

## 1. Inbound → `reference/raw/payroll_assumption/2026/03/internal_payroll__2026-03-31.csv`

Row shape: `(market or region, segment, management_mode, role_slug, band_type, amount, unit)`. `unit` is `dollars_per_year`, `dollars_per_hour`, or `percent` depending on band_type.

## 2. Validation

- Schema check against `reference/normalized/schemas/payroll_assumption.yaml`.
- `band_type` ordering check: within a role, `base_salary_low <= base_salary_mid <= base_salary_high`.
- Plausibility: hourly rates in `[12, 75]` range for on-site operating roles.

## 3. Normalization

Write to `reference/normalized/payroll_assumptions__<region>_<segment>.csv`. Most rows land in `payroll_assumptions__southeast_middle_market.csv`.

## 4. Approval

Changes within +/- 5% auto-approve. Larger shifts route to `cfo_finance_leader` because they feed the annual budget payroll line.

## 5. Change Log Entry

```yaml
change_log_id: chg_2026_03_05_0008
change_type: update
target_kind: reference_record
target_ref: reference/normalized/payroll_assumptions__southeast_middle_market.csv#pa-se-mm-3pm-mtech-hourly-mid
old_value:
  value: 24
new_value:
  value: 26
source_name: "Internal payroll survey 2026-Q1 (illustrative)"
source_type: internal_record
source_date: 2026-03-05
as_of_date: 2026-02-28
proposed_by: agent:payroll_benchmark_agent
approved_by: human:cfo_owner
proposed_at: 2026-03-05T14:00:00Z
approved_at: 2026-03-06T10:30:00Z
confidence: medium
reason_for_change: |
  Southeast market wage pressure: maintenance tech hourly_mid up ~8% over trailing 12 months.
  Rebased band effective 2026-03-01.
affected_skills:
  - workflows/annual_budget
  - roles/cfo_finance_leader
  - roles/reporting_finance_ops_lead
```

## 6. Derived Recomputation

No direct derived file; the annual budget workflow picks up the new rate on next run.

## 7. Notifications

Logged impact on annual budgeting and finance ops.

## 8. Archival

Prior row archived to `reference/archives/payroll_assumption/2026/01/`.
