# Construction Connector (stub, vendor-neutral)

Ground-up development and major-renovation project data. Development budgets, estimate line items, bid packages, commitments, change orders, draw requests, schedule milestones, and punch items.

## Status

`status: stub` — schema, mapping template, sample, and reconciliation checks only. No Procore / Sage / Autodesk / Smartsheet / e-Builder adapter code lives here.

## Entities

| Entity | One-liner |
|---|---|
| `dev_budget` | One row per development-budget line per project per period. |
| `estimate_line_item` | One row per estimate line item within a project's estimate. |
| `bid_package` | One row per bid package issued. |
| `commitment` | One row per signed subcontract or material commitment. |
| `change_order` | One row per change order. |
| `draw_request` | One row per lender-draw request. |
| `schedule_milestone` | One row per scheduled milestone (baseline and current). |
| `punch_item` | One row per punch-list item. |

## Scope

Vendor-agnostic. Defines the entity shape for construction-side data that does not sit in the PMS or GL. Overlaps intentionally with `ap.commitment` (AP tracks invoice-match; construction tracks subcontract scope and CO status) and `gl.commitment` (GL captures posted balances; construction captures the full contract snapshot).

## Integration

- `construction.dev_budget` feeds dev-proforma-engine and annual-budget-engine for development-stage properties.
- `construction.estimate_line_item` feeds construction-budget-gc-analyzer.
- `construction.bid_package` + `construction.commitment` feed construction-procurement-contracts-engine.
- `construction.change_order` feeds ChangeOrder canonical object (see `_core/ontology.md`); reconciles against ap.commitment invoice-cap.
- `construction.draw_request` feeds DrawRequest canonical object; reconciled against commitment + CO totals via `qa/commitment_change_order_draw.yaml`.
- `construction.schedule_milestone` + `construction.punch_item` feed construction-project-command-center.

See `INGESTION.md`.
