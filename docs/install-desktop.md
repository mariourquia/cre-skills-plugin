# Installing CRE Skills Plugin -- Claude Desktop / Claude.ai

This guide covers installing the CRE Skills Plugin for Claude Desktop (the macOS/Windows app) and Claude.ai (the browser interface).

---

## Recommended: macOS DMG Installer

The simplest installation method for Claude Desktop users on macOS.

1. Download `cre-skills-v3.0.0.dmg` from the [latest release](https://github.com/mariourquia/cre-skills-plugin/releases/latest).
2. Open the DMG.
3. Double-click "CRE Skills Installer".
4. Follow the Terminal prompts. The installer detects whether you have Claude Code, Claude Desktop, or both, and configures each automatically.
5. Restart Claude Desktop.

After installation, start a new conversation and use `/cre-skills:cre-route` to verify the plugin is active.

If you prefer a manual approach or are on Windows, use one of the options below.

---

## Option A: Plugin Marketplace (When Available)

When the Claude plugin marketplace is live, this will be the simplest path.

1. Open Claude Desktop or navigate to claude.ai
2. Open **Settings** > **Plugins**
3. Search for **"CRE Skills"** or **"commercial real estate"**
4. Click **Install**
5. The plugin loads automatically in all new conversations

<!-- Screenshot placeholder: marketplace search results showing cre-skills plugin -->
<!-- Screenshot placeholder: plugin detail page with Install button -->

---

## Option B: Manual Plugin Loading

Until the marketplace is available, load the plugin manually.

### Prerequisites

- Claude Desktop installed (macOS or Windows), or a Claude.ai Pro/Team account
- Git installed on your machine

### Steps

**1. Clone the repository**

```bash
git clone https://github.com/mariourquia/cre-skills-plugin.git
```

Note where you cloned it. Example: `~/Documents/GitHub/cre-skills-plugin`

**2. Open Claude Desktop settings**

- macOS: **Claude** menu > **Settings** > **Plugins**
- Windows: **File** menu > **Settings** > **Plugins**

<!-- Screenshot placeholder: Claude Desktop Settings window with Plugins tab -->

**3. Add the plugin directory**

Click **Add Plugin** (or **Load from Disk**) and select the cloned `cre-skills-plugin` directory.

<!-- Screenshot placeholder: file picker selecting the plugin directory -->

**4. Confirm the plugin is loaded**

After adding, you should see `cre-skills` in your plugin list with status **Active**.

<!-- Screenshot placeholder: plugin list showing cre-skills as Active -->

**5. Restart the conversation**

Start a new conversation. The SessionStart hook will load the CRE routing index automatically.

---

## Using Skills Once Installed

All skills are under the `/cre-skills:` namespace. Three entry points:

### `/cre-skills:cre-route`

The main router. Describe your task and it finds the right skill.

```
/cre-skills:cre-route quick screen this deal
/cre-skills:cre-route size a loan for a $15M multifamily
/cre-skills:cre-route normalize this T-12
```

### `/cre-skills:cre-workflows`

Browse the 6 end-to-end workflow chains that connect multiple skills into a pipeline:

- Deal Pipeline (Acquisition)
- Capital Stack Assembly
- Hold Period Management
- Disposition Pipeline
- Development Pipeline
- Fund Management

### `/cre-skills:cre-agents`

List the 55 expert subagents organized by category:

- **Investment Function** (8): Acquisitions analyst, asset manager, capital markets, etc.
- **Adversarial / Challenge** (6): Conservative lender, IC challenger, skeptical LP, etc.
- **Titan Thinking-Style** (6): Channel Zell, Linneman, Sternlicht, Ross, Gray, Barrack
- **Stakeholder Perspective** (8): Tenant, lender, municipality, appraiser, etc.
- **Institutional Buyer** (5): Pension fund, PE, REIT, family office, syndicator
- **Analytical Lens** (5): Quantitative, qualitative, contrarian, risk, ESG
- **Composite** (2): CRE veteran, deal team lead

---

## How It Works

The plugin does not run any code. It is a structured knowledge base:

- **105 SKILL.md files**: Each defines a specific CRE workflow step with trigger conditions, input schema, step-by-step process, output format, red flags, and chain notes pointing to the next skill.
- **55 agent definitions**: Expert personas with analytical frameworks, key questions, and output styles.
- **Routing index**: Maps natural language requests to the right skill without loading all 105 skill files.
- **SessionStart hook**: Injects a brief system prompt telling Claude the plugin is active and where to find the routing index.

No API keys, no external services, no data leaves your conversation.

---

## Updating

To update to the latest version:

```bash
cd path/to/cre-skills-plugin
git pull
```

Then restart Claude Desktop or start a new conversation.

---

## Troubleshooting

**Skills not appearing**: Make sure you started a new conversation after adding the plugin. The SessionStart hook only fires at conversation start.

**Commands not recognized**: Verify the plugin shows as Active in Settings > Plugins. If it shows an error, check that the `.claude-plugin/plugin.json` file exists in the repo root.

**Wrong skill activated**: Use `/cre-skills:cre-route` with a description of your task. The router matches against 80+ trigger patterns. If the match is ambiguous, it will present 2-3 options.
