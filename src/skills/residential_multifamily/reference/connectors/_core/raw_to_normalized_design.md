# Raw to Normalized - Transformation Design

The standardized pipeline pattern every connector follows when promoting raw
records to normalized records. The pipeline is deterministic, auditable, and
fail-closed. The same pattern applies to all eight connectors: `pms`, `gl`,
`crm`, `ap`, `market_data`, `construction`, `hr_payroll`, `manual_uploads`.

## Pipeline stages

The pipeline has seven ordered stages. Each stage can halt a row (move to
quarantine), emit an exception, or pass the row to the next stage.

1. Input format validation.
2. Provenance completeness check.
3. Field mapping.
4. Type coercion.
5. Enum mapping.
6. Identity resolution.
7. Provenance attachment and normalization stamp.

A row that passes all seven enters `reference/normalized/`. A row that fails
any of them enters `reference/normalized/_quarantine/` with a reason code.

## Stage 1 - input format validation

**Purpose.** Confirm the raw artifact is machine-readable and matches the
declared format before parsing rows.

**Checks.**

- File extension matches connector's declared format (csv, json, jsonl).
- File is valid in that format (CSV parses, JSON parses, JSONL has no
  malformed lines).
- File is not empty.
- File size is within the operator's configured bounds.
- File checksum (SHA-256) matches the lineage manifest if the manifest was
  pre-registered during landing.

**Outcome.** A malformed file halts the pipeline. No rows are attempted. An
exception of category `schema_drift` or `dq_blocker` is emitted per
`exception_taxonomy.md`. The file is not moved; remediation replaces the raw
artifact.

## Stage 2 - provenance completeness

**Purpose.** Confirm every row carries the required provenance fields before
mapping begins. Rows without complete provenance never enter the mapping
stage; they quarantine with reason `provenance_incomplete:<field>`.

**Required fields.** `source_name`, `source_type`, `source_date`,
`extracted_at`, `extractor_version`, `source_row_id`. (See `lineage.md`.)

**Outcome.** Incomplete rows are written to
`reference/normalized/_quarantine/<connector>/<entity>/<YYYY>/<MM>/` with the
reason code. Complete rows pass to Stage 3.

## Stage 3 - field mapping

**Purpose.** Apply the connector's `mapping.yaml` to translate source fields
to canonical fields per `field_mapping_template.md`.

**Behavior.**

- Every mapping entry with `required_for_load: true` must produce a non-null
  canonical value (after type coercion in Stage 4). A null at that boundary
  quarantines the row with reason `required_field_null:<canonical_field>`.
- Unmapped source fields are logged (informational) but do not block.
- Optional source fields that are absent pass through as null.
- Vendor-specific overrides (`<connector>/vendors/<vendor>/mapping.yaml`)
  apply where present and leave a `mapping_override_log.yaml` entry.

**Outcome.** The row now holds a canonical field set, possibly with
unresolved types and unmapped enums. Pass to Stage 4.

## Stage 4 - type coercion

**Purpose.** Cast each canonical field to the declared canonical type per
`normalization_patterns.md`.

**Behavior.**

- Dates: parse to ISO date.
- Datetimes: parse to UTC; preserve offset if the field is a
  `datetime_with_offset` variant.
- Money: parse to decimal, apply FX conversion against `fx_rates` table,
  emit paired base/source/fx fields.
- Numbers: coerce to canonical precision per the schema.
- Booleans: apply `boolean_map`.
- Text: apply `canonicalize_text_identifier` or `canonicalize_text_display`
  per the field rule.

**Outcome.** A row with typed canonical values. Type-coercion failures
quarantine with reason `type_coerce_failed:<canonical_field>:<source_value>`.
Pass to Stage 5.

## Stage 5 - enum mapping

**Purpose.** Translate source enums to canonical enums per
`normalization_patterns.md` "Enum mapping with unknown-value handling."

**Behavior.**

- Every `enum_map` rule is applied.
- Unmapped source values quarantine the row with reason
  `enum_value_unmapped:<canonical_field>:<source_value>`. A
  `source_schema_change_log.yaml` entry is appended with
  `change_type: enum_added` if the value is net-new.
