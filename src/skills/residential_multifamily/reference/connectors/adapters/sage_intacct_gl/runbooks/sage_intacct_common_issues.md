# Sage Intacct Common Issues Runbook

Status: wave_4_template
Audience: corporate_controller, finance_systems_team, data_platform_team
Last updated: 2026-04-15

Every section below maps a recurring operational issue to detection,
triage, and resolution. Issue anchors are referenced by name from
`reconciliation_checks.yaml`, `dq_rules.yaml`, `edge_cases.md`, and the
cross-stack `stack_reconciliation_matrix.md`. Tolerance band names are
cited from `reference/normalized/schemas/reconciliation_tolerance_band.yaml`;
no numeric values are hardcoded.

---

## stale_feed

**Detection.** `ic_freshness_actual_lines_daily` at blocker severity.

**Trigger.** Intacct Web Services extraction lagged beyond
`expected_latency_minutes` in the `source_registry` entry for
`sage_intacct_prod`.

**Triage.**
1. Check Intacct Web Services API availability and authentication.
2. Check extractor service logs for timeout or token rotation failure.
3. Confirm the operator's Intacct tenant is not under scheduled
   maintenance.

**Resolution.** Restart the extractor; if credential is expired, rotate
per `security/secrets_rotation.md`. On repeated failure, open a vendor
support ticket and escalate to `data_platform_team`.

---

## close_feed_lag

**Detection.** `ic_freshness_closed_period_lag`.

**Trigger.** Intacct period close emitted `period_close_timestamp`, but
the full post-close actuals feed did not land within
`close_feed_lag_band`.

**Triage.**
1. Check for pending entries awaiting approval that blocked the close.
2. Confirm the extractor polled the close event and kicked off the
   post-close backfill.
3. Compare counts: `actual_line` rows per property between the last
   pre-close snapshot and the current close snapshot.

**Resolution.** Re-run the close backfill. If manual post-close adjustments
are still in flight, extend `close_feed_lag_band` for that specific close
cycle with a `manual_overrides.yaml` row and reviewer sign-off.

---

## period_reopen_drift

**Detection.** `ic_consistency_posting_period_close_lock`,
`ic_recon_period_reopen_drift`.

**Trigger.** Postings appear with `BATCH_DATE > period_close_timestamp`
without a formal Intacct reopen event.

**Triage.**
1. Check for unauthorized late posts via batch export.
2. Confirm whether the post is the result of an allowed reopen (e.g.,
   year-end audit adjustments) that was not flagged in the adapter's
   reopen feed.
3. Identify the `CREATED_BY` user and surface the post for manual review.

**Resolution.** If the post is legitimate, document the reopen in the
adapter's reopen registry and re-run `monthly_property_operating_review`
for the affected period. If the post is unauthorized, reverse it and
escalate to `corporate_controller`.

---

## dim_property_duplication_after_entity_reorg

**Detection.** `ic_recon_property_dim_present`,
`ic_conformance_property_dim_in_crosswalk`.

