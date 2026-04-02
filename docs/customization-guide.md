# Skill Customization Guide

Adapt any CRE skill to how your team actually works -- without modifying plugin files.

## What This Does

The customization system creates **local overrides** of base skills. Your customized version takes priority whenever the plugin loads that skill. Base skills are never modified, so plugin updates do not overwrite your changes.

## Quick Start

Run the customize command:

```
/cre-skills:customize-skill
```

The plugin walks you through:
1. Picking a skill to customize
2. Making your changes
3. Recording why you changed it
4. Optionally sharing feedback with the maintainer

## How Overrides Work

```
Plugin loads skill "deal-quick-screen"
  ↓
Check ~/.cre-skills/customizations/deal-quick-screen/SKILL.md
  ↓ exists?
YES → use customized version
NO  → use base skill from plugin
```

Every MCP tool (`cre_skill_detail`, `cre_route`, etc.) and the Claude Code skill loader follow this resolution order automatically.

## Where Files Live

| File | Location |
|------|----------|
| Base skills (read-only) | `<plugin>/skills/<slug>/SKILL.md` |
| Your customized skills | `~/.cre-skills/customizations/<slug>/SKILL.md` |
| Frozen base snapshot | `~/.cre-skills/customizations/<slug>/base-snapshot.md` |
| Customization metadata | `~/.cre-skills/customizations/<slug>/metadata.json` |
| Customization index | `~/.cre-skills/customizations/index.json` |
| Feedback & config | `~/.cre-skills/config.json` |

On Windows, `~` maps to `C:\Users\<username>`.

## Common Customization Types

| Category | Example |
|----------|---------|
| **Terminology** | Rename "NOI" to "Net Operating Profit" in outputs |
| **Approval chain** | Add a compliance officer review step |
| **Required steps** | Add ESG screening to your underwriting process |
| **Compliance** | Insert FIRPTA disclosure in disposition workflows |
| **Deliverable format** | Restructure IC memo sections for your committee |
| **Tone / style** | Make investor updates more concise |
| **Missing fields** | Add a "deal source" input field |
| **Output structure** | Change table layouts to match your templates |
| **Calculation method** | Use MOIC instead of IRR as primary return metric |
| **Regional / market** | Add NYC transfer tax tiers |

## Managing Customizations

### List all customizations

Use the `cre_list_customizations` MCP tool, or run:

```
/cre-skills:customize-skill
```

and choose "list" when prompted.

### View a customization

The `cre_customization_detail` MCP tool shows:
- When it was created and last updated
- A diff summary (what changed)
- Change categories and rationale

### Revert to base

The `cre_revert_customization` MCP tool removes the local override. You can also delete the directory manually:

```bash
rm -rf ~/.cre-skills/customizations/<slug>
```

## Export & Import

Share customizations with teammates or back them up.

**Export:**
Use the `cre_export_customization` MCP tool with a skill name. It produces a self-contained JSON bundle containing the customized content, the original base snapshot, and all metadata.

**Import:**
Use the `cre_import_customization` MCP tool with the bundle. It creates or replaces the local customization for that skill.

Bundles are portable across macOS and Windows.

## Health Check

Check if the base plugin skills have been updated since you created your customizations.

Use the `cre_customization_health_check` MCP tool:
- With a specific skill name to check one customization
- With `all: true` to check all customizations at once

Statuses:
- **current** -- base skill unchanged, your customization is up to date
- **drifted** -- base skill was updated in a newer plugin version; review your customization to incorporate upstream improvements
- **base_missing** -- the base skill was removed from the plugin; your customization still works

## Templates

Pre-built customization starting points for common enterprise needs. Templates apply modifications automatically so you don't start from scratch.

Use `cre_list_templates` to see available templates. Use `cre_apply_template` to apply one.

Shipped templates:
- **firpta-screening** -- Adds FIRPTA compliance check to deal screening
- **nyc-transfer-tax** -- Adds NYC/NYS transfer tax calculations to deal screening
- **esg-screening** -- Adds ESG pre-screening to acquisition underwriting

