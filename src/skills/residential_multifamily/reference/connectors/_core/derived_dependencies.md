# Derived Dependencies

Master tables that map canonical metrics and canonical workflows to the
connectors, normalized objects, reference categories, and derived inputs they
need. These tables are the ground truth for workflow activation gating and
for the DQ exception routing logic.

- Connectors referenced: `pms`, `gl`, `crm`, `ap`, `market_data`,
  `construction`, `hr_payroll`, `manual_uploads`.
- Metric slugs match `_core/metrics.md` exactly.
- Workflow slugs match `workflows/` exactly.
- The machine-readable view of the workflow table is
  `workflow_activation_map.yaml`.

Reading tip: "required_" means activation cannot proceed without it.
"optional_enrichment_" means activation proceeds and surfaces confidence
downgrade when missing.

## Metric-to-connector dependency table

Columns:

- `metric_slug` - canonical slug.
- `required_raw_sources` - connector domains that must land data.
- `required_normalized_objects` - canonical objects the metric reads.
- `required_reference_categories` - reference categories the metric cites.
- `optional_enrichment_sources` - connector domains that improve confidence
  when available.

### Property Operations family

| metric_slug | required_raw_sources | required_normalized_objects | required_reference_categories | optional_enrichment_sources |
|---|---|---|---|---|
| physical_occupancy | pms | Property, Building, Unit, Lease | occupancy_benchmark | market_data, manual_uploads |
| leased_occupancy | pms | Unit, Lease, LeaseEvent | occupancy_benchmark | market_data, manual_uploads |
| economic_occupancy | pms, gl | Unit, Lease, Charge, Payment | occupancy_benchmark | manual_uploads |
| notice_exposure | pms | Lease, LeaseEvent | occupancy_benchmark | manual_uploads |
| preleased_occupancy | pms, crm | Unit, Lease, Application | occupancy_benchmark | market_data |
| lead_response_time | crm | Lead, Tour | - | pms, manual_uploads |
| tour_conversion | crm, pms | Lead, Tour, Application | - | manual_uploads |
| application_conversion | crm, pms | Application, ApprovalOutcome | - | manual_uploads |
| approval_rate | pms | Application, ApprovalOutcome | - | - |
| move_in_conversion | pms | Application, Lease, LeaseEvent | - | crm |
| renewal_offer_rate | pms | Lease, LeaseEvent | - | manual_uploads |
| renewal_acceptance_rate | pms | Lease, LeaseEvent | - | manual_uploads |
| turnover_rate | pms | Lease, LeaseEvent, Unit | - | manual_uploads |
| average_days_vacant | pms | Unit, Lease, LeaseEvent | - | manual_uploads |
| make_ready_days | pms | WorkOrder, TurnProject, Unit | unit_turn_cost | manual_uploads |
| open_work_orders | pms | WorkOrder | - | manual_uploads |
| work_order_aging | pms | WorkOrder | - | manual_uploads |
| repeat_work_order_rate | pms | WorkOrder | - | manual_uploads |
| delinquency_rate_30plus | pms, gl | ResidentAccount, Charge, Payment, DelinquencyCase | - | manual_uploads |
| collections_rate | pms, gl | Charge, Payment, DelinquencyCase | - | manual_uploads |
| bad_debt_rate | gl, pms | Charge, Payment | - | manual_uploads |
| concession_rate | pms | Lease, Charge | concession_benchmark | market_data |
| rent_growth_new_lease | pms | Lease, LeaseEvent | market_rent_benchmark | market_data |
| rent_growth_renewal | pms | Lease, LeaseEvent | market_rent_benchmark | market_data |
| blended_lease_trade_out | pms | Lease, LeaseEvent | market_rent_benchmark | market_data |
| market_to_lease_gap | pms, market_data | Lease, Unit | market_rent_benchmark, rent_comp | - |
| loss_to_lease | pms, market_data | Lease, Unit | market_rent_benchmark, rent_comp | - |
| payroll_per_unit | hr_payroll, gl | Property, Unit, StaffingPlan | payroll_assumption, staffing_model | manual_uploads |
| rm_per_unit | gl, ap | Property, Unit | - | manual_uploads |
| utilities_per_unit | gl, ap | Property, Unit | utility_benchmark | manual_uploads |
| controllable_opex_per_unit | gl | Property, Unit | - | ap, manual_uploads |

