# Reconciliation Rules: manual_sources_expanded

Narrative companion to `reconciliation_checks.yaml`. Every numeric tolerance
cites `reference/normalized/schemas/reconciliation_tolerance_band.yaml`. No
hardcoded dollar or percent values live in this document; they live in the
band schema and are referenced by slug.

Canonical source-of-truth claims for this adapter derive from
`../../_core/stack_wave4/source_of_truth_matrix.md`. Manual is **primary**
for `variance_explanation`, `escalation_event`, `approval_request` (manual
branch), `staffing_position` (when no `hr_payroll` feed), and
`approval_threshold_policy`. Manual is **secondary** for TPM-derived
`lease / charge / payment / work_order` (when TPM is on a shared PMS) and
for `bid_comparison` (when Procore covers the scope).

## Manual <-> Intacct (variance_explanation on actuals)

A manual variance narrative lives on top of Intacct actuals. When the
narrative arrives without the underlying Intacct actual line, the variance
is unbacked and the narrative cannot promote.

- `ms_recon_variance_vs_intacct` (blocker): every `variance_explanation`
  row must reference a `budget_line_id` resolved via
  `master_data/account_crosswalk.yaml` to a known Intacct account with a
  posted actual in the matching `period`.
- `ms_recon_variance_amount_matches` (warning within band; blocker outside
  band): the narrative's `variance_amount` must reconcile to
  `actual - budget` for the referenced budget line. Drift within
  `variance_match_band` reduces confidence to `medium`; drift beyond
  blocks. Tolerance cited, not hardcoded.
- `ms_recon_variance_period_alignment` (blocker): the narrative `period`
  must match the Intacct posting period. Cross-period narratives are not
  accepted here; they must be restated via
  `manual_property_correction`.

## Manual <-> AppFolio (TPM scorecard drift)

When the TPM also reports on AppFolio, a drift check compares the TPM
scorecard vs the AppFolio-native rollup. Drift outside band reduces
confidence on downstream workflows that consume TPM numbers
(`third_party_manager_scorecard_review`,
`executive_operating_summary_generation`).

- `ms_recon_tpm_occupancy_vs_appfolio` (warning within band; blocker
  outside band): `occupancy_physical` from the TPM submission vs the
  AppFolio-computed occupancy for the same `(property_id, period)` must
  sit within `tpm_occupancy_drift_band`. Tolerance cited, not hardcoded.
  Known degradation: TPM submissions lag AppFolio by up to the staleness
  threshold; drift is sampled at `as_of_date` of TPM submission, not real
  time.
- `ms_recon_tpm_collections_vs_appfolio` (warning): `collections_rate`
  from the TPM submission vs AppFolio-computed collections for the same
  period must sit within `tpm_collections_drift_band`. Drift beyond
  band reduces confidence.
- `ms_recon_tpm_lag_enforcement` (warning): the
  `submitted_date - period_end` gap must not exceed the TPM submission
  cadence plus `tpm_submission_band`. Enforced by `msx_tpm_submission_lag`
  in `dq_rules.yaml`.

## Manual <-> Excel (analyst benchmark drift)

When a manual correction updates a value that is also sourced from an
Excel benchmark (e.g., a turn cost library row), the two must reconcile.

- `ms_recon_correction_vs_excel_benchmark` (warning within band; blocker
  outside band): any `manual_property_correction` row that modifies a
  field sourced from an Excel benchmark must stay within
  `analyst_override_band` of the benchmark value. Drift outside band
  requires the operator to either (a) file a benchmark refresh or (b)
  attach a policy exception via `approval_request`.
- `ms_recon_correction_refresh_link` (warning): a correction pointing at
  an Excel-sourced field must carry a `refresh_ref` or a
  `policy_exception_ref`. Missing both routes to the exception queue.

## Manual <-> Procore (bid tab vs bid_package)

Manual bid tabs are secondary to Procore `bid_package` for in-scope
projects. Reconciliation prevents dual-awarded scopes.

- `ms_recon_bidtab_vs_procore` (blocker): a manual `bid_tab_construction`
  row for a project that also has a Procore `bid_package` cannot promote
  until Procore is retired for that scope OR the Procore bid_package is
  closed. Double-awarding is a governance blocker.
- `ms_recon_bidtab_leveling_complete` (blocker): a recommendation row
  carrying `recommended_award = true` must have complete leveling notes.
  Rows without `leveling_notes` cannot promote.
- `ms_recon_bidtab_rationale_present` (blocker): a recommendation row
  carrying `recommended_award = true` must have a
  `recommendation_rationale`. Empty rationale blocks.

## Approval matrix effective-dating

Approval matrix threshold sets are effective-dated. Retroactive changes
are allowed only with a paired authority_change row citing the prior row
in `change_log_ref`.

- `ms_recon_approval_matrix_effective_dating` (blocker): no
  `approval_matrix_threshold_set` row may have `effective_start` earlier
  than the latest prior row's `effective_end` unless the change is paired
  with an `approval_matrix_authority_change` row referencing it.
- `ms_recon_approval_change_has_log` (blocker): every change to an
  existing threshold set must carry a `change_log_ref`. Changes without
  a log reference block.

## Escalation log completeness

Escalations without an owner cannot promote. Every row must resolve
`routed_to` to a known role.

- `ms_recon_escalation_has_owner` (blocker): `routed_to` must be non-null
  and map to a known role in the org overlay.

## Promotion gate

Landing promotes from `reference/raw/manual_uploads/` to
`reference/normalized/` only when all blocker checks in
`reconciliation_checks.yaml` pass. Warning-level failures log and allow
promotion but reduce `confidence` to `medium` on downstream output.
Info-level failures report and do not gate.
