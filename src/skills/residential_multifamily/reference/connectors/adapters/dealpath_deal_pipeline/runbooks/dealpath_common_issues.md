# Dealpath Common Issues Runbook

Status: stub (wave_4)
Audience: data_platform_team, investments_lead, asset_mgmt_director,
finance_systems_team

Maps commonly observed operator issues to the triggering DQ rule /
reconciliation check, the investigation path, and the remediation owner.
Tolerances cite
`reference/normalized/schemas/reconciliation_tolerance_band.yaml`.

---

## stale_feed

**Trigger rule.** `dp_freshness_deals`.
**Symptom.** The Dealpath feed has not landed within
`expected_latency_minutes` from `source_registry_entry.yaml`.
**Investigation.**

1. Check the Dealpath API status page.
2. Confirm the adapter's last successful extractor run in
   `monitoring/observability_events.yaml`.
3. Check for credential expiration — keys that rolled overnight are
   the most common cause.

**Remediation.** Roll the API key per `security/secrets_handling.md`,
re-run the extractor, confirm freshness.
**Owner.** `data_platform_team`; escalates to `investments_lead` if
blocker persists >1 business day.

---

## rename_after_approval

**Trigger rule.** `dp_renamed_after_approval`,
`dp_recon_deal_rename_audit`.
**Symptom.** `deal_name` changed after `pipeline_stage = ic_approved`;
audit row missing or change not reflected in downstream workflows.
**Investigation.**

1. Confirm the rename in Dealpath UI by `deal_id`.
2. Check `deal_status_history` for a row with
   `transition_type = rename`.
3. If the audit row is missing, check the extractor for a bug in the
   status-history pull.

**Remediation.** Backfill the audit row via
`master_data/unresolved_exceptions_queue.md`. Confirm downstream
workflows resolve by `deal_id`, not `deal_name`.
**Owner.** `investments_lead` acknowledges; `data_platform_team`
patches the extractor.

---

## multi_property_deals

**Trigger rule.** `dp_one_deal_multiple_projects`,
`dp_recon_one_deal_one_property`.
**Symptom.** One Dealpath `deal_id` corresponds to multiple AppFolio
`PropertyId`s or multiple Procore projects.
**Investigation.**

1. Confirm the deal is a portfolio acquisition or phased delivery.
2. Check `property_master_crosswalk` for `manual_override = true` on
   the affected rows.

**Remediation.** Set `manual_override = true` with a `rationale` on
each related crosswalk row. Document the split in the deal-notes
field. Downstream `post_ic_property_setup` runs once per related
property.
**Owner.** `asset_mgmt_director` and `investments_lead` jointly
approve the override.

---

## declined_then_resurrected

**Trigger rule.** `dp_recon_dead_deal_resurrection`.
**Symptom.** Deal previously marked `status = dead` or
`ic_declined` has been re-activated without an IC re-presentation
record.
**Investigation.**

1. Confirm the status transition in `deal_status_history`.
2. Check for a new `ic_decision` row post-resurrection.
3. Confirm the deal team reviewed prior-decision conditions.

**Remediation.** Require an IC re-presentation if the prior decision
was `declined`. Create a new `ic_decision` row; the resurrected deal
cannot progress past `psa_executed` without a fresh approval.
**Owner.** `investments_lead`.

---

## asset_id_reuse

**Trigger rule.** Not a standalone rule; observed during
`asset_crosswalk` resolution.
**Symptom.** The same Dealpath `asset_id` appears on multiple deals
with overlapping active windows.
**Investigation.**

1. Confirm whether one deal is a reprise of the other.
2. Check `asset_crosswalk` for multiple rows with the same
   `dealpath_id` but different `effective_start`.

**Remediation.** Effective-date the crosswalk correctly; ensure the
active deal resolves to the current canonical_asset_id. Prior deal
retains its original mapping as `status = superseded`.
**Owner.** `data_platform_team`.

---

## ic_condition_unresolved

**Trigger rule.** `dp_recon_condition_resolution_at_close`,
`dp_recon_ic_decision_to_approval_request`.
**Symptom.** Deal approaching or at close with unresolved conditions
from a `conditional` IC decision.
**Investigation.**

1. List outstanding conditions from the `ic_decision.conditions` array.
2. Verify resolution status via the canonical
   `approval_request.decisions[].notes` stream.
3. If the deal has already closed, flag the guardrail breach.

**Remediation.** Block close until conditions resolve, OR obtain a
documented `policy_override_id` (requires `chief_investment_officer`
sign-off). Override propagates to audit.
**Owner.** `investments_lead` with `chief_investment_officer` on
override path.

---

## debt_term_sheet_drift

**Trigger rule.** `dp_recon_debt_term_sheet_vs_executed_loan`.
**Symptom.** Debt term sheet value recorded at
`milestone.debt_term_sheet` differs from the executed loan posted in
Intacct post-close beyond `debt_term_sheet_variance_band` (cite
`reconciliation_tolerance_band.yaml`).
**Investigation.**

