# CRE Orchestrator — User Guide

> How to launch pipelines, what to expect, and how the system works.

> **Note:** The CLI scripts referenced below (`launch-deal.js`, `launch-pipeline.js`) are from the original orchestrator design and have not been implemented. Use the `/cre-skills:orchestrate` slash command instead, which provides the same functionality through Claude Code's skill system.

---

## Quick Start

### 1. Run an Acquisition Analysis

**Current method (recommended):**
```
/cre-skills:orchestrate acquisition
```

**Legacy CLI design (not implemented):**
```bash
# Prepare deal config
cp config/deal-example.json config/deal.json
# Edit config/deal.json with your deal parameters

# Launch the pipeline
node scripts/launch-deal.js --deal config/deal.json --phases all

# Or launch specific phases
node scripts/launch-deal.js --deal config/deal.json --phases dd,uw
```

### 2. Run Hold Period Monitoring

```bash
# After acquisition closes, launch hold period
node scripts/launch-pipeline.js --pipeline hold-period --entity PROP-001

# Run a specific quarterly monitoring cycle
node scripts/launch-pipeline.js --pipeline hold-period --entity PROP-001 --phase performance-monitoring --quarter Q1-2026

# Trigger a hold/sell/refi evaluation
node scripts/launch-pipeline.js --pipeline hold-period --entity PROP-001 --phase trigger-evaluation
```

### 3. Run PM Operations

```bash
# PM operations are invoked automatically by hold-period agents
# But you can also invoke directly for testing:
node scripts/launch-pipeline.js --pipeline pm --entity PORT-001 --request work-orders --property PROP-001
```

---

## System Architecture

### What This System Is

A multi-agent orchestration system for commercial real estate private equity operations. It coordinates specialized AI agents that analyze deals, monitor properties, manage operations, and produce institutional-grade reports.

### How It Works

```
You (the operator)
  │
  ▼
Launch Script (launch-deal.js or launch-pipeline.js)
  │  Validates config, creates directories, initializes checkpoints
  ▼
Master Orchestrator (or Pipeline Orchestrator)
  │  Reads config, determines phase sequence, manages lifecycle
  │  Runs as a Claude Code agent with Opus 4.6 (1M context)
  ▼
Phase Orchestrators
  │  Each phase has 2-7 specialist agents
  │  Orchestrator launches agents, collects results, determines verdict
  ▼
Specialist Agents
  │  Each agent has a specific mission (e.g., "analyze the rent roll")
  │  Runs as a fresh Claude Code subagent with isolated context
  │  Reads skill reference files for methodology
  │  Writes structured output + checkpoints
  ▼
Output: Reports, verdicts, handoff data for downstream pipelines
```

### The 10 Pipelines + PM Sub-Pipeline

| Pipeline | What It Does | Triggered By |
|----------|-------------|-------------|
| **Acquisition** | Evaluate a deal: DD, underwriting, financing, legal, closing | User launches deal |
| **Hold Period** | Monitor property during ownership: quarterly performance, leasing, capex, exit triggers | Acquisition closing handoff |
| **PM Operations** | Execute daily property management: collections, maintenance, leasing, compliance | Hold period agents |
| **Disposition** | Sell a property: pricing, marketing, offers, buyer DD, closing | Hold period EXIT verdict |
| **Capital Stack** | Finance/refinance: loan sizing, lender sourcing, term negotiation | Acquisition, hold period, or development |
| **Fund Management** | Manage the fund: formation, capital raise, deployment, LP reporting, distributions | Investment strategy |
| **Development** | Build a property: land, design, construction, lease-up, stabilization | Investment strategy |
| **Portfolio Management** | Manage the portfolio: allocation, attribution, risk monitoring, rebalancing | Fund management |
| **Investment Strategy** | Define strategy: market selection, thesis, target identification, pipeline | Portfolio feedback |
| **Research Intelligence** | Research markets: macro, sector, submarket, policy, regulatory | Feeds all pipelines |
| **LP Intelligence** | Evaluate from LP perspective: GP evaluation, terms, monitoring, re-up decision | Fund management |

