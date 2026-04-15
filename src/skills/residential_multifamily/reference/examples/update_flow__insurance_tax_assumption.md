# Update Flow Walk-Through — `insurance_tax_assumption`

Scenario: Dallas County re-assessed tax roll on 2026-04-01 with an effective-rate increase from 2.45% to 2.55%.

## 1. Inbound → `reference/raw/insurance_tax_assumption/2026/03/internal_placeholders__2026-03-31.csv`

Row shape: `(market, state, county, segment, property_form, assumption_slug, assumption_category, amount, unit)`.

## 2. Validation

- Schema check against `reference/normalized/schemas/insurance_tax_assumption.yaml`.
- `unit` matches category (tax rates in `percent_of_value` or `millage_rate`).

## 3. Normalization

Write to `reference/normalized/insurance_tax_assumptions__<region>_mf.csv`.

## 4. Approval

Any tax-rate or insurance assumption change that crosses 5 bps or 10% of premium routes to `cfo_finance_leader` approval. This is because these are planning placeholders and can easily propagate into misquoted budgets; approval gate is deliberately tight.

## 5. Change Log Entry

```yaml
change_log_id: chg_2026_04_01_0003
change_type: update
target_kind: reference_record
target_ref: reference/normalized/insurance_tax_assumptions__southeast_mf.csv#ita-dallas-retax
old_value:
  value: 0.0245
new_value:
  value: 0.0255
source_name: "Dallas County reassessment notice (illustrative)"
source_type: government_publication
source_date: 2026-04-01
as_of_date: 2026-04-01
proposed_by: agent:insurance_tax_agent
approved_by: human:cfo_owner
proposed_at: 2026-04-01T10:00:00Z
approved_at: 2026-04-01T14:00:00Z
confidence: high
reason_for_change: |
  Dallas County 2026 tax roll update: effective property tax rate up 10 bps.
  Underwriting placeholder rebased; real operating figures come from per-property tax bills.
affected_skills:
  - workflows/acquisition_underwriting
  - workflows/annual_budget
  - roles/cfo_finance_leader
  - roles/asset_manager
```

## 6. Derived Recomputation

None automatic. Acquisition underwriting workflow picks up on next run.

## 7. Notifications

Logged impact on acquisition underwriting and annual budget.

## 8. Archival

Prior row archived to `reference/archives/insurance_tax_assumption/2026/02/`.
