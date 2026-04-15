# Third-Party Manager Oversight - Integration Layer Support

Owner-side oversight of third-party property managers (TPMs) is a first-class
use case for this integration layer. Many operators hold portfolios managed
by outside firms; the subsystem supports them explicitly. This document
describes how the integration layer supports that oversight: what it checks,
how it handles manager-submitted files, and what it surfaces to the
compliance-and-risk audience.

TPM-adjacent connectors:

- `pms` - direct system feeds when the TPM permits owner read access.
- `gl` - owner-side GL when the owner books its own books; manager-side GL
  when the owner consumes the manager's ledger.
- `hr_payroll` - staffing plans and roster when the owner has visibility.
- `manual_uploads` - the primary channel when the owner cannot integrate
  directly and must ingest manager-submitted files.

## Why manual_uploads matters here

Not every TPM permits direct system access. Some owners receive monthly
packets: rent rolls, operating statements, variance commentary, work-order
logs, leasing reports, staffing rosters, scorecards, and narrative
write-ups. Those files land through `manual_uploads`, are parsed against
file-drop templates (versioned per template), and then flow through the
same raw-to-normalized pipeline as direct feeds.

File-drop templates live at
`reference/connectors/manual_uploads/templates/<template_slug>/`. Each
template defines:

- Expected file format (csv, xlsx, pdf with structured extraction, json).
- Expected column or field set and canonical mapping.
- Attestation metadata (who at the TPM signed the file, on what date).
- Template version.

A manager-submitted file that lands without a matching template version is
quarantined with reason `template_version_unrecognized`.

## What the integration layer checks

### KPI timeliness

Every KPI has a cadence (`monthly`, `weekly`, `daily`). The integration
layer tracks the arrival timestamp of the last observation per KPI per
property. If the next expected observation is past its due date, the
scorecard surfaces a `stale_source` exception. The property-manager
agreement (PMA) in the org overlay names the target cadence and SLA.

Signal flow:

1. `manual_uploads` (or direct feed) lands a new observation.
2. The normalized layer updates the KPI's `last_observation_at`.
3. A nightly check compares `last_observation_at` vs the cadence's next-due
   timestamp per property.
4. KPIs past due generate exceptions routed per `exception_taxonomy.md`.

### KPI completeness

The scorecard requires a specific set of KPIs per property per period. The
PMA (tracked in `overlays/org/<org_id>/pma/<tpm_id>.yaml`) names the
required set. The `kpi_completeness` metric measures the share of required
KPIs present for the period. Below threshold blocks scorecard composite.

### Report-delivery aging

Beyond individual KPIs, the PMA requires specific reports (monthly
financials, operating narrative, variance explanations, leasing reports,
capex tracker). Each report has a calendar due date derived from the PMA.
The integration layer tracks delivery aging:

- `report_on_time` - delivered by due date.
- `report_late` - delivered after due date; report-level SLA still met.
- `report_very_late` - delivered past remediation threshold.
- `report_missing` - not delivered; age counts.

The `report_timeliness` metric rolls up the distribution.

### Budget and forecast governance

The integration layer checks:

- Budget baseline signed-off by both owner and TPM before period start.
- Forecast refreshed at the PMA cadence (commonly quarterly).
- Variance explanations completed for material variances.
- Reforecast adopted through `reforecast` workflow with required approvals.

Governance gaps surface as `dq_warning` at minimum; persistent gaps
escalate to the compliance-risk audience.

### Collections oversight

The `tpm_collections_performance` metric compares property-level
`collections_rate` to the market benchmark. Sustained underperformance
(two consecutive months below the PMA-defined floor) flags the property
for a TPM review.

For manager-submitted-only portfolios (no direct feed), collections
oversight depends on the manager's accounts-receivable report being
delivered on cadence. Missing AR reports block the metric and surface a
`tpm_report_feed_missing` exception.

### Turn performance oversight

The `tpm_turn_performance` metric compares `make_ready_days` to the
benchmark. Sustained underperformance triggers TPM review. For
manager-submitted-only portfolios, the metric depends on the turn log in
the monthly packet.

