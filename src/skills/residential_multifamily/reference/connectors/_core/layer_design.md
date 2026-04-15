# Layer Design - raw, normalized, derived

This document specifies the three-layer data model that every connector feeds.
The contract is the same across all eight connectors: `pms`, `gl`, `crm`, `ap`,
`market_data`, `construction`, `hr_payroll`, `manual_uploads`.

## Core claim

Data moves in exactly one direction: `raw → normalized → derived`. Each layer
has a narrower purpose, a stricter contract, and a different set of allowed
writers and readers than the one before it. Promotion between layers is gated.
Regression from a later layer back to an earlier layer is forbidden.

## Layer one - raw

**Purpose.** Preserve source evidence exactly as received. Raw is the audit
trail. Every record that ever drove a downstream number is reproducible from
raw.

**Contents.** Source-of-truth inbound records. One physical file per source
system per extraction event. CSV, JSON, or JSONL.

**File naming.** `reference/raw/<connector_domain>/<YYYY>/<MM>/<source>__<as_of>.{csv|json|jsonl}`

- `connector_domain` is one of `pms`, `gl`, `crm`, `ap`, `market_data`,
  `construction`, `hr_payroll`, `manual_uploads`.
- `source` is the operator-facing source label (e.g., `east_region_pms`,
  `property_manager_report_q2`).
- `as_of` is `YYYY-MM-DD`, the date the data represents.

**Provenance fields required on every record.**

- `source_name` (string)
- `source_type` (enum: connector domain)
- `source_date` (date)
- `extracted_at` (timestamp, UTC preferred, original offset preserved if present)
- `extractor_version` (string: semver or content hash)
- `source_row_id` (string: stable row identifier inside the source system)

Missing provenance fields cause landing rejection to
`reference/raw/<connector>/_rejected/<YYYY>/<MM>/` with a reason code.

**Status transitions.** Raw has two states per file:

- `landed` - file accepted at landing; provenance complete; file unmodified.
- `quarantined` - file rejected at landing or found malformed during mapping;
  file preserved under `_rejected/`; reason logged.

Raw files never transition to `processed` or `deleted`. Raw is immutable after
landing. The immutability rule has exactly two exceptions, both externally
authored:

1. A legal retention policy that requires removing personally identifying
   information. Removal is logged to `manual_correction_log.yaml` with approver
   metadata. The file is replaced with a redaction stub, not deleted.
2. A confirmed secret leakage. The file is redacted in place, the original is
   shredded, and a change entry is appended to the lineage record.

**Allowed writers.** The operator's ingestion adapter. No connector code writes
raw. No skill pack writes raw. No agent writes raw without a manual
correction entry.

**Allowed readers.** The normalization pass. Audit tooling.
`tests/test_connector_contracts.py`. Humans during incident review. No skill
pack reads raw directly.

## Layer two - normalized

**Purpose.** A clean, schema-conforming working layer. Every field conforms to
a canonical type. Every enum value belongs to the canonical set. Every primary
key is unique. Every row carries lineage back to raw.

**Contents.** One logical entity per file (or table). Field names conform to
the canonical ontology (`_core/ontology.md`). Row identities resolved against
the master data layer.

**File naming.** `reference/normalized/<entity>__<scope>.<csv|jsonl>`

- `entity` is a canonical object slug: `lease`, `unit`, `charge`, `work_order`,
  `staffing_plan`, etc. (from the ontology.)
- `scope` is the aggregation axis if any: `portfolio`, `<market>_mf`,
  `<property_id>`, etc.

**Provenance fields required on every row.**

Everything in raw, plus:

- `normalized_version` (semver stamp of the mapping and schema pair used)
- `lineage_manifest_id` (FK into the lineage index)
- `identity_resolution_status` (enum: `resolved`, `proposed`, `unresolved`)
- `as_of_date` (required; copied or derived from raw)

**Status transitions.** Normalized records carry a row-level status:

- `pending_validation` - mapped but not yet validated.
- `valid` - passes schema and contract validation.
- `quarantined` - fails a mapping or contract rule; row isolated with a reason
  code; not promoted to derived.
- `superseded` - replaced by a later row for the same primary key; retained for
  lineage.
- `manually_corrected` - a manual correction rewrote specific fields; entry in
  `manual_correction_log.yaml` is required.

