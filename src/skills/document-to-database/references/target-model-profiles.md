# Target-Model Profiles

The five database adapters the family can map a canonical payload into. Defined in `src/calculators/ingest/profiles.py` and consumed by the target-model calculators: `map_to_target_model` (proves the payload fits and reports per-table row counts), `emit_sql_ddl` (reviewable `CREATE TABLE` DDL), and `emit_load_plan` (FK-ordered, upsert-keyed load order). Each profile is a declarative table catalog where a table entry is `{grain, primary_key, columns:[(name, sql_type, nullable)], foreign_keys, load_order}`.

A profile describes a TARGET WAREHOUSE schema. It is NOT the prototype runtime's staging schema — see the boundary note at the end.

## The five profiles

### `raw_landing` — audit tier
One table, `cre_raw_extraction_record`: one row per extracted record with the raw payload preserved (`jsonb`), a `document_hash`, and the full provenance superset. Use it when the requirement is an immutable, replayable record of exactly what arrived, before any normalization is trusted. This is the tier a compliance or audit reviewer reads to reconstruct an ingestion.

### `normalized_relational` — application entities (the cash-flow spine)
The relational realization of the spine: `cre_fund`, `cre_property`, `cre_document`, `cre_unit`, `cre_tenant` (pseudonymized), `cre_lease`, `cre_charge_schedule`, `cre_account`, `cre_account_mapping`, `cre_operating_statement_line`, plus the run/governance tables `cre_ingestion_run`, `cre_validation_issue`, `cre_human_review_item`, and `cre_reconciliation_result`. Foreign keys enforce the spine (a charge line references its lease, a lease references its unit and tenant, an operating-statement line references its property and canonical account). Use it when the destination is the operational application that serves the cash-flow spine to underwriting and asset-management workflows.

### `star_schema` — analytics
Conformed dimensions (`dim_property`, `dim_tenant`, `dim_lease`, `dim_unit`, `dim_account`, `dim_charge_code`, `dim_time`, `dim_document`) and grain-explicit facts (`fact_lease_charge` at lease x charge x period, `fact_operating_statement` at property x account x period x line_type, `fact_reconciliation_variance` at property x dimension x period). Use it when the destination is a BI / analytics layer that slices income, expense, and variance across properties and time.

### `data_vault` — enterprise lineage
Hubs (business keys), links (relationships), and satellites (descriptive, hash-diffed attributes): `hub_property` / `hub_tenant` / `hub_lease` / `hub_unit` / `hub_account` / `hub_charge_code` / `hub_document`; links such as `link_tenant_lease`, `link_lease_unit`, `link_charge_code_account`, and `link_rent_roll_t12_reconciliation`; satellites such as `sat_lease_terms`, `sat_charge_schedule`, `sat_document_extraction`, and `sat_validation_results`. Use it when the destination is an enterprise warehouse that must track full historical lineage and source attribution across loads.

### `hybrid_recommended` — the default composition
Not a new table set: a composition of `raw_landing` -> `normalized_relational` -> `star_schema`, with the vault as an opt-in addition for enterprises that need lineage. Land raw for audit, normalize into the spine for the application, project a star for analytics. This is the recommended default because it preserves the audit trail, serves the application, and feeds analytics from one ingestion without forcing a premature single-model choice.

## Choosing a profile

| If the destination is... | Use |
|---|---|
| an immutable audit / replay record | `raw_landing` |
| the operational app serving the cash-flow spine | `normalized_relational` |
| a BI / analytics layer | `star_schema` |
| an enterprise warehouse needing full lineage | `data_vault` |
| a general-purpose deal/data-room pipeline | `hybrid_recommended` (default) |

## What the three emitters do

- **`map_to_target_model`** resolves the profile to its catalog, maps the payload's records/leases/units/accounts/issues/reconciliation into the profile's tables, and reports `{row_count, sample_row}` per table plus a summary (`table_count`, `tables_populated`, `total_rows_mapped`). It is the proof that the payload maps cleanly before any DDL is emitted.
- **`emit_sql_ddl`** emits Postgres `CREATE TABLE IF NOT EXISTS` statements in FK-target-before-referrer order, with primary keys and (for relational/star/vault) foreign-key constraints. It NEVER emits DML — no `INSERT`/`UPDATE`/`DELETE`/`DROP`/`TRUNCATE`. The output is a specification a human reviews and applies; it does not execute. Only the `postgres` dialect is supported today.
- **`emit_load_plan`** emits the table load order (every FK target precedes its referrer), the upsert keys (the primary key) per table, and each table's dependencies, with a `topologically_valid` flag. It is a plan, not an execution.

## The staging boundary (read this before assuming the DDL runs)

The emitted DDL is target-WAREHOUSE DDL and is NOT executed by the prototype runtime. The prototype's staging tables are a deliberately flatter, foreign-key-free, session-scoped subset, because the serverless Postgres HTTP driver runs one statement per round-trip and the house staging schema carries no foreign keys. The emitters say so in their own output note. Treat the profiles as the shape a downstream warehouse should adopt, not as something the prototype will create for you.
