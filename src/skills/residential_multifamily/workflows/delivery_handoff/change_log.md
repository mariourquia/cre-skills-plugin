# Change Log — delivery_handoff

## 0.1.0 — 2026-04-15

- Pack initialized. Wave-5 introduction. Authored as part of stack-specific
  operationalization of `reference/connectors/_core/stack_wave4/lifecycle_handoffs.md`
  Handoff 8 (Procore -> AppFolio at delivery, construction -> operations).
- Delivery handoff checklist authored: TCO/CO recording, punchlist state review,
  retainage release schedule, rent-roll transition from lease-up plan to active,
  vendor rationalization (construction subs archived; operating service vendors
  onboarded) via `master_data/identity_resolution_framework.md`, warranty
  package handoff, system as-built documentation acceptance, capex project
  closeout in Intacct, `dev_project_crosswalk.yaml` closure (procore_project_id
  -> property_id linkage), `property_master_crosswalk.yaml` transition
  (`pre_takeover`/`construction` -> `lease_up`), lease-up pricing policy seed,
  and downstream trigger for `workflows/lease_up_first_period`.
- Proposed metrics introduced: `cco_to_first_lease_days`,
  `tco_to_first_unit_ready_days`, `delivery_handoff_completeness_score`,
  `retainage_release_lag_days`, `warranty_package_completeness`,
  `as_built_doc_completeness`, `vendor_rationalization_count` (shared with
  `acquisition_handoff`), `capex_closeout_lag_days`,
  `dev_project_crosswalk_closure_lag_days`. To be lifted into `_core/metrics.md`
  before promotion beyond draft. Existing metrics used: `punchlist_closeout_rate`,
  `lease_up_pace_post_delivery`.
- Approval gates: row 4 (safety-critical if TCO before punchlist complete),
  row 7 (handoff lag + terminal sign-off), row 11 (major capex / CO closeout),
  row 13 (lease-up pricing policy), row 17 (policy-marked acceptance: warranty
  package, missing-approver, insurance gap), row 19 (vendor agreement
  signatures).
- Blocking issue ids cited: `recon_pc_to_af_at_delivery`,
  `ap_lease_up_setup_complete`, `pc_to_af_handoff`.
- Downstream workflow activation: `workflows/lease_up_first_period` triggered
  on terminal sign-off.
- Status: draft.
