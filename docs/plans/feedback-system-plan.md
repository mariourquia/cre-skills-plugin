# Feedback System Implementation Plan

**Status:** In Progress (Slice 1)
**Branch:** `feature/feedback-system`
**Created:** 2026-04-01

---

## Overview

Add a direct feedback channel to the CRE Skills Plugin so users can report problems and share feedback without leaving their session or navigating to GitHub Issues.

## Design Principles

1. **Local-first.** All feedback is written to `~/.cre-skills/` before anything else. Remote submission is a future opt-in.
2. **No new dependencies.** Node.js stdlib only, consistent with existing hooks.
3. **Commands are the interface.** Slash commands instruct Claude how to gather and persist structured feedback. Hooks handle lifecycle config init.
4. **Redaction by default.** Even for local storage, sanitize context fields to build the habit before remote sending ships.
5. **Testable utilities.** Put behavioral logic in standalone modules (not hooks) so it can be tested with the existing Node.js test pattern.

---

## Slice 1 (This PR) -- Direct Feedback Channel

### New Files

| File | Purpose |
|------|---------|
| `schemas/feedback-submission.schema.json` | Data format for feedback records |
| `schemas/feedback-config.schema.json` | Config additions for feedback settings |
| `scripts/redact-feedback.mjs` | Standalone sanitization utility |
| `commands/send-feedback.md` | Guided general feedback intake |
| `commands/report-problem.md` | Structured bug reporting |
| `tests/test-redaction.mjs` | Behavioral tests for redaction |
| `docs/feedback-system.md` | Architecture documentation |
| `docs/plans/feedback-system-plan.md` | This plan |

### Modified Files

| File | Change |
|------|--------|
| `hooks/telemetry-init.mjs` | Add `feedback` config block with defaults |
| `hooks/hooks.json` | Update SessionStart prompt to list new commands |
| `tests/test_plugin_integrity.py` | Structural tests for new files |
| `README.md` | Add feedback commands section |
| `PRIVACY.md` | Update data flow description |

### Data Flow (Slice 1)

```
User invokes /cre-skills:send-feedback or /cre-skills:report-problem
  -> Claude follows command instructions
  -> Gathers structured input from user
  -> Calls scripts/redact-feedback.mjs to sanitize context (if included)
  -> Writes validated JSONL record to ~/.cre-skills/feedback-log.jsonl
  -> User can view via /cre-skills:feedback-summary (existing command)
```

### Config Model (Slice 1)

Added to `~/.cre-skills/config.json`:

```json
{
  "feedback": {
    "mode": "local_only",
    "include_context": true,
    "backend_url": ""
  }
}
```

| Key | Values | Default | Notes |
|-----|--------|---------|-------|
| `mode` | `local_only`, `ask_each_time`, `anonymous_remote`, `remote_with_contact` | `local_only` | Modes other than `local_only` require a non-empty `backend_url` |
| `include_context` | boolean | `true` | Whether to auto-attach skill slugs and sanitized session info |
| `backend_url` | string (HTTPS URL or empty) | `""` | Set by maintainer when Slice 3 backend is deployed. Empty = remote disabled. |

Commands already contain the remote submission logic gated on `mode` and `backend_url`. Flipping the config is all that's needed to enable remote sending once a backend is live.

### Redaction Rules (Slice 1)

Strip from context fields:
- Absolute file paths (`/Users/...`, `C:\...`, `~/...`)
- Email addresses in free text (not in explicit contact field)
- Sequences of 5+ digits (SSNs, account numbers, phone numbers)
- Environment variable values (`KEY=value` patterns)

Never include:
- Prompt content or AI responses
- Deal data, financial figures, tenant/borrower names
- Stack traces (reduce to error category only)

### What Slice 1 Does NOT Include

- No remote submission (no outbox, no sender, no backend)
- No proactive prompts (no session-end prompt, no error-triggered prompt)
- No `feedback-settings` command
- No `request-feature` or `contact` commands
- No changes to `session-summary.mjs` or `telemetry-capture.mjs`

---

## Slice 2 -- Proactive Prompts (Future PR)

- `hooks/feedback-prompt.mjs` -- prompt decision logic
- Update `session-summary.mjs` -- optional rating + comment at session end
- `commands/feedback-settings.md` -- manage consent, prompt frequency
- Config additions: `prompt_frequency`, `last_prompted_at`
- Update `telemetry-capture.mjs` -- recent skill buffer for auto-populating context

## Slice 3 -- Remote Submission + Feature Requests (Future PR)

