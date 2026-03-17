---
description: "Agent roster index for the CRE skills plugin. Lists all agents grouped by category with one-line descriptions. Used by deal-team-lead to select agents for multi-agent analysis. Includes 8 pre-built team compositions for common CRE tasks."
---

# CRE Agent Roster

## Institutional Buyer Agents

Represent how different buyer types evaluate the same asset. Deploy when analyzing buyer universe or positioning an asset for sale.

| Agent | File | Description |
|-------|------|-------------|
| Pension Fund Allocator | `buyer-pension-fund.md` | $50B+ public pension, ODCE mandate, core/long-hold/income-focused, max 40% LTV, 90-120 day DD, GRESB-required |
| Private Equity Fund | `buyer-private-equity.md` | $5B dry powder, opportunistic/value-add, 15-20% net IRR target, 65-75% LTV, 3-5 year hold, exit-driven underwriting |
| Public REIT | `buyer-reit.md` | $15B enterprise value, FFO/AFFO accretion lens, NAV methodology, analyst reaction awareness, sector-focused |
| Family Office | `buyer-family-office.md` | Ultra-HNW generational wealth, 10-30 year hold, after-tax optimization, 1031/cost seg/estate planning, operational simplicity |
| Multifamily Syndicator | `buyer-syndicator.md` | Deal-by-deal capital raise, 50-200 accredited investors, fee-driven GP economics, 75-80% LTV, Sun Belt value-add |

## Analytical Lens Agents

Provide different analytical frameworks for the same data. Deploy when you need to see a deal from multiple angles.

| Agent | File | Description |
|-------|------|-------------|
| Quantitative Analyst | `lens-quantitative.md` | Pure numbers: DCF, sensitivity grids, Monte Carlo framing, regression, breakeven analysis, rejects narrative without math |
| Qualitative Analyst | `lens-qualitative.md` | Market narrative: demographic shifts, neighborhood trajectory, political dynamics, tenant quality, competitive positioning |
| Contrarian Analyst | `lens-contrarian.md` | Consensus inverter: identifies crowded trades, mean-reversion opportunities, variant perceptions, catalyst timelines |
| Risk Manager | `lens-risk-manager.md` | Downside focus: tail risk, stress testing, leverage discipline, liquidity analysis, covenant monitoring, 8-dimension risk taxonomy |
| ESG/Impact Specialist | `lens-esg-impact.md` | Sustainability lens: GRESB, TCFD, CRREM stranding, climate physical/transition risk, social impact, governance quality |

## Composite Agents

General-purpose and orchestration agents for broad CRE tasks.

| Agent | File | Description |
|-------|------|-------------|
| CRE Veteran | `cre-veteran.md` | 30-year generalist across all CRE functions, default first-call agent, routes to specialists, provides institutional context |
| Deal Team Lead | `deal-team-lead.md` | Multi-agent orchestrator: assembles 3-5 agent teams, structures disagreement, synthesizes recommendations, manages 8 pre-built teams |

---

## Pre-Built Team Compositions

Standard agent teams for common CRE tasks. The deal-team-lead assembles these or builds custom teams.

### 1. Acquisition Investment Committee
**When**: Full analysis of a potential acquisition for IC presentation.
**Agents**: CRE Veteran, Quantitative Analyst, Qualitative Analyst, Risk Manager, + relevant buyer agent.
**Sequence**: Veteran -> Qualitative -> Quantitative -> Risk Manager -> Buyer -> Synthesis.

### 2. Capital Stack Optimization
**When**: Structuring optimal debt/equity mix for a deal or refinancing.
**Agents**: Quantitative Analyst, Risk Manager, + relevant buyer agent.
**Sequence**: Quantitative -> Risk Manager -> Buyer -> Synthesis.

### 3. Disposition Strategy
**When**: Positioning an asset for sale and ranking the buyer universe.
**Agents**: CRE Veteran, Pension Fund, PE Fund, REIT, Family Office.
**Sequence**: Veteran -> All buyers in parallel -> Synthesis (buyer universe ranking).

### 4. Development Feasibility
**When**: Evaluating whether a ground-up or adaptive reuse project pencils.
**Agents**: CRE Veteran, Quantitative Analyst, Qualitative Analyst, Risk Manager.
**Sequence**: Veteran -> Qualitative -> Quantitative -> Risk Manager -> Synthesis.

### 5. Lease Negotiation Strategy
**When**: Preparing for a major lease negotiation (landlord or tenant side).
**Agents**: CRE Veteran, Quantitative Analyst, Risk Manager.
**Sequence**: Veteran -> Quantitative -> Risk Manager -> Synthesis.

### 6. Fund Formation / Capital Raise
**When**: Structuring a new fund or evaluating a fund offering.
**Agents**: CRE Veteran, Quantitative Analyst, Risk Manager, ESG Specialist.
**Sequence**: Veteran -> Quantitative -> Risk Manager -> ESG -> Synthesis.

### 7. Market Cycle Assessment
**When**: Determining cycle positioning and adjusting strategy accordingly.
**Agents**: CRE Veteran, Quantitative Analyst, Qualitative Analyst, Contrarian Analyst, Risk Manager.
**Sequence**: Veteran -> Quantitative -> Qualitative -> Contrarian -> Risk Manager -> Synthesis.

### 8. Crisis Response
**When**: Rapid assessment and action plan for portfolio distress.
**Agents**: Risk Manager, CRE Veteran, Quantitative Analyst, Contrarian Analyst.
**Sequence**: Risk Manager -> Veteran -> Quantitative -> Contrarian -> Synthesis.

---

## Agent Selection Guide

**Single-perspective questions**: Use one agent directly.
- "How would a pension fund price this?" -> `buyer-pension-fund.md`
- "Run a sensitivity analysis" -> `lens-quantitative.md`
- "What's the bear case?" -> `lens-contrarian.md`

**Multi-perspective questions**: Use `deal-team-lead.md` to orchestrate.
- "Should we acquire this asset?" -> Acquisition IC team
- "Who should we market this to?" -> Disposition Strategy team
- "Where are we in the cycle?" -> Market Cycle team

**Uncertain what you need**: Start with `cre-veteran.md` for routing.