### Staffing vacancy oversight

The `staffing_vacancy_rate_tpm` metric compares vacant approved positions
against the staffing plan. Data arrives through `hr_payroll` when the
owner has visibility or through `manual_uploads` when the owner relies on
the manager's roster. Stale roster data triggers a `stale_source`
exception.

### Service-level adherence

The `service_level_adherence` metric rolls up SLA events (response time,
completion time, reporting deadlines). Inputs combine `pms` (work order
and lead events) with `manual_uploads` (manager-attested SLA logs).

### Approval routing response time

The `approval_response_time_tpm` metric tracks days from a TPM approval
request to an owner decision. The metric flags owner-side slowness (the
owner is part of the loop) as well as TPM-side slowness (requests arrive
after policy requires).

### Issue escalation

Any blocker-severity exception generated against a TPM-managed property
routes to the compliance-risk audience. Dwell-time SLAs per exception
category are defined in `exception_taxonomy.md`. Exceptions unresolved past
SLA escalate to the org-overlay-named escalation chain.

### Audit and exception tracking

The integration layer maintains a per-property audit tracker:

- Open audit findings (severity + age).
- Open exception tally (by category, by severity).
- Completed remediation evidence (documents, attestations).

The `audit_issue_count_and_severity` metric aggregates open findings.

## Scorecard-completeness checks

The `third_party_manager_scorecard_review` workflow (see
`workflow_activation_map.md`) depends on the full suite of TPM-oversight
metrics and surfaces a `completeness_score` prominently. Composite
scorecard does not compute below threshold - the workflow refuses rather
than synthesize a misleading number.

Checklist per scorecard run:

1. Every required KPI present for the period.
2. Every required report delivered or flagged.
3. Every variance over materiality threshold has a `VarianceExplanation`.
4. Every staffing vacancy tracked past its grace window.
5. Every SLA event with an outcome logged.
6. Every approval request decided or explicitly pending.
7. Every open audit finding resolved or on a remediation plan.

Failures per row produce exceptions. The scorecard lists them. Composite
calculation waits.

## Delayed-reporting flags

For manual_uploads-driven portfolios specifically, the integration layer
emits these flags:

- `manual_upload_missing_for_period` - expected file for the period did not
  arrive.
- `manual_upload_template_version_mismatch` - file arrived but the template
  version does not match; mapping fails.
- `manual_upload_attestation_missing` - file arrived but the required
  manager signature block is missing.
- `manual_upload_arithmetic_tie_out_fail` - file arrived and maps but the
  totals inside the file do not tie out.
- `manual_upload_content_contradicts_prior` - file's figures for a prior
  period contradict prior submissions without an amendment note.

## Missing-schedule flags

Every PMA defines a report schedule. The integration layer emits:

- `schedule_undefined_in_pma` - the PMA for this property does not define a
  required schedule; compliance-risk should decide.
- `schedule_defined_but_uncovered` - the PMA defines a schedule but no file
  or feed has ever landed for it.
- `schedule_defined_and_stale` - a file or feed landed in the past but the
  next expected delivery is past due.

## Third-party manager review cadence

Per the PMA, the integration layer supports quarterly TPM reviews:

1. Generate TPM scorecard through `third_party_manager_scorecard_review`.
2. Roll up exception history from the period.
3. Compare to prior periods.
4. Recommend action: maintain, remediate, or contract action.

Contract actions (termination, renegotiation) are always human-gated. The
integration layer never initiates contract-level decisions.

## Boundary with site_ops

Site-level operational decisions (dispatch, triage, turn scheduling) belong
to site-ops. TPM oversight is owner-side: it measures manager execution,
not the execution itself. The integration layer keeps these audiences
separate - the same normalized data serves both, but the workflow
activation context is different.

## Boundary with canonical subsystem

TPM oversight does not mutate canonical metrics or objects. It uses the
canonical `_core/metrics.md` family `tpm_oversight` as-is. Org-specific
TPM thresholds, approver identity, escalation chains, and reporting
preferences live in `overlays/org/<org_id>/`, not here. The integration
layer reads those org-scoped values; it never writes them.