### Asset Management family

| metric_slug | required_raw_sources | required_normalized_objects | required_reference_categories | optional_enrichment_sources |
|---|---|---|---|---|
| revenue_variance_to_budget | gl, pms | BudgetLine, Charge, Payment | - | manual_uploads |
| expense_variance_to_budget | gl, ap | BudgetLine | - | manual_uploads |
| noi | gl, pms | Property, Charge, Payment | - | ap, manual_uploads |
| noi_margin | gl, pms | Property | - | manual_uploads |
| dscr | gl | Property | - | manual_uploads |
| debt_yield | gl | Property | - | manual_uploads |
| capex_spend_vs_plan | gl, construction | CapexProject, BudgetLine | capex_line_item | ap, manual_uploads |
| renovation_yield_on_cost | pms, gl, construction | CapexProject, Lease, Unit | - | market_data |
| stabilization_pace_vs_plan | pms | Lease, LeaseEvent, Unit | - | market_data |
| renewal_rent_delta_dollars | pms | Lease, LeaseEvent | market_rent_benchmark | - |
| forecast_accuracy | gl | ForecastLine, BudgetLine | - | manual_uploads |

### Portfolio Management family

| metric_slug | required_raw_sources | required_normalized_objects | required_reference_categories | optional_enrichment_sources |
|---|---|---|---|---|
| same_store_noi_growth | gl, pms | Property | - | - |
| occupancy_by_market | pms | Property, Unit, Lease | occupancy_benchmark | market_data |
| delinquency_by_market | pms, gl | Property, ResidentAccount, Charge, Payment | - | - |
| turn_cost_by_market | pms, construction, ap | Property, WorkOrder, TurnProject | unit_turn_cost | - |
| portfolio_concentration_market | pms | Property | - | - |
| asset_watchlist_score | pms, gl | Property | occupancy_benchmark | market_data, manual_uploads |
| budget_attainment | gl | BudgetLine | - | manual_uploads |

### Development and Construction family

| metric_slug | required_raw_sources | required_normalized_objects | required_reference_categories | optional_enrichment_sources |
|---|---|---|---|---|
| dev_cost_per_unit | construction, gl | CapexProject, EstimateLineItem | development_budget_assumption, capex_line_item | ap |
| dev_cost_per_gsf | construction, gl | CapexProject, EstimateLineItem | development_budget_assumption | - |
| dev_cost_per_nrsf | construction, gl | CapexProject, EstimateLineItem | development_budget_assumption | - |
| contingency_remaining | construction, gl | CapexProject, ChangeOrder, DrawRequest | - | ap |
| contingency_burn_rate | construction, gl | CapexProject, ChangeOrder, DrawRequest | - | ap |
| change_orders_pct_of_contract | construction | CapexProject, BidPackage, ChangeOrder | - | ap |
| cost_to_complete | construction, gl | CapexProject, EstimateLineItem, ChangeOrder | capex_line_item | ap |
| schedule_variance_days | construction | CapexProject, ScheduleMilestone | construction_duration_assumption | - |
| milestone_slippage_rate | construction | CapexProject, ScheduleMilestone | construction_duration_assumption | - |
| trade_buyout_variance | construction | CapexProject, BidPackage, EstimateLineItem | capex_line_item, labor_rate, material_cost | ap |
| draw_cycle_time | construction, gl | DrawRequest | - | ap |
| punchlist_closeout_rate | construction | CapexProject, ScheduleMilestone | - | - |
| lease_up_pace_post_delivery | pms, construction | Lease, LeaseEvent, Unit, CapexProject | occupancy_benchmark, market_rent_benchmark | market_data |

### TPM Oversight family

