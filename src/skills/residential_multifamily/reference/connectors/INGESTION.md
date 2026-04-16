# Ingestion Protocol

Canonical contract every connector in this directory must satisfy. Prose is vendor-neutral. The protocol is enforced by per-connector `tests/test_manifest.py` and `tests/test_sample_normalizes.py`, plus the family-wide `tests/test_connector_contracts.py` at the subsystem root.

## 1. Source-agnostic interface

A connector declares four artifacts and must keep them in sync:

1. `manifest.yaml` — identity, owner, version, status, entity list, required provenance fields, handshake placeholders (auth kind and access pattern). Conforms to `_schema/connector_manifest.schema.yaml`.
2. `schema.yaml` — per-entity contracts: grain, time basis, primary key, required fields, optional fields, foreign keys, null handling, status convention, provenance. Conforms to `_schema/entity_contract.schema.yaml`.
3. `mapping.yaml` — raw-column to normalized-column template per entity: source column name, normalized column name, transform rule, dedup rule, as-of handling. Missing fields fail closed; the operator either maps the field or marks it `optional_source: true`.
4. `reconciliation_checks.yaml` — list of checks; each conforms to `_schema/reconciliation_check.schema.yaml` and names a severity, inputs, invariant, and remediation.

A connector MUST NOT carry vendor credentials, API tokens, hostnames, or URLs. Those live in the operator's deployment environment. The connector's `handshake` block names only the auth kind (e.g., `api_key`, `sftp`, `file_drop`) and the access pattern (e.g., `pull_scheduled`, `push_webhook`, `manual_upload`).

## 2. Raw landing

Operators land inbound files under the convention:

```
reference/raw/<domain>/<YYYY>/<MM>/<source>__<as_of>.{csv|json|jsonl}
```

Example: `reference/raw/pms/2026/04/sample_feed__2026-04-15.jsonl`.

Every record (row in CSV, object in JSON/JSONL) MUST carry these provenance fields:

| Field | Type | Meaning |
|---|---|---|
| `source_name` | string | Operator-facing source label (e.g., `"east_region_pms"`). |
| `source_type` | string | Connector kind (`pms`, `gl`, `crm`, `ap`, `market_data`, `construction`). |
| `source_date` | date | Date the source was extracted or published. |
| `extracted_at` | timestamp | Precise extraction timestamp; used for dedup tie-breaks. |
| `extractor_version` | string | Semver or hash of the adapter that produced the file. |
| `source_row_id` | string | Stable row identifier within the source system; never null. |

A record with any required provenance field missing is rejected at landing; it is written to `reference/raw/<domain>/_rejected/<YYYY>/<MM>/` with a reason.

## 3. Normalization

The operator applies `mapping.yaml` per entity to produce normalized records in `reference/normalized/<entity>__<scope>.csv` (or `.jsonl`). Normalization rules:

- **Missing required field on the destination side.** Fail closed. Record is rejected; nothing is inferred or defaulted.
- **Missing optional field.** Pass through as null. Downstream consumers handle null per the null-handling rule declared in `schema.yaml`.
- **Unit / enum normalization.** Transform rules in `mapping.yaml` convert units (e.g., dollars → cents, percent-as-fraction → percent-as-integer) and map source enums to canonical enums. Unmapped enum values are rejected — no silent bucketing.
- **Deduplication.** Per-entity dedup rule in `mapping.yaml` names the key (`primary_key`, `primary_key + source_date`, or an explicit tuple) and the tie-breaker (`latest_extracted_at_wins`, `latest_source_date_wins`, `reject_on_conflict`).
- **As-of handling.** Each normalized record carries `as_of_date`. Late-arriving records (`extracted_at > prior_extracted_at` for same primary key but `source_date < prior_source_date`) do not overwrite unless the entity is marked `allow_backfill: true` in `mapping.yaml`.
- **Status preservation.** If a source record has a status (e.g., lease status, work order status), the mapping preserves it per the entity's `status_convention`. Status transitions that skip states (e.g., `notice → terminated` without `move_out`) are logged as warnings but not rejected.

## 4. Derived dependencies

Each normalized entity unblocks a downstream set of metrics, workflows, templates, or dashboards. A connector's `schema.yaml` SHOULD carry a `dependents` comment (informational only — not enforced) so a future agent tracing a QA failure can see what is broken upstream.

| Normalized entity (example) | Downstream users |
|---|---|
| `pms/property` | all per-property metrics; property master reconciliation; reporting roll-ups |
| `pms/unit` | occupancy rollups; unit-type weighted rents; turn planning |
| `pms/lease` + `pms/lease_event` | lease expiry schedule; renewal retention metrics; delinquency workflow |
| `pms/charge` + `pms/payment` | collections metrics; aging; delinquency workflow; variance narratives |
| `gl/actual` + `gl/budget` | budget vs actual templates; variance narratives; reporting |
| `gl/capex_actual` + `gl/commitment` | capex prioritizer skill; draw request workflow |
| `crm/lead_interaction` | lease-up war room; leasing-strategy roles |
| `ap/invoice` + `ap/contract` | vendor invoice validator skill; commitment tracking |
| `market_data/rent_comp` | comp-snapshot skill; market-rent-benchmark reference category |
| `construction/dev_budget` + `change_order` | construction command center; draw request workflow |

## 5. QA and reconciliation

Each connector's `reconciliation_checks.yaml` references one or more checks in `qa/`:

- **Record count** — raw rows (minus rejects) equal normalized rows within tolerance.
- **Duplicate primary key** — no duplicate PK in normalized output.
- **Null critical field** — critical fields (as declared in `schema.yaml`) are non-null.
- **Date coverage** — no gaps vs prior period; forward-coverage matches expected cadence.
- **Unit count reconciliation** — PMS unit count matches property master.
- **Lease status reconciliation** — occupied + vacant + notice + preleased = unit count.
- **Budget vs actual alignment** — GL budget totals reconcile with source budget.
- **Commitment + CO + draw** — construction commitment + approved change orders + cumulative draws stay consistent.

Each check emits a row in `reconciliation_report.json`:

```json
{ "check_id": "pms_unit_count_reconciles", "severity": "blocker", "status": "fail", "observed": 248, "expected": 250, "remediation_ref": "qa/unit_count_reconciliation.yaml" }
```

Blocker failures prevent promotion of the landing to `normalized/` (the normalized write is held). Warning failures log but do not block. Info checks report and do not gate.

## 6. Integration checklist for a new connector

When a future vendor adapter is forked under a connector:

1. Copy the domain connector directory to a vendor subpath (out of scope for this pass).
2. Keep `manifest.yaml` entity list unchanged; add vendor-specific `mapping.yaml` entries.
3. Extend `reconciliation_checks.yaml` with vendor-specific invariants.
4. Ensure `sample_input.json` is replaced with a sanitized vendor-shape sample (never real property data).
5. Run the connector test suite. No CI green light without tests green.
