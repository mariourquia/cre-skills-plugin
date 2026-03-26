# Telemetry and Survey Infrastructure: Implementation Plan

**Status**: planned
**Branch**: feature/orchestrator-gap-skills
**Scope**: local-only telemetry, optional survey, two new slash commands

---

## Overview

This plan describes how to add opt-in local telemetry and session feedback to the CRE Skills Plugin. All data stays on-device in `~/.cre-skills/`. No network calls in v1. The system is consent-first: telemetry and survey both default to `false`.

---

## 1. Config File Schema

**Path**: `~/.cre-skills/config.json`

```json
{
  "telemetry": false,
  "survey": false,
  "anonymousId": "<uuid-v4>",
  "firstRunComplete": false,
  "version": "2.0.0"
}
```

### Field Definitions

| Field | Type | Default | Purpose |
|---|---|---|---|
| `telemetry` | boolean | `false` | Enable local JSONL skill-invocation logging |
| `survey` | boolean | `false` | Enable end-of-session rating prompt |
| `anonymousId` | string (uuid-v4) | generated once | Correlates records across sessions without PII |
| `firstRunComplete` | boolean | `false` | Guards the first-run consent prompt (fires exactly once) |
| `version` | string | `"2.0.0"` | Config schema version; used for future migrations |

### Initialization Logic

1. On first CRE skill invocation in a session, the SessionStart hook checks whether `~/.cre-skills/config.json` exists.
2. If it does not exist, create `~/.cre-skills/` and write the config with all defaults (`telemetry: false`, `survey: false`, `firstRunComplete: false`, a fresh uuid-v4 as `anonymousId`).
3. If `firstRunComplete` is `false`, display the first-run prompt (see below) and then set `firstRunComplete: true`.
4. If the file exists and `firstRunComplete` is `true`, skip the prompt entirely.

### First-Run Prompt

The SessionStart hook presents this once per installation:

```
CRE Skills Plugin -- First-Time Setup

This plugin can log which skills you invoke to ~/.cre-skills/telemetry.jsonl.
No deal data, file paths, or financial figures are ever recorded.

Enable local telemetry? (y/N): [user input]
Enable end-of-session feedback prompts? (y/N): [user input]

Settings saved to ~/.cre-skills/config.json. You can change them anytime by editing that file.
```

Defaults are `N` (no). The user must affirmatively type `y` to enable either feature.

---

## 2. Telemetry Hook Implementation

### Hook Type

`PostToolUse` -- fires after any tool invocation within a session.

### Trigger Condition

The hook inspects the tool call to determine whether a CRE skill SKILL.md was loaded. Specifically, it fires when the tool result indicates a file read from the `skills/<slug>/SKILL.md` path pattern within the plugin root.

### Skill-Invocation Event Schema

Each invocation appends one JSONL record to `~/.cre-skills/telemetry.jsonl`:

```json
{
  "event": "skill_invoked",
  "skill": "acquisition-underwriting-engine",
  "investor_type": "private-equity",
  "workflow_chain": "acquisition-pipeline",
  "date": "2026-03-26",
  "anonymous_id": "a1b2c3d4"
}
```

| Field | Source | Notes |
|---|---|---|
| `event` | constant | Always `"skill_invoked"` |
| `skill` | parsed from file path | The slug extracted from `skills/<slug>/SKILL.md` |
| `investor_type` | parsed from SKILL.md frontmatter | Pull from `investor_type` tag if present; otherwise `"unknown"` |
| `workflow_chain` | parsed from SKILL.md frontmatter | Pull from `workflow_chain` tag if present; otherwise `"standalone"` |
| `date` | system clock | ISO 8601 date only (no timestamp, no timezone) |
| `anonymous_id` | `config.json` | The persistent uuid-v4; never changes after first run |

### Session-Summary Event Schema

At session end (Stop hook), if telemetry is enabled and at least one CRE skill was used, append one summary record:

```json
{
  "event": "session_end",
  "skills_used": ["acquisition-underwriting-engine", "sensitivity-stress-test"],
  "duration_minutes": 45,
  "verdict": "GO",
  "date": "2026-03-26",
  "anonymous_id": "a1b2c3d4"
}
```

