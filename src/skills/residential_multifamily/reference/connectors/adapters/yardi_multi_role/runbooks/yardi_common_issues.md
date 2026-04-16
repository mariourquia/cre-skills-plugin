# Yardi Common Issues Runbook

Well-known Yardi gotchas observed across operator onboardings. Each
section is anchored to DQ rules or reconciliation checks that surface
the issue, plus the operator remediation path.

---

## stale_voyager_feed

**Symptom.** `yd_freshness_voyager_pms` fires. Extract is older than
declared `expected_latency_minutes`.

**Likely causes.**
- API rate-limit pause or retry loop
- Voyager tenant maintenance window
- Scheduled extract job failure (SFTP or warehouse ETL)

**Remediation.**
1. Check extract job logs for last successful run.
2. Confirm Voyager tenant status with operator's Yardi contact.
3. Re-run extract; if still failing, open ticket with Yardi support.
4. Annotate downstream workflow outputs with `stale_extract = true`
   until resolved.

---

## data_connect_lag

**Symptom.** `yd_freshness_data_connect` warns; warehouse lags Voyager
by more than `data_connect_lag_band`.

**Likely causes.**
- Data Connect refresh schedule behind
- Upstream ETL failure
- Large batch in progress

**Remediation.**
1. Check Data Connect refresh job status.
2. For month-close period, pull directly from Voyager API instead of
   Data Connect until catch-up completes.
3. Block month-close workflows until lag returns to within band.

---

## t_code_mapping

**Symptom.** `yd_conformance_tcode_decoded` blocks records.

**Likely causes.**
- Voyager tcode represents a lifecycle phase not yet registered in
  `t_code_decode` (e.g., skip, subsidy_hold, fair_housing_investigation).
- Operator customized tcode lineage beyond defaults.

**Remediation.**
1. Log the unknown tcode pattern with its context (applicant /
   resident / past-resident / collections).
2. Extend adapter-local `t_code_decode` mapping to include the
   pattern.
3. Run unit tests for the mapping; add regression tests.
4. Deploy updated mapping; re-ingest blocked records.

---

## chargecode_per_property

**Symptom.** `yd_conformance_chargecode_property_scoped` blocks
records. A chargecode did not resolve under property scope.

**Likely causes.**
- New chargecode introduced at a property without updating the
  crosswalk.
- Chargecode reused across properties with different meanings, and
  only the global decode is registered.

**Remediation.**
1. Consult Voyager chargecode table for the specific property via
   operator's Yardi admin.
2. Register the (propid, chargecode) pair in
   `master_data/charge_code_crosswalk_by_property` with the correct
   canonical charge_type.
3. Re-process blocked charges.
4. If the chargecode pattern is genuinely new, escalate to canonical
   review — a canonical charge_type may need extension.

---

## posting_vs_accrual

**Symptom.** `yd_consistency_post_vs_accrual` warns. A charge or
actual_line has post_date in a different month than its accrual
month.

**Likely causes.**
- Normal late-posting after month cutover
- Backdated entry for prior-period correction

**Remediation.**
1. Accrual month is canonical for period attribution. Do NOT move
   the record.
2. If drift exceeds `post_vs_accrual_band`, escalate to
   finance_reporting for operator review.
3. Watch for patterns; persistent large drift may indicate
   operator's post-period close discipline.

---

## rentcafe_voyager_drift

**Symptom.**
- `yd_consistency_rentcafe_vs_voyager` warns
- `yd_recon_rentcafe_vs_voyager_lead_state` outside band
- `yd_consistency_rentcafe_leadstate_vs_voyager` warns

**Likely causes.**
- RentCafe and Voyager are two systems; sync between them lags
- Leasing agent updates RentCafe but forgets to reflect in Voyager
- RentCafe API scope does not cover some lifecycle transitions
  observable in Voyager

**Remediation.**
1. Precedence rule (per `bounded_assumptions.yaml::rentcafe_voyager_drift_defaults`):
   - Voyager wins for resident state
   - RentCafe wins for pre-resident lead state
2. Document the drift pattern in the operator's leasing SOP.
3. If persistent, run weekly sync report to operator's leasing
   manager.

---

## recovery_fee_posting

**Symptom.** charge record carries non-null `recovery_code` on a
residential-only portfolio.

**Likely causes.**
- Property reclassified from mixed_use to residential without
  updating recovery-fee posting rules in Voyager
- Mistakenly configured recovery-fee template applied to residential
  unit

**Remediation.**
1. Divert record to audit bucket per
   `bounded_assumptions.yaml::recovery_fee_handling_residential_suppressed`.
2. Notify operator to reconfigure recovery-fee posting in Voyager
   for the property.
3. Do not roll into canonical charge stream.

---

## refund_handling_post_move_out

**Symptom.** `yd_consistency_refund_posting_after_move_out` info-level
trigger. A charge posts to a closed resident_account.

**Likely causes.**
- Normal security deposit refund
- Utility reconciliation after move-out
- Damage charge offset

**Remediation.**
1. No action required; informational.
2. Preserved for audit. Downstream aggregations handle correctly.

