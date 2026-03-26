---
name: cre-route
description: "Find the right CRE skill for your task. Reads the routing index and recommends which skill(s) to invoke. Covers 98 CRE skills across 16 subcategories."
---

# CRE Skill Router

Read the routing index at `${CLAUDE_PLUGIN_ROOT}/routing/CRE-ROUTING.md` and use it to identify the correct skill(s) for the user's request.

If the user provided arguments ("$ARGUMENTS"), match their request against the routing table and either:
1. Invoke the matching skill directly if there's a clear match
2. Present the top 2-3 matches if ambiguous, and ask the user to pick

If no arguments provided, show the category summary from the routing index.

Do NOT load all SKILL.md files. Only load the specific skill identified by the routing index.
