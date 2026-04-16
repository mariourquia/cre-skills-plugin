# Procore Adapter — Edge Cases

Operational edge cases the wave-5 rollout must handle or at least surface.
Each case names the observable signal, the adapter-side behavior, the
canonical knock-on effect, and the runbook that resolves it. All numeric
thresholds cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.

## 1. Project re-baselined mid-construction

- Signal: `baseline_revision_id` advances on one or more milestones during a
  pull; prior `baseline_date` values no longer appear.
- Adapter behavior: Preserve the prior baseline under
  `prior_baseline_revisions[]` in the raw landing zone; require an operator
  note attached to the new `baseline_revision_id`; fail
  `pc_consistency_schedule_baseline_preserved` when the note is missing.
- Canonical effect: Slippage computation uses the current baseline; prior
  baselines are audit-only.
- Runbook: `runbooks/procore_common_issues.md::schedule_baseline_overwrite`.

## 2. Commitment cancelled but draws already posted

- Signal: `commitment.status = void OR terminated` but associated
  `draw_request` rows exist with `approval_status IN (approved, funded)`.
- Adapter behavior: Flag commitment for reconciliation; keep the draws as
  audit rows tied to the void commitment; do not remove posted Intacct
  entries (those require a reversing JE in Intacct).
- Canonical effect: `capex_actual` retains the posted amount; the
  commitment-vs-paid reconciliation logs the gap as a legacy-posted
  anomaly.
- Runbook: `runbooks/procore_common_issues.md::commitment_void_with_draws`.

## 3. Change order pending approval but work performed

- Signal: `change_order.status = pending` but field reports indicate the
  added scope has begun; draws begin referencing the CO line.
- Adapter behavior: Do not include the pending CO in
  `revised_contract_total_cents`; flag the draw as referencing a non-approved
  CO; raise a `change_order_review` workflow block.
- Canonical effect: Ceiling not extended; draw payout potentially frozen
  pending CO approval.
- Runbook: `runbooks/procore_common_issues.md::pending_co_work_performed`.

## 4. Draw rejected and resubmitted

- Signal: Two draws for the same commitment within one billing period; the
  first carries `status = rejected`; the second is `status = submitted`.
- Adapter behavior: Both draws load; the rejected draw is flagged
  non-billable; the resubmit is the active draw; rejection audit trail is
  preserved in `draw_request_crosswalk` effective dating.
- Canonical effect: Canonical `DrawRequest` for the period reflects the
  resubmit; `approval_status = submitted` or `in_review`.
- Runbook: `runbooks/procore_common_issues.md::draw_rejected_resubmit`.

## 5. Vendor change mid-project (subcontract substitution)

- Signal: A new `commitment` opens with an alternate `contract_company_id`
  while the original commitment's status transitions to `void OR terminated`.
- Adapter behavior: Preserve both commitment rows; record a substitution
  note in `vendor_master_crosswalk` with `manual_override = true`; link
  the substituted and original commitments via `related_canonical_ids`.
- Canonical effect: Canonical `commitment` set carries both records;
  downstream CO and draw feeds re-anchor to the new commitment_id.
- Runbook: `runbooks/procore_common_issues.md::vendor_substitution`.

## 6. Schedule slip past go-live

- Signal: `milestone.current_forecast_date` for a go-live milestone
  (e.g., Temporary CO) slips beyond `target_completion` per
  `delivery_handoff_band`.
- Adapter behavior: Raise a blocker on the delivery handoff recon
  (`pc_recon_project_to_property_delivery_handoff`); pause lease-up first
  period workflow; surface in schedule_risk_review.
- Canonical effect: `ConstructionProject.status` stays `in_progress`; the
  downstream AppFolio property_setup trigger does not fire.
- Runbook: `runbooks/procore_common_issues.md::delivery_handoff`.

## 7. Retainage release

- Signal: At commitment closeout, pay-app line carries
  `retainage_released_this_period > 0` reducing `retainage_balance` to zero.
- Adapter behavior: Final pay-app carrying retainage release loads
  normally; `pc_recon_retainage_at_closeout` runs to reconcile total
  retention held minus released to commitment `retention_balance_cents`.
- Canonical effect: `commitment.status = closed`;
  `retention_balance_cents = 0`.
- Runbook: `runbooks/procore_common_issues.md::retainage_closeout_drift`
  when drift exceeds band.

## 8. Deductive change order

- Signal: `change_order.cost_delta < 0` with `status = approved`.
- Adapter behavior: Load without special handling; the canonical
  `ChangeOrder.cost_delta_cents` stores the negative value;
  `pc_consistency_co_sum_vs_revised` reconciles the net (additive +
  deductive) sum to the revised contract amount.
- Canonical effect: Commitment revised total decreases; downstream budget
  snapshot reflects the reduction.
- Runbook: None specific; edge is standard behavior.

## 9. CO bundling vs individual posting

- Signal: Multiple Procore COs posted together to Intacct as a single
  journal line, or conversely one Procore CO split across multiple Intacct
  journal lines.