### How Pipelines Connect

```
Investment Strategy ──▶ Research Intelligence ──▶ Fund Management
                                                      │
                                           ┌── Acquisition ──┐
                                           │                  │
                                   Development                │
                                           │                  │
                                           ▼                  ▼
                                     Capital Stack ◀──── Hold Period ──▶ PM Operations
                                           │               │    │
                                           │               │    ▼
                                           │               │  Disposition
                                           ▼               ▼    │
                                   Portfolio Mgmt ◀── Fund Mgmt ◀┘
                                           │
                                           ▼
                                     LP Intelligence
```

---

## What to Expect When You Launch

### Acquisition Pipeline (~45-90 minutes)

1. **Phase 1: Due Diligence** (7 agents, parallel)
   - Rent roll analysis, OpEx review, physical inspection, market study, environmental, title, tenant credit
   - Agents research market data via web search
   - You'll see log entries as each agent completes
   - **Output:** DD report with red flags and data gaps

2. **Phase 2: Underwriting** (3 agents, sequential)
   - Financial model → 27 scenario analysis → IC memo
   - Depends on DD data
   - **Output:** Base case model, sensitivity matrix, Investment Committee memo

3. **Phase 3: Financing** (3 agents, sequential)
   - Lender outreach → quote comparison → term sheet
   - **Output:** Recommended financing terms

4. **Phase 4: Legal** (6 agents, partially parallel with Phase 2-3)
   - PSA review, title/survey, estoppels, insurance, loan docs, transfer docs
   - Can start when DD is 80%+ complete
   - **Output:** Legal readiness assessment

5. **Phase 5: Closing** (2 agents, sequential)
   - Closing checklist → funds flow memo
   - Requires all prior phases
   - **Output:** Closing readiness, Go/No-Go verdict

6. **Challenge Layer** (post-pipeline)
   - Multi-perspective stress test of the verdict
   - 3-4 perspectives challenge the base recommendation
   - May override the pipeline verdict

**Final Output:**
- `data/reports/{deal-id}/final-report.md` — Full acquisition report
- `data/reports/{deal-id}/decision-card.md` — One-page executive decision card
- `data/reports/{deal-id}/ic-memo.md` — Investment Committee memo
- Verdict: **PROCEED** / **CONDITIONAL** / **KILL**

### Hold Period Pipeline (ongoing)

Once launched, the hold period runs as a lifecycle:

1. **Phase 1: Onboarding** (one-time, ~30 min)
   - PM transition, vendor inventory, insurance transfers, systems inventory
   - **Output:** Onboarding checklist, baseline property profile

2. **Phase 2: Budget Setup** (annual, ~30 min)
   - Revenue model, expense budget, capex plan, debt service projections
   - **Output:** Annual operating budget, 5-year capex plan

3. **Phase 3: Quarterly Monitoring** (recurring every quarter, ~20 min per cycle)
   - Performance vs budget, tenant health, market conditions, covenant compliance
   - **This is the heartbeat.** Every quarter, 4 agents analyze the property.
   - **Output:** Quarterly report with verdict: ON_TRACK / WATCH / INTERVENE / EXIT_TRIGGER

4. **Phases 4-6: Triggered as needed**
   - Leasing strategy, capital planning, tenant management
   - Activated when Phase 3 identifies issues or during annual reviews
   - Not every phase runs every quarter

5. **Phase 7: Trigger Evaluation** (when triggered)
   - Hold/sell/refi NPV analysis
   - Only runs when Phase 3 says INTERVENE or EXIT_TRIGGER
   - **Output:** CONTINUE / INTERVENE / EXIT decision card

**If INTERVENE:** A 90-day NOI sprint plan is generated.
**If EXIT:** A handoff package is created for the Disposition pipeline.

### PM Operations (continuous)

PM runs in the background, invoked by hold-period agents:

- **Collections:** Daily monitoring, weekly delinquency aging, monthly bad debt analysis
- **Leasing:** Lead pipeline tracking, lease execution, unit turn management
- **Maintenance:** Work order triage (P1-P4), preventive maintenance scheduling, emergency response
- **Accounting:** Monthly P&L, quarterly owner packages, annual CAM reconciliation
- **Vendors:** Contract management, COI compliance, performance scorecards
- **Compliance:** Fair housing monitoring, regulatory tracking, insurance program
- **Residents:** Communications, satisfaction tracking, amenity management

**Platform Adapters:** The PM orchestrator automatically selects the right platform adapter (Yardi, AppFolio, or RealPage) based on property configuration.

---

## Monitoring Progress

### Live Logs

Logs are written in real-time to `data/logs/{entity-id}/`:

```bash
# Watch the master log
tail -f data/logs/DEAL-2025-001/master.log

# Watch a specific phase
tail -f data/logs/PROP-001/hold-period.log

# Watch PM operations
tail -f data/logs/PORT-001/pm.log
```

Log format:
```
[2026-03-27T14:32:07.000Z] [agent-name] [CATEGORY] message
```

Categories: ACTION (doing something), FINDING (discovered data), INFO (status), ERROR (failure), COMPLETE (finished)

### Checkpoint Files

Check pipeline progress:

```bash
# Master checkpoint
cat data/status/DEAL-2025-001.json | python3 -m json.tool

# Specific agent
cat data/status/PROP-001/agents/performance-analyst.json | python3 -m json.tool

# Quarterly cycle
cat data/status/PROP-001/quarterly/Q1-2026/cycle-summary.json | python3 -m json.tool
```

### Resume After Interruption

If the pipeline is interrupted (timeout, crash, user interruption), restart it:

```bash
# Resume acquisition from where it left off
node scripts/launch-deal.js --deal config/deal.json --resume

# Resume hold period
node scripts/launch-pipeline.js --pipeline hold-period --entity PROP-001 --resume
```

The system reads the checkpoint file and skips completed phases/agents.

---

## Configuration

### Deal Configuration (`config/deal.json`)

```json
{
  "dealId": "DEAL-2025-001",
  "dealName": "Sunset Gardens Apartments",
  "propertyId": "PROP-001",
  "address": "123 Main St, Austin, TX 78701",
  "propertyType": "multifamily",
  "units": 200,
  "yearBuilt": 1985,
  "acquisitionPrice": 25000000,
  "strategy": "value-add",
  "investorProfile": {
    "investorType": "private-equity"
  },
  "pmPlatform": "yardi"
}
```

### Portfolio Configuration (`config/portfolio.json`)

```json
{
  "portfolioId": "PORT-001",
  "portfolioName": "Sunset Capital Fund I",
  "aum": 3000000000,
  "totalUnits": 30000,
  "propertyCount": 52,
  "regions": [
    { "regionId": "southeast", "units": 8500, "properties": 14 },
    { "regionId": "southwest", "units": 7200, "properties": 12 },
    { "regionId": "midwest", "units": 6800, "properties": 11 },
    { "regionId": "northeast", "units": 4500, "properties": 9 },
    { "regionId": "west", "units": 3000, "properties": 6 }
  ],
  "platforms": {
    "yardi": { "properties": 38, "units": 24000 },
    "appfolio": { "properties": 10, "units": 4500 },
    "realpage": { "properties": 4, "units": 1500 }
  }
}
```

### Thresholds (`config/thresholds.json`)

Investment criteria that agents use for go/no-go decisions. Customize these to match your investment strategy:

- `primaryCriteria`: DSCR, cap rate spread, cash-on-cash, debt yield, LTV
- `strategyThresholds`: Per-strategy minimums (core, core-plus, value-add, opportunistic)
- `holdPeriod`: Budget variance tolerance, occupancy targets, covenant cushions, exit triggers
- `propertyManagement`: Collections targets, leasing SLAs, maintenance SLAs, vendor performance

