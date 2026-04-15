# Installing CRE Skills Plugin -- Team / Cowork Environments

This guide covers deploying the CRE Skills Plugin across a team using Claude Code's managed plugin features.

---

## Adding as a Team-Managed Plugin

Team administrators can push the plugin to all team members so it loads automatically in every session.

### Step 1: Add to Team Plugin Configuration

In your team's Claude Code settings (typically managed via your organization's configuration):

```json
{
  "plugins": [
    {
      "name": "cre-skills",
      "source": "github:mariourquia/cre-skills-plugin",
      "version": "4.0.0",
      "enabled": true
    }
  ]
}
```

This ensures every team member gets the plugin without manual installation.

### Step 2: Verify Team-Wide Availability

Each team member can confirm the plugin is active:

```
/cre-skills:cre-route
```

If the routing index loads and returns skill categories, the plugin is working.

---

## Pinning a Version

To prevent unexpected changes from affecting active workflows, pin the plugin to a specific version or commit.

### Pin to a release tag

```json
{
  "source": "github:mariourquia/cre-skills-plugin",
  "version": "4.0.0"
}
```

### Pin to a specific commit

```json
{
  "source": "github:mariourquia/cre-skills-plugin",
  "ref": "abc1234"
}
```

### Update schedule recommendation

- **Quarterly**: Review new skills and agent updates. Test in a sandbox project before rolling out.
- **On new hires**: Ensure onboarding includes plugin verification.
- **On major releases**: Read the changelog, test workflow chains end-to-end, then update the pinned version.

---

## Configuring Which Skills Are Enabled

The plugin ships with all 113 skills active by default. For teams that only use a subset (e.g., an acquisitions team that does not need construction management skills), you can scope the active skills.

### Option A: Registry-Based Filtering

The `registry.yaml` file at the repo root lists every skill with its category and metadata. Fork the repo and remove or comment out skills your team does not use:

```yaml
# registry.yaml (excerpt)
skills:
  - slug: deal-quick-screen
    category: deal-pipeline
    enabled: true

  - slug: construction-project-command-center
    category: construction
    enabled: false    # Disabled for acquisitions team
```

### Option B: Routing Index Scoping

Edit `src/routing/CRE-ROUTING.md` in your fork to remove categories or skills that are not relevant. The router only finds skills listed in the routing index, so removing entries effectively hides them.

### Option C: Separate Plugin Forks per Team

For organizations with distinct groups (acquisitions, asset management, development), maintain separate forks with only the relevant skills:

```
cre-skills-plugin-acquisitions/    # 25 skills: screening, underwriting, DD, closing
cre-skills-plugin-asset-mgmt/     # 20 skills: NOI, capex, leasing, budgets
cre-skills-plugin-development/    # 15 skills: proformas, entitlements, construction
```

Each fork uses the same plugin structure but with a trimmed `src/skills/` directory and routing index.

---

## Managed Settings for Auto-Enable

### Claude Code CLI

Add to your team's shared `.claude/settings.json`:

```json
{
  "plugins": {
    "cre-skills": {
      "path": "~/.claude/plugins/cre-skills-plugin",
      "autoLoad": true
    }
  }
}
```

### Claude Desktop (Managed Deployment)

For organizations using managed Claude Desktop deployments, include the plugin path in the managed configuration profile:

```json
{
  "managedPlugins": [
    {
      "name": "cre-skills",
      "source": "github:mariourquia/cre-skills-plugin",
      "version": "4.0.0",
      "autoEnable": true,
      "allowDisable": false
    }
  ]
}
```

Setting `allowDisable: false` prevents individual users from turning off the plugin, ensuring consistent behavior across the team.

---

## Onboarding New Team Members

Share these instructions with new hires:

1. **Verify the plugin is active**: Start a new Claude Code session and run `/cre-skills:cre-route`. You should see the skill category listing.

2. **Learn the three entry points**:
   - `/cre-skills:cre-route [task description]` -- find the right skill
   - `/cre-skills:cre-workflows` -- browse workflow chains
   - `/cre-skills:cre-agents` -- list expert agents

3. **Start with a real task**: Try screening a deal, sizing a loan, or generating an IC memo. The router will guide you to the right skill.

4. **Chain skills for complex workflows**: Use `/cre-skills:cre-workflows` to see how skills connect. Example: Deal Quick Screen -> Acquisition Underwriting -> DD Command Center -> IC Memo -> Closing Checklist.

---

## Monitoring Usage

Track which skills your team uses most frequently to identify:

- **Training gaps**: If a skill is never used, the team may not know it exists. Run a lunch-and-learn.
- **Missing skills**: If the team keeps asking for something not covered, file an issue on the repo.
- **Workflow bottlenecks**: If one skill in a chain is always the slowest or most error-prone, it may need reference file improvements.

---

## Security Notes

- The plugin's skill content is Markdown, YAML, and JSON. JavaScript hooks (telemetry, feedback) and the MCP server run locally with no external network calls unless the user explicitly opts in to remote feedback submission.
- No deal data leaves the conversation. The plugin provides structured prompts and reference material. Telemetry records only skill slugs and dates locally.
- No API keys, tokens, or credentials are required.
- Python calculators (in `src/calculators/`) are zero-dependency scripts that run locally.
- Safe to deploy in regulated environments (FINRA, SEC, SOX) with appropriate review of the hook scripts and calculator code.
