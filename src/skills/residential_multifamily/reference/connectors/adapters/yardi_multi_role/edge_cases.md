# Yardi Edge Cases

Every edge case from the Yardi spec, documented with scenario,
detection, system response, and operator action. Tolerance bands cite
`reference/normalized/schemas/reconciliation_tolerance_band.yaml`.

---

## 1. Legacy read-only during cutover

**Scenario.** Operator is migrating from Yardi to AppFolio. Yardi is
read-only; operating writes happen in AppFolio. Historical data in
Yardi must remain accessible for comparatives; new writes in Yardi are
an error.

**Detection.** Rule `yd_consistency_historical_only_mode`: any
`extracted_at > cutover_effective_date` for a property declared in
historical-only mode.

**System response.** Block the record. Log to exception queue. Retain
original in raw landing for audit.

**Operator action.** Confirm whether the write was intentional (e.g.,
back-office correction). If intentional, update
`runbooks/yardi_migration_to_appfolio.md::post_cutover_corrections` to
document the exception; otherwise halt the write source.

---

## 2. Both Yardi and AppFolio live for overlapping period

**Scenario.** Cutover is in progress; both systems carry the same
property-period. Dual-run window is bounded by a declared
`cutover_overlap_band`.

**Detection.** Check `yd_recon_yardi_vs_appfolio_overlap` at
property-period grain. Drift within `cutover_overlap_band` = warning;
outside band = blocker.

**System response.** Warning raised during window; downstream workflows
annotate outputs with `dual_run_active = true` and degrade confidence to
`medium`. After `cutover_effective_date` per property, Yardi writes
blocked per edge case 1.

**Operator action.** Monitor cutover burn-down. Close cutover per
property as soon as dual-run window ends per
`runbooks/yardi_migration_to_appfolio.md`.

---

## 3. Yardi and Intacct duplicate financials

**Scenario.** Operator runs `yardi_plus_intacct` — Yardi PMS + Intacct
GL. Charges and payments exist in both systems. Accidentally aggregating
both double-counts revenue.

**Detection.** Reconciliation check `yd_recon_yardi_vs_intacct_gl_parallel`
at property-account-period grain. Exact match expected within
`gl_parallel_band`.

**System response.** Within band: silent_audit. Outside band: blocker;
route to `unmapped_account_handling.md`. Canonical precedence:
Intacct wins post-close per `posting_period_close_wins`.

**Operator action.** Reconcile the specific property-account-period
tuple; usually either missing Intacct posting or late-arriving Yardi
charge that has not yet reached Intacct.

---

## 4. Property-code mismatch

**Scenario.** Voyager `scode` or `propid` does not resolve via
`property_master_crosswalk`. Usually due to new property not yet seeded
or drift between Voyager naming and Intacct entity naming.

**Detection.** Rule `yd_recon_property_code_resolves_on_crosswalk`.

**System response.** Blocker on first encounter. Row retained in raw
landing with `crosswalk_pending = true`. Downstream aggregation skips
the row.

**Operator action.** Add a row to `property_master_crosswalk` with
`effective_start`, `survivorship_rule`, and
`source_of_record_per_attribute`. Follow
`runbooks/yardi_onboarding.md::property_crosswalk_seed`.

---

## 5. Missing submarket or manager tags

**Scenario.** Voyager property record lacks `submarket_label` or the
regional-manager tag the operator expects. Common on older properties
or during cutover.

**Detection.** Rule `yd_completeness_required_property_fields` warns on
required fields; optional fields (submarket, manager tag) surface as
`info`-severity completeness issues in monitoring.

**System response.** Property row ingested; downstream rent-comp and
benchmarking workflows that require submarket run in
`partial_mode_behavior`.

**Operator action.** Populate missing tags in Voyager OR add override in
`submarket_crosswalk` / operator metadata.

---

## 6. Stale report exports

**Scenario.** Manual Yardi report export is emailed or dropped days to
weeks after its internal `as_of_date`. Using the file as current-period
data is incorrect.

