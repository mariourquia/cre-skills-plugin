---
name: Post-IC Property Setup
slug: post_ic_property_setup
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Pre-close placeholder conventions (property_id reservation scheme, legal-entity
  naming prefixes, and pre-acquisition tax/insurance policies) live in org overlays
  and drift. The gap between IC approval and deal close varies by deal; lag bands
  are overlay-tunable. Pre-close binder minimum terms and formation-state policies
  live in `overlays/org/_defaults/` and are refreshed by counsel.
applies_to:
  segment: [middle_market, luxury]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise, high_rise]
  lifecycle: [pre_acquisition]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [data_platform_team, regional_ops_director, asset_manager, reporting_finance_ops_lead, portfolio_manager]
  output_types: [handoff_checklist, kpi_review, memo]
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
    - reference/connectors/master_data/identity_resolution_framework.md
    - reference/connectors/master_data/crosswalk.schema.yaml
    - reference/normalized/schemas/reconciliation_tolerance_band.yaml
    - reference/normalized/approval_threshold_defaults.csv
    - reference/normalized/insurance_program__portfolio.csv
  writes:
    - reference/connectors/master_data/property_master_crosswalk.yaml
    - reference/connectors/master_data/asset_crosswalk.yaml
    - reference/connectors/master_data/unresolved_exceptions_queue.md
metrics_used:
  - pre_close_setup_completeness_score   # proposed: true
  - placeholder_crosswalk_creation_lag_days  # proposed: true
  - pre_close_insurance_binder_lead_days # proposed: true
  - legal_entity_formation_lag_days      # proposed: true
  - tax_lot_research_completion_rate     # proposed: true
  - handoff_baton_readiness_score        # proposed: true
escalation_paths:
  - kind: handoff_lag
    to: data_platform_team -> regional_ops_director -> approval_request(row 7)
  - kind: missing_required_approver
    to: deal_team_lead -> approval_request(row 17)
  - kind: doc_package_incomplete
    to: reporting_finance_ops_lead -> asset_mgmt_director
  - kind: legal_entity_formation_delay
    to: deal_team_lead + legal counsel -> approval_request(row 17)
  - kind: insurance_binder_gap
    to: deal_team_lead + asset_mgmt_director -> approval_request(row 17)
approvals_required:
  - deal_team_lead_pre_close_signoff
  - legal_entity_formation_engagement
  - pre_acquisition_insurance_binder
description: |
  Pre-close shadow setup. Fires at IC approval (Handoff 1 in
  reference/connectors/_core/stack_wave4/lifecycle_handoffs.md) before the deal
  actually closes. Creates placeholder property in AppFolio (status:
  pre_acquisition), placeholder entity dim in Intacct, placeholder
  property_master_crosswalk + asset_crosswalk rows, reserves the canonical
  property_id slot, routes to compliance for legal-entity formation, secures
  tax-lot and assessment research, and binds pre-acquisition insurance.
  Terminates by passing a baton payload to acquisition_handoff at close. The
  workflow never promotes the placeholder to operating; that is acquisition_handoff's
  job. Writes proposed placeholder rows to master_data via approval-gated writes.
---

# Post-IC Property Setup

## Workflow purpose

Between IC approval and deal close, pre-wire the operating and data-platform stack
so that the close-day handoff is a promotion rather than a cold start. The
workflow reserves identifiers, drafts placeholder rows, engages outside parties
(formation counsel, pre-close insurance carrier, tax-research provider), and
tracks readiness against the tolerance band. On close, it packages a
baton-pass payload for `workflows/acquisition_handoff` with every placeholder
id, crosswalk draft status, approval status, and known outstanding issue.

## Trigger conditions

