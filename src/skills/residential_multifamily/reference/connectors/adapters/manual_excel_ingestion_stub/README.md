# Manual Excel Ingestion Stub

Adapter id: `manual_excel_ingestion_stub`
Vendor family: `excel_file_stub`
Connector domain: `manual_uploads`
Status: `stub`

## Scope

Stub overlay on the canonical `manual_uploads` connector at
`../../manual_uploads/`, specialized for spreadsheet-based inbound.
Documents budget-sheet, variance-report, and owner-report page
conventions and the common parsing hazards that spreadsheets introduce.
Canonical `manual_uploads` schema remains the contract.

Orientation examples (not endorsements, not in file paths): budget
templates, monthly variance packages, and quarterly owner reports are
commonly authored in Excel, Google Sheets, or Numbers. Operators
typically converge on a shared template and revise it each fiscal year.

## Assumed source objects

- `budget_line` (row per account per property per period)
- `forecast_line` (reforecast rows with version tag)
- `variance_explanation` (narrative rows joined on account and period)

## Raw payload naming

- `<property>_budget_<fy>.xlsx`
- `<property>_variance_<yyyymm>.xlsx`
- `<portfolio>_owner_report_<yyyymm>.xlsx`

The synthetic example in this directory is stored as JSON Lines with
one row per notional cell batch, simulating a post-parse state.

## Mapping template usage

Apply `mapping_template.yaml` on top of the canonical manual_uploads
mapping at `../../manual_uploads/mapping.yaml`. Canonical mapping wins
on conflict. Excel parsing upstream of this adapter is the operator's
responsibility; the adapter assumes a row-normalized JSONL landing
shape.

## Known limitations

- Spreadsheets are inherently low-structure. The hints below cover the
  most common hazards, not every variation.
- Macros, external links, and embedded charts require upstream
  preprocessing before this adapter is useful.
- Template drift across properties is the single largest source of
  ingestion breakage.

## Common gotchas

- Merged cells break row-oriented parsers. Unmerge before parse and
  carry the anchor value down the column.
- Blank rows that visually separate sections are not empty from a
  parser's standpoint. Preserve section boundaries via the
  `report_section` anchor.
- Column headers vary across properties (`Jan` vs `January` vs
  `Period 1`). Normalize through an alias table.
- Embedded charts and images can cause parsers to skip rows silently.
  Use sheet-level bounds rather than cell-level walks.
- Macros that transform values at open-time. Parse the values-only
  snapshot, never the formula snapshot, unless the formulas are the
  primary artifact.
- Multi-sheet references and external links. Resolve them before
  ingest or flag the workbook.
- Template drift between properties. Track the central template
  version in `budget_version` and fail-loud when version tags do not
  match.
- Row categories nested by indentation rather than by hierarchy
  columns. Infer hierarchy from indentation depth, not only row order.
- Owner-report page sections (portfolio roll-up, property detail,
  variance narrative) carry distinct row layouts. Route by section.
- Negative numbers represented with trailing minus, parentheses, or
  red font only. Normalize sign early; red-font is not machine-readable
  without style parsing.
