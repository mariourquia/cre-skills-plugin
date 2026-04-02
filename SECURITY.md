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

This project is a Claude Code plugin delivering CRE skill methodology and agent prompts. It does not process real financial data or connect to external APIs by default. The plugin runs entirely within the user's local Claude Code session.

**In scope:**
- Skill methodology logic and process definitions
- Agent prompt content that could be used to elicit harmful outputs
- Routing logic that could be manipulated to misroute queries
- Any local telemetry or feedback file handling (if telemetry is enabled)

**Out of scope:**
- Deal data, financial figures, or PII (the plugin does not collect or transmit these by default)
- Third-party integrations built on top of the plugin by users
- The Claude Code CLI itself (report those to Anthropic)

If you have extended the plugin with real API integrations or live deal data pipelines, standard application security practices apply to your extension.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 4.0.x   | Yes       |
| 3.0.x   | Yes       |
| 2.0.x   | Yes       |
| 1.0.x   | No        |

## Privacy

For information on how the plugin handles local telemetry and feedback data, see [PRIVACY.md](PRIVACY.md).
