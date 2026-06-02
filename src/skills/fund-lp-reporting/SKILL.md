---
name: fund-lp-reporting
slug: fund-lp-reporting
version: 0.1.0
status: deployed
category: workspace
description: "Orchestrate fund management and LP communications across formation, capital raising, quarterly reporting, performance attribution, and distributions. Use when a user needs to form a fund, communicate with LPs, raise capital, track performance, or manage distributions — routes to the appropriate specialist skill and maintains persistent fund context across sessions."
user-invocable: true
triggers:
  - "fund management"
  - "investor reporting"
  - "LP update"
  - "capital raise"
  - "distributions"
  - "fund formation"
  - "quarterly report"
  - "NAV reporting"
  - "pitch deck"
targets:
  - claude_code
---

# Fund & LP Reporting

Orchestrate fund management workflows by routing to specialist skills, gathering fund context, and maintaining persistent workspace state across sessions. See [routing-map.md](references/routing-map.md) for the full skill routing reference.

## When to Activate

- User needs fund formation, entity structuring, or PPM drafting
- User is preparing a capital raise, pitch deck, or investor update
- User needs performance attribution, NAV reporting, or distribution notices
- User is working on fund compliance, regulatory filings, or fee calculations

**Do NOT activate for:**
- Individual deal-level underwriting — use `acquisition-underwriting-engine`
- Portfolio-level allocation or rebalancing — use `portfolio-allocator`
- Single-property investor communications — use `quarterly-investor-update` directly

## Input Schema

| Field | Required | Default if Missing |
|-------|----------|--------------------|
| fund_or_vehicle_name | Yes | Ask user |
| task_type (formation / active_management / reporting / capital_raise) | Yes | Infer from user request |
| fund_size | No | Ask if needed for routing |
| reporting_period | No | Current quarter |
| lp_base_composition | No | Ask if producing LP-facing deliverables |

If fewer than 2 required fields are present, ask clarifying questions before routing.

## Process

### Step 1: Resume or Create Workspace

Read `~/.cre-skills/workspaces/` for any active fund workspace matching the fund name. If found, offer to resume with a summary of prior state. Otherwise, collect the inputs above and create a new workspace.

### Step 2: Route to Specialist Skills

Route based on `task_type`:

| Task Type | Primary Skill | Secondary Skills |
|-----------|--------------|-----------------|
| Formation | [fund-formation-toolkit](../fund-formation-toolkit/SKILL.md) | [sec-reg-d-compliance](../sec-reg-d-compliance/SKILL.md), [fund-raise-negotiation-engine](../fund-raise-negotiation-engine/SKILL.md) |
| Capital Raise | [lp-pitch-deck-builder](../lp-pitch-deck-builder/SKILL.md) | [capital-raise-machine](../capital-raise-machine/SKILL.md), [investor-lifecycle-manager](../investor-lifecycle-manager/SKILL.md) |
| Reporting | [quarterly-investor-update](../quarterly-investor-update/SKILL.md) | [performance-attribution](../performance-attribution/SKILL.md), [distribution-notice-generator](../distribution-notice-generator/SKILL.md) |
| Compliance | [fund-operations-compliance-dashboard](../fund-operations-compliance-dashboard/SKILL.md) | [sec-reg-d-compliance](../sec-reg-d-compliance/SKILL.md), [investor-lifecycle-manager](../investor-lifecycle-manager/SKILL.md) |

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

- Routing to formation skills when the fund already exists — confirm fund status first
- Producing LP-facing deliverables without loading brand guidelines — check `~/.cre-skills/brand-guidelines.json`
- Generating distribution notices without verifying the current NAV and waterfall terms

## Chain Notes

- **Upstream**: `deal-intake` (new fund setup), `closing-checklist-tracker` (post-close fund administration)
- **Downstream**: All specialist skills listed in the routing table above
- **Parallel**: `portfolio-allocator` (fund-level allocation decisions), `performance-attribution` (return decomposition)
