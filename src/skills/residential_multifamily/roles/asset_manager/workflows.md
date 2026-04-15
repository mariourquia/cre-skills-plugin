# Workflows invoked by asset_manager

| Workflow | Cadence | Trigger |
|---|---|---|
| `workflows/monthly_asset_review` | Monthly | month-end close |
| `workflows/quarterly_asset_review` | Quarterly | quarter-end |
| `workflows/business_plan_refresh` | Annual + event-triggered | annual cycle or material event |
| `workflows/hold_sell_refi_screen` | Quarterly | quarter-end or market signal |
| `workflows/debt_covenant_check` | Monthly | lender compliance window |
| `workflows/capital_project_intake_and_prioritization` | Quarterly | quarter-end |
| `workflows/renovation_program_yield_review` | Quarterly (if applicable) | renovation tranche completion |
| `workflows/lender_compliance_package` | Monthly / quarterly | lender calendar |
| `workflows/investor_reporting_package` | Monthly / quarterly | investor calendar |
| `workflows/budget_build` | Annual | budget cycle |
| `workflows/reforecast` | Quarterly | reforecast cycle |
| `workflows/property_tax_appeal_decision` | Annual | assessment notice |
| `workflows/insurance_program_review` | Annual + claim events | renewal window or claim |
| `workflows/pma_amendment` | As needed | PMA change |
| `workflows/draw_request_review` | Per draw | draw request created |
| `workflows/tpm_scorecard_review` | Monthly (TPM assets) | TPM reporting window |
| `workflows/market_rent_refresh` | Quarterly | quarter-end |