| metric_slug | required_raw_sources | required_normalized_objects | required_reference_categories | optional_enrichment_sources |
|---|---|---|---|---|
| report_timeliness | manual_uploads | Property | - | pms, gl |
| kpi_completeness | manual_uploads | Property | - | pms, gl |
| variance_explanation_completeness | manual_uploads, gl | VarianceExplanation, BudgetLine | - | pms |
| budget_adherence_tpm | gl | BudgetLine | - | manual_uploads |
| staffing_vacancy_rate_tpm | hr_payroll | StaffingPlan | staffing_model, payroll_assumption | manual_uploads |
| tpm_collections_performance | pms, gl | Charge, Payment, DelinquencyCase | occupancy_benchmark | manual_uploads |
| tpm_turn_performance | pms | WorkOrder, TurnProject, Unit | unit_turn_cost | manual_uploads |
| service_level_adherence | pms, crm | WorkOrder, Tour, Lead | - | manual_uploads |
| approval_response_time_tpm | pms | ApprovalRequest | - | manual_uploads |
| audit_issue_count_and_severity | manual_uploads | Property | - | - |

## Workflow activation table

Columns:

- `workflow_slug` - canonical workflow slug.
- `required_normalized_inputs` - canonical objects the workflow reads.
- `required_derived_inputs` - derived categories the workflow reads.
- `optional_enrichment_inputs` - categories that improve confidence.
- `minimum_confidence_threshold` - activation threshold (`low`, `medium`,
  `high`).
- `blocking_data_issues` - DQ exceptions that block activation at `blocker`
  severity.
- `fallback_mode_when_partial` - how the workflow degrades with missing
  inputs.

### monthly_property_operating_review

- required_normalized_inputs: Property, Building, Unit, UnitType, Lease,
  LeaseEvent, Charge, Payment, DelinquencyCase, WorkOrder, TurnProject,
  BudgetLine, ForecastLine, VarianceExplanation
- required_derived_inputs: role_kpi_targets, occupancy_benchmark,
  concession_benchmark
- optional_enrichment_inputs: market_rent_benchmark, utility_benchmark
- minimum_confidence_threshold: medium
- blocking_data_issues: unit_count_reconciliation_fail,
  lease_status_sum_not_equal_unit_count, budget_actual_alignment_fail,
  null_critical_occupancy_field
- fallback_mode_when_partial: produce property scorecard with data-gap
  annotations; mark missing KPIs as "unavailable"; exclude market-comparison
  panel if market_rent_benchmark absent; flag for site-ops and regional-ops.

### monthly_asset_management_review

- required_normalized_inputs: Property, BudgetLine, ForecastLine,
  VarianceExplanation, Charge, Payment, CapexProject
- required_derived_inputs: asset_watchlist_score, role_kpi_targets
- optional_enrichment_inputs: occupancy_benchmark, market_rent_benchmark
- minimum_confidence_threshold: medium
- blocking_data_issues: budget_actual_alignment_fail,
  forecast_completeness_fail
- fallback_mode_when_partial: produce asset-level commentary; mark watchlist
  score as stale with `confidence=low`; surface missing inputs at top of
  output.

### quarterly_portfolio_review

- required_normalized_inputs: Property, Building, Unit, Lease, BudgetLine,
  ForecastLine, CapexProject
- required_derived_inputs: same_store_noi_growth, occupancy_by_market,
  delinquency_by_market, portfolio_concentration_market
- optional_enrichment_inputs: market_rent_benchmark, utility_benchmark
- minimum_confidence_threshold: medium
- blocking_data_issues: same_store_cohort_undefined,
  portfolio_cohort_membership_missing
- fallback_mode_when_partial: produce partial roll-up; flag properties with
  missing inputs; exclude affected properties from same-store cohort with
  rationale.

### third_party_manager_scorecard_review

- required_normalized_inputs: Property, Charge, Payment, DelinquencyCase,
  WorkOrder, TurnProject, ApprovalRequest, StaffingPlan, VarianceExplanation
- required_derived_inputs: report_timeliness, kpi_completeness,
  tpm_collections_performance, tpm_turn_performance,
  staffing_vacancy_rate_tpm, service_level_adherence,
  budget_adherence_tpm, variance_explanation_completeness,
  approval_response_time_tpm
