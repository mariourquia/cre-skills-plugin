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
| `backend_url` | HTTPS endpoint for remote submission. Empty = disabled. | `""` (empty) |

Existing installs get this block backfilled on next session start with `local_only` defaults. Remote submission activates only when the user explicitly sets `mode` to a non-`local_only` value AND provides a non-empty HTTPS `backend_url`.

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

Remote submission is **disabled by default** (`local_only` mode). Users who want to share feedback with the maintainer must explicitly configure it.

**To enable remote submission:**
1. Set `feedback.mode` to `ask_each_time`, `anonymous_remote`, or `remote_with_contact`
2. Set `feedback.backend_url` to `https://cre-skills-feedback-api.vercel.app/api/feedback`

**Modes:**
- `local_only` (default) -- all feedback stays on your machine
- `ask_each_time` -- prompt user before each remote send
- `anonymous_remote` -- send without contact_email/organization
- `remote_with_contact` -- send all fields

**Backend:** Vercel Function + Supabase. Secrets are server-side only. The plugin only knows the public URL. See the [cre-skills-feedback-api](https://github.com/mariourquia/cre-skills-feedback-api) repo.
