# Excel Market Surveys Adapter

Adapter id: `excel_market_surveys`
Vendor family: `excel_benchmark_family`
Connector domain: `market_data` (primary) + `manual_uploads` (secondary)
Status: `stub` (adapter lifecycle) / `active` (operational intake)
Rollout wave: `wave_4`

## Why Excel is a first-class production input

Market surveys, analyst benchmark packs, and operator spreadsheets are
already in production use every week across every residential multifamily
platform this skill supports. Rent comp refreshes, concession trackers,
capex cost libraries, labor rate sheets, material price sheets, vendor rate
cards, staffing benchmarks, and schedule assumption sheets live in Excel
because analysts compose, revise, and approve them in Excel. Treating these
files as "temporary hacks" is wrong: they are the canonical form of the
benchmark data until an API-fed equivalent exists, and for some categories
(analyst judgment calls, asset-specific comp packs, market commentary) an
API equivalent is never coming.

This adapter frames the contract that governs those files:

- A named intake manifest lists every file family, its drop location, its
  cadence, its filename pattern, its template schema, and its reviewer role
- A template schema per file family declares columns, required fields,
  validation rules, and permitted values, all cross-referenced to the
  canonical normalized schemas at `../../../normalized/schemas/`
- A field mapping per file family declares column-level mapping
- DQ rules enforce schema conformance, staleness, outlier detection,
  submarket tag validity, duplicate detection, unit-type comparability,
  segment mismatch (luxury-in-middle-market contamination), analyst-formula
  detection, merged-cell artifacts, provenance completeness, and reviewer
  sign-off presence for high-impact files
- Reconciliation rules cross-check Excel benchmarks against operational
  reality (actual payroll, actual invoices, actual turn spending,
  Procore estimates and commitments, AppFolio property submarket tags)
- A sample_valid library and a sample_invalid library document what
  conformant rows look like and what errors look like

Excel benchmark packs remain the contract until every category has a
non-Excel equivalent. For several categories, the Excel workbook is the
permanent canonical form.

## Provenance controls

Every record carries a provenance envelope:

- `source_file` (workbook filename as dropped)
- `sheet_tab` (worksheet name within the workbook)
- `as_of_date` (the benchmark effective date, not the file-drop date)
- `analyst_name` (who composed the row)
- `reviewer` (who signed off)
- `extracted_at` (when the row was parsed)
- `row_id` (stable identifier across re-extractions of the same workbook)

Hidden tabs are enumerated and tagged `sheet_tab` the same way visible tabs
are. Analyst formula cells are rewritten to the value snapshot at extract
time; the formula itself is logged for audit but not propagated downstream.

## Staleness controls

Every file family declares a `staleness_threshold_days` in
`intake_manifest.yaml`. Downstream workflows refuse to consume a file that
is older than its staleness threshold:

- Rent comp weekly: tight threshold (stale comps produce misleading
  market-to-lease gap signals)
- Concession tracker monthly: medium threshold (monthly churn is normal)
- Capex cost library quarterly: moderate threshold (material costs drift
  but quarterly cadence is enough unless a supply shock triggers a
  mid-quarter refresh)
- Labor rate sheet quarterly: moderate threshold (wage adjustments are
  quarterly at most)
- Schedule assumption sheet: slow cadence (annual or on-event)
- Market commentary file: on-event (attached to a narrative, not a
  periodic refresh)

Numeric thresholds live in each template schema file under
`template_schemas/`, never inline in prose.

## Outlier handling

Outlier detection uses a z-score or percent-from-median band. The tolerance
bands are declared in the segment overlays at
`overlays/segments/<segment>/overlay.yaml` and referenced by dq_rules.yaml.
Outlier rows are flagged but not dropped; a manual reviewer either
reclassifies the row (e.g., reclassify a luxury comp that ended up in the
middle_market sheet) or confirms the outlier with a paired source note.

## Manual reviewer model

Every file family declares a `required_reviewer` role in
`intake_manifest.yaml`. The reviewer role reflects the accountability for
the file content:

- Rent comp weekly: research_analyst + regional_ops_director cross-sign
- Concession tracker monthly: leasing_director
- Market survey workbook: research_analyst
- Analyst benchmark pack: investments_director
- Staffing benchmark: hr_director + regional_ops_director
- Labor rate sheet: capital_projects_team + hr_director (cross-market)
- Material price sheet: capital_projects_team
- Vendor rate card: procurement_lead
- Turn cost library: regional_ops_director
- Capex cost library: development_director + capital_projects_team cross-sign
- Schedule assumption sheet: development_director
- Market commentary file: investments_director

Reviewer sign-off presence is a DQ blocker for high-impact files (capex
cost library, labor rate sheet) and a DQ warning for routine refreshes
(rent comp weekly, concession tracker monthly).

## Layout

- `manifest.yaml` - adapter manifest
- `intake_manifest.yaml` - every file family with drop location, cadence,
  filename pattern, template schema path, reviewer role, staleness threshold
- `template_schemas/` - one YAML schema per file family
- `normalized_contract.yaml` - how each file family maps to canonical
  reference files and ontology objects
- `field_mapping.yaml` - column-level mapping per file family
- `sample_valid/` - JSONL "as if converted from Excel" samples per family
- `sample_invalid/` - JSONL samples with known problems per family
- `dq_rules.yaml` - DQ rules spanning schema, staleness, outliers,
  duplicates, comparability, segment mismatch, provenance, reviewer
- `reconciliation_rules.md` - Excel vs system reconciliation contract
- `reconciliation_checks.yaml` - machine-readable checks
- `edge_cases.md` - documented edge cases
- `source_registry_entry.yaml` - registry rows, one per file family
- `crosswalk_additions.yaml` - submarket crosswalk additions; flags if
  `market_crosswalk.yaml` or `submarket_crosswalk.yaml` must be created
- `workflow_activation_additions.yaml` - which workflows each file family
  activates
- `tests/test_adapter.py` - manifest, intake manifest, template schema,
  sample, crosswalk validity
- `runbooks/excel_market_survey_onboarding.md` - onboarding runbook
- `runbooks/excel_market_survey_common_issues.md` - troubleshooting runbook

## Non-goals

- Does not re-implement the canonical market_data or manual_uploads schemas
- Does not store credentials; intake is credential-less (shared drive or
  email inbox access is managed outside the adapter)
- Does not override the canonical `market_data/mapping.yaml` or
  `manual_uploads/mapping.yaml`
- Does not hardcode numeric staleness thresholds or outlier tolerances in
  prose; thresholds live in template schemas and overlays
