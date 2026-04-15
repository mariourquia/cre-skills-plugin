# Workflows invoked by coo_operations_leader

| Workflow | Cadence | Trigger |
|---|---|---|
| `workflows/weekly_exec_brief_ops` | Weekly | weekly cycle |
| `workflows/monthly_operating_decision_memo` | Monthly | month-end close |
| `workflows/quarterly_operating_review_exec` | Quarterly | quarter-end |
| `workflows/policy_change_proposal` | On decision (consumes) | DOO proposal route |
| `workflows/vendor_portfolio_review` | Quarterly (consumes) | enterprise vendor review |
| `workflows/staffing_plan_review` | Quarterly (consumes) | enterprise staffing review |
