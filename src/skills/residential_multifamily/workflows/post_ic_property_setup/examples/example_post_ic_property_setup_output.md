# Example — Post-IC Property Setup Output (abridged)

**Prompt:** "Open pre-close setup for deal d_2026_acq_004 (Riverwood). IC approval was 2026-03-22; expected close 2026-04-10."

**Handoff id (per `lifecycle_handoffs.md`):** `h_dp_to_approved_2026Q1_acq_004`
**Trigger (per `lifecycle_handoffs.md`):** Handoff 1 (IC-approved, pre-close window)
**Deal id:** `d_2026_acq_004`
**Canonical asset id:** `asset_riverwood_acq`
**Reserved canonical property id:** `prop_riverwood` (pending promotion at close)
**IC approval date:** 2026-03-22
**Expected close date:** 2026-04-10
**As-of date:** 2026-04-03

## Axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- lifecycle_stage: pre_acquisition
- management_mode: third_party_managed
- market: Charlotte
- org_id: {org}
- role: data_platform_team

## Pre-close setup checklist

| # | Workstream | Owner | Status | Lag days | Tolerance band check | Notes |
|---|---|---|---|---|---|---|
| 1 | property_id reservation | data_platform_team | complete | 0 | within band | reserved `prop_riverwood` pending close |
| 2 | AppFolio placeholder property (lifecycle_stage=pre_acquisition) | data_platform_team | complete | 2 | within band | address + market + submarket populated; unit records empty |
| 3 | Intacct placeholder entity dim | finance_systems_team | in_progress | 8 | within band | `legal_entity_id=ENT_RIVERWOOD_LLC` reserved; dim gated on counsel formation cert |
| 4 | Legal-entity formation (counsel engagement) | deal_team_lead + legal | in_progress | 12 | within band | engagement 2026-03-25; target effective 2026-04-03; `legal_entity_formation_lag_days=12` |
| 5 | Tax-lot and assessment research | asset_manager | complete | 5 | within band | 3 parcels closed; one parcel has open appeal flagged |
| 6 | Pre-acquisition insurance binder | asset_mgmt_director | complete | 10 | within band | bound 2026-04-01, effective 2026-04-10; `pre_close_insurance_binder_lead_days=9` |
| 7 | property_master_crosswalk placeholder row | data_platform_team | in_progress | 6 | within band | draft pending reviewer approval; `placeholder_crosswalk_creation_lag_days=6` |
| 8 | asset_crosswalk placeholder row | data_platform_team | in_progress | 6 | within band | draft pending reviewer approval |
| 9 | PMA draft on file (TPM) | asset_mgmt_director + legal | complete | 7 | n/a | draft filed; execution deferred to close (acquisition_handoff gate) |
| 10 | Baton-pass payload for acquisition_handoff | data_platform_team | ready_pending_signoff | n/a | n/a | payload assembled; signoff is the terminal gate |

## Scorecard

- `pre_close_setup_completeness_score` (proposed): **0.83** (weighted).
- `handoff_baton_readiness_score` (proposed): **0.90** (ready-pending-signoff).
- `placeholder_crosswalk_creation_lag_days` (proposed): **6** (within band).
- `pre_close_insurance_binder_lead_days` (proposed): **9** (within band, meets T-7 overlay lead).
- `legal_entity_formation_lag_days` (proposed): **12** (within band).
- `tax_lot_research_completion_rate` (proposed): **100%** (3 of 3 parcels).

## Open blockers

1. Intacct entity dim creation gated on counsel-delivered formation certificate (target 2026-04-03).
2. `property_master_crosswalk` + `asset_crosswalk` placeholder rows pending review by regional_ops_director.
3. One parcel with an open appeal flagged for asset_manager review pre-close.

## Gates potentially triggered

- row 7 (handoff lag) — not triggered; within band.
- row 17 (pre-close sign-off) — packet routed to deal_team_lead.
- row 17 (legal-entity formation delay) — not triggered; within band.
- row 17 (insurance binder gap) — not triggered; binder effective at close.
- row 19 (counsel engagement contract) — approval on file for formation engagement.

## ApprovalRequest — pre-close sign-off

- `approval_request_id`: ar_post_ic_d_2026_acq_004
- Row: 17 (policy-overlay-marked pre-close sign-off)
- Approver: deal_team_lead
- Packet: checklist, readiness scorecard, baton-pass payload, placeholder crosswalk drafts, formation status
- Status: pending_approver_review
- Routed via: `workflows/owner_approval_routing`

## Baton-pass handoff to `workflows/acquisition_handoff`

On close (`deal_close_date_actual` becomes non-null):
- Reserved `property_id=prop_riverwood` is consumed by acquisition_handoff.
- Placeholder `property_master_crosswalk` and `asset_crosswalk` rows are promoted to canonical per `survivorship_rules.md`.
- AppFolio `lifecycle_stage` transitions from `pre_acquisition` to `stabilized` (per Handoff 3).
- Intacct entity dim is finalized with counsel-delivered formation cert.
- PMA is executed (if TPM); lender registration initiated.

## Confidence banner

```
References:
- lifecycle_handoffs.md@wave_4_authoritative
- source_of_truth_matrix.md@wave_4_authoritative
- dealpath_deal_pipeline/dq_rules.yaml@2026-04-15 (stub)
- property_master_crosswalk.yaml@2026-03-31 (sample)
- asset_crosswalk.yaml@2026-03-31 (sample)
- reconciliation_tolerance_band.yaml@2026-03-31 (starter)
- approval_threshold_defaults.csv@2026-03-31 (starter)
- insurance_program__portfolio.csv@2026-02-28 (starter)
Blocking rules cited: dp_completeness_ic_record, dp_handoff_lag,
dp_one_deal_multiple_projects (none fired).
Note: placeholder crosswalk writes are proposed-then-approve; no rows merged to
canonical until deal close and acquisition_handoff promotes them.
```
