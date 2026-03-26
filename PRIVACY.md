# Privacy Policy

**CRE Skills Plugin v2.0.0**
**Last updated:** 2026-03-26

## Data Collection Scope

The CRE Skills Plugin does NOT collect, transmit, or store any deal data, financial figures, property details, or personally identifiable information. All skill execution happens locally in the user's Claude Code session. No data leaves the user's machine unless they explicitly opt into remote telemetry (future, not available in v2).

## Telemetry (Opt-In Only)

Telemetry is **disabled by default**. The user must explicitly enable it by setting `telemetry: true` in `~/.cre-skills/config.json`.

When enabled, telemetry records ONLY:

| Field | Example | Purpose |
|-------|---------|---------|
| skill_slug | `acquisition-underwriting-engine` | Which skills are used most |
| investor_type | `private-equity` | Which investor profiles are active |
| workflow_chain | `acquisition-pipeline` | Which workflow chains are executed |
| duration_minutes | `45` | Session length (rounded to nearest minute) |
| verdict | `GO` | Outcome category only (no underlying data) |
| date | `2026-03-26` | Date only (no time, no timezone) |
| anonymous_id | `a1b2c3d4-...` | Random UUID generated at first run (no PII linkage) |

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

## Remote Telemetry (Future -- Not Available in v2)

Remote telemetry will:
- Require a SEPARATE opt-in beyond local telemetry (`remote_telemetry: true`)
- Transmit only the same anonymized fields stored locally
- Use HTTPS POST to a documented endpoint
- Never transmit deal data, financial figures, or PII
- Have its endpoint URL and data schema published in this privacy policy before activation

## Third-Party Services

The plugin does not integrate with any third-party analytics, tracking, or advertising services. No cookies, no browser fingerprinting, no device identification.

## User Rights

| Right | How |
|-------|-----|
| **View** | `~/.cre-skills/telemetry.jsonl` and `feedback.jsonl` are plain-text, human-readable JSONL |
| **Delete** | Remove either file at any time: `rm ~/.cre-skills/telemetry.jsonl` |
| **Disable** | Set `telemetry: false` and/or `survey: false` in `~/.cre-skills/config.json` |
| **Export** | Files are standard JSONL, portable to any system |
| **Purge all** | `rm -rf ~/.cre-skills/` removes all plugin data |

## Contact

For privacy questions or concerns: open an issue at https://github.com/mariourquia/cre-skills-plugin/issues or email the maintainer directly.
