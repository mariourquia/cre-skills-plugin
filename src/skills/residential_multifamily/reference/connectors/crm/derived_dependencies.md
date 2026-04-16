# CRM Derived Dependencies

Which canonical metrics, workflows, and templates depend on normalized CRM data.

## Required normalized inputs

- `crm.lead_interaction`: all inbound and outbound touches against leads.
- `crm.campaign_source`: campaigns with medium and spend.

## Optional enrichment inputs

- `crm.resident_communication`: resident-facing outreach history (retention and satisfaction analytics).
- `crm.service_request`: non-maintenance resident requests.
- `crm.follow_up_task`: agent task queue and SLA tracking.

## Confidence minimum

- No open blocker failures on `crm.lead_interaction` landing.
- Protected-class scan clean.
- Merge survivorship resolved.

## Blocking data issues

- Protected-class token in free text.
- Merged lead without survivor pointer.
- Source_channel value not resolvable to campaign_id or enum.
- Provenance missing on any interaction row.

## Fallback mode when partial

- Without lead_interaction, lead_response_time and funnel touch metrics refuse.
- Without campaign_source, cost-per-lead and cost-per-lease refuse; conversion rates still compute.
- Without resident_communication, retention outreach metrics refuse; renewal workflows still run on PMS-only data.
- Without service_request, resident satisfaction signal is limited to maintenance-only proxies.
- Without follow_up_task, SLA dashboards refuse.

## Canonical metrics that depend on CRM

### Property Operations family

- `lead_response_time`: requires `crm.lead_interaction`, `pms.lead`.
- `tour_conversion`: requires `crm.lead_interaction` (to ground tour-scheduling touches) + `pms.tour`.
- `application_conversion`: indirectly depends on CRM for the attribution of lead to application.
- `move_in_conversion`: CRM is the traceability anchor linking a lead's journey to a lease.

## Example output types

- Lead-to-lease funnel diagnostic report.
- Cost-per-lead attribution dashboard (per campaign).
- Lead-response-time coaching report.
- Open-follow-up task queue.
- Stale-pipeline exception list.
- Campaign ROI dashboard.

## Dependent workflows

- `lead_to_lease_funnel_review` (CRM is the primary driver).
- `renewal_retention` (enriched by resident_communication).
- `move_in_administration` (uses interaction history for context).
- Leasing-strategy marketing planner (cost-per-lead analytics).
