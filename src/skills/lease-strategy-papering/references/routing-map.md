# Lease Strategy & Papering — Skill Routing Map

Reference for the `lease-strategy-papering` workspace skill. Maps leasing task types to specialist skills, including invocation order and data dependencies.

## Routing Decision Tree

```
User request
  ├─ Tenant retention / renewals
  │   └─ tenant-retention-engine → rent-optimization-planner → lease-negotiation-analyzer
  │
  ├─ Lease-up campaign / absorption
  │   └─ lease-up-war-room → leasing-operations-engine → rent-optimization-planner
  │
  └─ Lease documentation / amendments / options
      └─ lease-document-factory → lease-option-structurer → lease-trade-out-analyzer
```

## Specialist Skill Summaries

| Skill | Purpose | Key Output |
|-------|---------|-----------|
| `tenant-retention-engine` | Renewal probability scoring, retention NPV | Retention matrix, NPV comparison |
| `rent-optimization-planner` | Loss-to-lease waterfall, effective rent NPV | Rent optimization plan, concession analysis |
| `lease-negotiation-analyzer` | Complex negotiation scenario analysis | Negotiation matrix, BATNA analysis |
| `lease-up-war-room` | Funnel diagnostics, pricing strategy, absorption | Lease-up dashboard, pricing recommendations |
| `leasing-operations-engine` | Inquiry response, tour prep, pipeline CRM | Pipeline report, tour prep package |
| `lease-document-factory` | Amendments, template refresh, options | Draft lease documents, amendment redlines |
| `lease-option-structurer` | Option structuring and NPV analysis | Option valuation, exercise analysis |
| `lease-trade-out-analyzer` | Renewal vs. re-tenant NPV comparison | Trade-out matrix, NPV comparison |

## Data Flow Between Skills

1. **Retention workflow**: Start with `rent-roll-analyzer` output (expiration schedule) → `tenant-retention-engine` (scoring) → `rent-optimization-planner` (pricing) → `lease-negotiation-analyzer` (deal structuring) → `lease-document-factory` (papering)
2. **Lease-up workflow**: Start with `comp-snapshot` output (market data) → `lease-up-war-room` (strategy) → `leasing-operations-engine` (execution) → `lease-document-factory` (papering)

## Workspace State Schema

The workspace JSON at `~/.cre-skills/workspaces/<workspace-id>.json` tracks:

- `property_name`: Property identifier
- `property_type`: Asset class
- `occupancy`: Current occupancy rate
- `expiration_schedule`: Lease expiration summary
- `task_history`: Array of completed specialist skill invocations
- `active_negotiations`: Pending lease actions
- `decisions`: Key leasing decisions made
- `next_actions`: Recommended next steps