- `hooks/feedback-outbox.mjs` -- retry queue for failed remote sends
- `hooks/feedback-submit.mjs` -- SessionStart hook to flush pending outbox items
- `commands/request-feature.md` -- feature request intake
- `commands/contact.md` -- direct maintainer contact
- `commands/feedback-settings.md` -- UI for changing mode, backend_url, include_context
- Config additions: `consent_version`, `last_submitted_at`
- Backend deployment (separate repo, see Backend Recommendations below)
- Update PRIVACY.md with remote data flow, retention policy, deletion process
- Set `backend_url` in config (distributed via `scripts/update.sh` or docs)

Note: `backend_url` is already in the config schema and commands already contain
the full remote submission logic (gated on `mode != local_only && backend_url != ""`).
Slice 3 mainly needs the backend, the retry hook, and the PRIVACY.md updates.

---

## Backend Recommendations (For Maintainer)

Since this is an **open-source plugin**, the backend should be:

1. **Minimal and self-hostable.** A single serverless function + lightweight database.
2. **Free-tier friendly.** No cost at low volumes typical of an OSS plugin.
3. **No vendor lock-in.** Standard PostgreSQL, not proprietary APIs.
4. **No tokens in the plugin.** Secrets live server-side only.

### Architecture: Thin Proxy

```
Plugin (public, open-source)          Vercel Function (private)
         |                                      |
         |  POST backend_url/api/feedback       |
         |  { submission JSON }                 |
         |  ------------------------------>     |
         |                                      |  SUPABASE_URL (env var)
         |                                      |  SUPABASE_ANON_KEY (env var)
         |                                      |  -----> Supabase INSERT
         |  200 { ok: true }                    |
         |  <------------------------------     |
```

The plugin only knows the public `backend_url`. All secrets (`SUPABASE_URL`,
`SUPABASE_ANON_KEY`) live exclusively in Vercel environment variables -- never
in source code, never distributed to users.

### Recommended Stack: Vercel Function + Supabase Free Tier

- **One Vercel Function** (`api/feedback/route.ts`, ~40 lines)
  - POST `/api/feedback` -- validates schema, rate limits, INSERTs to Supabase
  - GET `/api/health` -- sender diagnostics
- **Supabase free tier**: 500MB Postgres, 50K monthly rows, built-in auth
- **Supabase RLS policy**: anon role can INSERT only (no SELECT/UPDATE/DELETE)
- **Vercel Marketplace**: `vercel integration add supabase` auto-provisions env vars
- **Total cost at plugin scale**: $0/month

### Why Not GitHub Issues API?

Considered and rejected:
- Cannot assume users have GitHub accounts (CRE professionals)
- No SQL queries, aggregation, or structured data analysis
- Any token embedded in the plugin source can be extracted by anyone
- Rate limited (5000 req/hr)

### Backend Schema

```sql
CREATE TABLE feedback_submissions (
  id              TEXT PRIMARY KEY,       -- fb_<hex16>
  type            TEXT NOT NULL,          -- general | bug | feature | contact
  rating          INTEGER,               -- 1-5, nullable
  severity        TEXT,                   -- low | medium | high | critical
  message         TEXT NOT NULL,
  skill_slug      TEXT,
  workflow_slug   TEXT,
  orchestrator_slug TEXT,
  cre_domain      TEXT,
  contact_email   TEXT,                   -- only if user opted in
  organization    TEXT,
  plugin_version  TEXT NOT NULL,
  install_id_hash TEXT NOT NULL,          -- SHA-256 of anonymousId
  context         JSONB,                  -- sanitized session context
  created_at      TIMESTAMPTZ DEFAULT now()
);

-- RLS: anon can only INSERT
ALTER TABLE feedback_submissions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "anon_insert" ON feedback_submissions
  FOR INSERT TO anon WITH CHECK (true);
```

### What You Need to Procure (Slice 3)

1. **Supabase project** -- free tier, create at supabase.com, run the CREATE TABLE above
2. **Vercel project** -- for the single API function (new repo or subdirectory)
3. **`vercel integration add supabase`** -- auto-provisions SUPABASE_URL and SUPABASE_ANON_KEY
4. **Rate limiting** -- Vercel WAF (free tier includes basic rules) or in-function IP limiter
5. **Set `backend_url`** -- deployed at `https://cre-skills-feedback-api.vercel.app`. Update `scripts/update.sh` to set `feedback.backend_url` in user configs, or document the manual step
6. **Update PRIVACY.md** -- document the endpoint, data retention policy, and deletion request process before going live

None of this is needed for Slice 1. The commands already contain the full
remote submission logic gated on `mode != "local_only" && backend_url != ""`.
Deploying the backend and setting `backend_url` is all that's needed to activate it.
