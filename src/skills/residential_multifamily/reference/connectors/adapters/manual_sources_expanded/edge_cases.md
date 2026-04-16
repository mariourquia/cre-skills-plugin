# Manual Sources Expanded - Edge Cases

Reference catalog of known edge cases this adapter encounters in practice.
Each entry names the trigger, the detection, the handling, and the rule
or runbook that owns the response. Rule ids use the `ms_` prefix.

## 1. Variance narrative without underlying Intacct line

**Trigger.** A manual `operator_variance_narrative` row arrives for a
`(property_id, period, account_code)` that has no posted actual in Intacct.

**Detection.** `reconciliation_checks.yaml::ms_recon_variance_vs_intacct`
blocks on a missing Intacct match.

**Handling.** The narrative cannot promote. Operator waits for Intacct
close to post the actual, then resubmits. If the actual will never post
(account retired, property divested), the narrative is retired and
replaced by a `manual_property_correction` row documenting the closeout.

## 2. TPM scorecard occupancy doesn't match AppFolio

**Trigger.** A TPM submission reports `occupancy_physical = 0.942` while
the AppFolio rollup for the same `(property_id, period)` shows `0.921`.

**Detection.** `ms_recon_tpm_occupancy_vs_appfolio` fires at landing.
Drift within `tpm_occupancy_drift_band` reduces confidence to `medium`;
drift outside band blocks.

**Handling.** Known degradation: TPM lag is expected. At landing,
confidence is reduced on any downstream metric derived from the TPM
number. Beyond the band, escalation routes to `asset_mgmt_director` per
`runbooks/manual_common_issues.md::tpm_drift`.

## 3. Bid tab missing leveling

**Trigger.** A `bid_tab_construction` row carries
`recommended_award = true` but `leveling_notes` is null or blank.

**Detection.** `ms_recon_bidtab_leveling_complete` blocks.

**Handling.** Award cannot promote. Construction lead completes leveling
in-line (usually noting normalizations applied across bidders) and
resubmits. Runbook: `runbooks/manual_common_issues.md::bidtab_leveling`.

## 4. Approval threshold set effective-dated retroactively

**Trigger.** A new `approval_matrix_threshold_set` row has
`effective_start = 2026-01-01` but arrives in April 2026. The prior
threshold set has `effective_end` of `2025-12-31`. No paired
`approval_matrix_authority_change` row accompanies.

**Detection.** `ms_recon_approval_matrix_effective_dating` blocks.

**Handling.** Retroactive change without paired authority_change row is
a governance blocker. Operator either (a) attaches the authority_change
row citing `chg_log_YYYY_NNN`, or (b) shifts `effective_start` forward
to the landing date.

## 5. Escalation logged without owner

**Trigger.** An `escalation_log` row arrives with `routed_to` blank.

**Detection.** `ms_recon_escalation_has_owner` blocks.

**Handling.** Escalation without owner cannot promote. Operator assigns
a `routed_to` role before resubmission. Default routing fallback is
`regional_ops_director` for operational kinds, `general_counsel` for
legal, `cfo_finance_leader` for financial_threshold.

## 6. Payroll summary missing employee detail

**Trigger.** An `operator_payroll_summary` row arrives for
`(property_id, period, role_slug)` with `headcount_fte = 1.0` and
`total_labor_cost` populated but no backing employee-level roster has
been provided.

**Detection.** The adapter permits the summary row to land, but the
downstream `hr_payroll_reconciliation_workflow` cannot calibrate because
employee-level detail is absent. Confidence is set to `medium`.

**Handling.** `runbooks/manual_common_issues.md::payroll_no_roster`.
Operator supplies the roster in the next submission cycle. Until then,
staffing_position rows derived from this summary are flagged
`roster_pending`.

## 7. Manual correction overriding canonical without approver

**Trigger.** A `manual_property_correction` row arrives with `approver`
blank.

**Detection.** `normalized_contract.yaml::manual_property_correction`
null-handling rejects records with null `approver`. Reinforced by
`dq_rules.yaml::msx_correction_requires_approver`.

**Handling.** Correction cannot promote. Requestor obtains approver
sign-off and resubmits. High-value corrections (touching `property`,
`lease`, `budget_line` objects) additionally require an
`approval_request` linkage per `_core/approval_matrix.md`.

## 8. File received in wrong template version

**Trigger.** Operator submits an approval_matrix workbook using the
2025-Q4 template (with 5 action_type rows) instead of the 2026-Q1
template (with 8 action_type rows including the new
`concession_above_policy` row).