**Trigger.** Operator reorganized the dim hierarchy (split a roll-up
entity, moved a property's fund class, etc.) and two dims now point to
the same canonical property_id without `effective_start`/`effective_end`
boundaries.

**Triage.**
1. Identify the overlapping crosswalk rows.
2. Confirm the reorg effective date.
3. Check which Intacct postings fell into the overlap window.

**Resolution.** Close the old crosswalk row with `effective_end` on the
reorg date. Open a new row for the new dim with matching `effective_start`.
Same canonical property_id, continuous history.

---

## budget_version_sprawl

**Detection.** `ic_conformance_posting_state_enum`,
`ic_freshness_budget_version_monthly`.

**Trigger.** Operator publishes multiple overlapping `BUDGETID`s with
drifted labels (`initial_2026`, `fy26_v1`, `2026 Approved`, `Board
Approved 2026`), none matching `map_intacct_budget_version`.

**Triage.**
1. Export all active `BUDGETID`s from the sandbox or prod Intacct.
2. Confirm with corporate_controller which version is authoritative.
3. Review the onboarding runbook's budget-version naming convention.

**Resolution.** Rename non-conforming `BUDGETNAME` fields to match the
convention. Retire obsolete budget versions via Intacct's `RETIRE`
state. Re-run the budget feed backfill.

---

## accrual_reversal_misalignment

**Detection.** `ic_consistency_accrual_reverses_next_period`.

**Trigger.** An accrual has `REVERSAL` flag true but the `REVERSAL_OF`
pointer is missing, wrong, or points to a different period.

**Triage.**
1. Pull the original posting and the reversal row.
2. Confirm the original was actually reversed (vs. left standing).
3. Check for duplicate reversals.

**Resolution.** Repair the `REVERSAL_OF` pointer in Intacct (requires
reopen of the affected period if already closed). Re-run the adapter
feed for the affected period.

---

## payroll_entity_drift

**Detection.** `ic_recon_payroll_entity_attribution` at warning.

**Trigger.** Sum of HR/Payroll rows by canonical property_id disagrees
with sum of Intacct payroll account postings by resolved property_id
beyond `staffing_drift_band`.

**Triage.**
1. Identify the employees whose property attribution differs between
   systems. Most common: regional maintenance leads with
   `fte_share` splits.
2. Confirm the `employee_crosswalk` and `staffing_plan` share the same
   `fte_share` values as the current payroll split.
3. Check for a mid-period reassignment not yet reflected in the
   crosswalk.

**Resolution.** Update `employee_crosswalk::notes` with current
`fte_share`. Re-run the derived payroll allocation for the affected
period.

---

## vendor_crosswalk_mismatch

**Detection.** `ic_recon_vendor_three_way`, `ic_referential_vendor_in_master`.

**Trigger.** Same vendor appears with different names, different tax ids,
or different legal entities in Intacct, AppFolio, and Procore.

**Triage.**
1. Pull the three source rows side-by-side.
2. Confirm whether the mismatch is a rename (same tax id, different
   name), an alias (same legal entity, multiple source ids), or a true
   duplicate vendor (distinct legal entities).

**Resolution.**
- For a rename: update `vendor_master_crosswalk` with `effective_start` on
  the rename date; tax id survives.
- For an alias: create a second crosswalk row with matching canonical id.
- For a true duplicate: keep separate canonical ids; note the
  relationship in `notes` but do not merge.

---

## 1099_vs_corporate_flag_mismatch

**Detection.** `ic_recon_labor_classification`.

**Trigger.** Vendor is flagged as 1099 in Intacct (`W9_ON_FILE = true` with
individual tax id) but flagged as corporate in AppFolio or Procore, or
vice versa.

**Triage.**
1. Confirm the vendor's actual legal status via W9 on file.
2. Check whether Intacct is set to issue a 1099 at year-end to the
   vendor.
3. Surface to AP manager for reconciliation.

**Resolution.** Align the flag across all three systems to match the W9.
Update `vendor_master_crosswalk` with a `notes` entry explaining the
resolution. Re-run the three-way reconciliation.

---

## dim_lock_during_close

**Detection.** Internal; raised by the Intacct extraction process during
the close window.

**Trigger.** Operator sets a dimension (property or project) to locked
status during a close window; new postings referencing that dim are
rejected.

**Triage.**
1. Confirm the dim lock is intentional (pre-close scrub, audit
   adjustment window).
2. Identify postings that failed to land due to the lock.

**Resolution.** Wait for the close cycle to complete, then unlock the
dim. Re-run the postings that were held. If the lock is indefinite
(e.g., a property is being disposed), update `property_master_crosswalk`
with `effective_end`.

---

## journal_source_code_drift

**Detection.** `ic_conformance_posting_state_enum`,
`ic_recon_manual_journal_attribution`.

**Trigger.** Operator adds a new journal source code (e.g., `XJ` for a
custom workflow) that is not recognized by the adapter's
`map_intacct_posting_state` or by downstream classification.

**Triage.**
1. Pull the journal source code catalog from Intacct.
2. Confirm whether the new code is legitimate (new workflow, new module)
   or an error.

**Resolution.** If legitimate, extend `map_intacct_posting_state` and
document the new code in `edge_cases.md`. If an error, correct the code
at source.

---

## fx_translation_false_positive

**Detection.** `ic_conformance_posting_state_enum` on `source_currency`
outside the expected USD/CAD range.

**Trigger.** Multi-entity portfolio includes a CAD entity. FX rate
registry produces a translated USD value that appears outside
`revenue_basis_band` when reconciled against AppFolio cash (USD-only
portfolio assumption).

**Triage.**
1. Confirm the CAD entity is in scope for the current reconciliation.
2. Check the FX rate used by the adapter against the `fx_rate_registry`
   for the posting date.
3. Compare translated USD to the AppFolio cash receipt (USD only).

**Resolution.** If the FX rate is stale, refresh `fx_rate_registry`. If
the reconciliation is inappropriate (CAD entity should be excluded from
USD-only rollups), update the workflow definition to scope out the
entity. Document in `notes`.

---

## manual_journal_attrib

**Detection.** `ic_recon_manual_journal_attribution`.

**Trigger.** Manual top-side journal posted with `SOURCE_MODULE = Manual`
but no `LOCATIONID` or `ENTITYID` beyond the corporate entity.

**Triage.**
1. Identify the posting and the `CREATED_BY` user.
2. Ask the user which property or properties the posting is intended to
   affect.
3. Confirm the allocation basis (by_unit_count, by_revenue, etc.).

**Resolution.** Two paths:
- **Split at source**: reverse the posting and repost with per-property
  splits.
- **Allocate downstream**: apply a named allocation basis from
  `property_master_crosswalk`. The allocated rows are tagged
  `derived_allocation = true`.

If unresolved by close, `ic_recon_manual_journal_attribution` escalates
to blocker.

---

## unmapped_account

**Detection.** `ic_conformance_account_in_coa`, `ic_recon_unmapped_account`.

**Trigger.** Posting references a `GLACCOUNTNO` not present in
`chart_of_accounts` or not resolved via `account_crosswalk`.

**Triage.**
1. Pull the posting and the account detail from Intacct.
2. Confirm whether the account is newly created, renamed, or
   retired-but-referenced.

**Resolution.** Extend `account_crosswalk_additions` with the new mapping.
If a rename, open `effective_end` on the old row and `effective_start` on
the new row with the same `canonical_id`.

---

## capex_opex_misclass

**Detection.** `ic_consistency_capex_opex_misclass`,
`ic_recon_capex_opex_misclass`.

**Trigger.** Posting uses a capex account without `PROJECTID`, or uses an
opex account with `PROJECTID` tied to a capex_family project.

**Triage.**
1. Identify the posting and the user who created it.
2. Confirm the intended classification.

**Resolution.** Reclass via a new journal entry (reverse the original,
post with correct account and dim). Update controls in Intacct to
require `PROJECTID` on all capex accounts via account-level defaults.

---

## post_close_entity_setup

**Detection.** `ic_recon_post_close_entity_setup`.

**Trigger.** Dealpath deal closed; property entity not yet provisioned
in Intacct beyond `handoff_lag_band`.

**Triage.**
1. Confirm close date from Dealpath.
2. Check status of entity provisioning request.
3. Identify the canonical property_id expected.

**Resolution.** Provision the Intacct entity (or location) per the
onboarding runbook. Create the `property_master_crosswalk` row. Retire
any placeholder `PRJ_PLACEHOLDER_*` rows and open concrete project dims.
Unblock `acquisition_handoff`.