- **Explicit:** "open pre-close setup for {deal}", "post-IC setup status", "reserve property_id for {deal}", "pre-close readiness for {property}".
- **Implicit:** Dealpath `deal.stage` transitions to `ic_approved` for an acquisition deal type (Handoff 1 in `reference/connectors/_core/stack_wave4/lifecycle_handoffs.md`). `deal_close_date_actual` must be null (post-IC but pre-close); if already non-null the workflow refuses and routes to `workflows/acquisition_handoff`.
- **Recurring:** none. Strictly event-driven from the IC approval trigger.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Dealpath deal record (IC-approved, pre-close) | record | required | must include `deal_id`, `asset_id`, `ic_approval_date`, `ic_approved_amount`, `deal_team_lead`, `expected_close_date`, `target_property_count`, `market`, `submarket`, `segment`, `form_factor`, `lifecycle_stage_target`, `management_mode` |
| Canonical `deal`, `asset` placeholders | records | required | seeded by Dealpath adapter at IC approval |
| IC approval record | record | required | the IC `approval_request` row, per `source_of_truth_matrix.md` |
| Proposed property_name, address | payload | required | may be subject to re-trade or assignment change pre-close; the workflow accepts updates |
| Proposed legal entity structure | record | required | entity type, formation state, governing docs status |
| Tax-lot research intent | record | required | parcel ids, assessor packets, known appeals status |
| Pre-acquisition insurance binder plan | record | required | carrier, policy type, effective/expiry dates, deposit status |
| Handoff-lag tolerance band | yaml | required | from `reference/normalized/schemas/reconciliation_tolerance_band.yaml` |
| Approver roster | yaml | required | resolved per org overlay |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Pre-close setup checklist | `handoff_checklist` | per-item status (`complete`, `in_progress`, `blocked`, `waived_with_approval`) with owner, due-date, tolerance-band check |
| Readiness scorecard | `kpi_review` | `pre_close_setup_completeness_score` (proposed) + per-workstream completion % + lag days |
| Placeholder crosswalk drafts | record | proposed `property_master_crosswalk.yaml` row (status: `pre_acquisition`), `asset_crosswalk.yaml` row |
| AppFolio placeholder property payload | record | `lifecycle_stage=pre_acquisition`, reserved `property_id`, address, market, submarket |
| Intacct placeholder entity payload | record | reserved `legal_entity_id`, project/property dim draft |
| Baton-pass payload | record | consumed by `workflows/acquisition_handoff` at close |
| ApprovalRequest: deal_team_lead sign-off | record | row 17 pre-close gate |
| Unresolved exception list | `checklist` | items routed to `master_data/unresolved_exceptions_queue.md` |

## Required context

`asset_class`, `segment`, `form_factor`, `lifecycle_stage` (always `pre_acquisition`), `management_mode`, `market`, `deal_id`, `org_id`. `jurisdiction` required for legal-entity formation. `expected_close_date` required to compute lag bands.

## Process

1. **Receive IC approval event.** Consume the Dealpath IC-approved trigger (Handoff 1 in `lifecycle_handoffs.md`). Confirm `deal.stage = ic_approved` and `deal_close_date_actual` is null. If `deal_close_date_actual` is already non-null, refuse and route to `workflows/acquisition_handoff`.
2. **Load baseline.** Pull canonical placeholder `deal`, `asset`, and the IC `approval_request` record. Per `source_of_truth_matrix.md`, Dealpath is primary for `deal` and `asset` in the pre-close window.
3. **Reserve property_id.** Allocate a canonical `property_id` from the org's reservation scheme; record as reserved-pending-close.
4. **AppFolio placeholder property.** Draft the AppFolio payload with `lifecycle_stage=pre_acquisition`, `status=pre_setup`, populated address, market, submarket, segment, form_factor. Unit-level records remain empty until close. Per `source_of_truth_matrix.md`, AppFolio is primary for `property` once it exists; at this stage it is a placeholder.
5. **Intacct placeholder legal entity dim.** Draft the Intacct entity dimension structure with reserved `legal_entity_id`. Per `source_of_truth_matrix.md` row `property`: secondary = intacct for `legal_entity_id`.
6. **Legal-entity formation routing.** Engage counsel for the entity formation in the target jurisdiction. Track `legal_entity_formation_lag_days` (proposed) from IC approval. Formation delay risks breaking the close date; surface via row 17 if beyond band.
7. **Tax-lot and assessment research.** Open a tax-lot research packet per parcel id. Track `tax_lot_research_completion_rate` (proposed). Known appeals or re-assessment activity flagged for asset_manager review.
8. **Pre-acquisition insurance binder.** Bind pre-close insurance with carrier per `reference/normalized/insurance_program__portfolio.csv` minimum terms. Record `pre_close_insurance_binder_lead_days` (proposed). Binder must be in force by close date minus overlay-defined lead.
9. **Placeholder crosswalk drafts.** Propose `property_master_crosswalk.yaml` row (status: `pre_acquisition`, canonical_id reserved) and `asset_crosswalk.yaml` row per `master_data/crosswalk.schema.yaml`. Proposed rows go to a staging area gated by `workflows/owner_approval_routing` before merge; see `survivorship_rules.md`.
10. **Readiness screen.** Compute `placeholder_crosswalk_creation_lag_days` (proposed), `pre_close_setup_completeness_score` (proposed), and per-workstream lag. Any workstream exceeding the tolerance band triggers row 7.
11. **Baton-pass payload assembly.** Compose the payload that `workflows/acquisition_handoff` will consume on close: reserved property_id, placeholder legal_entity_id, placeholder crosswalk ids, all approval statuses, all known issues.
12. **Deal-team-lead sign-off.** Route the pre-close packet via `workflows/owner_approval_routing` row 17 for deal_team_lead sign-off. Sign-off is a condition of the baton-pass being marked `ready`.
13. **Close-date watch.** If `expected_close_date` is less than overlay-defined lead (typically T-10 business days) and readiness score is below threshold, escalate to asset_mgmt_director.
14. **Confidence banner.** Surface `as_of_date` and `status` tags for every reference file and crosswalk referenced; cite the `lifecycle_handoffs.md` handoff id (`h_dp_to_approved_...`).

