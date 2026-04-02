# CRE Orchestration Engine

A multi-agent pipeline engine that coordinates skills and expert agents into automated, multi-phase CRE workflows. Each orchestrator defines a sequence of phases, the agents and skills wired into each phase, dependency constraints between phases, checkpoint persistence, verdict logic, and optional post-pipeline challenge layers.

Derived from the [CRE Acquisition Orchestrator](https://github.com/ahacker-1/cre-acquisition-orchestrator) by **Avi Hacker** ([The AI Consulting Network](https://www.theaiconsultingnetwork.com)), licensed under Apache 2.0. See [NOTICE](../NOTICE) for full attribution.

---

## How It Works

Each orchestrator is a JSON configuration file in `configs/` that registers with the pipeline engine schema (`engine/pipeline-engine-schema.json`). The engine reads the config and executes the pipeline as follows:

1. **Phase sequencing**: Phases execute in declared order. Each phase has a weight (summing to 1.0 across the pipeline) that drives progress tracking.
2. **Agent dispatch**: Within each phase, specialist agents are launched as subagents (via the Agent tool). Agents run in parallel when they have no declared dependencies, or sequentially when upstream data is required.
3. **Skill wiring**: Each agent references one or more plugin skills (`skillRefs`) that provide the structured methodology, reference data, and calculators the agent uses.
4. **Checkpoint persistence**: After each agent completes, its findings, red flags, data gaps, and verdict are written to a checkpoint. If the pipeline is interrupted, it resumes from the last checkpoint.
5. **Verdict logic**: Each phase applies verdict rules (pass/fail/conditional thresholds, minimum agent completion counts, dealbreaker checks) to produce a phase-level verdict.
6. **Challenge layer** (optional): After the pipeline produces a verdict, perspective agents from the challenge layer stress-test the conclusion before final IC presentation.
7. **Cross-chain handoffs**: Pipelines connect -- the acquisition pipeline's closing output feeds the hold-period pipeline's onboarding input, and so on. The handoff registry (`engine/handoff-registry.json`) defines the data contracts between orchestrators.

---

## Available Orchestrators

### 1. Acquisition (`configs/acquisition.json`)

Full multifamily acquisition lifecycle from initial due diligence through closing. Coordinates 21+ specialist agents across 5 phases (DD, underwriting, financing, legal, closing) plus an optional challenge layer with 8 perspective agents and conditional triggers. Produces a **GO / CONDITIONAL / NO-GO** verdict. On GO, hands off to the hold-period orchestrator.

### 2. Capital Stack (`configs/capital-stack.json`)

Optimal debt/equity structuring pipeline. Qualifies the deal, sizes senior debt via DSCR/LTV/debt-yield constraints, structures mezzanine and preferred equity layers, optimizes blended cost of capital, and gates at IC. Produces a **PROCEED / RESTRUCTURE / KILL** verdict.

### 3. Hold Period (`configs/hold-period.json`)

Recurring asset management pipeline that runs post-acquisition. Onboards the property, sets annual budgets, monitors quarterly performance (recurring loop), manages leasing strategy, plans capital expenditures, and evaluates exit triggers. Coordinates 18+ skills and 4 asset management agents. Produces a **CONTINUE / INTERVENE / EXIT** verdict.

### 4. Disposition (`configs/disposition.json`)

Sell-side execution pipeline. Runs hold-sell-refi analysis, develops pricing strategy, prepares marketing materials, targets buyers, manages offers, coordinates seller-side DD response, and executes closing with 1031 exchange coordination. Produces a **SELL / HOLD / REFI** verdict.

### 5. Development (`configs/development.json`)

Ground-up development pipeline from land analysis through stabilization. Coordinates land residual/HBU analysis, entitlement feasibility, development pro forma, construction budget, lease-up war room, and stabilization monitoring. Produces a **BUILD / KILL / DEFER** verdict.

### 6. Fund Management (`configs/fund-management.json`)

Full fund lifecycle from formation through wind-down. Coordinates fund formation, capital raise, deployment (via handoff to acquisition), monitoring and reporting, distributions, and exit. Tracks GP economics across management fees, carried interest, co-invest, and clawback. Produces a **DEPLOY / HOLD / WIND-DOWN** verdict.

### 7. Research Intelligence (`configs/research-intelligence.json`)

Market intelligence pipeline that identifies target markets and acquisition opportunities before deals enter the pipeline. Runs macro screening, submarket deep dive, competitive set analysis, opportunity identification, and research memo production. Produces an **INVEST / MONITOR / PASS** verdict with a ranked opportunity map.

### 8. Investment Strategy (`configs/investment-strategy.json`)

Translates available capital and market conditions into a structured investment strategy. Assesses capital profile, positions against market cycle, formulates strategy, constructs portfolio targets with concentration limits and pacing models, and produces a strategy memo. Produces a **DEPLOY / REVISE / HOLD** verdict.

### 9. Portfolio Management (`configs/portfolio-management.json`)

Portfolio-level oversight across an entire portfolio of assets. Analyzes composition, assesses concentration risk across multiple dimensions, decomposes performance attribution, formulates rebalancing strategy, runs stress tests, and produces portfolio reporting. Produces a **REBALANCE / HOLD / DIVEST** verdict.

### 10. LP Intelligence (`configs/lp-intelligence.json`)

Inverts the standard GP-centric perspective to serve Limited Partners evaluating their GP allocations. Evaluates GP track record, formulates data requests and DDQs, monitors fund performance, oversees portfolio construction, and produces re-up recommendations. Produces a **RE-UP / REDUCE / EXIT** verdict.

---

## Running an Orchestrator

Use the `/cre-skills:orchestrate` command:

```
/cre-skills:orchestrate acquisition
/cre-skills:orchestrate hold-period
/cre-skills:orchestrate disposition
```

The command reads the orchestrator config, loads the orchestrator prompt, dispatches agents phase by phase, collects outputs, applies verdict logic, and optionally runs the challenge layer.

---

## Challenge Layer

The challenge layer (`challenge-layer/config.json`) is a post-pipeline adversarial review system. After the pipeline produces a verdict, perspective agents stress-test and re-evaluate that verdict before final IC presentation.

### Three Tiers

| Tier | Execution | Purpose |
|------|-----------|---------|
| **Tier 1** (always-run) | Sequential, 8 agents | Core verdict validation: CRE Veteran, IC Challenger, Risk Manager, Appraiser, Legal, Lender, Dynamic Buyer, Qualitative |
| **Tier 2** (conditional) | Parallel groups, triggered by deal attributes | Environmental flags, high capex, entitlement dependency, insurance gaps, large lease roll, conditional verdict, high LTV, value-add strategy |
| **Tier 3** (on-request) | User-triggered | Additional buyer perspectives, ESG, disposition, capital markets, property management, analyst cross-check |

After all tiers complete, the Deal Team Lead agent synthesizes all outputs into a challenge summary with verdict confirmation or revision, unresolved disagreements, conditions precedent, and an IC recommendation.

---

## Investor Profiles

The orchestration engine adapts thresholds and verdict criteria by investor type. Eight investor profiles are available in `investor-profiles/`:

| Profile | File | Key Characteristics |
|---------|------|---------------------|
| Institutional | `institutional.json` | ODCE mandate, max 40% LTV, GRESB required, core/core-plus only |
| Private Equity | `private-equity.json` | 15-20% net IRR, 65-75% LTV, value-add/opportunistic, exit-driven |
| Public REIT | `reit.json` | FFO/AFFO accretion, 50% max LTV, sector-focused, analyst-aware |
| Family Office | `family-office.json` | 10-30 year hold, after-tax optimization, operational simplicity |
| Family Office (Extended) | `family-office-extended.json` | Generational wealth, operating partner model, after-tax IRR required |
| Individual HNW | `individual-hnw.json` | Passive LP, plain-language business plan, max 7-year illiquidity |
| Small Operator | `small-operator.json` | 1-10 properties, self-management, personal guaranty, recourse debt |
| Syndicator | `syndicator.json` | Deal-by-deal raise, 50-200 LPs, GP fee economics, 75-80% LTV |

The strategy matrix (`investor-profiles/strategy-matrix.json`) maps strategy x investor-type to allowed/excluded combinations with underwriting parameters.

The thresholds file (`thresholds.json`) defines primary criteria (DSCR, cap rate spread, cash-on-cash, debt yield, LTV), secondary criteria (occupancy, expense ratio, rent-to-market), dealbreakers, risk scoring, and strategy-specific overrides -- all parameterized by investor type.

---

## Cross-Chain Handoffs

Orchestrators connect into multi-pipeline workflows via the handoff registry (`engine/handoff-registry.json`). Each handoff defines:

- **Trigger condition**: When the handoff fires (e.g., `acquisition.verdict == 'GO' AND closing.status == 'COMPLETED'`).
- **Data contract**: Required and optional fields that must be passed from the source phase to the target phase, with type specs, source paths, and descriptions.

### Active Handoffs

| From | To | Trigger |
|------|----|---------|
| Acquisition (closing) | Hold Period (onboarding) | Acquisition GO + closing completed |
| Hold Period (trigger-evaluation) | Disposition (hold-sell-analysis) | Hold Period EXIT verdict |
| Hold Period (trigger-evaluation) | Capital Stack (deal-qualification) | Hold Period INTERVENE + refinance |
| Fund Management (deployment) | Acquisition (due-diligence) | Fund deployment deal selected |
| Research Intelligence (opportunity-map) | Acquisition (due-diligence) | Research INVEST verdict |
| Investment Strategy (strategy-memo) | Fund Management (formation) | Strategy DEPLOY verdict |

---

## Schemas

Two JSON schemas in `schemas/` support the challenge layer's structured disagreement and reversal tracking:

- **`disagreement.schema.json`**: Captures divergent findings between perspective agents -- topic, base assumption, each agent's position with evidence and confidence, IRR sensitivity, and resolution method.
- **`reversal-trigger.schema.json`**: Defines specific conditions that would change the deal verdict -- trigger threshold, probability, severity, verdict transition, monitoring source, and mitigation.

---

## Directory Structure

```
orchestrators/
  engine/
    pipeline-engine-schema.json    # Engine registration schema (all orchestrators conform to this)
    handoff-registry.json          # Cross-chain data contracts
  configs/
    acquisition.json               # 10 orchestrator configs
    capital-stack.json
    hold-period.json
    disposition.json
    development.json
    fund-management.json
    research-intelligence.json
    investment-strategy.json
    portfolio-management.json
    lp-intelligence.json
  prompts/
    master-orchestrator.md         # Master orchestration prompt
    due-diligence-orchestrator.md   # 14 phase-level orchestrator prompts
    underwriting-orchestrator.md
    financing-orchestrator.md
    legal-orchestrator.md
    closing-orchestrator.md
    challenge-layer-orchestrator.md
    asset-management-orchestrator.md
    disposition-orchestrator.md
    fund-management-orchestrator.md
    research-intelligence-orchestrator.md
    investment-strategy-orchestrator.md
    portfolio-management-orchestrator.md
    lp-intelligence-orchestrator.md
  challenge-layer/
    config.json                    # 3-tier challenge layer configuration
  investor-profiles/
    institutional.json             # 8 investor profiles
    private-equity.json
    reit.json
    family-office.json
    family-office-extended.json
    individual-hnw.json
    small-operator.json
    syndicator.json
    strategy-matrix.json           # Strategy x InvestorType allowed combos
  schemas/
    disagreement.schema.json       # Agent disagreement record
    reversal-trigger.schema.json   # Verdict reversal trigger
  thresholds.json                  # Investment thresholds (base + investor-type overrides)
  README.md                        # This file
```
