# Change Log — acquisition_handoff

## 0.1.0 — 2026-04-15

- Pack initialized. Wave-5 introduction. Authored as part of stack-specific
  operationalization of `reference/connectors/_core/stack_wave4/lifecycle_handoffs.md`
  Handoff 1 (Dealpath -> approved acquisition) and Handoff 3 (Dealpath/Intacct ->
  AppFolio property setup).
- Handoff checklist, AppFolio property setup verification, Intacct entity dim
  verification, vendor master rationalization via
  `master_data/identity_resolution_framework.md`, opening rent roll reconciliation,
  PMA execution check (TPM), lender reporting registration, and data-platform
  crosswalk row creation authored.
- Proposed metrics introduced: `handoff_completeness_score`, `handoff_lag_days`,
  `vendor_rationalization_count`, `opening_rent_roll_reconciliation_variance`,
  `pma_execution_lag_days`, `crosswalk_row_creation_lag_days`. To be lifted into
  `_core/metrics.md` before promotion beyond draft.
- Approval gates: row 7 (handoff lag), row 14 (lender registration), row 17
  (missing required approver / insurance gap), row 19 (PMA execution, vendor
  master conflict).
- Blocking issue ids cited: `dp_handoff_lag`, `dp_one_deal_multiple_projects`.
- Status: draft.
