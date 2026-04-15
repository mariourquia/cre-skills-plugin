# Market Data Derived Dependencies

Which canonical metrics, workflows, and templates depend on normalized market_data.

## Required normalized inputs

- `market_data.rent_comp`: at minimum for any market where an owned property operates.

## Optional enrichment inputs

- `market_data.concession_observation`: concession benchmark derivation.
- `market_data.occupancy_benchmark`: market-level occupancy reference.
- `market_data.payroll_reference`: payroll benchmarking per role.
- `market_data.labor_reference`: labor hourly rates per trade.
- `market_data.material_reference`: material cost references.
- `market_data.utility_reference`: utility cost benchmarks.

## Confidence minimum

- Coverage count in every active (market, submarket) meets the minimum declared in `market_data/manifest.yaml`.
- Freshness SLA met per category.
- Endorsement status on derived benchmarks.

## Blocking data issues

- Coverage gap in an active submarket (comp-snapshot refuses).
- Stale feed past the SLA for a required category.
- Unmapped unit_type_label (reject at landing).
- Unregistered source_name (warn; skills down-weight to zero until registered).
- Outlier observations unquarantined.

## Fallback mode when partial

- Without rent_comp in a market, comp-snapshot, rent-optimization-planner, and comp-based underwriting skills refuse for that market.
- Without concession_observation, effective-rent calculations degrade to asking rents with a degraded-confidence flag.
- Without occupancy_benchmark, market-to-lease-gap skill uses only owned-portfolio observations.
- Without payroll_reference, annual-budget-engine uses last-reviewed historical payroll per role.
- Without labor_reference, turn-cost benchmarks degrade to historical internal averages.
- Without material_reference, construction-budget-gc-analyzer falls back to bid history.
- Without utility_reference, utility-benchmark comparisons refuse.

## Canonical metrics that depend on market_data

### Property Operations family

- `market_to_lease_gap`: requires `market_data.rent_comp`.
- `loss_to_lease`: requires `market_data.rent_comp` and PMS rent roll.
- `concession_rate`: enriched by `market_data.concession_observation` for comparability.

### Asset Management family

- `noi` projections: enriched by market_data for forecasting.

### Portfolio Management family

- `occupancy_by_market`: contextualized against `market_data.occupancy_benchmark`.
- `portfolio_concentration_market`: uses market gazetteer for classification.

### Development and Construction family

- `dev_cost_per_unit`, `dev_cost_per_nrsf`, `dev_cost_per_gsf`: cross-checked against `material_reference` and `labor_reference`.
- `trade_buyout_variance`: references `labor_reference` for baseline.

## Example output types

- Comp snapshot report (rent comps + adjustment grid).
- Submarket truth-serum brief.
- Concession benchmark dashboard.
- Market-level occupancy trend chart.
- Payroll benchmark versus actual comparison.
- Turn-cost benchmark versus actual.
- Material-cost benchmark per region.

## Dependent workflows

- `market_rent_refresh` (dedicated to maintaining the market_data feed).
- `rent_comp_intake`.
- `quarterly_portfolio_review` (uses market benchmarks for context).
- `budget_build` (uses labor, material, payroll, utility references).
- `capex_estimate_generation` (uses material and labor references).
