# GL Connector (stub, vendor-neutral)

General-ledger feed. Source of truth for financial actuals, budgets, forecasts, variance, capex actuals, and commitments at the property or entity level.

## Status

`status: stub` — schema, mapping template, sample, and reconciliation checks only. No NetSuite / Sage / QuickBooks / MRI / Yardi-GL adapter code lives here.

## Entities

| Entity | One-liner |
|---|---|
| `chart_of_accounts` | One row per account in the owner's CoA. |
| `account_mapping` | One row per source-account → canonical-account mapping. |
| `actual` | One row per posted GL actual per account per period per property. |
| `budget` | One row per budget line per account per period per property. |
| `forecast` | One row per forecast line per account per period per property. |
| `variance_line` | One row per period per account capturing budget-actual variance. |
| `capex_actual` | One row per capex posting (to an asset account). |
| `commitment` | One row per open GL commitment (PO, contract, accrual). |

## Scope

Vendor-agnostic. Defines the entity shape every GL feed must provide, plus a chart-of-accounts mapping layer so the subsystem's canonical line labels stay stable across operators with different CoAs.

## Integration

- `gl.actual` + `gl.budget` feed variance-narrative-generator, property-performance-dashboard, and the finance_reporting audience.
- `gl.capex_actual` + `gl.commitment` feed the capex-prioritizer and construction-command-center workflows.
- `gl.chart_of_accounts` + `gl.account_mapping` normalize operator CoAs to the canonical account space the metric contract uses.

See `INGESTION.md` for the landing convention and `reconciliation_checks.yaml` for the domain-specific QA invariants.
