```
 ██████╗██████╗ ███████╗    ███████╗██╗  ██╗██╗██╗     ██╗     ███████╗
██╔════╝██╔══██╗██╔════╝    ██╔════╝██║ ██╔╝██║██║     ██║     ██╔════╝
██║     ██████╔╝█████╗      ███████╗█████╔╝ ██║██║     ██║     ███████╗
██║     ██╔══██╗██╔══╝      ╚════██║██╔═██╗ ██║██║     ██║     ╚════██║
╚██████╗██║  ██║███████╗    ███████║██║  ██╗██║███████╗███████╗███████║
 ╚═════╝╚═╝  ╚═╝╚══════╝    ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝

            ┌──┐                        ┌─────┐   ┌──┐
            │  │  ┌──┐    ┌───┐  ┌──┐   │     │   │  │     ┌─┐
       ┌──┐ │  │  │  │ ┌┐ │   │  │  │┌──┤     │┌──┤  │  ┌┐ │ │  ┌──┐
       │  │ │  │┌─┤  │ ││ │   │┌─┤  ││  │     ││  │  │┌─┤│ │ │┌─┤  │
    ┌──┤  │ │  ││ │  ├─┤│ │   ││ │  ││  │     ││  │  ││ ││ │ ││ │  │
  ──┤  │  ├─┤  ││ │  │ ││ │   ││ │  ││  │     ││  │  ││ ││ │ ││ │  ├──
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
```

# CRE Skills Plugin

A Claude plugin delivering **80 institutional-grade commercial real estate skills** that cover the full investment lifecycle -- from deal sourcing and screening through underwriting, structuring, due diligence, asset management, leasing, capital markets, investor relations, development, disposition, tax planning, ESG, portfolio strategy, and daily property operations. Each skill includes structured process logic, reference documents, and chain connections to other skills. Deploy as a plugin in Claude Code, Claude Desktop, or Claude.ai and get an entire CRE acquisitions shop in your terminal.

## Key Stats

| Metric | Count |
|--------|-------|
| Skills | **80** |
| Expert Agents | **40** |
| Reference Files | **171** |
| Workflow Chains | **6** |
| Skill Categories | **16** |
| Workflow Coverage | **~97%** |

---

## Installation

### Claude Code (CLI)

```bash
claude plugin add /path/to/cre-skills-plugin
# or from GitHub:
claude plugin add github:mariourquia/cre-skills-plugin
```

### One-Line Installer

```bash
curl -fsSL https://raw.githubusercontent.com/mariourquia/cre-skills-plugin/main/scripts/install.sh | bash
```

### macOS DMG (Double-Click Installer)

