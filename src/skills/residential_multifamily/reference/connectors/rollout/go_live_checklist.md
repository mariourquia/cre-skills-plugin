# Go-Live Checklist

status_tag: reference

Step-by-step checklist for moving from pilot to production go-live. Run once per wave, not once total. The first go-live (Wave 1) is the most involved; later waves reuse most of the same checks with narrower scope.

## Pre-go-live (the week before)

### Source registry

- [ ] Every source planned for the wave is in `source_registry/source_registry.yaml` at `status: stubbed` with a complete owner set (`data_owner`, `business_owner`, `technical_owner`).
- [ ] Every source's `object_coverage` is an exact match for the connector's `manifest.yaml` entity list or a documented subset.
- [ ] `expected_latency_minutes` is set realistically based on the adapter's observed behavior during pilot.
- [ ] `pii_classification`, `financial_sensitivity`, `legal_sensitivity` are set per the operator's classification scheme.
- [ ] Planned status transitions for the wave (`stubbed -> active`) are documented.

### Crosswalks

- [ ] `master_data/property_master_crosswalk.yaml` covers every property in scope.
- [ ] `master_data/account_crosswalk.yaml` covers every account used by in-scope properties; unmapped bucket is empty or explicitly documented.
- [ ] `master_data/vendor_master_crosswalk.yaml` covers the vendor list for in-scope properties (may grow during Wave 2).
- [ ] Crosswalk survivorship rules are declared; conflicting source values resolve deterministically.
- [ ] Effective-start dates set on all crosswalk rows.

### Connectors

- [ ] Every connector's `tests/test_manifest.py` passes.
- [ ] Every connector's `tests/test_sample_normalizes.py` passes for the golden path and negative cases.
- [ ] `reconciliation_checks.yaml` exists, references valid `../qa/` checks, and has been run against the pilot sample with no blocker failures.
- [ ] For every entity, `mapping.yaml` covers every raw field (either mapped or `optional_source: true`).

### DQ and reconciliation

- [ ] `date_coverage`, `record_count`, `duplicate_id`, `null_critical_field` green across all in-scope domains.
- [ ] `unit_count_reconciliation` green for pms.
- [ ] `lease_status_reconciliation` green for pms.
- [ ] `budget_actual_alignment` green for gl.
- [ ] `commitment_change_order_draw` green for construction (Wave 3).
- [ ] Reconciliation reports are retained (`reconciliation_report.json` attached to each landing).

### Workflow activation smoke test

- [ ] Every canonical workflow in the wave's scope activates against pilot-property data and produces a non-degraded output.
- [ ] Workflow activation map (`../_core/workflow_activation_map.yaml`, planned) returns the expected activation status for each pilot property.
- [ ] Executive-facing workflows (`executive_operating_summary_generation`, `monthly_asset_management_review`, `quarterly_portfolio_review`) produce outputs that match operator-prepared comparisons within the tolerance set by `finance_reporting`.

### Approval matrix wiring

- [ ] `_core/approval_matrix.md` mapped to the operator's overlay (`overlays/org/<org_id>/approval_matrix.yaml`).
- [ ] Every approval-gated workflow in the wave's scope routes correctly to the named approvers.
- [ ] Test approval: open a low-risk `ApprovalRequest`, route, approve, execute. Confirm `approval_audit_log.jsonl` tail is consistent.

### Monitoring

- [ ] `alert_policies.yaml` wired to the operator's ops surface.
- [ ] `exception_routing.yaml` routes fire to the correct channels.
- [ ] `observability_events.yaml` emissions are observable.
- [ ] SLO dashboards (operator-specific) reflect `slo_definitions.md` bands.
- [ ] Fair-housing-sensitive and legal-sensitive alert paths tested with a synthetic event; confirm they stay off broad channels.

### Runbooks

- [ ] Every runbook under `../runbooks/` has been read by `on_call_ops` at least once.
- [ ] `on_call_ops` rotation scheduled for the go-live window and the subsequent two cadence cycles.
- [ ] `compliance_risk` and `legal_counsel` named deputies confirmed for the go-live window.

### Rollback plan

- [ ] `../rollout/rollback_plan.md` reviewed; per-wave rollback steps specific to the go-live have been extracted and rehearsed.
- [ ] Prior snapshots of `reference/derived/` and `master_data/` are retained and restorable.
- [ ] Communication templates for stakeholder notification are prepared (do not send; hold in draft).

### Stakeholder communications

- [ ] `executive` briefed on the go-live timeline and escalation path.
- [ ] Affected consumer audiences briefed on changes to their workflow outputs and any expected confidence-band shifts.
- [ ] `compliance_risk` briefed on any regulatory-program scope changes.
- [ ] `legal_counsel` briefed if the wave touches legal-sensitive content.

## Day-of go-live

- [ ] `on_call_ops` confirmed available and paging.
- [ ] Source status transitions applied in the registry (`stubbed -> active`).
- [ ] First production landings observed; provenance validated.
- [ ] Normalization runs; reconciliation runs; report retained.
- [ ] Canonical workflows activated for at least one pilot property; outputs reviewed by consumer audience.
- [ ] Alert and exception queue steady; any items opened triaged before close of business.
- [ ] End-of-day readout to go-live stakeholders summarizing status.

## First-week monitoring

- [ ] Daily `exception_queue_review.md` executed.
- [ ] Reconciliation reports spot-checked across in-scope domains.
- [ ] Workflow activation map reviewed for any `workflow_blocked` entries unrelated to the wave.
- [ ] Any approval-gate activity reviewed for log consistency.
- [ ] Confidence-band drift monitored; unexpected downgrades investigated.
- [ ] SLO bands tracked and any breach flagged per `slo_definitions.md`.

## First-week retro

- [ ] Meeting attended by `on_call_ops`, `data_owner` representatives, `business_owner` representatives, primary consumer audiences, and `compliance_risk` and `legal_counsel` if their content was touched.
- [ ] Document: incidents opened, incidents closed, runbooks executed, open items.
- [ ] Decide: stay on course, tighten monitoring, pause scope expansion, or trigger rollback.
- [ ] Update `source_registry.yaml` notes with observations from the week.
- [ ] Log retro outcome per `_core/change_log_conventions.md`.

## Post-first-week handoff to steady-state operations

- [ ] Go-live ticket closed.
- [ ] Steady-state monitoring cadence established per `post_launch_monitoring_cadence.md`.
- [ ] `on_call_ops` rotation returns to normal cadence.
- [ ] Wave marked complete; next wave pre-go-live preparation begins when ready.

## Checklist hygiene

- This checklist is executed end-to-end per wave, not checked once.
- Items are not skipped even if they appear to have been done in a prior wave; new sources, new crosswalks, and new approval routes always re-require the check.
- Failures of individual checks do not auto-abort go-live; the lead operator decides whether the failure is blocking or deferrable. Document the decision.
