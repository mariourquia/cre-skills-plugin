# CRM Connector (stub, vendor-neutral)

Prospect and resident relationship-management feed. Complements the PMS feed with richer interaction, campaign-source, and follow-up detail — some operators run a dedicated CRM (leasing-specific or resident-lifecycle), others layer CRM features inside the PMS.

## Status

`status: stub` — schema, mapping template, sample, and reconciliation checks only. No Salesforce / Knock / Rentgrata / HubSpot / custom CRM adapter code lives here.

## Entities

| Entity | One-liner |
|---|---|
| `lead_interaction` | One row per prospect interaction touch (email, call, text, tour, portal). |
| `campaign_source` | One row per campaign or attribution source. |
| `resident_communication` | One row per communication sent to an existing resident. |
| `service_request` | One row per non-maintenance resident service request (amenity, concierge). |
| `follow_up_task` | One row per agent-queued follow-up task. |

## Scope

Vendor-agnostic. Defines the lead-interaction shape independent of the PMS lead entity; the two are reconciled via `lead_id` where possible. Protected-class attributes are never captured in CRM interaction notes.

## Integration

- `crm.lead_interaction` reconciles with `pms.lead` via `lead_id`. Discrepancies flag a broken attribution path.
- `crm.campaign_source` feeds lead-source ROI analysis in leasing roles.
- `crm.resident_communication` feeds the tenant-retention-engine skill.
- `crm.service_request` feeds property-operations-admin and tenant-event-planner workflows.
- `crm.follow_up_task` supports leasing-funnel SLA monitoring.

See `INGESTION.md` for the landing convention.
