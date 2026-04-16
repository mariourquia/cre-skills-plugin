# Identity Resolution: HR, Payroll, Property Assignment

How an employee resolves across the HR master, the payroll system, and the property management assignment layer. This connector is read-only from the subsystem's perspective; the crosswalk tables live in `reference/connectors/master_data/employee_crosswalk.yaml` (shared, not vendor-specific).

## Key surfaces

- HR master key: `employee_id` (opaque identifier, not SSN). PII is dropped or hashed at landing per `mapping.yaml.dropped_source_columns`.
- Payroll key: usually `payroll_employee_number` or `payroll_emp_id`, which may or may not match `employee_id`. The crosswalk holds the pair.
- PM assignment key: usually `property_code` + an employee reference. Crosswalk maps the payroll `employee_id` to one or more `property_id` records.

## Common failure modes

1. Shared employees across properties. Regional maintenance techs, roving leasing consultants, shared floaters all split time across two or more properties. Resolution: `property_assignment.assignment_kind = shared` with `allocation_pct`. Payroll lines are allocated per pay period by the downstream cost allocator; this connector does not perform the split.
2. Temp and contractor staff. Temp agency workers invoiced through `ap` never appear in `payroll_line`. Contractors classified as `contractor_1099` in `employee_vs_contractor_flag` must have a `contractor_vendor_id` pointing to `ap.vendor`. The reconciliation check `hr_contractor_flag_consistency` enforces this.
3. Overtime not tagged to property. Maintenance surge OT is frequently booked to a regional cost center rather than the property of origin. `overtime_line.property_id` is optional but `null_handling: escalate_missing` flags the row for operator action. Work-order-linked OT can be auto-resolved via `work_order_id -> work_order.property_id`.
4. Vacant roles budgeted but unfilled. `staffing_position.position_status = vacant` combined with `vacancy_status.vacancy_state = open_posted` or `offer_out` carries forward the budgeted FTE but no payroll line. Headcount reconciliation uses `budgeted_fte` minus `filled_fte` as the vacancy delta.
5. Contractor labor outside payroll feeds. Leasing commissions paid through AP, janitorial contracted through AP, landscaping contracted through AP all land in `ap.invoice` and are not HR data. The StaffingPlan must declare which roles are contractor-filled so the headcount reconciliation does not flag the position as an HR gap.
6. Rehire with new `employee_id`. Some HR systems issue a new opaque id on rehire. Crosswalk must resolve old and new ids to a single person identity for vacancy-to-fill velocity metrics; otherwise the new id looks like a fresh hire event.
7. Terminated-but-still-paid severance. Severance lines carry `earnings_type = severance` with `pay_period_end` after `employee.term_date`. These records are valid but should not count toward active headcount.

## Crosswalk pointer

See `reference/connectors/master_data/employee_crosswalk.yaml` for the canonical crosswalk schema. It holds `(hr_employee_id, payroll_employee_number, property_code, effective_from, effective_to, notes)` tuples and is a shared artifact; no vendor code lives there.

## Review gate

Any row that fails identity resolution (missing crosswalk, dangling FK, classification gap) is routed to `reference/raw/hr_payroll/_rejected/<YYYY>/<MM>/` with a reason. Blocker reconciliations prevent promotion to normalized until the crosswalk is updated.
