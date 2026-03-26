---
name: feedback-summary
description: View aggregated feedback ratings and comments from CRE skill sessions
---

# CRE Skill Feedback Summary

Read `~/.cre-skills/feedback.jsonl`. If the file does not exist or is empty, respond:

```
No feedback data found. Enable the survey in ~/.cre-skills/config.json by setting "survey": true.
```

Otherwise, parse all JSONL records and produce the following sections.

## Overall Average Rating

Compute the mean of all non-null `rating` fields. Round to one decimal place. State the record count (N) used in the calculation.

## Average Rating by Skill

For each skill slug that appears in any record's `skills_used` array, compute the mean rating across all sessions that included that skill. Show the top 10 skills by session count. Present as a Markdown table with columns: Skill, Sessions, Avg Rating.

## Rating Distribution

Count occurrences of each rating value (1 through 5). Present as a simple ASCII histogram using pipe characters scaled to relative frequency. Example format:

```
5 | ████████████  (12)
4 | ████████      (8)
3 | ███           (3)
2 | █             (1)
1 |               (0)
```

Use block characters or dashes if block characters are unavailable.

## Recent Comments

List the 10 most recent records where `comment` is not null. For each, show the date and the comment text. Do not show rating or anonymous_id. Present as a simple numbered list.

## Trend

Compute this only if data spans >= 28 days (4 weeks).

Compare the average rating in the most recent 14 days vs. the 14 days before that.

- If the recent average is more than 0.2 points higher: label "Improving"
- If the recent average is more than 0.2 points lower: label "Declining"
- Otherwise: label "Stable"

Show the two period averages and the label. If fewer than 28 days of data exist, omit this section entirely.

---

Handle malformed lines in the JSONL file gracefully: skip unparseable lines and note how many were skipped at the end of the output. Records where both `rating` and `comment` are null were never written (by design), so no special handling is needed for them.
