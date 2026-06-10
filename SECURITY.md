# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly.

**Do NOT open a public issue.** Instead, email security concerns to 60152193+mariourquia@users.noreply.github.com with:

1. Description of the vulnerability
2. Steps to reproduce
3. Potential impact
4. Suggested fix (if you have one)

I will acknowledge receipt within 48 hours and work with you on a fix before any public disclosure.

## Scope

This project is a Claude Code plugin delivering CRE skill methodology, agent prompts, and a set of deterministic, standard-library ingestion calculators (the `document-to-database` family). By default it connects to no external APIs and runs entirely within the user's local Claude Code session. The ingestion calculators read document content the user chooses to process, but do so **locally and statelessly** (zero data retention): they make no network calls, hold no state between runs, write nothing to disk beyond the user's own chosen output, and emit no deal content to telemetry or feedback (see [PRIVACY.md](PRIVACY.md)). Natural-person PII is pseudonymized on ingest and never emitted; a redaction breach is a non-overridable failure that halts the run.

**In scope:**
- Skill methodology logic and process definitions
- Agent prompt content that could be used to elicit harmful outputs
- Routing logic that could be manipulated to misroute queries
- Document-to-database ingestion: the PII redaction/pseudonymization boundary, charge-code/account mapping, and the fail-closed grading gate
- Any local telemetry or feedback file handling (if telemetry is enabled)

**Out of scope:**
- Real deal data or PII transmitted off the user's machine (the plugin does not collect or transmit deal content by default; ingestion is local and stateless)
- Persisting ingestion output into a real database/warehouse, which is the user's stateful extension under their own application security and data-processing agreement
- Third-party integrations built on top of the plugin by users
- The Claude Code CLI itself (report those to Anthropic)

If you have extended the plugin with real API integrations, persistent storage, or live deal-data pipelines, standard application security practices apply to your extension.

## Editions (open core vs paid)

This policy covers the free, open-source core (this repository). The paid
`cre-skills-pro` edition adds a governance and state harness (lifecycle hooks, an
approval engine, deal-state memory, and an audit log) with its own security and
data posture, maintained in a separate private repository. The honest
enforcement boundary for that edition: its hooks run client-side at user
privilege, so on a self-install they are a strong guardrail plus a tamper-evident
audit, not an operator-proof control. Hard, unbypassable enforcement requires
managed deployment (admin-pushed settings the user cannot override) plus a
server-side approval/identity service and an external append-only audit store.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 5.2.x   | Yes       |
| 5.1.x   | Yes       |
| < 5.1   | No        |

## Privacy

For information on how the plugin handles local telemetry and feedback data, see [PRIVACY.md](PRIVACY.md).
