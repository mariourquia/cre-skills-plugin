# Post-Launch Monitoring Cadence

status_tag: reference

Weekly, monthly, and quarterly reviews after go-live. Each cadence has a scope, attendees, inputs, outputs, and a relationship to the canonical workflows that already exist in `../../workflows/`.

## Weekly review

### Scope

Integration-layer steady-state: exception queue health, reconciliation status, SLO bands, approval-request pipeline.

### Attendees

- `on_call_ops` (lead).
- At least one `data_owner` representative for each active source.
- One representative from `regional_ops`, `asset_mgmt`, and `finance_reporting`.
- `compliance_risk` attends when any fair-housing or regulatory exception is open.

### Inputs

- Exception queue dump (open, new, closed, aging).
- Reconciliation report summaries for the week per domain.
- SLO status band per `../monitoring/slo_definitions.md`.
- Alert volume summary per `../monitoring/alert_policies.yaml`.
- Approval-request aging from `approval_audit_log.jsonl`.

### Agenda

1. Aging items review. Anything past SLA receives immediate owner assignment.
2. New exception categories or unexpected volume.
3. Any source at risk of `status: degraded`.
4. Approval-request pipeline: any near-expiry or contested.
5. Benchmark refresh status for any refreshes landed during the week.
6. Planned cutover or deprecation steps scheduled for the coming week.

### Outputs

- Weekly readout in the operations channel (see `../monitoring/alert_channel_design.md`).
- Aging-item disposition list.
- Escalations to monthly cadence where appropriate.

### Does not roll up to a canonical workflow directly

The weekly review is operational and feeds the monthly roll-ups rather than being a workflow output itself.

## Monthly review

### Scope

Subsystem-wide data-quality and operational-performance readout; integration-layer contribution to the monthly property and asset operations reviews.

### Attendees

- Integration-layer operations lead.
- All 8 canonical audiences (executive, regional_ops, asset_mgmt, finance_reporting, development, construction, compliance_risk, site_ops), attendance required per their scope.
- Any `business_owner` or `data_owner` with an incident in the prior month.

### Inputs

- Aggregated weekly readouts.
- `monthly_property_operating_review` outputs per property.
- `monthly_asset_management_review` outputs per asset.
- SLO status bands for the month.
- Exception-taxonomy category distribution.
- Approval-gate statistics (opened, approved, denied, aged).
- Any runbook executions during the month.

### Agenda

1. SLO band movement month-over-month.
2. Review of incidents that triggered runbooks, root cause and corrective-action status.
3. Source status changes (new `stubbed -> active`, any `degraded`, any `deprecated`).
4. Benchmark refresh recap, any rollbacks, any drift tolerance exceedances.
5. Crosswalk stability, new entries, pending changes.
6. Regulatory-program readiness (if in scope).
7. Cutover / deprecation progress for any in-flight transition.
8. Preview of the next month's planned changes.

### Outputs

- Monthly readout feeding:
  - `executive_operating_summary_generation` (executive summary)
  - `monthly_asset_management_review` (asset-level roll-up)
  - `monthly_property_operating_review` (property-level detail)
- Corrective-action list carried into the weekly review cadence.
- Update to `source_registry.yaml` notes for sources with state changes.
- Change log per `_core/change_log_conventions.md` for any content updates.

### Roll-up into canonical workflows

The integration-layer monthly review feeds the canonical workflows:

- `executive_operating_summary_generation`, the integration-layer health section is one of the executive's standing inputs.
- `monthly_asset_management_review`, per-asset data-quality and activation status.
- `monthly_property_operating_review`, per-property data-freshness and reconciliation status.
- `third_party_manager_scorecard_review`, TPM-driven integration-layer contribution.

## Quarterly review

### Scope

Subsystem trend review; structural health; overlay-threshold calibration; rollout progress for any in-flight wave; regulatory-program posture.

### Attendees

- `executive` (required).
- All 8 canonical audiences (required).
- Subsystem maintainer and designated reviewers.
- `legal_counsel` attends for any quarter with a fair-housing or legal-sensitive incident.

### Inputs

- Monthly readouts rolled up across the quarter.
- SLO trend across the quarter.
- Approval-gate activity trend.
- Rollout wave progress.
- Benchmark refresh cadence adherence.
- Cross-wave regression analysis.
- Any overlay-threshold proposals that have accumulated.

### Agenda

1. SLO trend: what is stable, what is deteriorating, what is improving.
2. Rollout progression: current wave, entry-criteria status for next wave, gating issues.
3. Threshold calibration: any overlay parameter changes warranted by observed data.
4. Regulatory posture: compliance filings landed, upcoming deadlines, any near-miss incidents.
5. Fair-housing and legal-sensitive posture: any incidents, containment quality, structural gaps.
6. Vendor-family health: patterns of schema drift, reliability, cost, consolidation candidates.
7. Connector deprecation or cutover candidates for the next quarter.
8. Change-log review per `_core/change_log_conventions.md`.

### Outputs

- Quarterly readout feeding:
  - `quarterly_portfolio_review` (canonical workflow).
  - `executive` and investor-facing narratives (with approval per `_core/approval_matrix.md` row 15).
- Overlay-threshold change proposals sent to the governance process.
- Rollout wave entry criteria reviewed; any wave crossing into a new phase documented.

### Roll-up into canonical workflows

The integration-layer quarterly review feeds directly into `quarterly_portfolio_review`. It also informs the annual planning cycle used by `budget_build` and any strategic planning captured in `executive` reporting.

## Annual review

Less formal than the other cadences at the integration-layer level; performed as part of the subsystem's annual governance cycle. Includes:

- Exception taxonomy review: are categories still accurate, are new categories needed.
- Runbook review: any runbooks that have not been exercised in twelve months are audited for relevance.
- Alert policy review: any alert that fired zero times or fired thousands of times gets re-tuned.
- Rollout wave retrospective: the full year's rollout progression and outstanding waves.
- SLO calibration at the subsystem level: canonical floor bands reviewed by subsystem maintainer.
- Vendor-relationship review: any vendor contributing persistent integration-layer toil.

## Cadence alignment with canonical workflows

| Cadence | Feeds |
|---|---|
| Weekly | Daily operations; does not feed a canonical workflow directly |
| Monthly | `monthly_property_operating_review`, `monthly_asset_management_review`, `executive_operating_summary_generation`, `third_party_manager_scorecard_review` |
| Quarterly | `quarterly_portfolio_review` |
| Annual | Governance cycle; canonical-content change log per `_core/change_log_conventions.md` |

## Output retention

- Weekly readouts: retained for at least one quarter.
- Monthly readouts: retained for at least one year.
- Quarterly readouts: retained for at least three years.
- Annual review outputs: retained permanently as part of the subsystem's governance record.

Retention policies are operator-configurable in their overlay but cannot fall below the above floors.
