---
name: asset-ops-cockpit
slug: asset-ops-cockpit
version: 0.1.0
status: deployed
category: workspace
description: "Orchestrate ongoing asset management and property operations across budgeting, performance monitoring, capex prioritization, NOI optimization, compliance, maintenance, and vendor management. Use when a user needs to manage property performance, build budgets, handle delinquencies, or run day-to-day operations — routes to the appropriate specialist skill and maintains persistent asset context across sessions."
user-invocable: true
triggers:
  - "asset management"
  - "property ops"
  - "budget review"
  - "performance dashboard"
  - "maintenance"
  - "NOI improvement"
  - "capex"
  - "work order"
  - "vendor management"
targets:
  - claude_code
---

# Asset Operations Cockpit

Orchestrate asset management workflows by routing to specialist skills for budgeting, performance monitoring, capital planning, compliance, and day-to-day operations. Maintains persistent workspace state across sessions. See [routing-map.md](references/routing-map.md) for the full skill routing reference.

## When to Activate

- User needs to build or review an annual operating budget
- User wants property performance reports, NOI improvement plans, or variance analysis
- User needs capex analysis, prioritization, or IRR/NPV evaluation
- User is managing maintenance, work orders, vendor contracts, or lease compliance
- User has delinquent tenants or collection issues

**Do NOT activate for:**
- Leasing strategy or lease documentation — use `lease-strategy-papering`
- Deal-level underwriting or acquisition analysis — use `acquisition-underwriting-engine`
- Fund-level reporting or LP communications — use `fund-lp-reporting`

## Input Schema

| Field | Required | Default if Missing |
|-------|----------|--------------------|
| property_name | Yes | Ask user |
| property_type | Yes | Ask user |
| task_type (budgeting / performance / capex / compliance / maintenance) | Yes | Infer from user request |
| current_occupancy | No | Ask if needed for routing |
| financial_data (T-12, budget, rent roll) | No | Ask when routing to financial skills |

If fewer than 2 required fields are present, ask clarifying questions before routing.

## Process

### Step 1: Resume or Create Workspace

Read `~/.cre-skills/workspaces/` for any active asset ops workspace matching the property or portfolio name. If found, offer to resume with a summary of prior state. Otherwise, collect the inputs above and create a new workspace.

### Step 2: Route to Specialist Skills

Route based on `task_type`:

| Task Type | Primary Skill | Secondary Skills |
|-----------|--------------|-----------------|
| Budgeting | [annual-budget-engine](../annual-budget-engine/SKILL.md) | [cam-reconciliation-calculator](../cam-reconciliation-calculator/SKILL.md), [variance-narrative-generator](../variance-narrative-generator/SKILL.md) |
| Performance | [property-performance-dashboard](../property-performance-dashboard/SKILL.md) | [noi-sprint-plan](../noi-sprint-plan/SKILL.md), [vendor-invoice-validator](../vendor-invoice-validator/SKILL.md) |
| Capex | [capex-prioritizer](../capex-prioritizer/SKILL.md) | [noi-sprint-plan](../noi-sprint-plan/SKILL.md) |
| Compliance | [lease-compliance-auditor](../lease-compliance-auditor/SKILL.md) | [tenant-delinquency-workout](../tenant-delinquency-workout/SKILL.md) |
| Maintenance | [building-systems-maintenance-manager](../building-systems-maintenance-manager/SKILL.md) | [work-order-triage](../work-order-triage/SKILL.md), [property-operations-admin-toolkit](../property-operations-admin-toolkit/SKILL.md) |

Invoke the primary skill first. After it completes, save workspace state, then suggest the next skill with rationale.

### Step 3: Save Workspace State

After each specialist skill completes, update `~/.cre-skills/workspaces/<workspace-id>.json` with results, decisions, and next actions.

## Output Format

End every response with:

```
---
## Decision Summary
[One-sentence verdict from the latest stage]

## Assumptions Used
- [Key assumptions]

## Missing Inputs
- [What's still needed]

## Recommended Next Actions
1. [Next skill to invoke with rationale]
2. [Alternative path if applicable]
```

## Red Flags

- Running NOI improvement plans without current T-12 data — request actuals before proceeding
- Prioritizing capex without knowing current DSCR covenant levels — check with `debt-covenant-monitor`
- Approving vendor invoices without verifying against contract terms and market rates

## Chain Notes

- **Upstream**: `post-close-onboarding-transition` (newly acquired assets), `deal-intake` (new asset setup), `t12-normalizer` (cleaned financial data)
- **Downstream**: All specialist skills listed in the routing table above
- **Parallel**: `lease-strategy-papering` (leasing as NOI lever), `insurance-risk-manager` (risk and coverage review)
