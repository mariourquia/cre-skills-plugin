# Dealpath Reconciliation Rules

Narrative describing how Dealpath reconciles against downstream systems
across the pre-close -> post-close handoff. Tolerances cite
`reference/normalized/schemas/reconciliation_tolerance_band.yaml`;
no numeric thresholds appear in this document.

## Reconciliation scope

Dealpath is primary for pre-close deal, asset, development_project
(seed), and IC approval_request. Post-close, downstream systems take
over per `_core/stack_wave4/source_of_truth_matrix.md`. Reconciliation
covers the handoff lag, identity mapping, and financial/legal
consistency at the transition points.

Sources reconciled against:

- AppFolio (PMS) — post-close property setup and operating identity
- Procore (construction) — post-IC project creation for development deals
- Intacct (GL) — legal entity setup, project/location dimensions, close
  posting
- Yardi (PMS/GL alternate) — operator-specific post-IC operations where
  AppFolio is not the operating PMS

## Dealpath <-> AppFolio (post-close property setup)

Trigger event: Dealpath deal `pipeline_stage` transitions to `closed`
with `deal_close_date_actual` non-null, and `deal_type` in
{acquisition, recap}.

**Identity reconciliation.** Every closed Dealpath asset must resolve to
an AppFolio PropertyId via `property_master_crosswalk`. The mapping
carries `effective_start = deal_close_date_actual` and survives under
`dealpath_wins_until_setup_complete`; once AppFolio property setup
completes, AppFolio becomes primary for operating identity.

**Unit count reconciliation.** Dealpath `asset.unit_count` (planned or
diligence count) must match AppFolio `property.UnitCount` at setup
within the `unit_count_drift_band` tolerance (cite
`reconciliation_tolerance_band.yaml`). Drift above the band blocks
`post_ic_property_setup` until reconciled.

**Handoff lag.** AppFolio property setup must land within
`handoff_lag_threshold_days` of `deal_close_date_actual` (cite
`reconciliation_tolerance_band.yaml`). Exceedance surfaces through
`dp_handoff_lag` (warning) and escalates to blocker after the lag
threshold multiplier documented in the tolerance band file.

**Effective-dating semantics.** The asset record in Dealpath carries an
implicit effective window from `asset.created_at` to
`deal_close_date_actual`. After close, the canonical Asset is represented
through AppFolio Property; the Dealpath row is preserved in
`source_record_audit` but does not overwrite. Late corrections to
purchase price or legal entity on the Dealpath deal are preserved as
audit rows and do not back-propagate to the operating Property.

## Dealpath <-> Procore (development project handoff)

Trigger event: Dealpath deal `deal_type = development` AND milestone
`gc_selected` status transitions to `achieved`.

**Identity reconciliation.** Every ic_approved development deal in
Dealpath must resolve to a Procore project via `dev_project_crosswalk`.
Mapping carries `effective_start = milestone.gc_award.actual_date` and
survives under `procore_wins_at_project_execution`.

**Handoff lag.** Procore project creation must land within
`dev_handoff_lag_threshold_days` of `gc_selected` achievement (cite
`reconciliation_tolerance_band.yaml`). Exceedance surfaces through
`dp_handoff_dev_lag` (warning) and escalates to blocker after the
multiplier.

**Debt term sheet variance.** Dealpath `milestone.debt_term_sheet` value
is reconciled against the executed loan recorded in Intacct once the
development deal closes. Variance within the `debt_term_sheet_variance_band`
(cite `reconciliation_tolerance_band.yaml`) is tolerated; beyond band
triggers a narrative requirement at `investment_committee_prep`.

**Effective-dating semantics.** A Procore project created from a
development deal inherits `dev_project_crosswalk.effective_start` at
Procore `project.created_at`, not at Dealpath IC approval. Procore-
primary state for schedule, cost commitments, and change orders begins
from that date; Dealpath retains governance milestones (IC, post-IC
conditions) on the same deal.

## Dealpath <-> Intacct (legal entity setup post-close)

Trigger event: Dealpath deal `pipeline_stage = closed` AND
`deal_close_date_actual` non-null.

**Identity reconciliation.** Every closed deal with non-refi deal_type
must resolve `sponsor_entity_id` to a canonical `legal_entity_id` via
`legal_entity_crosswalk`. Intacct is primary for legal entity; Dealpath
sponsor_entity_id is a placeholder until reconciliation.

**Dimension setup.** Intacct `entity`, `project`, and `location`
dimensions must be created within
`legal_entity_setup_lag_threshold_days` (cite
`reconciliation_tolerance_band.yaml`) of `deal_close_date_actual`.
Exceedance generates `dp_handoff_lag` at warning with escalation to
blocker.

**Effective-dating semantics.** Legal entity records effective from
`deal_close_date_actual`. If the Intacct entity is set up late, the
effective date back-dates to `deal_close_date_actual` (not to Intacct
row-creation date) to preserve close-period consistency. The delay is
audit-logged.

## Dealpath <-> Yardi (post-IC operations, where applicable)

Trigger event: Operator flag on the Dealpath deal indicates Yardi is
the operating PMS instead of AppFolio. Trigger is deal
`pipeline_stage = closed` with `deal_close_date_actual` non-null.

**Identity reconciliation.** Analogous to Dealpath <-> AppFolio; the
`property_master_crosswalk` row carries `source_system = yardi_prod`
rather than `appfolio_prod`. Yardi-specific adapter rules apply beyond
that point; Dealpath reconciliation terminates at crosswalk resolution.

**Handoff lag.** Same `handoff_lag_threshold_days` as AppFolio; warnings
surface through `dp_handoff_lag` regardless of target PMS.

## Deal -> property/project transition: effective-dating rules

| Canonical Object | Effective start | Dealpath claim ends | New primary |
|---|---|---|---|
| Deal | sourcing (created_at) | never (Dealpath retains pre-close audit) | n/a |
| Asset | asset.created_at | deal_close_date_actual | AppFolio + Intacct co-define operating identity |
| DevelopmentProject | milestone.ic_approved.actual_date | milestone.gc_award.actual_date | Procore |
| ApprovalRequest (IC) | ic_decision.decided_date | never (governance artifact retained) | n/a |
| LegalEntity (sponsor) | deal_close_date_actual | n/a (Intacct primary at close) | Intacct |

All effective dates live on crosswalk rows, never on canonical objects.
Late-arriving data supersedes per `late_arriving_data_supersedes`
resolution rule from `source_of_truth_matrix.md`.

## Escalation triggers

- A blocker reconciliation failure halts the `acquisition_handoff`,
  `post_ic_property_setup`, or `development_pipeline_tracking` workflow
  depending on the affected object. Exception routed via
  `monitoring/exception_routing.yaml`.
- A warning reconciliation failure promotes the landing but flags the
  drift in the `pipeline_review` and `executive_pipeline_summary`
  workflows.
- Repeat warnings (same deal failing same check in consecutive landings)
  escalate to the `investments_lead` or `asset_mgmt_director` audience
  per the escalation matrix declared in `_core/approval_matrix.md`.

## Cross-domain reconciliation dependencies

The Dealpath reconciliation report is an input to AppFolio and Procore
reconciliation reports. A blocker on the Dealpath side prevents
promotion of downstream post-close state until the upstream deal
record is re-landed successfully. The chain is enforced by
`tests/test_connector_contracts.py` at the subsystem root.
