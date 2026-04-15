---
name: Acquisition Handoff
slug: acquisition_handoff
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Handoff-lag threshold bands, vendor-rationalization policy, opening rent roll load
  cutover windows, and insurance-binder minimum term live in overlays and tolerance
  bands. Timer constants drift. Source-of-truth primacy between dealpath, AppFolio, and
  Intacct for post-close operating objects is overlay-tunable.
applies_to:
  segment: [middle_market, luxury]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise, high_rise]
  lifecycle: [stabilized, renovation, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [asset_manager, regional_manager, reporting_finance_ops_lead, portfolio_manager, third_party_manager_oversight_lead]
  output_types: [checklist, kpi_review, memo]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/connectors/_core/stack_wave4/lifecycle_handoffs.md
    - reference/connectors/_core/stack_wave4/source_of_truth_matrix.md
    - reference/connectors/adapters/dealpath_deal_pipeline/manifest.yaml
    - reference/connectors/adapters/dealpath_deal_pipeline/dq_rules.yaml
    - reference/connectors/adapters/appfolio_pms/manifest.yaml
    - reference/connectors/adapters/sage_intacct_gl/manifest.yaml
    - reference/connectors/master_data/property_master_crosswalk.yaml
    - reference/connectors/master_data/asset_crosswalk.yaml
    - reference/connectors/master_data/vendor_master_crosswalk.yaml
    - reference/connectors/master_data/identity_resolution_framework.md
    - reference/normalized/schemas/reconciliation_tolerance_band.yaml
    - reference/normalized/approval_threshold_defaults.csv
  writes:
    - reference/connectors/master_data/property_master_crosswalk.yaml
    - reference/connectors/master_data/asset_crosswalk.yaml
    - reference/connectors/master_data/vendor_master_crosswalk.yaml
    - reference/connectors/master_data/unresolved_exceptions_queue.md
metrics_used:
  - handoff_completeness_score        # proposed: true
  - handoff_lag_days                   # proposed: true
  - vendor_rationalization_count       # proposed: true
  - opening_rent_roll_reconciliation_variance  # proposed: true
  - pma_execution_lag_days             # proposed: true
  - crosswalk_row_creation_lag_days    # proposed: true
escalation_paths:
  - kind: handoff_lag
    to: regional_ops_director -> asset_mgmt_director -> approval_request(row 7)
  - kind: missing_required_approver
    to: asset_mgmt_director -> approval_request(row 17)
  - kind: doc_package_incomplete
    to: reporting_finance_ops_lead -> asset_mgmt_director
  - kind: vendor_master_conflict
    to: regional_ops_director -> approval_request(row 19)
  - kind: insurance_gap_during_transition
    to: asset_mgmt_director + legal counsel -> approval_request(row 17)
approvals_required:
  - asset_mgmt_director_handoff_signoff
  - pma_execution_if_tpm
  - lender_reporting_registration
description: |
  Coordinates the handoff from deal close to an operating asset. Fires when Dealpath
  emits the deal-close event (Handoff 1 + Handoff 3 in
  reference/connectors/_core/stack_wave4/lifecycle_handoffs.md). Drives AppFolio
  property setup, Intacct legal-entity dimension setup, vendor master rationalization,
  opening rent roll load, PMA execution if third-party managed, lender reporting
  registration, and data-platform property_master_crosswalk row creation. Produces a
  handoff checklist with per-item status, verifies completion within the handoff-lag
  tolerance band, and surfaces blockers for gated approval. Writes back to master_data
  crosswalks via approval before the handoff is marked complete.
---

# Acquisition Handoff

## Workflow purpose

Turn a closed Dealpath deal into a fully-operational asset with auditable handoff
completion across AppFolio (operating), Intacct (financial), master data crosswalks
(data platform), and the vendor master. The workflow does not itself execute setup
steps in vendor systems; it composes the handoff checklist, validates each item's
completion against the source-of-truth matrix, and routes gated items through
`workflows/owner_approval_routing`. Handoff is not complete until every item is
within the tolerance band on `reconciliation_tolerance_band.yaml` and the
asset_mgmt_director has signed off.

## Trigger conditions

- **Explicit:** "acquisition handoff for {deal}", "open operating handoff package", "close the handoff for {property}", "handoff status for {deal}".
- **Implicit:** Dealpath `deal.stage` transitions to `closed` AND `deal_close_date_actual` is non-null for an acquisition deal type (Handoff 1 in `reference/connectors/_core/stack_wave4/lifecycle_handoffs.md`). Downstream `post_ic_property_setup` emits a `handoff_baton_pass` event at close.
- **Recurring:** none. Strictly event-driven.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Dealpath deal record (closed) | record | required | must include `deal_id`, `asset_id`, `deal_close_date_actual`, `deal_team_lead`, `target_property_count`, `lifecycle_stage_target`, `management_mode` |
| Canonical `deal`, `asset` objects | records | required | seeded by `post_ic_property_setup` or directly by Dealpath adapter |
| Placeholder `property` canonical | record | required | seeded by `post_ic_property_setup` at IC approval |
| Placeholder `approval_request` (IC) | record | required | the IC approval row from Dealpath |
| Property-level ingest expected fields | payload | required | `property_name, address, market, submarket, segment, form_factor, unit_count_total, unit_count_rentable, nrsf_total, acquired_date, legal_entity_id, management_mode` |
| Vendor onboarding intent list | list | required | inherited vendor relationships + new vendors for this asset |
| Opening rent roll (pre-close snapshot) | table | required | must reconcile to AppFolio first-load rent roll |
| PMA draft (if `management_mode=third_party_managed`) | record | conditional | required only for TPM assets |
| Lender reporting registration package | package | required | includes asset registration details, covenant reporting schedule |
| Handoff-lag tolerance band | yaml | required | from `reference/normalized/schemas/reconciliation_tolerance_band.yaml` |
| Approver roster | yaml | required | resolved per org overlay |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Handoff checklist | `handoff_checklist` | per-item status (`complete`, `in_progress`, `blocked`, `waived_with_approval`) with owner, due-date, tolerance-band check |
| Handoff completeness scorecard | `kpi_review` | `handoff_completeness_score` (proposed) + per-workstream completion % + lag days |
| Blocker memo | `memo` | narrative with cited blocker ids and source-of-truth matrix references |
| Crosswalk row draft | record | proposed `property_master_crosswalk` / `asset_crosswalk` / `vendor_master_crosswalk` rows for approval |
| ApprovalRequest: handoff sign-off | record | row 7 if handoff lag exceeds band; otherwise a terminal sign-off |
| Unresolved exception list | `checklist` | items routed to `master_data/unresolved_exceptions_queue.md` |

## Required context

`asset_class`, `segment`, `form_factor`, `lifecycle_stage`, `management_mode`, `market`, `deal_id`, `property_id` (or placeholder), `org_id`. `jurisdiction` conditionally required for legal-entity setup and lender registration.

## Process

1. **Receive close event.** Consume the Dealpath close trigger (Handoff 1 in `lifecycle_handoffs.md`). Confirm `deal.stage = closed` and `deal_close_date_actual` present. If absent, refuse.
2. **Load baseline.** Pull canonical `deal`, `asset`, placeholder `property`, IC `approval_request`, and the baton-pass payload from `post_ic_property_setup`.
3. **AppFolio property setup.** Confirm property record promoted from `pre_acquisition` to the target `lifecycle_stage` per `source_of_truth_matrix.md` (`property` primary = AppFolio). Verify `unit_count_total`, `unit_count_rentable`, `nrsf_total`, `address`, `market`, `submarket`, `form_factor` all populated. Any missing field is a `blocker`.
4. **Intacct legal entity dim.** Confirm `legal_entity_id` recorded in Intacct dimension structure (`source_of_truth_matrix.md` row `property`: secondary = intacct for legal_entity_id). Confirm project/property dimension created in Intacct.
5. **Vendor master rationalization.** For each inherited + new vendor: run identity resolution per `master_data/identity_resolution_framework.md`; de-duplicate against existing `vendor_master_crosswalk.yaml`; emit proposed additions or merges. Count goes to `vendor_rationalization_count` (proposed).
6. **Opening rent roll load.** Reconcile the pre-close rent roll to the AppFolio first-load rent roll within tolerance band (`opening_rent_roll_reconciliation_variance`, proposed). Outside-band variance blocks the handoff until explained.
7. **PMA execution (if TPM).** Verify the PMA has been executed if `management_mode=third_party_managed`. Lag computed as `pma_execution_lag_days` (proposed) from close date. Late PMA opens an exception row.
8. **Lender reporting registration.** Confirm lender-facing package submitted and acknowledgment received. Registration status becomes a checklist item; lack of acknowledgment > band triggers row 14 escalation via `workflows/owner_approval_routing`.
9. **Data-platform crosswalk row creation.** Propose new `property_master_crosswalk.yaml` row, `asset_crosswalk.yaml` row, and `vendor_master_crosswalk.yaml` additions per `master_data/crosswalk.schema.yaml`. Proposed rows are written to a staging area and only merged after approval; see `survivorship_rules.md`.
10. **Handoff-lag screen.** Compute `handoff_lag_days` (proposed) per workstream against `handoff_lag_threshold_days` from `reconciliation_tolerance_band.yaml`. Any breach routes to `workflows/owner_approval_routing` row 7.
11. **Completeness score.** Compose `handoff_completeness_score` (proposed) as weighted completion of the checklist (weights per overlay).
12. **Sign-off packet.** Assemble the asset_mgmt_director sign-off packet with the checklist, scorecard, blocker memo, and crosswalk drafts. Route via `workflows/owner_approval_routing` row 7.
13. **Confidence banner.** Surface `as_of_date` and `status` tags for every reference file and crosswalk referenced; cite the `lifecycle_handoffs.md` handoff id (`h_dp_int_to_af_setup_...`).

## Metrics used

- `handoff_completeness_score` (**proposed: true**) — weighted completion of the handoff checklist; `grain=deal`, `time_basis=as_of_date`.
- `handoff_lag_days` (**proposed: true**) — days between `deal_close_date_actual` and each handoff workstream's completion; `grain=deal`, `time_basis=event_stamped`.
- `vendor_rationalization_count` (**proposed: true**) — count of vendor master rows rationalized at handoff; `grain=deal`.
- `opening_rent_roll_reconciliation_variance` (**proposed: true**) — variance between pre-close rent roll and AppFolio first-load; `grain=property`, unit=percent.
- `pma_execution_lag_days` (**proposed: true**) — days between close and executed PMA for TPM assets; `grain=deal`.
- `crosswalk_row_creation_lag_days` (**proposed: true**) — days between close and crosswalk-row approval; `grain=deal`.

Proposed metrics will be lifted into `_core/metrics.md` in a dedicated change-log entry before the workflow is promoted beyond draft.

## Reference files used

- `reference/connectors/_core/stack_wave4/lifecycle_handoffs.md` — handoff definitions (Handoff 1 and Handoff 3).
- `reference/connectors/_core/stack_wave4/source_of_truth_matrix.md` — primacy and effective-dating rules for every canonical object surfaced.
- `reference/connectors/adapters/dealpath_deal_pipeline/manifest.yaml` and `dq_rules.yaml` — source shape; blocking rules `dp_handoff_lag` and `dp_one_deal_multiple_projects` cited.
- `reference/connectors/adapters/appfolio_pms/manifest.yaml` — PMS primary for `property`, `unit`, `lease`.
- `reference/connectors/adapters/sage_intacct_gl/manifest.yaml` — GL primary for `legal_entity_id`, posted actuals.
- `reference/connectors/master_data/property_master_crosswalk.yaml`, `asset_crosswalk.yaml`, `vendor_master_crosswalk.yaml` — crosswalks the workflow proposes rows for.
- `reference/connectors/master_data/identity_resolution_framework.md` and `survivorship_rules.md` — identity and survivorship policy.
- `reference/normalized/schemas/reconciliation_tolerance_band.yaml` — handoff lag and rent-roll reconciliation bands.
- `reference/normalized/approval_threshold_defaults.csv` — approval thresholds (rows 7, 14, 17, 19 per approval matrix).

## Escalation points

- **Handoff lag.** Any workstream exceeding `handoff_lag_threshold_days` escalates to `regional_ops_director -> asset_mgmt_director` and opens `approval_request` row 7.
- **Missing required approver.** If the asset_mgmt_director sign-off cannot be routed (role vacant per approver roster), escalates per row 17.
- **Vendor master conflict.** Unresolved duplicate or survivorship conflict goes to `master_data/unresolved_exceptions_queue.md` and routes to row 19.
- **Insurance gap during transition.** If the acquisition insurance binder expires before the owner's permanent policy is bound, escalates to legal + asset_mgmt_director per row 17.
- **Doc package incomplete.** Lender reporting or PMA docs below completeness threshold routes to `reporting_finance_ops_lead`.

## Required approvals

- `asset_mgmt_director_handoff_signoff` — terminal approval that marks handoff complete. Required for every acquisition.
- `pma_execution_if_tpm` — row 19 (PMA amendment / owner-binding contract) if `management_mode=third_party_managed`.
- `lender_reporting_registration` — row 14 (lender-facing submission marked `final`) when the registration package is transmitted.
- Crosswalk row additions to master_data: routed via `workflows/owner_approval_routing` per `survivorship_rules.md`.

## Failure modes

1. **Silent lifecycle_stage advance.** Property flipped to `stabilized` in AppFolio without AppFolio primary confirmation. Fix: source-of-truth matrix check required before promotion.
2. **Vendor master duplication.** New vendors added without identity resolution. Fix: `identity_resolution_framework.md` is a required step.
3. **Opening rent roll ignored.** Variance > band passed forward. Fix: handoff halts until variance explained or waived with approval.
4. **PMA missing for TPM.** Handoff marked complete without PMA. Fix: conditional required input; `pma_execution_if_tpm` approval gate.
5. **Crosswalk row approved before handoff completeness verified.** Fix: staging area + survivorship rule enforcement.
6. **Lender registration drift.** Registration acknowledgment not received before close + 10 business days. Fix: escalation via row 14.
7. **Multi-asset deal split not propagated.** `dp_one_deal_multiple_projects` warning raised by Dealpath but handoff assumes 1:1. Fix: workflow refuses until mapping is manually resolved.
8. **Stale confidence banner.** `as_of_date` references older than the close date without acknowledgement. Fix: banner required per overlay staleness rule.

## Edge cases

- **Late deal close.** Dealpath `deal_close_date_actual` arrives later than expected. The workflow backfills on arrival; `handoff_lag_days` computed from actual, not expected, close.
- **Multi-asset deal split.** One deal spawns multiple properties (per `dp_one_deal_multiple_projects`). The workflow opens one handoff instance per property; parent deal record carries the union of completion statuses.
- **Vendor master not rationalized at close.** Handoff proceeds for operating handoffs while vendor rationalization remains `in_progress`; `vendor_rationalization_count` tracks. Sign-off allowed only if rationalization deferred via row 19 waiver.
- **Crosswalk row not created on time.** `crosswalk_row_creation_lag_days` breach triggers data-platform escalation; the workflow refuses final sign-off.
- **Lender notification missed.** `lender_reporting_registration` not acknowledged by covenant reporting start date. Routes to row 14 + reporting_finance_ops_lead.
- **Insurance gap during transition.** Seller policy ends before owner binder effective. Mid-handoff insurance binder gap triggers immediate row 17 escalation; operating handoff halts for any insurance-dependent checklist item.
- **PMA execution lag.** TPM assets where PMA is signed after close: the operating handoff may run in `partial_mode_behavior` but sign-off halts until PMA is executed.
- **Property-master-crosswalk row not merged.** If a proposed row conflicts with an existing canonical_id or the review is stalled, the item lands in `master_data/unresolved_exceptions_queue.md` with `reviewer: regional_ops_director`.
- **Re-trade at close.** Final purchase price adjusts at close; Intacct setup amounts re-reconciled before close is declared canonical.

## Example invocations

1. "Run the acquisition handoff for deal d_2026_acq_004 (Riverwood). Close was 2026-04-10."
2. "Status of the Ashford Park handoff — flag any items outside the lag band."
3. "Open the handoff sign-off packet for the asset_mgmt_director for deal d_2026_acq_007."

## Example outputs

### Output — Handoff checklist (abridged, Riverwood d_2026_acq_004)

**Handoff id.** `h_dp_int_to_af_setup_riverwood` (per `lifecycle_handoffs.md`).

**AppFolio property setup.** `complete`. `lifecycle_stage=stabilized`, unit_count reconciled to acquisition drawings. Owner: `regional_ops_director`.

**Intacct entity dim.** `complete`. `legal_entity_id=ENT_RIVERWOOD_LLC`. Project dim created. Owner: `finance_systems_team`.

**Vendor master rationalization.** `in_progress`. 3 of 5 inherited vendors resolved; 2 pending identity resolution (`master_data/identity_resolution_framework.md` section 7.3). `vendor_rationalization_count=3`.

**Opening rent roll.** `complete`. Variance within band per `reconciliation_tolerance_band.yaml`. `opening_rent_roll_reconciliation_variance=0.4%`.

**PMA execution (TPM).** `complete`. Executed 2026-04-08; `pma_execution_lag_days=-2` (pre-close).

**Lender reporting registration.** `complete`. Acknowledgment received 2026-04-12. Row 14 approval on file.

**Data-platform crosswalk rows.** `in_progress`. `property_master_crosswalk` row draft pending review by `regional_ops_director`. `crosswalk_row_creation_lag_days=4`.

**Handoff completeness score.** 82% (proposed metric).

**Open blockers.** Vendor identity resolution for 2 rows; crosswalk row review.

**ApprovalRequest.** Terminal sign-off packet assembled; routed to `asset_mgmt_director` via `workflows/owner_approval_routing`.

**Confidence banner.** `property_master_crosswalk@2026-03-31 (sample)`; `source_of_truth_matrix@wave_4_authoritative`; `reconciliation_tolerance_band@2026-03-31 (starter)`; `dealpath_deal_pipeline@wave_4 (stub)`.
