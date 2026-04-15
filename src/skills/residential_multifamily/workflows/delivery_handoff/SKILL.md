---
name: Delivery Handoff
slug: delivery_handoff
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  TCO/CO policy, retainage release schedules, warranty package standards, vendor
  rationalization windows (construction subs vs operating service vendors), and
  punchlist SLA bands live in org and segment overlays. Handoff-lag thresholds
  drift. Construction tracker project closeout templates are segment-dependent.
  System as-built documentation completeness bands live in
  `overlays/org/_defaults/`.
applies_to:
  segment: [middle_market, luxury]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise, high_rise]
  lifecycle: [development, construction, lease_up]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [development_manager, asset_manager, regional_manager, portfolio_manager, reporting_finance_ops_lead, construction_manager]
  output_types: [handoff_checklist, kpi_review, memo]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/connectors/_core/stack_wave4/lifecycle_handoffs.md
    - reference/connectors/_core/stack_wave4/source_of_truth_matrix.md
    - reference/connectors/_core/stack_wave4/stack_reconciliation_matrix.md
    - reference/connectors/adapters/procore_construction/manifest.yaml
    - reference/connectors/adapters/procore_construction/dq_rules.yaml
    - reference/connectors/adapters/procore_construction/reconciliation_checks.yaml
    - reference/connectors/adapters/appfolio_pms/manifest.yaml
    - reference/connectors/adapters/appfolio_pms/dq_rules.yaml
    - reference/connectors/adapters/sage_intacct_gl/manifest.yaml
    - reference/connectors/adapters/dealpath_deal_pipeline/manifest.yaml
    - reference/connectors/master_data/property_master_crosswalk.yaml
    - reference/connectors/master_data/dev_project_crosswalk.yaml
    - reference/connectors/master_data/capex_project_crosswalk.yaml
    - reference/connectors/master_data/vendor_master_crosswalk.yaml
    - reference/connectors/master_data/identity_resolution_framework.md
    - reference/connectors/master_data/survivorship_rules.md
    - reference/normalized/schemas/reconciliation_tolerance_band.yaml
    - reference/normalized/approval_threshold_defaults.csv
    - reference/normalized/punchlist_sla__middle_market.csv
  writes:
    - reference/connectors/master_data/property_master_crosswalk.yaml
    - reference/connectors/master_data/dev_project_crosswalk.yaml
    - reference/connectors/master_data/capex_project_crosswalk.yaml
    - reference/connectors/master_data/vendor_master_crosswalk.yaml
    - reference/connectors/master_data/unresolved_exceptions_queue.md
metrics_used:
  - cco_to_first_lease_days              # proposed: true
  - tco_to_first_unit_ready_days         # proposed: true
  - delivery_handoff_completeness_score  # proposed: true
  - punchlist_closeout_rate              # existing (see _core/metrics.md)
  - retainage_release_lag_days           # proposed: true
  - warranty_package_completeness        # proposed: true
  - as_built_doc_completeness            # proposed: true
  - vendor_rationalization_count         # proposed: true (shared with acquisition_handoff)
  - capex_closeout_lag_days              # proposed: true
  - dev_project_crosswalk_closure_lag_days  # proposed: true
  - lease_up_pace_post_delivery          # existing (see _core/metrics.md)
escalation_paths:
  - kind: handoff_lag
    to: development_lead -> asset_mgmt_director -> approval_request(row 7)
  - kind: missing_required_approver
    to: development_lead -> approval_request(row 17)
  - kind: doc_package_incomplete
    to: reporting_finance_ops_lead -> asset_mgmt_director
  - kind: vendor_master_conflict
    to: regional_ops_director -> approval_request(row 19)
  - kind: warranty_package_incomplete
    to: development_lead + legal counsel -> approval_request(row 17)
  - kind: tco_before_punchlist_complete
    to: development_lead + construction_manager -> approval_request(row 4)
  - kind: capex_closeout_drift
    to: reporting_finance_ops_lead -> approval_request(row 11)
