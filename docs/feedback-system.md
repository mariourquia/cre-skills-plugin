# Feedback System Architecture

## Overview

The feedback system lets users share feedback and report problems without leaving their Claude session. All data is stored locally by default. Remote submission is planned for a future release.

## Components

### Commands (User Interface)

| Command | Purpose | Output File |
|---------|---------|-------------|
| `/cre-skills:send-feedback` | General feedback, ratings, suggestions | `~/.cre-skills/feedback-log.jsonl` |
| `/cre-skills:report-problem` | Structured bug reports with severity | `~/.cre-skills/feedback-log.jsonl` |
| `/cre-skills:feedback-summary` | View aggregated feedback (existing) | stdout |

### Schemas (Data Contracts)

| Schema | Purpose |
|--------|---------|
| `schemas/feedback-submission.schema.json` | Defines the JSONL record format |
| `schemas/feedback-config.schema.json` | Defines the config.json `feedback` block |

### Redaction (Privacy)

`scripts/redact-feedback.mjs` sanitizes free-text fields before storage.

**What gets redacted:**
- Absolute file paths (`/Users/...`, `C:\...`, `~/...`)
- Email addresses in free text (not in the explicit `contact_email` field)
- Sequences of 5+ digits (account numbers, SSNs, phone numbers)
- Environment variable assignments (`KEY=value`)

**What is never stored:**
- Prompt content or AI responses
- Deal data, financial figures, rent rolls
- Tenant, borrower, or sponsor names
- Full stack traces (reduced to error category)

### Config

Added to `~/.cre-skills/config.json` by `telemetry-init.mjs`:

```json
{
  "feedback": {
    "mode": "local_only",
    "include_context": true,
    "backend_url": ""
  }
}
```

| Key | Purpose | Default |
|-----|---------|---------|
| `mode` | `local_only`, `ask_each_time`, `anonymous_remote`, `remote_with_contact` | `local_only` |
| `include_context` | Attach sanitized session metadata | `true` |
| `backend_url` | HTTPS endpoint for remote submission. Empty = disabled. | `""` |

Existing installs get this block backfilled on next session start. Remote submission activates only when both `mode != "local_only"` and `backend_url` is a non-empty HTTPS URL.

## Data Flow

```
1. User invokes /cre-skills:send-feedback or /cre-skills:report-problem
2. Claude follows command instructions to gather structured input
3. Claude reads config for anonymousId and telemetry for session context
4. Claude pipes submission through scripts/redact-feedback.mjs
5. Redacted JSONL record appended to ~/.cre-skills/feedback-log.jsonl
6. User can review via /cre-skills:feedback-summary
```

## Storage Layout

All files in `~/.cre-skills/`:

| File | Format | Purpose |
|------|--------|---------|
| `config.json` | JSON | User preferences, anonymousId, feedback settings |
| `telemetry.jsonl` | JSONL | Skill invocation events (opt-in) |
| `feedback.jsonl` | JSONL | Session survey responses (existing, opt-in) |
| `feedback-log.jsonl` | JSONL | Structured feedback submissions (this system) |

`feedback-log.jsonl` is distinct from `feedback.jsonl`. The former stores structured command-driven submissions; the latter stores the existing session-end survey responses.

## Remote Submission

Remote submission is active by default (`ask_each_time` mode). The commands POST redacted submissions to `https://cre-skills-feedback-api.vercel.app/api/feedback` after local save, with user confirmation.

**Modes:**
- `ask_each_time` (default) -- prompt user before each remote send
- `anonymous_remote` -- send without contact_email/organization
- `remote_with_contact` -- send all fields
- `local_only` -- disable remote submission entirely

**Backend:** Vercel Function + Supabase. Secrets are server-side only. The plugin only knows the public URL. See the [cre-skills-feedback-api](https://github.com/mariourquia/cre-skills-feedback-api) repo.

**Remaining work:**
- `hooks/feedback-outbox.mjs` -- SessionStart hook to retry failed remote sends
