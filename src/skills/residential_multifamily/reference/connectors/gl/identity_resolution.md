# GL Identity Resolution

How accounts, legal entities, and properties in the GL connector crosswalk to canonical identifiers used by the residential multifamily subsystem.

## Crosswalk pointers

- `reference/connectors/master_data/account_crosswalk.yaml`: chart-of-accounts identity across time and systems.
- `reference/connectors/master_data/entity_crosswalk.yaml`: legal entity to property mapping.
- `reference/connectors/master_data/property_crosswalk.yaml`: property identity across systems (shared with PMS).
- `reference/connectors/master_data/fx_rate_registry.yaml`: FX reference for non-USD entities.

Each crosswalk declares canonical slugs with effective windows; account renames preserve prior account_ids as aliases with rename_to pointers.

## Match methods

| Method | Use | Confidence |
|---|---|---|
| `exact` | Operator's native account_id, entity_id, property_id where the source system is authoritative. | Highest. The default join path. |
| `composite` | (source_account_id, effective_period) where accounts have been renamed; (entity_id, property_id) where one entity spans multiple properties. | High. Required for time-series integrity across account renames. |
| `fuzzy` | Normalized account_label string match when source_account_id changes without rename_to trail; rare and operator-reviewed. | Low. Queued for operator adjudication. |
| `manual` | Operator-declared canonical_account_slug override recorded in account_mapping with reviewer and timestamp. | Authoritative once recorded. |

## Confidence scoring

Every account_mapping row carries `approval_status` in (`proposed`, `endorsed`, `deprecated`). Only `endorsed` mappings feed downstream metrics; `proposed` rows are queued for review. `deprecated` mappings retain their effective window so historical reporting remains stable.

## Hard cases

### One legal entity spanning multiple operating properties

A single LLC may hold two or more properties. The GL publishes postings under the entity's account structure, but costs must be allocated across the properties for NOI and variance reporting. The entity_crosswalk declares the entity_id as `multi_property = true` and registers the allocation_basis (unit_count, square_footage, revenue, or direct-coded property_id). Failure mode: without an allocation basis, shared-entity postings silently bucket to one property and distort per-property NOI. Mitigation: `gl_mixed_entity_property_accounting_flagged`.

### Account rename over time

Operators periodically rename or renumber chart-of-accounts rows. A renamed account lands in `chart_of_accounts` as a new `account_id`, while the historical `account_id` continues to appear in prior-period `gl_actual`. The account_mapping preserves both account_ids with rename_to pointers and effective windows, so the canonical_account_slug remains stable across the rename. Failure mode: a rename without crosswalk entry breaks the variance time series at the rename date. Mitigation: `gl_account_rename_history`.

### Reclasses and late postings

Closing entries for a period may post after the period close date. Reclasses moving balances between accounts also post after the fact. Both patterns are permitted but must carry metadata: `late_accrual_flag` on late postings, `reclass_source_account_id` on reclassifications. Failure mode: late postings change prior-period totals silently, breaking month-over-month variance. Mitigation: `gl_late_accrual_tagged` warns; downstream variance narratives flag variance deltas that move after the prior report was issued.

### Capex posted through opex codes

Capitalizable spend sometimes lands against opex accounts, usually because the capex authorization came after the invoice was coded. The `gl_capex_coded_as_opex_exception` check flags opex postings that reference a capex_project_id; the reverse (`gl_opex_coded_as_capex_exception`) flags capex-account postings that lack a capex_project_id. Both require operator review. Failure mode: silent miscoding distorts NOI, capex spend plans, and renovation-yield metrics. Mitigation: the exception flags plus the capitalization threshold referenced from org overlay.

### Multi-currency postings

Portfolios that include non-USD assets must normalize every posting to USD at a reference FX rate. The fx_rate_registry declares the rate of record per (source_currency, as_of_date). Failure mode: an unreferenced rate silently drops to zero or uses a stale rate. Mitigation: `gl_fx_currency_normalized_if_applicable` blocks landing until the rate is registered.

## Failure modes summary

| Failure | Symptom | Check |
|---|---|---|
| Unregistered entity with multiple properties | Shared costs bucket to one property | `gl_mixed_entity_property_accounting_flagged` |
| Account rename without crosswalk entry | Variance time series breaks at rename date | `gl_account_rename_history` |
| Late accrual untagged | Prior-period totals move silently | `gl_late_accrual_tagged` |
| Capex posted as opex | NOI understated; capex plan overstated | `gl_capex_coded_as_opex_exception` |
| Opex posted as capex | NOI overstated; renovation-yield distorted | `gl_opex_coded_as_capex_exception` |
| Non-USD posting without FX rate | Zero or stale USD normalization | `gl_fx_currency_normalized_if_applicable` |
| Property mapping missing on GL row | Per-property NOI distorted | `gl_missing_property_mapping` |
