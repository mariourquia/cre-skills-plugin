# Workflows invoked by regional_manager

| Workflow | Cadence | Trigger |
|---|---|---|
| `workflows/regional_operating_review` | Weekly, monthly, quarterly | weekly/monthly/quarterly cycle |
| `workflows/monthly_property_operating_review` | Monthly (consumes site MORs) | month-end close |
| `workflows/corrective_action_plan` | On signal | site outside band 2 weeks |
| `workflows/capital_project_intake_and_prioritization` | Quarterly | quarter-end |
| `workflows/vendor_portfolio_review` | Quarterly | quarter-end |
| `workflows/staffing_plan_review` | Quarterly | quarter-end |
| `workflows/budget_build` | Annual | budget cycle |
| `workflows/reforecast` | Quarterly | reforecast cycle |
| `workflows/policy_adherence_audit` | Monthly (sample) | month-end close |
| `workflows/delinquency_collections` | Weekly (region view) | weekly cycle |
| `workflows/market_rent_refresh` | Quarterly | quarter-end |