approvals_required:
  - development_lead_handoff_signoff
  - capex_project_closeout_in_intacct
  - warranty_package_acceptance
  - lease_up_pricing_policy_seeded
description: |
  Coordinates the transition from construction delivery to operating asset. Fires
  on Procore schedule_milestone `temp_co_received` or `final_co_received` (with
  units_ready_for_lease >= 1), or on AppFolio C/O recording (Handoff 8 in
  reference/connectors/_core/stack_wave4/lifecycle_handoffs.md). Drives TCO/CO
  recording, punchlist state review, retainage release schedule, rent-roll
  transition from lease-up plan to active, construction-sub vs operating-vendor
  rationalization, warranty package handoff, system as-built documentation
  acceptance, capex project closeout in Intacct, and dev_project_crosswalk
  closure (procore_project_id -> property_id linkage). Triggers
  lease_up_first_period once the AppFolio unit roster is active. Writes back
  to master_data crosswalks via approval. Handoff is not complete until every
  item lands within the tolerance band and development_lead signs off.
---

# Delivery Handoff

## Workflow purpose

Turn a Procore construction project at TCO/CO into an operating, leasable
asset with auditable handoff completion across AppFolio (operating),
Intacct (financial closeout), master data crosswalks (data platform), the
vendor master (construction subs out, operating service vendors in), and the
warranty + as-built documentation registry. The workflow does not execute
setup steps in vendor systems; it composes the handoff checklist, validates
each item's completion against the source-of-truth matrix, and routes gated
items through `workflows/owner_approval_routing`. Handoff is not complete
until every item is within the tolerance band on
`reconciliation_tolerance_band.yaml` and `development_lead` has signed off.
On completion, `workflows/lease_up_first_period` is triggered to pick up
the first operating period for the newly-active property.

## Trigger conditions

- **Explicit:** "delivery handoff for {project}", "open delivery handoff package for {property}", "close the delivery handoff for {dev_project}", "handoff status for {project}".
- **Implicit:** Procore `schedule_milestone` fires `temp_co_received` or `final_co_received` AND `units_ready_for_lease >= 1` (Handoff 8 in `reference/connectors/_core/stack_wave4/lifecycle_handoffs.md`). Alternatively, AppFolio records a C/O for a property currently at `lifecycle_stage=pre_takeover` or `construction`. Either trigger activates the same workflow instance.
- **Recurring:** none. Strictly event-driven.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Procore project record (at or past TCO) | record | required | must include `construction_project_id`, `dev_project_id` (parent), `schedule_milestone (temp_co_received or final_co_received)`, `punchlist_items[]`, `closeout_documents[]`, `retainage_release_schedule`, `warranty_package_ref`, `as_built_package_ref` |
| Canonical `development_project`, `construction_project`, `capex_project` objects | records | required | per `source_of_truth_matrix.md`: procore primary for `construction_project`; dealpath seeded `development_project` |
| AppFolio property record (at `pre_takeover` or equivalent) | record | required | reserved `property_id` from earlier `post_ic_property_setup` (if applicable) or dev-specific setup |
| Unit roster (as-built) | table | required | must match construction drawings exactly; unit_count_total, unit_count_rentable, nrsf_total populated per unit |
| Lease-up pricing policy draft | record | required | pricing policy + concession band for opening lease-up; ties into `workflows/market_rent_refresh` |
| Retainage release schedule | record | required | trade, amount held, release trigger, target release date |
| Warranty package | package | required | GC warranty, manufacturer warranties, effective dates, start-date triggers |
| As-built documentation package | package | required | drawings, specifications, systems manuals, commissioning reports |
| Construction sub vendor list | list | required | subs to be archived / flagged as non-operating |
| Operating service vendor list | list | required | new operating vendors to be onboarded (turf, pest, pool, waste, HVAC service, etc.) |
| Capex closeout package | package | required | final cost ledger, change-order summary, retainage status, contingency closeout |
| Handoff-lag tolerance band | yaml | required | from `reference/normalized/schemas/reconciliation_tolerance_band.yaml` |
| Approver roster | yaml | required | resolved per org overlay |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Delivery handoff checklist | `handoff_checklist` | per-item status (`complete`, `in_progress`, `blocked`, `waived_with_approval`) with owner, due-date, tolerance-band check |
| Delivery completeness scorecard | `kpi_review` | `delivery_handoff_completeness_score` (proposed) + per-workstream completion % + lag days |
| Blocker memo | `memo` | narrative with cited blocker ids and source-of-truth matrix references |
| Crosswalk row draft / closure | record | proposed `property_master_crosswalk.yaml` transition (pre_takeover -> lease_up), `dev_project_crosswalk.yaml` closure (procore_project_id -> property_id linkage), `capex_project_crosswalk.yaml` closeout, `vendor_master_crosswalk.yaml` additions/retirements |
| ApprovalRequest: handoff sign-off | record | row 7 if lag exceeds band; otherwise a terminal sign-off |
| Unresolved exception list | `checklist` | items routed to `master_data/unresolved_exceptions_queue.md` |
| lease_up_first_period trigger payload | record | event payload consumed by `workflows/lease_up_first_period` on completion |

