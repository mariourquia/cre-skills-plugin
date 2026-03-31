# Knowledge System Protocol

> How the Shared Knowledge System connects all pipelines, maintains entity records, routes events, and produces periodic intelligence. Every pipeline orchestrator MUST read this document.

---

## 1. System Overview

The Knowledge System is the shared intelligence layer that connects all pipeline silos. Without it, each pipeline operates in isolation -- the acquisition pipeline does not know what the hold-period pipeline discovered, the fund-management pipeline cannot see property-level performance, and market signals from research never reach the asset management team.

### Architecture

```
Pipeline Orchestrators
       |
       | (publish events via event-publisher)
       v
  Event Stream (knowledge/graph/events/)
       |
       | (knowledge-manager reads, processes, routes)
       v
  Entity Records (knowledge/graph/entities/)
       |
       |---> Subscriber Notifications (knowledge/subscriptions/notifications/)
       |---> Broadcast Channels (knowledge/broadcasts/)
       |---> Insight Synthesizer (knowledge/graph/insights/)
       |---> Rollup Generator (knowledge/rollups/)
```

### Agents

| Agent | Model | Role |
|-------|-------|------|
| knowledge-manager | Opus | Central orchestrator. Reads events, updates entities, routes to subscribers, detects patterns, triggers synthesis and rollups. Only agent with portfolio-wide READ access. |
| event-publisher | Sonnet | Gateway writer. Validates, tags, enriches, and writes events to the stream. Called by pipeline orchestrators after significant actions. |
| insight-synthesizer | Opus | Pattern discoverer. Reads events + entities to find cross-pipeline correlations invisible to individual agents. |
| rollup-generator | Sonnet | Summary producer. Aggregates entity data and events into weekly, monthly, quarterly, and annual reports. |

### Data Flow

```
Pipeline Agent completes work
  --> Pipeline Orchestrator calls event-publisher (via Task tool)
  --> event-publisher validates, tags, enriches, writes event to stream
  --> knowledge-manager (on next run) reads event
  --> knowledge-manager updates affected entity records
  --> knowledge-manager routes event to matching subscribers
  --> knowledge-manager checks for cross-entity patterns
  --> If patterns found: triggers insight-synthesizer
  --> If rollup period reached: triggers rollup-generator
```

---

## 2. How Pipeline Orchestrators Publish Events

Every pipeline orchestrator MUST publish events after significant actions. This is not optional -- unpublished events create blind spots in the knowledge graph.

### When to Publish

| Event Occasion | eventType | Severity Guidance |
|---------------|-----------|-------------------|
| Phase completed with significant findings | FINDING | INFO (routine), WARNING (concerning), ALERT (requires attention) |
| Investment decision made (buy/pass/hold/sell) | DECISION | WARNING (routine), ALERT (significant portfolio impact) |
| Risk discovered during analysis | RISK_FLAG | WARNING (minor), ALERT (material), CRITICAL (threatens investment thesis) |
| Market conditions changed | MARKET_ALERT | INFO (routine update), WARNING (trend shift), ALERT (significant move), CRITICAL (market dislocation) |
| Policy or threshold changed | POLICY_CHANGE | WARNING (minor adjustment), ALERT (significant policy shift) |
| Performance metrics updated | PERFORMANCE_UPDATE | INFO (routine), WARNING (below budget), ALERT (significantly below UW) |
| Milestone reached (closing, stabilization, etc.) | MILESTONE | INFO (routine), WARNING (delayed) |
| Action taken (lease signed, capex completed, etc.) | ACTION | INFO (routine), WARNING (non-standard) |

### How to Publish

Call the event-publisher via Task tool after each significant action:

```
Task(agent="agents/knowledge/event-publisher.md", parameters={
  eventType: "PERFORMANCE_UPDATE",
  severity: "WARNING",
  source: {
    pipeline: "hold-period",
    agent: "performance-analyst",
    entityId: "PROP-2026-001",
    phase: "Phase 3: Performance Monitoring",
    orchestrator: "asset-management-orchestrator"
  },
  title: "Q1 2026 NOI 8.3% below underwriting projection",
  summary: "T-12 NOI of $1.62M vs UW projection of $1.77M, a negative variance of 8.3%. Primary drivers: economic occupancy at 89.1% (UW: 93.0%) due to 3 large unit turns in January, and effective rent growth of 0.8% (UW: 2.5%) as concessions increased to offset new supply in the submarket.",
  data: {
    noi_t12: 1620000,
    noi_uw: 1770000,
    variance_pct: -0.083,
    economic_occupancy: 0.891,
    economic_occupancy_uw: 0.930,
    rent_growth_actual: 0.008,
    rent_growth_uw: 0.025
  },
  affectedEntities: [{ entityId: "PROP-2026-001" }],
  tags: ["noi-miss", "occupancy-below-plan"]
})
```