- State-carrying fields with paired columns (`<name>` and `<name>_state`) are
  populated per their rule.

**Outcome.** A row with canonical enum values. Pass to Stage 6.

## Stage 6 - identity resolution

**Purpose.** Resolve source-side identifiers to canonical identifiers against
the master data layer (`reference/connectors/master_data/`).

**Behavior.**

- Each `identity_resolve_reference` rule looks up the resolver-defined
  source keys in the declared crosswalk file and writes the target canonical
  id.
- Resolution outcomes:
  - `resolved` - an exact match exists. Canonical id written. Row proceeds.
  - `proposed` - a partial or fuzzy match exists and the resolver's
    `on_unresolved: propose` rule allows. Canonical id is written as a
    proposed id and the row carries `identity_resolution_status=proposed`. A
    proposed entry is added to `identity_resolution_proposals.yaml` for
    human review.
  - `unresolved` - no acceptable match. Row quarantines with reason
    `identity_unresolved:<object>:<source_key>` unless the resolver's
    `on_unresolved: quarantine` is overridden (overrides are rare and
    require an entry in `mapping_override_log.yaml`).

**Outcome.** A row with canonical ids and an identity resolution status. Pass
to Stage 7.

## Stage 7 - provenance attachment and normalization stamp

**Purpose.** Attach the final provenance block and stamp the normalization
version.

**Behavior.**

- Attach `lineage_manifest_id` produced by the run (the manifest is emitted
  at run start and referenced by every row).
- Attach `normalized_version` (semver from the active `mapping.yaml` +
  `schema.yaml` pair).
- Attach `mapping_checksum`, `schema_checksum`, and `extractor_version`.
- Set `row_status=valid`.
- Write the row to `reference/normalized/<entity>__<scope>.<csv|jsonl>`.
  Dedup logic from the entity's rule in `mapping.yaml` applies; superseded
  rows are retained with `row_status=superseded`.

**Outcome.** The row is queryable by skill packs, reconciliation checks, and
the derived recomputation pass.

## Rejection and quarantine policy

Quarantined rows stay under
`reference/normalized/_quarantine/<connector>/<entity>/<YYYY>/<MM>/` until the
underlying cause is remediated:

- **Bad data at source.** The operator fixes the source and re-ingests. The
  new raw artifact produces a new normalized row. The quarantined row is left
  in place as evidence.
- **Mapping gap.** The mapping is updated, a new normalized run is triggered,
  and the quarantined rows re-flow through the pipeline.
- **Identity crosswalk gap.** The crosswalk is updated and the run is
  re-triggered.

Quarantined rows never silently disappear. They are retained for the
connector's configured retention window and then moved to long-term archive.

Blocker-level exceptions emitted during any stage are routed per
`exception_taxonomy.md`.

## Output destination

- Valid rows land in `reference/normalized/<entity>__<scope>.<csv|jsonl>`.
- Quarantined rows land in
  `reference/normalized/_quarantine/<connector>/<entity>/<YYYY>/<MM>/`.
- A per-run `normalization_report.json` lands alongside the raw artifact
  with:
  - `manifest_id`
  - `rows_attempted`
  - `rows_valid`
  - `rows_quarantined_by_reason` (object)
  - `exceptions_emitted` (array of `{category, severity, count}`)

## Idempotency

- The pipeline is idempotent on inputs. Running it twice on the same raw
  artifact produces identical normalized output.
- Dedup logic prevents duplicate normalized rows. The entity's dedup rule
  names the key and the tie-breaker (see `INGESTION.md`).

## End-to-end worked example - synthetic PMS lease row

**Step 0 - raw artifact landed.**

Path: `reference/raw/pms/2026/04/east_region_pms__2026-04-15.jsonl`.

Row (status: sample):

```json
{
  "LeaseKey": "L-0009881",
  "PropCode": "HG1",
  "Unit": "204",
  "StartDt": "20250815",
  "EndDt": "20260814",
  "LeasedMoRent": "1850.00",
  "Status": "OCC",
  "PetAllowed": "Y",
  "source_name": "east_region_pms",
  "source_type": "pms",
  "source_date": "2026-04-15",
  "extracted_at": "2026-04-15T04:12:33Z",
  "extractor_version": "adapter-0.4.2",
  "source_row_id": "east_region_pms::lease::L-0009881"
}
```

