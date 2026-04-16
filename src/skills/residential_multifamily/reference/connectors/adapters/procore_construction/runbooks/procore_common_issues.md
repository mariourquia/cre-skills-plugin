# Procore Common Issues Runbook

Audience: data_platform_team, construction_lead, finance_systems_team
Status: wave_5

Resolution playbooks for recurring Procore integration issues. Each issue
carries a trigger signal, a diagnostic sequence, and a resolution path.
Referenced by DQ rules (`dq_rules.yaml`) and reconciliation checks
(`reconciliation_checks.yaml`). Numeric tolerances cite
`reference/normalized/schemas/reconciliation_tolerance_band.yaml`.

## stale_project_feed

Trigger: `pc_freshness_projects` fails; Procore project feed has not landed
within the expected latency window.

Resolution:
- Verify OAuth token validity; refresh if expired.
- Check Procore Developer portal API status.
- Rerun the extractor; if the second pull also fails, escalate to
  data_platform_team and pause downstream workflows that depend on
  project feed freshness.

## stale_commitment_feed

Trigger: `pc_freshness_commitments` fails.

Resolution: Same diagnostic as `stale_project_feed` scoped to the
commitments endpoint. Commitment feed latency blocks
`bid_leveling_procurement_review` and `cost_to_complete_review`.

## stale_co_feed

Trigger: `pc_freshness_change_orders` fails.

Resolution: Same diagnostic as `stale_project_feed` scoped to the
change-orders endpoint. CO feed latency blocks `change_order_review`.

## stale_draw_feed

Trigger: `pc_freshness_draws` fails.

Resolution: Same diagnostic as `stale_project_feed` scoped to the
payment-applications endpoint. Draw feed latency blocks
`draw_package_review`.

## cost_code_drift

Trigger: `pc_conformance_csi_division` warns; cost codes do not match
the CSI two-digit division pattern.

Resolution:
- If the cost code is a legitimate non-CSI operator convention, alias it
  via `map_cost_code` to the closest CSI division and annotate.
- If the cost code is a typo or custom code with no CSI equivalent,
  coach the operator to use the standard library; do not block the
  commitment but flag the estimate for review.
- Open a master_data ticket to extend `account_crosswalk.yaml` if the
  new code requires a dedicated GL mapping.

## co_sum_mismatch

Trigger: `pc_consistency_co_sum_vs_revised` or
`pc_recon_co_pending_excluded_from_budget` fails; the sum of approved
commitment COs does not equal `revised_contract_amount -
original_contract_amount`.

Diagnostic:
1. List all COs for the commitment by status; sum `cost_delta` where
   `status = approved`.
2. Compare to `commitment.revised_contract_amount -
   commitment.original_contract_amount`.
3. Identify whether a pending CO was incorrectly counted, an approved
   CO was missed, or a CO was voided without adjusting the revised
   total.

Resolution:
- If a pending CO was counted: exclude it from the revised total; only
  approved COs extend the ceiling.
- If an approved CO was missed: ensure the revised_contract_amount
  reflects all approved COs; Procore normally computes this
  automatically, so manual divergence indicates a data entry error.
- Run `pc_recon_co_pending_excluded_from_budget` to confirm fix.

## draw_cost_drift

Trigger: `pc_consistency_draw_cost_vs_total` fails; draw `cost_to_date +
cost_to_complete_estimate` does not reconcile to
`commitment.revised_contract_amount` within band.

Diagnostic:
1. Sum reported cost_to_date and cost_to_complete on the active draw.
2. Compare to commitment revised total.
3. Identify drift source: stale cost-to-complete estimate, missing
   CO reflection in cost-to-date, stored materials allocation.

Resolution:
- Update the GC's cost-to-complete estimate on the current draw.
- Confirm stored materials are properly included or excluded per
  lender policy.
- If drift persists, request an updated schedule-of-values from the GC.

## expired_insurance_active_commitment

Trigger: `pc_consistency_vendor_insurance_active` fails; vendor bound
to an active commitment has lapsed insurance per `insurance_expiry`.

Resolution:
- Request current COI from the vendor before next pay-app approval.
- Block further draws to the vendor until COI is current.
- If vendor cannot produce current COI, escalate to construction_lead
  and consider vendor substitution per `vendor_substitution`.