**Detection.** Rule `yd_freshness_stale_exports`:
`file_received_at - as_of_date > report_export_staleness_band`.

**System response.** Warning. Record retained, tagged
`stale_export = true`. Downstream workflows treat as historical only.

**Operator action.** Confirm intent. If export is historical backfill,
tag as such in the upload portal; otherwise rerun a fresh export.

---

## 7. Replicated data lag (Data Connect)

**Scenario.** Data Connect warehouse lags Voyager by minutes to hours.
Pulling reports from Data Connect too early misses late Voyager entries.

**Detection.** Rule `yd_freshness_data_connect`; reconciliation check
`yd_recon_data_connect_vs_voyager_charges` at charge-grain drift.

**System response.** Warning within `data_connect_lag_band`. Month-close
workflows (close_month_report, monthly_property_review) block if lag
exceeds band.

**Operator action.** Wait for replication to complete OR pull directly
from Voyager API for the period under close.

---

## 8. Resident-PII restrictions on downstream output

**Scenario.** Classification Dimension 4 declares resident PII should
not flow to specific downstream consumers (e.g., leasing-pipeline
dashboards, TPM scorecards).

**Detection.** Post-classification PII policy enforced at
`security/pii_classification.md`.

**System response.** Redact or hash per-field per declared posture
before downstream emission. No raw resident names, SSNs, or contact
info reach non-whitelisted consumers.

**Operator action.** Re-run classification Dimension 4 if downstream
scope changes. Sign-off required from `compliance_risk`.

---

## 9. Historical leases not mapping to current property structure

**Scenario.** Property underwent renovation, unit split, combine, or
reclass. Historical leases reference `hunit` ids that no longer map to
current unit structure.

**Detection.** Historical lease with `effective_end_date IS NOT NULL`
AND unit with `effective_end_date IS NOT NULL`; join through
`dc_dim_unit_effective` for effective-dated resolution.

**System response.** Historical lease retained with original `hunit`.
Current-period workflows skip the record. Monthly and quarterly reports
that compare to historical periods use `dc_dim_unit_effective` to tie
back to a current-unit-equivalent row if one exists.

**Operator action.** Populate `dc_dim_unit_effective` during renovation
as part of `runbooks/yardi_onboarding.md::renovation_unit_restructure`.

---

## 10. Partial property migrations

**Scenario.** Operator migrates some properties to AppFolio while others
remain in Yardi. `mixed_by_portfolio_segment` classification posture.

**Detection.** Classification Dimension 3 declares the split. Adapter
surfaces `portfolio_segment` tag on each property.

**System response.** Per-property classification determines primary
source. Workflows that span segments run cross-source and annotate
outputs with source-provenance per property.

**Operator action.** Maintain portfolio-segment map in Dimension 3;
update on any migration event.

---

## 11. Yardi-only historical comparatives

**Scenario.** All operating state has cut over to AppFolio, but the
executive team wants 3-5 year historical comparatives that predate the
cutover. Yardi holds those comparatives.

**Detection.** Classification = `yardi_cutover_completed_archival`. No
current-period reads expected.

**System response.** Historical reads allowed; current-period writes
blocked per edge case 1. Downstream historical comparatives annotated
with `source = yardi_historical_archive`.

**Operator action.** Periodically confirm archive read-paths still work
(runbook `yardi_migration_to_appfolio.md::archive_verification`).

---

## 12. Voyager t-code overloading

**Scenario.** Same hten carries multiple t-code generations across an
applicant -> resident -> past-resident -> collections lifecycle.
Joining by raw tcode mislabels records.

**Detection.** Rule `yd_conformance_tcode_decoded`.

**System response.** Block any record whose tcode cannot be decoded
into the canonical lineage enum.

**Operator action.** Follow
`runbooks/yardi_common_issues.md::t_code_mapping` to register lineage
rules; update adapter's `t_code_decode` implementation.

---

## 13. RentCafe scope not equal to Voyager scope

**Scenario.** RentCafe exposes a subset of resident / leasing state
compared to Voyager. Some operator-critical fields (full ledger detail,
lease documents) live only in Voyager.

