# Runbook: Excel Market Surveys Onboarding

Audience: data_platform_team, research_analyst, capital_projects_team,
procurement_lead, development_director.

Prerequisite reading: `manifest.yaml`, `intake_manifest.yaml`, `README.md`,
`template_schemas/`, `field_mapping.yaml`.

---

## 1. File delivery channel

Excel files land in one of three ways. Only the shared-drive path supports
automated intake; the other two are escalation paths only.

| Channel | Use Case | Intake Path |
|---|---|---|
| SFTP (`sftp://excel-intake.mu.private/<family_slug>/`) | Primary for automated drops from analyst endpoints that support SFTP | Monitored by intake runner; files move to quarantine if filename pattern mismatch |
| Shared drive (`shared_drive://market_data/<family_slug>/`) | Primary for analyst-authored drops; analyst drops the final workbook in the family-specific subdirectory | Watched path; filename pattern enforced |
| Email inbox (`excel-intake@mu.private`) | Escalation only; analyst sends when shared-drive access is down | Manual triage; file moved to shared drive before intake runs |

Drop locations are declared per file_family in `intake_manifest.yaml`.
Every drop carries the filename pattern from `intake_manifest.file_pattern`
and the corresponding template schema in `template_schemas/`.

## 2. Template version pinning

Every workbook family ships at a specific `library_version` / `workbook_version`
/ `pack_version` label in the `cover_metadata` sheet. Version rules:

- Analyst authors a workbook against the current template release; the
  version label must match the release in effect on the `as_of` date
- When the template is revised, the new release is stamped with an
  effective_start; dq rule `ex_conformance_column_headers_match_schema`
  accepts either the prior or the new headers during the dual-run window
  (typically one quarter)
- The template release registry lives at
  `reference/connectors/master_data/template_release_registry.yaml`
  (to be created; flagged as a wave-4 dependency)

A workbook landing with a version that does not match the current release
and is not within the dual-run window blocks intake.

## 3. Intake schedule

Automated intake runs on the cadence declared per file_family:

- `rent_comp_weekly`: Monday 08:00 ET; late-arriving drops within 48h
  trigger a delta pipeline that refreshes downstream aggregates
- `concession_tracker_monthly`: 1st calendar day of the month 09:00 ET
- `market_survey_workbook`: 5th business day of the quarter 10:00 ET
- `analyst_benchmark_pack`: 10th business day of the quarter 10:00 ET
- `staffing_benchmark`: 1st calendar day of the month 09:00 ET
- `labor_rate_quarterly`: 5th business day of the quarter 10:00 ET
- `material_price_sheet`: 1st calendar day of the month 09:00 ET
- `vendor_rate_card`: on_demand + annual refresh; intake runs on drop
- `turn_cost_library`: 10th business day of the quarter 10:00 ET
- `capex_cost_library`: 10th business day of the quarter 10:00 ET
- `schedule_assumption_sheet`: annual (Q1 of each year) + on_demand
- `market_commentary_file`: on_demand; intake runs on drop
- `asset_specific_comp_pack`: on_demand; intake runs on drop

## 4. Dual-run validation

Every new template release runs in dual-mode for one quarter.

- Analyst drops both the prior version and the new version for the same
  period
- Intake runs both files; the prior-version canonical output remains the
  source-of-truth; the new-version output lands in a parallel audit
  location
- Downstream reconciliation compares the two; drift within
  `reconciliation_tolerance_band.yaml::template_release_drift` is logged
- At the end of the dual-run window, the new version takes over; the
  prior version is archived in `reference/connectors/master_data/template_archive/`

## 5. Analyst sign-off model

Each file family declares a `required_reviewer` and optional
`optional_reviewer` in `intake_manifest.yaml`. The sign-off model follows:

- Analyst composes the workbook and populates `cover_metadata.analyst_name`
- Reviewer inspects the workbook and signs the `cover_metadata.reviewer`
  and `cover_metadata.signed_off_date` cells
- High-impact families (capex_cost_library, labor_rate_quarterly,
  turn_cost_library, vendor_rate_card, analyst_benchmark_pack,
  market_survey_workbook) block intake without reviewer + signed_off_date
- Rent_comp_weekly, concession_tracker_monthly, and material_price_sheet
  produce a warning (not blocker) when reviewer is absent; the row
  lands but confidence is reduced to medium

Cross-sign requirements (where two reviewers must sign):

- capex_cost_library: development_director + capital_projects_team
- labor_rate_quarterly: capital_projects_team + hr_director
- rent_comp_weekly: research_analyst + regional_ops_director

## 6. Operational checklist (first-run for a new file family)

1. Review `intake_manifest.yaml` entry for the family; verify drop_location,
   file_pattern, template_schema_ref, required_reviewer, staleness_threshold_days
2. Review the matching `template_schemas/<family>.yaml` entry; verify
   expected sheets, columns, enums
3. Align the analyst workbook with the template (column headers match
   exactly; cover_metadata populated; version label set)
4. Dry-run the drop to the `quarantine` prefix of the drop_location;
   confirm dq rules pass under `dq_rules.yaml`
5. Promote to the live drop_location; monitor the intake runner output
6. Confirm downstream workflows (see `workflow_activation_additions.yaml`)
   picked up the drop without blocking_issues
7. If blocking_issues surface, route per `runbooks/excel_common_issues.md`
