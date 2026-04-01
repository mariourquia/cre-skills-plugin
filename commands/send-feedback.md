---
name: send-feedback
description: Share feedback about CRE Skills -- quality, suggestions, or general comments
---

# Share Feedback About CRE Skills

Guide the user through submitting structured feedback. Use conversational tone, no jargon.

## Step 1: Category

Ask what the feedback is about. Present these options:

1. **Skill quality** -- a skill's output, process, or accuracy
2. **Missing capability** -- something that should exist but doesn't
3. **Documentation** -- unclear instructions, missing references
4. **Workflow or orchestrator** -- multi-step pipeline behavior
5. **General** -- anything else

## Step 2: Which skill or workflow (optional)

Ask which skill, workflow, or orchestrator this relates to. Accept a slug, a plain description, or "not sure". If the user names something, validate it exists by checking the routing index at `${CLAUDE_PLUGIN_ROOT}/routing/CRE-ROUTING.md`. If it doesn't match, suggest the closest match or proceed with the user's text.

## Step 3: Rating (optional)

Ask: "On a scale of 1-5, how would you rate your experience? (Enter to skip)"

- 5 = Excellent
- 4 = Good
- 3 = Okay
- 2 = Poor
- 1 = Very poor

## Step 4: Message

Ask: "What would you like to share?"

Accept free-form text. Minimum 1 character, maximum 5000 characters.

## Step 5: Contact (optional)

Ask: "Want to include your email for follow-up? (Enter to skip)"

If provided, also ask for organization name (optional).

## Step 6: Context

Read `~/.cre-skills/config.json`. If `feedback.include_context` is true (or the key doesn't exist, default to true):

- Read `~/.cre-skills/telemetry.jsonl` and extract today's skill slugs for this session.
- If skills were found, include them as `context.skills_used_this_session`.
- Tell the user: "I'll include the skill slugs used in this session as context. No deal data or prompts are included."

If the user objects, omit the context.

## Step 7: Sanitize and save

1. Read `~/.cre-skills/config.json` to get `anonymousId` and plugin version.
2. Read `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` to get the current `version`.
3. Generate a submission ID: `fb_` followed by 16 random hex characters.
4. Compute `install_id_hash` as SHA-256 hex of the `anonymousId`.
5. Run the redaction utility on the message and context fields:
   ```bash
   echo '<submission_json>' | node "${CLAUDE_PLUGIN_ROOT}/scripts/redact-feedback.mjs"
   ```
6. Build the final record matching `schemas/feedback-submission.schema.json`:

```json
{
  "submission_id": "fb_<hex16>",
  "submission_type": "general",
  "timestamp": "<ISO 8601>",
  "plugin_version": "<from plugin.json>",
  "install_id_hash": "<sha256 of anonymousId>",
  "message": "<redacted message>",
  "rating": <1-5 or null>,
  "severity": null,
  "category": "<selected category>",
  "skill_slug": "<slug or null>",
  "workflow_slug": "<slug or null>",
  "orchestrator_slug": "<slug or null>",
  "cre_domain": null,
  "contact_email": "<email or null>",
  "organization": "<org or null>",
  "context": { ... } or null
}
```

7. Append the JSON record as a single line to `~/.cre-skills/feedback-log.jsonl`.

## Step 8: Remote submission (if configured)

Read `feedback.mode` and `feedback.backend_url` from `~/.cre-skills/config.json`.

**If `mode` is `local_only` OR `backend_url` is empty:** skip remote submission. Confirm:

```
Feedback saved locally to ~/.cre-skills/feedback-log.jsonl
View your feedback history with /cre-skills:feedback-summary
```

**If `mode` is `ask_each_time`:** ask the user: "Would you also like to send this to the plugin maintainer? (yes/no)". If no, skip. If yes, proceed to send.

**If `mode` is `anonymous_remote`:** send automatically. Strip `contact_email` and `organization` before sending.

**If `mode` is `remote_with_contact`:** send automatically with all fields.

**To send:** POST the redacted JSON record to `feedback.backend_url` with headers:
```
Content-Type: application/json
X-Plugin-Version: <version>
```

- On success (2xx): confirm "Feedback saved locally and sent to maintainer."
- On failure (network error, non-2xx): confirm "Feedback saved locally. Remote submission failed -- it will be retried next session." Append the submission to `~/.cre-skills/outbox.jsonl` for retry (Slice 3 retry logic).
- Never block the session on a failed send. Local save is always the source of truth.

## Notes

- Never include prompt content, AI responses, deal data, or financial figures in the submission.
- If `~/.cre-skills/` doesn't exist, create it.
- If the config file is missing or malformed, proceed with defaults (generate a fresh anonymousId, use "unknown" for version).
- Local save always happens regardless of remote submission outcome.
