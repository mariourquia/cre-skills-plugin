# Manual Sources Expanded - Onboarding Runbook

Purpose. Step-by-step for onboarding a new manual file family (or a new
submitter within an existing family) into the `manual_sources_expanded`
adapter. Covers delivery-channel setup, template version pinning, the
sign-off model, the analyst override workflow, and refresh cadence
enforcement.

Audience. `data_platform_team` (primary), `regional_ops_director` or
`asset_mgmt_director` depending on file family (business owner).

## 1. Pre-onboarding intake

1. Confirm the file family is registered in
   `file_family_registry.yaml`. If not, add an entry first (requires
   review by `data_platform_team`). Every entry declares `family_id`,
   `expected_format`, `expected_headers`, `delivery_channel`, `cadence`,
   `provenance_required`, `staleness_threshold_days`,
   `target_canonical_object`.
2. Confirm the target canonical object is declared in
   `normalized_contract.yaml` with `precedence`, `primary_key`,
   `required_canonical_fields`, and `null_handling`.
3. Confirm the `source_id` for the submitter is in
   `source_registry_entry.yaml` (or create a new source row).

## 2. File delivery channel setup

Each `delivery_channel` has its own setup:

### shared_drive

- Assign a drop path: `shared_drive://manual_uploads/<family_id>/<region>/`
  (or `/<property_code>/` for per-property files).
- Grant `read` to `data_platform_team` service account.
- Grant `write` to the submitting role (operator, TPM contact, analyst).
- Configure the landing watcher to poll the drop path at the cadence
  declared in `file_family_registry.yaml`.

### email_drop

- Configure inbox `manual_uploads+<family_id>@<domain>`.
- Add a routing rule: attachments matching `expected_format` forward to
  the landing helper.
- Reply-to is the submitter's email; bounce-back on format mismatch.

### sftp

- Provision SFTP credentials scoped to `/<family_id>/<region>/`.
- Rotate passphrases per security policy.

### portal

- Web-upload form submits the file plus a structured envelope
  (submitted_by, as_of_date, signed_off). Envelope fields feed
  provenance directly; no envelope = reject at upload.

## 3. Template version pinning

Manual files drift. Pinning the template prevents silent schema
evolution.

1. Record the template version in the file_family registry entry via
   the `expected_headers` list. Version bumps are additive; a removal
   or rename is a breaking change and requires a new `family_id` or a
   major version bump with a deprecation window.
2. Publish a canonical template file (xlsx or csv skeleton) under
   `reference/connectors/manual_uploads/file_templates/<family_id>/`.
   Submitters copy this file rather than editing the previous month's
   submission.
3. The landing helper validates the header row against
   `expected_headers`. Mismatches route the file to
   `_rejected/<YYYY>/<MM>/` with an operator-readable log entry naming
   the expected and observed headers.
4. When a template bump is required (new field, renamed field), follow
   the `_core/change_log_conventions.md` process: draft, review,
   effective-date, announce to submitters. Allow a deprecation window
   during which both the old and new template are accepted.

## 4. Sign-off model

Required reviewers per file family live in the registry. Some families
(`tpm_submission_monthly_report`, `operator_owner_report`,
`approval_matrix_threshold_set`) require `signed_off = true` and a
named reviewer before promotion. Others (`escalation_log`,
`operator_variance_narrative` without owner-report linkage) are
submitted-only.

1. Submitter completes the file and toggles `signed_off = true` (or
   affixes signature on PDF for `vendor_award_recommendation`).
2. The landing helper validates `signed_off = true` AND reviewer role
   resolves to a known role in `_core/approval_matrix.md`.
3. Files that require sign-off but land without it are quarantined with
   a `missing_signature` log entry. See
   `runbooks/manual_common_issues.md::missing_signature`.

## 5. Analyst override workflow

Manual files occasionally override values from other sources (Excel
benchmarks, AppFolio rollups, Intacct actuals). Overrides are
governed, not arbitrary.

1. Submitter fills a `manual_property_correction` row with `object_type`,
   `object_id`, `field_changed`, `prior_value`, `new_value`,
   `rationale`, `requested_by`, `approver`, `approved_date`.
2. The landing helper validates `approver` is non-null and maps to a
   known role. Corrections without approver reject.
3. Reconciliation checks compare the override vs the original-source
   value:
   - `ms_recon_correction_vs_excel_benchmark` for Excel-sourced fields.
   - (future) per-source override checks for AppFolio and Intacct.
4. Within-band overrides promote with confidence reduced. Out-of-band
   overrides require a benchmark refresh OR a `policy_exception_ref`
   per `_core/approval_matrix.md`.
5. Every promoted override is logged to `source_record_audit` for
   traceability.

## 6. Refresh cadence enforcement

Each family has a `cadence` and a `staleness_threshold_days`. Cadence
enforcement prevents silent staleness.

1. The landing watcher tracks `last_landed_at` per `(family_id,
   source_id)`.
2. When the cadence window closes without a landing, a reminder is sent
   to the submitter role.
3. When the staleness threshold is exceeded, an escalation fires to
   the business owner role:
   - `tpm_*` families escalate to `asset_mgmt_director`.
   - `operator_*` families escalate to `regional_ops_director`.
   - `approval_matrix_*` escalates to `cfo_finance_leader`.
4. Repeat staleness (three consecutive periods) triggers a TPM
   contract-compliance review per the
   `third_party_manager_scorecard_review` workflow.

## 7. Cut-over validation

Before promoting a new family to active:

1. Submit at least three consecutive period files that pass all
   `dq_rules.yaml` blockers.
2. Reconciliation checks run clean or within expected-band tolerance.
3. Downstream workflows consuming the family's output confirm
   compatibility (e.g., owner_approval_routing consumes
   approval_matrix_threshold_set).
4. `data_platform_team` advances the adapter status from `stub` to
   `starter`, then `production` per
   `../../adapter_lifecycle.md`.

## 8. Decommissioning

When a source retires (operator changes, TPM contract ends, system
replaced):

1. Set `effective_end` on the `source_registry_entry` row.
2. Set `effective_end` on any crosswalk rows sourced from this system
   (see `crosswalk_additions.yaml`).
3. Archive the last 12 months of files to
   `reference/raw/manual_uploads/_archive/<family_id>/`.
4. Update `file_family_registry.yaml` if the family is fully
   retired.

## Cross-references

- `file_family_registry.yaml` - registry of recognized families
- `normalized_contract.yaml` - canonical object shapes
- `reconciliation_checks.yaml` - blockers and warnings
- `reconciliation_rules.md` - narrative companion
- `edge_cases.md` - known quirks
- `runbooks/manual_common_issues.md` - per-incident runbooks
- `../../adapter_lifecycle.md` - status progression
- `../../master_data/identity_resolution_framework.md` - crosswalk conventions
- `_core/approval_matrix.md` - role registry and approval thresholds
