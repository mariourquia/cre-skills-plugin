# Connector Overview: hr_payroll

Operator-facing onboarding for the HR / payroll / staffing connector. Covers what to export, what cadence to pull at, and how to organize the files. Vendor-neutral; any payroll platform that can export tabular data per pay period can land here.

## What to export

One file per entity per landing (csv or jsonl both accepted). Every row carries the six provenance fields (`source_name`, `source_type`, `source_date`, `extracted_at`, `extractor_version`, `source_row_id`) or the landing is rejected.

| Entity | Contents |
|---|---|
| `employee` | One row per active or recently-terminated employee. Opaque id, status, hire and term dates, FT/PT flag. No PII. |
| `staffing_position` | One row per budgeted position in the staffing plan. Role code, budgeted FTE, status. |
| `role_assignment` | One row per employee-to-position assignment. Effective dates, allocation percent. |
| `property_assignment` | One row per employee-to-property assignment. Includes shared and remote cases. |
| `vacancy_status` | One row per vacant position per pay period observation. |
| `payroll_line` | One row per employee per pay period per earnings type. |
| `overtime_line` | One row per overtime event per employee per pay period. |
| `employee_vs_contractor_flag` | One row per employee with W2 vs 1099 classification. |

## Cadence

- `payroll_line` and `overtime_line`: per pay period (weekly, bi-weekly, semi-monthly, or monthly per operator's pay calendar).
- `employee`, `property_assignment`, `role_assignment`, `employee_vs_contractor_flag`: full refresh weekly at minimum; pay-period-aligned is ideal.
- `staffing_position` and `vacancy_status`: monthly full refresh, or on demand when the StaffingPlan is edited.

## Typical vendor families

All vendor-neutral. The connector works with any of the following export shapes and more:

- ADP family (ADP Workforce Now, ADP Run, ADP Vantage). Tabular exports available via scheduled report delivery.
- Paylocity family. CSV and API exports, both supported via the operator's adapter.
- Paychex family (Paychex Flex). CSV exports, report scheduling.
- Gusto family. CSV exports, API.
- Rippling family. CSV exports, API.
- Workday family. Worksheet reports, integrations via SFTP.
- Generic payroll export. Any platform that can emit columnar data for the entities above with stable ids and dates.

This connector does not encode any vendor specifics. The operator's adapter is responsible for mapping vendor column names to the source columns listed in `mapping.yaml`.

## Landing folder

```
reference/raw/hr_payroll/<YYYY>/<MM>/<source>__<as_of>.<ext>
```

Example:

```
reference/raw/hr_payroll/2026/04/sample_feed__2026-04-15.jsonl
```

## Required columns at landing

Operators must ensure the following before landing:

- The provenance fields are set on every row.
- PII columns (first_name, last_name, ssn, dob, home_address, personal_email, phone) are dropped or replaced with opaque equivalents. The connector rejects rows that still carry these columns.
- All enum-valued columns resolve to a value declared in `schema.yaml`.
- Dollar amounts are in the source's native currency (assumed USD); the `parse_currency` transform converts to cents.

## What the operator does not do

- No auth tokens or credentials live in this connector. They belong in the operator's deployment environment.
- No vendor-specific mapping lives here. The vendor adapter handles that.
- No cash figures or percentages in the prose; every concrete threshold is in `reconciliation_checks.yaml` or `dq_rules.yaml`.
- No PII augmentation. If the operator needs name-based display, use `display_code`.

## Troubleshooting

- A landing rejected with "missing required provenance field" means the row lacks one of `source_name`, `source_type`, `source_date`, `extracted_at`, `extractor_version`, or `source_row_id`.
- A landing rejected with "PII column detected" means the operator's adapter did not drop one of the dropped_source_columns.
- A landing promoted-but-warning on `hr_role_code_conforms_to_staffing_plan_roles` means the role catalog is stale; edit `master_data/role_catalog.yaml` and re-land.
- A landing blocked on `hr_payroll_total_matches_gl` means the payroll feed and GL feed disagree beyond tolerance; use `reconciliation_rules.md` as the troubleshooting runbook.
