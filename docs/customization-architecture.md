# Skill Customization Architecture

Technical reference for maintainers working on the customization system.

## Module Structure

```
lib/
├── customization.mjs    -- CRUD, override resolution, index management
├── diff.mjs             -- LCS-based line diff, hunk construction, section detection
└── feedback-payload.mjs -- Payload construction, privacy filtering, local/remote save
```

All modules are zero-dependency (Node stdlib only). They are imported by `mcp-server.mjs` and the test suite.

## Override Resolution

The `resolveSkillPath(slug, skillsDir)` function is the single point of override resolution:

```
1. Check ~/.cre-skills/customizations/<slug>/SKILL.md
2. If exists → return { path: <customization>, source: "customized" }
3. If not   → return { path: <skillsDir>/<slug>/SKILL.md, source: "base" }
```

This function is called by:
- `mcp-server.mjs` → `toolSkillDetail()`
- Any future consumer that needs to load a skill

The skill dispatcher (`routing/skill-dispatcher.mjs`) is not modified because it returns slugs, not file contents. Override resolution happens at the content-loading layer.

## Storage Layout

```
~/.cre-skills/customizations/
├── index.json                    # Fast lookup: { customizations: { [slug]: {...} } }
└── <slug>/
    ├── SKILL.md                  # Editable override (full copy, not a patch)
    ├── base-snapshot.md          # Frozen copy of base skill at creation time
    └── metadata.json             # Structured customization record
```

The `base-snapshot.md` enables diffing even after plugin updates change the base skill. It represents what the user customized *from*, not the current base.

## Diff Engine

Uses LCS (Longest Common Subsequence) at the line level. O(n*m) time and space, which is fine for skill files (typically 100-300 lines).

Output:
- **hunks**: Context-grouped change regions (3 lines of context, like unified diff)
- **stats**: { added, removed, unchanged }
- **sections_changed**: Markdown headings (## or ###) that contain changes

The `formatDiffText()` function produces unified-diff-style output for human review.

## Feedback Payload Pipeline

```
User customizes skill
  ↓
buildPayload() -- full payload with all fields
  ↓
filterByMode(payload, mode) -- strips fields per privacy level
  ↓
previewPayload() -- human-readable summary shown to user
  ↓
User consents (if require_consent)
  ↓
savePayloadLocally() -- append to feedback-log.jsonl (always)
  ↓
enqueueForRetry() -- append to outbox.jsonl (if endpoint configured)
  ↓
outbox drain on next session start (existing mechanism)
```

## Privacy Mode Cascade

Each mode includes all data from the modes below it:

| Mode | Skill slug, categories, rationale, hashes | Diff stats, sections | Full diff text | Full content |
|------|:---:|:---:|:---:|:---:|
| `off` | | | | |
| `metadata_only` | x | | | |
| `metadata_and_summary` | x | x | | |
| `metadata_and_diff` | x | x | x | |
| `metadata_and_content` | x | x | x | x* |

\* Only if `consented_to_content === true`. Even in `metadata_and_content` mode, content is stripped without explicit consent.

## Config Integration

Config lives in `~/.cre-skills/config.json` under the `customization` key:

```json
{
  "feedback": { ... },
  "customization": {
    "feedback_enabled": true,
    "feedback_mode": "metadata_only",
    "feedback_endpoint": "",
    "require_consent": true,
    "dry_run": false
  }
}
```

The `plugin.json` `userConfig` exposes `customization_feedback_mode` and `customization_feedback_endpoint` for Claude Code's native settings UI.

## MCP Tool Design

Thirteen customization tools added to `mcp-server.mjs` (21 total):

| Tool | Sync/Async | Side effects |
|------|-----------|-------------|
| `cre_customize_skill` | sync | Creates dirs + files |
| `cre_save_customization` | sync | Writes SKILL.md + metadata |
| `cre_list_customizations` | sync | Reads index.json |
| `cre_customization_detail` | sync | Reads files + computes diff |
| `cre_revert_customization` | sync | Deletes directory |
| `cre_submit_customization_feedback` | sync | Appends to JSONL; enforces `require_consent` |
| `cre_export_customization` | sync | Reads files, returns bundle |
| `cre_import_customization` | sync | Creates dirs + files from bundle |
| `cre_customization_health_check` | sync | Reads + compares base vs snapshot |
| `cre_list_templates` | sync | Reads template directory |
| `cre_apply_template` | sync | Creates dirs + files from template |
| `cre_upstream_suggestion` | sync | Reads files, returns issue body |
| `cre_customization_analytics` | sync | Reads feedback-log.jsonl |

All tools are synchronous. Remote sending is deferred to the outbox retry mechanism (existing `hooks/feedback-outbox.mjs`).

## Test Architecture

Tests use the same source patching approach as `test-outbox.mjs`:
- Create a temp directory
- Override paths via `_setTestPaths()` / `_resetPaths()` exports
- Run assertions against the temp state
- Clean up on exit

Test coverage (152 assertions):
- Diff: hash, compute, summarize, sections, format, CRLF normalization
- CRUD: create, has, resolve, save, get, list, revert
- Security: path traversal prevention (7 malicious slug patterns + import)
- Export/Import: roundtrip, invalid bundle rejection
- Health check: current, drifted, base missing, check-all
- Templates: list, create from template
- Payload: build, filter by all 5 modes, preview, consent enforcement
- Upstream suggestion: title, body, labels
- Analytics: empty state
- Config: disabled behavior
- Paths: cross-platform resolution

## Extending

### Adding a new privacy mode

1. Add to `FEEDBACK_MODES` in `lib/feedback-payload.mjs`
2. Add filtering logic in `filterByMode()`
3. Add to the enums in `schemas/customization.schema.json` (`$defs/config` and `$defs/feedback`)
5. Add a bullet in the Step 7 mode description list in `commands/customize-skill.md`
6. Update `docs/customization-guide.md` table

### Adding a new change category

1. Add to `CHANGE_CATEGORIES` in `lib/customization.mjs`
2. Add to enums in both schema files
3. Add description to `commands/customize-skill.md` step 4
4. Update the `description` string in `cre_save_customization` tool's `inputSchema` in `mcp-server.mjs`
5. Update `docs/customization-guide.md` table

### Adding a new MCP tool

1. Write a `toolFoo(args)` handler function in `mcp-server.mjs`
2. Add a tool definition object to the `TOOLS` array with `name`, `description`, `inputSchema`
3. Register in `TOOL_HANDLERS` map: `cre_foo: toolFoo`
4. Update the header comment at the top of `mcp-server.mjs`

### Adding a new template

Drop a JSON file in `templates/customizations/` with these fields:
- `name`: Display name
- `description`: What the template does
- `target_skill`: Slug of the skill to customize
- `categories`: Array of change category tags
- `rationale`: Why this template exists
- `content` (full replacement) OR `replacements` (array of `{ find, replace }` pairs)

No code changes required.
