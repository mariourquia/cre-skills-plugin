# Source Registry

The source registry is the canonical list of every inbound data source known to the residential multifamily subsystem. Each entry describes what a source is, who owns it, how it lands, how often it updates, what canonical objects it carries, and what its current lifecycle status is. The registry sits immediately adjacent to the connector contracts (see `../README.md`) but answers a different question:

- A **connector** defines what a *class* of feed (pms, gl, crm, ap, market_data, construction) must look like.
- A **source** is a *specific* instance of that class (for example, an operator-owned PMS instance, a shared-drive budget drop, a particular market-data subscription), tagged with operational metadata.

The registry is vendor-neutral. It names vendor families in a hint file (`vendor_family_hints.md`) for orientation, but it carries no credentials, endpoints, tokens, or secrets. Access configuration lives in the operator's deployment environment.

## Purpose

1. Track every integrated or proposed source system in a single inventory.
2. Force each source to declare an owner (data, business, technical) so QA failures have a named responder.
3. Classify each source by PII, financial, and legal sensitivity so downstream tooling can apply the correct handling rules.
4. Feed audit and lineage reports: every record that reaches the normalized layer must point back to a registry entry.
5. Serve as the hand-off artifact when a stub source transitions to an active adapter.

## How operators register a new source

1. Draft a registry entry that conforms to `source_registry.schema.yaml`. Pick a `source_id` that is snake_case, stable across environments, and describes the feed in one phrase (for example, `east_region_pms`, `fund_a_gl_export`, `market_rent_comps_primary`).
2. Assign the three ownership roles: `data_owner` (accountable for data quality), `business_owner` (accountable for the business use of the data), and `technical_owner` (accountable for the adapter and credentials).
3. Set `status` to `planned` if the integration has not been built yet, `stubbed` if the connector contract exists but no live adapter is running, `active` when the live adapter has passed an initial reconciliation window, `degraded` when the feed is running but flagged, or `deprecated` when the feed has been retired.
4. Set `credential_method` to the placeholder matching the expected auth approach. Do not add real credentials to this file. All credential strings in the registry are placeholder labels only.
5. Set `object_coverage` to the list of canonical objects (from `_core/ontology.md`) the source carries.
6. Submit the entry through the normal change-control flow for the subsystem (see `../../../_core/BOUNDARIES.md`).

## What happens when status transitions

- `planned` to `stubbed`: the connector's contract has been written and the sample-input test passes. No live data yet.
- `stubbed` to `active`: a live adapter has landed at least one file that passes reconciliation checks for the source's domain (`../qa/`). The `last_validated_at` field is set.
- `active` to `degraded`: reconciliation checks have failed over a configured window; the source is still producing data but outputs are flagged as lower confidence. Downstream skills must handle degraded gracefully.
- `active` or `degraded` to `deprecated`: the feed is being retired. Crosswalks referencing this source must be repointed before deprecation completes, and the registry keeps the record with a `notes` entry naming the replacement.

## How the registry feeds audit and lineage

Every normalized record already carries the six provenance fields declared in `../INGESTION.md`. The `source_name` provenance value on each record MUST match a `source_id` in `source_registry.yaml`. This lets the audit layer:

- Trace any derived metric back through the normalized layer to the originating source.
- Join normalized records against the registry to pick up PII / financial / legal sensitivity classifications.
- Identify which source a failing reconciliation check should notify (via the registered owners).
- Detect orphan records whose `source_name` does not resolve to a registry entry; such records are held and escalated.

## Relationship to the master data framework

The registry is an inventory of *systems*. The master data layer (`../master_data/`) is the inventory of *business records* (properties, units, leases, vendors, etc.) and their cross-source identity. The two layers are joined by the `source_id` column appearing in every master-data crosswalk row.

## No secrets rule

No file in this directory may contain credentials, tokens, hostnames, or URLs. Any appearance of such values is a failure of the no-secrets rule in `../../../_core/BOUNDARIES.md` and must be removed before the registry is committed. Placeholder strings declare only the *kind* of credential a source uses (for example, `api_key_placeholder`, `sftp_key_placeholder`).
