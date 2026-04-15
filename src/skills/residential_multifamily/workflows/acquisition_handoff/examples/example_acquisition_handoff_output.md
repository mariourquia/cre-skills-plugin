# Example — Acquisition Handoff Output (abridged)

**Prompt:** "Run the acquisition handoff for deal d_2026_acq_004 (Riverwood). Close was 2026-04-10."

**Handoff id (per `lifecycle_handoffs.md`):** `h_dp_int_to_af_setup_riverwood`
**Trigger (per `lifecycle_handoffs.md`):** Handoff 1 + Handoff 3 (close complete)
**Deal id:** `d_2026_acq_004`
**Canonical asset id:** `asset_riverwood_acq`
**Canonical property id (promoted from placeholder):** `prop_riverwood`
**Close date:** 2026-04-10
**As-of date:** 2026-04-15

## Axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- lifecycle_stage: stabilized (transition from `pre_acquisition`)
- management_mode: third_party_managed
- market: Charlotte
- org_id: {org}
- role: asset_manager

## Handoff checklist

| # | Workstream | Owner | Status | Lag days | Tolerance band check | Notes |
|---|---|---|---|---|---|---|
| 1 | AppFolio property setup (promote placeholder -> stabilized) | regional_ops_director | complete | 2 | within band | unit_count_total=248, unit_count_rentable=244, nrsf_total=218,560 all populated |
| 2 | Intacct legal entity dim | finance_systems_team | complete | 1 | within band | legal_entity_id=ENT_RIVERWOOD_LLC; project dim created |
| 3 | Intacct project dim for opening capex reserves | finance_systems_team | complete | 3 | within band | reserves slotted to property dim |
| 4 | Vendor master rationalization | regional_ops_director | in_progress | 4 | within band | 3 of 5 vendors resolved; 2 pending identity resolution (section 7.3) |
| 5 | Opening rent roll load + reconciliation | regional_ops_director | complete | 2 | within band | `opening_rent_roll_reconciliation_variance=0.4%` |
| 6 | PMA execution (TPM) | asset_mgmt_director + legal | complete | -2 | n/a | Executed 2026-04-08 (pre-close); pma_execution_lag_days=-2 |
| 7 | Lender reporting registration | reporting_finance_ops_lead | complete | 2 | within band | Acknowledgment 2026-04-12; row 14 approval on file |
| 8 | Property tax lot + assessment registration | finance_systems_team | complete | 3 | within band | research inherited from post_ic_property_setup |
| 9 | Operating insurance binder bound | asset_mgmt_director | complete | 0 | n/a | Bound day of close; no transition gap |
| 10 | Data-platform property_master_crosswalk row | data_platform_team | in_progress | 4 | within band | row draft pending review; `crosswalk_row_creation_lag_days=4` |
| 11 | Data-platform asset_crosswalk row | data_platform_team | in_progress | 4 | within band | same reviewer |
| 12 | Data-platform vendor_master_crosswalk additions | data_platform_team | in_progress | 4 | within band | gated on vendor rationalization item #4 |

## Scorecard

- `handoff_completeness_score` (proposed): **0.82** (weighted).
- `handoff_lag_days` (proposed), worst-workstream: **4 days** (within `handoff_lag_threshold_days` band per `reference/normalized/schemas/reconciliation_tolerance_band.yaml`).
- `vendor_rationalization_count` (proposed): **3 of 5** resolved.
- `opening_rent_roll_reconciliation_variance` (proposed): **0.4%** (within band).
- `pma_execution_lag_days` (proposed): **-2** (pre-close).
- `crosswalk_row_creation_lag_days` (proposed): **4** (within band).

## Open blockers

1. Vendor identity resolution for 2 inherited vendors (pest and landscape). Reviewer: regional_ops_director per `identity_resolution_framework.md` section 7.3.
2. `property_master_crosswalk` + `asset_crosswalk` row review pending. Reviewer: regional_ops_director.
3. Vendor rationalization gate on `vendor_master_crosswalk.yaml` additions (gated on item 1).

## Gates potentially triggered

- row 7 (handoff lag) — not triggered; within band.
- row 14 (lender registration) — approval on file.
- row 17 (missing approver / insurance gap) — n/a.
- row 19 (PMA amendment) — approval on file.

## ApprovalRequest — terminal sign-off

- `approval_request_id`: ar_acq_handoff_d_2026_acq_004
- Row: 7 (handoff completion sign-off routed as row 7 per overlay policy)
- Approver: asset_mgmt_director
- Packet: checklist, scorecard, blocker memo, proposed crosswalk rows
- Status: pending_approver_review
- Routed via: `workflows/owner_approval_routing`

## Confidence banner

```
References:
- lifecycle_handoffs.md@wave_4_authoritative
- source_of_truth_matrix.md@wave_4_authoritative
- dealpath_deal_pipeline/dq_rules.yaml@2026-04-15 (stub)
- property_master_crosswalk.yaml@2026-03-31 (sample)
- asset_crosswalk.yaml@2026-03-31 (sample)
- vendor_master_crosswalk.yaml@2026-03-31 (sample)
- reconciliation_tolerance_band.yaml@2026-03-31 (starter)
- approval_threshold_defaults.csv@2026-03-31 (starter)
Blocking rules cited: dp_handoff_lag, dp_one_deal_multiple_projects (neither fired).
Note: data-platform crosswalk writes are proposed-then-approve; no crosswalk rows
merged until `asset_mgmt_director` sign-off completes.
```