- Update `vendor_master_crosswalk` and AP vendor master with refreshed
  `insurance_expiry_date` once COI is received.

## commitment_vs_po_ambiguity

Trigger: A Procore Purchase Order and a Work Order Contract (subcontract)
appear for overlapping scope on the same project, creating a canonical
`commitment` double-count risk.

Diagnostic:
1. Inspect `commitment.title` and `cost_code` across both records.
2. Review the PO's billing activity; POs for material supply usually
   have single-shot billing, subcontracts have progressive billing.
3. Confirm with the project accountant which contract carries the active
   scope.

Resolution:
- Keep both canonical `commitment` rows but flag one as
  `commitment_type = purchase_order` and the other as `subcontract`.
- If the PO is actually a subset of the subcontract scope (materials
  furnished through the subcontractor), close the duplicate PO in Procore
  and preserve history.
- Reconcile billed-to-date sums against the project cost_to_complete
  calculation; ensure no double-count.

## co_category_drift

Trigger: `change_order.reason_code` values drift from the expected Procore
taxonomy (operator team introduces custom reason codes like "PM request"
that do not map to canonical `category` enum).

Diagnostic:
1. List unique `reason_code` values across the last 90 days of Procore COs.
2. Identify codes not in the expected set:
   `owner_directive, design_error, unforeseen, scope_clarification, site_condition`.

Resolution:
- Update `map_procore_co_category` mapping for legitimate new variants
  (e.g., add `pm_request -> owner_directed`).
- Coach the operator team on the standard taxonomy; Procore custom
  reason codes should be aliased, not invented.
- Add a canonical `category = null` flag for codes that legitimately have
  no canonical equivalent; require operator narrative for each.

## cost_posting_lag

Trigger: `pc_recon_commitment_vs_posted_spend` fails; Procore
`paid_to_date` exceeds Intacct posted `capex_actual` beyond
`capex_posting_band`.

Diagnostic:
1. Identify the specific commitments with the largest gaps.
2. Check the Intacct AP invoice queue for unposted batches referencing
   the Procore pay-app.
3. Check the Intacct GL for correct `dim_project` attribution per
   `capex_project_crosswalk`.

Resolution:
- If the gap is a queued AP batch, expedite posting per the operator's
  AP close schedule.
- If the gap is a misattribution (Intacct posting lacks `dim_project`),
  post a correcting reclass JE per
  `sage_intacct_common_issues.md::manual_journal_attrib`.
- If the gap is a structural mismatch (Procore pay-app tied to a
  commitment not yet synced to Intacct), create the Intacct AP record
  and backdate the invoice to the Procore-side billing date.

## co_posting_lag

Trigger: `pc_recon_co_approved_vs_invoice_posted` fails; approved Procore
CO has no matching Intacct invoice line within `co_posting_lag_band`.

Diagnostic:
1. Look up the Procore CO approval date and the expected Intacct posting
   window.
2. Check the Intacct AP queue for a posted invoice referencing the CO.
3. Confirm the CO is linked in `change_order_crosswalk`.

Resolution:
- If lag is operational (paperwork queue), expedite Intacct posting.
- If the CO is genuinely miscategorized (approved in Procore but the GC
  has not yet billed against the CO), flag as expected-lag and track.
- If the Intacct invoice exists but is not linked to the Procore CO, add
  the `change_order_crosswalk` row and re-run the recon.

## draw_posting_lag

Trigger: `pc_recon_draw_approved_vs_cash_funded` fails; approved Procore
draw lacks a corresponding Intacct funding line within
`draw_posting_lag_band`.

Diagnostic:
1. Confirm the draw's `status = approved OR funded`.
2. Check with the lender (or equity commitment) for funding status.
3. Check the Intacct GL for the funding receipt.

Resolution:
- Normal lag (funding in transit): track; clears on funding receipt.
- Structural lag (operator failed to reserve the Intacct journal id):
  create the Intacct funding line and backdate.
- Lender delay: escalate via `draw_package_review` workflow; do not
  auto-approve further draws until the lag clears.

## schedule_baseline_overwrite

Trigger: `pc_consistency_schedule_baseline_preserved` fails; milestone
`baseline_date` changed without an operator note or
`baseline_revision_id` advance.

