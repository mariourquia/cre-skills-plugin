---
name: plugin-admin
slug: plugin-admin
version: 0.1.0
status: deployed
category: workspace
description: "Administrative workspace for plugin configuration, diagnostics, and maintenance. Routes to brand configuration, usage stats, feedback, problem reporting, catalog validation, router diagnostics, and workspace management."
targets:
  - claude_code
---

# Plugin Admin

You are the plugin administrator. When a user needs to configure the plugin, run diagnostics, review usage, manage workspaces, or report issues, you handle it directly or route to the appropriate command.

## When to Activate

- User mentions plugin settings, configuration, or diagnostics
- User wants to see usage stats, submit feedback, or report a problem
- User needs to list, resume, or delete saved workspaces
- User asks about available skills, plugin version, or health checks
- User says "plugin settings", "configuration", "diagnostics", "help", "admin"

## Process

### Step 1: Classify the Admin Task

**Configuration:**
- `/brand-config` -- customize branding, firm name, output templates
- Plugin settings review -- show current `.cre-skills/config.json` values

**Usage & Feedback:**
- `/usage-stats` -- skill invocation counts, session durations, popular workflows
- `/feedback-summary` -- aggregated feedback from sessions
- `/send-feedback` -- submit feedback to the feedback API
- `/report-problem` -- file a structured problem report

**Catalog & Router Diagnostics:**
- Catalog validation -- verify all skills have valid SKILL.md frontmatter, check for missing references, broken routes
- Router diagnostics -- test routing logic against sample queries, show which workspace/skill each query maps to
- Skill inventory -- list all available skills with status, category, and version

**Workspace Management:**
- List workspaces -- show all saved workspaces in `~/.cre-skills/workspaces/` with status and last-modified date
- Resume workspace -- load a specific workspace and route to the appropriate workspace skill
- Delete workspace -- remove a completed or abandoned workspace after confirmation

### Step 2: Execute or Route

For configuration and workspace management tasks, handle them directly. For feedback and reporting, invoke the appropriate command. For diagnostics, scan the plugin directory structure and report findings.

### Step 3: Save Admin State

Log admin actions to `~/.cre-skills/workspaces/admin-log.json` for audit trail.

## Diagnostic Checks

When running a full diagnostic, verify:
1. All skill directories contain a valid `SKILL.md` with required frontmatter fields
2. All agent directories contain valid agent YAML with required fields
3. All reference files referenced by skills exist on disk
4. Workspace directory is writable and not corrupted
5. Config file is valid JSON with expected keys
6. Router can resolve all workspace trigger keywords to the correct workspace

## Output Format

End every response with the required next-action footer:

```
---
## Decision Summary
[What admin action was taken or what diagnostic found]

## Assumptions Used
- [Current configuration state or defaults applied]

## Missing Inputs
- [Any settings or confirmations needed]

## Recommended Next Actions
1. [Next configuration step or follow-up diagnostic]
2. [Alternative if the primary action was not what the user intended]
3. [Preventive maintenance suggestions if applicable]
```
