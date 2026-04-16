# Lineage - provenance and version tracking

Every row that reaches the normalized or derived layer must be traceable back
to a source system, an extraction event, and a versioned transformation. This
document specifies the lineage model, the log schemas, and the approval
metadata that apply across all eight connectors: `pms`, `gl`, `crm`, `ap`,
`market_data`, `construction`, `hr_payroll`, `manual_uploads`.

## What lineage covers

Lineage answers these questions for any cell in any normalized or derived
file:

1. Which source system or file did this value come from?
2. When was it extracted, and what does it claim its as_of_date is?
3. Which version of the mapping produced the normalized row?
4. Which version of the derived transformation produced the derived value?
5. Which reference assumptions were in force when the row was computed?
6. Who approved any non-deterministic choices (mapping overrides, benchmark
   changes, manual corrections, approval overrides)?

Anything not answered by lineage is undefined. Audit tooling and
reconciliation checks fail closed on undefined lineage.

## Provenance model

The provenance model has four nested objects.

### Source identity

Every record - raw, normalized, derived - carries a source identity block.

- `source_system_or_file`: one of
  - `connector_domain://<source_name>` for system feeds (e.g.,
    `pms://east_region_pms`, `hr_payroll://adp_primary`).
  - `manual_uploads://<template_slug>/<source_label>` for manager-submitted
    files (e.g., `manual_uploads://monthly_financial_report/property_manager_tpm_a`).
- `source_row_id`: stable identifier within the source system or file.
- `source_date`: the date the source claims the data represents.
- `extracted_at`: the timestamp the extraction event completed.
- `extractor_version`: semver or content hash of the adapter or file-drop
  template.

### Extraction identity

- `extraction_id`: deterministic hash of `source_system_or_file` +
  `source_date` + `extracted_at` + `extractor_version`.
- `extraction_timestamp`: UTC; preserves original offset in a side field if
  the source supplied one.
- `file_checksum`: SHA-256 of the raw landing artifact.

### Normalization identity

- `normalized_version`: semver of the mapping and schema pair that produced
  the normalized row.
- `mapping_checksum`: SHA-256 of the active `mapping.yaml` at the time of the
  run.
- `schema_checksum`: SHA-256 of the active `schema.yaml` at the time of the
  run.
- `identity_resolution_status`: `resolved`, `proposed`, or `unresolved`.

### Derived identity

Applies only to derived rows.

- `transformation_version`: semver of the derivation recipe.
- `transformation_recipe_checksum`: SHA-256 of the recipe definition.
- `derived_from_manifest_ids`: array of `manifest_id` values for the
  normalized inputs that fed the derivation.
- `reference_assumptions_used`: array of `{path, as_of, confidence}` objects;
  records which reference files were cited and their state at the time of the
  derivation.
- `approver_metadata`: optional; present when the recipe or a benchmark
  update required human approval.

## Lineage manifest

The lineage manifest is the canonical index that ties a run to its inputs and
outputs. One manifest is emitted per transformation event (normalization or
derivation). Manifests are append-only.

See `lineage_manifest.schema.yaml` for the formal schema.

### Required fields

- `manifest_id`: unique identifier. Pattern: `lm_<yyyy_mm_dd>_<connector>_<source>_<sequence>`.
- `produced_by`: slug of the producer - `pass:raw_to_normalized`,
  `pass:recompute_derived`, or `correction:manual`.
- `produced_at`: UTC timestamp.
- `source_system_or_file`: as above.
- `extraction_timestamp`: as above.
- `as_of_date`: the effective date of the data the manifest covers.
- `normalized_version`: required for normalization manifests.
- `transformation_version`: required for derived manifests.
- `reference_assumptions_used`: array; may be empty for normalization-only
  manifests.
- `approver_metadata`: optional.
- `notes`: free-text; short.

### Example manifest

```yaml
manifest_id: lm_2026_04_15_pms_east_region_00017
produced_by: pass:raw_to_normalized
produced_at: 2026-04-15T05:01:08Z
source_system_or_file: pms://east_region_pms
extraction_timestamp: 2026-04-15T04:12:33Z
as_of_date: 2026-04-15
normalized_version: pms-lease-0.3.1
transformation_version: null
reference_assumptions_used: []
approver_metadata: null
notes: routine nightly landing; all blockers passed; zero quarantine.
status: sample
```

## Transformation versioning scheme

All transformations are versioned with `<scope>-<name>-<major>.<minor>.<patch>`.

- **Scope.** The data surface the transformation operates on.
  - `pms-lease`, `gl-actual`, `ap-invoice`, etc., for normalized mappings.
  - `rent-growth`, `collections`, `capex-variance`, etc., for derived recipes.
- **Name.** Optional second-level grouping when the scope is shared by several
  transformations.
- **Version.** Semver.
  - `major` changes on incompatible schema or recipe changes; old outputs are
    deprecated.
  - `minor` changes on additive changes (new optional fields, new optional
    rule branches).
  - `patch` changes on bug fixes that do not alter expected outputs on the
    golden path.

A new transformation version lands with:

1. A migration plan in `change_log.md` of the affected pack or connector.
2. A benchmark recomputation for any derived outputs that depend on it.
3. A lineage manifest per recomputed scope.
4. An entry in `benchmark_update_log.yaml` if the transformation change causes
   derived values to shift beyond the configured delta threshold.

## Benchmark update log

Every change to a derived benchmark or assumption is logged. The log is
append-only and lives at
`reference/connectors/_core/benchmark_update_log.yaml` at the subsystem level
(or under a per-scope directory for large corpora).

See `benchmark_update_log.schema.yaml` for the formal schema.

### Required fields

