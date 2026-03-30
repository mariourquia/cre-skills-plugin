# Agent Communication Protocol

> How agents in this system communicate, hand off data, spawn subagents, and avoid context window leaks.
> Every agent and orchestrator MUST read this document before operating.

---

## 1. Core Principles

**No agent reads another agent's prompt file.** Agents communicate exclusively through structured data written to well-known file paths. An agent never loads another agent's `.md` prompt into its context -- that would leak implementation details and waste context window.

**No agent guesses data formats.** Every piece of data passed between agents conforms to a JSON schema in `schemas/`. If a schema doesn't exist for a data handoff, the handoff is broken and must be fixed before the pipeline runs.

**Orchestrators own routing.** Individual agents never launch other agents directly. The phase orchestrator (or PM orchestrator lead) decides what to launch, when, and with what data. Agents report results to their orchestrator; orchestrators route to the next agent.

**Context windows are isolated.** Each agent runs as a fresh `general-purpose` subagent via the Task tool. It receives only: (1) its own prompt, (2) the deal/property config, (3) upstream data from completed agents. It never inherits the parent orchestrator's full conversation history.

---

## 2. The Three Communication Channels

### Channel 1: Checkpoint Files (Agent → Orchestrator)

Every agent writes its status and results to its checkpoint file. The orchestrator polls these files to track progress.

**Path:** `data/status/{entity-id}/agents/{agent-id}.json`

**Schema:** `schemas/checkpoint/agent-checkpoint.schema.json`

```
Agent completes work
  → Writes output to data/reports/{entity-id}/{output-file}
  → Updates checkpoint: status=COMPLETED, outputPath=<path>
  → Orchestrator reads checkpoint
  → Orchestrator reads output file
  → Orchestrator passes output data to next agent
```

**Entity ID mapping:**
| Pipeline | Entity Type | ID Source | Path Example |
|----------|------------|-----------|--------------|
| Acquisition | deal | config/deal.json → dealId | data/status/DEAL-2025-001/agents/ |
| Hold Period | property | config/deal.json → propertyId | data/status/PROP-001/agents/ |
| PM Sub-pipeline | portfolio | config/portfolio.json → portfolioId | data/status/PORT-001/agents/ |
| Fund Management | fund | config/fund.json → fundId | data/status/FUND-001/agents/ |
| Development | project | config/deal.json → projectId | data/status/PROJ-001/agents/ |

### Channel 2: Phase Data Contracts (Phase → Phase)

When a phase completes, its orchestrator writes a `dataForDownstream` object into the master checkpoint. The next phase's orchestrator reads this object and injects it into agent prompts.

**Path:** `data/status/{entity-id}.json` → `phases.{phaseId}.dataForDownstream`

**Schema:** `schemas/phases/{pipeline}-{phase}-data.schema.json`

```
Phase 1 orchestrator compiles agent outputs
  → Writes dataForDownstream into master checkpoint
  → Phase 2 orchestrator reads dataForDownstream
  → Phase 2 orchestrator injects data into Phase 2 agent prompts
  → Phase 2 agents receive ONLY the structured data, not Phase 1 agent prompts
```

**What gets passed (always):**
- Structured data (JSON objects with typed fields)
- File paths to detailed reports (agent reads if it needs depth)
- Verdict and confidence score from upstream phase

**What NEVER gets passed:**
- Agent prompt text
- Raw conversation history
- Orchestrator internal state
- Tool call logs

### Channel 3: Cross-Chain Handoffs (Pipeline → Pipeline)

When one pipeline triggers another (e.g., hold-period EXIT → disposition), data flows through the handoff registry.

**Registry:** `engines/handoff-registry.json`

**Schema:** Each handoff entry defines the exact data contract (required fields, types, source paths).

```
Hold Period exit-trigger-evaluator produces EXIT verdict
  → Hold Period orchestrator writes handoff package to:
    data/handoffs/{source-pipeline}-to-{target-pipeline}/{entity-id}.json
  → Target pipeline's launch script reads handoff package
  → Target pipeline starts with handoff data as input
```

---

## 3. How Orchestrators Launch Agents

### The Launch Sequence