## Required context

`asset_class`, `segment`, `form_factor`, `lifecycle_stage` (`development` or `construction` at trigger, transitioning to `lease_up`), `management_mode`, `market`, `property_id`, `construction_project_id`, `dev_project_id`, `org_id`. `jurisdiction` required for C/O recording and any permitting signoffs.

## Process

1. **Receive delivery trigger.** Consume the Procore TCO/CO milestone (`temp_co_received` or `final_co_received` with `units_ready_for_lease >= 1`) per Handoff 8 in `lifecycle_handoffs.md`. Alternatively consume the AppFolio C/O record for the property. If both arrive, reconcile via `stack_reconciliation_matrix.md::recon_pc_to_af_at_delivery`. If neither trigger is valid, refuse.
2. **Load baseline.** Pull canonical `development_project`, `construction_project`, `capex_project`, placeholder `property`, and the unit roster drafted from construction drawings. Per `source_of_truth_matrix.md`, Procore is primary for `construction_project` and `schedule_milestone`; AppFolio is primary for `property` once operating.
3. **TCO/CO recording.** Verify the certificate of occupancy has been received and recorded in AppFolio. If only temp CO is in hand, classify the handoff as `partial_delivery` and run in `partial_mode_behavior` until final CO recorded.
4. **Punchlist state review.** Read the Procore punchlist; compute `punchlist_closeout_rate` (existing; see `_core/metrics.md`). Outstanding p1/p2 punchlist items block operating handoff for units with those items; cite `punchlist_sla__middle_market.csv` for SLA band.
5. **Retainage release schedule.** Confirm the retainage release plan per trade, target release date, and trigger condition. Compute `retainage_release_lag_days` (proposed). Outside-band items flagged for reporting_finance_ops_lead.
6. **Rent-roll transition.** Move the AppFolio unit roster from the lease-up plan (hypothetical units per development) to active (real units available for lease). Unit count must match construction drawings exactly per `appfolio_pms.dq_rules.yaml::ap_lease_up_setup_complete`. Mismatch is a `blocker`.
7. **Vendor rationalization (construction subs vs operating service vendors).** For each construction sub: confirm archived / flagged as non-operating in `vendor_master_crosswalk.yaml`. For each new operating vendor: run identity resolution per `master_data/identity_resolution_framework.md`; emit proposed additions or merges. Count goes to `vendor_rationalization_count` (proposed, shared with `acquisition_handoff`).
8. **Warranty package handoff.** Read the warranty package; confirm GC warranty start date + manufacturer warranties + effective windows are all captured. Track `warranty_package_completeness` (proposed). Missing warranty items escalate via row 17.
9. **System as-built documentation.** Confirm drawings, specifications, systems manuals, commissioning reports are in the docs registry. Track `as_built_doc_completeness` (proposed). Incomplete packages escalate via `reporting_finance_ops_lead`.
10. **Capex project closeout in Intacct.** Verify final cost ledger, change-order summary, retainage status, and contingency closeout are posted in Intacct per `source_of_truth_matrix.md` row `capex_project`: procore for scope/commitments; intacct for posted spend. Track `capex_closeout_lag_days` (proposed). Row 11 approval required for major capex closeout.
11. **dev_project_crosswalk closure.** Close the `dev_project_crosswalk.yaml` row by linking `procore_project_id -> property_id`; per `survivorship_rules.md::dev_project_default`. Track `dev_project_crosswalk_closure_lag_days` (proposed).
12. **property_master_crosswalk transition.** Propose the `lifecycle_stage` transition (`pre_takeover` or `construction` -> `lease_up`) in `property_master_crosswalk.yaml`. Proposed rows are staged and only merged after approval; see `survivorship_rules.md`.
13. **Lease-up pricing policy seeded.** Confirm the opening lease-up pricing policy has been seeded via `workflows/market_rent_refresh` or equivalent. Required approval gate before `lease_up_first_period` can run.
14. **Handoff-lag screen.** Compute `tco_to_first_unit_ready_days` (proposed), `cco_to_first_lease_days` (proposed), and per-workstream lag against `handoff_lag_threshold_days` from `reconciliation_tolerance_band.yaml`. Any breach routes to `workflows/owner_approval_routing` row 7.
15. **Completeness score.** Compose `delivery_handoff_completeness_score` (proposed) as weighted completion of the checklist (weights per overlay).
16. **Sign-off packet.** Assemble the development_lead sign-off packet with the checklist, scorecard, blocker memo, and crosswalk drafts. Route via `workflows/owner_approval_routing` row 7.
17. **Trigger `lease_up_first_period`.** On final sign-off, emit the event payload for `workflows/lease_up_first_period` to pick up the first operating period for the now-active property.
18. **Confidence banner.** Surface `as_of_date` and `status` tags for every reference file and crosswalk referenced; cite the `lifecycle_handoffs.md` handoff id for Handoff 8.

