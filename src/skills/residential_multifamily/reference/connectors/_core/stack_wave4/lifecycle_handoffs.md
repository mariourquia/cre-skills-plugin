# Lifecycle Handoffs — Wave 4 Stack

Status: wave_4_authoritative
Audience: data_platform_team, asset_mgmt, finance_reporting, regional_ops, construction_lead

Each handoff is an explicit cross-system event with required state, gating
approvals, blocking issues, and downstream workflow activation. No silent
state transitions; every handoff lands a `source_record_audit` row.

---

## Handoff 1 — Dealpath → approved acquisition or development record

- **Trigger event**: Dealpath deal `stage` transitions to `ic_approved` AND `deal_close_date_actual` is non-null (acquisition) OR `gc_award_date` is non-null (development).
- **Source objects**: `deal`, `asset`, `deal_milestone(ic_approved)`, `deal_key_dates`.
- **Destination objects**: canonical `deal`, `asset`, `approval_request` (IC record), `property` (placeholder), `development_project` or `capex_project` seed.
- **Required fields**: deal_id, asset_id, deal_type, ic_approval_date, ic_approved_amount, deal_team_lead, expected_close_date, target_property_count, target_unit_count, market, submarket, segment, form_factor (if known), lifecycle_stage_target.
- **Optional fields**: financing_term, equity_partner, jv_structure, target_hold_period.
- **Gating approvals**: IC approval present, executive sign-off if deal size > policy band (cite `reference/normalized/schemas/approval_threshold_policy.yaml`).
- **Blocking issues**: missing IC approval record, deal type unrecognized, asset_crosswalk row absent, property setup not initiated downstream within 5 business days.
- **Quality checks**: `deal_pipeline.dq_rules.yaml` rules `dp_completeness_ic_record`, `dp_referential_asset_present`, `dp_handoff_lag`.
- **Open questions queue**: any unresolved field surfaced via `master_data/unresolved_exceptions_queue.md`.
- **Example handoff payload**:

```json
{
  "handoff_id": "h_dp_to_approved_2026Q1_acq_004",
  "source_event": {"system": "dealpath", "deal_id": "d_2026_acq_004", "stage": "ic_approved", "occurred_at": "2026-03-22T15:14:00Z"},
  "canonical_emit": [
    {"object": "deal", "canonical_id": "deal_2026_acq_004", "status": "ic_approved"},
    {"object": "asset", "canonical_id": "asset_riverwood_acq", "status": "pre_close"},
    {"object": "approval_request", "canonical_id": "ar_dp_ic_2026_acq_004", "status": "approved", "policy_ref": "ic_policy_v3"},
    {"object": "property", "canonical_id": "prop_riverwood_placeholder", "status": "pre_setup"},
    {"object": "development_project", "canonical_id": null, "status": "n/a (acquisition)"}
  ],
  "downstream_workflows_activated": ["acquisition_handoff", "post_ic_property_setup", "executive_pipeline_summary"]
}
```

- **Downstream workflows activated**: `acquisition_handoff`, `post_ic_property_setup` (proposed), `executive_pipeline_summary` (proposed), `pre_close_deal_tracking` (proposed).

---

## Handoff 2 — Dealpath → Procore (development project setup)

- **Trigger event**: development deal IC-approved AND `gc_selected_at` non-null.
- **Source objects**: `deal`, `dev_project`, `deal_team_assignments`.
- **Destination objects**: Procore `project`, canonical `development_project`, canonical `construction_project`.
- **Required fields**: project_name, address, gc_vendor_id, target_break_ground_date, target_completion_date, total_budget_seed, scope_summary, project_dim_for_intacct.
- **Optional fields**: phasing_plan, schedule_baseline_imported, contracted_units_count.
- **Gating approvals**: dev_project canonical exists, IC approval signed, vendor master entry for GC.
- **Blocking issues**: target_completion_date in past, gc_vendor_id unresolved, no Intacct project dimension created.
- **Quality checks**: `dev_project_crosswalk` row populated, vendor_master_crosswalk resolves GC, `procore_construction.dq_rules.yaml` rule `pc_handoff_dealpath_alignment`.
- **Example handoff payload**:

```json
{
  "handoff_id": "h_dp_to_pc_dev_2026_riverwood",
  "source_event": {"system": "dealpath", "deal_id": "d_2026_dev_007", "milestone": "gc_selected"},
  "canonical_emit": [
    {"object": "construction_project", "canonical_id": "cp_riverwood_phase1", "status": "pre_construction"},
    {"object": "vendor", "canonical_id": "vendor_acme_construction", "role": "general_contractor"}
  ],
  "downstream_setup_required": ["procore_project_create", "intacct_project_dim_create"],
  "downstream_workflows_activated": ["capital_project_intake_and_prioritization", "schedule_risk_review"]
}
```

- **Downstream workflows activated**: `capital_project_intake_and_prioritization`, `schedule_risk_review`, `cost_to_complete_review` (post-baseline).

---

## Handoff 3 — Dealpath / Intacct → AppFolio (property setup)

- **Trigger event**: deal_close_date_actual non-null (acquisition) OR construction milestone `temp_co_received` (development).
- **Source objects**: Dealpath `deal`/`asset`; Intacct `entity`/`location`/`project` dimensions.
- **Destination objects**: AppFolio `property`, canonical `property`, market/submarket tags, lifecycle_stage tag.
- **Required fields**: property_id (canonical), property_name, address, legal_entity_id (intacct entity), market, submarket, segment, form_factor, lifecycle_stage, unit_count_total, unit_count_rentable, management_mode, takeover_date or delivery_date.
- **Optional fields**: portfolio_tag, gl_partner_code, ownership_pct, third_party_manager_id.
- **Gating approvals**: property_master_crosswalk row created, asset → property mapping confirmed, lifecycle_stage assigned.
- **Blocking issues**: unit_count_total absent, market unmapped (no markets/<market>/ entry under reference), management_mode missing.
- **Quality checks**: `appfolio_pms.dq_rules.yaml` rule `ap_handoff_property_complete`.
- **Example handoff payload**:

```json
{
  "handoff_id": "h_dp_int_to_af_setup_riverwood",
  "source_event": {"system": "dealpath+intacct", "deal_id": "d_2026_acq_004", "trigger": "close_complete"},
  "canonical_emit": [
    {"object": "property", "canonical_id": "prop_riverwood", "status": "pre_takeover", "lifecycle_stage": "stabilized"}
  ],
  "downstream_setup_required": ["appfolio_property_create", "unit_roster_seed", "rent_roll_first_load"],
  "downstream_workflows_activated": ["monthly_property_operating_review", "lead_to_lease_funnel_review"]
}
```

- **Downstream workflows activated**: `monthly_property_operating_review`, `lead_to_lease_funnel_review`, `delinquency_collections`, `move_in_administration`.

---

## Handoff 4 — AppFolio + Intacct → monthly property review

- **Trigger event**: month_end + close_period_complete + appfolio_extract_landed.
- **Source objects**: AppFolio (operating); Intacct (financial).
- **Destination objects**: `property_scorecard_markdown` per `monthly_property_operating_review`.
- **Required fields**: full canonical Property + Building + Unit + Lease + LeaseEvent + Charge + Payment + DelinquencyCase + WorkOrder + TurnProject + BudgetLine + ForecastLine + VarianceExplanation.
- **Optional fields**: market_rent_benchmark (excel) for market-comparison panel.
- **Gating approvals**: none for read-only review; concession_over_policy or vendor_over_policy if remediation.
- **Blocking issues**: unit_count_reconciliation_fail, lease_status_sum_not_equal_unit_count, budget_actual_alignment_fail, null_critical_occupancy_field.
- **Quality checks**: see `workflow_activation_map.yaml::monthly_property_operating_review.blocking_issues`.
- **Downstream workflows activated**: `monthly_asset_management_review`, `quarterly_portfolio_review`.

---

## Handoff 5 — Procore + Intacct → project controls review

