---
name: usage-stats
description: View aggregated CRE skill usage statistics from local telemetry data
---

# CRE Skill Usage Stats

Read `~/.cre-skills/telemetry.jsonl`. If the file does not exist or is empty, respond:

```
No telemetry data found. Enable telemetry in ~/.cre-skills/config.json by setting "telemetry": true.
```

Otherwise, parse all JSONL records and produce the following sections.

## Top 10 Most-Used Skills

Filter records where `event == "skill_invoked"`. Count occurrences by `skill` field. Rank descending. Present as a numbered list with invocation counts.

## Workflow Chain Distribution

Group `skill_invoked` records by `workflow_chain`. For each chain, show total invocation count and percentage of all invocations. Use a Markdown table.

## Investor Type Distribution

Group `skill_invoked` records by `investor_type`. For each type, show count and percentage of all invocations. Use a Markdown table.

## Average Session Duration

Filter records where `event == "session_end"`. Compute mean of the `duration_minutes` field. Show the mean (rounded to one decimal) and the number of sessions included in the calculation. If no `session_end` records exist, note that session duration data is not yet available.

## Usage Trend

Determine the date range spanned by all records (earliest `date` to latest `date`).

- If range >= 60 days: show monthly invocation counts (skill_invoked records grouped by YYYY-MM).
- If range >= 14 days: show weekly invocation counts (grouped by ISO week).
- If range < 14 days: show daily invocation counts (grouped by date).

Present as a Markdown table with date period and count columns.

## Total Sessions

Count of records where `event == "session_end"`. State the count plainly.

---

Handle malformed lines in the JSONL file gracefully: skip unparseable lines and note how many were skipped at the end of the output. Fields missing from a record (`investor_type`, `workflow_chain`) should be treated as `"unknown"` rather than causing an error.