Diagnostic:
1. Identify which milestones changed baseline.
2. Review Procore's schedule change log for the change author and date.
3. Confirm whether the change was intentional (re-baselining after a
   major CO) or accidental (PM dragging a Gantt bar).

Resolution:
- Intentional re-baselining: advance `baseline_revision_id` (e.g.,
  `baseline_v2`); attach an operator note explaining the trigger; preserve
  prior baseline under `prior_baseline_revisions[]`.
- Accidental change: revert the baseline in Procore; coach the PM on
  baseline preservation discipline.
- If Procore's schedule baseline feature was never enabled, open a data
  readiness gap ticket per `runbooks/procore_onboarding.md::step_6`.

## vendor_master_duplication

Trigger: `pc_recon_vendor_three_way_identity` warns; the same legal
vendor appears with different `source_id` values in Procore, Intacct, and
AppFolio but resolves inconsistently through `vendor_master_crosswalk`.

Diagnostic:
1. List the distinct canonical_ids the vendor resolves to across the
   three systems.
2. Compare `legal_name`, `tax_id_last_four`, and trade.
3. Check the crosswalk's `effective_start` and `effective_end` on each
   row for vendor rename/split history.

Resolution:
- Merge: Pick the surviving canonical_id per `vendor_master_default`
  survivorship rule; close the duplicate canonical rows with
  `effective_end`; add a `related_canonical_ids` pointer for history.
- Split: If two legal entities share a name, confirm distinct
  `tax_id_last_four` and keep the canonical_ids separate; annotate the
  crosswalk with an operator note.
- Escalation: Route to AP manager for AP-side consolidation; the AP
  record is authoritative for legal name and tax_id per survivorship.

## bid_leveling_normalization

Trigger: A Procore bid package's leveled-bid output carries unit prices
that deviate from the Excel `material_cost_reference` by more than
`material_reference_drift_band`.

Diagnostic:
1. Compare the leveled bid line items to the reference library unit
   costs by cost_code.
2. Identify whether the deviation is a legitimate market-cost change
   (lead time, tariff, spec escalation) or a bid error.
3. Check the as_of_date on the Excel reference.

Resolution:
- If the reference is stale (as_of_date > staleness_threshold), refresh
  per `runbooks/benchmark_refresh.md`.
- If the bid is genuinely above market, negotiate down or confirm the
  escalation rationale in the bid comparison notes.
- If the bid is below market (suspicious), request the bidder confirm
  scope coverage; underbids often reflect scope gaps that become COs.

## retainage_closeout_drift

Trigger: `pc_recon_retainage_at_closeout` fails at commitment closeout;
commitment `retention_balance_cents` does not equal sum of retainage
held minus released per pay-app within `retainage_closeout_band`.

Diagnostic:
1. Total pay-app `retainage_held_this_period` and subtract
   `retainage_released_this_period` per commitment.
2. Compare to commitment `retention_balance_cents`.
3. Review the retainage schedule in the commitment (often stepped release
   at 50% completion and final closeout).

Resolution:
- Reconcile differences at the pay-app level; adjust the final pay-app
  retainage release amount.
- If there is a structural error in the commitment retainage schedule,
  open a commitment amendment (rare but permitted in Procore).
- Record the resolution note on the commitment and close.

## percent_complete_drift

Trigger: Physical percent complete (from schedule or punchlist) and cost
percent complete (from Procore pay-app) diverge by more than the allowed
band.

Diagnostic:
1. Compare `milestone.percent_complete` for related milestones to
   `draw.percent_complete_cost`.
2. Check for front-loaded billing (cost % > physical %) or slow billing
   (cost % < physical %).

Resolution:
- Front-loaded billing: Require the GC to rebalance the schedule of
  values; retainage adjustment may apply.
- Slow billing: Expedite pay-app submission; confirm cost accruals in
  Intacct.
- Persistent drift: Raise a schedule vs billing alignment flag in
  `draw_package_review`.

## orphan_commitment

Trigger: `pc_referential_commitment_project_fk` fails; commitment
references a project_id not resolvable through `capex_project_crosswalk`.

Diagnostic:
1. Confirm the Procore project_id exists in the current feed.
2. Check whether `capex_project_crosswalk` has a row for that project.
3. Confirm the canonical_id the project should resolve to.