| Field | Source | Notes |
|---|---|---|
| `event` | constant | Always `"session_end"` |
| `skills_used` | accumulated in-session list | De-duplicated list of slugs used |
| `duration_minutes` | session clock | Rounded to nearest minute |
| `verdict` | parsed from session output | Detect GO/NO-GO/CONDITIONAL string in assistant output; `null` if not found |
| `date` | system clock | ISO 8601 date only |
| `anonymous_id` | `config.json` | Same uuid-v4 as above |

### Storage

Append-only writes to `~/.cre-skills/telemetry.jsonl`. One JSON object per line. Never rewrite existing lines. If the file does not exist, create it on first write.

### Privacy Constraints (hard requirements)

- NO file paths (absolute or relative)
- NO deal names, property addresses, or entity names
- NO financial figures (IRR, NOI, price, cap rate, loan amount)
- NO user names, email addresses, or any PII
- NO environment variables or system metadata
- The `anonymous_id` is a random uuid-v4 generated locally; it is NOT tied to any account

---

## 3. Survey Hook Implementation

### Hook Type

`Stop` -- fires when the session ends.

### Condition

The survey prompt fires only when ALL of the following are true:

1. `survey: true` in `~/.cre-skills/config.json`
2. At least one CRE skill was invoked during the session (tracked in-session state)
3. The current session is not already a feedback-entry session (guard against recursion)

### Prompt

Non-blocking. User can press Enter to skip any field.

```
How useful was this CRE session? (1-5, or Enter to skip)
> [user input]
Any comments? (Enter to skip)
> [user input]
```

Rating validation: accept integers 1-5 only. Any other input (including non-numeric) is treated as a skip (`null`).

### Storage

Append one JSONL record to `~/.cre-skills/feedback.jsonl`:

```json
{
  "date": "2026-03-26",
  "rating": 4,
  "comment": "Great underwriting output",
  "skills_used": ["acquisition-underwriting-engine", "sensitivity-stress-test"],
  "anonymous_id": "a1b2c3d4"
}
```

| Field | Type | Notes |
|---|---|---|
| `date` | string | ISO 8601 date only |
| `rating` | integer or null | 1-5; null if skipped |
| `comment` | string or null | Raw user text; null if skipped |
| `skills_used` | array of strings | Slugs used in the session |
| `anonymous_id` | string | Same uuid-v4 from config |

If both `rating` and `comment` are null (user skipped both), do not write a record.

---

## 4. Usage Stats Command

**Command**: `/cre-skills:usage-stats`

**Source file**: `commands/usage-stats.md`

**Input**: `~/.cre-skills/telemetry.jsonl`

**Behavior**:

1. Read and parse `~/.cre-skills/telemetry.jsonl`. If the file does not exist or is empty, output: `No telemetry data found. Enable telemetry in ~/.cre-skills/config.json.`
2. Filter to records where `event == "skill_invoked"`.
3. Produce the following sections:

**Top 10 Most-Used Skills**
Rank skills by invocation count (descending). Show slug and count.

**Workflow Chain Distribution**
Group `skill_invoked` records by `workflow_chain`. Show count and percentage of total invocations per chain.

**Investor Type Distribution**
Group by `investor_type`. Show count and percentage.

**Average Session Duration**
From `session_end` records, compute mean `duration_minutes`. Show count of sessions included.

**Usage Trend**
If data spans >= 14 days: show weekly invocation counts.
If data spans >= 60 days: show monthly invocation counts.
If data spans < 14 days: show daily counts.

**Total Sessions**
Count of `session_end` records.

**Output format**: Markdown tables and bullet lists. No charts (plain text only).

---

## 5. Feedback Summary Command

**Command**: `/cre-skills:feedback-summary`

**Source file**: `commands/feedback-summary.md`

**Input**: `~/.cre-skills/feedback.jsonl`

**Behavior**:

1. Read and parse `~/.cre-skills/feedback.jsonl`. If the file does not exist or is empty, output: `No feedback data found. Enable survey in ~/.cre-skills/config.json.`
2. Filter to records where `rating` is not null.
3. Produce the following sections:

**Overall Average Rating**
Mean of all non-null ratings. Show N (record count).

**Rating by Skill**
For each skill that appears in `skills_used`, compute mean rating across sessions that included that skill. Show top 10 by invocation count.

**Rating Distribution (histogram)**
Count of each rating value (1, 2, 3, 4, 5). Show as a simple bar using ASCII pipes or dashes.