## Metrics used

- `cco_to_first_lease_days` (**proposed: true**) — days from final CO recording to first executed lease on the property; `grain=property`, unit=days, `time_basis=event_stamped`.
- `tco_to_first_unit_ready_days` (**proposed: true**) — days from temp CO to first unit marked ready-to-lease in AppFolio; `grain=property`, unit=days.
- `delivery_handoff_completeness_score` (**proposed: true**) — weighted completion of the delivery handoff checklist; `grain=property`, `time_basis=as_of_date`.
- `punchlist_closeout_rate` (existing; see `_core/metrics.md`) — percent of punchlist items closed at handoff; `grain=project`.
- `retainage_release_lag_days` (**proposed: true**) — days between release trigger met and actual release; `grain=project`, unit=days.
- `warranty_package_completeness` (**proposed: true**) — percent of required warranty docs on file; `grain=property`, unit=percent.
- `as_built_doc_completeness` (**proposed: true**) — percent of required as-built docs on file; `grain=property`, unit=percent.
- `vendor_rationalization_count` (**proposed: true**) — count of vendor master rows rationalized at delivery handoff (construction subs archived + operating vendors onboarded); `grain=property`.
- `capex_closeout_lag_days` (**proposed: true**) — days between final sign-off target and capex closeout posted in Intacct; `grain=project`, unit=days.
- `dev_project_crosswalk_closure_lag_days` (**proposed: true**) — days between delivery trigger and `dev_project_crosswalk.yaml` row closure; `grain=project`, unit=days.
- `lease_up_pace_post_delivery` (existing; see `_core/metrics.md`) — units leased per week after TCO; surfaced as the downstream handoff metric into `lease_up_first_period`.

