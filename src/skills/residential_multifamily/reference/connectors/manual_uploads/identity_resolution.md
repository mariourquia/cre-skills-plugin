# Identity Resolution: Manual Uploads

How manual-upload templates crosswalk to existing master data. Manual uploads are a first-class intake channel; the records they carry must resolve to the same canonical identifiers as system feeds or they cannot be joined.

## Property crosswalk

Every template that carries `property_id` resolves to the property master. The property master is canonical (not operator-specific); a `property_id` value in a manual upload must either match a property master row or be part of a property_list upload that is itself creating the master row.

Resolution order:

1. If the template is `property_list`, this is the source of truth. New `property_id` values declared here are acceptable.
2. For every other template, `property_id` must exist in the property master at landing time. A dangling value blocks promotion.
3. Sentinels (`shared`, `remote`, `corporate`, `portfolio`) are permitted where the property scope is intentionally unscoped.

## Vendor crosswalk

`vendor_bid_tab.vendor_id` must exist in the AP vendor master at landing. A dangling vendor_id either indicates a new bidder not yet set up in AP (operator adds to vendor master first) or a typo. New bidders must be onboarded through `ap.vendor` before a bid tab is landed; the connector does not auto-create vendor rows.

## Project crosswalk

`draw_package_upload.project_id` and `capex_request_upload` (through the GL capex account code) must crosswalk to the construction project master. The crosswalk lives in `master_data/project_crosswalk.yaml`.

## Employee crosswalk

`pm_scorecard_upload.employee_id` must exist in `hr_payroll.employee`. Manual-upload scorecards cannot reference an employee who does not exist in the HR master.

## Resident crosswalk

`delinquency_report_upload.resident_account_id` must exist in `pms.lease` (as `resident_account_id`). Dangling values block promotion.

## GL account crosswalk

`budget_file.account_code`, `forecast_file.account_code`, and `capex_request_upload` (category mapping) all resolve to the chart of accounts. Unknown account codes block promotion; operator adds the account to `gl.chart_of_accounts` first.

## Document versus data

Some templates (owner_report, monthly_review_pack, draw_package_upload) are narrative documents rather than structured data. Their rows are parsed sections, not transactional records. The primary-key tuple (`property_id` + `report_period` + `section_key`) ensures each section is uniquely identified even though the body is free-form markdown.

## Common failure modes

- Operator lands a budget file before the property_list is up to date. Blocks on property crosswalk.
- Operator lands a bid tab with a vendor id that was issued locally in a spreadsheet rather than through AP. Blocks on vendor crosswalk.
- Operator lands a PM scorecard with an employee id that has been deactivated. Warning; check the HR feed for a rehire transition.
- Operator edits the template header line and drops a required column. Blocker at file-format check.
