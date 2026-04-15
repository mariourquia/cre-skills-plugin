# GL Derived Dependencies

Which canonical metrics, workflows, and templates depend on normalized GL data.

## Required normalized inputs

- `gl.chart_of_accounts`: must be current and include account_type for every posted account.
- `gl.account_mapping`: every posted account must be mapped to a canonical_account_slug with an effective window covering the posting period.
- `gl.actual`: period-level postings by property_id, account_id, period.
- `gl.budget`: baseline and approved scenarios for the fiscal year in scope.

## Optional enrichment inputs

- `gl.forecast`: reforecast vintages per property, account, period, as_of_date.
- `gl.variance_line`: pre-computed variance rows.
- `gl.capex_actual`: capex posting history.
- `gl.commitment`: open commitments and accruals.

## Confidence minimum

Downstream consumption requires:

- No open blocker failures on the required inputs.
- Every posted account mapped with approval_status = endorsed.
- No unresolved property-mapping gaps on gl.actual or gl.budget.
- FX rates resolved for any non-USD source rows.

## Blocking data issues

The following issues block every GL-dependent metric and workflow:

- Actual-vs-trial-balance failure.
- Budget-vs-source-header failure.
- Property-mapping missing on gl.actual or gl.budget.
- Chart-of-accounts mapping coverage gap.
- Non-USD postings without registered FX rate.
- Duplicate primary keys unresolved after dedup.

## Fallback mode when partial

When only a subset of GL entities is available:

- With only chart_of_accounts and actual (no budget), variance workflows refuse; NOI still computes.
- With only budget (no actual), budget-build workflow produces scenarios but variance reporting refuses.
- With actual and budget but no forecast, reforecast workflow refuses.
- With actual but no account_mapping, every aggregation-dependent metric refuses.

No metric silently ingests partial data.

## Canonical metrics that depend on GL

### Asset Management family

- `revenue_variance_to_budget`: requires `gl.actual`, `gl.budget` on revenue accounts.
- `expense_variance_to_budget`: requires `gl.actual`, `gl.budget` on expense accounts.
- `noi`: requires the full set of revenue and expense postings per property and period.
- `noi_margin`: derived from noi.
- `dscr`: derived from noi and debt-schedule reference.
- `debt_yield`: derived from noi and debt-schedule reference.
- `capex_spend_vs_plan`: requires `gl.capex_actual` and `gl.budget` on capex accounts.
- `renovation_yield_on_cost`: requires `gl.capex_actual` and rent-post-renovation from PMS.
- `forecast_accuracy`: requires `gl.forecast` across two vintages plus `gl.actual`.

### Property Operations family

- `payroll_per_unit`: requires `gl.actual` on payroll accounts, `pms.property` for unit count.
- `rm_per_unit`: requires `gl.actual` on repair-and-maintenance accounts.
- `utilities_per_unit`: requires `gl.actual` on utility accounts.
- `controllable_opex_per_unit`: requires `gl.actual` on controllable opex accounts per taxonomy.

### Portfolio Management family

- `same_store_noi_growth`: requires `gl.actual` across two comparable periods with same-store cohort.
- `budget_attainment`: requires `gl.actual` and `gl.budget`.

### Development and Construction family

- `capex_spend_vs_plan` and related capex metrics: require `gl.capex_actual` reconciled to construction draws.

### TPM Oversight family

- `budget_adherence_tpm`: requires `gl.actual` and `gl.budget` under the TPM reporting scope.

## Example output types

- Monthly property operating review report.
- Variance narrative per property per period.
- Annual budget build artifact.
- Reforecast vintage comparison report.
- Quarterly portfolio NOI attribution.

## Dependent workflows

- `monthly_property_operating_review`
- `monthly_asset_management_review`
- `quarterly_portfolio_review`
- `reforecast`
- `budget_build`
- `executive_operating_summary_generation`
- `third_party_manager_scorecard_review`
- `cost_to_complete_review` (for capex project-level reconciliation)
