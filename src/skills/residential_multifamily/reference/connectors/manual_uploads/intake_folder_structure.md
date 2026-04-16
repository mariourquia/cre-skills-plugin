# Intake Folder Structure

Canonical drop-zone layout for the manual_uploads connector. Every landed file must conform to this structure or the landing helper rejects it with a readable error.

## Base pattern

```
reference/raw/manual_uploads/<template_slug>/<YYYY>/<MM>/<source>__<as_of>.<ext>
```

Where:

- `<template_slug>` matches an entity slug in `schema.yaml.entities`.
- `<YYYY>` is the four-digit year of the `as_of` date.
- `<MM>` is the two-digit month (01-12) of the `as_of` date.
- `<source>` is a stable operator-chosen source label, snake_case.
- `<as_of>` is the effective date of the file in `YYYY-MM-DD` form.
- `<ext>` matches `expected_file_format` for the template (csv | xlsx | pdf | md | yaml).

## Per-template folder examples

```
reference/raw/manual_uploads/budget_file/2026/01/east_region_budget__2026-01-15.csv
reference/raw/manual_uploads/forecast_file/2026/04/east_region_forecast__2026-04-10.csv
reference/raw/manual_uploads/owner_report/2026/03/quarterly_owner_pack__2026-03-31.md
reference/raw/manual_uploads/vendor_bid_tab/2026/04/rfp_001_bid_tab__2026-04-05.xlsx
reference/raw/manual_uploads/rent_survey/2026/04/submarket_survey__2026-04-01.csv
reference/raw/manual_uploads/market_comp_sheet/2026/03/comp_sales_q1__2026-03-31.csv
reference/raw/manual_uploads/approval_matrix_upload/2026/04/approval_matrix_v3__2026-04-01.yaml
reference/raw/manual_uploads/property_list/2026/04/portfolio_list__2026-04-01.csv
reference/raw/manual_uploads/staffing_model_upload/2026/01/annual_staffing_model__2026-01-15.csv
reference/raw/manual_uploads/capex_request_upload/2026/04/capex_req_sample__2026-04-01.yaml
reference/raw/manual_uploads/draw_package_upload/2026/04/draw_3_proj_sample__2026-04-05.md
reference/raw/manual_uploads/monthly_review_pack/2026/03/monthly_review__2026-03-31.md
reference/raw/manual_uploads/delinquency_report_upload/2026/03/delinquency_march__2026-04-01.csv
reference/raw/manual_uploads/work_order_backlog_upload/2026/03/wo_backlog_march__2026-04-01.csv
reference/raw/manual_uploads/pm_scorecard_upload/2026/04/pm_scorecard_q1__2026-04-10.csv
```

## Provenance filename pattern

The filename itself is a provenance artifact. The landing helper extracts the three tokens:

- `<source>` -> provenance `source_name` for every row in the file.
- `<as_of>` -> provenance `source_date` for every row in the file.
- file path mtime -> provenance `extracted_at`.

For templates where the file contains multiple rows (CSV, XLSX), the landing helper stamps these provenance fields onto every row unless the file itself already carries them at the row level.

For narrative templates (markdown, PDF), the landing helper parses the document into sections and stamps provenance onto each parsed section.

## Rejected landings

Files that fail to match the pattern land in:

```
reference/raw/manual_uploads/_rejected/<YYYY>/<MM>/<source>__<as_of>.<ext>.rejected.log
```

The `.rejected.log` sidecar names the template that was expected (if a template_slug can be inferred), the observed deviation (wrong extension, missing header column, malformed YAML), and a pointer to the remediation step.

## Forward-compatible layout

When a new template is added to `schema.yaml.entities` and `schema.yaml.templates`, a new folder is created under `reference/raw/manual_uploads/<new_template_slug>/`. No existing folders are renamed; templates are additive.
