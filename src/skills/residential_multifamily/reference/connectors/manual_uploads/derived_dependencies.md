# Derived Dependencies: manual_uploads -> workflows

Which subsystem workflows depend on manual_uploads data when system integration is absent. Manual uploads are the intake fallback whenever a PMS, GL, or AP system cannot be integrated directly (operator lacks API access, vendor is cheap, data simply does not live in any system).

## Budget and forecast workflows

- `annual_budget_engine` consumes `budget_file` to build property-level budgets. When no GL feed exists, `budget_file` is the authoritative budget source and feeds the budget vs actual dashboard via a `gl.budget` equivalence.
- `variance_narrative_generator` consumes `budget_file` + `forecast_file` + a GL actuals feed (or a GL-substitute landed through the GL connector). Manual uploads fill the budget side; actuals still require a real GL feed or manual journal entry drops.
- `quarterly_investor_update` consumes `forecast_file` + `owner_report` + `monthly_review_pack`.

## Owner and investor reporting

- `quarterly_investor_update` depends on `owner_report.approval_status = approved` and `monthly_review_pack.approval_status = approved`.
- `property_performance_dashboard` consumes `monthly_review_pack` sections, filtered to approved.
- `investor_lifecycle_manager` consumes `owner_report` for LP communication drafts.

## Bid leveling and vendor workflows

- `construction_procurement_contracts_engine` consumes `vendor_bid_tab` to run bid leveling and produce award recommendations.
- `vendor_invoice_validator` uses `approval_matrix_upload` to determine approver routing for vendor invoices.

## Market and comp workflows

- `comp_snapshot` consumes `rent_survey` + `market_comp_sheet` when no market data vendor feed is available. Manual uploads substitute for `market_data.rent_comp` and `market_data.sale_comp`.
- `rent_optimization_planner` consumes `rent_survey` for effective rent benchmarking.
- `market_memo_generator` consumes `market_comp_sheet` for transaction-backed narrative.

## Capex workflows

- `capex_prioritizer` consumes `capex_request_upload` to rank requests.
- `construction_project_command_center` consumes `draw_package_upload` and `vendor_bid_tab` for project-level reviews.
- `construction_budget_gc_analyzer` consumes bid tabs and capex request amounts for benchmarking.

## Operations workflows

- `tenant_delinquency_workout` consumes `delinquency_report_upload` when no PMS delinquency feed exists.
- `work_order_triage` consumes `work_order_backlog_upload` for triage when no PMS work order feed exists.
- `noi_sprint_plan` consumes `pm_scorecard_upload` for performance context.
- `property_performance_dashboard` consumes `pm_scorecard_upload` for the staffing and performance panel.

## Portfolio and master data workflows

- `property_list` is the bootstrap file for the property master when the operator has no centralized system. Every downstream connector that references `property_id` depends on this file being complete.
- `staffing_model_upload` bootstraps the StaffingPlan when `hr_payroll.staffing_position` is not yet available. It can be deprecated once the HR feed stabilizes.
- `approval_matrix_upload` bootstraps approval gating for AP, capex, and leasing workflows.

## Missing-doc matrix

Manual uploads are often the operator's only evidence of certain artifacts. When an operator lands a monthly_review_pack missing a section, the `tailoring/MISSING_DOC_MATRIX.md` picks up the gap and routes the operator to the right template. Manual uploads are the fallback channel every time the matrix resolves a miss.