Proposed metrics will be lifted into `_core/metrics.md` in a dedicated change-log entry before the workflow is promoted beyond draft.

## Reference files used

- `reference/connectors/_core/stack_wave4/lifecycle_handoffs.md` — handoff definitions (Handoff 8).
- `reference/connectors/_core/stack_wave4/source_of_truth_matrix.md` — primacy rules for `development_project`, `construction_project`, `capex_project`, `property`, `schedule_milestone`.
- `reference/connectors/_core/stack_wave4/stack_reconciliation_matrix.md` — `recon_pc_to_af_at_delivery` blocker-severity check.
- `reference/connectors/adapters/procore_construction/manifest.yaml`, `dq_rules.yaml`, `reconciliation_checks.yaml` — source shape; `pc_to_af_handoff` check cited.
- `reference/connectors/adapters/appfolio_pms/manifest.yaml`, `dq_rules.yaml` — `ap_lease_up_setup_complete` rule cited.
- `reference/connectors/adapters/sage_intacct_gl/manifest.yaml` — GL primary for capex posted spend and closeout.
- `reference/connectors/adapters/dealpath_deal_pipeline/manifest.yaml` — Dealpath governance signoffs for development project.
- `reference/connectors/master_data/property_master_crosswalk.yaml`, `dev_project_crosswalk.yaml`, `capex_project_crosswalk.yaml`, `vendor_master_crosswalk.yaml` — crosswalks the workflow proposes rows for / closes.
- `reference/connectors/master_data/identity_resolution_framework.md`, `survivorship_rules.md` — identity and survivorship policy (specifically `dev_project_default` and `capex_project_default`).
- `reference/normalized/schemas/reconciliation_tolerance_band.yaml` — handoff-lag bands.
- `reference/normalized/approval_threshold_defaults.csv` — approval thresholds (rows 4, 7, 11, 17, 19).
- `reference/normalized/punchlist_sla__middle_market.csv` — punchlist SLA band for p1/p2 items at delivery.

## Escalation points

- **Handoff lag.** Any workstream exceeding `handoff_lag_threshold_days` escalates to `development_lead -> asset_mgmt_director` and opens `approval_request` row 7.
- **Missing required approver.** If the development_lead sign-off cannot be routed (role vacant per approver roster), escalates per row 17.
- **Vendor master conflict.** Unresolved duplicate or survivorship conflict goes to `master_data/unresolved_exceptions_queue.md` and routes to row 19.
- **Warranty package incomplete.** Missing warranty documentation escalates to `development_lead + legal counsel` per row 17.
- **TCO before punchlist complete.** Temp CO received while p1/p2 punchlist items are open on units proposed for lease. Escalates to `development_lead + construction_manager` per row 4 (safety-critical maintenance decision). Workflow runs in `partial_mode_behavior`.
- **Capex closeout drift.** Major capex closeout posting lag in Intacct beyond band routes to `reporting_finance_ops_lead` per row 11 (change-order threshold class).
- **Doc package incomplete.** As-built package below completeness threshold routes to `reporting_finance_ops_lead`.

## Required approvals

- `development_lead_handoff_signoff` — terminal approval that marks delivery handoff complete. Required for every delivery. Row 7 policy.
- `capex_project_closeout_in_intacct` — row 11 (major CO / capex closeout) for the final capex posting in Intacct.
- `warranty_package_acceptance` — row 17 (policy-marked, legal review of warranty terms prior to acceptance).
- `lease_up_pricing_policy_seeded` — row 13 (pricing policy above / at policy) for the opening lease-up pricing structure.
- Crosswalk row transitions and closures (property_master, dev_project, capex_project, vendor_master): routed via `workflows/owner_approval_routing` per `survivorship_rules.md`.

## Failure modes

