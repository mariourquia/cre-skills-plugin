# Derived Dependencies: hr_payroll -> canonical metrics

Which canonical metrics and workflows depend on normalized `hr_payroll` data. Metric slugs reference `_core/metrics.md` where they exist; anything not yet canonicalized is tagged `derived_only, proposed addition, not yet canonicalized`.

## Core payroll metrics

- `payroll_per_unit` - sum of `payroll_line.gross_pay_cents` + `overtime_line.ot_pay_cents` per property per period, divided by `property.unit_count_rentable`. Feeds variance narratives and budget benchmarking.
- `payroll_per_occupied_unit` - same numerator, divided by count of occupied units for the period. `derived_only, proposed addition, not yet canonicalized`.
- `payroll_pct_of_opex` - payroll sum divided by total operating expense from `gl.actual`. `derived_only, proposed addition, not yet canonicalized`.
- `overtime_ratio` - sum of `overtime_line.ot_pay_cents` divided by sum of `payroll_line.gross_pay_cents` (both same period). Threshold alerting on abnormal OT spikes.
- `overtime_hours_ratio` - sum of `overtime_line.ot_hours` divided by sum of `payroll_line.regular_hours`. `derived_only, proposed addition, not yet canonicalized`.

## Staffing and vacancy metrics

- `staffing_coverage_ratio` - filled FTE divided by budgeted FTE for a property. Filled FTE comes from `role_assignment.allocation_pct` summed across active rows; budgeted comes from `staffing_position.budgeted_fte`.
- `vacancy_ratio` - count of `staffing_position` rows with `position_status = vacant` divided by total positions. Complements `staffing_coverage_ratio`.
- `time_to_fill_days` - average `days_vacant` at the moment a vacancy transitions to `filled_effective_next_period`. `derived_only, proposed addition, not yet canonicalized`.
- `headcount_budget_variance` - `budgeted_fte - filled_fte` per property per period. Feeds annual budget engine variance narrative.

## Workforce composition metrics

- `contractor_ratio` - count of employees classified `contractor_1099` divided by total active employees. `derived_only, proposed addition, not yet canonicalized`.
- `ft_pt_mix` - count of employees by `ft_pt_flag`. Feeds staffing plan review.
- `turnover_rate` - count of terminations in period divided by average headcount. `derived_only, proposed addition, not yet canonicalized`.
- `tenure_distribution` - distribution of `employee.hire_date` to-now across active employees. Informational only.

## Cross-connector reconciliation metrics

- `payroll_gl_reconciliation_delta` - absolute difference between payroll sum and gl.actual payroll-account sum per property per period. The corresponding qa check is `hr_payroll_total_matches_gl`.
- `staffing_plan_vs_actual_payroll_delta` - delta between budgeted payroll (implied by `staffing_position.budgeted_fte * role-level pay band target`) and actual payroll. `derived_only, proposed addition, not yet canonicalized`. Depends on pay_band reference data not yet canonicalized.

## Workflow dependencies

- `annual_budget_engine` - depends on staffing_position + payroll_line history.
- `variance_narrative_generator` - depends on payroll_line + gl.actual for month-over-month explanation.
- `property_performance_dashboard` - payroll_per_unit and overtime_ratio panels.
- `tenant_retention_engine` - indirectly: property operations staffing levels affect resident experience scores.
- `work_order_triage` - overtime_line.work_order_id links maintenance surge to WO throughput.
- `capex_prioritizer` - staffing constraints on capex execution (shared maintenance FTE).

## Stubs flagged for human review

- Benefits load factor. Some operators add benefits-loaded payroll to the same GL account as cash comp; others post benefits to a separate family. The reconciliation tolerance of `hr_payroll_total_matches_gl` assumes benefits post to a separate account family. If the operator posts benefits into the same account as payroll, update `master_data/gl_payroll_account_crosswalk.yaml` accordingly.
- Pay band reference data is not yet canonicalized. Budgeted payroll cannot be synthesized from staffing_position alone without a pay_band -> cents_per_period mapping. Proposed addition.