- **Trigger event**: weekly cadence + procore_extract_landed + intacct_close_for_period.
- **Source objects**: Procore (project, budget, commitments, COs, draws, schedule); Intacct (capex postings, project dim).
- **Destination objects**: `cost_to_complete_review` output, `change_order_review` output, `draw_package_review` output, `schedule_risk_review` output.
- **Required fields**: capex_project, estimate_line_item, change_order, draw_request, schedule_milestone + intacct actuals at project_dim grain.
- **Optional fields**: vendor_rate references, material_cost references for benchmark commentary.
- **Gating approvals**: CO above policy, draw above policy, contingency burn above policy.
- **Blocking issues**: project_name not matching property name, vendor duplicates, CO approved without intacct posting >10 days, draw timing mismatch >5 days, schedule baseline missing.
- **Downstream workflows activated**: `change_order_review`, `cost_to_complete_review`, `draw_package_review`, `schedule_risk_review`.

---

## Handoff 6 — Excel market surveys + AppFolio → pricing and renewal support

- **Trigger event**: weekly excel_rent_comp landed + appfolio_extract_landed.
- **Source objects**: Excel (rent_comp, concession, market_rent_benchmark, occupancy_benchmark); AppFolio (Lease, Charge, lease_event renewal).
- **Destination objects**: `market_rent_refresh` output, `renewal_retention` output.
- **Required fields**: rent_comp passing dq, market_rent_benchmark current within staleness window, current AppFolio rent roll.
- **Optional fields**: concession_benchmark, asset_specific_comp_pack.
- **Gating approvals**: pricing-policy override if market_to_lease_gap > policy band; renewal_offer above policy.
- **Blocking issues**: rent_comp staleness, submarket tag mismatch (excel vs appfolio), luxury contamination in middle_market sheet.
- **Downstream workflows activated**: `market_rent_refresh`, `rent_comp_intake`, `renewal_retention`.

---

## Handoff 7 — All sources → quarterly portfolio review and executive summary

- **Trigger event**: quarter_end + all wave-4 sources extract_complete.
- **Source objects**: every wave-4 source (Dealpath, AppFolio, Intacct, Procore, Excel, GraySail-when-classified, manual).
- **Destination objects**: `quarterly_portfolio_review` output, `executive_operating_summary_generation` output.
- **Required fields**: deal pipeline, project execution, operating performance, benchmark context, financial rollups, risk flags.
- **Optional fields**: confidence and missing-data annotations from source_record_audit.
- **Gating approvals**: allocation_shift, hold_sell_recommendation, executive_summary_signoff.
- **Blocking issues**: any source in `degraded` status without operator acknowledgement; GraySail unresolved.
- **Quality checks**: confidence floor `medium` per `workflow_activation_map.yaml`.
- **Downstream workflows activated**: `executive_operating_summary_generation`, `owner_approval_routing`.

---

## Handoff 8 — Procore → AppFolio at delivery (construction → operations)

- **Trigger event**: schedule_milestone `temp_co_received` OR `final_co_received` AND units_ready_for_lease >= 1.
- **Source objects**: Procore `schedule_milestone`, `punchlist_items`, `closeout_documents`.
- **Destination objects**: AppFolio property + unit roster transition from `pre_takeover` to `lease_up`.
- **Required fields**: unit_roster_count_matches_construction_drawings, certificate_of_occupancy_received, address_validated, lifecycle_stage transitioning to `lease_up`.
- **Optional fields**: warranty_period_start, gc_punchlist_count_remaining.
- **Gating approvals**: lifecycle_stage transition, lease-up pricing policy seeded.
- **Blocking issues**: unit count mismatch (construction drawings vs operational roster), CO not received, address invalid.
- **Quality checks**: `procore_construction.reconciliation_checks.yaml::pc_to_af_handoff` and `appfolio_pms.dq_rules.yaml::ap_lease_up_setup_complete`.
- **Downstream workflows activated**: `lead_to_lease_funnel_review`, `monthly_property_operating_review`, `quarterly_portfolio_review`.

---

## Tracking

Every handoff lands one row to `monitoring/observability_events.yaml` event type
`stack_handoff_completed`, plus one row to `source_record_audit` per canonical
object emitted. The exception_routing.yaml rule `handoff_lag_alert` fires when
expected handoff does not complete within `handoff_lag_threshold_days` per
`reference/normalized/schemas/handoff_lag_policy.yaml`.
