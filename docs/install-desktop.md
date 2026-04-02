# Installing CRE Skills Plugin -- Claude Desktop

This guide is for Claude Desktop users on macOS and Windows. If you use Claude Code CLI, see the [main install guide](install-guide.md).

---

## macOS

Download [`cre-skills-v4.0.0.dmg`](https://github.com/mariourquia/cre-skills-plugin/releases/latest) from the latest release.

1. Open the DMG in Finder
2. Double-click **CRE Skills Installer**
3. A Terminal window opens -- follow the prompts (no commands to type)
4. Restart Claude Desktop

The installer:
- Copies the plugin to `~/.claude/plugins/`
- Registers the MCP server in Claude Desktop's config
- Detects if you also have Claude Code and configures both

## Windows

Download [`cre-skills-v4.0.0-setup.exe`](https://github.com/mariourquia/cre-skills-plugin/releases/latest) from the latest release.

1. Run the installer. Windows SmartScreen may warn you -- click **More info**, then **Run anyway** (the installer is not code-signed yet; you can verify the SHA256 checksum from the release page)
2. Follow the wizard. Default location: `%APPDATA%\cre-skills-plugin`
3. Restart Claude Desktop

No admin privileges required. The installer detects Claude Desktop and Claude Code and configures both.

---

## After Installation

Restart Claude Desktop, then start a new conversation. The plugin's MCP server gives Claude 21 tools it can call automatically. Core tools:

| Tool | What it does | Example prompt |
|------|-------------|----------------|
| `cre_route` | Routes your request to the right CRE skill | "Screen this deal -- 240-unit multifamily, Raleigh, $42M" |
| `cre_list_skills` | Browse and filter the 112 skills | "What leasing skills do you have?" |
| `cre_skill_detail` | Read the full process for a skill | "Show me the full deal-quick-screen process" |
| `cre_workspace_create` | Start tracking a deal or asset | "Create a workspace for the Raleigh deal" |
| `cre_workspace_get` | Resume a workspace from a prior session | "Load my Raleigh deal workspace" |
| `cre_workspace_list` | See all your active workspaces | "List my workspaces" |
| `cre_workspace_update` | Add notes, decisions, next actions | "Update the Raleigh workspace with today's findings" |
| `cre_send_feedback` | Report issues or suggest improvements | "Send feedback about the deal screening skill" |

You do not need to call these tools by name. Just describe your CRE task in plain language and Claude will use the right tool automatically.

### Example Prompts for Desktop Users

**Deal screening:**
> Screen this deal -- 240-unit garden-style multifamily in Raleigh NC, $42M asking, 2018 vintage, 93% occupied, $2.6M NOI, rents 12% below market

**Loan sizing:**
> Size a loan for a $15M multifamily acquisition at 65% LTV

**Lease analysis:**
> Analyze the rent roll I pasted above and flag rollover risk

**Market research:**
> Give me a submarket brief for downtown Austin office

**Underwriting:**
> Walk me through a full acquisition underwriting for this deal

Claude will route each prompt to the appropriate specialist skill, which provides a structured process, red flags, and follow-up recommendations.

---

## How It Works

The MCP server (`mcp-server.mjs`) runs locally on your machine. No data leaves your computer. No API keys required.

When you ask Claude a CRE question in Desktop:
1. Claude calls `cre_route` to find the matching skill
2. Claude reads the skill's full process via `cre_skill_detail`
3. Claude follows the structured steps to produce institutional-grade output
4. If you create a workspace, state persists at `~/.cre-skills/workspaces/` for future sessions

The plugin itself is a structured knowledge base (112 process documents, 247 reference files, 54 expert agent definitions). Claude reads these docs to guide its analysis -- no external services or AI models beyond Claude itself.

---

## Claude Desktop vs Claude Code

| Feature | Desktop | Code |
|---------|---------|------|
| Skills available | 112 (via MCP routing) | 112 (via slash commands) |
| How you invoke skills | Plain language prompts | `/cre-skills:cre-route` or slash commands |
| Auto-routing on session start | No -- ask Claude directly | Yes -- SessionStart hook loads router |
| Persistent workspaces | Yes | Yes |
| Telemetry | Not collected | Opt-out (local only) |
| Feedback commands | Via MCP tool | Via `/cre-skills:send-feedback` |
| Python calculators | Requires Node.js | Requires Node.js + Python 3.10+ |
| Output styles | Not yet supported | 5 styles (exec-brief, ic-memo, etc.) |

Both platforms access the same 112 skills. Desktop users just interact through natural conversation instead of slash commands.

---

## Updating

Download the latest DMG or EXE from the [releases page](https://github.com/mariourquia/cre-skills-plugin/releases) and run the installer again. Your workspaces and settings at `~/.cre-skills/` are preserved across updates.

---

## Troubleshooting

**MCP tools not showing up:**
- Restart Claude Desktop after installation
- Check that `cre-skills` appears in Claude Desktop's MCP server list (Settings > Developer > MCP Servers)
- Verify Node.js 18+ is installed: open Terminal and run `node --version`

**"cre-skills" not in MCP list:**
- The installer writes to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows)
- Check that the file contains a `"cre-skills"` entry under `"mcpServers"`
- If missing, add manually:
  ```json
  {
    "mcpServers": {
      "cre-skills": {
        "command": "node",
        "args": ["/path/to/cre-skills-plugin/mcp-server.mjs"]
      }
    }
  }
  ```

**Skills seem to give generic responses:**
- Make sure you are describing a specific CRE task, not asking a general question
- Try: "Screen this deal -- [property details]" instead of "Tell me about CRE"
- The routing works best with concrete deal parameters

**Windows SmartScreen blocks the installer:**
- Click "More info" then "Run anyway"
- The installer is not code-signed yet. You can verify integrity by comparing the SHA256 checksum from the release page

**Node.js not found:**
- Download Node.js 18+ from https://nodejs.org
- After installing Node.js, re-run the CRE Skills installer
