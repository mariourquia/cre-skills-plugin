---
name: lease-strategy-papering
slug: lease-strategy-papering
version: 0.1.0
status: deployed
category: workspace
description: "Orchestrate leasing workflows across tenant retention, lease-up campaigns, rent optimization, negotiations, and lease documentation. Use when a user brings a leasing task — routes to the appropriate specialist skill and maintains persistent leasing context across sessions."
user-invocable: true
triggers:
  - "leasing strategy"
  - "lease strategy"
  - "tenant renewal"
  - "lease-up"
  - "rent optimization"
  - "lease document"
  - "lease amendment"
  - "concession analysis"
  - "trade-out comparison"
targets:
  - claude_code
---

# Lease Strategy & Papering

Orchestrate leasing workflows by routing to specialist skills, gathering property and tenant context, and maintaining persistent workspace state across sessions. See [routing-map.md](references/routing-map.md) for the full skill routing reference.

## When to Activate

- User needs tenant retention analysis, renewal probability scoring, or NPV comparison
- User is planning a new lease-up campaign or absorption strategy
- User needs to draft, amend, or restructure lease documents
- User wants rent optimization, concession analysis, or trade-out comparison

**Do NOT activate for:**
- Single-lease abstraction or data extraction — use `lease-abstract-extractor`
- CAM reconciliation calculations — use `cam-reconciliation-calculator`
- Lease compliance auditing — use `lease-compliance-auditor` directly

## Input Schema

| Field | Required | Default if Missing |
|-------|----------|--------------------|
| property_name | Yes | Ask user |
| property_type | Yes | Ask user |
| task_type (retention / lease_up / documentation / renewal) | Yes | Infer from user request |
| current_occupancy | No | Ask if routing to retention or lease-up skills |
| lease_expiration_schedule | No | Ask if routing to retention skills |

If fewer than 2 required fields are present, ask clarifying questions before routing.

## Process

### Step 1: Resume or Create Workspace

Read `~/.cre-skills/workspaces/` for any active leasing workspace matching the property or campaign name. If found, offer to resume with a summary of prior state. Otherwise, collect the inputs above and create a new workspace.

### Step 2: Route to Specialist Skills

Route based on `task_type`:

| Task Type | Primary Skill | Secondary Skills |
|-----------|--------------|-----------------|
| Retention & Renewals | [tenant-retention-engine](../tenant-retention-engine/SKILL.md) | [rent-optimization-planner](../rent-optimization-planner/SKILL.md), [lease-negotiation-analyzer](../lease-negotiation-analyzer/SKILL.md) |
| Lease-Up Campaigns | [lease-up-war-room](../lease-up-war-room/SKILL.md) | [leasing-operations-engine](../leasing-operations-engine/SKILL.md), [rent-optimization-planner](../rent-optimization-planner/SKILL.md) |
| Lease Documentation | [lease-document-factory](../lease-document-factory/SKILL.md) | [lease-option-structurer](../lease-option-structurer/SKILL.md), [lease-trade-out-analyzer](../lease-trade-out-analyzer/SKILL.md) |

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

- Routing to lease-up skills when the property is >95% occupied — this is a retention task, not lease-up
- Generating lease documents without confirming current rent roll data matches actual lease terms
- Proceeding with concession analysis without market comp data from `comp-snapshot`

## Chain Notes

- **Upstream**: `rent-roll-analyzer` (verified rent roll and expiration data), `comp-snapshot` (market rent comparisons), `property-performance-dashboard` (leasing as NOI lever)
- **Downstream**: All specialist skills listed in the routing table above
- **Parallel**: `leasing-strategy-marketing-planner` (marketing materials and broker strategy), `noi-sprint-plan` (leasing as part of NOI improvement)
