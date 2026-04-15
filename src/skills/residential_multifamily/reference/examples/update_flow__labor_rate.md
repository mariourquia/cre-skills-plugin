# Update Flow Walk-Through — `labor_rate`

Scenario: Charlotte HVAC journeyman rates reprice from $110/hr to $118/hr driven by trade shortage heading into summer.

## 1. Inbound → `reference/raw/labor_rate/2026/03/local_survey__2026-03-31.csv`

Row shape: `(market, region, segment, trade_slug, labor_tier, rate_type, rate_amount, unit)`.

## 2. Validation

- Schema check against `reference/normalized/schemas/labor_rate.yaml`.
- Trade_slug enumerated; labor_tier matches the schema enum.
- Magnitude check: > 10% jump flags for approval.

## 3. Normalization

Write to `reference/normalized/labor_rates__<market>_residential.csv`.

## 4. Approval

Auto-approve if delta within +/- 5%. HVAC journeyman jump (+7.3%) routes for approval to `construction_manager` because it affects both capex and R&M assumptions.

## 5. Change Log Entry

```yaml
change_log_id: chg_2026_03_10_0001
change_type: update
target_kind: reference_record
target_ref: reference/normalized/labor_rates__charlotte_residential.csv#lr-charlotte-hvac-journey-hrly
old_value:
  value: 110
new_value:
  value: 118
source_name: "Local vendor rate survey 2026-Q1 (illustrative)"
source_type: local_survey
source_date: 2026-03-10
as_of_date: 2026-02-28
proposed_by: agent:labor_rate_agent
approved_by: human:construction_manager_owner
proposed_at: 2026-03-10T11:00:00Z
approved_at: 2026-03-10T14:00:00Z
confidence: medium
reason_for_change: |
  Charlotte HVAC journeyman rates up ~7% entering summer cooling season. Rebase
  effective 2026-03-15. Impacts unit-turn HVAC line items and R&M budget assumptions.
affected_skills:
  - workflows/unit_turn_make_ready
  - workflows/capex_prioritization
  - roles/construction_manager
  - roles/maintenance_supervisor
```

## 6. Derived Recomputation

`unit_turn_cost_library__middle_market.csv` rows whose scope items include HVAC components (currently none in the starter library but reserved for future) would be flagged.

## 7. Notifications

Logged impact on turn make-ready, capex prioritization, maintenance supervisor pack.

## 8. Archival

Prior row archived to `reference/archives/labor_rate/2026/01/`.