## Metrics used

- `pre_close_setup_completeness_score` (**proposed: true**) — weighted completion of the pre-close setup checklist; `grain=deal`, `time_basis=as_of_date`.
- `placeholder_crosswalk_creation_lag_days` (**proposed: true**) — days between IC approval and placeholder-crosswalk row approval; `grain=deal`, `time_basis=event_stamped`.
- `pre_close_insurance_binder_lead_days` (**proposed: true**) — days between binder-in-force date and expected close; `grain=deal`, unit=days.
- `legal_entity_formation_lag_days` (**proposed: true**) — days between IC approval and entity formation effective date; `grain=deal`.
- `tax_lot_research_completion_rate` (**proposed: true**) — share of tax-lot research packets closed pre-close; `grain=deal`, unit=percent.
- `handoff_baton_readiness_score` (**proposed: true**) — composite of sign-off status + crosswalk-draft status + insurance-binder status that governs handoff readiness at close; `grain=deal`, unit=percent.

Proposed metrics will be lifted into `_core/metrics.md` in a dedicated change-log entry before the workflow is promoted beyond draft.

## Reference files used

- `reference/connectors/_core/stack_wave4/lifecycle_handoffs.md` — handoff definitions (Handoff 1).
- `reference/connectors/_core/stack_wave4/source_of_truth_matrix.md` — primacy and effective-dating rules for `deal`, `asset`, `property`.
- `reference/connectors/adapters/dealpath_deal_pipeline/manifest.yaml` and `dq_rules.yaml` — source shape; blocking rule `dp_handoff_lag` cited; `dp_completeness_ic_record` cited.
- `reference/connectors/adapters/appfolio_pms/manifest.yaml` — PMS primary for `property` once operating.
- `reference/connectors/adapters/sage_intacct_gl/manifest.yaml` — GL primary for `legal_entity_id`, entity dims.
- `reference/connectors/master_data/property_master_crosswalk.yaml`, `asset_crosswalk.yaml` — crosswalks the workflow proposes placeholder rows for.
- `reference/connectors/master_data/identity_resolution_framework.md` and `crosswalk.schema.yaml` — identity and schema policy.
- `reference/normalized/schemas/reconciliation_tolerance_band.yaml` — lag thresholds and readiness bands.
- `reference/normalized/approval_threshold_defaults.csv` — approval thresholds (rows 7, 17, 19 per approval matrix).
- `reference/normalized/insurance_program__portfolio.csv` — minimum binder terms and carrier panel.

## Escalation points

- **Handoff lag.** Any workstream exceeding the pre-close lag band routes to `data_platform_team -> regional_ops_director -> approval_request` row 7.
- **Missing required approver.** If the deal_team_lead sign-off cannot be routed, escalates per row 17.
- **Legal-entity formation delay.** Formation lag beyond overlay band routes to deal_team_lead + legal counsel per row 17.
- **Insurance binder gap.** Binder lead below overlay band routes to deal_team_lead + asset_mgmt_director per row 17.
- **Doc package incomplete.** Pre-close docs (formation package, tax-lot research, binder) below completeness threshold routes to `reporting_finance_ops_lead`.

## Required approvals

- `deal_team_lead_pre_close_signoff` — row 17 (policy-overlay-marked action). Terminal pre-close gate; required to mark the baton-pass payload `ready`.
- `legal_entity_formation_engagement` — row 19 (contract binding the owner, counsel engagement).
- `pre_acquisition_insurance_binder` — row 17 (policy-overlay-marked action for binder binding pre-close).
- Crosswalk row additions (placeholder rows) to master_data: routed via `workflows/owner_approval_routing` per `survivorship_rules.md`.

## Failure modes

