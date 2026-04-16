# What to Use When

## What is this project?

CRE Skills Plugin is a structured knowledge base of institutional-grade commercial real estate skills, expert agents, Python calculators, and orchestrator pipelines (current counts: see the README's Key Stats). It plugs into Claude Code (CLI) via the plugin system and into Claude Desktop via a local MCP server. It is NOT a Claude Desktop marketplace plugin. Install it with the DMG/EXE installer or the Claude Code CLI -- not by pasting a URL into "Add marketplace."

---

## Choose your install method

| If you use... | Install via... | What you get |
|---|---|---|
| **Claude Code (CLI)** | `claude plugin install` or DMG/EXE installer | Full plugin: skills, agents, workflow chains, orchestrators, slash commands, SessionStart hook, telemetry |
| **Claude Desktop (app)** | DMG (macOS) or EXE (Windows) installer | MCP server with tools for routing, skill detail, workspace management, feedback |
| **Cowork** | Download `cre-skills-cowork.zip` from the latest [GitHub Release](https://github.com/mariourquia/cre-skills-plugin/releases/latest) | Stripped plugin: skills + agents + commands (no MCP server, no orchestrators, no calculators). Uses the same SKILL.md format recognized by Claude Code and Cowork. |

---

## Do NOT paste this repo URL into "Add marketplace"

Claude Desktop has an "Add marketplace" dialog that expects a specific manifest structure (`marketplace.json`). This repo does not have one and will never have one. Pasting `https://github.com/mariourquia/cre-skills-plugin` into that dialog will produce a validation error.

**The correct install path for Claude Desktop is the DMG or EXE installer from the GitHub Releases page.** The installer copies plugin files to the right location and registers the MCP server in Claude Desktop's config file automatically.

---

## What the installer does

Whether you run the DMG (macOS) or the EXE (Windows), the installer performs these steps:

1. **Detects** which Claude surfaces are installed (Claude Code, Claude Desktop, or both).
2. **Copies** the plugin source (`src/`) to the Claude plugin cache directory.
3. **Creates** `.claude-plugin/plugin.json` in the cache directory (not in the repo).
4. **Registers the MCP server** in Claude Desktop's config file (`claude_desktop_config.json`) so Desktop can call the CRE tools.
5. **Creates** `~/.cre-skills/` for user data (config, brand guidelines, workspaces, telemetry, feedback).

No data leaves your machine. No API keys are required. The MCP server runs locally via Node.js.

---

## What shows up in Claude Desktop

After installing and restarting Claude Desktop, the plugin appears as an **MCP server** named `cre-skills` in Settings > Developer > MCP Servers. It exposes tools that Claude can call automatically when you describe a CRE task in plain language.

You will NOT see slash commands (like `/cre-skills:cre-route`) in Claude Desktop. Slash commands are a Claude Code feature. In Desktop, you interact through natural conversation and Claude routes to the right skill via the MCP tools behind the scenes.

**Core MCP tools:**

| Tool | Purpose |
|------|---------|
| `cre_route` | Routes your prompt to the matching CRE skill |
| `cre_list_skills` | Browse and filter all skills |
| `cre_skill_detail` | Read the full structured process for any skill |
| `cre_workspace_create` | Start a persistent workspace for a deal or asset |
| `cre_workspace_get` | Resume a workspace from a prior session |
| `cre_workspace_update` | Add notes, decisions, or next actions to a workspace |
| `cre_send_feedback` | Report issues or suggest improvements |

You do not need to call these by name. Just describe what you need -- "screen this deal", "size a loan", "analyze this rent roll" -- and Claude picks the right tool.

---

## How orchestrators and workspace skills work

**Orchestrators** coordinate multiple skills into end-to-end pipelines. For example, the `acquisition` orchestrator runs due diligence, underwriting, financing, legal, closing, and challenge phases in sequence and produces a GO / CONDITIONAL / NO-GO verdict. Pipelines cover acquisitions, dispositions, development, fund management, portfolio oversight, and more.

Orchestrators are available in Claude Code via `/cre-skills:orchestrate <pipeline>`. They are NOT available in Claude Desktop or Cowork -- Desktop users can still access the individual skills that make up each pipeline, just not the automated multi-phase orchestration.

**Workspace skills** (deal-intake, lease-strategy-papering, asset-ops-cockpit, capital-projects-development, fund-lp-reporting, navigator, plugin-admin) provide persistent state that carries across sessions. Create a workspace for a deal, come back tomorrow, and resume where you left off. Workspaces are stored locally at `~/.cre-skills/workspaces/` and are available in both Claude Code and Claude Desktop.

---

## How to send feedback or report problems

**In Claude Code:**
- `/cre-skills:send-feedback` -- share feedback about skill quality, missing capabilities, or general suggestions
- `/cre-skills:report-problem` -- report a bug with structured severity and reproduction context

**In Claude Desktop:**
- Ask Claude: "Send feedback about the deal screening skill" or "Report a problem with loan sizing"
- Claude will use the `cre_send_feedback` MCP tool

**On GitHub:**
- Open an issue at [github.com/mariourquia/cre-skills-plugin/issues](https://github.com/mariourquia/cre-skills-plugin/issues)

All feedback is saved locally to `~/.cre-skills/feedback-log.jsonl` first. Free-text fields are automatically sanitized (file paths, emails, digit sequences stripped). You are asked before anything is sent remotely.