To create your own template, drop a JSON file in `<plugin>/templates/customizations/` with `name`, `description`, `target_skill`, `categories`, and either `content` (full replacement) or `replacements` (find/replace pairs).

## Upstream Suggestions

If you want the plugin maintainer to consider incorporating your changes, use the `cre_upstream_suggestion` MCP tool. It generates a structured GitHub issue body with your rationale, change categories, and diff.

## Analytics

View patterns across all your customizations:

```
/cre-skills:customization-analytics
```

Shows: which skills you customize most, common change categories, health status, upstream suggestion rate, and monthly trends.

---

## Feedback & Privacy

When you customize a skill, you can optionally send structured feedback to the plugin maintainer. This helps improve the plugin for everyone.

### What gets sent (by privacy mode)

| Mode | Data included |
|------|--------------|
| `off` | Nothing (feedback disabled) |
| `metadata_only` (default) | Skill slug, change categories, rationale, content hashes |
| `metadata_and_summary` | Above + line counts, affected sections |
| `metadata_and_diff` | Above + full line-by-line diff |
| `metadata_and_content` | Above + full customized SKILL.md (requires explicit consent) |

### What is never sent

- Deal data, financial figures, or prompts
- Company names, addresses, or PII
- Your Claude conversation history
- Any data without your knowledge

### Configuration

Edit `~/.cre-skills/config.json`:

```json
{
  "customization": {
    "feedback_enabled": true,
    "feedback_mode": "metadata_only",
    "feedback_endpoint": "",
    "require_consent": true,
    "dry_run": false
  }
}
```

### Example configurations

**Fully local (no remote sends):**

```json
{
  "customization": {
    "feedback_enabled": true,
    "feedback_mode": "metadata_only",
    "feedback_endpoint": "",
    "require_consent": true
  }
}
```

**Metadata-only feedback to maintainer:**

```json
{
  "customization": {
    "feedback_enabled": true,
    "feedback_mode": "metadata_only",
    "feedback_endpoint": "https://cre-skills-feedback-api.vercel.app/api/feedback",
    "require_consent": true
  }
}
```

**Full feedback with explicit consent:**

```json
{
  "customization": {
    "feedback_enabled": true,
    "feedback_mode": "metadata_and_content",
    "feedback_endpoint": "https://cre-skills-feedback-api.vercel.app/api/feedback",
    "require_consent": true
  }
}
```

**Enterprise -- point to your own endpoint:**

```json
{
  "customization": {
    "feedback_enabled": true,
    "feedback_mode": "metadata_and_summary",
    "feedback_endpoint": "https://internal.yourcompany.com/api/cre-feedback",
    "require_consent": false
  }
}
```

**Completely disabled:**

```json
{
  "customization": {
    "feedback_enabled": false
  }
}
```

### Dry-run mode

Set `"dry_run": true` to see exactly what would be sent without actually sending anything. Useful for auditing before enabling remote feedback.

## Plugin Updates

When the plugin is updated:
- Your customizations are **preserved** (they live outside the plugin directory)
- If a base skill changed significantly, the frozen snapshot in `base-snapshot.md` still reflects the version you customized from
- You can re-run `/cre-skills:customize-skill` to view the diff between your version and the new base

## MCP Tools Reference

| Tool | Purpose |
|------|---------|
| `cre_customize_skill` | Initialize a new customization |
| `cre_save_customization` | Save changes with metadata |
| `cre_list_customizations` | List all active customizations |
| `cre_customization_detail` | View metadata, diff, content |
| `cre_revert_customization` | Remove a customization |
| `cre_submit_customization_feedback` | Send feedback (respects privacy config) |
| `cre_export_customization` | Export as portable JSON bundle |
| `cre_import_customization` | Import from a bundle |
| `cre_customization_health_check` | Check for base skill drift |
| `cre_list_templates` | List available customization templates |
| `cre_apply_template` | Apply a pre-built template |
| `cre_upstream_suggestion` | Generate a GitHub issue suggestion |
| `cre_customization_analytics` | Analyze customization patterns |
