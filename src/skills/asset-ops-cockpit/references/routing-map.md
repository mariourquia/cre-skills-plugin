# Asset Operations Cockpit — Skill Routing Map

Reference for the `asset-ops-cockpit` workspace skill. Maps asset management task types to specialist skills, including invocation order and data dependencies.

## Routing Decision Tree

```
User request
  ├─ Budgeting / financial planning
  │   └─ annual-budget-engine → cam-reconciliation-calculator → variance-narrative-generator
  │
  ├─ Performance monitoring / NOI
  │   └─ property-performance-dashboard → noi-sprint-plan → vendor-invoice-validator
  │
  ├─ Capital planning
  │   └─ capex-prioritizer → noi-sprint-plan (quick wins before major capex)
  │
  ├─ Compliance / collections
  │   └─ lease-compliance-auditor → tenant-delinquency-workout
  │
  └─ Maintenance / operations
      └─ building-systems-maintenance-manager → work-order-triage → property-operations-admin-toolkit
```

## Specialist Skill Summaries

| Skill | Purpose | Key Output |
|-------|---------|-----------|
| `annual-budget-engine` | Institutional-quality operating budgets | Line-item budget, benchmark comparison |
| `cam-reconciliation-calculator` | Annual CAM reconciliation by tenant | Reconciliation statements, over/under calculations |
| `variance-narrative-generator` | Ownership-ready variance narratives | Monthly/quarterly variance report |
| `property-performance-dashboard` | Monthly/quarterly performance reports | Performance dashboard, KPI trends |
| `noi-sprint-plan` | 90-day operational sprint to raise NOI | Sprint plan with prioritized initiatives |
| `vendor-invoice-validator` | Validate invoices against contracts | Invoice audit report, discrepancy flags |
| `capex-prioritizer` | IRR/NPV evaluation of competing capex | Ranked capex matrix, ROI analysis |
| `lease-compliance-auditor` | CAM, percentage rent, insurance compliance | Compliance audit report, recovery schedule |
| `tenant-delinquency-workout` | Structured workout for delinquent tenants | Workout plan, collection timeline |
| `building-systems-maintenance-manager` | Preventive maintenance, equipment lifecycle | Maintenance schedule, replacement forecast |
| `work-order-triage` | Priority classification, SLA assignment | Triaged work order queue |
| `property-operations-admin-toolkit` | Parking, inspections, landscaping, janitorial | Operations checklist, vendor scorecards |

## Common Workflow Sequences

1. **Annual cycle**: `annual-budget-engine` (Q4) → `property-performance-dashboard` (monthly) → `variance-narrative-generator` (monthly/quarterly) → `cam-reconciliation-calculator` (year-end)
2. **NOI improvement**: `property-performance-dashboard` (diagnose) → `noi-sprint-plan` (90-day plan) → `capex-prioritizer` (longer-term projects) → `lease-compliance-auditor` (recover leakage)
3. **Maintenance response**: `work-order-triage` (classify) → `building-systems-maintenance-manager` (systematic fix) → `vendor-invoice-validator` (verify costs)

## Workspace State Schema

The workspace JSON at `~/.cre-skills/workspaces/<workspace-id>.json` tracks:

- `property_name`: Property identifier
- `property_type`: Asset class
- `occupancy`: Current occupancy rate
- `financial_period`: Current reporting period
- `task_history`: Array of completed specialist skill invocations
- `urgent_issues`: Active operational issues
- `decisions`: Key asset management decisions
- `next_actions`: Recommended next steps
