# Reference Layer

Every mutable figure the subsystem uses lives here. Skill prose references files by path; it does not embed numbers.

## Directory layout

```
reference/
  raw/           source-of-truth inbound records (CSV or JSON, one file per source + date)
  normalized/    cleaned, schema-conforming; the working layer for skills
  derived/       computed benchmarks produced from normalized (target bands, blended weights)
  archives/      superseded records (audit trail)
  examples/      end-to-end walk-throughs showing how an update flows
```

## Record schema

Every record in `normalized/` and `raw/` conforms to `_core/schemas/reference_record.yaml`. Minimum fields:

- `reference_id`
- `category` (one of the 16 categories below)
- `scope` (market / submarket / segment / form / lifecycle / mode / role / org / property)
- `value`
- `unit`
- `scenario`
- `source_name`, `source_type`, `source_date`
- `as_of_date`
- `confidence`
- `status` (draft / proposed / approved / deprecated / sample / starter / illustrative / placeholder)
- `proposed_by`

Category-specific extensions are documented per category below.

## 16 Reference categories

1. **rent_comp** — Individual rent comparable observations (property-level).
2. **market_rent_benchmark** — Aggregated market rents by market / submarket / unit type.
3. **concession_benchmark** — Concession levels offered in market.
4. **occupancy_benchmark** — Market physical / leased / economic occupancy norms.
5. **staffing_model** — Staffing headcount ratios by property size / segment / form.
6. **payroll_assumption** — Salary bands, burden rate, benefit load per role.
7. **labor_rate** — Trade labor rates by market (plumber, electrician, HVAC, etc.).
8. **material_cost** — Material cost history (flooring, appliances, paint, roofing, HVAC components).
9. **vendor_rate** — Rate cards for contracted vendors.
10. **unit_turn_cost** — Per-unit turn cost by scope (classic vs. renovation-level).
11. **capex_line_item** — Line items in the capex library (cost per unit, cost per sf, assembly cost).
12. **development_budget_assumption** — Hard cost, soft cost, FF&E, developer fee norms.
13. **construction_duration_assumption** — Typical durations by trade / milestone.
14. **utility_benchmark** — Utility cost norms net of RUBS by market / form.
15. **insurance_tax_assumption** — Insurance and real estate tax assumption placeholders.
16. **approval_threshold_policy** — Dollar thresholds triggering approvals.

## File naming

- `normalized/<category>__<scope_suffix>.csv` where `scope_suffix` captures the scoping axis. Examples:
  - `normalized/market_rents__charlotte_mf.csv`
  - `normalized/market_rents__nashville_mf.csv`
  - `normalized/material_costs__southeast_residential.csv`
  - `normalized/labor_rates__phoenix_residential.csv`
  - `normalized/staffing_ratios__middle_market.csv`
  - `normalized/capex_line_items__middle_market_value_add.csv`

- `raw/<category>/<yyyy>/<mm>/<source>__<as_of>.csv` for inbound. Example:
  - `raw/rent_comp/2026/04/costar__2026-03-31.csv`

- `derived/<category>__<scope>.csv` for computed benchmarks. Example:
  - `derived/role_kpi_targets.csv` (blended across segment and market defaults).

## Update flows

Each category's update flow is documented in `examples/update_flow__<category>.md`. Generic flow:

1. **Inbound.** Agent or human drops a new record into `raw/<category>/...`. Record carries `status: proposed`.
2. **Validation.** Record is validated against `_core/schemas/reference_record.yaml` + category schema.
3. **Normalization.** Record is copied to `normalized/<category>__<scope>.csv` with normalized column mapping. `prior_reference_id` is set if superseding.
4. **Approval.** An `ApprovalRequest` is opened if the record's magnitude crosses a configured delta threshold vs. prior (e.g., market rent > 8% change). Otherwise the record is auto-approved.
5. **Change log.** A `change_log_entry` is appended to `archives/change_log.jsonl`.
6. **Derived recomputation.** Any `derived/` file that depends on the category is re-derived; a `change_log_entry` is produced for each derived file that changed.
7. **Skill notification (optional).** Packs whose `reference_manifest.yaml` lists the path are logged as affected.

See `examples/update_flow__rent_comp.md` for a worked example.

## Sample vs. live data

All starter files in this initial commit are tagged `status: sample | starter | illustrative | placeholder` at the row level. Skills must surface the tag when citing a sample row. Do not use sample data as operating fact.

## Cross-reference to skill packs

Every skill pack's `reference_manifest.yaml` lists which paths it reads. Tests fail if a pack reads a reference not listed in its manifest.

## Archival and rollback

Superseded records are moved to `archives/<category>/<yyyy>/<mm>/`. A rollback produces a new `change_log_entry` with `change_type: rollback` referencing the reversed entry.