### What the Event-Publisher Does

1. Validates event against `schemas/knowledge/event.schema.json`
2. Generates unique event ID: `EVT-{YYYY}-{MM}-{DD}-{hash}`
3. Auto-tags based on content analysis (adds pipeline, type, market, financial keywords)
4. Enriches affected entities via knowledge graph lookup
5. Checks for duplicate events (same type + source + title within 24 hours)
6. Determines broadcast channels (severity >= ALERT goes to broadcast)
7. Writes event to: `knowledge/graph/events/{YYYY}/{MM}/{DD}/{eventId}.json`
8. Returns eventId to the calling orchestrator

### Publishing Rules

1. **One event per significant action.** Do not batch multiple findings into a single event. Each finding, decision, or metric update gets its own event.
2. **Title must be specific.** "Performance update" is bad. "Q1 2026 NOI 8.3% below UW" is good.
3. **Summary must answer: what happened, why it matters, what changed.** Max 2000 characters.
4. **Always include source.entityId** when the event relates to a specific property, fund, or deal.
5. **Set severity honestly.** INFO for routine. WARNING for concerning. ALERT for attention-required. CRITICAL for thesis-threatening. Over-escalation creates noise; under-escalation creates blind spots.

---

## 3. How Orchestrators Read Subscriber Notifications

Pipeline orchestrators and their agents can receive cross-pipeline intelligence through the subscription system.

### At Agent Launch Time

When a pipeline orchestrator spawns an agent, it SHOULD check for pending notifications:

```
1. Check for notification package:
   Path: knowledge/subscriptions/notifications/{subscriberId}/
   Read the most recent notification file (sorted by timestamp)

2. If notification exists and is newer than the agent's last run:
   Inject the notification summary into the agent's context
   Include as a "Cross-Pipeline Intelligence" section in the agent's input data

3. The notification package contains:
   - Summary: "N new events since {lastDeliveredAt}: X MARKET_ALERTs, Y RISK_FLAGs, ..."
   - Events: summarized or full event objects (per subscription config)
   - Grouped by: eventType, entity, severity, or tag (per subscription config)
```

### For Direct Injection Subscribers

Some critical subscriptions use `DIRECT_INJECTION` delivery. For these:

```
1. Before launching the agent:
   Read: knowledge/subscriptions/injections/{subscriberId}/pending.json

2. If pending.json exists:
   Include its contents in the agent's prompt injection
   After the agent completes, delete or archive pending.json

3. This ensures the agent sees cross-pipeline intelligence
   in its FIRST context window, not as an afterthought.
```

### For Polling Subscribers

Some agents poll the event stream directly:

```
1. The subscription registry records lastDeliveredEventId
2. The agent reads events from the stream with eventId > lastDeliveredEventId
3. The agent applies its own tag/entity/severity filters
4. After processing, the agent updates lastDeliveredEventId
```

---

## 4. How Entity Records Are Updated

Entity records are the portfolio's single source of truth. They are updated by the knowledge-manager based on pipeline outputs.

### Update Flow

```
Pipeline agent writes output
  --> Pipeline agent publishes event via event-publisher
  --> Event includes: affectedEntities with fieldsAffected
  --> knowledge-manager reads event
  --> knowledge-manager reads affected entity record
  --> knowledge-manager applies field updates from event.data
  --> knowledge-manager recalculates derived fields (cap rate, DSCR, etc.)
  --> knowledge-manager writes updated entity record
  --> knowledge-manager increments record version
```

### Entity Record Schema

Entity records follow `schemas/knowledge/entity-record.schema.json`. Key sections:

| Section | Updated By | Frequency |
|---------|-----------|-----------|
| `acquisition` | Acquisition pipeline | Once (at closing) |
| `currentPerformance` | Hold-period pipeline (performance-analyst) | Quarterly |
| `debt` | Capital-stack pipeline, hold-period (covenant-watchdog) | As needed |
| `operations` | PM pipeline (PM orchestrator lead) | Monthly |
| `market` | Research pipeline, hold-period (market-pulse-analyst) | Quarterly |
| `riskFlags` | Any pipeline that detects a risk | As discovered |
| `holdPeriodVerdict` | Hold-period pipeline (exit-trigger-evaluator) | Quarterly |
| `timeline` | Any pipeline that produces a significant event | As events occur |