**Allowed writers.** The normalization pass only. Manual correction applies
only through the manual-correction workflow and leaves a log entry.

**Allowed readers.** All skill packs that declare the path in their
`reference_manifest.yaml`. The derived pass. Reconciliation checks. Tests.

## Layer three - derived

**Purpose.** Computed, versioned values that downstream skills consume as
benchmarks, target bands, and roll-ups. Derived outputs are reproducible from
normalized inputs plus the transformation version.

**Contents.** Target bands by role, scope, and segment; blended weights;
rolling-window aggregations; scorecard baselines; market benchmark rollups.

**File naming.** `reference/derived/<category>__<scope>.<csv|jsonl>`

- `category` matches the subsystem's sixteen reference categories.
- `scope` is the aggregation axis.

**Provenance fields required on every row.**

- `derived_from_manifest_ids` (array of lineage manifest ids)
- `transformation_version` (semver stamp of the recipe that produced the row)
- `reference_assumptions_used` (array of {path, as_of, confidence})
- `computed_at` (timestamp)
- `confidence` (enum: `low`, `medium`, `high`)

**Status transitions.** Derived rows carry a status:

- `proposed` - newly recomputed; awaiting approval if delta crosses a
  configured threshold vs. prior.
- `approved` - accepted for skill consumption.
- `deprecated` - superseded by a later recomputation; preserved for audit.
- `withdrawn` - removed because inputs changed in a way that invalidates the
  row before a replacement exists; skills fallback to prior.

**Allowed writers.** The derived recomputation pass only. Approvals are logged
to `benchmark_update_log.yaml` per this directory's schema.

**Allowed readers.** Skill packs that declare the path in their manifest.
Reporting templates. Market refresh workflows. Approval routing (threshold
lookups).

## Promotion gates

Promotion between layers is not automatic. Each step has a gate.

### raw → normalized gate

All of the following must pass, or the row does not enter normalized:

1. Provenance completeness (every required provenance field present).
2. Schema validation (types, required fields, enum membership).
3. Mapping contract validation (every non-optional source field has a target).
4. Identity resolution status set (`resolved` or `proposed`; `unresolved` rows
   are quarantined).
5. DQ blocker checks pass (null-critical, duplicate primary key, unit-count
   reconciliation, lease-status reconciliation; applicable checks only).

Warnings (severity: `warning`) do not block promotion but do emit exceptions
per `exception_taxonomy.md`.

### normalized → derived gate

All of the following must pass, or derived does not recompute for the affected
scope:

1. Reconciliation checks pass at blocker severity for the input scope
   (record count, budget vs actual alignment, commitment vs CO vs draw, etc.).
2. Input freshness check passes (no required input older than its staleness
   ceiling).
3. Reference assumptions are current (no cited assumption is in `deprecated`
   status).
4. Transformation version exists and is not withdrawn.

A failing gate leaves the derived row in its prior state and emits an
exception. Skills read the prior row and surface the confidence level.

## Idempotency and re-ingest

Every landing is idempotent by `source_name` + `source_date` + `extracted_at`.
Re-ingest of an unchanged file is a no-op and writes no new raw artifact. Re-
ingest of a changed file - same `source_name` + `source_date` but newer
`extracted_at` - writes a new raw file and does not overwrite the prior.

At the normalized layer, late-arriving or corrected rows supersede prior rows
per the entity's dedup rule (see `raw_to_normalized_design.md`). The superseded
row is retained with status `superseded` and a pointer to the successor.

At the derived layer, recomputation is idempotent on inputs. If inputs are
unchanged, derived recomputation yields identical bytes and does not emit a new
change entry.

## Immutability of raw

Raw is write-once. A record landed in raw is never modified in place. The
mechanism:

- The filesystem (or object store) is configured with retention locks where
  possible.
- Tests check raw file checksums against the lineage manifest. A mismatch
  triggers an incident.
- The two sanctioned exceptions (PII retention removal, secret shredding) go
  through `manual_correction_log.yaml` with explicit approver metadata. The
  file stub remains; the lineage record tracks the removal.

Violation of raw immutability is a severity-critical incident. Normalized and
derived outputs that depend on violated raw are flagged and recomputed from
the retained lineage where possible.

## Flow diagram

