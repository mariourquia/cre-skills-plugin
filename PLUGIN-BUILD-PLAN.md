# CRE Skills Plugin: Build Plan

## Plugin Identity

- **Name**: `cre-skills`
- **Namespace**: Skills invoked as `/cre-skills:deal-quick-screen`, `/cre-skills:loan-sizing-engine`, etc.
- **Repo**: `github.com/mariourquia/cre-skills-plugin`
- **License**: MIT

## Directory Structure

```
cre-skills-plugin/
├── .claude-plugin/
│   └── plugin.json                    # Manifest
├── skills/                            # 83 skill packs (auto-discovered)
│   ├── deal-quick-screen/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── screening-rubric.yaml
│   │       ├── replacement-cost-benchmarks.yaml
│   │       └── worked-screening-example.yaml
│   ├── loan-sizing-engine/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── loan-sizing-formulas.md
│   │       ├── lender-comparison-matrix.yaml
│   │       └── worked-sizing-examples.yaml
│   └── ... (81 more skill packs)
├── commands/                          # Slash commands
│   ├── cre-route.md                   # Main entry: routing index lookup
│   ├── cre-workflows.md               # Show workflow chains
│   └── cre-agents.md                  # List available expert agents
├── agents/                            # 40+ expert subagent definitions
│   ├── _index.md                      # Agent roster index
│   │
│   │ # Investment Function Agents (8)
│   ├── acquisitions-analyst.md
│   ├── asset-manager.md
│   ├── property-manager.md
│   ├── capital-markets-specialist.md
│   ├── investor-relations-director.md
│   ├── development-manager.md
│   ├── leasing-director.md
│   ├── disposition-strategist.md
│   │
│   │ # Adversarial / Challenge Agents (6)
│   ├── conservative-lender.md
│   ├── aggressive-gp.md
│   ├── skeptical-lp.md
│   ├── ic-challenger.md
│   ├── value-add-operator.md
│   ├── distressed-specialist.md
│   │
│   │ # Titan Thinking-Style Agents (6)
│   ├── titan-zell.md                  # Contrarian: buy when blood is in the streets
│   ├── titan-linneman.md              # Academic rigor: first principles, no shortcuts
│   ├── titan-sternlicht.md            # Brand + design + hospitality lens
│   ├── titan-ross.md                  # Development + mixed-use + placemaking
│   ├── titan-gray.md                  # Scale + data-driven + Blackstone playbook
│   ├── titan-barrack.md               # Relationships + timing + emerging markets
│   │
│   │ # Stakeholder Perspective Agents (8)
│   ├── perspective-tenant.md          # Total occupancy cost, space quality, flexibility
│   ├── perspective-lender.md          # Credit risk, collateral, covenant protection
│   ├── perspective-municipality.md    # Zoning, tax revenue, community impact, affordable housing
│   ├── perspective-insurance.md       # Risk classification, loss exposure, premium trajectory
│   ├── perspective-appraiser.md       # Valuation methodology, comparable selection, USPAP
│   ├── perspective-environmental.md   # Compliance, remediation, climate transition
│   ├── perspective-construction.md    # Buildability, cost, schedule, means & methods
│   ├── perspective-legal.md           # Contract risk, regulatory exposure, entity structure
│   │
│   │ # Institutional Buyer Agents (5)
│   ├── buyer-pension-fund.md          # Long hold, low leverage, stable income, ODCE mandate
│   ├── buyer-private-equity.md        # 3-5yr hold, value-add/opportunistic, promote-driven
│   ├── buyer-reit.md                  # FFO accretion, portfolio fit, NAV impact
│   ├── buyer-family-office.md         # Generational wealth, tax efficiency, direct ownership
│   ├── buyer-syndicator.md            # Investor returns, fee generation, repeat capital
│   │
│   │ # Analytical Lens Agents (5)
│   ├── lens-quantitative.md           # Pure numbers: IRR, NPV, sensitivity, Monte Carlo
│   ├── lens-qualitative.md            # Market narrative, demographic trends, tenant quality
│   ├── lens-contrarian.md             # What everyone else is missing, consensus is wrong
│   ├── lens-risk-manager.md           # Downside protection, tail risk, insurance, hedging
│   ├── lens-esg-impact.md             # Climate, social impact, governance, GRESB, TCFD
│   │
│   │ # Composite / Orchestration Agents (2)
│   ├── cre-veteran.md                 # General-purpose CRE domain expert
│   └── deal-team-lead.md              # Orchestrates other agents into deal teams
│
├── hooks/
│   └── hooks.json                     # SessionStart loads routing index
├── routing/
│   ├── CRE-ROUTING.md                # Trigger-to-skill routing index
│   └── workflows/                     # 6 workflow chain docs
│       ├── deal-pipeline-acquisition.md
│       ├── capital-stack-assembly.md
│       ├── hold-period-management.md
│       ├── disposition-pipeline.md
│       ├── development-pipeline.md
│       └── fund-management.md
├── registry.yaml                      # Machine-readable skill index
├── LICENSE                            # MIT
└── README.md                          # Installation + usage
```

## Build Script

The build script copies files from `~/.claude/skills-lab/` into the plugin structure.
It does NOT rewrite content -- just copies and reorganizes.

