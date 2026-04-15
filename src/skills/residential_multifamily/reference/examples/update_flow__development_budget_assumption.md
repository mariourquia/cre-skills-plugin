# Update Flow Walk-Through — `development_budget_assumption`

Scenario: hard_cost_shell per GSF is rebased after the lumber spike in `update_flow__material_cost.md` is approved and the broader hard-cost basket reprices.

## 1. Inbound → `reference/raw/development_budget_assumption/2026/03/internal_norms__2026-03-31.csv`

Row shape: `(market or region, segment, property_form, budget_line_slug, budget_line_category, amount, unit)`.

## 2. Validation

- Schema check against `reference/normalized/schemas/development_budget_assumption.yaml`.
- `unit` must match budget_line_category conventions (hard_cost in `dollars_per_gsf`, fee/contingency in `percent_of_*`).

## 3. Normalization

Write to `reference/normalized/development_budget_assumptions__middle_market_garden.csv`.

## 4. Approval

Changes to hard-cost per GSF > 3% route to `development_manager`. Fees/contingencies that change at all route to `cfo_finance_leader`.

## 5. Change Log Entry

```yaml
change_log_id: chg_2026_03_22_0001
change_type: update
target_kind: reference_record
target_ref: reference/normalized/development_budget_assumptions__middle_market_garden.csv#dba-se-mm-garden-hc-shell
old_value:
  value: 125
new_value:
  value: 132
source_name: "Internal dev budget norms refresh 2026-Q1 (illustrative)"
source_type: internal_record
source_date: 2026-03-22
as_of_date: 2026-02-28
proposed_by: agent:dev_budget_agent
approved_by: human:development_manager_owner
proposed_at: 2026-03-22T11:00:00Z
approved_at: 2026-03-23T09:00:00Z
confidence: medium
reason_for_change: |
  Rebase of wood-frame garden shell hard cost per GSF following lumber index spike and
  framing labor pressure. Impacts all active dev pro formas.
affected_skills:
  - workflows/dev_proforma
  - roles/development_manager
  - roles/cfo_finance_leader
```

## 6. Derived Recomputation

None direct; pro forma workflow picks up on next run.

## 7. Notifications

Logged impact on dev pro forma, development manager, finance leader.

## 8. Archival

Prior row archived to `reference/archives/development_budget_assumption/2026/01/`.
