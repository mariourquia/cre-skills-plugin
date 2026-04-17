```
 ██████╗██████╗ ███████╗    ███████╗██╗  ██╗██╗██╗     ██╗     ███████╗
██╔════╝██╔══██╗██╔════╝    ██╔════╝██║ ██╔╝██║██║     ██║     ██╔════╝
██║     ██████╔╝█████╗      ███████╗█████╔╝ ██║██║     ██║     ███████╗
██║     ██╔══██╗██╔══╝      ╚════██║██╔═██╗ ██║██║     ██║     ╚════██║
╚██████╗██║  ██║███████╗    ███████║██║  ██╗██║███████╗███████╗███████║
 ╚═════╝╚═╝  ╚═╝╚══════╝    ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝

                                │                                                                         |        
            *                   │           │           │                     _                          /|     |#|
           /|                  _│_         _|_          A          _        _[_]_                _|_    / |     |#|
          /_W_                /:::\       [_=_]        /_\        | |     _/_:::_\_      __     |:::|  |  |     |#|
          ( • )              /|:::|\      |:::|       ((^))       | |    |X/:::::\X|    |__|    |:::|  |  |     |#|
        \__/ \__[]           | |:::| |   _|_:_|_     /(:::)\     _|_|_   |/X:::::X\|    |::|    |:::|_ |  |     |#|
           | |              | |:::| |   |:::::::|    |:::::|    |:::::|  |\X:::::X/|    |::|    |:::::||  |    _|#|_
          /   \             | |:::| |  _|:::::::|_   |:::::|   _|:::::|_ |X/:::::\X|   _|::_|   |:::::||::|   |:::::|
         _|___|_            | |:::| | |:::::::::::|  |:::::|  |:::::::::||/X:::::X\|  |::::::| _|:::::||::|  _|:::::|_
    ___|=======|___________|_|:::|_|_|:::::::::::|__|:::::|__|:::::::::||\X:::::X/|__|::::::||:::::::||::|_|:::::::::|
           BROOKLYN BRIDGE                           WILLIAMSBURG BRIDGE                     QUEENSBORO BRIDGE
      _|_                     _|_                  |▔▔▔|               |▔▔▔|               _|_         _|_         _|_
     | ∩ |                   | ∩ |                 |XXX|               |XXX|              //|\\       //|\\       //|\\
    /| ∩ |\                 /| ∩ |\               /|   |\-------___---/|   |\            ///|\\\_____///|\\\_____///|\\
   / |___| \-------_-------/ |___| \-------------/ |___| \     /   \  /|___| \----------////|\\\\   ////|\\\\   ////|\\
  / /     \ \     / \     / /     \ \           / /     \ \   /     \/ /     \ \       / /  |  \ \ / /  |  \ \ / /  |  \
≈/≈/≈≈≈≈≈≈≈\≈\≈≈≈/≈≈≈\≈≈≈/≈/≈≈≈≈≈≈≈\≈\≈≈≈≈≈≈≈≈≈/≈/≈≈≈≈≈≈≈\≈\≈/≈≈≈≈≈≈≈\≈/≈≈≈≈≈≈\≈\≈≈≈≈≈/≈/≈≈≈|≈≈≈\≈/≈/≈≈≈|≈≈≈\≈/≈/≈≈|≈≈≈\
≈/≈/≈≈≈≈≈≈≈≈\≈\≈/≈≈≈≈≈\≈/≈/≈≈≈≈≈≈≈≈≈\≈\≈≈≈≈≈≈≈/≈/≈≈≈≈≈≈≈≈≈\≈\≈≈ EAST RIVER ≈≈≈\≈/≈≈≈≈/≈/≈≈≈≈|≈≈≈≈\≈/≈≈≈≈|≈≈≈≈\≈/≈≈≈|≈≈≈≈\
```

# CRE Skills Plugin

