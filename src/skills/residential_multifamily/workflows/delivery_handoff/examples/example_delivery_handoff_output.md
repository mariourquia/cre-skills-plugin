# Example — Delivery Handoff Output (abridged)

**Prompt:** "Run the delivery handoff for dev_project dev_chs_010_gu_2024 (Greystone Commons). Temp CO received 2026-04-02; first 24 of 72 units cleared for lease."

**Handoff (per `lifecycle_handoffs.md`):** Handoff 8 (Procore -> AppFolio at delivery)
**Trigger:** `schedule_milestone.temp_co_received` AND `units_ready_for_lease=24 (>= 1)`
**Dev project id:** `dev_chs_010_gu_2024`
**Construction project id:** `cp_greystone_phase1`
**Property id (promoted from pre_takeover):** `prop_greystone_commons`
**Temp CO date:** 2026-04-02
**Final CO target:** 2026-04-30
**As-of date:** 2026-04-15

## Axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- lifecycle_stage: transitioning from `construction` to `lease_up`
- management_mode: self_managed
- market: Charlotte
- org_id: {org}
- role: development_manager

## Delivery handoff checklist

| # | Workstream | Owner | Status | Lag days | Tolerance band check | Notes |
|---|---|---|---|---|---|---|
| 1 | TCO/CO recording (AppFolio) | regional_ops_director | complete | 1 | within band | temp CO recorded 2026-04-03; final CO target 2026-04-30 |
| 2 | Punchlist state review | construction_manager | in_progress | 13 | within band | `punchlist_closeout_rate=87%`; all p1/p2 closed on 24 TCO'd units |
| 3 | Retainage release schedule | reporting_finance_ops_lead | complete | 2 | within band | per-trade schedule on file; `retainage_release_lag_days=2` |
| 4 | Rent-roll transition to active (24 units) | regional_ops_director | complete | 3 | within band | `ap_lease_up_setup_complete` passed for 24 units; remaining 48 staged |
| 5 | Construction sub vendor archival | regional_ops_director | complete | 8 | within band | 9 subs archived in `vendor_master_crosswalk.yaml` |
| 6 | Operating service vendor onboarding | regional_ops_director | in_progress | 13 | within band | 7 of 11 onboarded; 4 pending identity resolution (section 7.3) |
| 7 | Warranty package handoff | development_lead + legal | complete | 5 | within band | GC + 12 manufacturer warranties captured; `warranty_package_completeness=100%` |
| 8 | As-built documentation acceptance | development_lead | complete | 7 | within band | drawings, specs, systems manuals, commissioning reports in registry; `as_built_doc_completeness=98%` |
| 9 | Capex project closeout in Intacct | reporting_finance_ops_lead | in_progress | 5 | within band | final ledger posted; contingency closeout pending row 11; `capex_closeout_lag_days=5` |
| 10 | dev_project_crosswalk.yaml closure | data_platform_team | in_progress | 3 | within band | `procore_project_id -> property_id` linkage drafted; `dev_project_crosswalk_closure_lag_days=3` |
| 11 | property_master_crosswalk.yaml transition | data_platform_team | in_progress | 3 | within band | draft row transitioning `lifecycle_stage` `pre_takeover` -> `lease_up` for TCO'd set |
| 12 | Lease-up pricing policy seeded | asset_manager | complete | 6 | within band | seeded via `workflows/market_rent_refresh`; row 13 approval on file |
| 13 | lease_up_first_period trigger payload | data_platform_team | ready_pending_signoff | n/a | n/a | gated on terminal sign-off |

## Scorecard

