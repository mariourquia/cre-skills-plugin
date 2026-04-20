# What to Use When

## What is this project?

CRE Skills Plugin is a structured knowledge base of institutional-grade commercial real estate skills, expert agents, Python calculators, and orchestrator pipelines (current counts: see the README's Key Stats). It installs as:

- a Claude Code plugin (core supported; CLI marketplace or local `--plugin-dir`),
- a local MCP server for the Claude Desktop Chat tab (core companion; DMG/EXE installer),
- a stripped plugin import for the Cowork tab (reduced secondary),
- a portable skill export for Codex / Gemini / Grok / Manus (experimental, no CI coverage).

See [`../README.md#release-maturity`](../README.md#release-maturity) for the support-tier table.

---

## Choose your install method

| If you use... | Install via... | What you get |
|---|---|---|
| **Claude Code (CLI or Desktop Code tab)** | `claude plugin marketplace add mariourquia/cre-skills-plugin` + `claude plugin install cre-skills@cre-skills` | Full plugin: skills, agents, workflow chains, orchestrators, slash commands, SessionStart hook, telemetry |
| **Claude Desktop Chat tab** | DMG (macOS) or EXE (Windows) installer from the [releases page](https://github.com/mariourquia/cre-skills-plugin/releases/latest) | Local MCP server with tools for routing, skill detail, workspace management, feedback |
| **Cowork tab** | Download `cre-skills-cowork.zip` from the [releases page](https://github.com/mariourquia/cre-skills-plugin/releases/latest), upload via Customize > Browse plugins | Skills + agents + commands only. No MCP server, no orchestrators, no calculators. |
| **Codex / Gemini / Grok / Manus / other agents** | Download `cre-skills-portable.zip`, extract `skills/` into your agent's skills directory | Experimental. Ships SKILL.md files only. A structural smoke test (`tests/install_smoke/test_portable_zip.py` + the `Portable ZIP Smoke` workflow) validates the ZIP layout, skills-tree mirroring, and frontmatter contract — but **cross-runtime invocation** (the skill actually loading and running inside Codex / Gemini / Grok / Manus) is not tested. Treat as unsupported until you verify it yourself on your runtime. |

---

## CLI marketplace vs Claude Desktop Chat tab "Add marketplace"

These are two different surfaces. Only one is supported by this repo. The paragraph below is the **canonical caveat** — it is duplicated verbatim in `README.md`, `docs/INSTALL.md`, `docs/install-guide.md`, `docs/install-desktop.md`, and `docs/install-cowork.md`, and a parity assertion in `tests/test_release_version_parity.py` fails if those copies drift from this source.

<!-- CANONICAL-CAVEAT:desktop-marketplace START -->
> **Do not paste this repo URL into Claude Desktop Chat tab's "Add marketplace" dialog.** Chat tab's "Add marketplace" is a separate surface and is **not supported by this repo** — pasting `https://github.com/mariourquia/cre-skills-plugin` there will produce a validation error. The canonical Chat tab install path is the DMG (macOS) or EXE (Windows) installer, which registers a local MCP server via `claude_desktop_config.json`. The Claude Code CLI marketplace (`claude plugin marketplace add mariourquia/cre-skills-plugin` followed by `claude plugin install cre-skills@cre-skills`) **is** supported and is the canonical CLI install path; it also works in the Desktop **Code** tab (which uses Claude Code under the hood).
<!-- CANONICAL-CAVEAT:desktop-marketplace END -->

If in doubt: if you are using the Claude Code CLI or the Desktop Code tab, use the marketplace. If you are using the Desktop Chat tab, use the DMG/EXE installer.

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
