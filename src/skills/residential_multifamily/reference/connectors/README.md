# Connectors — Vendor-Neutral Ingestion Layer

This layer defines the contract every inbound data source must satisfy before records are allowed to land in the 16-category reference system (`reference/raw/`, `reference/normalized/`, `reference/derived/`). See `reference/README.md` for the category catalog and `_core/BOUNDARIES.md` for how the connector layer sits relative to core canon and overlays.

## What a connector is

A connector is a named, scoped interface definition for a single class of inbound feed (PMS, GL, CRM, AP, market-data, construction). It specifies the entities the source emits, their required fields, primary keys, provenance, null handling, dedup logic, and the reconciliation checks that must pass before downstream metrics consume the records.

A connector is **not**:

- Live vendor code. This directory carries no Yardi, Entrata, MRI, RealPage, Procore, NetSuite, Sage, or Salesforce calls, credentials, or URLs.
- A data pipeline. The connector defines the contract; the operator implements the adapter and lands files under the convention described in `INGESTION.md`.
- A schema registry for derived metrics. Derived benchmarks live in `reference/derived/` and are recomputed after connector QA passes.

Every connector in this directory carries `vendor_neutral: true` and `status: stub` until a concrete operator forks a vendor adapter under its own path (e.g., a future `connectors/pms/vendors/<vendor>/` layout — out of scope for this pass).

## Scope of this directory

Six domain connectors are defined:

| Domain | Purpose |
|---|---|
| `pms/` | Property-management-system feeds — rent roll, leases, lease events, charges, payments, delinquency, leads, tours, applications, work orders, turns. |
| `gl/` | General-ledger feeds — chart of accounts, account mapping, actuals, budget, forecast, variance, capex actuals, commitments. |
| `crm/` | Prospect and resident CRM — lead interactions, campaign sources, resident communications, service requests, follow-ups. |
| `ap/` | Accounts-payable — vendor master, invoices, contracts, commitments, purchase orders, payment status. |
| `market_data/` | External benchmarks — rent comps, concession observations, occupancy, payroll, labor, materials, utility references. |
| `construction/` | Dev and major-renovation project data — development budgets, estimate line items, bid packages, commitments, change orders, draw requests, schedule milestones, punch items. |

Each connector directory provides the same shape:

```
<domain>/
├── README.md                       narrative and scope
├── manifest.yaml                   connector identity (vendor_neutral: true, status: stub)
├── schema.yaml                     per-entity contracts (grain, primary key, required fields, provenance)
├── mapping.yaml                    raw-column → normalized-column mapping template
├── sample_input.json               vendor-agnostic raw sample (tagged status: sample)
├── sample_normalized.json          what the sample looks like after mapping
├── reconciliation_checks.yaml      domain-specific QA checks
└── tests/
    ├── test_manifest.py            schema-conformance test
    └── test_sample_normalizes.py   golden-path + negative-case test
```

Cross-domain QA checks (record count, duplicate PK, null-critical, date coverage, unit-count, lease-status, budget-actual, commitment / CO / draw) live in `qa/` and are referenced by each connector's `reconciliation_checks.yaml`.

## Raw → normalized → derived flow

1. **Raw.** The operator lands a file under `reference/raw/<domain>/<YYYY>/<MM>/<source>__<as_of>.{csv,json,jsonl}`. Provenance fields (`source_name`, `source_type`, `source_date`, `extracted_at`, `extractor_version`, `source_row_id`) are required on every record. See `INGESTION.md`.
2. **Normalized.** `mapping.yaml` is applied per entity. The result conforms to `schema.yaml` and lands in `reference/normalized/<entity>__<scope>.csv` (or `.jsonl` for nested shapes). Primary keys are deduplicated per the entity's dedup rule; late-arriving records supersede prior per `as_of_date`.
3. **QA.** `reconciliation_checks.yaml` runs deterministic checks; results are written to a `reconciliation_report.json` attached to the landing. Blocker checks prevent promotion to derived; warnings are logged.
4. **Derived.** Downstream benchmarks (`reference/derived/*.csv`) recompute only after domain QA passes.

## Integration with the 16-category reference system

Connectors feed the reference system; they do not replace it. The 16 reference categories (see `reference/README.md`) describe the **output** shape skills read; connectors describe the **input** shape operators land. Many normalized entities (e.g., `market_data/rent_comp`) map 1:1 to a reference category; others (e.g., `pms/lease`) are operational records the subsystem uses directly without a derived-benchmark step.

The contract every connector must honor is captured in `_schema/connector_manifest.schema.yaml`, `_schema/entity_contract.schema.yaml`, and `_schema/reconciliation_check.schema.yaml`. Tests under each connector's `tests/` directory enforce conformance.