1. Pull the term sheet document from `deal_document` rows.
2. Confirm the executed loan face amount, rate, and term in Intacct.
3. Identify whether the variance is sizing, pricing, or structural.

**Remediation.** Operator narrative required at the next
`investment_committee_prep` run. If drift exceeds the escalation
threshold, trigger a debt-re-presentation event. Post-drift state is
canonical (Intacct primary).
**Owner.** `debt_lead` drafts the narrative;
`investments_lead` reviews.

---

## closed_deal_no_setup

**Trigger rule.** `dp_handoff_lag`, `dp_recon_asset_to_property`,
`dp_recon_handoff_lag_af`.
**Symptom.** Closed acquisition / recap deal lacks AppFolio property
setup beyond `handoff_lag_threshold_days` (cite
`reconciliation_tolerance_band.yaml`).
**Investigation.**

1. Verify the close event fired end-to-end (GL posting, wire
   confirmation, title transfer).
2. Check the `post_ic_property_setup` workflow queue for the missing
   trigger.
3. Confirm `property_master_crosswalk` row exists with
   `status = pending_close`.

**Remediation.** Kick off AppFolio property setup manually. Populate
the crosswalk row, flip to `status = active`, and trigger the setup
workflow. Escalate to `asset_mgmt_director` if the lag exceeds the
threshold multiplier.
**Owner.** `asset_mgmt_director` owns; `regional_ops_director`
executes setup.

---

## dev_handoff

**Trigger rule.** `dp_handoff_dev_lag`,
`dp_recon_dev_deal_to_procore_project`,
`dp_recon_dev_handoff_lag_pc`.
**Symptom.** Development deal with `milestone.gc_selected = achieved`
lacks a Procore project beyond `dev_handoff_lag_threshold_days` (cite
`reconciliation_tolerance_band.yaml`).
**Investigation.**

1. Confirm gc_selected event and associated gc_award documentation.
2. Check whether Procore project was created under a different name
   or company_id.
3. Inspect `dev_project_crosswalk` for a pending-award row.

**Remediation.** Create the Procore project with
`dev_project_crosswalk` effective_start = `milestone.gc_selected.actual_date`.
Notify `construction_lead` to take over project primary status.
**Owner.** `development_lead` owns; `construction_lead` executes
Procore setup.

---

## one_deal_multiple_projects

**Trigger rule.** `dp_one_deal_multiple_projects`,
`dp_recon_one_deal_one_property`.
**Symptom.** A single Dealpath development deal splits into multiple
Procore projects (phased delivery, multiple buildings).
**Investigation.**

1. Confirm the phasing plan against the approved IC memo.
2. Check whether the adapter created one or many
   `dev_project_crosswalk` rows.

**Remediation.** Set `manual_override = true` on all related
`dev_project_crosswalk` rows with `rationale = phased_delivery`. Each
Procore project runs its own `development_pipeline_tracking` instance.
The parent Dealpath deal remains one row.
**Owner.** `development_lead`; `investments_lead` acknowledges.

---

## late_legal_entity_setup

**Trigger rule.** `dp_recon_ic_approval_to_intacct_entity`.
**Symptom.** Closed deal lacks Intacct legal entity / project
dimension beyond `legal_entity_setup_lag_threshold_days` (cite
`reconciliation_tolerance_band.yaml`).
**Investigation.**

1. Check whether the entity was created under a different name or
   parent in Intacct.
2. Confirm close posting landed in Intacct.

**Remediation.** Set up the entity with `effective_date =
deal_close_date_actual` (back-dated) to preserve close-period
consistency. Log the delay as a `confidence_reduction` event.
**Owner.** `finance_systems_team` owns; `controller` signs off on
back-dating.

---

## retrade_purchase_price

**Trigger rule.** `dp_recon_retrade_purchase_price`.
**Symptom.** Purchase price adjusted after `psa_signed`; variance
exceeds `purchase_price_retrade_band`.
**Investigation.**

1. Pull the original PSA and the retrade amendment.
2. Confirm the `deal_status_history` row captures the change.
3. If variance exceeds the IC re-presentation threshold, check for
   `ic_re_presentation_flag = true` on the deal.

**Remediation.** Beyond the re-presentation threshold, deal cannot
progress without a fresh IC review. Document the retrade rationale
in the `reason` field.
**Owner.** `investments_lead`.

---

## legacy_sparse_field

**Trigger rule.** `dp_legacy_sparse_field`.
**Symptom.** Pre-wave-4 legacy deal lands with sparse required fields
(missing IC date, debt_target, etc.).
**Investigation.**

1. Confirm the deal is pre-wave-4 by inspecting `created_at`.
2. Identify which fields are null.

**Remediation.** Tag the record `confidence = medium` and leave in
place. Backfill via operator interview if the deal is still active.
Do not synthesize values.
**Owner.** `investments_lead` backfills; `data_platform_team`
monitors.
