# Workflows invoked by cfo_finance_leader

| Workflow | Cadence | Trigger |
|---|---|---|
| `workflows/weekly_exec_brief_finance` | Weekly (consumes) | weekly cycle |
| `workflows/monthly_finance_decision_memo` | Monthly | month-end close |
| `workflows/quarterly_finance_review_exec` | Quarterly | quarter-end |
| `workflows/covenant_cushion_memo` | Monthly (consumes) | covenant calendar |
| `workflows/lender_compliance_package` | Monthly / quarterly (sign-off) | lender calendar |
| `workflows/investor_reporting_package` | Monthly / quarterly / annual (sign-off) | investor calendar |
| `workflows/reforecast` | Quarterly (consumes) | reforecast cycle |
| `workflows/budget_build` | Annual (sign-off) | budget cycle |
| `workflows/fund_audit_status` | Annual / as needed | audit cycle |
| `workflows/accounting_policy_change` | On proposal | policy change |
| `workflows/refi_recap_decision` | On trigger | refi / recap need |
