# Workflows invoked by maintenance_supervisor

| Workflow | Cadence | Trigger |
|---|---|---|
| `workflows/work_order_triage` | Daily | new WO, P1 event |
| `workflows/unit_turn_make_ready` | Per move-out; weekly view | turn started |
| `workflows/preventive_maintenance_execution` | Daily; monthly compliance | PM calendar event |
| `workflows/vendor_dispatch_sla_review` | Weekly | vendor SLA breach or pattern |
| `workflows/life_safety_audit` | Quarterly | quarter-end |
| `workflows/capital_project_intake_and_prioritization` | Quarterly or on-demand | life-safety flag or deferred-maintenance pattern |
| `workflows/repeat_work_order_pattern_analysis` | Monthly | rolling-90 review |
