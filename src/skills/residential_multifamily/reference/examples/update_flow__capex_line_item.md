# Update Flow Walk-Through — `capex_line_item`

Scenario: the classic kitchen package line item is re-derived after a combined material cost + vendor rate refresh. `unit_kitchen_package_classic` drops from $4650/unit to $4520/unit.

## 1. Inbound → `reference/raw/capex_line_item/2026/03/internal_library__2026-03-31.csv`

Row shape: `(region, segment, property_form, line_item_slug, capex_category, assembly_basis, typical_useful_life_years, yield_on_cost_assumption, cost_amount, unit)`.

## 2. Validation

- Schema check against `reference/normalized/schemas/capex_line_item.yaml`.
- `line_item_slug` + `assembly_basis` consistency (e.g., `per_unit` for unit-interior; `per_sf` for building envelope).
- Plausibility band by capex_category.

## 3. Normalization

Write to `reference/normalized/capex_line_items__middle_market_value_add.csv`.

## 4. Approval

Changes within +/- 5% auto-approve; larger deltas route to `asset_manager`.

## 5. Change Log Entry

```yaml
change_log_id: chg_2026_03_20_0001
change_type: update
target_kind: reference_record
target_ref: reference/normalized/capex_line_items__middle_market_value_add.csv#capex-se-mm-garden-unitkit-classic
old_value:
  value: 4650
new_value:
  value: 4520
source_name: "Internal capex library refresh 2026-Q1 (illustrative)"
source_type: internal_record
source_date: 2026-03-20
as_of_date: 2026-02-28
proposed_by: agent:capex_library_agent
approved_by: human:asset_manager_owner
proposed_at: 2026-03-20T10:00:00Z
approved_at: 2026-03-20T15:00:00Z
confidence: medium
reason_for_change: |
  Rebased classic kitchen package following LVP distributor change and vendor paint re-bid.
affected_skills:
  - workflows/capex_prioritization
  - workflows/dev_proforma
  - roles/asset_manager
  - roles/construction_manager
```

## 6. Derived Recomputation

Capex budgeting workflows flagged for re-run; no automatic rewrite of derived files.

## 7. Notifications

Logged impact on capex prioritization and dev pro forma.

## 8. Archival

Prior row archived to `reference/archives/capex_line_item/2026/01/`.
