---
name: cre-route
description: "Find the right CRE skill for your task. Catalog-driven router with intent matching, artifact awareness, and confidence scoring."
---

# CRE Skill Router

Route the user's CRE task to the correct specialist skill using the catalog-driven dispatcher.

If the user provided arguments ("$ARGUMENTS"), run the dispatcher to match:

```bash
node "${CLAUDE_PLUGIN_ROOT}/routing/skill-dispatcher.mjs" "$ARGUMENTS"
```

Based on the JSON result:
1. If confidence is "high": invoke the recommended skill directly
2. If confidence is "medium": present the recommendation and alternatives, ask user to confirm
3. If confidence is "low" or "none": show alternatives, fall back to reading `${CLAUDE_PLUGIN_ROOT}/routing/CRE-ROUTING.md` for browsing

If no arguments provided, show the category summary from `${CLAUDE_PLUGIN_ROOT}/routing/CRE-ROUTING.md`.

Do NOT load all SKILL.md files. Only load the specific skill identified by the router.

## Artifact-Aware Routing

If the user mentions a specific document type, pass it as an artifact filter:

```bash
node "${CLAUDE_PLUGIN_ROOT}/routing/skill-dispatcher.mjs" --artifact "OM" "analyze this offering memorandum"
```

## Flags

- `--list`: print all registered skill slugs
- `--include-hidden`: include stub and experimental skills in results
- `--artifact <type>`: boost skills that accept this input artifact type (OM, rent roll, lease, T-12, budget, term sheet, PSA, LOI)
