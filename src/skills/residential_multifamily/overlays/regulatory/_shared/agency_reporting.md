# Agency Reporting

Status: stub. Placeholder for agency-reporting obligations (submissions
to HUD, state HFA, USDA, PHA, or state tax-credit authority).

## Concept

Regulated properties owe scheduled reports to the program authority:
annual owner certifications, voucher submissions, compliance reports,
audit packages. Each report has a submitter, a receiver, a cadence, a
form template, and a submission portal or file-transfer path. The
overlay owns the catalog of report types and the cadence; the actual
form content and submission workflow live in reference tables and in
Phase 2 workflow packs.

## Target keys the overlay will populate

- `reporting_emphasis` -> adds agency-submission status to the tracked
  reports surface.
- Adds:
  - `agency_report_catalog`
  - `agency_report_submission_status`
  - `agency_report_overdue_count`

## Report types (examples, not exhaustive)

- LIHTC annual owner certification (state HFA).
- LIHTC 8609 (first-year placed-in-service).
- HUD voucher submission (TRACS, iMAX, or successor portal).
- HUD HAP subsidy billing.
- State HFA compliance report (cadence per regulatory agreement).
- USDA RD MINC / annual reports.
- PHA inspection-response submittals.

## Cadence and dependencies

Each report has:

- cadence (annual / semi-annual / quarterly / monthly / event-driven)
- dependency (on recert data, on UA data, on tenant-file state, on
  inspection state)
- receiver (agency slug)
- form (reference to template catalog)

## Dependent reference files

- `reference/normalized/agency_reports__{program}.csv`
- `reference/normalized/agency_submission_portals.csv`

## Phase 1 does not implement

- Populated report catalog.
- Form templates.
- Submission-portal integration.
- Agency-specific submission formatters.