---

## prepay_vs_receivable

**Symptom.** `yd_consistency_prepay_vs_receivable_attribution` warns.
A prepay posting lands in unexpected account_class.

**Likely causes.**
- Operator config routes prepay to liability vs receivable
- `account_crosswalk` row missing for the prepay account code

**Remediation.**
1. Confirm operator's prepay accounting convention.
2. Register the prepay account code in `account_crosswalk` with
   correct account_class.
3. Revenue recognition follows accrual month; prepay balance rolls
   into revenue when accrual month arrives.

---

## deleted_not_purged

**Symptom.** `yd_consistency_deleted_but_not_purged` warns. Soft-deleted
rows appear in aggregations.

**Likely causes.**
- Voyager soft-deletes via status flag; full extracts include them
- Adapter filter missed the flag

**Remediation.**
1. Confirm soft-delete flag encoding (`status = deleted`, or `is_purged = true`, or tenant-specific).
2. Update adapter filter to exclude deleted rows from aggregations.
3. Retain in audit trail.

---

## rentcafe_api_scope_not_equal_voyager_scope

**Symptom.** Operator expects RentCafe to carry a field or object not
present in RentCafe API.

**Likely causes.**
- Misunderstanding of RentCafe scope
- Field exists in Voyager but not exposed via RentCafe

**Remediation.**
1. Document the scope gap in Dimension 2c of
   `classification_worksheet.md`.
2. Route the required field through Voyager API or Data Connect
   instead.
3. Update `normalized_contract.yaml` precedence rules accordingly.

---

## vendor_crosswalk_mismatch

**Symptom.** `yd_recon_vendor_three_way_with_yardi` outside
`identity_match_band`.

**Likely causes.**
- Vendor created independently in Yardi, Intacct, and Procore with
  slightly different names
- Vendor tax_id hash differs due to data entry drift

**Remediation.**
1. Open vendor match review in master_data review queue.
2. Declare survivorship (Intacct wins on tax_id; Yardi wins on
   service dispatch; Procore wins on construction commitments).
3. Merge in `vendor_master_crosswalk` with effective_start.

---

## historical_unit_structure

**Symptom.** Historical lease references hunit that does not resolve
in current unit roster.

**Likely causes.**
- Post-renovation unit split, combine, or retire
- Data migration from pre-renovation Yardi instance

**Remediation.**
1. Populate `dc_dim_unit_effective` with effective-dated unit
   structure.
2. Retain historical lease with `effective_end_date` set.
3. Current-period workflows skip the record; historical comparisons
   use effective-dating to align.

---

## book_id_undeclared

**Symptom.** `yd_conformance_book_id_declared` blocks. GL record
missing book_id.

**Likely causes.**
- Extract job did not include book_id in SELECT
- Yardi tenant runs only one book (accrual) and operator assumed it
  would default

**Remediation.**
1. Fix extract to include book_id explicitly.
2. If operator runs only accrual, confirm and encode the default at
   the adapter level.
3. Never silently default a book_id; fail loudly.

---

## report_export_template_drift

**Symptom.** `yd_conformance_report_columns` blocks. Unregistered
template_id in upload.

**Likely causes.**
- Operator edited the Yardi report template (added or removed
  columns)
- New report template introduced without registration

**Remediation.**
1. Register the new template_id in
   `master_data/report_export_templates` with its column_map.
2. Reprocess quarantined rows.
3. Notify operator to alert before template changes in future.

---

## stale_exports

**Symptom.** `yd_freshness_stale_exports` warns. File internal
`as_of_date` more than `report_export_staleness_band` older than
`file_received_at`.

**Likely causes.**
- Operator uploaded historical file without declaring it as such
- Upload batch behind schedule

**Remediation.**
1. Confirm with operator whether upload is historical backfill.
2. If backfill, tag as `stale_export = true` in metadata; downstream
   treats as historical only.
3. If not backfill, rerun fresh export and re-upload.

---

## canonical_gap

**Symptom.** Yardi-native object (e.g., some lease-charge subtype,
resident portal event, recovery-fee post sequence) has no canonical
home.

**Likely causes.**
- Canonical ontology does not yet cover the concept
- Concept is Yardi-specific and not relevant to canonical scope

**Remediation.**
1. Flag record in `bounded_assumptions.yaml` as
   `requires_canonical_extension`.
2. Retain in raw landing; do not emit canonical.
3. Open entry in `../../_core/stack_wave4/open_questions_and_risks.md`.
4. Route through canonical change-control per `_core/BOUNDARIES.md`
   before extending ontology.

---

## procore_yardi_jobcost_drift

**Symptom.** `yd_recon_yardi_jobcost_vs_procore` outside band.

**Likely causes.**
- Procore commitment posted but Yardi job_cost not yet caught up
- Yardi runs in Procore-free mode for a subset of projects

**Remediation.**
1. Confirm which system is primary for the project in `capex_project_crosswalk`.
2. Wait for catch-up; retry recon.
3. If persistent, escalate to construction_lead.