```
1. Orchestrator reads agent prompt file:
   Read agents/{pipeline-dir}/{agent-id}.md

2. Orchestrator reads deal/property config:
   Read config/deal.json (or config/portfolio.json for PM)

3. Orchestrator reads upstream phase data:
   Read data/status/{entity-id}.json → phases.{upstream}.dataForDownstream

4. Orchestrator composes the launch prompt:
   prompt = agent_prompt
         + "\n\n## Deal Configuration\n" + JSON.stringify(dealConfig)
         + "\n\n## Upstream Data\n" + JSON.stringify(upstreamData)
         + "\n\n## Runtime Parameters\n" + runtimeParams

5. Orchestrator launches via Task tool:
   Task(
     subagent_type="general-purpose",
     description="Run {agent-id} for {entity-id}",
     prompt=composedPrompt,
     run_in_background=true
   )

6. Orchestrator records task_id in checkpoint

7. Orchestrator polls for completion:
   TaskOutput(task_id=taskId) OR
   Read data/status/{entity-id}/agents/{agent-id}.json
```

### What the Agent Receives (and ONLY this)

| Data | Source | Purpose |
|------|--------|---------|
| Its own prompt (.md) | Injected by orchestrator | Instructions, strategy, output schema |
| Deal/property config | config/deal.json | Property details, business plan targets |
| Upstream phase data | Master checkpoint | Data from completed upstream phases |
| Runtime parameters | Orchestrator | entity-id, checkpoint path, log path, resume flag |
| Skill reference files | Agent reads directly | Methodology (e.g., `skills/underwriting-calc.md`) |

### What the Agent Does NOT Receive

- Other agents' prompts
- Other agents' output files (unless explicitly listed in upstream data)
- Orchestrator conversation history
- Challenge layer results from other agents
- Any data not in the composed prompt

---

## 4. How the PM Sub-Pipeline Integrates

The PM orchestrator is invoked by hold-period agents, not by the user directly.

### Invocation Flow

```
Hold Period Orchestrator
  → Launches operations-coordinator agent
    → operations-coordinator needs work order data from Yardi
    → operations-coordinator writes request to:
      data/requests/{property-id}/pm-request-{timestamp}.json
    → Hold Period orchestrator detects PM request
    → Hold Period orchestrator invokes PM orchestrator lead:

      Task(
        description="PM: process work order request for PROP-001",
        prompt=pm_orchestrator_lead_prompt
            + "\n\n## Request\n" + JSON.stringify(request)
            + "\n\n## Property Config\n" + JSON.stringify(propertyConfig)
      )

    → PM orchestrator lead:
      1. Reads request type (work_order, leasing, collections, reporting, etc.)
      2. Determines platform for this property (Yardi/AppFolio/RealPage)
      3. Launches target module agent + platform adapter
      4. Collects results
      5. Writes response to:
        data/responses/{property-id}/pm-response-{timestamp}.json

    → Hold Period orchestrator reads response
    → Hold Period orchestrator passes to operations-coordinator
```

### PM Request Format

```json
{
  "requestId": "REQ-{timestamp}",
  "requestType": "work_order | leasing | collections | financial_report | vendor | compliance | resident",
  "sourceAgent": "operations-coordinator",
  "sourcePipeline": "hold-period",
  "propertyId": "PROP-001",
  "portfolioId": "PORT-001",
  "priority": "P1 | P2 | P3 | P4",
  "payload": {
    // request-type-specific data
  },
  "responseDeadline": "ISO-timestamp or null"
}
```

### PM Response Format

```json
{
  "responseId": "RES-{timestamp}",
  "requestId": "REQ-{timestamp}",
  "status": "COMPLETED | PARTIAL | FAILED",
  "sourceModule": "maintenance | leasing | collections | accounting | vendor | compliance | resident",
  "platformUsed": "yardi | appfolio | realpage",
  "payload": {
    // response-type-specific data
  },
  "errors": [],
  "dataGaps": [],
  "nextActions": []
}
```

### Platform Adapter Selection

```
PM orchestrator lead reads property config:
  config/deal.json → properties[propertyId].pmPlatform

Platform mapping:
  "yardi"    → launch yardi-adapter agent
  "appfolio" → launch appfolio-adapter agent
  "realpage" → launch realpage-adapter agent

The target module agent (e.g., work-order-orchestrator) receives:
  1. Its own prompt
  2. The PM request payload
  3. Platform adapter identity (which adapter to use)

The module agent does NOT directly call the platform API.
Instead, it formulates a data request and the adapter agent executes it:

  Module Agent → writes data query to checkpoint
  Orchestrator → launches adapter with query
  Adapter → executes platform API call
  Adapter → writes normalized result
  Orchestrator → passes result back to module agent
```

---

