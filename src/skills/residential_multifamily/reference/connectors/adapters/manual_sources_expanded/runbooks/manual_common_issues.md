# Manual Sources Expanded - Common Issues Runbook

Per-incident guidance for the `manual_sources_expanded` adapter. Each
section names the symptom, the detection, the immediate remediation, and
the follow-up action. Cross-references cite
`reconciliation_checks.yaml`, `dq_rules.yaml`, and
`edge_cases.md`.

## File naming drift

**Symptom.** Operator submits a file named
`TPM_Monthly_Mar2026_v2_FINAL_RF.xlsx` instead of the expected pattern
`tpm_submission_monthly_report__<property_code>__2026-03.xlsx`.

**Detection.** Landing watcher fails filename regex match; file routes
to `_rejected/<YYYY>/<MM>/` with an `unknown_family` log entry.

**Immediate remediation.** `data_platform_team` renames the file to
match the pattern (or manually re-drops via the portal with a
filename override). The content is unchanged.

**Follow-up.** Reach out to submitter with the canonical filename
convention. If drift is chronic, pin a filename regex at the email-drop
or SFTP level so the landing helper rejects at intake rather than after
parsing.

## Missing as_of

**Symptom.** File parses but the `as_of_date` column or envelope field
is blank.

**Detection.** `dq_rules.yaml::msx_provenance_envelope` blocks.

**Immediate remediation.** If the file cover page or filename carries an
implied as_of (e.g., `2026-03` in filename), the landing helper stamps
`as_of_date` from the filename convention declared in the family
registry. If the filename also lacks a date, reject the file.

**Follow-up.** Instruct submitter to populate either the cell or the
filename date. Update the template skeleton to highlight the `as_of_date`
field.

## Missing signature

**Symptom.** File lands with `signed_off = false` or blank. Applies to
`tpm_submission_monthly_report`, `operator_owner_report`,
`approval_matrix_threshold_set`.

**Detection.** `normalized_contract.yaml` null-handling rejects.
`dq_rules.yaml::msx_attestation_required` backs it.

**Immediate remediation.** File holds in `_rejected/_pending_signature/`.
Notify the designated reviewer role; they either sign via the portal or
the submitter re-submits with sign-off.

**Follow-up.** Three consecutive unsigned submissions across one
property escalates to `asset_mgmt_director`. Persistent non-signing on
the TPM side may trigger `third_party_manager_scorecard_review` workflow
and contract-compliance review.

## Template version drift

**Symptom.** Operator uses last quarter's template. Header row differs
from `expected_headers`.

**Detection.** `dq_rules.yaml::msx_template_version_check` (added via
the family registry) rejects.

**Immediate remediation.** Reject the file with a log entry naming the
expected header list and the observed deviation. Point submitter at the
canonical template at
`reference/connectors/manual_uploads/file_templates/<family_id>/`.

**Follow-up.** If the operator's workflow is tied to the old template,
allow a 30-day deprecation window during which both templates are
accepted. After the window, revert to strict rejection.

## Cross-file inconsistency

**Symptom.** `operator_variance_narrative` for `(ASH-CLT-001, 2026-03,
6120-turn-expense)` cites `variance_amount = 5640.00`, but the Intacct
actuals for the same key show `variance = 4890.00`.

**Detection.** `reconciliation_checks.yaml::ms_recon_variance_amount_matches`
fires; drift outside `variance_match_band` blocks.

**Immediate remediation.** Operator restates the narrative to reconcile.
If the Intacct actual is wrong (posting error), a
`manual_property_correction` row is filed against the Intacct line
after a journal entry correction is approved.

**Follow-up.** Log the episode in the change_log for audit. If drift is
endemic for one property (consistent mis-keying on account codes),
schedule a reviewer refresh with the submitter.

## Late-submitted variance narrative

**Symptom.** Narrative arrives after the owner report has already been
distributed.

**Detection.** `as_of_date + staleness_threshold_days < received_at` on
`dq_rules.yaml::msx_freshness_per_family`.

**Immediate remediation.** Late narrative lands with `confidence = low`
and is flagged `out_of_cycle`. Owner report that went out without it is
NOT retracted; an addendum is issued via
`manual_property_correction` if the variance is material.

**Follow-up.** Repeated late narratives escalate to
`regional_ops_director` to address the root cause (close-process
bottleneck, reviewer availability, etc.).

## Approval-matrix retroactive change risk

**Symptom.** New `approval_matrix_threshold_set` lands with
`effective_start = 2026-01-01` on April 20, 2026, and no paired
`approval_matrix_authority_change` row.

**Detection.** `reconciliation_checks.yaml::ms_recon_approval_matrix_effective_dating`
blocks.

**Immediate remediation.** File holds in `_rejected/_pending_log_ref/`.
Operator attaches the authority_change row with the governance log
reference, or shifts `effective_start` to the landing date.

**Follow-up.** Review any approvals granted between the intended
`effective_start` and the landing date. Approvals that would have been
out-of-threshold under the new rules are flagged for retroactive review
by `cfo_finance_leader`.

## Multi-property file with missing rows

**Symptom.** A `operator_owner_report` bundle is supposed to cover 3
properties; the landing shows only 2.

**Detection.** Row-count check vs the operator's declared coverage list
in the bundle envelope. `dq_rules.yaml::msx_partial_period_flag` fires.

