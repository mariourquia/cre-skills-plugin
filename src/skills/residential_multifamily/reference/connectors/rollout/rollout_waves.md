# Rollout Waves

status_tag: reference

Wave definitions. Each wave has entry criteria, exit criteria, acceptance criteria, rollback triggers, typical duration bands (qualitative), and required sign-offs by audience.

## Wave 0, Foundation

Scope: source inventory, master-data crosswalk framework, source registry, canonical dependency map.

### Entry criteria

- Subsystem is installed; canonical `_core/` is intact (ontology, metrics, routing, schemas, approval matrix, guardrails).
- Connector contracts exist for every domain the operator will use (pms, gl, crm, ap, market_data, construction, hr_payroll, manual_uploads).
- Operator has completed (or nearly completed) the `executive` audience interview in `tailoring/`.

### Exit criteria

- `source_registry/source_registry.yaml` has an entry per inbound source, each at status `planned` or `stubbed`.
- `master_data/property_master_crosswalk.yaml` is populated for every property in scope.
- `master_data/account_crosswalk.yaml` is populated against the operator's chart of accounts.
- `master_data/vendor_master_crosswalk.yaml` has at least a seed of high-volume vendors (optional; the crosswalk may grow during Wave 2).
- Canonical dependency map (`_core/workflow_activation_map.yaml`, planned) is validated against the workflow set.

### Acceptance criteria

- No source in the registry is missing a `data_owner`, `business_owner`, or `technical_owner`.
- Every crosswalk row carries an effective-date and source attribution.
- Tests pass: `tests/test_source_registry.py` (planned), `tests/test_master_data_crosswalks.py` (planned), `tests/test_connector_contracts.py`.

### Rollback trigger

- Missing canonical content (ontology, metrics, approval matrix) requires holding Wave 0 until the canonical state is consistent.
- Registry entry with a disputed `data_owner` blocks exit until the ownership is resolved.

### Typical duration band

Short to medium. The work is crosswalk and inventory, tedious but not technically risky.

### Required sign-offs

- `executive` for scope and ownership decisions.
- `finance_reporting` for `account_crosswalk.yaml`.
- `asset_mgmt` for `property_master_crosswalk.yaml`.
- `compliance_risk` if any property is in a regulatory program.

## Wave 1, Core Financial and Operational Sources

Scope: pms, gl, market_data connectors activated to `status: active`.

### Entry criteria

- Wave 0 exit criteria met.
- pms, gl, market_data connector contracts intact; sample normalizations green.
- Adapters ready to land production files.

### Exit criteria

- pms and gl sources at `status: active`.
- market_data source(s) at `status: active`.
- First production landings reconciling green (or with only warnings triaged per `../runbooks/exception_queue_review.md`).
- `../../workflows/` that depend only on pms plus gl are able to activate with non-degraded confidence.

### Acceptance criteria

- `date_coverage`, `record_count`, `duplicate_id`, `null_critical_field`, `unit_count_reconciliation`, `lease_status_reconciliation`, `budget_actual_alignment` checks green for the wave's sources.
- Workflow activation map recomputes correctly for: `monthly_property_operating_review`, `reforecast`, `budget_build`, `monthly_asset_management_review` (partial, gl plus pms coverage), `market_rent_refresh`, `rent_comp_intake`.
- No aging `dq_blocker` exceptions attributable to the wave's sources.

### Rollback trigger

- Systematic reconciliation failure across a full cadence window.
- Schema drift that repeatedly blocks normalization.
- A discovered crosswalk gap that makes the pms or gl source unsafe to treat as authoritative.

### Typical duration band

Medium. Reconciliation stability is the gating condition; the operator may need iteration on crosswalks before exit.

### Required sign-offs

- `finance_reporting` for gl exit.
- `asset_mgmt` and `regional_ops` for pms exit.
- `asset_mgmt` for market_data exit.
- `compliance_risk` if regulatory-program properties are in scope.

## Wave 2, Transactional Counterparts

Scope: ap, crm, hr_payroll connectors activated to `status: active`.

### Entry criteria

- Wave 1 exit criteria met.
- Connector contracts for ap and crm intact; hr_payroll connector contract ready (either built or on schedule to complete in the wave).
- Adapters ready.

### Exit criteria

- ap, crm sources at `status: active`.
- hr_payroll source at `status: active` where scope includes it.
- Workflows that depend on ap or crm or hr_payroll activate with non-degraded confidence.

### Acceptance criteria

- Reconciliation green across the domain's checks.
- Vendor-dedup (ap), lead-dedup (crm), and employee-identity (hr_payroll) crosswalks stable.
- Workflow activation map green for: `lead_to_lease_funnel_review`, `bid_leveling_procurement_review`, `vendor_dispatch_sla_review`, hr-related sections of `monthly_property_operating_review` and `third_party_manager_scorecard_review`.

### Rollback trigger

- Persistent vendor-dedup failures that contaminate ap reconciliation.
- Lead-dedup failures that break `lead_to_lease_funnel_review` confidence.
- HR-payroll source carrying `pii_classification: restricted` without a compensating control; rollback immediate until control is in place.

