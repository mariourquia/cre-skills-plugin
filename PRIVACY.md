# Privacy Policy

**CRE Skills Plugin v5.2.0**
**Last updated:** 2026-06-09

## Data Collection Scope

The CRE Skills Plugin does NOT collect, transmit, or store any deal data, financial figures, property details, or personally identifiable information. All skill execution happens locally in the user's Claude Code session. No data leaves the user's machine unless they explicitly choose to send feedback remotely (mode: ask_each_time, anonymous_remote, or remote_with_contact in config).

## Editions and How Your Feedback Is Used

**Editions.** This policy covers the free, open-source core (this repository). A
separate, paid edition (`cre-skills-pro`) is in development as the
institution-grade governance layer; it has its own data and governance posture,
documented with that product.

**How feedback is used (including for the paid edition).** The feedback you choose
to send remotely is used to improve CRE Skills, and that explicitly includes
informing and refining the paid `cre-skills-pro` edition that will be offered for
purchase later. "Feedback you send remotely" means the redacted feedback record
plus the 30-day skill-usage summary bundled with it (skill slugs and counts
only), as described under [Remote Feedback Submission](#remote-feedback-submission-ask-each-time).
What is used: anonymous, non-deal product signals only (which skills are used,
ratings, and the free-text feedback you author and explicitly approve for
sending). What is NOT used: your deal data, financial figures, property details,
prompts, AI responses, and PII are never collected or transmitted, so none of
them are used for product development of any edition. Remote sending stays opt-in
and per-submission (`ask_each_time` by default). Local telemetry is never
transmitted on its own; it only leaves your machine if it is bundled into a
remote feedback submission you approve. To keep everything on your machine and
out of product development entirely, set `feedback.mode` to `local_only`.

## Document-to-Database Ingestion (Local, Stateless / Zero-Data-Retention)

The `document-to-database` family (rent roll, T-12 / operating statement, and rent-roll <-> T-12 tie-out) reads CRE document content (a rent roll or T-12 you choose to process) so it can produce structured records. That processing is **local, in-memory, and stateless**:

- The ingestion calculators are pure, standard-library Python that read a JSON payload and write a JSON result to stdout. They make **no network calls**, hold **no state between runs**, and write **nothing** to `~/.cre-skills/` or any telemetry/feedback file.
- **No deal content is ever written to telemetry or feedback.** Telemetry records only the skill slug and date (as above); it never records the document content, the extracted values, or the output.
- **Tenant identity is pseudonymized on ingest.** Natural-person names, per-unit actual rent tied to a named person, guarantor/signatory names, SSNs, and bank account/routing numbers are NEVER emitted; a verbatim `source_text_span` is retained only for non-PII fields (a cell-address locator is kept for PII fields, never the value). A redaction breach is a non-overridable failure that halts the run.
- This is the **zero-data-retention (ZDR) / stateless** path. A consumer that chooses to PERSIST ingestion output (e.g. into their own database) is operating their own stateful extension under their own application security and data-processing agreement; that persistence is not performed by the plugin.

Synthetic, clearly-fictional fixtures are the only document content committed to this repository.

## Telemetry (Enabled by Default, Opt-Out)

Telemetry is **enabled by default** and records only anonymous, non-invasive usage data. All telemetry data stays on your machine. Nothing is transmitted externally.

To opt out: set `"telemetry": false` in `~/.cre-skills/config.json`.

On first run, the plugin displays a clear notice explaining exactly what is and is not tracked.

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

## Remote Feedback Submission (Ask Each Time)

When you submit feedback or a bug report, you are **prompted before sending** ("Would you also like to send this to the plugin maintainer?"). Nothing leaves your machine without your explicit approval.

Default mode is `ask_each_time`: the plugin prompts for consent before each remote send and sends nothing without explicit per-submission approval. To suppress all remote sends, set `feedback.mode` to `local_only` in `~/.cre-skills/config.json`. You may also set `anonymous_remote` or `remote_with_contact` to auto-send without per-submission prompts.

When you approve a remote send:
- The redacted feedback/bug record is transmitted (same fields stored locally)
- A 30-day skill usage summary is included (skill slugs + counts only)
- HTTPS POST to `https://cre-skills-feedback-api.vercel.app/api/feedback` (Vercel Function + Supabase)
- Deal data, financial figures, prompts, and PII are never transmitted

These submissions are used to improve CRE Skills, including to inform and refine the paid `cre-skills-pro` edition that will be offered for purchase later. See [Editions and How Your Feedback Is Used](#editions-and-how-your-feedback-is-used).

Data deletion: open an issue at https://github.com/mariourquia/cre-skills-plugin/issues with your `install_id_hash` (found in your local feedback-log.jsonl records).

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