- optional_enrichment_inputs: audit_issue_count_and_severity
- minimum_confidence_threshold: medium
- blocking_data_issues: tpm_report_feed_missing, kpi_completeness_blocker
- fallback_mode_when_partial: produce scorecard with `completeness_score`
  visible; list missing KPIs; do not compute composite until completeness
  threshold is met.

### owner_approval_routing

- required_normalized_inputs: ApprovalRequest, Property, Lease,
  VendorAgreement, ChangeOrder, DrawRequest, CapexProject
- required_derived_inputs: approval_threshold_policy (reference category),
  approval_response_time_tpm
- optional_enrichment_inputs: -
- minimum_confidence_threshold: high
- blocking_data_issues: approval_matrix_not_loaded,
  approver_identity_unresolved, policy_violation
- fallback_mode_when_partial: do not route; surface missing threshold or
  approver with `dq_blocker` exception and wait.

### executive_operating_summary_generation

- required_normalized_inputs: Property, Charge, Payment, VarianceExplanation,
  BudgetLine, CapexProject
- required_derived_inputs: noi, noi_margin, budget_attainment,
  asset_watchlist_score, same_store_noi_growth
- optional_enrichment_inputs: market_rent_benchmark, occupancy_by_market
- minimum_confidence_threshold: medium
- blocking_data_issues: budget_actual_alignment_fail
- fallback_mode_when_partial: produce summary with data-gap sidebar; mark
  metrics with `confidence=low` and cite the gap in narrative.

### lead_to_lease_funnel_review

- required_normalized_inputs: Lead, Tour, Application, ApprovalOutcome,
  Lease, LeaseEvent
- required_derived_inputs: lead_response_time, tour_conversion,
  application_conversion, approval_rate, move_in_conversion
- optional_enrichment_inputs: preleased_occupancy, market_rent_benchmark
- minimum_confidence_threshold: medium
- blocking_data_issues: crm_feed_missing, lead_to_lease_join_rate_below_floor
- fallback_mode_when_partial: compute funnel from the stages that are joinable;
  flag missing stages; show funnel with unobserved segments.

### renewal_retention

- required_normalized_inputs: Lease, LeaseEvent, Unit, ResidentAccount
- required_derived_inputs: renewal_offer_rate, renewal_acceptance_rate,
  turnover_rate
- optional_enrichment_inputs: market_rent_benchmark, concession_benchmark
- minimum_confidence_threshold: medium
- blocking_data_issues: lease_event_sequence_gap,
  null_critical_renewal_window
- fallback_mode_when_partial: limit analysis to leases with complete event
  sequences; annotate excluded leases; output retention bands with
  confidence labels.

### move_in_administration

- required_normalized_inputs: Application, ApprovalOutcome, Lease,
  LeaseEvent, Unit, WorkOrder, TurnProject
- required_derived_inputs: make_ready_days
- optional_enrichment_inputs: -
- minimum_confidence_threshold: medium
- blocking_data_issues: unit_not_ready_blocker, approval_pending_blocker,
  fair_housing_sensitive
- fallback_mode_when_partial: surface blockers and wait; produce punch list
  of items that must resolve before move-in can proceed.

### move_out_administration

- required_normalized_inputs: Lease, LeaseEvent, Unit, WorkOrder,
  TurnProject, Charge, Payment, ResidentAccount
- required_derived_inputs: average_days_vacant, make_ready_days
- optional_enrichment_inputs: unit_turn_cost
- minimum_confidence_threshold: medium
- blocking_data_issues: final_account_statement_missing,
  lease_termination_reason_unmapped
- fallback_mode_when_partial: produce move-out packet with clearly-marked
  pending items; flag security-deposit accounting gaps.

### delinquency_collections

- required_normalized_inputs: ResidentAccount, Charge, Payment,
  DelinquencyCase, Lease
- required_derived_inputs: delinquency_rate_30plus, collections_rate,
  bad_debt_rate
- optional_enrichment_inputs: approval_threshold_policy
- minimum_confidence_threshold: medium
- blocking_data_issues: charge_payment_tie_out_fail,
  legal_sensitive_eviction_status
