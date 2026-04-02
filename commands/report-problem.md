---
name: report-problem
description: Report a bug or problem with a CRE skill, workflow, or orchestrator
---

# Report a Problem

Guide the user through submitting a structured bug report. Use conversational tone.

## Step 1: What were you trying to do?

Ask: "What were you trying to do when the problem happened?"

Accept free-form text. This goes into `context.what_user_tried`.

## Step 2: What happened?

Ask: "What happened instead of what you expected?"

Accept free-form text. This goes into `context.what_happened`.

## Step 3: Severity

Ask: "How serious was this?"

1. **Critical** -- blocked your work entirely, no workaround
2. **High** -- significantly impacted output quality or accuracy
3. **Medium** -- noticeable issue but you could work around it
4. **Low** -- minor annoyance, cosmetic, or edge case

## Step 4: Which skill, workflow, or orchestrator?

Ask which skill, workflow, or orchestrator was involved. Accept a slug, a plain description, or "not sure". Validate against the routing index at `${CLAUDE_PLUGIN_ROOT}/routing/CRE-ROUTING.md` if the user provides a name.

If the user ran an orchestrator pipeline, also capture the orchestrator slug.

## Step 5: Additional details (optional)

Ask: "Anything else you'd like to add? (Enter to skip)"

This is the main `message` field.

## Step 6: Contact (optional)

Ask: "Want to include your email so the maintainer can follow up? (Enter to skip)"

If provided, also ask for organization name (optional).

## Step 7: Context

Read `~/.cre-skills/config.json`. If `feedback.include_context` is true (or the key doesn't exist, default to true):

- Read `~/.cre-skills/telemetry.jsonl` and extract:
  - `context.skills_used_this_session`: today's skill slugs
  - `context.skills_used_last_30d`: deduplicated list of all skill slugs from the last 30 days, with per-skill invocation count (e.g. `{"deal-quick-screen": 12, "rent-roll-analyzer": 5}`)
  - `context.total_sessions_last_30d`: count of unique dates in the last 30 days
- Tell the user: "I'll include your recent skill usage summary (last 30 days) as context. This is just skill names and counts -- no deal data, prompts, or stack traces."

If the user objects, omit the context.

## Step 8: Sanitize and save

1. Read `~/.cre-skills/config.json` to get `anonymousId`.
2. Read `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` to get the current `version`.
3. Generate a submission ID: `fb_` followed by 16 random hex characters.
4. Compute `install_id_hash` as SHA-256 hex of the `anonymousId`.
5. Compose the message: if the user provided additional details in Step 5, use that. Otherwise, concatenate Step 1 and Step 2 responses.
6. Run the redaction utility:
   ```bash
   echo '<submission_json>' | node "${CLAUDE_PLUGIN_ROOT}/scripts/redact-feedback.mjs"
   ```
7. Build the final record matching `schemas/feedback-submission.schema.json`:

```json
{
  "submission_id": "fb_<hex16>",
  "submission_type": "bug",
  "timestamp": "<ISO 8601>",
  "plugin_version": "<from plugin.json>",
  "install_id_hash": "<sha256 of anonymousId>",
  "message": "<redacted message or combined Step 1 + Step 2>",
  "rating": null,
  "severity": "<low|medium|high|critical>",
  "category": null,
  "skill_slug": "<slug or null>",
  "workflow_slug": "<slug or null>",
  "orchestrator_slug": "<slug or null>",
  "cre_domain": null,
  "contact_email": "<email or null>",
  "organization": "<org or null>",
  "context": {
    "skills_used_this_session": [...],
    "error_category": null,
    "what_user_tried": "<redacted>",
    "what_happened": "<redacted>"
  }
}
```

8. Append the JSON record as a single line to `~/.cre-skills/feedback-log.jsonl`.

## Step 9: Remote submission (if configured)

Read `feedback.mode` and `feedback.backend_url` from `~/.cre-skills/config.json`.

**If `mode` is `local_only` OR `backend_url` is empty:** skip remote submission. Confirm:

```
Bug report saved locally to ~/.cre-skills/feedback-log.jsonl
View your feedback history with /cre-skills:feedback-summary

For critical issues, you can also open an issue at:
https://github.com/mariourquia/cre-skills-plugin/issues
```

**If `mode` is `ask_each_time`:** ask the user: "Would you also like to send this to the plugin maintainer? (yes/no)". If no, skip. If yes, proceed to send.

**If `mode` is `anonymous_remote`:** send automatically. Strip `contact_email` and `organization` before sending.

**If `mode` is `remote_with_contact`:** send automatically with all fields.

**To send:** POST the redacted JSON record to `feedback.backend_url` with headers:
```
Content-Type: application/json
X-Plugin-Version: <version>
```

- On success (2xx): confirm "Bug report saved locally and sent to maintainer."
- On failure (network error, non-2xx): confirm "Bug report saved locally. Remote submission failed -- it will be retried next session." Append the submission to `~/.cre-skills/outbox.jsonl` for retry (Slice 3 retry logic).
- Never block the session on a failed send. Local save is always the source of truth.

## Notes

- Never include prompt content, AI responses, deal data, financial figures, or full stack traces.
- Error information should be reduced to a high-level category (e.g., "FileReadError", "SchemaValidation", "OrchestratorTimeout") rather than raw trace output.
- If `~/.cre-skills/` doesn't exist, create it.
- Local save always happens regardless of remote submission outcome.