## 5. Recurring Quarterly Loop (Hold Period Phase 3)

The quarterly monitoring loop requires careful state management to avoid context leaks between cycles.

### Cycle State Management

```
Each quarterly cycle gets its own namespace:

  data/status/{property-id}/quarterly/Q{n}-{year}/
    ├── agents/               # Agent checkpoints for this cycle
    ├── reports/              # Agent outputs for this cycle
    └── cycle-summary.json    # Cycle verdict and metrics

The master checkpoint tracks:
  phases.performanceMonitoring.currentCycle: "Q1-2026"
  phases.performanceMonitoring.cycleHistory: [
    { cycle: "Q4-2025", verdict: "ON_TRACK", noi: 1250000 },
    { cycle: "Q1-2026", verdict: "WATCH", noi: 1180000 }
  ]
```

### What Carries Between Cycles

| Data | Carries? | How |
|------|----------|-----|
| Prior quarter metrics | Yes | cycleHistory array in master checkpoint |
| Budget baseline | Yes | Phase 2 dataForDownstream (never changes mid-year) |
| Trend data (rolling) | Yes | Each cycle reads prior 4 cycles from cycleHistory |
| Agent internal state | No | Each cycle launches fresh agents |
| Orchestrator conversation | No | Each cycle is a fresh orchestrator session |

### What Does NOT Carry

- Agent prompt text from prior cycles
- Detailed agent outputs (only summary metrics carry)
- Orchestrator reasoning or decisions
- Tool call logs

If a Phase 3 agent needs detailed prior data, it reads the report file:
`data/status/{property-id}/quarterly/Q{n-1}-{year}/reports/{agent-id}-output.json`

---

## 6. Context Window Budget

Each agent operates within a fixed context window. The orchestrator is responsible for ensuring agents don't exceed their budget.

### Context Budget Allocation

| Component | Budget | Notes |
|-----------|--------|-------|
| Agent prompt | ~3,000-5,000 tokens | The .md file itself |
| Deal/property config | ~1,000-2,000 tokens | Injected by orchestrator |
| Upstream phase data | ~2,000-5,000 tokens | Structured JSON, not raw reports |
| Skill reference file(s) | ~3,000-8,000 tokens | Agent reads 1-3 skill files |
| Working space | Remainder | Agent's reasoning, tool calls, output |

### Orchestrator Responsibilities

1. **Summarize, don't pass through.** When compiling upstream data for injection, the orchestrator extracts key metrics and structured data. It does NOT pass the full raw output of every upstream agent.

2. **Use file paths for depth.** If an agent needs detailed data from an upstream agent, pass the file path in the upstream data object. The agent reads the file only if it needs the detail.

3. **Cap upstream data injection.** If the structured upstream data exceeds 5,000 tokens, the orchestrator must summarize it. Key metrics first, file paths for detail.

4. **Never chain agent prompts.** Agent A's prompt is never injected into Agent B's context. Each agent gets ONLY its own prompt.

### Agent Responsibilities

1. **Read skill files selectively.** Don't read the entire skill file if you only need one section. Use offset/limit parameters.

2. **Write structured output.** Always write JSON output conforming to the schema. Free-text narratives go in separate .md files.

3. **Checkpoint frequently.** Write checkpoints after each major step so work survives context window exhaustion.

4. **Report data gaps explicitly.** If upstream data is missing a field you need, log it as a data gap. Don't guess or hallucinate values.

---

## 7. Error Propagation

### Error Categories

| Category | Agent Action | Orchestrator Action |
|----------|-------------|-------------------|
| Missing input data | Log ERROR, report NEEDS_DATA in checkpoint | Retry upstream agent or flag data gap |
| Calculation inconsistency | Log WARNING, retry with explicit checks | If retry fails, mark phase CONDITIONAL |
| Platform API failure | Log ERROR, retry with backoff (3 attempts) | If all retries fail, use cached data or skip |
| Context window exceeded | Write partial checkpoint before exhaustion | Re-launch agent with resume=true |
| Agent timeout | N/A (agent is killed) | Re-launch with error context |
| Upstream phase failed | N/A (agent never launched) | Abort pipeline or skip to independent phases |

### Error Propagation Chain

```
Agent fails → writes ERROR to checkpoint
  → Phase orchestrator reads checkpoint
  → Phase orchestrator decides: retry / skip / fail phase
  → If phase fails → master checkpoint updated
  → Master orchestrator decides: retry phase / skip / fail pipeline
  → If pipeline fails → user notified with failure report
```