### Typical duration band

Medium. hr_payroll is higher risk because of PII classification, expect additional compliance scrutiny.

### Required sign-offs

- `finance_reporting` for ap.
- `regional_ops` for crm.
- `compliance_risk` and `finance_reporting` for hr_payroll.
- `legal_counsel` for hr_payroll if the overlay classifies staff data at a restricted tier.

## Wave 3, Development and Construction, Manual Uploads

Scope: construction and manual_uploads connectors activated to `status: active`.

### Entry criteria

- Wave 2 exit criteria met.
- construction connector contract intact; manual_uploads connector contract ready.
- At least one active development or major-renovation project to validate against (for construction).
- For manual_uploads, the operator has selected the initial set of file templates to support.

### Exit criteria

- construction source at `status: active` for at least one project.
- manual_uploads landings reconciling green across the declared file templates.

### Acceptance criteria

- Reconciliation green across construction checks: `commitment_change_order_draw`, `date_coverage`, `budget_actual_alignment` for capex.
- Workflow activation map green for: `capex_estimate_generation`, `bid_leveling_procurement_review`, `change_order_review`, `draw_package_review`, `construction_meeting_prep_and_action_tracking`, `cost_to_complete_review`, `schedule_risk_review`, `capital_project_intake_and_prioritization`.
- manual_uploads reconciling on the declared templates; template-versioning tests pass (`tests/test_manual_upload_templates.py`, planned).

### Rollback trigger

- Draw-lien-waiver reconciliation failure persists and would risk an approval gate; rollback construction activation until reconciliation is stable.
- manual_uploads contract leakage (file contents not matching template) that would contaminate downstream workflows.

### Typical duration band

Medium to long. Construction has more approval gates than any other domain (draw, change order, bid award) and requires careful coordination.

### Required sign-offs

- `construction` and `development` (if pipeline present).
- `asset_mgmt`.
- `finance_reporting`.
- `executive` for draw and major bid gates (per `_core/approval_matrix.md`).
- `compliance_risk` for any construction activity that touches regulatory-program rehab.

## Wave 4, Full Workflow Activation

Scope: full workflow activation across the 27 canonical workflows; executive and owner reporting live; reconciliation dashboards in production; monitoring fully rolled out per `../monitoring/`.

### Entry criteria

- Waves 0 through 3 exit criteria met.
- No source in `degraded` status.
- Monitoring fully wired: `alert_policies.yaml`, `exception_routing.yaml`, `observability_events.yaml` feeding the operator's ops surface.
- `../monitoring/escalation_matrix.md` validated by `on_call_ops`.

### Exit criteria

- Every canonical workflow in `../../workflows/` activates with non-degraded confidence for in-scope properties.
- Executive and owner reporting produced on cadence per `executive_operating_summary_generation`, `monthly_asset_management_review`, `quarterly_portfolio_review`, `third_party_manager_scorecard_review`.
- Reconciliation dashboards in production; SLO bands tracked per `../monitoring/slo_definitions.md`.

### Acceptance criteria

- The exception queue is steady-state bounded.
- SLOs on target per `../monitoring/slo_definitions.md`.
- `../rollout/success_metrics.md` bands at "on target" or better for all categories.

### Rollback trigger

- SLO breach across multiple categories simultaneously: fall back to degraded activation and open a structural-review ticket.
- Repeated approval-gate breaches: halt full activation, reopen control investigations.

### Typical duration band

Long-tail steady state. Wave 4 never truly "ends"; it marks the transition into operations.

### Required sign-offs

- `executive` for overall readiness.
- All 8 canonical audiences for their portion of the workflow set.
- `compliance_risk` for fair-housing and regulatory-program scope.

## Wave deferred, Regulatory intake

Scope (deferred to overlay-driven activation): `regulatory_program_intake` source and any regulatory-overlay-specific workflows.

This scope does not move through the standard wave sequence. Activation is gated by `compliance_risk` sign-off on the program-specific overlay and `legal_counsel` review of the applicable program statute or contract. The source `regulatory_program_intake` in `source_registry.yaml` is flagged `rollout_wave: wave_deferred` to reflect this.

## Required sign-off matrix (quick reference)

| Wave | executive | regional_ops | asset_mgmt | finance_reporting | development | construction | compliance_risk | site_ops |
|---|---|---|---|---|---|---|---|---|
| 0 | required | optional | required | required | optional | optional | conditional | optional |
| 1 | informational | required | required | required | optional | optional | conditional | informational |
| 2 | informational | required | required | required | optional | optional | required | optional |
| 3 | informational | informational | required | required | conditional | required | conditional | optional |
| 4 | required | required | required | required | conditional | conditional | required | required |
| deferred | informational | informational | required | required | optional | optional | required | informational |

"conditional" = required if the overlay or portfolio makes it applicable (for example, `development` required only if the operator has a dev pipeline; `compliance_risk` required only if any property is in a regulatory program).
