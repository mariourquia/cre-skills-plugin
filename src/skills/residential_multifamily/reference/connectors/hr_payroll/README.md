# HR / Payroll / Staffing Connector (stub, vendor-neutral)

HR, payroll, and staffing feed for the residential_multifamily subsystem. Carries employee identity stubs (PII-minimized), the StaffingPlan shape, property assignments, vacancy observations, payroll lines, overtime lines, and classification flags. Feeds StaffingPlan roll-ups and BudgetLine reconciliation via crosswalks; there is no canonical Employee object in the subsystem ontology, so every employee row is reference-only and anchors payroll and assignment records.

## Status

`status: stub`. Schema, mapping template, sample, reconciliation checks, DQ rules, and tests only. No ADP, Paylocity, Paychex, Gusto, Rippling, Workday, or generic-export adapter code lives here. A future vendor adapter forks this connector and supplies vendor-specific `mapping.yaml` entries.

## Rollout wave

Wave 2. This connector ships together with `manual_uploads` as the second batch after the wave 1 set (pms, gl, crm, ap, market_data, construction).

## Entities

| Entity | One-liner |
|---|---|
| `employee` | One row per employee stub (opaque id, no PII). |
| `staffing_position` | One row per budgeted position in the StaffingPlan. |
| `role_assignment` | One row per employee-to-position assignment, time-sliced. |
| `property_assignment` | One row per employee-to-property assignment (including shared, remote). |
| `vacancy_status` | One row per vacant position per pay-period observation. |
| `payroll_line` | One row per employee per pay period per earnings type. |
| `overtime_line` | One row per overtime event per employee per pay period. |
| `employee_vs_contractor_flag` | W2 vs 1099 classification per employee. |

## Scope

In scope: employee identity stubs, staffing plan, role and property assignments, vacancy, payroll lines, overtime, contractor classification.

Out of scope (and deliberately so):

- Benefits enrollment and medical / dental / vision elections.
- Direct deposit bank account detail.
- I-9, E-Verify, work authorization documentation.
- Tax forms (W-2, W-4, 1099 reporting).
- Performance reviews and compensation planning.
- Garnishments, child support, liens.

These are handled by the HR and payroll systems of record; the subsystem intentionally does not re-ingest them. A vendor adapter that needs to surface any of them forks this connector and declares new entities in its own `schema.yaml`.

## PII minimization

The HR and payroll worlds are PII-dense. This connector carries the minimum fields needed to run StaffingPlan reconciliation and payroll-to-GL reconciliation:

- `employee_id` is an opaque identifier (not SSN, not email).
- `display_code` is an optional non-PII handle.
- No name, SSN, DOB, home address, personal email, or phone ever lands in normalized. `mapping.yaml.dropped_source_columns` names the columns the operator must drop or hash at landing.
- Payroll lines carry gross pay in cents but no tax withholding, no benefit deductions, no bank account detail.
- Overtime and payroll lines are the only entities with cash amounts; all other entities carry metadata.

## Integration

- `hr_payroll.payroll_line` + `overtime_line` reconcile against `gl.actual` for payroll-class accounts (see `reconciliation_checks.yaml.hr_payroll_total_matches_gl`).
- `hr_payroll.staffing_position` + `role_assignment` reconcile against the StaffingPlan canonical object.
- `hr_payroll.employee_vs_contractor_flag` must cross-reference `ap.vendor` when classification is `contractor_1099`.
- `hr_payroll.property_assignment` cross-references the property master.
- `hr_payroll.overtime_line.work_order_id` (optional) cross-references `pms.work_order` for maintenance-surge attribution.

See `INGESTION.md` for the landing convention, `identity_resolution.md` for crosswalk semantics, and `reconciliation_checks.yaml` for the domain-specific QA invariants.

## Connector kind classification note

The `connector_kind` field in `manifest.yaml` is constrained by the subsystem schema enum `[pms, gl, crm, ap, market_data, construction]`. HR/payroll is not explicitly listed. This connector picks `ap` as the closest semantic match (payroll lines are disbursement-family records posted through the same approval chain as vendor payables). Flag for human review: if a future schema revision adds an `hr_payroll` kind, update `manifest.yaml` and the `INGESTION.md` source_type table.
