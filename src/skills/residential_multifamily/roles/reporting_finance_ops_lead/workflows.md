# Workflows invoked by reporting_finance_ops_lead

| Workflow | Cadence | Trigger |
|---|---|---|
| `workflows/month_end_close` | Monthly | close calendar |
| `workflows/variance_reporting_pack` | Monthly | close complete |
| `workflows/covenant_cushion_memo` | Monthly per loan | covenant calendar |
| `workflows/lender_compliance_package` | Monthly / quarterly | lender calendar |
| `workflows/investor_reporting_package` | Monthly / quarterly / annual | investor calendar |
| `workflows/reforecast` | Quarterly | reforecast cycle |
| `workflows/budget_build` | Annual | budget cycle |
| `workflows/forecast_accuracy_measurement` | Monthly | close complete |
| `workflows/reference_update` | On proposal | finance-domain library drift |
| `workflows/same_store_cohort_refresh` | Annual + event | portfolio change |
| `workflows/draw_request_cycle` | Per draw | draw calendar |