A Claude plugin delivering a large library of **commercial real estate skills** covering the full investment lifecycle -- deal sourcing, screening, underwriting, structuring, due diligence, capital markets, market research, asset management, leasing, investor relations, development, disposition, tax planning, ESG, portfolio strategy, and daily property operations. Each skill includes structured process logic, reference documents, chain connections to other skills, and Python calculators for precise quantitative output. Deploys as a plugin in Claude Code (CLI or Desktop Code tab) or as a local MCP server for Claude Desktop Chat tab. See [Key Stats](#key-stats) for current counts and [Release Maturity](#release-maturity) for status by surface.

## Release Maturity

This release is an **internal beta / controlled release candidate**. Most top-level skills (1:1 with a single `src/skills/<slug>/SKILL.md`) are self-contained and usable today. The residential multifamily subsystem and several install surfaces are held to a higher fail-closed bar and are labeled below.

| Surface / component | Status | What this means |
|---|---|---|
| Top-level skills (all but one) | Deployed | Runnable today. Expected behavior per SKILL.md. |
| `residential_multifamily` subsystem | **Beta RC (v0.6.0)** | Routing core plus workflows and roles are architected and tested. Subsystem ships with placeholder org overlays; all `reference/` files are tagged `sample / starter / illustrative / placeholder`. Decision-grade use requires an org onboarding pass (tailoring interview) to supply real data. Final-marked outputs (executive, IC, quarterly portfolio, executive pipeline) fail closed when required inputs are absent, enforce a period-seal gate (`close_status`, `close_lock_timestamp`, `budget_version`), and must follow the [executive output contract](src/skills/residential_multifamily/_core/executive_output_contract.md) (verdict-first + source-class labels + refusal artifacts). |
| Orchestrators | Template / semi-manual | Orchestrators are phase + agent + verdict **templates**. There is no autonomous engine that sequences phases, polls agents, or aggregates verdicts without Claude acting as conductor. Treat as structured prompts, not fire-and-forget pipelines. |
| Marketplace install | Supported (CLI) | `claude plugin marketplace add` from Claude Code CLI. Claude Desktop's "Add marketplace" dialog is **not** supported — this repo does not expose a manifest at that URL. See [docs/WHAT-TO-USE-WHEN.md](docs/WHAT-TO-USE-WHEN.md). |
| macOS DMG / Windows EXE installer | Supported | Smoke-tested by `scripts/installer_smoke_test.py` (fresh install). |
| Cowork ZIP import | Partial | Skills + agents + commands only. Hooks, MCP tools, orchestrators, calculators are not part of the Cowork surface. |
| Manual MCP config (Claude Desktop Chat tab) | Supported | `.mcp.json` + `mcp-server.mjs`; operational MCP tools with organizational aliases. |
| Codex / Gemini / Grok / Manus portable ZIP | Experimental | Skills ship as SKILL.md files. CLI-specific registration, calculator execution, and orchestrator support are **not tested** on these surfaces. |

**Upgrade, uninstall/reinstall, and corrupted-config recovery** paths do not currently have automated smoke tests. The existing smoke tests exercise fresh-install only. See [docs/install_smoke_test_matrix.md](docs/install_smoke_test_matrix.md) for the full coverage matrix and gaps.

## Known Limitations

- The `residential_multifamily` subsystem is `status: beta_rc` (v0.6.0). Every reference file ships as sample/starter/illustrative/placeholder. Final-marked workflows (executive, IC, quarterly, pipeline summary) declare `fallback_behavior: refuse` on required inputs — they fail closed rather than proceed with stale data — and period-grade workflows (monthly operating review, reforecast, quarterly portfolio review, executive operating summary, budget build) additionally refuse if the GL is not at the declared `close_status` floor (`soft_close` or `hard_close`). Non-final operating workflows will proceed with starter data tagged in their confidence banners. Do not treat any output as decision-grade until an org overlay has been applied.
- Six regulatory/affordable compliance workflows (`compliance_calendar_review`, `income_certification_cycle`, `rent_limit_test`, `agency_reporting_prep`, `file_audit_prep`, `recertification_batch`) are **phase-1 scaffolding** — the router recognizes them and the overlay slots exist, but no workflow pack implements them yet. The routing rule `r011_regulatory_workflow_explicit` is gated behind an explicit `regulatory_program` axis and `rent_limits` / `income_limits` reference files; missing references refuse the match.
- The **tailoring TUI** (`src/skills/residential_multifamily/tailoring/tools/tailoring_tui.py`) has a documented capability matrix in [docs/tailoring_capability_matrix.md](docs/tailoring_capability_matrix.md). Conflict surfacing across audiences is now surfaced (not silently collapsed). Approval-floor checks, canonical-definition-redefinition refusal, and preview-bundle YAML emission are **not yet implemented**; the matrix tracks each.
- **Orchestrator pipelines are templates, not autonomous engines.** `/cre-skills:orchestrate` loads phase + agent + verdict schemas; it relies on Claude to actually sequence the work. Verdict aggregation (GO/CONDITIONAL/KILL), phase checkpoint resume, and cross-phase evidence threading are not in code.
- **Windows installer** defends against UTF-8 BOM edge cases in PowerShell 5.1 but does not currently halt on missing Node/Python/npm prerequisites. Update Claude Code before install (older versions have MCP path issues on Windows).
- **Codex / Gemini / Grok / Manus** install targets are advertised via the portable ZIP but are not in the CI smoke-test matrix. Treat as experimental.

## Roadmap

Upcoming work is tracked in [`docs/ROADMAP.md`](docs/ROADMAP.md) — phased from v4.3 (near-term hardening), through v4.4 (agent orchestration upgrade) and v5.0 (real-world data integration), to v6.0 (domain completeness). A separate enterprise track covers SOC 2, RBAC, licensing, and team collaboration. Preview / staging mode for `status: beta_rc` and `status: experimental` skills is documented at [`docs/PREVIEW_MODE.md`](docs/PREVIEW_MODE.md).

## Key Stats

<!-- CATALOG:STATS:START -->
| Metric | Count |
|--------|-------|
| Skills | **113** |
| Expert Agents | **54** |
| Reference Files | **247** |
| Python Calculators | **12** |
| Workflow Chains | **6** |
| Orchestrator Pipelines | **10** |
| Slash Commands | **11** |
| Skill Categories | **18** |
<!-- CATALOG:STATS:END -->

---

## What's New in v4.2.0

**Hardening pass 2 close**: `residential_multifamily` subsystem moves from `status: draft` (v0.5.0) to `status: beta_rc` (v0.6.0). Three deferred objectives close: sealed-close gating (Obj 5) pins period-grade workflows behind a declared `close_status` floor; a finance-critical placeholder scanner (Obj 6) rejects un-labeled TBD/PLACEHOLDER rows in every CSV read by a final-marked workflow; an executive output contract (Obj 8) requires verdict-first structure + source-class labels on every numeric cell. +13 tests (total 436). See `CHANGELOG.md` for the full v4.2.0 entry.

**Catalog-driven architecture**: Single source of truth (`src/catalog/catalog.yaml`). Every public surface -- README stats, plugin.json, hooks prompt, routing table, registry -- is generated from the catalog. CI catches drift.

**MCP server**: Zero-dependency MCP server (`src/mcp-server.mjs`) for Claude Desktop support. macOS DMG and Windows .exe installers auto-detect Claude Code and Claude Desktop.

**Workspace skills**: deal-intake, lease-strategy-papering, asset-ops-cockpit, capital-projects-development, fund-lp-reporting, navigator, plugin-admin. Persistent workspace state for cross-session continuity.

**Feedback system**: `/cre-skills:send-feedback` and `/cre-skills:report-problem` with automatic redaction, optional remote submission (ask_each_time mode), and retry outbox for failed sends.

Current counts live in [Key Stats](#key-stats) above; it is regenerated from the catalog by CI. See [CHANGELOG.md](CHANGELOG.md) for full history.

---

## Installation

This repo is a self-contained Claude marketplace. Choose the install method that fits your setup.

> See [docs/WHAT-TO-USE-WHEN.md](docs/WHAT-TO-USE-WHEN.md) for a detailed comparison of all install surfaces.

| Method | Best for | What you get |
|--------|----------|-------------|
| **Marketplace install** | Claude Code users (CLI or Desktop Code tab) | Full: skills, agents, commands, hooks, MCP tools |
| **macOS DMG** | Non-technical macOS users | Full plugin + Claude Desktop MCP registration |
| **Windows EXE** | Non-technical Windows users | Full plugin + Claude Desktop MCP registration |
| **Cowork upload** | Cowork tab users | Skills, agents, commands (no hooks/orchestrators) |
| **Manual config** | Chat tab only (MCP tools) | MCP tools via claude_desktop_config.json |

### Marketplace Install (recommended)

From Claude Code CLI or the Desktop Code tab:

```bash
claude plugin marketplace add mariourquia/cre-skills-plugin
claude plugin install cre-skills@cre-skills
```

Or interactively: type `/plugin` in Claude Code, select **Add plugin**, and search for `cre-skills`.

This gives you the full set of skills, agents, commands, hooks, and MCP tools.

### Installer (macOS DMG / Windows EXE)

Download from the [latest GitHub release](https://github.com/mariourquia/cre-skills-plugin/releases/latest):

- **macOS**: Download the `.dmg`, open it, double-click **CRE Skills Installer**
- **Windows**: Download the `.exe`, run the wizard (SmartScreen: click "More info" > "Run anyway")

The installer auto-detects Claude Desktop, Claude Code, or both and configures each. No admin privileges required. Restart Claude Desktop after installation.

### Cowork Tab

In the Claude Desktop Cowork tab, click **Customize** > **Browse plugins** to find CRE Skills, or upload the plugin ZIP from the release page. Skills, agents, and commands work in Cowork. Hooks and orchestrators are Code-tab only.

### CLI Alternatives

```bash
# Install script (downloads and registers automatically)
curl -fsSL https://raw.githubusercontent.com/mariourquia/cre-skills-plugin/main/scripts/install.sh | bash

# Local development
git clone https://github.com/mariourquia/cre-skills-plugin.git
claude --plugin-dir ./cre-skills-plugin
```

### What to Expect After Installation

Claude Desktop has three tabs. Each provides different capabilities:

| | Code Tab | Chat Tab | Cowork Tab |
|---|---|---|---|
| **Install method** | Marketplace or installer | Installer (MCP config) | Cowork plugin import |
| **Skills** | Yes, via `/cre-skills:*` | No (MCP tools instead) | Yes, via `/` commands |
| **Agents** | Yes, auto-invoked | No | Yes, as sub-agents |
| **Skill routing** | `/cre-skills:cre-route` | `cre_route` MCP tool | Manual |
| **Orchestrators** | `/cre-skills:orchestrate` | Not available | Not available |
| **Workspace** | Yes | Yes (MCP tools) | No |
| **Hooks** | Yes (session start/stop) | No | No |
| **Customization** | Yes | Yes (MCP tools) | No |

**Code tab** gives the full experience. **Chat tab** gives MCP tools. **Cowork tab** gives skills and agents without hooks or orchestrators.

### Verify Installation

After restarting, try:
```
/cre-skills:cre-route screen this deal
```

Or ask Claude: **"What CRE skills do you have?"**

For a structural check: `bash scripts/verify-install.sh`

### Troubleshooting

**Skills don't appear (Code tab):**
1. Start a new conversation (SessionStart hook fires at start)
2. Run `/plugin` to verify the plugin is enabled
3. If not listed: `claude plugin marketplace add mariourquia/cre-skills-plugin`

**MCP tools don't appear (Chat tab):**
1. Restart Claude Desktop completely
2. Check Settings > Developer > MCP Servers for `cre-skills`
3. Verify Node.js 18+ is installed (`node --version`)
4. Re-run the installer if the MCP entry is missing

**Cowork tab:**
1. Click Customize > Browse plugins to check if CRE Skills is installed
2. If not listed, upload the plugin ZIP from the release page

### Windows known issues

**Update Claude Code first.** Older versions of Claude Code on Windows have a bug where
colons in MCP log directory paths cause plugin MCP servers to fail silently
([anthropics/claude-code#13679](https://github.com/anthropics/claude-code/issues/13679)).
Update to the latest version before installing:

```powershell
npm i -g @anthropic-ai/claude-code@latest
# or: irm https://claude.ai/install.ps1 | iex
```

**Cowork marketplace empty on Windows.** The Cowork plugin marketplace may not load
because `plugins.claude.ai` does not resolve via DNS on some Windows configurations.
This is an Anthropic infrastructure issue
([anthropics/claude-code#28853](https://github.com/anthropics/claude-code/issues/28853)).
The plugin still works in the Code tab and CLI.

**Plugin installed but not showing.** If the installer completed but skills don't
appear, verify the plugin is enabled in `~/.claude/settings.json`:

```json
{
  "enabledPlugins": {
    "cre-skills@local": true
  }
}
```

The installer writes this automatically, but some Claude Code versions have a bug where
`enabledPlugins` is not populated
([anthropics/claude-code#20661](https://github.com/anthropics/claude-code/issues/20661)).

See [docs/INSTALL.md](docs/INSTALL.md) for detailed per-platform instructions.

---

## Quick Start

**Screen a deal in seconds:**

```
/cre-skills:cre-route screen this deal -- 240-unit garden-style multifamily,
Raleigh NC, $42M asking, 2018 vintage, 93% occupied, $2.6M NOI, rents 12% below market
```

**Underwrite with full depth:**

```
/cre-skills:cre-route underwrite this deal
```

**Review loan documents:**

```
/cre-skills:cre-route review these loan docs
```

**See all workflow chains:**

```
/cre-skills:cre-workflows
```

**Browse expert agents:**

```
/cre-skills:cre-agents
```

**Run an orchestrated pipeline:**

```
/cre-skills:orchestrate acquisition
```

**Set up brand guidelines (once):**

```
/cre-skills:brand-config
```

---

## Skill Categories

### By Category

| # | Category | Count | Key Skills |
|---|----------|-------|------------|
| 01 | **Deal Screening** | 2 | `deal-quick-screen`, `om-reverse-pricing` |
| 02 | **Underwriting & Analysis** | 4 | `acquisition-underwriting-engine`, `rent-roll-analyzer`, `sensitivity-stress-test`, `monte-carlo-return-simulator` |
| 03 | **Deal Structuring** | 6 | `loi-offer-builder`, `psa-redline-strategy`, `jv-waterfall-architect`, `1031-exchange-executor`, `creative-seller-financing`, `1031-pipeline-manager` |
| 04 | **Due Diligence** | 4 | `dd-command-center`, `distressed-acquisition-playbook`, `title-commitment-reviewer`, `tenant-credit-analyzer` |
| 05 | **Capital Markets** | 7 | `loan-sizing-engine`, `capital-stack-optimizer`, `refi-decision-analyzer`, `mezz-pref-structurer`, `debt-portfolio-monitor`, `workout-playbook`, `term-sheet-builder` |
| 06 | **Market Research** | 4 | `submarket-truth-serum`, `comp-snapshot`, `supply-demand-forecast`, `market-cycle-positioner` |
| 07 | **Asset Management** | 7 | `annual-budget-engine`, `property-performance-dashboard`, `capex-prioritizer`, `noi-sprint-plan`, `lease-compliance-auditor`, `tenant-delinquency-workout`, `small-operator-pm` |
| 08 | **Leasing** | 9 | `tenant-retention-engine`, `lease-up-war-room`, `lease-negotiation-analyzer`, `rent-optimization-planner`, `leasing-operations-engine`, `leasing-strategy-marketing-planner`, `lease-document-factory`, `lease-option-structurer`, `lease-trade-out-analyzer` |
| 09 | **Investor Relations** | 11 | `ic-memo-generator`, `quarterly-investor-update`, `lp-pitch-deck-builder`, `capital-raise-machine`, `fund-formation-toolkit`, `fund-operations-compliance-dashboard`, `investor-lifecycle-manager`, `sec-reg-d-compliance`, `distribution-notice-generator`, `emerging-manager-evaluator`, `fund-raise-negotiation-engine` |
| 10 | **Development** | 7 | `dev-proforma-engine`, `land-residual-hbu-analyzer`, `entitlement-feasibility`, `construction-budget-gc-analyzer`, `construction-project-command-center`, `construction-procurement-contracts-engine`, `post-close-onboarding-transition` |
| 11 | **Disposition** | 2 | `disposition-strategy-engine`, `disposition-prep-kit` |
| 12 | **Deal Sourcing** | 1 | `sourcing-outreach-system` |
| 13 | **Tax & Entity** | 3 | `cost-segregation-analyzer`, `opportunity-zone-underwriter`, `partnership-allocation-engine` |
| 14 | **ESG & Climate** | 2 | `carbon-audit-compliance`, `climate-risk-assessment` |
| 15 | **Portfolio Strategy** | 3 | `portfolio-allocator`, `performance-attribution`, `deal-attribution-tracker` |
| 16 | **Daily Operations** | 27 | `t12-normalizer`, `rent-roll-formatter`, `cam-reconciliation-calculator`, `debt-covenant-monitor`, `lease-abstract-extractor`, `estoppel-certificate-generator`, `cpi-escalation-calculator`, `variance-narrative-generator`, `closing-checklist-tracker`, `vendor-invoice-validator`, `property-tax-appeal-analyzer`, `coi-compliance-checker`, `work-order-triage`, `lender-compliance-certificate`, `stacking-plan-builder`, `building-systems-maintenance-manager`, `insurance-risk-manager`, `compliance-regulatory-response-kit`, `crisis-special-situations-playbook`, `property-operations-admin-toolkit`, `tenant-event-planner`, `loan-document-reviewer`, `transfer-document-preparer`, `funds-flow-calculator`, `gp-performance-evaluator`, `fund-terms-comparator`, `lp-data-request-generator` |

---

## Workflow Chains

Six end-to-end workflow chains that orchestrate multiple skills in sequence.

| # | Chain | Steps |
|---|-------|-------|
| 1 | **Acquisition Pipeline** | sourcing -> quick-screen -> om-reverse -> rent-roll-analyzer -> underwriting-engine -> sensitivity -> ic-memo -> loi -> psa-redline -> dd-command-center -> close |
| 2 | **Capital Stack Assembly** | underwriting-engine -> loan-sizing -> mezz-pref -> jv-waterfall -> capital-stack-optimizer -> refi-decision |
| 3 | **Hold Period Management** | annual-budget -> performance-dashboard -> capex / lease-compliance / delinquency-workout / retention-engine -> noi-sprint |
| 4 | **Disposition Pipeline** | performance-dashboard -> disposition-strategy -> [SELL] disposition-prep -> 1031-exchange \| [HOLD] refi-decision \| [REFI] loan-sizing |
| 5 | **Development Pipeline** | land-residual + entitlement -> dev-proforma -> construction-budget -> loan-sizing -> capital-stack -> ic-memo -> lease-up-war-room -> refi-decision |
| 6 | **Fund Management** | fund-formation -> pitch-deck -> capital-raise -> portfolio-allocator -> [deploy via acquisition pipeline] -> quarterly-update + performance-attribution |

Each chain has a detailed workflow document in `src/routing/workflows/` with step-by-step orchestration logic.

---

## Orchestration Engine

The plugin includes a multi-agent orchestration engine (derived from [Avi Hacker's CRE Acquisition Orchestrator](https://github.com/ahacker-1/cre-acquisition-orchestrator)) that coordinates skills into automated pipelines.

### Available Orchestrators

| Orchestrator | Purpose | Phases | Verdict |
|---|---|---|---|
| acquisition | Full acquisition lifecycle | DD -> UW -> Financing -> Legal -> Closing -> Challenge | GO / CONDITIONAL / NO-GO |
| capital-stack | Optimal debt/equity structuring | Qualification -> Sizing -> Structuring -> Optimization -> IC | PROCEED / RESTRUCTURE / KILL |
| hold-period | Asset management (recurring loop) | Onboarding -> Monitoring (loop) -> Leasing -> Capital -> Tenant -> Reposition | CONTINUE / INTERVENE / EXIT |
| disposition | Asset sale pipeline | Hold/Sell -> Pricing -> Marketing -> Buyers -> Offers -> DD Mgmt -> Close | SELL / HOLD / REFI |
| development | Ground-up development | Land -> Entitlement -> Proforma -> Construction -> Lease-Up -> Stabilization | BUILD / KILL / DEFER |
| fund-management | Full fund lifecycle | Formation -> Raise -> Deploy -> Monitor -> Distribute -> Exit | DEPLOY / HOLD / WIND-DOWN |
| research | Market intelligence | Macro -> Submarket -> Competitive -> Opportunity -> Memo | INVEST / MONITOR / PASS |
| strategy | Investment strategy formulation | Capital -> Cycle -> Strategy -> Portfolio -> Memo | DEPLOY / REVISE / HOLD |
| portfolio | Portfolio-level oversight | Composition -> Concentration -> Attribution -> Rebalance -> Stress -> Report | REBALANCE / HOLD / DIVEST |
| lp-intelligence | LP evaluation of GPs | GP Eval -> Data Request -> Performance -> Portfolio -> Re-Up | RE-UP / REDUCE / EXIT |

Run with: `/cre-skills:orchestrate acquisition`

See `src/orchestrators/README.md` for full documentation.

---

## Expert Agents

Expert agents across multiple categories, each with a distinct analytical perspective.

| Category | Count | Agents |
|----------|-------|--------|
| **Institutional Buyers** | 5 | Pension Fund, Private Equity, Public REIT, Family Office, Syndicator |
| **Analytical Lenses** | 5 | Quantitative, Qualitative, Contrarian, Risk Manager, ESG/Impact |
| **Investment Functions** | 8 | Acquisitions Analyst, Asset Manager, Property Manager, Capital Markets, IR Director, Development Manager, Leasing Director, Disposition Strategist |
| **Challenge Agents** | 6 | Conservative Lender, Aggressive GP, Skeptical LP, IC Challenger, Value-Add Operator, Distressed Specialist |
| **Titan Styles** | 6 | Zell, Linneman, Sternlicht, Ross, Gray, Barrack |
| **Stakeholder Views** | 8 | Tenant, Lender, Municipality, Insurance, Appraiser, Environmental, Construction, Legal |
| **Research & Strategy** | 4 | Market Research Analyst, Submarket Specialist, Chief Investment Officer, Portfolio Strategist |
| **Asset Management** | 2 | Asset Manager Lead, Leasing Manager |
| **Portfolio** | 2 | Portfolio Manager, Risk Officer |
| **Fund Management** | 2 | Fund Controller, Investor Relations Associate |
| **Disposition** | 1 | Disposition Manager |
| **LP Intelligence** | 3 | LP Advisor, Fund Analyst, Allocation Committee Member |
| **Composite** | 2 | CRE Veteran (generalist router), Deal Team Lead (multi-agent orchestrator) |

The **Deal Team Lead** agent assembles multi-agent teams from 10 pre-built compositions: Acquisition IC, Capital Stack Optimization, Disposition Strategy, Development Feasibility, Lease Negotiation, Fund Formation, Market Cycle Assessment, Crisis Response, Portfolio Review, and LP Due Diligence.

---

## Python Calculators

12 standalone Python scripts (zero external dependencies) that agents can execute for precise quantitative output.

| Script | Skill | Calculations |
|--------|-------|-------------|
| `quick_screen.py` | deal-quick-screen | Cap rate, DSCR, CoC, replacement ratio, 3-scenario IRR |
| `debt_sizing.py` | loan-sizing-engine | DSCR/LTV/debt yield constraint optimization |
| `covenant_tester.py` | loan-document-reviewer | DSCR/LTV/debt yield by year, breach detection |
| `npv_trade_out.py` | lease-trade-out-analyzer | NPV comparison, breakeven, 2D sensitivity grid |
| `option_valuation.py` | lease-option-structurer | Termination fees, cap rate impact, package NPV |
| `waterfall_calculator.py` | jv-waterfall-architect | GP/LP distributions, multi-tier promote, IRR |
| `tenant_credit_scorer.py` | tenant-credit-analyzer | HHI, WALT, expected annual loss, OCR |
| `proration_calculator.py` | funds-flow-calculator | Per diem prorations (actual/365, 30/360) |
| `transfer_tax.py` | transfer-document-preparer | All 50 states + DC with tiered rates |
| `monte_carlo_simulator.py` | monte-carlo-return-simulator | Stochastic return distributions, confidence intervals, tail risk |
| `fund_fee_modeler.py` | fund-raise-negotiation-engine | Management fee modeling, carried interest schedules, blended fee load, MFN cascade |

All calculators are in `src/calculators/`. Run directly with `python3 src/calculators/<script>.py`.

---

## Brand Guidelines

Skills that produce investor-facing deliverables (pitch decks, IC memos, investor updates, offering packages, leasing marketing materials) automatically load your brand guidelines from `~/.cre-skills/brand-guidelines.json`.

Run `/cre-skills:brand-config` to set up your brand colors, fonts, disclaimers, and contact info once. All future deliverables will use your brand automatically.

### What Gets Saved

| Setting | Description |
|---------|-------------|
| Company/fund name | Appears in all headers and footers |
| Primary, secondary, accent colors | Applied to formatting instructions |
| Heading and body fonts | Referenced in all layout directives |
| Layout style | `minimal`, `corporate`, `boutique`, or `institutional` |
| Number format | `full` ($1,234,567), `abbreviated` ($1.2M), or `both` |
| Units preference | `psf`, `per_unit`, or `auto` |
| Disclaimer text | Appended to every page/section |
| Confidentiality notice | Applied to cover pages |
| Contact information block | Placed on final page of deliverables |
| Logo file path | Referenced (not embedded) |

### Skills That Auto-Load Brand Guidelines

| Skill | Deliverable Type |
|-------|-----------------|
| `lp-pitch-deck-builder` | LP pitch decks (16-slide) |
| `ic-memo-generator` | Investment committee memos |
| `quarterly-investor-update` | Quarterly LP letters and reports |
| `capital-raise-machine` | LP packs, capital call notices, onboarding materials |
| `fund-formation-toolkit` | PPM drafting guidance, fund term materials |
| `disposition-prep-kit` | Offering packages, buyer marketing materials |
| `investor-lifecycle-manager` | LP meeting prep, benchmark reports, GIPS composites |
| `leasing-strategy-marketing-planner` | Leasing flyers, brochures, marketing plans |

### First-Use Behavior

On first invocation of any deliverable skill, if no brand guidelines file exists, the skill will prompt:

> "I don't have your brand guidelines saved yet. Would you like to set them up now with `/cre-skills:brand-config`? Or I can proceed with professional defaults."

Professional defaults: navy `#1B365D`, white `#FFFFFF`, gold accent `#C9A84C`, Helvetica Neue/Arial fonts, standard CRE disclaimer language.

---

## Feedback

Share feedback or report problems without leaving your session:

- `/cre-skills:send-feedback` -- share feedback about skill quality, missing capabilities, or general suggestions
- `/cre-skills:report-problem` -- report a bug with structured severity, reproduction context, and skill identification

Feedback is saved locally to `~/.cre-skills/feedback-log.jsonl`. Free-text fields are automatically sanitized (file paths, emails, digit sequences stripped). No deal data, prompts, or financial figures are ever stored. After submitting, you're asked if you'd also like to send it to the maintainer (you approve each send). To disable: set `feedback.mode` to `local_only` in `~/.cre-skills/config.json`.

View your feedback history with `/cre-skills:feedback-summary`.

---

## Skill Customization

Adapt any skill to how your team actually works. Local overrides take priority over base skills -- the base files are never modified.

```
/cre-skills:customize-skill
```

The plugin walks you through: select a skill, make changes, record why. Common customizations:

| Category | Example |
|----------|---------|
| Terminology | Rename fields to match your organization |
| Approval chain | Add compliance officer review steps |
| Required steps | Insert ESG screening into underwriting |
| Deliverable format | Restructure IC memo for your committee |
| Calculation method | Use MOIC instead of IRR as primary metric |
| Regional / market | Add NYC transfer tax tiers |

Customizations are stored at `~/.cre-skills/customizations/<slug>/` and persist across plugin updates. You can optionally share structured feedback about your changes with the maintainer to help improve the plugin.

**Privacy**: Default mode is `metadata_only` -- only skill name, change categories, and rationale are shared. No skill content leaves your machine without explicit consent. Set `customization.feedback_mode` to `off` in `~/.cre-skills/config.json` to disable entirely.

See [docs/customization-guide.md](docs/customization-guide.md) for full details, configuration examples, and MCP tool reference.

---

## Privacy & Telemetry

Anonymous usage telemetry is **enabled by default** and **local-only**. It records which skills you use (slug only) and the date -- nothing else. No deal data, financial figures, file paths, prompts, or identity information is ever tracked. All data stays on your machine in `~/.cre-skills/telemetry.jsonl`. To opt out: set `"telemetry": false` in `~/.cre-skills/config.json`.

- `/cre-skills:usage-stats` -- view your aggregated skill usage patterns
- `/cre-skills:feedback-summary` -- view your session ratings and comments
- `/cre-skills:send-feedback` -- share structured feedback (saved locally)
- `/cre-skills:report-problem` -- report bugs (saved locally)

See [PRIVACY.md](PRIVACY.md) for what is and is not collected.

---

## Project Structure

```
cre-skills-plugin/
  src/
    plugin/
      plugin.json            # Plugin manifest
    skills/
      <slug>/
        SKILL.md             # Skill definition (process, inputs, outputs)
        references/          # Supporting reference documents (.md and .yaml)
    agents/
      _index.md              # Agent roster and team compositions
      <agent>.md             # expert agent definitions (flat directory)
    orchestrators/
      engine/                # Pipeline engine schema and handoff registry
      configs/               # orchestrator JSON configurations
      prompts/               # orchestrator prompt files
      challenge-layer/       # Post-pipeline adversarial review config
      investor-profiles/     # 8 investor profiles + strategy matrix
      schemas/               # Disagreement and reversal trigger schemas
      thresholds.json        # Investment thresholds (base + investor overrides)
      README.md              # Orchestration engine documentation
    commands/
      cre-route.md           # Skill router command
      cre-workflows.md       # Workflow chain browser
      cre-agents.md          # Agent roster browser
      brand-config.md        # Brand guidelines setup
      customize-skill.md     # Skill customization workflow
      orchestrate.md         # Multi-agent pipeline orchestrator
      usage-stats.md         # Telemetry summary
      feedback-summary.md    # Session feedback log
      send-feedback.md       # Share feedback
      report-problem.md      # Report a bug
    lib/
      customization.mjs      # Skill override CRUD and resolution
      diff.mjs               # LCS-based line diff engine
      feedback-payload.mjs   # Customization feedback payload builder
    routing/
      CRE-ROUTING.md         # Master routing index
      workflows/             # Detailed workflow chain documents
    hooks/
      hooks.json             # Hook definitions (SessionStart, PostToolUse, Stop)
      telemetry-init.mjs     # Initializes user config on first run
      telemetry-capture.mjs  # Tracks skill invocations (opt-in)
      session-summary.mjs    # Session end record and feedback
    calculators/             # 12 Python calculator scripts
    catalog/                 # Catalog schema and canonical catalog.yaml
    mcp-server.mjs           # MCP server for Claude Desktop
    templates/
      output-styles/         # Output format templates
  scripts/
    redact-feedback.mjs    # Feedback sanitization utility
    install.sh             # Fresh install with v1->v2 migration
    update.sh              # Pull latest, detect breaking changes
    uninstall.sh           # Clean removal with data preservation
    verify-install.sh      # 7-check health report
  registry.yaml            # Skill registry with metadata and chain mappings
  tests/                   # pytest suite: structural integrity, catalog parity,
                           # release hygiene, docs/surface/version parity, MCP server,
                           # orchestrator engine (deal state, gates, calculator bridge),
                           # installer hardening, and end-to-end calculator exec
```

---

## Attribution

This release integrates orchestration patterns derived from the [CRE Acquisition Orchestrator](https://github.com/ahacker-1/cre-acquisition-orchestrator) by **Avi Hacker** ([The AI Consulting Network](https://www.theaiconsultingnetwork.com)), licensed under Apache 2.0. See [NOTICE](NOTICE) for full attribution.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding new skills, agents, and calculators.

---

## License

[Apache 2.0](LICENSE)

See [NOTICE](NOTICE) for attribution and patent grant details.

---

## Author

**Mario Urquia** -- [mariourquia.com](https://mariourquia.com)

Quant, Data, and Startup Product Builder. Building proof-of-concepts for commercial real estate investment management across equity, debt, and infrastructure.
