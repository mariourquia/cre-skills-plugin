---
name: customize-skill
description: Adapt a CRE skill to your workplace workflow -- creates a local override without modifying base skill files
---

# Customize a CRE Skill

Walk the user through creating or editing a local skill customization. Keep the tone conversational and non-technical. The user does not need to understand file paths or JSON.

## Step 1: Select a skill

Ask: "Which skill would you like to customize? You can name it, describe your use case, or type 'list' to browse."

- If the user names a skill, validate it exists via the `cre_route` MCP tool or by checking `${CLAUDE_PLUGIN_ROOT}/routing/CRE-ROUTING.md`.
- If the user says "list", use the `cre_list_skills` MCP tool to show available skills grouped by lifecycle phase.
- If the user describes a task, route it via `cre_route` and confirm the match.

Once confirmed, store the skill slug for subsequent steps.

## Step 2: Check for existing customization

Use the `cre_list_customizations` MCP tool to check if this skill already has a local override.

- **If yes:** Ask "You already have a customization for this skill (last updated [date]). Would you like to edit it, view it, or start fresh?"
  - Edit: proceed to Step 4 with the existing customized content.
  - View: show a summary via `cre_customization_detail` and ask what to do next.
  - Start fresh: revert the existing customization via `cre_revert_customization`, then proceed to Step 3.
- **If no:** Proceed to Step 3.

## Step 3: Initialize customization

First, check if there are templates for this skill using the `cre_list_templates` MCP tool. If a matching template exists, offer it:

"There's a pre-built template available for this skill: [template name]. It [template description]. Would you like to start from this template, or customize from scratch?"

If the user picks a template, use `cre_apply_template`. Otherwise, use `cre_customize_skill` with the skill slug. Tell the user:

"I've created a local copy of [skill name] that you can customize. Your changes won't affect the base plugin -- you can always revert to the original."

Read the base skill content via `cre_skill_detail` and show the user a summary of its structure:
- Persona / role
- Number of process steps
- Input schema highlights
- Output format

## Step 4: Guide the editing

Ask: "What would you like to change about this skill? Common customizations include:"

1. **Terminology** -- rename fields, labels, or roles to match your organization
2. **Approval / review chain** -- add or modify approval steps
3. **Required steps** -- add, remove, or reorder process steps
4. **Compliance / governance** -- add regulatory or policy requirements
5. **Deliverable format** -- change output structure, tables, or sections
6. **Tone / writing style** -- adjust formality, length, or audience
7. **Missing data fields** -- add inputs your workflow needs
8. **Output structure** -- restructure how results are presented
9. **Calculation method** -- change formulas, thresholds, or benchmarks
10. **Regional / market** -- adapt for a specific geography or market

Let the user describe their changes in their own words. Apply the changes to the SKILL.md content. After each change, confirm what was modified.

## Step 5: Save the customization

Once the user is satisfied, save the modified content via the `cre_save_customization` MCP tool.

Ask: "Why did you make this change? This helps us understand how teams use these skills differently."

Accept free-form text (1-2 sentences is fine). Store as the `rationale`.

Then ask: "Which of these categories best describe your changes? (pick all that apply)"

Present the numbered list from Step 4. Store as `change_categories`.

Optionally ask: "Any additional notes?" Store as `notes`.

## Step 6: Confirm and check health

Show a summary:
- Skill name and slug
- Status: active
- Categories: [selected tags]
- Rationale: [user text]
- Files: `~/.cre-skills/customizations/[slug]/SKILL.md`

Use the `cre_customization_health_check` MCP tool to verify the base skill is current. If drifted, mention it: "Note: The base version of this skill has been updated since the plugin was installed. You may want to review the upstream changes."

Tell the user: "This skill is now customized. Whenever you or the plugin use [skill name], it will use your version instead of the default."

Also mention:
- "You can export this customization to share with teammates: ask me to export it."
- "Run `/cre-skills:customization-analytics` to see patterns across all your customizations."

## Step 7: Feedback (encouraged)

Read the customization config from `~/.cre-skills/config.json` (the `customization` block). If missing, use defaults: `feedback_enabled: true`, `feedback_mode: metadata_only`, `require_consent: true`.

**If `feedback_enabled` is false or `feedback_mode` is "off":** Skip this step entirely.

**If `feedback_enabled` is true:**

Say: "Your customization helps the maintainer understand how teams are adapting these skills in practice. Sharing structured feedback (just the change categories and your rationale -- no deal data) directly shapes which skills get improved next."

Ask: "Would you like to share this with the plugin maintainer?"

Present what would be shared based on the configured mode:

- **metadata_only:** "I would share: skill name, change categories, your rationale, and content fingerprints (hashes, not actual content). No skill text or diff is included."
- **metadata_and_summary:** "I would share the above plus a summary of changes (e.g., '12 lines added, 3 removed, Process section affected')."
- **metadata_and_diff:** "I would share the above plus the full line-by-line diff."
- **metadata_and_content:** "I would share the above plus the full customized skill content. This requires your explicit consent."

If the user says yes:
1. Build the payload via `cre_submit_customization_feedback` MCP tool.
2. If `dry_run` is true, show the preview and stop.
3. If `require_consent` is true, show the preview first and ask "Send this? (yes/no)".
4. On consent, submit. Report success or local-save fallback.

Also ask: "Would you like the maintainer to consider incorporating your changes into a future plugin version?"
Store as `wants_upstream_consideration`.

If the user declines feedback, confirm: "No problem. Your customization is saved locally and fully functional."

## Notes

- Never send content without the user seeing a preview first.
- Never send anything when `feedback_mode` is "off" or `feedback_enabled` is false.
- If the remote send fails, the payload is saved locally and queued for retry. Tell the user: "Saved locally. The feedback will be retried next session."
- Customizations persist at `~/.cre-skills/customizations/`. They survive plugin updates unless the user explicitly reverts them.
- If the user asks how to revert: "Run `/cre-skills:customize-skill` and choose the skill, then select 'start fresh', or I can revert it right now."