1. **Silent lifecycle_stage advance.** Property flipped to `lease_up` in AppFolio without Procore TCO/CO primacy confirmation. Fix: `recon_pc_to_af_at_delivery` is a blocker-severity check; workflow halts on mismatch.
2. **Unit roster mismatch.** AppFolio unit roster differs from construction drawings. Fix: `ap_lease_up_setup_complete` dq rule gates; refuse until reconciled.
3. **Punchlist ignored.** Operating handoff marked complete while p1/p2 items open on proposed-lease units. Fix: workflow refuses unit-by-unit handoff for affected units; escalates via row 4.
4. **Warranty package incomplete.** Delivery marked complete without warranty coverage in docs registry. Fix: conditional required input; `warranty_package_acceptance` approval gate.
5. **Capex closeout drift.** Capex project closed in Procore but not posted in Intacct. Fix: `capex_closeout_lag_days` tracked; row 11 approval required.
6. **dev_project_crosswalk left open.** Row never closes; procore_project_id and property_id never linked in canonical crosswalk. Fix: closure is a mandatory checklist item.
7. **Construction subs not archived.** Construction subs remain active in operating vendor master. Fix: vendor rationalization step is required; `vendor_master_conflict` escalation.
8. **Operating vendors not onboarded.** Handoff complete but no operating service vendors on file. Fix: operating vendor list is a required input; gap surfaces in handoff checklist.
9. **Stale confidence banner.** `as_of_date` references older than the TCO/CO date without acknowledgement. Fix: banner required per overlay staleness rule.
10. **lease_up_first_period triggered prematurely.** Downstream workflow fires before sign-off completes. Fix: trigger is gated on terminal sign-off.

## Edge cases

- **Late deal close.** Not applicable (delivery is a development event, not an acquisition event). For acquisition path late close see `workflows/acquisition_handoff`.
- **Multi-asset deal split.** For development, one deal spawns one or more properties. The workflow opens one delivery-handoff instance per property delivered; parent `development_project` carries union status across siblings.
- **Dev TCO before punch list complete.** The workflow runs in `partial_mode_behavior`. TCO-proven units with no open p1/p2 items may be marked ready-to-lease; other units remain pre-lease until punchlist closed. `tco_to_first_unit_ready_days` computed on first-ready unit.
- **Partial delivery.** Phase-1 delivery ahead of phase-2: one delivery handoff per phase; `property_master_crosswalk` row updates `lifecycle_stage` only for the unit set delivered. `dev_project_crosswalk` closure deferred until final phase delivery unless `survivorship_rules.md::dev_project_phase_closure` allows per-phase close.
- **Vendor master not rationalized.** Delivery proceeds for operating rent-roll activation while vendor rationalization remains `in_progress`; `vendor_rationalization_count` tracks. Sign-off allowed only if rationalization deferred via row 19 waiver.
- **Crosswalk row not created on time.** `dev_project_crosswalk_closure_lag_days` breach triggers data-platform escalation; the workflow refuses final sign-off.
- **Lender notification missed.** Lender construction-to-permanent conversion is a distinct workflow; delivery handoff only emits the operating-property readiness signal. A missing lender conversion flag on the dev_project_crosswalk row routes to `reporting_finance_ops_lead`.
- **Insurance gap during transition.** Builder's risk policy ending vs. operating property policy effective date. Mid-handoff gap triggers immediate row 17 escalation; rent-roll activation halts for any insurance-dependent checklist item.
- **PMA execution lag.** Not applicable to delivery (PMA, if TPM, executed at acquisition or dev-deal activation).
- **property_master_crosswalk row not merged.** If a proposed transition row conflicts with an existing canonical_id or the review is stalled, the item lands in `master_data/unresolved_exceptions_queue.md` with `reviewer: regional_ops_director`.
- **Final CO delayed past temp CO by >band.** The workflow escalates via row 4; partial operating handoff may continue for already-TCO'd units.
- **Warranty start-date ambiguity.** If GC warranty and manufacturer warranties have different start-date triggers (e.g., substantial completion vs. individual-unit completion), escalate to legal per row 17.
- **Capex overrun at closeout.** Final posted spend > approved budget + contingency. Row 11 approval gate required before closeout can be marked complete.