**Step 1 - input format validation.**

- JSONL parse: pass.
- File checksum matches manifest: pass.
- File not empty: pass.

**Step 2 - provenance completeness.**

- `source_name`, `source_type`, `source_date`, `extracted_at`,
  `extractor_version`, `source_row_id` all present: pass.

**Step 3 - field mapping.**

Canonical fields produced (interim):

- `lease.lease_external_id` ← `LeaseKey`
- `lease.property_source_code` ← `PropCode` (awaiting identity resolution)
- `lease.unit_source_code` ← `Unit` (awaiting identity resolution)
- `lease.start_date_raw` ← `StartDt`
- `lease.end_date_raw` ← `EndDt`
- `lease.monthly_rent_source` ← `LeasedMoRent`
- `lease.status_source` ← `Status`
- `lease.pets_allowed_source` ← `PetAllowed`

**Step 4 - type coercion.**

- `lease.start_date` = parse(`20250815`, `YYYYMMDD`) → `2025-08-15`: pass.
- `lease.end_date` = parse(`20260814`, `YYYYMMDD`) → `2026-08-14`: pass.
- `lease.monthly_rent_base_currency` = parse(`1850.00`, `USD`, fx=1.0) →
  `1850.00`; paired `_source_currency=USD`, `_fx_rate_to_base=1.0`: pass.

**Step 5 - enum mapping.**

- `lease.status` = enum_map(`OCC`) → `occupied`: pass.
- `lease.pets_allowed` = boolean_map(`Y`) → `true`: pass.

**Step 6 - identity resolution.**

- `lease.property_id` = resolve(`PropCode=HG1`) → `hg1_columbus_oh`: resolved.
- `lease.unit_id` = resolve(`PropCode=HG1`, `Unit=204`) → `hg1_unit_204`:
  resolved.

**Step 7 - provenance attachment and normalization stamp.**

- `lease.lineage_manifest_id` = `lm_2026_04_15_pms_east_region_00017`.
- `lease.normalized_version` = `pms-lease-0.3.1`.
- `lease.row_status` = `valid`.

**Normalized row written.**

Path: `reference/normalized/lease__portfolio.csv` (append with dedup on
`lease.lease_external_id + source_name`).

```csv
lease_id,lease_external_id,property_id,unit_id,lease_start_date,lease_end_date,lease_end_date_state,monthly_rent_base_currency,monthly_rent_source_currency,monthly_rent_fx_rate_to_base,status,pets_allowed,as_of_date,normalized_version,lineage_manifest_id,identity_resolution_status,row_status
l_east_region_pms_0009881,L-0009881,hg1_columbus_oh,hg1_unit_204,2025-08-15,2026-08-14,known,1850.00,USD,1.0,occupied,true,2026-04-15,pms-lease-0.3.1,lm_2026_04_15_pms_east_region_00017,resolved,valid
```

Status: `sample`.

**Normalization report.**

```json
{
  "manifest_id": "lm_2026_04_15_pms_east_region_00017",
  "rows_attempted": 1,
  "rows_valid": 1,
  "rows_quarantined_by_reason": {},
  "exceptions_emitted": []
}
```

Status: `sample`.

**Edge case - a quarantined sibling row.**

A second row in the same file carries `Status=CONV` (new source value). It
passes Stages 1 through 4 and fails Stage 5:

- Reason: `enum_value_unmapped:lease.status:CONV`.
- A `source_schema_change_log.yaml` entry is appended with
  `change_type: enum_added`.
- The row is written to
  `reference/normalized/_quarantine/pms/lease/2026/04/` with the reason.
- The first row (above) is unaffected and lands in the valid output.

This is the design: per-row fail-closed, pipeline-level idempotent, every
outcome traced back through lineage to its manifest. No dollar figures appear
in prose; all numeric behavior is shown in the illustrative row itself.
