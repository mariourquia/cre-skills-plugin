# Manual Sources Expanded Adapter

Status: stub
Wave: 4 (scaffold) + 5 (fill)
Domain: manual_uploads (extending existing connector)

## Role

Captures the long tail of manual file submissions that the wave-4 stack
depends on:

- TPM submissions (third-party manager monthly scorecards and quarterly packs)
- Operator monthly owner reports
- Operator variance narratives
- Bid tab workbooks (construction and services)
- Approval matrix threshold sets and authority changes
- Vendor award recommendation memos
- Escalation logs
- Operator property-level payroll summaries
- Manual property data corrections

Each file family has intake metadata, validation rules, reviewer
attestation, reconciliation rules, and canonical-object mappings.

## File family registry

See `file_family_registry.yaml` - declares 12 file families. Each entry
captures:

- `family_id`, `family_name`
- `expected_format` (xlsx | csv | pdf | email_table)
- `expected_headers` (list)
- `delivery_channel` (sftp | shared_drive | email | portal)
- `cadence` (monthly | quarterly | event_driven | ad_hoc | weekly | annual)
- `provenance_required` (fields the landing helper must capture)
- `staleness_threshold_days` (numeric; cites
  `reference/normalized/schemas/reconciliation_tolerance_band.yaml`)
- `target_canonical_object` (from `_core/ontology.md`)

## Canonical-object mapping

See `normalized_contract.yaml` - maps each file family to its target
canonical object shape with precedence (primary/secondary/tertiary),
primary key transform, required canonical fields, null-handling, and
derived-vs-computed field attribution. Canonical schemas under
`../../../normalized/schemas/` and `_core/schemas/` remain the contract;
this adapter only supplies data.

## Source-of-truth claims

Per `../../_core/stack_wave4/source_of_truth_matrix.md`:

| Object | Role | When primary | Notes |
|---|---|---|---|
| variance_explanation | primary | always | Manual narrative on Intacct actuals; unbacked narrative blocks |
| escalation_event | primary | always | Manual sole source |
| approval_threshold_policy | primary | always | Approval matrix workbook canonical |
| approval_request | primary | when manual branch | Vendor award memos, policy exceptions |
| staffing_position | primary | when no hr_payroll feed | Secondary when hr_payroll lands |
| tpm_scorecard | primary | always | TPM file drop; appfolio_drift flag if TPM on AppFolio |
| owner_report_bundle | primary | always | Emailed monthly bundle |
| bid_comparison (construction) | secondary | until Procore covers | Double-award blocks |
| bid_comparison (services) | primary | always | No Procore pattern for services contracts |
| source_record_audit (manual correction) | primary | always | Override governance |

## Workflows activated

See `workflow_activation_additions.yaml`:

- `third_party_manager_scorecard_review` (primary; TPM submissions)
- `owner_approval_routing` (primary; approval matrix)
- `executive_operating_summary_generation` (contributing)
- `budget_build` (contributing; operator staffing plans)
- `capital_project_intake_and_prioritization` (contributing; bid tabs)
- `monthly_property_operating_review` (contributing; operator monthly
  reports)
- `bid_leveling_procurement_review` (contributing; bid tab workbooks)

## Quality and reconciliation

- `dq_rules.yaml` - blockers, warnings, info rules (prefix `msx_`)
- `reconciliation_checks.yaml` - >= 15 reconciliation checks (prefix
  `ms_recon_`)
- `reconciliation_rules.md` - narrative companion; cites tolerance
  bands from `reference/normalized/schemas/reconciliation_tolerance_band.yaml`
- `edge_cases.md` - >= 16 known edge cases with detection and handling

Reconciliation pairings:

- Manual <-> Intacct for `variance_explanation`
- Manual <-> AppFolio for TPM scorecard drift
- Manual <-> Excel for analyst override vs benchmark refresh
- Manual <-> Procore for bid tab vs bid_package

## Crosswalks

See `crosswalk_additions.yaml` - fragments for merging into:

- `../../master_data/property_master_crosswalk.yaml` (operator property
  codes -> canonical property_id)
- `../../master_data/employee_crosswalk.yaml` (TPM submitted_by ->
  canonical owner identity)
- `../../master_data/vendor_master_crosswalk.yaml` (bid tab bidder name
  -> canonical vendor_id)

## Sample data

See `sample_files/` - synthetic CSV samples (fictional names) covering:

- `tpm_submission_monthly_report_2026_03.csv`
- `operator_variance_narrative_2026_03.csv`
- `bid_tab_construction_2026_03.csv`
- `approval_matrix_threshold_set_2026_03.csv`
- `escalation_log_2026_03.csv`
- `operator_payroll_summary_2026_03.csv`
- `manual_property_correction_2026_03.csv`

## Runbooks

- `runbooks/manual_sources_onboarding.md` - file delivery setup,
  template version pinning, sign-off model, analyst override workflow,
  refresh cadence enforcement
- `runbooks/manual_common_issues.md` - per-incident runbook covering
  file naming drift, missing as_of, missing signature, template version
  drift, cross-file inconsistency, late variance narratives,
  retroactive approval-matrix changes, multi-property splits,
  cell-typed-as-text, TPM drift, late TPM submission, payroll without
  roster, bid-tab leveling incomplete, analyst override without refresh

## Tests

- `tests/test_manual_sources_adapter.py` - pytest coverage of manifest
  conformance, file_family_registry validity, sample-file header match,
  dq_rules format, reconciliation_checks ms_recon prefix, and
  crosswalk_additions fragment shape
