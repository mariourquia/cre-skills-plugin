# Reconciliation Rules: hr_payroll

Narrative description of how the hr_payroll connector reconciles against adjacent systems. Codified checks live in `reconciliation_checks.yaml`; this file is the operator-facing explanation.

## Payroll totals to GL

The sum of `payroll_line.gross_pay_cents` plus `overtime_line.ot_pay_cents` for a (property_id, pay_period_end) tuple must reconcile with the sum of `gl.actual.amount_cents` for payroll-class accounts for the same property and period. The crosswalk `master_data/gl_payroll_account_crosswalk.yaml` names which GL account codes count as payroll. Tolerance is tight (sub-penny absolute, sub-percent relative) because both feeds are authoritative accounting sources.

Common reasons for a delta:

- Benefit-loaded payroll posted to a different account family. Operator confirms the crosswalk.
- Pay-period cut-off mismatch. GL uses accounting-period boundaries; payroll uses pay-period boundaries. Reconciliation runs after the first close of the month and uses accrual entries to bridge.
- Unmapped GL account. A new payroll account appears in the chart of accounts and is not yet in the crosswalk.
- Severance or one-time pay routed through a manual JE rather than the payroll feed. Flag as a reconciling item; do not auto-heal.

## Staffing to StaffingPlan

`staffing_position.budgeted_fte` summed per property equals the sum the StaffingPlan declares for that property. When the reconciliation fails:

- A position was filled but the plan still marks it vacant. The StaffingPlan is stale; operator refreshes.
- A new property was onboarded but its positions were not yet loaded. Block landing until the plan is current.
- Role eliminations are in the plan but not yet in the HR export. Escalate to the operator; do not auto-drop.

`role_assignment.allocation_pct` summed per active assignment for a given `position_id` must not exceed 100 percent. A position over-filled by more than a small tolerance signals either a dual-person transition period (one exiting, one arriving, both flagged active) or a data-entry error. Operator-confirmable.

## HR to property master

Every active employee must resolve to a property via `property_assignment`. The resolution accepts sentinels (`shared`, `remote`, `corporate`, `floater`) alongside real `property_id` values. An active employee with no property_assignment row is a blocker.

`property_id` (when non-null and non-sentinel) must exist in the property master. Dangling `property_id` either signals a newly-onboarded property (operator adds to the master first) or a typo (correct in the source).

## Contractor classification

Contractors classified as `contractor_1099` must not carry payroll_line entries; their disbursement exposure belongs in `ap.invoice` keyed by `contractor_vendor_id`. A contractor row with payroll lines indicates a misclassification. A contractor row without a `contractor_vendor_id` indicates an incomplete AP crosswalk. Both are blockers.

## Period alignment

The connector emits data at pay-period granularity. Monthly reporting consumers roll pay periods up to a calendar month; bi-weekly pay periods can span two calendar months. Consumers that need a calendar-month view must use the allocation logic described in `reference/connectors/gl/` for cross-period accrual; this connector does not perform that split.

## Promotion gate

The landing promotes from `reference/raw/hr_payroll/` to `reference/normalized/` only when all blocker reconciliation checks pass. Warning-level failures log and allow promotion. Info-level failures report and do not gate.
