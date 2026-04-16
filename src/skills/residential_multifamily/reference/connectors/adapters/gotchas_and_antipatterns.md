# Gotchas and Antipatterns: Cross-Cutting Warnings

Rules that apply to every adapter under
`reference/connectors/adapters/`, regardless of vendor family.

## Do not silently overwrite canonical schemas

Adapters are ergonomic overlays. They do not redefine canonical field
names, entity shapes, enums, or reconciliation checks.

- An adapter mapping hint that suggests a canonical field name different
  from what is declared in the matching `connector_kind/schema.yaml`
  should fail review. The canonical schema wins, every time.
- An adapter that wants to expose a field the canonical schema does not
  yet carry must raise a canonical-schema amendment request. Adapters
  never fork canonical fields into their own private naming.
- If an operator's vendor emits a column that the canonical schema
  treats as illegal, the column is dropped during normalization. The
  adapter records the drop in an ingest log, not by mutating the
  canonical contract.

## Do not hardcode credentials

No adapter file under this tree carries a live credential. Ever.

- No API keys, tokens, OAuth client secrets, SFTP keys, passwords.
- No hostnames that resolve to live systems.
- No inbox addresses that receive real traffic.
- `credential_method` in `source_registry.yaml` is a placeholder label,
  never a credential value.
- `author_metadata.authored_by` is a role slug or a team label. It is
  not a personal identifier; do not embed emails.

Credentials live in the operator's deployment environment (secret
manager, vault, Kubernetes secret, etc.). The subsystem is cloud-agnostic.

## Do not bury vendor-specific logic in shared normalization

Shared normalization code (transforms, validators, reconciliation
checks) must remain vendor-neutral.

- Vendor-specific parsing, field coercion, or enum flattening goes in
  the adapter's `mapping_template.yaml` only.
- If a vendor quirk requires a new transform, it lives in the adapter
  directory as a named transform with a stable slug, not as an inline
  conditional in shared code.
- A transform that branches on vendor family is an antipattern. Replace
  it with per-adapter transforms and a shared default.

## Do not skip provenance

Every record, at every stage, carries the six canonical provenance
fields: `source_name`, `source_type`, `source_date`, `extracted_at`,
`extractor_version`, `source_row_id`. Adapters do not drop or rename
these fields.

- Synthetic stubs carry provenance stubs with placeholder values.
- Starter and production data carry real provenance values drawn from
  the operator's extraction pipeline.
- If a vendor payload lacks a natural `source_row_id`, the adapter
  constructs one deterministically from stable fields and documents the
  construction rule in the adapter `README.md`.

## Do not let adapter names leak into canonical outputs

Canonical records do not carry adapter slugs, vendor family names, or
adapter version strings. Provenance tracks source system, not adapter.

- `source_type` in provenance is the canonical connector kind (`pms`,
  `gl`, `crm`, `ap`, `market_data`, `construction`, `hr_payroll`,
  `manual_uploads`), not the adapter slug.
- `source_name` is the source system's slug from the source registry
  (for example, `east_region_pms`), not the adapter slug.
- If downstream consumers need to know which adapter was in play, that
  is a debug-log concern, not a canonical-record concern.

## Common vendor-family gotchas

These are orientation examples; the per-adapter README files carry the
authoritative list for each family.

- PMS exports: model units missing, mixed unit-status taxonomies,
  concessions as credits vs negative rent, unit-number suffix
  conventions (`-A`, `-B`, `.01`), future-lease rows inconsistently
  present.
- GL exports: multi-entity consolidation rolls, account-rename history,
  late accruals landing in the wrong period, capex-opex coding drift.
- CRM exports: duplicate leads from channel cross-posting, merged
  leads losing source attribution, offline touches not represented in
  the pipeline, inconsistent lead-source taxonomies, timezone
  ambiguity on tour timestamps.
- AP exports: duplicate vendors across legacy and current systems,
  credit memos silently reversing posted invoices, partial payments
  split across pay runs, shared contracts touching multiple properties,
  missing property assignment leaving invoices unallocated.
- Market data: conflicting sources for the same comp, stale comps
  where the underlying lease is months old, outlier rents from broker
  puffery, missing submarket tags requiring internal mapping.
- Construction: multiple budget versions in flight, owner vs contractor
  contingency commingled, pending vs approved change orders blurred,
  draw timing lagging actual work, rehab and opex coding mixed.
- Excel / manual uploads: merged cells, blank rows, inconsistent
  column headers, embedded charts, macros, multi-sheet references,
  template drift across properties.
- HR / payroll: employees shared across properties, temp staff
  outside payroll feeds, overtime not tagged to property, vacant
  budgeted roles not filled, contractor labor in separate feeds,
  PII minimization required.

## Antipattern: treating adapters as production credentials

Adapters document how a vendor-family payload is expected to look. They
do not ingest data. An adapter is code-free in this subsystem; the
operator's ingestion service reads the adapter files as configuration
and applies them. If an operator finds themselves writing credentials
into an adapter file to make ingestion work, something is wrong with
the deployment environment, not the adapter.

## Antipattern: one mega-adapter per vendor

Each adapter maps one vendor family to one canonical connector. A
vendor that serves multiple canonical domains (for example, a platform
that carries PMS and CRM and AP together) gets multiple adapters, one
per canonical domain. This keeps the adapter-to-canonical overlay
clean and makes lifecycle gates per-domain.

## Antipattern: skipping the stub stage

New adapters enter at `stub` regardless of how well the author knows
the vendor. The stub stage forces sample payloads, mapping hints, and
gotchas to be written down where the next operator can read them,
which is the whole point of the adapter layer.