Errors NEVER propagate through agent-to-agent communication. They always go through the orchestrator, which decides the appropriate response.

---

## 8. File System Layout

```
data/
├── status/
│   ├── {entity-id}.json                    # Master checkpoint
│   ├── {entity-id}/
│   │   ├── agents/
│   │   │   └── {agent-id}.json             # Per-agent checkpoint
│   │   └── quarterly/                      # Hold period quarterly cycles
│   │       └── Q{n}-{year}/
│   │           ├── agents/
│   │           └── reports/
│
├── reports/
│   └── {entity-id}/
│       ├── {output-file}.json              # Agent output artifacts
│       ├── {output-file}.md                # Narrative reports
│       └── quarterly/                      # Quarterly reports
│
├── handoffs/
│   └── {source}-to-{target}/
│       └── {entity-id}.json                # Cross-pipeline handoff data
│
├── requests/
│   └── {property-id}/
│       └── pm-request-{timestamp}.json     # PM sub-pipeline requests
│
├── responses/
│   └── {property-id}/
│       └── pm-response-{timestamp}.json    # PM sub-pipeline responses
│
└── logs/
    └── {entity-id}/
        ├── master.log                      # Master orchestrator log
        ├── {phase}.log                     # Phase-specific logs
        └── pm.log                          # PM sub-pipeline log
```

---

## 9. Summary: What Prevents Context Leaks

| Risk | Prevention |
|------|-----------|
| Agent reads another agent's prompt | Agents only receive their own prompt via orchestrator injection |
| Agent inherits parent conversation | Each agent is a fresh Task subagent with isolated context |
| Quarterly cycles accumulate state | Each cycle runs fresh agents; only summary metrics carry via cycleHistory |
| PM adapter leaks platform details | Adapter outputs normalized data; consuming agents never see raw API responses |
| Upstream data bloats context | Orchestrator caps injection at ~5K tokens; uses file paths for detail |
| Error state leaks between agents | Errors propagate through orchestrator, never agent-to-agent |
| Challenge layer contaminates base | Challenge agents get the base verdict + datacard, not the full pipeline state |

---

## 10. Financial Planning Integration

### How Financial Planning Connects to Pipelines

The financial planning system is an operational layer that sits across all pipelines:

| Trigger | Financial Planning Action |
|---------|-------------------------|
| Hold Period Phase 2 (Budget Setup) | budget-orchestrator creates property budget |
| Monthly (by 15th) | actuals-collector pulls from PM platforms |
| Monthly (after actuals) | variance-engine produces variance report |
| Hold Period Phase 3 (Quarterly) | Reads variance + actuals for performance analysis |
| Quarterly (after Phase 3) | reforecast-modeler updates full-year projection |
| Fund Management Phase 4 (Monitoring) | portfolio-aggregator produces fund-level rollup |
| Fund Management Phase 4 (Reporting) | artifact-generator produces LP letter |
| Annually (Sept-Dec) | budget-orchestrator runs next-year budget cycle |
| Investment Strategy Phase 5 (Review) | scenario-modeler runs strategy pivot analysis |
| Portfolio Mgmt Phase 4 (Rebalancing) | portfolio-aggregator feeds rebalancing data |

### User-Selectable Scope

All financial planning operations accept a scope selector:

```json
{
  "scope": {
    "level": "portfolio | region | property_type | custom | property",
    "filters": { ... },
    "comparison": { "sameStore": true, ... },
    "timeframe": { "current": "2026", "priorYear": "2025", "projectionYears": 5 }
  }
}
```

Users invoke financial planning via launch-pipeline.js:

```bash
# Portfolio-level budget for next year
node scripts/launch-pipeline.js --pipeline financial-planning --entity PORT-001 --action budget --year 2027

# Reforecast for a single property
node scripts/launch-pipeline.js --pipeline financial-planning --entity PROP-001 --action reforecast --quarter Q1-2026

# 5-year business plan for a region
node scripts/launch-pipeline.js --pipeline financial-planning --entity PORT-001 --action business-plan --scope region --region southeast

# Scenario analysis across portfolio
node scripts/launch-pipeline.js --pipeline financial-planning --entity PORT-001 --action scenario --scenario rate-shock-200bps

# YTD performance vs budget for all value-add properties
node scripts/launch-pipeline.js --pipeline financial-planning --entity PORT-001 --action variance --scope property_type --type multifamily --strategy value-add
```
