# Workflows invoked by director_of_operations

| Workflow | Cadence | Trigger |
|---|---|---|
| `workflows/regional_operating_review` | Weekly (consumes) | weekly cycle |
| `workflows/monthly_property_operating_review` | Monthly (consumes region rollups) | month-end close |
| `workflows/policy_change_proposal` | On proposal | policy drift / regulatory change |
| `workflows/vendor_portfolio_review` | Quarterly (enterprise) | quarter-end |
| `workflows/staffing_plan_review` | Quarterly (enterprise) | quarter-end |
| `workflows/training_plan_execution` | Monthly / quarterly | training calendar |
| `workflows/policy_adherence_audit` | Monthly (enterprise sample) | month-end |
| `workflows/reforecast` | Quarterly | reforecast cycle |
| `workflows/budget_build` | Annual | budget cycle |
