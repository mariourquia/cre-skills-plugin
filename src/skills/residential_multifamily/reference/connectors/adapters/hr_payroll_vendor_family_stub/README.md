# HR/Payroll Vendor Family Stub

Adapter id: `hr_payroll_vendor_family_stub`
Vendor family: `generic_hr_payroll_stub`
Connector domain: `hr_payroll`
Status: `stub`

## Scope

Stub overlay on the canonical `hr_payroll` connector at
`../../hr_payroll/`. Documents employee identity (PII-minimized), role
coding, property assignment, pay-period accounting, and contractor
flagging conventions commonly seen across HR and payroll platforms.
Canonical `hr_payroll` schema remains the contract.

Orientation examples (not endorsements, not in file paths): platforms
commonly encountered include ADP, Workday, Paychex, Paycom, Paylocity,
Rippling, and Gusto families, plus agency-staffing intake files that
arrive separately. Operators fork this stub to an internal codename.

## Assumed source objects

- `employee` (PII-minimized identity anchor)
- `staffing_position` (budgeted positions per property)
- `role_assignment` (which employee holds which position)
- `property_assignment` (allocation split across properties)
- `vacancy_status` (open / filled / pending)
- `payroll_line` (per-pay-period earnings)
- `overtime_line` (OT earnings, ideally tagged to property)
- `employee_vs_contractor_flag` (W-2 vs 1099 distinction)

## Raw payload naming

- `payroll_register_<yyyymmdd>.csv`
- `staffing_roster_<yyyymmdd>.csv`
- `agency_hours_<yyyymmdd>.csv`

Synthetic example at `example_raw_payload.jsonl`, `status: sample`.

## Mapping template usage

Apply `mapping_template.yaml` over the canonical hr_payroll mapping at
`../../hr_payroll/` references. Canonical contract wins on conflict.
PII minimization is explicit: `employee_number` and `role_code` carry
through, names and tax ids do not.

## Known limitations

- Stubs carry synthetic data only.
- Temp staff and contractor labor frequently live outside the main
  payroll feed and require separate intake paths.
- PII minimization rules may be stricter than the defaults here
  depending on the operator's privacy posture; tighten rather than
  relax.

## Common gotchas

- Employees shared across multiple properties require an allocation
  split. Do not double-count `gross_pay`. Allocation lives in the
  property_assignment table.
- Temp staff and agency workers typically outside the main payroll
  feed. Maintain a separate intake and reconcile at period close.
- Overtime not tagged to property. Expect manual allocation via the
  staffing_position table.
- Vacant roles that are budgeted appear in staffing_position but not
  in payroll. Do not infer spend from position alone.
- Contractor labor sits in AP rather than HR. Join via the
  `vendor_master_crosswalk` to reconcile total labor spend.
- PII minimization required. Use `employee_number` and `role_code` as
  canonical identifiers. Do not propagate names, SSN, tax ids, or
  bank-account numbers through the adapter.
- Pay-period-end dates vary (weekly, biweekly, semimonthly). Always
  carry `pay_period_end` explicitly.
- Employees who change role mid-period show up on two lines. Preserve
  both and reconcile at close.
- Property assignment sometimes only at cost-center level. Map
  cost-center to property via the crosswalk.
