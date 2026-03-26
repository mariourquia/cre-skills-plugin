---
name: cre-workflows
description: "Show available CRE multi-skill workflow chains (acquisition pipeline, capital stack, hold period, disposition, development, fund management)."
---

# CRE Workflow Chains

Read the workflow chain index from `${CLAUDE_PLUGIN_ROOT}/routing/CRE-ROUTING.md` (the "Workflow Chains" section) and present the available chains to the user.

If the user specified a workflow ("$ARGUMENTS"), read the detailed workflow document from `${CLAUDE_PLUGIN_ROOT}/routing/workflows/` for that chain and walk the user through it step by step, invoking each skill in sequence.

Available chains:
1. **Acquisition Pipeline**: sourcing -> screening -> tenant-credit -> underwriting -> IC memo -> LOI -> PSA -> financing (term sheet + loan docs) -> DD (title + transfer docs) -> closing (checklist + funds flow) -> post-close
2. **Capital Stack Assembly**: underwriting -> loan sizing -> term-sheet-builder -> mezz/pref -> JV waterfall -> optimizer -> refi
3. **Hold Period Management**: budget -> dashboard -> capex/compliance/delinquency/retention -> NOI sprint
4. **Disposition Pipeline**: dashboard -> strategy (sell/hold/refi) -> prep -> 1031 exchange
5. **Development Pipeline**: land residual + entitlements -> proforma -> construction -> lease-up -> perm takeout
6. **Fund Management**: formation -> pitch deck -> capital raise -> deploy -> quarterly update -> attribution