**Recent Comments**
Last 10 records where `comment` is not null. Show date and comment text (no rating, no id).

**Trend**
If >= 4 weeks of data: compare average rating in the most recent 2 weeks vs. the prior 2 weeks. Label as "improving", "declining", or "stable" (within 0.2 points).

**Output format**: Markdown tables and bullet lists.

---

## 6. Privacy Controls

Users retain full control over all data. No data is transmitted in v1.

| Action | How |
|---|---|
| Disable telemetry | Set `"telemetry": false` in `~/.cre-skills/config.json` |
| Disable survey | Set `"survey": false` in `~/.cre-skills/config.json` |
| Delete telemetry data | `rm ~/.cre-skills/telemetry.jsonl` |
| Delete feedback data | `rm ~/.cre-skills/feedback.jsonl` |
| Delete everything | `rm -rf ~/.cre-skills/` |
| Export data | Files are standard JSONL (newline-delimited JSON); portable to any tool |
| Inspect data | `cat ~/.cre-skills/telemetry.jsonl` or any JSON viewer |

The config file itself (`config.json`) contains no sensitive data. The `anonymousId` is a locally generated random uuid-v4 with no external registration.

---

## 7. Testing Strategy

### Unit Tests

- **No-PII assertion**: Parse a sample JSONL file and assert that no field contains a file path pattern (`/Users/`, `/home/`, `~/`), no field contains numeric strings that could be financial figures (> 6 digits), and no field contains email-address patterns.
- **Disabled telemetry**: When `telemetry: false`, assert that no records are written to `telemetry.jsonl` after a simulated skill invocation.
- **Disabled survey**: When `survey: false`, assert that the feedback prompt does not fire and no records are written to `feedback.jsonl`.
- **Config creation**: Delete `~/.cre-skills/config.json`, simulate a first invocation, and assert the file is created with correct defaults (`telemetry: false`, `survey: false`, `firstRunComplete: false`).
- **First-run guard**: After first-run completes (`firstRunComplete: true`), assert the prompt does not fire again on subsequent sessions.

### Integration Tests

- **Graceful handling of missing files**: Run `/cre-skills:usage-stats` and `/cre-skills:feedback-summary` with no JSONL files present. Assert each command outputs the "no data found" message without errors.
- **Graceful handling of corrupted JSONL**: Insert a malformed line into `telemetry.jsonl`. Assert the commands skip the bad line and process the rest without crashing.
- **Partial records**: Records missing optional fields (`investor_type`, `workflow_chain`, `verdict`) should be processed as `"unknown"` or `null` without errors.
- **Empty session**: A session where no CRE skill is invoked should produce no `session_end` record and no survey prompt, regardless of config settings.

### Manual Verification

- Confirm `telemetry.jsonl` contains no deal names, addresses, or financial figures after a real session.
- Confirm the first-run prompt fires exactly once across two sequential sessions.
- Confirm that disabling and re-enabling telemetry mid-session produces no partial records.

---

## 8. Future Remote Telemetry (v2 Placeholder)

This section documents the intended v2 design. Nothing here is implemented in v1.

### Additional Config Field

```json
{
  "remote_telemetry": false
}
```

`remote_telemetry` is a separate opt-in from `telemetry`. Enabling `telemetry` (local) does NOT imply enabling `remote_telemetry`. The user must opt in to each independently.

### Transmission Design

- **Batch upload**: Records accumulate locally and are sent in a single POST request once per day (or on-demand via a command). Not real-time.
- **Endpoint**: A documented HTTPS endpoint. The URL and request schema will be published in `PRIVACY.md` before the feature is activated in any release.
- **Payload**: Identical schema to local JSONL records. No additional fields added during upload.
- **Failure handling**: If the upload fails (network unavailable, non-200 response), records remain local. No retry storm. Next daily attempt processes the backlog.
- **Deletion**: A `DELETE /opt-out?id=<anonymousId>` endpoint will be provided to purge server-side records. This will be documented before v2 ships.

### Governance Requirements Before v2 Ships

1. `PRIVACY.md` published in the repo describing exact data collected, retention period, and deletion process.
2. Endpoint URL and request/response schema documented publicly.
3. Server-side retention policy defined (suggest: 90 days rolling).
4. Opt-out endpoint implemented and tested before any remote collection begins.
5. Release notes for the v2 version explicitly list the new capability and link to `PRIVACY.md`.