- `update_id`: pattern `bu_<yyyy_mm_dd>_<category>_<sequence>`.
- `category`: which reference category the update affects.
- `scope`: the scope axis (market, submarket, segment, form, etc.).
- `prior_values_path`: path to the prior file or snapshot.
- `new_values_path`: path to the new file.
- `as_of_date`: effective date.
- `source`: provenance tag for the new values.
- `confidence`: `low`, `medium`, `high`.
- `reason_for_change`: short prose.
- `proposed_by`: agent or role slug.
- `approved_by`: human approver slug or role.
- `affected_skills`: array of skill pack slugs whose manifests include the
  changed paths.
- `rollback_path`: where to find the prior snapshot if a rollback is needed.

## Source schema change log

Connectors track source schema changes that affect mapping. Schema drift is a
first-class event - not a silent remap.

The log lives at `reference/connectors/<domain>/source_schema_change_log.yaml`
per connector.

Required fields:

- `change_id`: pattern `sc_<yyyy_mm_dd>_<connector>_<sequence>`.
- `source_system_or_file`: as above.
- `change_type`: `field_added`, `field_removed`, `field_renamed`,
  `type_changed`, `enum_added`, `enum_removed`, `enum_renamed`,
  `primary_key_changed`, `grain_changed`.
- `detected_at`: UTC timestamp.
- `detected_by`: `schema_drift_check`, `manual_review`, `vendor_notice`.
- `prior_definition`: snapshot.
- `new_definition`: snapshot.
- `mapping_action_required`: boolean.
- `remediation_plan_ref`: path to the change plan.
- `status`: `open`, `mapping_updated`, `waived`, `closed`.

## Mapping override log

When a mapping requires a non-default transformation (e.g., a specific
vendor's `Y/N` column maps to boolean in a non-standard way), the override is
logged.

See `mapping_override_log.schema.yaml` for the formal schema.

## Manual correction log

When a specific row is corrected by a human outside the mapping pipeline, the
correction is logged.

Log lives at `reference/connectors/_core/manual_correction_log.yaml`.

Required fields:

- `correction_id`: pattern `mc_<yyyy_mm_dd>_<entity>_<sequence>`.
- `target_layer`: `raw` (rare; only for sanctioned PII or secret cases),
  `normalized`, or `derived`.
- `target_path`: absolute repo-relative path of the file corrected.
- `target_row_id`: primary key of the affected row.
- `corrected_fields`: object mapping `field_name` to `{prior, new}`.
- `reason`: short prose.
- `requested_by`: agent or role slug.
- `approved_by`: human approver slug.
- `effective_at`: UTC timestamp of the correction.
- `rollback_plan`: how to reverse if needed.
- `downstream_recompute_required`: boolean.
- `recompute_scope`: array of affected derived paths.

## Approval override log

When an approval matrix threshold is overridden for a specific event (e.g., an
emergency vendor dispatch above the normal threshold), the override is
logged.

Log lives at `reference/connectors/_core/approval_override_log.yaml`.

Required fields:

- `override_id`: pattern `ao_<yyyy_mm_dd>_<workflow>_<sequence>`.
- `workflow_slug`: the canonical workflow the approval served.
- `approval_request_id`: the approval request identifier.
- `canonical_threshold_path`: path to the canonical threshold file.
- `org_threshold_path`: path to the org-scoped threshold file if present.
- `override_amount_direction`: `higher` or `lower` than normal (no figures in
  prose - the files carry the numbers).
- `reason`: short prose.
- `requested_by`: role slug.
- `approved_by`: role slug.
- `effective_window`: object with `start_at` and `end_at` timestamps.
- `audit_trail_link`: path or external id.

## Approver metadata

When any of the above logs carries an `approved_by` value, it resolves to an
approver record. Approver records live in the org overlay
(`overlays/org/<org_id>/approvers.yaml`) and carry:

- `approver_id`: slug.
- `name`: preferred display name.
- `role`: one of the canonical role slugs.
- `contact`: opaque identifier (email, internal id); stored at org scope, not
  in canonical core.
- `active`: boolean.
- `effective_window`: optional date range.

The integration layer never stores approver PII in the lineage manifests -
only the `approver_id` reference. PII stays in the org overlay and is governed
by its retention policy.

## Change history for benchmark and reference refreshes

Benchmark and reference refreshes are the highest-churn lineage events. The
history model:

1. A proposed refresh lands in `reference/normalized/` or
   `reference/derived/` as a row with `status: proposed`.
2. If the delta vs prior crosses the configured threshold, an approval request
   opens. Threshold per category is configured in
   `overlays/org/<org_id>/approval_matrix.yaml` and defaults from
   `_core/approval_matrix.md`.
3. On approval, the row transitions to `status: approved`. A
   `benchmark_update_log.yaml` entry is written.
4. The prior row transitions to `status: deprecated` and is moved to
   `reference/archives/` with a `change_log_entry` linking both.
5. Skill packs whose `reference_manifest.yaml` names the affected path are
   logged as potentially-impacted.

Rollback:

1. A rollback request references the `update_id` in
   `benchmark_update_log.yaml`.
2. The approved row transitions to `deprecated`. The prior row moves from
   archives back to active with status `approved`.
3. A new `benchmark_update_log.yaml` entry is written with
   `change_type: rollback` and a reference to the reversed `update_id`.
4. Affected derived recomputations run.

## Rules that must always hold

- Every normalized row has a `lineage_manifest_id`. No exceptions.
- Every derived row has a non-empty `derived_from_manifest_ids` array.
- Every approved benchmark update has a `benchmark_update_log.yaml` entry
  and, where applicable, an `approver_id`.
- Every manual correction has a `manual_correction_log.yaml` entry.
- Raw file checksums match the lineage manifest. Mismatches are
  severity-critical exceptions.
- Lineage manifests are append-only. Corrections are new manifests, not edits.
