# Monitoring, Integration Layer

status_tag: reference

Alerts, exception routing, SLOs, channel design, observability events, and escalation matrix for the residential multifamily integration layer. This directory defines the monitoring contract; it does not specify a vendor product.

## How monitoring fits into operations

The integration layer emits structured events and metrics at every significant transition (landing, normalization, reconciliation, workflow activation, approval request, manual override). Event schemas are declared in `observability_events.yaml`. Alerts are declared in `alert_policies.yaml` as trigger conditions over those events. Exception categories (from `_core/exception_taxonomy.md`, planned) carry default routing and severity floors in `exception_routing.yaml`. Service-level objectives live in `slo_definitions.md`. Channel design is described at the level of channel roles (operations, compliance, legal, executive) in `alert_channel_design.md`; the operator maps those roles to whatever product they use (Slack, Teams, PagerDuty, Opsgenie, email).

## File map

| File | Purpose |
|---|---|
| `README.md` | This file. |
| `alert_policies.yaml` | Structured list of alert policies: alert_id, trigger_condition, severity, default_route, dwell_time_sla, repeat_policy, mute_policy, related_runbook. |
| `exception_routing.yaml` | Mapping from exception-taxonomy category to default routing audience, severity floor, and escalation chain. |
| `slo_definitions.md` | Freshness, resolution time, reconciliation completion, and workflow-activation success SLOs. Qualitative bands only. |
| `alert_channel_design.md` | Channel structure (operations, compliance, legal, executive), vendor-neutral. |
| `observability_events.yaml` | Catalog of events emitted by the integration layer. |
| `escalation_matrix.md` | Who gets called when, mapped to audience slugs and approval-floor categories. |

## No numbers in prose

SLOs are declared as qualitative bands. Exact thresholds, if any, are set by each operator in `overlays/org/<org_id>/`. Dollar and percent figures never appear in this directory's prose.

## Relationship to runbooks

Every alert in `alert_policies.yaml` references a `related_runbook` by filename under `../runbooks/`. On-call operators move from alert to runbook to remediation without having to improvise the routing.

## Relationship to workflow activation

Monitoring observes data; the workflow activation map (`../_core/workflow_activation_map.yaml`, planned) translates data state into workflow-ready / workflow-blocked states. The two surfaces reinforce each other, a workflow should never activate on data that monitoring has flagged degraded unless the workflow's degradation mode explicitly permits it.