**Detection.** Manual during Dimension 2c classification. Any workflow
declared to consume RentCafe-only must verify field coverage.

**System response.** Per-field source precedence declared in
`normalized_contract.yaml`. RentCafe primary for lead funnel
pre-application; Voyager primary for post-application state.

**Operator action.** Document scope mismatch in Dimension 2c of
`classification_worksheet.md`.

---

## 14. Posting-month vs operating-month drift

**Scenario.** A charge accrues in operating month (e.g., 2026-03) but
posts in 2026-04. Budget vs actual comparisons using post_date
mis-attribute the amount.

**Detection.** Rule `yd_consistency_post_vs_accrual` and check
`yd_recon_post_vs_accrual_drift`.

**System response.** Accrual month (`month`) is canonical for period
attribution. Post_date preserved for audit only. Warning if drift
beyond `post_vs_accrual_band`.

**Operator action.** Confirm convention in Dimension 2b of
`classification_worksheet.md`. Operator may override post_date-primary
in edge cases.

---

## 15. Recovery-fee handling

**Scenario.** Mixed-use / commercial properties carry recovery-fee
posting logic (CAM, insurance, tax pass-throughs). Residential-only
portfolios should see no recovery codes.

**Detection.** `charge.recovery_code IS NOT NULL` on a property whose
classification is residential-only.

**System response.** Residential-only: divert to audit bucket; do not
roll into canonical charge stream. Mixed-use: preserve and map per
commercial/mixed recovery-fee logic (outside residential_multifamily
scope; may require canonical extension).

**Operator action.** Confirm segment posture; if residential-only,
investigate why recovery codes are posting.

---

## 16. Chargecode by property variation

**Scenario.** Same logical charge (e.g., base_rent) uses different
Voyager chargecodes per property. Global chargecode decode maps
incorrectly.

**Detection.** Rule `yd_conformance_chargecode_property_scoped`.

**System response.** Block any chargecode decoded without a
property-scoped table. `charge_code_crosswalk_by_property` must carry a
row for every (propid, chargecode) in scope.

**Operator action.** Load property-scoped chargecode table during
onboarding. See `runbooks/yardi_onboarding.md::charge_code_seed`.

---

## 17. Deleted but not purged

**Scenario.** Voyager soft-deletes rows via a status flag. Full extracts
include deleted rows unless filtered.

**Detection.** Rule `yd_consistency_deleted_but_not_purged` warns when
deleted rows appear in aggregate-bound payloads.

**System response.** Deleted rows retained in audit trail; downstream
aggregations filter by active status.

**Operator action.** Confirm soft-delete flag encoding; update adapter
filter if Yardi config changes.

---

## 18. Refund handling (post move-out)

**Scenario.** Security deposit refunds post days to months after the
resident moves out. The resident_account is closed but still carries
late-arriving debits.

**Detection.** `yd_consistency_refund_posting_after_move_out` (info-severity).

**System response.** Refund-dated charges retained against closed
resident_accounts; treated as expected.

**Operator action.** No action; preserved for audit.

---

## 19. Prepay vs receivable posting

**Scenario.** Prepaid rent on some Yardi configs posts to a liability
account (not revenue) until the accrual month arrives. A careless GL
pull mis-attributes revenue.

**Detection.** `yd_consistency_prepay_vs_receivable_attribution` against
`account_crosswalk` declared account_class.

**System response.** Route prepay postings to declared account_class;
revenue attribution follows accrual month regardless of post_date.

**Operator action.** Confirm account_crosswalk is loaded for every
account code in use; close gaps before month-end.

---

## 20. Report export template drift

**Scenario.** Yardi report templates edited by operator staff; column
labels change. Adapter bound to label position breaks.

**Detection.** Rule `yd_conformance_report_columns`: every report-export
record must resolve a registered template_id; unregistered templates
rejected.

**System response.** Block the record. Log template_id and submitter to
exception queue.

**Operator action.** Register the new column_map in
`master_data/report_export_templates`; reprocess quarantined rows.