- Adapter behavior: `change_order_crosswalk` supports N:1 and 1:N linkage
  via `related_canonical_ids`; adapter does not enforce 1:1 mapping; recon
  sums Intacct side by canonical CO id set.
- Canonical effect: Every canonical `ChangeOrder` reconciles to its set of
  Intacct posting lines; operator notes document the split.
- Runbook: `runbooks/procore_common_issues.md::co_posting_lag` covers
  detection; the crosswalk file carries the mapping.

## 10. Project handoff during close period

- Signal: Procore project transitions to `Post Construction` within a
  day or two of an Intacct close period; final cost snapshot timing
  straddles the close.
- Adapter behavior: Adapter respects `posting_period_close_wins` — once
  Intacct closes the period, Intacct is authoritative for any cost
  actualization within the closed period; Procore continues to update
  construction-side state for the post-close period.
- Canonical effect: `capex_actual` from Intacct freezes for the closed
  period; Procore-side corrections require a new-period reclass entry.
- Runbook: `runbooks/procore_common_issues.md::cost_posting_lag` + close
  coordination with `runbooks/sage_intacct_common_issues.md` (proposed).

## 11. Project archived while final draw pending

- Signal: `project.active = false` and `stage = Closed OR Warranty` while
  one or more draws carry `status IN (submitted, under_review)`.
- Adapter behavior: Archive flag suspends ingest of new objects for the
  project but preserves in-flight records; flag final-draw lag for
  expeditious closeout review.
- Canonical effect: Canonical project status stays `in_progress` until
  final draw resolves; archive does not close the project canonically.
- Runbook: `runbooks/procore_common_issues.md::project_archived_pending_draw`.

## 12. Commitment overdrawn from forex/escalation

- Signal: `commitment.paid_to_date + retainage_balance > revised_contract_amount`
  beyond `overdrawn_tolerance_band`, typically due to forex translation
  differences on imported materials or post-quote escalation on
  long-lead-time items without a CO to paper the increase.
- Adapter behavior: Block the commitment at
  `pc_consistency_commitment_overdrawn`; route to construction_lead for
  corrective CO or write-off decision.
- Canonical effect: Commitment flagged; downstream
  `cost_to_complete_review` blocks for the project until resolution.
- Runbook: `runbooks/procore_common_issues.md::commitment_overdrawn`.

## 13. Mid-project sub-bankruptcy

- Signal: Subcontractor vendor becomes inactive or marked in legal
  distress; commitment `status` manually flipped to `void` or
  `terminated`; pay-apps abruptly cease; insurance lapses.
- Adapter behavior: Raise
  `pc_consistency_vendor_insurance_active` blocker; preserve commitment
  history; require operator to open a substitution commitment (see edge
  case 5); block further draws to the distressed vendor.
- Canonical effect: Vendor flagged; commitment retained as historical
  reference; replacement vendor's commitment becomes canonical forward.
- Runbook: `runbooks/procore_common_issues.md::subcontractor_distress`.

## Summary matrix

| Edge Case | DQ Rule | Recon Check | Runbook |
|---|---|---|---|
| Re-baselined schedule | pc_consistency_schedule_baseline_preserved | pc_recon_schedule_baseline_preserved | schedule_baseline_overwrite |
| Void commitment with draws | pc_consistency_commitment_overdrawn (adjacent) | pc_recon_commitment_overdrawn | commitment_void_with_draws |
| Pending CO + work performed | pc_consistency_co_sum_vs_revised | pc_recon_co_pending_excluded_from_budget | pending_co_work_performed |
| Rejected and resubmit draw | pc_uniqueness_draw_request_id | pc_recon_draw_approved_vs_cash_funded | draw_rejected_resubmit |
| Vendor substitution | pc_referential_vendor_master_fk | pc_recon_vendor_three_way_identity | vendor_substitution |
| Schedule slip past go-live | pc_consistency_schedule_baseline_preserved | pc_recon_project_to_property_delivery_handoff | delivery_handoff |
| Retainage release | pc_consistency_co_sum_vs_revised (adjacent) | pc_recon_retainage_at_closeout | retainage_closeout_drift |
| Deductive CO | pc_consistency_co_sum_vs_revised | pc_recon_co_pending_excluded_from_budget | n/a |
| CO bundling | pc_uniqueness_change_order_id | pc_recon_co_approved_vs_invoice_posted | co_posting_lag |
| Handoff during close | n/a | pc_recon_commitment_vs_posted_spend | cost_posting_lag |
| Archived w/ pending draw | pc_freshness_draws | pc_recon_draw_approved_vs_cash_funded | project_archived_pending_draw |
| Commitment overdrawn | pc_consistency_commitment_overdrawn | pc_recon_commitment_overdrawn | commitment_overdrawn |
| Subcontractor distress | pc_consistency_vendor_insurance_active | pc_recon_vendor_three_way_identity | subcontractor_distress |