Download `cre-skills-v1.0.0.dmg` from the [latest release](https://github.com/mariourquia/cre-skills-plugin/releases/latest).

1. Open the DMG
2. Double-click "CRE Skills Installer"
3. Follow the Terminal prompts
4. Restart Claude Code or Claude Desktop

The installer automatically detects whether you have Claude Code, Claude Desktop, or both, and configures accordingly.

### Claude Desktop

The DMG installer (above) handles Claude Desktop configuration automatically. For manual setup, see [docs/install-desktop.md](docs/install-desktop.md).

### Claude.ai / Cowork (Team Environments)

For team deployment, add to your marketplace configuration or use managed settings.
See [docs/install-cowork.md](docs/install-cowork.md) for detailed instructions.

### Claude Code (local development)

```bash
git clone https://github.com/mariourquia/cre-skills-plugin.git
claude --plugin-dir ./cre-skills-plugin
```

---

## Quick Start

**Screen a deal in seconds:**

```
/cre-skills:deal-quick-screen

240-unit garden-style multifamily in Raleigh, NC. Asking $42M. 2018 vintage.
Current occupancy 93%. In-place NOI $2.6M. Broker says rents are 12% below market.
```

**See all workflow chains:**

```
/cre-skills:cre-workflows
```

**Browse expert agents:**

```
/cre-skills:cre-agents
```

---

## Skill Catalog

### By Category (16 subcategories)

| # | Category | Skills | Key Skills |
|---|----------|--------|------------|
| 01 | **Deal Screening** | 2 | `deal-quick-screen`, `om-reverse-pricing` |
| 02 | **Underwriting & Analysis** | 3 | `acquisition-underwriting-engine`, `rent-roll-analyzer`, `sensitivity-stress-test` |
| 03 | **Deal Structuring** | 5 | `loi-offer-builder`, `psa-redline-strategy`, `jv-waterfall-architect`, `1031-exchange-executor`, `creative-seller-financing` |
| 04 | **Due Diligence** | 2 | `dd-command-center`, `distressed-acquisition-playbook` |
| 05 | **Capital Markets** | 6 | `loan-sizing-engine`, `capital-stack-optimizer`, `refi-decision-analyzer`, `mezz-pref-structurer`, `debt-portfolio-monitor`, `workout-playbook` |
| 06 | **Market Research** | 4 | `submarket-truth-serum`, `comp-snapshot`, `supply-demand-forecast`, `market-cycle-positioner` |
| 07 | **Asset Management** | 6 | `annual-budget-engine`, `property-performance-dashboard`, `capex-prioritizer`, `noi-sprint-plan`, `lease-compliance-auditor`, `tenant-delinquency-workout` |
| 08 | **Leasing** | 7 | `tenant-retention-engine`, `lease-up-war-room`, `lease-negotiation-analyzer`, `rent-optimization-planner`, `leasing-operations-engine`, `leasing-strategy-marketing-planner`, `lease-document-factory` |
| 09 | **Investor Relations** | 5 | `ic-memo-generator`, `quarterly-investor-update`, `lp-pitch-deck-builder`, `capital-raise-machine`, `fund-formation-toolkit` |
| 10 | **Development** | 7 | `dev-proforma-engine`, `land-residual-hbu-analyzer`, `entitlement-feasibility`, `construction-budget-gc-analyzer`, `construction-project-command-center`, `construction-procurement-contracts-engine`, `post-close-onboarding-transition` |
| 11 | **Disposition** | 2 | `disposition-strategy-engine`, `disposition-prep-kit` |
| 12 | **Deal Sourcing** | 1 | `sourcing-outreach-system` |
| 13 | **Tax & Entity** | 3 | `cost-segregation-analyzer`, `opportunity-zone-underwriter`, `partnership-allocation-engine` |
| 14 | **ESG & Climate** | 2 | `carbon-audit-compliance`, `climate-risk-assessment` |
| 15 | **Portfolio Strategy** | 2 | `portfolio-allocator`, `performance-attribution` |
| 16 | **Daily Operations** | 23 | `t12-normalizer`, `rent-roll-formatter`, `cam-reconciliation-calculator`, `debt-covenant-monitor`, `lease-abstract-extractor`, `estoppel-certificate-generator`, `cpi-escalation-calculator`, `variance-narrative-generator`, `closing-checklist-tracker`, `vendor-invoice-validator`, `property-tax-appeal-analyzer`, `coi-compliance-checker`, `work-order-triage`, `lender-compliance-certificate`, `stacking-plan-builder`, `building-systems-maintenance-manager`, `fund-operations-compliance-dashboard`, `investor-lifecycle-manager`, `insurance-risk-manager`, `compliance-regulatory-response-kit`, `crisis-special-situations-playbook`, `property-operations-admin-toolkit`, `tenant-event-planner` |

---

## Agent Roster

40 expert agents across 8 categories, each with a distinct analytical perspective.

| Category | Count | Agents |
|----------|-------|--------|
| **Institutional Buyers** | 5 | Pension Fund, Private Equity, Public REIT, Family Office, Syndicator |
| **Analytical Lenses** | 5 | Quantitative, Qualitative, Contrarian, Risk Manager, ESG/Impact |
| **Investment Functions** | 8 | Acquisitions Analyst, Asset Manager, Property Manager, Capital Markets, IR Director, Development Manager, Leasing Director, Disposition Strategist |
| **Challenge Agents** | 6 | Conservative Lender, Aggressive GP, Skeptical LP, IC Challenger, Value-Add Operator, Distressed Specialist |
| **Titan Styles** | 6 | Zell, Linneman, Sternlicht, Ross, Gray, Barrack |
| **Stakeholder Views** | 8 | Tenant, Lender, Municipality, Insurance, Appraiser, Environmental, Construction, Legal |
| **Composite** | 2 | CRE Veteran (generalist router), Deal Team Lead (multi-agent orchestrator) |

The **Deal Team Lead** agent assembles multi-agent teams from 8 pre-built compositions: Acquisition IC, Capital Stack Optimization, Disposition Strategy, Development Feasibility, Lease Negotiation, Fund Formation, Market Cycle Assessment, and Crisis Response.

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

## Project Structure

```
cre-skills-plugin/
  .claude-plugin/
    plugin.json            # Plugin manifest
  skills/
    <slug>/
      SKILL.md             # Skill definition (process, inputs, outputs)
      references/          # Supporting reference documents
  agents/
    _index.md              # Agent roster and team compositions
    <agent>.md             # Individual agent definitions
  commands/
    cre-route.md           # Skill router command
    cre-workflows.md       # Workflow chain browser
    cre-agents.md          # Agent roster browser
  routing/
    CRE-ROUTING.md         # Master routing index
    workflows/             # Detailed workflow chain documents
  hooks/
    hooks.json             # Session start hook (loads routing context)
  registry.yaml            # Skill registry with metadata and chain mappings
```

---

## Contributing

### Adding a New Skill

1. Create `skills/<slug>/SKILL.md` with frontmatter (`name`, `slug`, `version`, `status`, `category`, `description`, `targets`).
2. Add reference files in `skills/<slug>/references/` as needed.
3. Add a routing entry in `routing/CRE-ROUTING.md` under the appropriate category.
4. Add a registry entry in `registry.yaml` with `chains_to` and `chains_from` mappings.
5. If the skill belongs to a workflow chain, update the relevant file in `routing/workflows/`.

### Adding a New Agent

1. Create `agents/<agent-name>.md` with the agent persona, evaluation framework, and output format.
2. Add the agent to `agents/_index.md` under the appropriate category.
3. If the agent fits a pre-built team composition, update the team definition in `_index.md`.

### PR Process

1. Branch from `main`: `git checkout -b feature/<skill-or-agent-name>`.
2. Add skill/agent files and update routing, registry, and index files.
3. Open a PR with a description of what the skill does and where it fits in the workflow chains.
4. Merge after review.

---

## License

[MIT](LICENSE)

---

## Author

**Mario Urquia** -- [mariourquia.com](https://mariourquia.com)

Quant, Data, and Startup Product Builder. Building proof-of-concepts for commercial real estate investment management across equity, debt, and infrastructure.
