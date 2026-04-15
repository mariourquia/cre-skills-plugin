# Workflows invoked by portfolio_manager

| Workflow | Cadence | Trigger |
|---|---|---|
| `workflows/monthly_portfolio_review` | Monthly | month-end close |
| `workflows/quarterly_portfolio_review` | Quarterly | quarter-end |
| `workflows/hold_sell_refi_screen` | Quarterly (consumes AM output) | quarter-end or market signal |
| `workflows/debt_covenant_check` | Monthly (portfolio view) | lender compliance window |
| `workflows/investor_reporting_package` | Quarterly, annual | investor calendar |
| `workflows/concentration_monitoring` | Monthly | month-end |
| `workflows/capital_allocation_memo` | Quarterly or on pipeline event | capital pipeline signal |
| `workflows/business_plan_refresh` | Annual (portfolio layer) | annual cycle |
| `workflows/budget_build` | Annual (portfolio roll-up) | budget cycle |
| `workflows/reforecast` | Quarterly (portfolio roll-up) | reforecast cycle |
| `workflows/same_store_cohort_refresh` | Annual + event-triggered | portfolio changes |
