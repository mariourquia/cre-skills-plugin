# Target Compatibility Matrix

## Build Targets

| Target | Artifact | Host | Install Method |
|--------|----------|------|----------------|
| `cowork` | `cre-skills-cowork.zip` | Cowork | Plugin import |
| `claude-code` | `cre-skills-claude-code.zip` | Claude Code | `claude plugin install` or `--plugin-dir` |
| `raw-source` | Git repo | Development | Not for end-user install |

## Component Availability

| Component | Claude Code | Cowork | Notes |
|-----------|:-----------:|:------:|-------|
| Skills (112) | All fields | name+description only | Cowork strips slug, version, status, category, targets |
| Agents (54) | name, description | name, description, model, color | Cowork requires model+color (injected from defaults) |
| Commands (11) | All fields | No `name` field | Cowork forbids `name` in command frontmatter |
| Hooks (full) | All types | Prompt-only | Cowork gets no command-type hooks, no .mjs scripts |
| Orchestrators (10) | Included | Excluded | Cowork does not support orchestrator pipelines |
| MCP Server | Included | Excluded | Cowork uses native MCP |
| Calculators (12) | Included | Excluded | Python calculators not portable to Cowork |
| Routing | Included | Included | CRE-ROUTING.md and workflow chains |
| Catalog | Included | Included | catalog.yaml for metadata |
| Templates | Included | Included | Output styles and customization templates |
| Schemas | Included | Included | Validation schemas |
| Manifest | Full (with userConfig) | Stripped (no userConfig) | Cowork may not support userConfig |

## Agent Color Scheme (Cowork)

| Category | Color | Agents |
|----------|-------|--------|
| Default | blue | Most functional agents (acquisitions-analyst, portfolio-manager, etc.) |
| Titans | gold | titan-zell, titan-linneman, titan-sternlicht, titan-ross, titan-gray, titan-barrack |
| Challengers | red | aggressive-gp, conservative-lender, skeptical-lp, ic-challenger |
| Buyers | green | buyer-pension-fund, buyer-private-equity, buyer-reit, buyer-family-office, buyer-syndicator |
| Perspectives | purple | perspective-tenant, perspective-lender, perspective-municipality, perspective-insurance, perspective-appraiser, perspective-environmental, perspective-construction, perspective-legal |
| Lenses | teal | lens-contrarian, lens-esg-impact, lens-qualitative, lens-quantitative, lens-risk-manager |