```
 source system or file drop
         │
         ▼
 ┌───────────────────┐         rejection path
 │ landing adapter   │────────────────────────────┐
 │  - provenance     │                            │
 │  - checksum       │                            ▼
 └───────────────────┘                    reference/raw/<domain>/_rejected/
         │
         ▼
 reference/raw/<domain>/<YYYY>/<MM>/<source>__<as_of>
         │          (immutable)
         ▼
 ┌───────────────────────────────────────────────┐
 │ raw → normalized gate                         │
 │  - schema validate                            │
 │  - mapping contract                           │
 │  - type coerce                                │
 │  - enum map                                   │
 │  - identity resolve                           │
 │  - provenance attach                          │
 │  - DQ blocker checks                          │    quarantine path
 └───────────────────────────────────────────────┘─────────────────────┐
         │ pass                                                        │
         ▼                                                             ▼
 reference/normalized/<entity>__<scope>               reference/normalized/_quarantine/
         │
         ▼
 ┌───────────────────────────────────────────────┐
 │ normalized → derived gate                     │
 │  - reconciliation checks pass                 │
 │  - input freshness                            │
 │  - assumptions current                        │
 │  - transformation version valid               │
 └───────────────────────────────────────────────┘
         │ pass
         ▼
 reference/derived/<category>__<scope>
         │
         ▼
 skill packs (read-only via reference_manifest.yaml)
```

## Worked example - a PMS lease record moving through the layers

**Input.** A PMS vendor exports a lease row into a JSONL file at
`reference/raw/pms/2026/04/east_region_pms__2026-04-15.jsonl`. The row carries
source-side fields `LeaseKey`, `PropCode`, `Unit`, `StartDt`, `EndDt`,
`LeasedMoRent`, `Status`, and the required provenance fields.

Status: `sample`.

**Raw layer.**

```json
{
  "LeaseKey": "L-0009881",
  "PropCode": "HG1",
  "Unit": "204",
  "StartDt": "20250815",
  "EndDt": "20260814",
  "LeasedMoRent": "1850.00",
  "Status": "OCC",
  "source_name": "east_region_pms",
  "source_type": "pms",
  "source_date": "2026-04-15",
  "extracted_at": "2026-04-15T04:12:33Z",
  "extractor_version": "adapter-0.4.2",
  "source_row_id": "east_region_pms::lease::L-0009881"
}
```

The file is immutable after landing. Checksum stored in the lineage manifest.

**raw → normalized gate.** Every provenance field present. Schema validation
converts `StartDt` and `EndDt` from `YYYYMMDD` to ISO date per
`normalization_patterns.md`. `LeasedMoRent` coerces to a numeric rent field
(units tracked as operator base currency per month). `Status` maps from source
enum `OCC` to canonical `occupied`. Identity resolution matches `PropCode=HG1`
to `Property.property_id=hg1_columbus_oh` via `master_data/`. All DQ blockers
pass.

**Normalized layer.**

```csv
lease_id,property_id,unit_id,lease_start_date,lease_end_date,monthly_rent_base_currency,status,as_of_date,normalized_version,lineage_manifest_id,identity_resolution_status,row_status
l_east_region_pms_0009881,hg1_columbus_oh,hg1_unit_204,2025-08-15,2026-08-14,1850.00,occupied,2026-04-15,pms-lease-0.3.1,lm_2026_04_15_pms_east_region_00017,resolved,valid
```

Status: `sample`.

**normalized → derived gate.** For `rent_growth_renewal` or
`blended_lease_trade_out` at the property scope, the lease row joins with
prior-lease rows and lease-event rows. Reconciliation checks pass (unit count
matches, lease status sum matches unit count, charge records reconcile to
payments within tolerance). Derived `rent_growth_renewal__hg1_columbus_oh`
is recomputed.

**Derived layer.** A row in `reference/derived/rent_growth_renewal__hg1_columbus_oh.csv`
is updated with `transformation_version=rent-growth-0.2.0`,
`derived_from_manifest_ids=[lm_2026_04_15_pms_east_region_00017]`,
`computed_at=2026-04-15T05:02:11Z`, and `confidence=high`. Status: `proposed`
until approved (or auto-approved if the delta vs prior is below the configured
threshold per `benchmark_update_log.schema.yaml`).

At no point is a dollar or percent figure written into prose. Numbers live in
data files. Prose references the files by path.
