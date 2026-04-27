# Fund & LP Reporting — Skill Routing Map

Reference for the `fund-lp-reporting` workspace skill. Maps fund management task types to specialist skills, including invocation order and data dependencies.

## Routing Decision Tree

```
User request
  ├─ Fund formation / entity structuring / PPM
  │   └─ fund-formation-toolkit → sec-reg-d-compliance → fund-raise-negotiation-engine
  │
  ├─ Capital raise / pitch deck / LP outreach
  │   └─ lp-pitch-deck-builder → capital-raise-machine → investor-lifecycle-manager
  │
  ├─ Quarterly reporting / performance attribution / distributions
  │   └─ quarterly-investor-update → performance-attribution → distribution-notice-generator
  │
  └─ Compliance / operations / fee monitoring
      └─ fund-operations-compliance-dashboard → sec-reg-d-compliance → investor-lifecycle-manager
```

## Specialist Skill Summaries

| Skill | Purpose | Key Output |
|-------|---------|-----------|
| `fund-formation-toolkit` | Entity structuring, PPM drafting, Reg D compliance | Fund term sheet, PPM outline, entity diagram |
| `sec-reg-d-compliance` | Regulatory compliance and filing preparation | Form D filing checklist, compliance matrix |
| `fund-raise-negotiation-engine` | Side letter negotiation, fee structuring | Fee model, MFN cascade, side letter matrix |
| `lp-pitch-deck-builder` | Slide-by-slide pitch deck with track record | 16-slide pitch deck |
| `capital-raise-machine` | Data room, investor tracking, capital call notices | Data room index, capital call notices |
| `investor-lifecycle-manager` | LP meetings, re-up solicitation, benchmarking | Meeting prep, benchmark report, re-up analysis |
| `quarterly-investor-update` | LP-ready quarterly update letters | Quarterly letter, performance tables |
| `performance-attribution` | Return decomposition by income, appreciation, leverage | Attribution waterfall, TWR/IRR comparison |
| `distribution-notice-generator` | Distribution calculations and investor notices | Distribution notice, waterfall allocation |
| `fund-operations-compliance-dashboard` | Regulatory monitoring, fee calculations | Compliance dashboard, fee reconciliation |

## Workspace State Schema

The workspace JSON at `~/.cre-skills/workspaces/<workspace-id>.json` tracks:

- `fund_name`: Fund or vehicle identifier
- `strategy`: Fund investment strategy
- `fund_size`: Target or committed capital
- `task_history`: Array of completed specialist skill invocations with timestamps
- `decisions`: Key decisions made during the workflow
- `next_actions`: Recommended next steps
- `reporting_period`: Current reporting period (if applicable)
- `lp_base`: LP composition breakdown
