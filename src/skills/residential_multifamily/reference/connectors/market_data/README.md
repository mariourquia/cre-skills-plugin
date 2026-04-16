# Market Data Connector (stub, vendor-neutral)

External market-intelligence feeds — rent comps, concessions, occupancy benchmarks, payroll, labor, material, and utility references. This is the only connector whose output maps directly into the 16-category reference system as benchmark inputs.

## Status

`status: stub` — schema, mapping template, sample, and reconciliation checks only. No CoStar / Yardi Matrix / RealPage Data / Reis / CBRE / JLL adapter code lives here.

## Entities

| Entity | One-liner |
|---|---|
| `rent_comp` | One row per property-level rent comparable observation. |
| `concession_observation` | One row per observed concession offer. |
| `occupancy_benchmark` | One row per market-level occupancy benchmark observation. |
| `payroll_reference` | One row per role-level payroll benchmark observation. |
| `labor_reference` | One row per trade labor rate observation. |
| `material_reference` | One row per material cost observation. |
| `utility_reference` | One row per utility cost benchmark observation. |

## Scope

Vendor-agnostic. Each entity maps to a reference-layer category (see `reference/README.md`). This connector is the primary inbound surface for market_rent_benchmark, concession_benchmark, occupancy_benchmark, payroll_assumption, labor_rate, material_cost, and utility_benchmark.

## Integration

- `market_data.rent_comp` feeds the `rent_comp` reference category; derived benchmarks in `reference/derived/market_rent_benchmark__*.csv` recompute after landing.
- `market_data.concession_observation` → `concession_benchmark` reference category.
- `market_data.occupancy_benchmark` → `occupancy_benchmark` reference category.
- `market_data.payroll_reference` → `payroll_assumption` reference category.
- `market_data.labor_reference` → `labor_rate` reference category.
- `market_data.material_reference` → `material_cost` reference category.
- `market_data.utility_reference` → `utility_benchmark` reference category.

Skills consuming this connector: comp-snapshot, submarket-truth-serum, market-memo-generator, acquisition-underwriting-engine, annual-budget-engine.

See `INGESTION.md`.