- fallback_mode_when_partial: produce aged schedule; exclude accounts where
  charge-payment tie-out fails; flag exceptions to finance-reporting.

### capital_project_intake_and_prioritization

- required_normalized_inputs: CapexProject, EstimateLineItem, Property, Unit,
  WorkOrder
- required_derived_inputs: capex_spend_vs_plan
- optional_enrichment_inputs: capex_line_item, labor_rate, material_cost,
  construction_duration_assumption
- minimum_confidence_threshold: low
- blocking_data_issues: capex_project_scope_undefined
- fallback_mode_when_partial: rank projects by available signals; mark
  ranking confidence as `low` when cost references are absent; surface
  missing inputs.

### capex_estimate_generation

- required_normalized_inputs: CapexProject, EstimateLineItem, Property, Unit
- required_derived_inputs: capex_line_item
- optional_enrichment_inputs: labor_rate, material_cost, vendor_rate
- minimum_confidence_threshold: low
- blocking_data_issues: capex_line_item_reference_missing
- fallback_mode_when_partial: produce estimate with explicit assumption
  citations; mark gaps.

### schedule_risk_review

- required_normalized_inputs: CapexProject, ScheduleMilestone
- required_derived_inputs: schedule_variance_days, milestone_slippage_rate
- optional_enrichment_inputs: construction_duration_assumption
- minimum_confidence_threshold: medium
- blocking_data_issues: milestone_sequence_incomplete
- fallback_mode_when_partial: produce schedule risk view for milestones with
  complete data; exclude incomplete phases; flag gap.

### cost_to_complete_review

- required_normalized_inputs: CapexProject, EstimateLineItem, ChangeOrder,
  DrawRequest
- required_derived_inputs: cost_to_complete, contingency_remaining,
  contingency_burn_rate
- optional_enrichment_inputs: capex_line_item, labor_rate, material_cost
- minimum_confidence_threshold: medium
- blocking_data_issues: commitment_co_draw_reconciliation_fail
- fallback_mode_when_partial: compute cost-to-complete for reconciled
  packages; surface unreconciled packages.

### change_order_review

- required_normalized_inputs: CapexProject, BidPackage, ChangeOrder,
  DrawRequest
- required_derived_inputs: change_orders_pct_of_contract
- optional_enrichment_inputs: capex_line_item
- minimum_confidence_threshold: medium
- blocking_data_issues: change_order_scope_unmapped,
  approval_override_pending
- fallback_mode_when_partial: list change orders with confidence labels;
  isolate pending-approval items.

### draw_package_review

- required_normalized_inputs: DrawRequest, CapexProject, BidPackage,
  ChangeOrder
- required_derived_inputs: draw_cycle_time, contingency_remaining
- optional_enrichment_inputs: -
- minimum_confidence_threshold: medium
- blocking_data_issues: commitment_co_draw_reconciliation_fail,
  lien_waiver_missing
- fallback_mode_when_partial: produce draw package with missing-document
  checklist; do not route until completeness threshold met.

### bid_leveling_procurement_review

- required_normalized_inputs: CapexProject, BidPackage, Vendor,
  VendorAgreement, EstimateLineItem
- required_derived_inputs: trade_buyout_variance
- optional_enrichment_inputs: capex_line_item, labor_rate, material_cost,
  vendor_rate
- minimum_confidence_threshold: medium
- blocking_data_issues: bid_scope_not_comparable_across_bidders
- fallback_mode_when_partial: produce leveled view with non-comparable
  scope items flagged; require human sign-off to proceed.

### construction_meeting_prep_and_action_tracking

- required_normalized_inputs: CapexProject, ScheduleMilestone, ChangeOrder,
  DrawRequest
- required_derived_inputs: schedule_variance_days, cost_to_complete
- optional_enrichment_inputs: -
- minimum_confidence_threshold: low
- blocking_data_issues: action_tracker_missing
- fallback_mode_when_partial: produce agenda and open-action list from
  whatever is available; surface missing inputs at top.

### vendor_dispatch_sla_review

- required_normalized_inputs: WorkOrder, Vendor, VendorAgreement
- required_derived_inputs: service_level_adherence,
  tpm_turn_performance