## Example invocations

1. "Run the delivery handoff for dev_project dev_chs_010_gu_2024 (Greystone Commons). Temp CO received 2026-04-02."
2. "Status of the Greystone delivery handoff — flag any items outside the lag band."
3. "Open the handoff sign-off packet for the development_lead for project dev_chs_010_gu_2024."

## Example outputs

### Output — Delivery handoff checklist (abridged, Greystone Commons dev_chs_010_gu_2024)

**Handoff id.** Handoff 8 per `lifecycle_handoffs.md`.

**TCO/CO recording.** `complete`. Temp CO recorded 2026-04-02; final CO targeted 2026-04-30. Partial mode while final CO pending.

**Punchlist state.** `in_progress`. `punchlist_closeout_rate=87%`. All p1/p2 items closed on the first 24 units proposed for lease; other units carry minor cosmetic items.

**Retainage release schedule.** `complete`. Per-trade schedule on file; `retainage_release_lag_days=2` (within band).

**Rent-roll transition.** `complete`. AppFolio unit roster activated for the 24 TCO'd units; remaining 48 units staged. `ap_lease_up_setup_complete` check passed for the TCO'd set.

**Vendor rationalization.** `in_progress`. 9 construction subs archived; 7 of 11 operating vendors onboarded. `vendor_rationalization_count=16` (9 archived + 7 onboarded).

**Warranty package.** `complete`. GC warranty + 12 manufacturer warranties on file; all start dates captured. `warranty_package_completeness=100%`.

**As-built documentation.** `complete`. Drawings, specs, systems manuals, commissioning reports in registry. `as_built_doc_completeness=98%` (one minor spec pending).

**Capex closeout in Intacct.** `in_progress`. Final cost ledger posted; contingency closeout pending row 11 approval. `capex_closeout_lag_days=5`.

**dev_project_crosswalk closure.** `in_progress`. `procore_project_id -> property_id` linkage drafted; pending reviewer approval. `dev_project_crosswalk_closure_lag_days=3`.

**property_master_crosswalk transition.** `in_progress`. Draft row transitioning `lifecycle_stage` from `pre_takeover` to `lease_up` for the TCO'd unit set; pending approval.

**Lease-up pricing policy seeded.** `complete`. Seeded via `workflows/market_rent_refresh`; row 13 approval on file.

**Handoff completeness score.** `delivery_handoff_completeness_score=0.86`.

**Lag days.** `tco_to_first_unit_ready_days=3`; `cco_to_first_lease_days=n/a` (final CO pending).

**Open blockers.** Operating vendor identity resolution for 4 rows; `property_master_crosswalk` + `dev_project_crosswalk` reviewer approval; capex contingency closeout row 11.

**ApprovalRequest.** Terminal sign-off packet assembled; routed to `development_lead` via `workflows/owner_approval_routing` row 7.

**lease_up_first_period trigger.** Gated on terminal sign-off; payload staged.

**Confidence banner.** `dev_project_crosswalk@2026-03-31 (sample)`; `capex_project_crosswalk@2026-03-31 (sample)`; `property_master_crosswalk@2026-03-31 (sample)`; `vendor_master_crosswalk@2026-03-31 (sample)`; `source_of_truth_matrix@wave_4_authoritative`; `stack_reconciliation_matrix@wave_4_authoritative`; `reconciliation_tolerance_band@2026-03-31 (starter)`; `procore_construction@wave_4 (stub)`; `appfolio_pms@wave_4 (stub)`; `punchlist_sla__middle_market@2026-03-31 (starter)`. Blocking rules cited: `recon_pc_to_af_at_delivery`, `ap_lease_up_setup_complete`, `pc_to_af_handoff` (none fired as blocker; one confidence-reduced in partial-mode on final CO pending).
