---
name: customization-analytics
description: View aggregated analytics about local skill customizations -- which skills are adapted most, common change patterns, and upstream suggestion rate
---

# Customization Analytics

Show the user a summary of their local customization activity and feedback patterns.

## Step 1: Gather data

Use the `cre_customization_analytics` MCP tool to get aggregated statistics from the local feedback log.

Also use `cre_list_customizations` to get the current active customizations.

And use `cre_customization_health_check` with `all: true` to check for drift across all customizations.

## Step 2: Present the dashboard

Format the results as a clear summary:

### Active Customizations
- Total count
- List each with slug, status, and last updated date

### Health Status
- How many are current (base unchanged)
- How many have drifted (base updated since customization)
- Flag any that need attention

### Feedback Patterns (if feedback exists)
- Total customization feedback entries
- Skills most frequently customized (top 5, with counts)
- Most common change categories (bar-chart style, sorted by count)
- Upstream suggestion rate (% of customizations where user wanted maintainer to consider)
- Sections most changed (what parts of skills are being adapted)
- Monthly trend (if enough data)

### Insights
Based on the data, offer 2-3 actionable observations. Examples:
- "70% of your customizations are in the 'compliance_governance' category -- consider applying the ESG pre-screening template to other underwriting skills."
- "3 of your 5 customizations have drifted. Run the health check to review upstream changes."
- "You've requested upstream consideration for 4 customizations. Consider running /cre-skills:customize-skill on those to generate GitHub issue suggestions."

## Notes

- If there are no customizations or feedback yet, say so and suggest trying `/cre-skills:customize-skill`.
- All data comes from local files only. Nothing is fetched remotely.
- The analytics are only as good as the feedback the user has submitted. If they've been saving locally without feedback, the patterns section will be sparse.
