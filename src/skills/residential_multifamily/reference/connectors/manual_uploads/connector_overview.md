# Connector Overview: manual_uploads

Operator-facing onboarding for the manual uploads connector. Covers what files to drop, where to drop them, and how to tag them so downstream workflows can consume them.

## Why this connector exists

Not every operator has full API access to their PMS, GL, or AP system, and some artifacts simply do not live in any system (bid tabs, rent surveys, approval matrices). Manual uploads are the first-class fallback. Operators can run the subsystem entirely off manual uploads if that is their reality; the connector does not treat them as second-class data.

## File-drop structure

Every landing lives under:

```
reference/raw/manual_uploads/<template_slug>/<YYYY>/<MM>/<source>__<as_of>.<ext>
```

Examples:

```
reference/raw/manual_uploads/budget_file/2026/01/sample_feed__2026-01-15.csv
reference/raw/manual_uploads/owner_report/2026/04/sample_feed__2026-04-10.md
reference/raw/manual_uploads/approval_matrix_upload/2026/04/sample_feed__2026-04-01.yaml
```

The template_slug (folder name) matches the entity slug in `schema.yaml.entities`. If the operator drops a file in the wrong folder, the landing is rejected with an error pointing to the correct folder.

## Naming convention

- `<source>` is a stable operator-chosen label (e.g., `east_region_budget`, `q1_2026_owner_pack`, `sample_feed` for stubs).
- `<as_of>` is the effective date of the file in `YYYY-MM-DD` form.
- Extension matches the `expected_file_format` declared in `schema.yaml.templates.<template>`.

## Approval tagging

For templates with an approval lifecycle (owner_report, monthly_review_pack, capex_request_upload, draw_package_upload), the operator sets `approval_status` to one of the declared enum values. Rows without approval land but do not feed approval-gated downstream workflows (investor update, draw disbursement).

## Cadence per template

| Template | Typical cadence |
|---|---|
| `budget_file` | annual, with mid-year reforecast uploads as needed |
| `forecast_file` | monthly or quarterly |
| `owner_report` | monthly |
| `vendor_bid_tab` | per-RFP, event-driven |
| `rent_survey` | monthly or quarterly |
| `market_comp_sheet` | quarterly |
| `approval_matrix_upload` | on change |
| `property_list` | on change |
| `staffing_model_upload` | annual, with mid-year updates |
| `capex_request_upload` | event-driven |
| `draw_package_upload` | per draw, event-driven |
| `monthly_review_pack` | monthly |
| `delinquency_report_upload` | monthly (only when no PMS feed exists) |
| `work_order_backlog_upload` | monthly (only when no PMS feed exists) |
| `pm_scorecard_upload` | quarterly |

## Common mistakes

- Dropping a CSV file when YAML is expected (or vice versa). Check `schema.yaml.templates.<template>.expected_file_format`.
- Renaming a column in the header row. Use the template files under `file_templates/` as the canonical header.
- Using a resident or staff name in an identifier column. Always use opaque ids.
- Landing multiple files for the same primary-key tuple without tagging `extracted_at` correctly. The tie-breaker is `latest_extracted_at_wins`; stamps must be distinguishable.
- Editing an approved owner_report in place without incrementing `source_date` and `extracted_at`. Dedup will keep the older landing.
- Putting dollar signs and percent signs in the prose fields. Keep figures in the numeric columns; prose fields are for narrative only.
- Including PII (resident full name, employee full name, addresses) in body fields. Landing may accept the row but the PII check will emit a warning.

## Template starting point

Pull the template from `file_templates/<template>_template.{csv,xlsx,md,yaml}` and edit it in place. Every template carries `status: template` and a footer pointing to the schema. The operator does not rename the template when saving the real landing.

## Sensitive template handling

`delinquency_report_upload` and `pm_scorecard_upload` are the highest-PII-risk templates. Operators must use opaque identifiers and confirm that narrative fields carry no PII. The connector's `mu_sensitive_fields_masked_if_flagged` check enforces masking when a sensitive_flag is raised.