### Update Rules

1. **Never overwrite newer data with older data.** Check event timestamps before applying updates.
2. **Increment version on every update.** Version numbers must strictly increase.
3. **Clear staleFields entries when fields are updated.** A field that was stale becomes fresh.
4. **Add to timeline, never replace.** The timeline is append-only.
5. **Deduplicate riskFlags.** Same flag text + source within 7 days = duplicate.

---

## 5. How Periodic Rollups Are Triggered

Rollups are triggered by the knowledge-manager based on calendar schedule and event-count thresholds.

### Calendar Schedule

| Rollup Type | Schedule | Audience |
|-------------|----------|----------|
| Weekly | Every Monday | Operations team |
| Monthly | First 5 business days of each month | Asset management |
| Quarterly | First 5 business days of each quarter | LP / IC |
| Annual | First 10 business days of January | Board / Strategic |

### Event-Count Thresholds

Rollups can also be triggered by event volume, independent of calendar:

| Rollup Type | Event Threshold |
|-------------|----------------|
| Weekly | 100+ events since last weekly rollup |
| Monthly | 500+ events since last monthly rollup |

### Rollup Content by Type

| Content | Weekly | Monthly | Quarterly | Annual |
|---------|--------|---------|-----------|--------|
| Portfolio metrics | Top-line | Segment-level | Property-level | Property + trend |
| Events included | ALERT/CRITICAL | WARNING+ | All significant | All + thematic |
| Insights included | ACT_NOW | ACT_NOW + INVESTIGATE | All active | All + outcomes |
| Decisions included | None | Operational | All | All + outcomes |
| Prior period comparison | Prior week | Prior month | Prior quarter + YoY | Prior year + multi-year |
| Size target | < 5K tokens | < 15K tokens | < 40K tokens | < 80K tokens |

### Rollup Output

Rollups are written to `knowledge/rollups/{period}/{filename}.json` and broadcast to `knowledge/broadcasts/portfolio-updates/`.

---

## 6. How the Insight Synthesizer Runs

The insight-synthesizer discovers cross-pipeline patterns that emerge only at portfolio scale.

### Trigger Conditions

The knowledge-manager triggers the insight-synthesizer when ANY of these conditions are met:

| Trigger | Condition |
|---------|-----------|
| SCHEDULED | Weekly on Monday |
| EVENT_THRESHOLD | 50+ unprocessed events since last synthesis |
| KNOWLEDGE_MANAGER_REFERRAL | Knowledge-manager detected actionable patterns in its cross-entity analysis |
| HIGH_SEVERITY | 3+ ALERT or CRITICAL events in the last 7 days |

### Analysis Scope

The insight-synthesizer analyzes:
- All entity records in the portfolio
- All events from the last 30 days
- Active decisions and policies
- Prior insights (for trend tracking and deduplication)

### Pattern Categories

| Category | Example |
|----------|---------|
| MARKET_TREND | "Rent deceleration across 3 Austin properties concurrent with rising concessions" |
| OPERATIONAL_CORRELATION | "PM Company X underperforming across all 5 managed properties" |
| FINANCIAL_PATTERN | "4 loans maturing Q3 2026 with aggregate balance of $45M" |
| RISK_CONVERGENCE | "Environmental risk flags appearing across 3 properties in Houston" |
| OPPORTUNITY_SIGNAL | "Industrial sector showing cap rate compression while portfolio is underweight" |
| PORTFOLIO_DRIFT | "Geographic allocation drifted 8% from target toward Sun Belt" |

### Insight Output

Each insight includes:
- Confidence score (0-100) with scoring factors
- Action recommendation (MONITOR, INVESTIGATE, ACT_NOW, ESCALATE, INFORM_ONLY)
- Urgency (IMMEDIATE, THIS_WEEK, THIS_MONTH, NEXT_QUARTER, INFORMATIONAL)
- Target pipelines and agents
- Evidence chain (traceable to specific events and entity data)

High-confidence + ACT_NOW/ESCALATE insights are broadcast to `knowledge/broadcasts/portfolio-updates/`.

---

## 7. Staleness Policy

Entity records become stale when their data fields are not updated within the staleness threshold.

### Thresholds

| Threshold | Duration | Classification |
|-----------|----------|---------------|
| Fresh | Updated within 30 days | No action needed |
| Stale | 30-60 days since update | Warning: data may not reflect current conditions |
| Critically stale | 60+ days since update | Alert: data is unreliable for decision-making |

### Staleness Detection

The knowledge-manager checks staleness on every run:

1. For each entity record, check `lastUpdatedAt`
2. If `lastUpdatedAt` > 30 days ago: entity is stale
3. For stale entities, check individual field timestamps:
   - `currentPerformance`: should be updated quarterly
   - `debt`: should be updated whenever a payment is made or rates change
   - `operations`: should be updated monthly
   - `market`: should be updated quarterly
4. Stale fields are listed in the entity's `staleFields` array
5. Staleness report is written to `knowledge/graph/staleness-report.json`

### Staleness Response

- Stale entities are included in rollups but flagged with a staleness warning
- Insights based on stale data receive a confidence penalty (-10 points)
- Critically stale entities trigger an ALERT-level event to prompt data refresh
- The staleness report is available to all agents for awareness

---

## 8. Event TTL Policy

Events have a time-to-live (TTL) that determines when they expire from the event stream.

### TTL Rules

| Event Type | Retention Policy | TTL |
|-----------|------------------|-----|
| MARKET_ALERT | STANDARD | 1 year |
| FINDING | STANDARD | 1 year |
| ACTION | STANDARD | 1 year |
| PERFORMANCE_UPDATE | STANDARD | 1 year |
| RISK_FLAG | EXTENDED | 3 years |
| MILESTONE | EXTENDED | 3 years |
| DECISION | PERMANENT | Never expires |
| POLICY_CHANGE | PERMANENT | Never expires |

### Rationale

- **STANDARD (1 year):** Routine events lose relevance after one year. Market conditions, performance snapshots, and operational actions from more than a year ago are superseded by newer data.
- **EXTENDED (3 years):** Risk flags and milestones have longer relevance. A risk flag from 2 years ago may still be relevant if the underlying condition persists. Milestones mark the property timeline permanently.
- **PERMANENT (never):** Decisions and policy changes form the institutional memory. They explain why the portfolio looks the way it does. A decision to pass on a deal in 2024 is relevant context when the same deal reappears in 2027.

### Expiration Handling

- Expired events are not deleted. They are moved to an archive directory.
- Archived events can be recalled for historical analysis but are excluded from routine event processing.
- The knowledge-manager skips expired events during its event stream scan.

---

## 9. Directory Structure

```
knowledge/
  graph/
    entities/
      properties/      # One JSON file per property entity
      funds/            # One JSON file per fund entity
      markets/          # One JSON file per market entity
      tenants/          # One JSON file per tenant entity
      vendors/          # One JSON file per vendor entity
      lenders/          # One JSON file per lender entity
      brokers/          # One JSON file per broker entity
    events/             # Organized by YYYY/MM/DD/
    decisions/          # One JSON file per decision
    insights/           # One JSON file per insight
    policies/           # One JSON file per active policy
  subscriptions/
    subscription-registry.json
    notifications/      # {subscriberId}/{timestamp}.json
    injections/         # {subscriberId}/pending.json
  broadcasts/
    market-alerts/
    policy-changes/
    portfolio-updates/
    operational-alerts/
  rollups/
    weekly/
    monthly/
    quarterly/
    annual/

schemas/knowledge/
  entity-record.schema.json
  event.schema.json
  decision.schema.json
  insight.schema.json
  subscription-registry.schema.json

agents/knowledge/
  knowledge-manager.md
  event-publisher.md
  insight-synthesizer.md
  rollup-generator.md
```

---

## 10. Integration Checklist for Pipeline Orchestrators

When integrating a pipeline with the Knowledge System:

- [ ] Import event-publisher call after each significant phase completion
- [ ] Define event types and severity levels for each publishable action
- [ ] Register subscriber subscriptions in `subscription-registry.json` for agents that need cross-pipeline intelligence
- [ ] Add notification package reading to agent launch sequence
- [ ] Map pipeline outputs to entity record fields (which fields does this pipeline update?)
- [ ] Define event tags for content-based routing
- [ ] Test event publishing with a sample event
- [ ] Verify subscriber notifications are received by target agents
- [ ] Confirm entity records are updated after pipeline runs

---

## 11. Schema Quick Reference

| Schema | Path | Purpose |
|--------|------|---------|
| Entity Record | `schemas/knowledge/entity-record.schema.json` | Base schema for all entities in the knowledge graph |
| Event | `schemas/knowledge/event.schema.json` | Event stream entry schema |
| Decision | `schemas/knowledge/decision.schema.json` | Decision log entry schema |
| Insight | `schemas/knowledge/insight.schema.json` | Cross-pipeline insight schema |
| Subscription Registry | `schemas/knowledge/subscription-registry.schema.json` | Subscription configuration schema |