- `delivery_handoff_completeness_score` (proposed): **0.86** (weighted).
- `tco_to_first_unit_ready_days` (proposed): **3** days (within band per `reference/normalized/schemas/reconciliation_tolerance_band.yaml`).
- `cco_to_first_lease_days` (proposed): **n/a** (final CO pending; will compute on final CO recording).
- `punchlist_closeout_rate` (existing): **87%** (all p1/p2 on TCO'd 24 units closed).
- `retainage_release_lag_days` (proposed): **2** (within band).
- `warranty_package_completeness` (proposed): **100%**.
- `as_built_doc_completeness` (proposed): **98%**.
- `vendor_rationalization_count` (proposed): **16** (9 subs archived + 7 operating vendors onboarded).
- `capex_closeout_lag_days` (proposed): **5** (within band; contingency closeout row 11 pending).
- `dev_project_crosswalk_closure_lag_days` (proposed): **3** (within band).
- `lease_up_pace_post_delivery` (existing): **n/a until first-lease event** (will begin computing once `lease_up_first_period` starts).

## Open blockers

1. Operating vendor identity resolution for 4 rows (irrigation, turf care, pest, pool). Reviewer: regional_ops_director per `identity_resolution_framework.md` section 7.3.
2. `property_master_crosswalk` + `dev_project_crosswalk` reviewer approval pending. Reviewer: regional_ops_director.
3. Capex contingency closeout pending row 11 approval; `capex_project_crosswalk.yaml` closure row gated on this.
4. Final CO outstanding; partial-mode operation continues; 48 non-TCO'd units remain pre-lease.

## Gates potentially triggered

- row 4 (TCO before punchlist complete) — not triggered on the TCO'd 24 units; monitored on remaining 48 pending final CO.
- row 7 (handoff lag + terminal sign-off) — within band; sign-off packet routed.
- row 11 (major capex / CO closeout) — approval pending for contingency closeout.
- row 13 (lease-up pricing policy) — approval on file.
- row 17 (warranty package acceptance / missing approver / insurance gap) — warranty acceptance approval on file; no gap.
- row 19 (vendor agreement signatures) — inherited from acquisition_handoff pattern; operating vendors flagged for row 19 where agreement size warrants.

## ApprovalRequest — terminal sign-off

- `approval_request_id`: ar_delivery_handoff_dev_chs_010_gu_2024
- Row: 7 (handoff completion sign-off routed as row 7 per overlay policy)
- Approver: development_lead
- Packet: checklist, scorecard, blocker memo, proposed crosswalk rows, lease_up_first_period trigger payload
- Status: pending_approver_review
- Routed via: `workflows/owner_approval_routing`

## Downstream workflow activation

On terminal sign-off:
- `workflows/lease_up_first_period` triggered for `prop_greystone_commons` (24 units).
- `property_master_crosswalk` row merged (`lifecycle_stage=lease_up`).
- `dev_project_crosswalk` row closed with `procore_project_id -> property_id` linkage.
- Operating service vendor crosswalk rows merged post identity-resolution close.
- Final phase of delivery (remaining 48 units) reopens this workflow instance on final CO; `partial_delivery` state carries forward until fully delivered.

## Confidence banner

```
References:
- lifecycle_handoffs.md@wave_4_authoritative
- source_of_truth_matrix.md@wave_4_authoritative
- stack_reconciliation_matrix.md@wave_4_authoritative
- procore_construction/dq_rules.yaml@2026-04-15 (stub)
- appfolio_pms/dq_rules.yaml@2026-04-15 (stub)
- dev_project_crosswalk.yaml@2026-03-31 (sample)
- capex_project_crosswalk.yaml@2026-03-31 (sample)
- property_master_crosswalk.yaml@2026-03-31 (sample)
- vendor_master_crosswalk.yaml@2026-03-31 (sample)
- reconciliation_tolerance_band.yaml@2026-03-31 (starter)
- approval_threshold_defaults.csv@2026-03-31 (starter)
- punchlist_sla__middle_market.csv@2026-03-31 (starter)
Blocking rules cited: recon_pc_to_af_at_delivery (not fired),
ap_lease_up_setup_complete (passed on TCO'd set), pc_to_af_handoff (passed).
Partial delivery: 24 of 72 units handed off; final CO pending for remaining 48.
Note: data-platform crosswalk writes are proposed-then-approve; no crosswalk
rows merged to canonical until `development_lead` sign-off completes.
```
