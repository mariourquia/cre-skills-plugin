# Example — Development Pipeline Tracking (abridged)

**Prompt:** "Run the weekly development pipeline tracker. Flag critical-path slip beyond tolerance, and check commitment overdrawn status across all active projects."

**Inputs:** Dealpath deal + milestone registers + Procore project + schedule-milestone + commitment + CO + draw registers + Intacct capex actuals + dev_project_crosswalk + capex_project_crosswalk + construction_duration_assumptions + reconciliation_tolerance_band + contingency_assumptions + approval_threshold_defaults.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- region: southeast (optional filter applied)
- deal_lead: all (unfiltered)
- project_id: n/a (pipeline-wide view)
- role: development_manager
- output_type: dashboard + memo
- decision_severity: recommendation

## Expected packs loaded

- `workflows/development_pipeline_tracking/`
- `workflows/schedule_risk_review/` (child — conditional handoff)
- `workflows/cost_to_complete_review/` (child — conditional handoff)
- `workflows/draw_package_review/` (child — conditional handoff)
- `workflows/change_order_review/` (child — conditional handoff)
- `workflows/lease_up_first_period/` (child — queued for near-delivery projects)
- `overlays/segments/middle_market/`

## Expected references

- `reference/connectors/_core/stack_wave4/source_of_truth_matrix.md`
- `reference/connectors/adapters/dealpath_deal_pipeline/normalized_contract.yaml`
- `reference/connectors/adapters/dealpath_deal_pipeline/reconciliation_rules.md`
- `reference/connectors/adapters/procore_construction/reconciliation_checks.yaml`
- `reference/connectors/adapters/procore_construction/runbooks/procore_common_issues.md`
- `reference/connectors/adapters/sage_intacct_gl/reconciliation_rules.md`
- `reference/connectors/master_data/dev_project_crosswalk.yaml`
- `reference/connectors/master_data/capex_project_crosswalk.yaml`
- `reference/normalized/construction_duration_assumptions__southeast.csv`
- `reference/normalized/schemas/reconciliation_tolerance_band.yaml`
- `reference/normalized/approval_threshold_defaults.csv`
- `reference/derived/contingency_assumptions__{org}.csv`

## Gates potentially triggered (elsewhere)

- `workflows/schedule_risk_review`: rebaseline approval (per overlay) — Willow Creek.
- `workflows/cost_to_complete_review`: budget reallocation approval — two projects approaching contingency-burn threshold.
- `workflows/draw_package_review`: row 12 (internal submission readiness) and row 14 (lender final submission) — Oakleaf next draw cycle.
- `workflows/change_order_review`: rows 10 / 11 per dollar threshold — one pending CO > overlay ceiling aging.

## Expected output shape

- Pipeline stage dashboard (sites_under_contract, in_entitlement, in_design,
  in_permitting, in_construction by phase).
- Schedule posture KPI table per project: `schedule_variance_days`,
  `milestone_slippage_rate`, `critical_path_slip_days` (proposed).
- Cost posture KPI table per project: `cost_to_complete` (inherited),
  `contingency_remaining`, `contingency_burn_rate`,
  `change_orders_pct_of_contract`, `trade_buyout_variance`,
  `capex_spend_vs_plan`.
- Draw posture KPI table per project: `draw_cycle_time`,
  `draw_burn_rate_vs_plan` (proposed), open draws by aging bucket.
- Commitment exposure: forward 12-month
  `commitment_exposure_forward_dollars` (proposed) aggregated + per-trade
  breakdown + commitments-overdrawn list with runbook pointers.
- Delivery outlook + lease-up readiness for near-delivery projects.
- Financing draw status forward 60 days.
- Reconciliation posture memo (dp/pc/intacct findings).
- Regional / deal-lead rollup.
- Top-3 watch items narrative.

## Confidence banner pattern

```
References: source_of_truth_matrix@wave_4_authoritative,
dev_project_crosswalk@2026-04-08 (starter),
capex_project_crosswalk@2026-04-08 (starter),
construction_duration_assumptions__southeast@2026-03-31 (starter),
reconciliation_tolerance_band@2026-03-31 (sample),
contingency_assumptions__{org}@2026-03-31 (starter),
approval_threshold_defaults@2026-03-31 (starter).
Proposed metrics (flagged): critical_path_slip_days,
draw_burn_rate_vs_plan, cco_to_first_lease_days,
handoff_lag_dealpath_to_procore, commitment_exposure_forward_dollars.
Canonical extensions required: deal, deal_milestone, commitment
(tracked separately under canonical change-control).
Cross-system posture: Dealpath primary for deal-state; Procore primary
for construction-state + commitments; Intacct primary for posted actuals.
```

## Example narrative excerpt

Portfolio-level schedule posture is within overlay tolerance in aggregate. One
critical-path slip (Willow Creek, framing trade lead-time) exceeds the
`reconciliation_tolerance_band.yaml::critical_path_slip_band`; hand-off to
`workflows/schedule_risk_review` triggered. Two commitments on Riverbend
sitework failed `pc_recon_commitment_overdrawn` — draws on Riverbend held per
the procore runbook `commitment_overdrawn` pending GC reconciliation. Atlantic
Grove (closed 2026-04-02, funded 2026-04-04) has no Procore project mapped as
of 2026-04-10 — `dp_handoff_dev_lag` warning raised at 6 business days; below
the blocker threshold of 10 business days but routed to development_manager
per dealpath runbook `dev_handoff`.

Regional rollup: Southeast carries 6 of 11 active construction projects and
82% of forward 12-month commitment exposure. Deal_lead rollup: three deal_leads
hold > $80M each of forward commitment exposure; Alex's book carries the
largest single-project exposure (Willow Creek).

South Fork enters the 180-day-pre-delivery window next week; handoff to
`workflows/lease_up_first_period` queued.