Resolution:
- Add the crosswalk row with the correct canonical_id.
- If the project was deleted in Procore but commitments remain, archive
  the commitments as historical and do not load canonically.
- Never accept a commitment without a resolved canonical project id.

## orphan_dev_project

Trigger: `pc_recon_procore_project_has_dealpath_anchor` fails; a Procore
development project (construction_type = new_construction) has no
`dev_project_crosswalk` row linking to a Dealpath asset.

Diagnostic:
1. Confirm the project was IC-approved in Dealpath.
2. Check whether the Dealpath deal was closed under a different asset_id
   than the Procore project expects.
3. Check whether the project was opened in Procore before IC approval
   (anti-pattern; flag).

Resolution:
- Add the `dev_project_crosswalk` row linking the Procore project to
  the Dealpath asset_id.
- If the Dealpath deal was never actually IC-approved, archive the
  Procore project and escalate to development_lead.

## orphan_co

Trigger: `pc_referential_change_order_commitment_fk` fails; CO references
a commitment_id not in the commitment feed.

Resolution:
- Confirm the commitment is in Procore (feed pull issue vs actual
  deletion).
- If commitment was deleted, the CO should also be voided; coordinate
  with the project accountant.
- If feed gap: rerun the commitment pull.

## orphan_draw

Trigger: `pc_referential_draw_project_fk` fails; draw references a
project_id not resolvable through `capex_project_crosswalk`.

Resolution: Same pattern as `orphan_commitment`; resolve project
crosswalk first before loading the draw canonically.

## commitment_overdrawn

Trigger: `pc_consistency_commitment_overdrawn` and
`pc_recon_commitment_overdrawn` fail.

Diagnostic:
1. Compute `paid_to_date + retainage_balance` vs
   `revised_contract_amount`.
2. Identify the overage driver: pending CO not yet approved, forex
   translation, bid escalation, double-posting.

Resolution:
- Approve the pending CO to extend the ceiling (normal path).
- Post a corrective reclass if the overage is a double-posting.
- Open a write-off approval if the overage is genuine overspend without
  a CO.
- Block further draws on the commitment until resolved.

## commitment_void_with_draws

Trigger: commitment `status = void OR terminated` with approved draws
posted.

Resolution:
- Confirm the Intacct postings remain valid or require a reversing JE.
- Record the void reason on the commitment.
- Open a substitution commitment (if a replacement vendor is engaged);
  reassign forward work.

## pending_co_work_performed

Trigger: Pending CO with field evidence of work performed.

Resolution:
- Expedite CO approval.
- Do not extend the commitment ceiling or approve draws against the
  pending CO amount until approved.
- Flag the draw package review workflow.

## draw_rejected_resubmit

Trigger: Prior-period draw `status = rejected`; same commitment and
period, new draw `status = submitted`.

Resolution:
- Preserve the rejected draw as audit; load the resubmit as the active
  draw.
- Confirm the rejection reason was addressed in the resubmit.

## vendor_substitution

Trigger: Commitment voided; new commitment opens with a different
vendor for the same scope.

Resolution:
- Open a substitution note in `vendor_master_crosswalk` with
  `manual_override = true`.
- Link original and replacement commitments via `related_canonical_ids`.
- Reassess vendor COI and W-9 on file for the new vendor.

## project_archived_pending_draw

Trigger: Project `active = false` with draws still in `submitted` or
`under_review`.

Resolution:
- Expedite draw closure; a project should not archive with pending
  draws.
- If archive was accidental, un-archive in Procore.

## subcontractor_distress

Trigger: Vendor insurance lapse or legal distress signal; commitment
flipped to void; pay-apps cease.

Resolution:
- Block further dispatch per `vendor_insurance_active` blocker.
- Initiate vendor substitution per above.
- Notify surety / bonding company if a bonded subcontractor.

## delivery_handoff

Trigger: Procore project reaches `Post Construction`, but
`property_master_crosswalk` has no AppFolio or Yardi row linking back.

Resolution:
- Create the PMS property record immediately; seed
  `property_master_crosswalk`.
- Block lease-up workflows until handoff completes.
- Coordinate with regional_ops_director and asset_mgmt_director per
  the `delivery_handoff` workflow's approval matrix.
