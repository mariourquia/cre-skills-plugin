# Dealpath Adapter — Edge Cases

Documented operator-observed edge cases and how the adapter handles
them. Each entry points to the rule_id or runbook that mitigates, and to
the tolerance-band reference where applicable. No numeric thresholds
appear inline; cite
`reference/normalized/schemas/reconciliation_tolerance_band.yaml`.

---

## 1. Deal renamed after IC approval

**Scenario.** The deal name is a free-text operator label and is
frequently changed after `ic_approved` for legal-entity alignment,
marketing alignment, or portfolio labeling.

**Adapter behavior.** `deal_id` is stable and primary; `deal_name` is
not. A rename produces a `deal_status_history` row with
`transition_type = rename` and is fed into `source_record_audit`.
Downstream workflows resolve by `deal_id` only. The rename check
(`dp_recon_deal_rename_audit`) warns if the audit row is missing.

**Owner.** `investments_lead` acknowledges; no downstream rebinding
required.

---

## 2. asset_id reused across pipeline stages

**Scenario.** Operators sometimes re-use the same Dealpath `asset_id`
to represent a reprise of a prior deal (e.g., a deal that went dead in
2024 is revived in 2026). The same asset_id may appear on multiple deal
rows with non-overlapping active windows.

**Adapter behavior.** `asset_id` is the Dealpath master key; the same
asset_id may legitimately appear on multiple deals. Canonical
`asset_crosswalk` resolution handles effective-dating via
`effective_start` per mapping row. No blocking; tracked under the
stable mapping rule. Where the prior deal had an AppFolio property
setup, the new deal inherits unless the operator flags
`reinitialize_property = true`.

---

## 3. Dev deal later reclassified as acquisition (or vice versa)

**Scenario.** A deal that entered as `deal_type = development` is later
switched to `acquisition` because the operator bought a completed
asset instead of ground-up, or vice versa.

**Adapter behavior.** Adapter captures the change via
`deal_status_history` with `transition_type = deal_type_change`. The
workflow activation map re-routes from
`development_pipeline_tracking` to `pre_close_deal_tracking` (or
reverse). Any Procore project created under the prior classification
remains intact; dev_project_crosswalk carries `superseded = true` on the
stale mapping.

---

## 4. One deal spawning multiple downstream properties (portfolio acquisition)

**Scenario.** A portfolio deal closes on five properties simultaneously;
one Dealpath deal record but five AppFolio properties and five
Intacct entities.

**Adapter behavior.** `property_master_crosswalk` supports many-to-one
via `manual_override = true`. The reconciliation check
`dp_recon_one_deal_one_property` warns but does not block when the
override flag is set. Each downstream property setup triggers a
separate `post_ic_property_setup` workflow instance. Cited in
`dq_rules.yaml` as `dp_one_deal_multiple_projects`.

---

## 5. One acquired asset later split into multiple operating sub-properties

**Scenario.** A single Dealpath asset closes as one deal, but after
close the operator segments it (e.g., split into two community names,
or carve a senior-housing component out of a mixed-use property).

**Adapter behavior.** Post-close reconfiguration is AppFolio-driven.
The original `property_master_crosswalk` row stays; a second row is
added with `effective_start = split_event_date` and the original row
carries `survivorship_rule = superseded_at_split`. Dealpath retains
the original single-asset record; no back-propagation.

---

## 6. Deal closed but not assigned to property setup queue

**Scenario.** Deal transitions to `pipeline_stage = closed`, but the
AppFolio property setup is not kicked off. Observed when the close
happens without a complete handoff package.

**Adapter behavior.** `dp_handoff_lag` warns at the threshold; blocker
escalates beyond the multiplier. Runbook:
`dealpath_common_issues.md::closed_deal_no_setup`. Cited under
`dq_rules.yaml::dp_handoff_lag`.

---

## 7. Deal resurrected from declined / dead status

**Scenario.** A deal marked `pipeline_stage = ic_declined` or
`status = dead` is re-opened because conditions changed (seller
re-engages at lower price, strategy pivot, etc.).

**Adapter behavior.** Resurrection produces a `deal_status_history` row
with `transition_type = resurrection` and a mandatory `reason` field.
Check: `dp_recon_dead_deal_resurrection`. Re-presentation to IC is
required if the prior IC outcome was `declined`; runbook:
`dealpath_common_issues.md::declined_then_resurrected`.

