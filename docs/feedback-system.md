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

## Remote Submission (Slice 3 -- commands already wired)

The commands already contain the full remote submission logic. It activates when:
1. `feedback.mode` is not `local_only`
2. `feedback.backend_url` is a non-empty HTTPS URL

When both conditions are met, after local save:

```
6. Check mode:
   - ask_each_time: prompt user for confirmation
   - anonymous_remote: send without contact_email/organization
   - remote_with_contact: send all fields
7. POST redacted JSON to backend_url with Content-Type and X-Plugin-Version headers
8. On success: confirm "sent to maintainer"
9. On failure: save to ~/.cre-skills/outbox.jsonl for retry
```

### What's still needed for Slice 3

- **Backend**: Vercel Function + Supabase (thin proxy, ~40 lines, secrets server-side only)
- **`hooks/feedback-outbox.mjs`**: SessionStart hook to flush failed sends from outbox
- **PRIVACY.md update**: Document the endpoint URL, retention policy, deletion process
- **Set `backend_url`** in user configs (via `scripts/update.sh` or docs)

See `docs/plans/feedback-system-plan.md` for the full architecture and procurement checklist.