1. **Premature promotion.** Placeholder flipped to operating `lifecycle_stage` before close. Fix: workflow refuses promotion; that is `acquisition_handoff`'s job.
2. **Missing IC record.** IC approval record not present. Fix: `dp_completeness_ic_record` dq rule gates the workflow; refuse without it.
3. **property_id collision.** Reserved `property_id` already in use. Fix: reservation via org scheme; workflow refuses on collision.
4. **Legal-entity formation silently delayed.** Counsel engagement opened but not tracked. Fix: `legal_entity_formation_lag_days` is a mandatory checklist item.
5. **Binder gap at close.** Binder expires before owner permanent policy binds. Fix: lead-day band enforced; row 17 escalation.
6. **Baton-pass marked ready without sign-off.** Fix: sign-off gate is structural; baton is not `ready` without the approval record.
7. **Placeholder crosswalk merged to canonical before close.** Fix: staging-area + survivorship enforcement; canonical merge is a close-time handoff, not a pre-close event.
8. **Close date moves and nobody re-checks the lag bands.** Fix: close-date watch step fires on any `expected_close_date` change.
9. **Multi-asset deal not split at placeholder stage.** Fix: `dp_one_deal_multiple_projects` check required; one placeholder instance per target property.

## Edge cases

- **Late deal close.** `expected_close_date` slips. Lag bands recomputed; insurance binder term extended if required; tax-lot research re-validated if stale.
- **Multi-asset deal split.** One deal spawns multiple properties. The workflow opens one pre-close setup instance per target property; parent deal carries union status.
- **Dev TCO before punch list complete.** Not applicable to acquisition; refer to `workflows/delivery_handoff` for development path.
- **Partial delivery.** Not applicable (delivery is a development concept).
- **Vendor master not rationalized.** Vendor rationalization is an `acquisition_handoff` concern; the pre-close workflow only stages reserved vendor relationships for later resolution.
- **Crosswalk row not created on time.** `placeholder_crosswalk_creation_lag_days` breach triggers data-platform escalation; the baton is not `ready` until approved.
- **Lender notification missed.** Lender registration is an `acquisition_handoff` step; the pre-close workflow only confirms the lender relationship is queued for that hand-off.
- **Insurance gap during transition.** Seller policy end vs. owner binder effective is checked pre-close; any gap is pre-routed to legal + asset_mgmt_director.
- **PMA execution lag.** PMA execution is not a pre-close gate (PMA binds at close). The workflow only verifies a draft PMA is on file if `management_mode=third_party_managed`.
- **Deal termination pre-close.** If the deal terminates pre-close, the workflow calls the unwinder: reserved `property_id` released, placeholder crosswalk rows withdrawn, binder cancellation routed, engagement letters closed.
- **Re-trade at IC.** Re-trade triggers a refresh of placeholder address, unit count, and entity naming if relevant; lag clocks re-baseline at the amended IC approval.

## Example invocations

1. "Open pre-close setup for deal d_2026_acq_004 (Riverwood). IC approval was 2026-03-22; expected close 2026-04-10."
2. "Status of the Riverwood pre-close setup — flag any items outside the lag band."
3. "Build the pre-close sign-off packet for the deal team lead on d_2026_acq_007."

## Example outputs

### Output — Pre-close setup checklist (abridged, Riverwood d_2026_acq_004)

**Handoff id.** `h_dp_to_approved_2026Q1_acq_004` (per `lifecycle_handoffs.md`).

**property_id reservation.** `complete`. Reserved `prop_riverwood` pending close.

**AppFolio placeholder property.** `complete`. `lifecycle_stage=pre_acquisition`, address + market + submarket populated; unit records intentionally empty.

**Intacct placeholder entity dim.** `in_progress`. `legal_entity_id=ENT_RIVERWOOD_LLC` reserved; project dim drafted; Intacct dim creation pending counsel formation certificate.

**Legal-entity formation.** `in_progress`. Counsel engaged 2026-03-25; target effective date 2026-04-03; `legal_entity_formation_lag_days=12` (within band).

**Tax-lot research.** `complete`. Three parcels researched; one parcel has open appeal flagged for asset_manager review.

**Pre-acquisition insurance binder.** `complete`. Bound 2026-04-01, effective 2026-04-10; `pre_close_insurance_binder_lead_days=9`.

**Placeholder crosswalk rows.** `in_progress`. `property_master_crosswalk` row draft pending review; `asset_crosswalk` row draft pending review; `placeholder_crosswalk_creation_lag_days=6`.

**Baton-pass payload.** `ready_pending_signoff`.

**Readiness scorecard.** `pre_close_setup_completeness_score=0.83` (proposed).

**ApprovalRequest.** Pre-close sign-off packet routed to `deal_team_lead` via `workflows/owner_approval_routing` row 17.

**Confidence banner.** `property_master_crosswalk@2026-03-31 (sample)`; `asset_crosswalk@2026-03-31 (sample)`; `lifecycle_handoffs.md@wave_4_authoritative`; `source_of_truth_matrix@wave_4_authoritative`; `reconciliation_tolerance_band@2026-03-31 (starter)`; `dealpath_deal_pipeline@wave_4 (stub)`. Blocking rules cited: `dp_handoff_lag`, `dp_one_deal_multiple_projects` (neither fired).
