# Privacy Policy

**CRE Skills Plugin v2.5.0**
**Last updated:** 2026-04-01

## Data Collection Scope

The CRE Skills Plugin does NOT collect, transmit, or store any deal data, financial figures, property details, or personally identifiable information. All skill execution happens locally in the user's Claude Code session. No data leaves the user's machine unless they explicitly opt into remote telemetry (future, not available in v2).

## Telemetry (Opt-In Only)

Telemetry is **disabled by default**. The user must explicitly enable it by setting `telemetry: true` in `~/.cre-skills/config.json`.

When enabled, telemetry records ONLY:

**Per skill invocation (PostToolUse hook):**

| Field | Example | Purpose |
|-------|---------|---------|
| event | `skill_invoked` | Event type identifier |
| skill | `acquisition-underwriting-engine` | Which skill was used (slug only) |
| date | `2026-03-26` | Date only (no time, no timezone) |
| anonymous_id | `a1b2c3d4-...` | Random UUID generated at first run (no PII linkage) |

**Per session summary (Stop hook):**

| Field | Example | Purpose |
|-------|---------|---------|
| event | `session_end` | Event type identifier |
| skills_used | `["skill-a", "skill-b"]` | Deduplicated list of skills used in session |
| date | `2026-03-26` | Date only |
| anonymous_id | `a1b2c3d4-...` | Same UUID as above |

**Future fields (not yet collected, planned for a later version):**
investor_type, workflow_chain, duration_minutes, verdict. These will be documented here before activation.

**What is NEVER tracked:**
- File paths, hostnames, IP addresses
- Deal data (property address, purchase price, NOI, rent rolls)
- Financial figures of any kind
- User identity, name, email, organization
- Prompt content or AI responses
- Error messages or stack traces

**Storage:** Append-only local file at `~/.cre-skills/telemetry.jsonl`. The user owns and controls this file.

## Survey Feedback (Opt-In Only)

Survey prompts are **disabled by default**. The user must explicitly enable by setting `survey: true` in `~/.cre-skills/config.json`.

When enabled, the plugin asks a brief question at the end of CRE skill sessions:
- Rating: 1-5 (skippable)
- Comment: free-text (skippable, user-authored only)

**Storage:** `~/.cre-skills/feedback.jsonl`. Comments are user-authored and user-controlled. The plugin never generates or infers feedback content.

## Structured Feedback (On-Demand, Local-Only)

Users can submit feedback at any time via `/cre-skills:send-feedback` or `/cre-skills:report-problem`. These commands guide the user through providing structured feedback.

**What is stored (all fields user-provided or derived from config):**

| Field | Source | Example |
|-------|--------|---------|
| submission_id | Generated | `fb_a1b2c3d4e5f67890` |
| submission_type | User selection | `general`, `bug` |
| timestamp | System clock | `2026-04-01T12:00:00Z` |
| plugin_version | `plugin.json` | `2.5.0` |
| install_id_hash | SHA-256 of anonymousId | `e3b0c442...` |
| message | User-authored | Free text (redacted) |
| rating | User-provided | 1-5 or null |
| severity | User-selected | `low`, `medium`, `high`, `critical` |
| skill_slug | User-identified | `rent-roll-analyzer` |
| contact_email | User-provided (optional) | Only if user explicitly enters it |
| context | Session metadata | Skill slugs used (no deal data) |

**Automatic redaction** (applied before storage):
- Absolute file paths are replaced with `[PATH_REDACTED]`
- Email addresses in free text are replaced with `[EMAIL_REDACTED]`
- Sequences of 5+ digits are replaced with `[NUM_REDACTED]`
- Environment variable assignments are replaced with `[ENV_REDACTED]`

The `contact_email` field is NOT redacted because the user explicitly provides it for follow-up purposes.

**What is NEVER stored in feedback submissions:**
- Prompt content or AI model responses
- Deal data (property address, purchase price, NOI, rent rolls)
- Financial figures of any kind
- Tenant, borrower, or sponsor names
- Full error stack traces (reduced to category only)

**Storage:** `~/.cre-skills/feedback-log.jsonl`. Local-only. The user owns and controls this file.

## Remote Submission (Future -- Not Available Yet)

Remote feedback/telemetry submission will:
- Require a SEPARATE opt-in (`feedback.mode` set to `ask_each_time`, `anonymous_remote`, or `remote_with_contact`)
- Default mode is `local_only` -- nothing leaves your machine unless you change this
- Transmit only the same redacted/anonymized fields stored locally
- Use HTTPS POST to a documented endpoint
- Never transmit deal data, financial figures, or PII
- Have its endpoint URL, data schema, retention policy, and deletion process published in this privacy policy before activation
- Support a data deletion request process (details TBD before activation)

## Third-Party Services

The plugin does not integrate with any third-party analytics, tracking, or advertising services. No cookies, no browser fingerprinting, no device identification.

## User Rights

| Right | How |
|-------|-----|
| **View** | `~/.cre-skills/telemetry.jsonl`, `feedback.jsonl`, and `feedback-log.jsonl` are plain-text, human-readable JSONL |
| **Delete** | Remove any file at any time: `rm ~/.cre-skills/feedback-log.jsonl` |
| **Disable telemetry** | Set `telemetry: false` and/or `survey: false` in `~/.cre-skills/config.json` |
| **Disable context** | Set `feedback.include_context: false` in config to prevent session metadata from being attached |
| **Export** | Files are standard JSONL, portable to any system |
| **Purge all** | `rm -rf ~/.cre-skills/` removes all plugin data |

## Contact

For privacy questions or concerns: open an issue at https://github.com/mariourquia/cre-skills-plugin/issues or email the maintainer directly.
