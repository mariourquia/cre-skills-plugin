# GL Reconciliation Rules

Narrative describing how reconciliation in the GL domain works.

## Reconciliation scope

The GL is the financial system of record for actuals, budgets, forecasts, capex postings, and commitments. It reconciles with:

- The source accounting system's trial balance (internal reconciliation).
- The budget system header totals (where budget arrives as a separate feed).
- The PMS charge and payment feeds (revenue and cash timing).
- The AP invoice and payment-status feeds (open payable balance).
- The construction connector's commitments and draws (capex spend).
- Payroll feeds (where payroll lands as a separate feed, it reconciles to GL salary expense).

## Totals that must agree

### Budget versus source budget header

For each property_id, period, and scenario, the sum of `gl_budget.amount_cents` equals the source budget header total. Tolerance is penny-level rounding as declared in `gl/manifest.yaml`. Enforced by `gl_budget_actual_alignment`.

### Actual versus source trial balance

For each property_id and period, the sum of `gl_actual.amount_cents` equals the source trial balance total. Tolerance is penny-level rounding. Enforced by `gl_budget_actual_alignment`.

### AP versus GL payable account

For each property_id and period, the sum of open AP invoice balance equals the GL `ap_payable` canonical_account_slug balance at period close. Tolerance is penny-level. Enforced cross-domain by `ap_ap_to_gl_payable_alignment`.

### PMS charges versus GL revenue

For each property_id and period, the sum of `pms.charge` rows for rental-income charge_types equals the GL `rental_income` canonical_account_slug balance. Tolerance is the cash-versus-accrual timing window declared in `gl/manifest.yaml`.

### PMS payments versus GL cash receipts

For each property_id and period, the sum of `pms.payment.amount_cents` equals the GL cash-receipts postings for the period. Tolerance is zero for monthly totals; intra-month timing differences are allowed within the cash-clearing window.

### Capex actual versus construction draws

For each property_id and capex_project_id, the sum of `gl_capex_actual.amount_cents` reconciles to the sum of `construction.draw_request` amounts with approval_status in (approved, funded) for the same project. Tolerance is zero at project completion; intermediate tolerances depend on retention and lien-waiver timing declared in the construction manifest.

### Consolidated portfolio versus property-level sum

For each period and canonical_account_slug, the consolidated portfolio sum equals the sum of individual property gl_actual rows within tolerance. Enforced by `gl_inter_property_consolidation_aligned`.

## Tolerances

| Reconciliation | Absolute tolerance | Relative tolerance |
|---|---|---|
| Budget vs source | 0 | referenced from gl/manifest.yaml penny-rounding |
| Actual vs source | 0 | referenced from gl/manifest.yaml penny-rounding |
| AP vs GL payable | 0 | referenced from gl/manifest.yaml penny-rounding |
| PMS charges vs GL revenue | within accrual timing window | referenced from gl/manifest.yaml |
| Capex actual vs construction draws | 0 at project close | retention and lien-waiver dependent intra-period |
| Portfolio consolidation | 0 | referenced from gl/manifest.yaml penny-rounding |

All non-zero tolerance values live in the connector manifest. No numeric thresholds appear in this document.

## Escalation triggers

- A blocker reconciliation failure holds the landing. If actual-vs-trial-balance fails, no period can close in the derived reports until reconciled.
- AP-GL variance beyond tolerance escalates to the compliance_risk audience because audit trail integrity is at stake.
- Capex-vs-draws variance escalates to the asset_mgmt and construction-project-command-center audiences; draws should not be approved with a variance outstanding.
- Portfolio-versus-property-sum variance escalates to the executive audience because consolidated reports are LP-facing.

## Cross-domain reconciliation dependencies

The GL reconciliation_report.json is the keystone for month-close workflows. A blocker here prevents monthly_property_operating_review, variance-narrative-generator, quarterly_portfolio_review, and reforecast from running. The chain is enforced by `tests/test_connector_contracts.py`.