**Immediate remediation.** File lands with a `partial_coverage` flag.
Missing property's row is requested from the submitter. Downstream
workflows (variance review, owner report generation) run on the
partial set with a visible note.

**Follow-up.** If partial coverage persists across periods for the same
property, escalate to `regional_ops_director` for operator outreach.

## Cell-value-typed-as-text in numeric column

**Symptom.** `bid_tab_construction.base_bid` arrives as `"184,200"`
(string) rather than `184200` (number). Excel formatted the cell as
text.

**Detection.** Numeric-coercion step in the landing parser logs a
coercion warning (if coercion succeeds) or a coercion error (if the
value is true non-numeric).

**Immediate remediation.** Parser strips thousands separators and
currency symbols, then parses as number. Coerced rows promote with a
`type_coercion_note`. Non-numeric values (`"TBD"`, `"see attached"`)
reject the row.

**Follow-up.** Update the template skeleton to pre-format numeric
columns as Number. Submitter training on xlsx cell formatting.

## TPM drift beyond band

**Symptom.** TPM-reported occupancy drifts from AppFolio rollup by
several percentage points.

**Detection.** `reconciliation_checks.yaml::ms_recon_tpm_occupancy_vs_appfolio`
fires with drift outside `tpm_occupancy_drift_band`.

**Immediate remediation.** Route to `asset_mgmt_director`. Pull the
underlying rent roll from AppFolio and the TPM-submitted roster; align
definitions (physical vs economic, exclude-model vs include-model).
Restate whichever side was definitionally wrong.

**Follow-up.** If drift is structural (operator uses a different
occupancy definition), codify the definition in the
`third_party_manager_oversight.md` and update the reconciliation band
or disable the check for that property with documented exception.

## Late TPM submission

**Symptom.** `tpm_submission_monthly_report` for March 2026 lands April
28, 2026 (past 10-day staleness threshold).

**Detection.** `dq_rules.yaml::msx_tpm_submission_lag` warning.

**Immediate remediation.** File still lands; confidence on derived
metrics is set to `medium`. Escalation email to `asset_mgmt_director`.

**Follow-up.** Three consecutive late submissions trigger
`third_party_manager_scorecard_review` workflow and a TPM contract
compliance review.

## Payroll without roster

**Symptom.** `operator_payroll_summary` lands with
`total_labor_cost` populated but no employee-level roster backing the
summary exists in `hr_payroll`.

**Detection.** Absence of matching `hr_payroll_payroll_summary` row
observed at downstream reconciliation.

**Immediate remediation.** Summary promotes with `confidence = medium`
and `staffing_position.roster_pending = true`. Workflows consuming the
staffing_position (budget_build) operate with the summary but flag the
roster-pending state.

**Follow-up.** Operator supplies the roster in the next submission
cycle (or via a dedicated `hr_payroll` feed if the operator subscribes).
Persistent gap routes to `hr_director` for follow-up.

## Bid-tab leveling incomplete

**Symptom.** `bid_tab_construction` recommendation with
`leveling_notes = ""` or blank.

**Detection.** `reconciliation_checks.yaml::ms_recon_bidtab_leveling_complete`
blocks.

**Immediate remediation.** Award cannot promote. Construction lead
re-submits with leveling notes describing normalizations applied
(insulation R-value alignment, warranty terms harmonization,
alt-bid quantity match).

**Follow-up.** If leveling is chronically missing, review the
construction-lead workflow and consider a template revision that
mandates the leveling_notes field.

## Analyst override without refresh

**Symptom.** `manual_property_correction` updates a capex_cost_library
value outside `analyst_override_band` with no `refresh_ref` attached.

**Detection.** `reconciliation_checks.yaml::ms_recon_correction_refresh_link`
fires; `ms_recon_correction_vs_excel_benchmark` fires outside band.

**Immediate remediation.** Correction holds pending either (a) a paired
benchmark refresh submission for the Excel source, or (b) a
`policy_exception_ref` linked to an approved `approval_request`.

**Follow-up.** If this is a one-off analyst override that reflects a
real policy change, the operator should file a benchmark refresh. If
it's a genuine exception, an approval_request with policy_exception
subject closes the loop.

## Unknown family / mis-dropped file

**Symptom.** File lands at a drop location that does not correspond to
any registered `family_id`, or with a filename that matches no family
pattern.

**Detection.** Landing watcher routes to `_rejected/_unknown_family/`.

**Immediate remediation.** `data_platform_team` reviews the file,
classifies it, and either (a) re-drops at the correct location, or (b)
initiates a new family registration if this is a new intake stream.

**Follow-up.** If a submitter is consistently mis-dropping, reach out
to clarify the drop convention.

## Cross-references

- `reconciliation_checks.yaml` - reconciliation blockers and warnings
- `reconciliation_rules.md` - narrative companion
- `dq_rules.yaml` - data-quality blockers, warnings, info
- `edge_cases.md` - catalog of known edge cases
- `manual_sources_onboarding.md` - step-by-step onboarding guide
- `file_family_registry.yaml` - registry of recognized families
- `normalized_contract.yaml` - canonical object mappings
- `../../master_data/unresolved_exceptions_queue.md` - exception queue for unresolved rows
