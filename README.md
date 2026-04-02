```
 ██████╗██████╗ ███████╗    ███████╗██╗  ██╗██╗██╗     ██╗     ███████╗
██╔════╝██╔══██╗██╔════╝    ██╔════╝██║ ██╔╝██║██║     ██║     ██╔════╝
██║     ██████╔╝█████╗      ███████╗█████╔╝ ██║██║     ██║     ███████╗
██║     ██╔══██╗██╔══╝      ╚════██║██╔═██╗ ██║██║     ██║     ╚════██║
╚██████╗██║  ██║███████╗    ███████║██║  ██╗██║███████╗███████╗███████║
 ╚═════╝╚═╝  ╚═╝╚══════╝    ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝

                                            ╔═╗
                                     ┌─┐    ║ ║  ┌─┐
                              ┌──┐   │ │    ║ ║  │ │
                     ┌───┐    │  │   │ │ ┌┐ ║ ║  │ │ ┌──┐
              ┌──┐   │   │ ┌┐ │  │┌──┤ │ ││ ║ ║  │ │ │  │   ┌─┐
         ┌──┐ │  │   │   │ ││ │  ││  │ │ ││ ║ ║┌─┤ │ │  │┌──┤ │
    ┌─┐  │  │ │  │┌──┤   │ ││ │  ││  │ │ ││ ║ ║│ │ │ │  ││  │ │  ┌─┐
    │ │  │  │ │  ││  │   │ ││ │  ││  │ │ ││ ║ ║│ │ │ │  ││  │ │  │ │
  ──┤ ├──┤  ├─┤  ││  │   ├─┤│ │  ││  │ ├─┤│ ║ ║│ │ ├─┤  ││  │ ├──┤ ├──
  ░░│B├░░│R├░│O├░│O├░│K├░│L├│Y│N│░░░░░░║M║A║N║H║A║T║T║A║N║░░░░░░░░░░░░
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  ░░░░░░░░░░░░≈≈≈≈≈≈≈≈≈ EAST  RIVER ≈≈≈≈≈≈≈≈≈░░░░░░░░░░░░░░░░░░░░░░░░░░
```

# CRE Skills Plugin

A Claude plugin delivering **112 institutional-grade commercial real estate skills** covering the full investment lifecycle -- deal sourcing, screening, underwriting, structuring, due diligence, capital markets, market research, asset management, leasing, investor relations, development, disposition, tax planning, ESG, portfolio strategy, and daily property operations. Each skill includes structured process logic, reference documents, chain connections to other skills, and Python calculators for precise quantitative output. Deploy as a plugin in Claude Code, Claude Desktop, or Claude.ai and get an entire CRE PE shop in your terminal.

## Key Stats

<!-- CATALOG:STATS:START -->
| Metric | Count |
|--------|-------|
| Skills | **112** |
| Expert Agents | **54** |
| Reference Files | **247** |
| Python Calculators | **12** |
| Workflow Chains | **6** |
| Orchestrator Pipelines | **10** |
| Slash Commands | **9** |
| Skill Categories | **18** |
<!-- CATALOG:STATS:END -->

---

## What's New in v4.1.0

**Feedback system**: `/cre-skills:send-feedback` and `/cre-skills:report-problem` for structured feedback without leaving your session. Submissions are saved locally with automatic redaction (file paths, emails, digit sequences, env vars stripped). Optional remote submission to the maintainer (ask_each_time mode -- you confirm each send).

**Weekly feedback prompt**: Brief, non-intrusive reminder at session end after 7+ days of use. Shown once per week, only when CRE skills were used. No opt-in required.

**112 skills, 54 agents, 12 calculators, 9 commands**: Full counts after prior additions (construction estimator, PM orchestrator, space planning) plus v4.1.0 catalog, MCP server, workspace skills.

**Claude Desktop support**: macOS DMG and Windows .exe installers auto-detect Claude Code and Claude Desktop. Both platforms fully supported.

See [CHANGELOG.md](CHANGELOG.md) for full history.

---

## Installation

### Claude Code (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/mariourquia/cre-skills-plugin/main/scripts/install.sh | bash
```

Or for a single session:

```bash
claude --plugin-dir /path/to/cre-skills-plugin
```

### One-Line Installer

```bash
curl -fsSL https://raw.githubusercontent.com/mariourquia/cre-skills-plugin/main/scripts/install.sh | bash
```

### macOS DMG (Double-Click Installer)

Download `cre-skills-v4.1.0.dmg` from the [latest release](https://github.com/mariourquia/cre-skills-plugin/releases/latest).

1. Open the DMG
2. Double-click "CRE Skills Installer"
3. Follow the Terminal prompts
4. Restart Claude Code or Claude Desktop

The installer automatically detects whether you have Claude Code, Claude Desktop, or both, and configures accordingly.

### Windows .exe Installer

Download `cre-skills-v4.1.0-setup.exe` from the [latest release](https://github.com/mariourquia/cre-skills-plugin/releases/latest).

1. Run the installer (SmartScreen warning: click "More info" > "Run anyway")
2. Follow the wizard
3. Restart Claude Code or Claude Desktop

The installer detects Claude Code CLI and Claude Desktop and configures both automatically. No admin privileges required.

### Manual (Local Development)

```bash
git clone https://github.com/mariourquia/cre-skills-plugin.git
claude plugin add ./cre-skills-plugin
```

### Verify Installation

```bash
./scripts/verify-install.sh
```

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

### By Category (16 subcategories, 105 skills)

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

Each chain has a detailed workflow document in `routing/workflows/` with step-by-step orchestration logic.

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

See `orchestrators/README.md` for full documentation.

---

## Expert Agents

54 expert agents across 13 categories, each with a distinct analytical perspective.

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

All calculators are in `scripts/calculators/`. Run directly with `python3 scripts/calculators/<script>.py`.

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
  .claude-plugin/
    plugin.json            # Plugin manifest
  skills/
    <slug>/
      SKILL.md             # Skill definition (process, inputs, outputs)
      references/          # Supporting reference documents (.md and .yaml)
  agents/
    _index.md              # Agent roster and team compositions
    <agent>.md             # 54 expert agent definitions (flat directory)
  orchestrators/
    engine/                # Pipeline engine schema and handoff registry
    configs/               # 10 orchestrator JSON configurations
    prompts/               # 16 orchestrator prompt files
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
    orchestrate.md         # Multi-agent pipeline orchestrator
    usage-stats.md         # Telemetry summary
    feedback-summary.md    # Session feedback log
    send-feedback.md       # Share feedback
    report-problem.md      # Report a bug
  routing/
    CRE-ROUTING.md         # Master routing index
    workflows/             # Detailed workflow chain documents
  hooks/
    hooks.json             # Hook definitions (SessionStart, PostToolUse, Stop)
    telemetry-init.mjs     # Initializes user config on first run
    telemetry-capture.mjs  # Tracks skill invocations (opt-in)
    session-summary.mjs    # Session end record and feedback
  scripts/
    calculators/           # 12 Python calculator scripts
    redact-feedback.mjs    # Feedback sanitization utility
    install.sh             # Fresh install with v1->v2 migration
    update.sh              # Pull latest, detect breaking changes
    uninstall.sh           # Clean removal with data preservation
    verify-install.sh      # 7-check health report
  registry.yaml            # Skill registry with metadata and chain mappings
  tests/                   # 9 structural integrity tests (pytest)
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