---

## 8. IC condition unresolved at close

**Scenario.** Deal has `ic_decision = conditional` with unresolved
conditions when `deal_close_date_actual` is populated. Violates the
guardrail "gated action without approved prerequisite".

**Adapter behavior.** `dp_recon_condition_resolution_at_close` is a
blocker. Only a documented `policy_override_id` can permit close with
unresolved conditions; the override propagates to
`canonical.approval_request.decisions[].notes` for audit. Runbook:
`dealpath_common_issues.md::ic_condition_unresolved`.

---

## 9. Debt term sheet variance from executed loan

**Scenario.** The debt term sheet recorded at the
`milestone.debt_term_sheet` event carries different loan sizing,
pricing, or structure than the executed loan posted in Intacct
post-close.

**Adapter behavior.** `dp_recon_debt_term_sheet_vs_executed_loan` warns
at the `debt_term_sheet_variance_band` threshold (cite
`reconciliation_tolerance_band.yaml`). Narrative requirement surfaces
at the next `investment_committee_prep` run. Runbook:
`dealpath_common_issues.md::debt_term_sheet_drift`.

---

## 10. Retraded purchase price

**Scenario.** The purchase price is adjusted after `psa_signed` (retrade)
due to post-DD findings, financing movement, or seller concessions.

**Adapter behavior.** Each retrade must produce a
`deal_status_history` row documenting the change. Check
`dp_recon_retrade_purchase_price` warns beyond
`purchase_price_retrade_band`; beyond that, IC re-presentation is
required and the deal cannot progress past PSA without
`ic_re_presentation_flag = true`. Runbook:
`dealpath_common_issues.md::retrade_purchase_price`.

---

## 11. Late legal entity assignment

**Scenario.** The deal closes, but Intacct legal entity and project
dimensions are not set up within
`legal_entity_setup_lag_threshold_days` of close. Observed when the
ops/finance handoff slips.

**Adapter behavior.** `dp_recon_ic_approval_to_intacct_entity` warns at
threshold; blocker beyond the multiplier. Back-dating rule ensures
entity effective date = `deal_close_date_actual`, not late-creation
date. Runbook: `dealpath_common_issues.md::late_legal_entity_setup`.

---

## 12. Multi-asset deal where some assets close and others don't

**Scenario.** A portfolio deal partially closes — three of five assets
clear due diligence and close; two fall out. Dealpath retains one deal
record; AppFolio / Intacct see three new operating entities, not five.

**Adapter behavior.** `property_master_crosswalk` rows for the closed
assets carry `effective_start = deal_close_date_actual`. The two
dropped assets carry `property_master_crosswalk.status = unmapped` with
`rationale = dropped_at_partial_close`. Reconciliation treats the deal
as closed with `partial_close_flag = true`; downstream IC summary
includes the dropped-asset narrative. No blocker; tracked as
`confidence = medium` for the dropped-asset lineage.

---

## 13. Legacy deals with sparse fields

**Scenario.** Deals created before the wave-4 data stack adoption carry
sparse required fields (missing IC date, missing debt_target, partial
milestones). Common for historical records imported at system rollout.

**Adapter behavior.** `dp_legacy_sparse_field` (info severity) tags
records with `confidence = medium`. Workflow outputs annotate the
lineage. No blocker; operator remediation queue tracks backfill.

---

## 14. Dealpath deal in on_hold for extended period

**Scenario.** A deal sits at `pipeline_stage = on_hold` for months
(market pause, regulatory wait, sponsor decision). The deal is active
in Dealpath but no actual movement.

**Adapter behavior.** `pipeline_review` workflow lists on_hold deals
with `on_hold_duration_days` annotated. Beyond a threshold in
`reconciliation_tolerance_band.yaml::on_hold_duration_band`, the deal
surfaces for investments_lead review. No blocker on the data side.

---

## 15. Dealpath deal deleted (soft delete) after downstream creation

**Scenario.** A closed deal is marked `deleted_flag = true` in Dealpath
after AppFolio and Intacct have already materialized. Rare but
observed in operator cleanup passes.

**Adapter behavior.** The Dealpath delete does NOT cascade. AppFolio
and Intacct records persist; `source_record_audit` captures the delete
event. A blocker-level alert fires if a deleted Dealpath deal has
non-deleted downstream dependencies — this surfaces as an operator
acknowledgement prompt, not an auto-delete.