**Detection.** `dq_rules.yaml::msx_template_version_check` fails the
header pattern match.

**Handling.** File is routed to `_rejected/<YYYY>/<MM>/` with a log
entry naming the expected template version. Runbook:
`runbooks/manual_common_issues.md::template_version_drift`.

## 9. Blank required field

**Trigger.** Any required field per `file_family_registry.yaml` arrives
blank. For example, `tpm_submission_monthly_report` with
`signed_off = ""` or `narrative_summary = null`.

**Detection.** `dq_rules.yaml::msx_provenance_envelope` for provenance
fields; `normalized_contract.yaml` null-handling for canonical required
fields.

**Handling.** Record-level reject with the raw `source_row_id` surfaced
to the operator for remediation.

## 10. Signature missing on TPM monthly

**Trigger.** A `tpm_submission_monthly_report` row lands with
`signed_off = false` or `signed_off` blank.

**Detection.** `normalized_contract.yaml` null-handling rejects records
where `signed_off` is not `true`. Supported by
`dq_rules.yaml::msx_attestation_required`.

**Handling.** Unsigned TPM scorecard cannot promote. Operator obtains
sign-off from the designated reviewer and resubmits. Persistent
unsigned rows across multiple periods escalate per
`runbooks/manual_common_issues.md::missing_signature`.

## 11. Bid recommendation lacking rationale

**Trigger.** A `bid_tab_construction` row has
`recommended_award = true`, `recommendation_rationale = ""`.

**Detection.** `ms_recon_bidtab_rationale_present` blocks.

**Handling.** Award cannot promote. Construction lead adds the rationale
(market-comparable, lowest qualified, sole-source justification, etc.)
and resubmits.

## 12. Approval threshold change without change_log_ref

**Trigger.** An `approval_matrix_threshold_set` or
`approval_matrix_authority_change` row arrives with `change_log_ref`
null or blank.

**Detection.** `ms_recon_approval_change_has_log` blocks.

**Handling.** Missing `change_log_ref` blocks; operator attaches the
governance-log entry and resubmits. The change_log is maintained per
`_core/change_log_conventions.md`.

## 13. Multi-property file split incorrectly

**Trigger.** An emailed `operator_owner_report` bundle covers 3
properties, but rows in the workbook are split such that property A's
revenue section contains property B's opex section (header misalignment
during template copy).

**Detection.** `property_id` crosswalk succeeds at the row level, but
downstream reconciliation against the Intacct property-level actuals
flags extreme drift on multiple accounts.

**Handling.** Adapter runs per-row crosswalk and flags any file where
crosswalk resolution rate is below the file-level
`property_resolution_floor_band`. Below-floor files are quarantined in
`_rejected/` pending operator restatement. Runbook:
`runbooks/manual_common_issues.md::multi_property_split_error`.

## 14. File received past cadence window

**Trigger.** A `tpm_submission_monthly_report` for March 2026 arrives
on April 28, 2026, past the `staleness_threshold_days = 10`.

**Detection.** `dq_rules.yaml::msx_freshness_per_family` and
`reconciliation_checks.yaml::ms_recon_tpm_lag_enforcement`.

**Handling.** Landing still accepts the file (we do not want to lose
the data), but confidence is reduced and an escalation fires to
`asset_mgmt_director`. Repeat late-submission incidents across three
consecutive periods escalate to a TPM scorecard review and contract
compliance check per `third_party_manager_scorecard_review` workflow.

## 15. Analyst override on Excel benchmark vs file refresh

**Trigger.** A `manual_property_correction` updates a field previously
sourced from an Excel capex_cost_library row, but no refresh_ref is
attached and the override is outside the `analyst_override_band`.

**Detection.** `ms_recon_correction_vs_excel_benchmark` (warning for
within-band drift) and `ms_recon_correction_refresh_link` (warning for
missing link).

**Handling.** Out-of-band override requires a benchmark refresh
submission or a policy_exception_ref. Runbook:
`runbooks/manual_common_issues.md::analyst_override_no_refresh`.

## 16. Cell value typed as text in numeric column

**Trigger.** A `bid_tab_construction` row has `base_bid = "184,200"`
instead of a number (Excel formatted the cell as text).

**Detection.** Parser coerces numeric fields; failures route to the
`type_coercion_warnings` log. If coercion succeeds (strip commas, parse
as number) the row promotes with a coercion note; if it fails (true
non-numeric like "TBD") the row is rejected.

**Handling.** Operator re-enters the value as a number. Runbook:
`runbooks/manual_common_issues.md::cell_typed_as_text`.