```bash
#!/bin/bash
# build-plugin.sh -- Assembles the CRE skills plugin from skills-lab

PLUGIN_DIR="$HOME/Documents/GitHub/cre-skills-plugin"
SKILLS_LAB="$HOME/.claude/skills-lab"

# 1. Create structure
mkdir -p "$PLUGIN_DIR"/{.claude-plugin,commands,agents,hooks,routing/workflows}

# 2. Copy all 83 CRE skill packs (SKILL.md + references/)
for slug in $(ls "$SKILLS_LAB/skills/" | grep -v -E '^(agent-planner|agent-team|architecture|article|assignment|award|backtest|ci-actions|code-review|concept|data-product|email|experiment|factor|feedback|file-org|flipper|idea|interrogator|interviewme|lesson|life-dec|literature|memo-invest|model-cap|model-sel|mortgage|nyc-doe|paper|points|project|puzzle|question|rag-rigor|release|research|security|skill-dep|skill-main|stakes|stern|team-of)$'); do
    cp -r "$SKILLS_LAB/skills/$slug" "$PLUGIN_DIR/skills/"
done

# 3. Copy routing and workflow files
cp "$SKILLS_LAB/CRE-ROUTING.md" "$PLUGIN_DIR/routing/"
cp "$SKILLS_LAB/plans/reit-cre/_workflows/"*.md "$PLUGIN_DIR/routing/workflows/"
cp "$SKILLS_LAB/plans/reit-cre/_registry.yaml" "$PLUGIN_DIR/registry.yaml"

# 4. Agents are written fresh (not copied -- they don't exist in skills-lab)
# 5. Commands are written fresh (plugin-specific)
# 6. Hooks are written fresh (plugin-specific)
```

## Agent Roster Design

### Investment Function Agents (8)
Role-based experts who analyze from their professional function's perspective.

| Agent | Perspective | When to Deploy |
|---|---|---|
| acquisitions-analyst | Buy-side: screening, underwriting, pricing, DD | Deal screening, underwriting, LOI, DD |
| asset-manager | Hold-period: NOI improvement, capex, tenant mgmt | Budgeting, performance review, capex planning |
| property-manager | Operations: maintenance, leasing, tenant relations | Work orders, inspections, tenant issues |
| capital-markets-specialist | Debt: sizing, structuring, hedging, workouts | Loan sizing, refi, cap stack, debt monitoring |
| investor-relations-director | LP-facing: reporting, fundraising, compliance | Investor updates, pitch decks, fund formation |
| development-manager | Build: proforma, entitlements, construction, CO | Development deals, construction management |
| leasing-director | Revenue: tenant mix, comps, concessions, retention | Lease-up, renewals, negotiations |
| disposition-strategist | Exit: timing, positioning, buyer universe, tax | Sell/hold/refi decisions, disposition prep |

### Adversarial / Challenge Agents (6)
Devil's advocate perspectives for stress-testing decisions.

| Agent | Bias | Use Case |
|---|---|---|
| conservative-lender | Sees every risk, demands coverage | Stress-test deal assumptions |
| aggressive-gp | Sees upside everywhere, minimizes risk | Challenge overly conservative analysis |
| skeptical-lp | Questions fees, alignment, transparency | Review investor-facing materials |
| ic-challenger | Pokes holes in every assumption | Pre-IC memo stress test |
| value-add-operator | Sees operational upside others miss | Identify hidden value creation |
| distressed-specialist | Sees opportunity in chaos | Evaluate workout/distressed scenarios |

### Titan Thinking-Style Agents (6)
Channel the decision-making frameworks of CRE legends.

| Agent | Style | Key Question They Ask |
|---|---|---|
| titan-zell | Contrarian, go where others won't | "What's the replacement cost and why is everyone afraid?" |
| titan-linneman | Academic rigor, first principles | "What does the math actually say when you strip away the narrative?" |
| titan-sternlicht | Brand, design, experience | "How does this property make people feel and what's that worth?" |
| titan-ross | Development, placemaking, mixed-use | "What could this become with the right vision and entitlements?" |
| titan-gray | Scale, data, institutional playbook | "Can we do this 100 times and what does the data say about the pattern?" |
| titan-barrack | Relationships, timing, global macro | "Who do we know and where are we in the cycle?" |

### Stakeholder Perspective Agents (8)
External viewpoints that deals must satisfy.

### Institutional Buyer Agents (5)
How different buyer types evaluate the same asset.

### Analytical Lens Agents (5)
Different ways to frame the same analysis.

### Composite Agents (2)
- **cre-veteran**: General-purpose domain expert, routes to specific agents
- **deal-team-lead**: Orchestrates multi-agent teams for complex tasks, selects from the roster based on task type

## Agent Team Compositions

Pre-built team configurations that skills can reference:

| Team | Task | Agents |
|---|---|---|
| Acquisition IC | Pre-IC deal review | acquisitions-analyst, conservative-lender, ic-challenger, titan-linneman, perspective-tenant |
| Capital Stack | Financing structure | capital-markets-specialist, conservative-lender, aggressive-gp, perspective-lender |
| Disposition Review | Sell/hold/refi | disposition-strategist, asset-manager, buyer-pension-fund, buyer-private-equity, lens-quantitative |
| Development Feasibility | Go/no-go on development | development-manager, perspective-municipality, perspective-construction, titan-ross, lens-risk-manager |
| Lease Negotiation | Complex lease deal | leasing-director, perspective-tenant, perspective-legal, asset-manager |
| Fund Formation | New fund launch | investor-relations-director, skeptical-lp, buyer-family-office, perspective-legal, lens-esg-impact |
| Market Cycle | Investment timing | titan-zell, titan-barrack, titan-gray, lens-contrarian, lens-quantitative |
| Crisis Response | Special situations | distressed-specialist, perspective-legal, conservative-lender, perspective-environmental |

## Next Steps

1. Run build-plugin.sh to copy skill files
2. Write all 40 agent .md files
3. Write plugin.json manifest
4. Write commands (cre-route, cre-workflows, cre-agents)
5. Write hooks.json (SessionStart loads routing)
6. Write README.md with installation instructions
7. Write LICENSE (MIT)
8. Test with `claude --plugin-dir ./cre-skills-plugin`
9. Push to GitHub
10. Submit to marketplace