### Investor Profiles (`config/investor-profiles/`)

The challenge layer adjusts its perspectives based on investor type:
- `institutional.json` — Pension funds, insurance companies
- `private-equity.json` — PE sponsors
- `reit.json` — Public and private REITs
- `family-office.json` — Family offices
- `syndicator.json` — Syndicators

---

## Output Files

### Where to Find Results

```
data/reports/{entity-id}/
├── final-report.md              # Acquisition final report
├── decision-card.md             # One-page verdict card
├── ic-memo.md                   # Investment Committee memo
├── base-case-model.json         # Financial model
├── scenario-matrix.json         # 27-scenario sensitivity analysis
├── onboarding-report.json       # Hold period onboarding
├── annual-budget.json           # Annual operating budget
├── quarterly/
│   └── Q1-2026-performance.json # Quarterly monitoring report
├── leasing-strategy.json        # Leasing strategy
├── capex-plan.json              # Capital expenditure plan
├── exit-evaluation.json         # Hold/sell/refi analysis
└── noi-sprint-plan.json         # 90-day NOI intervention plan

data/reports/{portfolio-id}/
├── collections/                 # Daily/weekly/monthly collection data
├── leasing/                     # Leasing pipeline and execution
├── maintenance/                 # Work orders, PM schedules
├── accounting/                  # P&L, AR, AP
├── vendors/                     # Procurement, COI compliance
├── compliance/                  # Fair housing, regulatory, insurance
├── resident/                    # Communications, satisfaction, amenities
├── dashboard/                   # Operations dashboards
├── regions/                     # Regional summaries
├── audit/                       # Internal audit reports
└── migrations/                  # Platform migration logs
```

---

## Troubleshooting

### Pipeline Stuck

```bash
# Check which agent is running
cat data/status/{entity-id}.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
for phase_id, phase in d.get('phases', {}).items():
    if phase.get('status') in ['IN_PROGRESS', 'RUNNING']:
        print(f'Phase: {phase_id} ({phase[\"status\"]})')
        for agent, status in phase.get('agentStatuses', {}).items():
            if status in ['RUNNING', 'PENDING']:
                print(f'  Agent: {agent} ({status})')
"

# Check logs for errors
grep ERROR data/logs/{entity-id}/*.log | tail -20

# Resume from the stuck point
node scripts/launch-pipeline.js --pipeline {pipeline} --entity {entity-id} --resume
```

### Agent Failed

Agent failures are logged with full error context. The orchestrator will retry up to 3 times with exponential backoff. If all retries fail:

1. Check the agent checkpoint: `data/status/{entity-id}/agents/{agent-id}.json`
2. Check the error field for details
3. Fix the underlying issue (usually missing data or API failure)
4. Resume the pipeline: `--resume`

### Data Quality Issues

Agents flag data gaps in their output. Check:

```bash
# Find all data gaps across the pipeline
grep "data_gap\|DATA_GAP\|dataGap" data/status/{entity-id}/agents/*.json
```

Data gaps reduce the confidence score but don't stop the pipeline unless the gap is critical.

---

## Agent Counts

| Pipeline | Agents | Orchestrator |
|----------|--------|-------------|
| Acquisition | 21 | master-orchestrator |
| Hold Period | 21 | asset-management-orchestrator |
| PM Operations | 28 | pm-orchestrator-lead |
| Disposition | 14 | disposition-orchestrator |
| Capital Stack | 12 | capital-stack-orchestrator |
| Fund Management | 22 | fund-management-orchestrator |
| Development | 18 | development-orchestrator |
| Portfolio Management | 11 | portfolio-management-orchestrator |
| Investment Strategy | 10 | investment-strategy-orchestrator |
| Research Intelligence | 10 | research-intelligence-orchestrator |
| LP Intelligence | 11 | lp-intelligence-orchestrator |
| **Total** | **178** | **11 orchestrators** |

Plus 3 PM platform adapters (Yardi, AppFolio, RealPage) and a challenge layer orchestrator.