- optional_enrichment_inputs: vendor_rate
- minimum_confidence_threshold: medium
- blocking_data_issues: vendor_agreement_unmapped
- fallback_mode_when_partial: produce SLA view per vendor for those with
  mapped agreements; flag unmapped vendors.

### unit_turn_make_ready

- required_normalized_inputs: WorkOrder, TurnProject, Unit, Lease,
  LeaseEvent
- required_derived_inputs: make_ready_days, unit_turn_cost
- optional_enrichment_inputs: vendor_rate, material_cost
- minimum_confidence_threshold: medium
- blocking_data_issues: turn_project_unit_link_unresolved
- fallback_mode_when_partial: produce turn dashboard for linked units; flag
  unresolved linkages.

### work_order_triage

- required_normalized_inputs: WorkOrder, Unit, Lease
- required_derived_inputs: open_work_orders, work_order_aging,
  repeat_work_order_rate
- optional_enrichment_inputs: vendor_rate
- minimum_confidence_threshold: low
- blocking_data_issues: work_order_priority_unmapped
- fallback_mode_when_partial: triage by available fields; escalate
  life-safety indicators immediately regardless of completeness.

### budget_build

- required_normalized_inputs: Property, Unit, Lease, LeaseEvent, Charge,
  Payment, BudgetLine, StaffingPlan, CapexProject
- required_derived_inputs: role_kpi_targets, occupancy_benchmark,
  concession_benchmark, payroll_assumption, staffing_model,
  utility_benchmark, capex_line_item
- optional_enrichment_inputs: market_rent_benchmark, labor_rate,
  material_cost, insurance_tax_assumption
- minimum_confidence_threshold: medium
- blocking_data_issues: unit_count_reconciliation_fail,
  staffing_plan_missing
- fallback_mode_when_partial: build budget with explicit assumption citations
  for missing references; mark lines with `confidence` labels.

### reforecast

- required_normalized_inputs: Property, Charge, Payment, BudgetLine,
  ForecastLine, VarianceExplanation, Lease, LeaseEvent
- required_derived_inputs: forecast_accuracy, role_kpi_targets
- optional_enrichment_inputs: market_rent_benchmark, occupancy_benchmark
- minimum_confidence_threshold: medium
- blocking_data_issues: ytd_actuals_missing, budget_line_to_actual_gap
- fallback_mode_when_partial: produce reforecast with annotated gaps; flag
  lines with stale inputs.

### market_rent_refresh

- required_normalized_inputs: Unit, UnitType, Lease
- required_derived_inputs: market_rent_benchmark, rent_comp
- optional_enrichment_inputs: concession_benchmark, occupancy_benchmark
- minimum_confidence_threshold: medium
- blocking_data_issues: rent_comp_scope_mismatch, stale_source
- fallback_mode_when_partial: refresh subset of units with matched comps;
  flag units without comps.

### rent_comp_intake

- required_normalized_inputs: Property, Unit, UnitType
- required_derived_inputs: rent_comp
- optional_enrichment_inputs: market_rent_benchmark
- minimum_confidence_threshold: low
- blocking_data_issues: comp_identity_unresolved, stale_source
- fallback_mode_when_partial: accept comps with higher confidence; flag
  proposed identities for human review.

## Cross-cutting observations

- Every activation that names `manual_uploads` as a required source supports
  owners of third-party-managed portfolios whose data arrives as files. The
  TPM oversight workflows deliberately depend on this connector.
- `hr_payroll` is new in this subsystem expansion. The staffing-related
  metrics (`payroll_per_unit`, `staffing_vacancy_rate_tpm`) and the
  `budget_build` workflow depend on it. Until `hr_payroll` lands, those
  activations will surface `required_source_missing` exceptions and degrade
  to `partial_mode`.
- `market_data` is treated as enrichment for most operating metrics and as
  required for the three rent-comparison metrics (`market_to_lease_gap`,
  `loss_to_lease`) and the `market_rent_refresh` and `rent_comp_intake`
  workflows.
- The TPM scorecard workflow is the densest consumer of derived inputs
  (nine), reflecting that scorecard completeness is the oversight contract.
