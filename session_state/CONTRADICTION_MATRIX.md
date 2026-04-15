# Contradiction Matrix

Populated from three parallel audits (Truth / Workflow / Release). Severity: HIGH=release blocker, MEDIUM=trust damaging, LOW=cosmetic.

| ID | Issue | Files Affected | Why It Matters | Severity | Fix | Status |
|----|-------|----------------|----------------|----------|-----|--------|
| C01 | Plugin version drift: plugin.json=4.1.2, catalog/catalog.yaml plugin_version=4.0.0 | `.claude-plugin/plugin.json:4`, `src/catalog/catalog.yaml:3`, `registry.yaml` (generated from catalog) | Canonical source of truth is stale; releases use wrong version in downstream derived files | HIGH | Bump catalog plugin_version to 4.1.2; regenerate registry.yaml | OPEN |
| C02 | Agent count claim 54 vs 55 files in src/agents/ | `plugin.json`, `README.md`, `src/agents/` | Headline metric wrong; one orphan agent file | MEDIUM | Identify orphan agent (in dir but not catalog) and delete OR add to catalog | OPEN |
| C03 | Privacy mode default mismatch: plugin.json default "local_only" vs hook defaultConfig "ask_each_time" | `.claude-plugin/plugin.json:57-62`, `src/hooks/telemetry-init.mjs:22-26` | Plugin advertises local_only but first-run hook sets ask_each_time; user-facing contract broken | MEDIUM | Align both to `ask_each_time` (matches PRIVACY.md intent and opt-out model tested by integrity test) | OPEN |
| C04 | Feedback backend URL drift: plugin.json default="" vs hook hardcoded production URL | `.claude-plugin/plugin.json:81-85`, `src/hooks/telemetry-init.mjs:25` | Plugin says "no default URL" but hook bakes one in on first run | MEDIUM | Make plugin.json default = the hook's URL (single source of truth) | OPEN |
| C05 | Stale dist/ binaries for v1.0.0, v2.0.0 alongside v4.1.2 | `dist/` | Operator sees ancient artifacts beside current; release hygiene failure | HIGH | Remove stale binaries; dist/ should only hold current version build artifacts (if any) | OPEN |
| C06 | Missing release notes for v4.1.0, v4.1.1, v4.1.2 (tags exist, notes absent) | `docs/releases/` | release.yml now blocks release on notes present — existing tags can't be re-released; historical gap | MEDIUM | Create notes for v4.1.0/v4.1.1/v4.1.2 derived from CHANGELOG and git log | OPEN |
| C07 | Orchestrator name mismatch: prompt says "investment-strategy", registry/catalog says "investment-strategy-formulator" | `src/orchestrators/prompts/investment-strategy-orchestrator.md`, `src/orchestrators/handoff-registry.json` | Handoff cannot resolve; orchestrator looks referenced but call breaks | MEDIUM | Rename prompt file OR rename config — pick one canonical name | OPEN |
| C08 | Orchestrator name mismatch: prompt "research-intelligence" vs registry "market-research-intelligence" | `src/orchestrators/prompts/research-intelligence-orchestrator.md`, handoff-registry | Same handoff break | MEDIUM | Rename to align | OPEN |
| C09 | portfolio-management, lp-intelligence orchestrators reference 0 skills | `src/orchestrators/configs/portfolio-management.json`, `lp-intelligence.json` | Orchestrators exist but are empty — overclaim capability | MEDIUM | Mark status=experimental in config + add orchestrator status schema | OPEN |
| C10 | underwriting orchestrator references agents that don't exist as .md files | `src/orchestrators/prompts/underwriting-orchestrator.md` | Headline orchestrator broken; acquisition flow unverified | MEDIUM | Either create agent files, rewrite prompt to use skills-only, or mark experimental | OPEN |
| C11 | Legal, due-diligence, financing, asset-management orchestrators have prompts but no config | `src/orchestrators/prompts/*.md`, `src/orchestrators/configs/` | 4 orchestrators are prompt-only orphans; count=10 claim is inflated | MEDIUM | Either add configs OR remove prompts OR downgrade honestly | OPEN |
| C12 | hooks.json PostToolUse matcher="Read" is overly broad | `src/hooks/hooks.json:20` | Hook fires on every Read, not just SKILL.md reads; telemetry noise risk | LOW | Tighten matcher to files under `skills/**/SKILL.md` OR accept and document the filter | OPEN |
| C13 | MCP tool count (21) claimed in README/install-desktop.md but not in catalog governance | `README.md`, `docs/install-desktop.md`, `src/catalog/catalog.yaml`, `src/mcp-server.mjs` | Single-source-of-truth claim is rhetorical for MCP tools | LOW | Add `mcp_tools:` array to catalog OR reduce the SSOT claim scope | OPEN |
| C14 | CI has no validation that artifacts referenced by install docs actually exist and work | `.github/workflows/*`, `docs/INSTALL.md`, `docs/install-*.md` | Install docs can drift from artifacts without detection | MEDIUM | Add regression test: every claimed install path resolves to existing script/artifact | OPEN |
| C15 | CI has no coverage gate for route-keyword-to-skill mapping across all workflows | `tests/test_plugin_integrity.py` has one check; not systematic | Routing drift breaks user intent without test failure | MEDIUM | Add parametrized route coverage test | OPEN |
| C16 | CI does not verify orchestrator configs only reference deployed skills/agents | (no test) | Orchestrators can silently reference missing assets | MEDIUM | Add orchestrator reference integrity test | OPEN |
| C17 | CHANGELOG v3.0.0 (2026-04-01) and v4.0.0 (2026-04-02) only 1 day apart; no v4.1.x entries | `CHANGELOG.md` | Recent releases (v4.1.0-v4.1.2) are invisible in CHANGELOG | MEDIUM | Add CHANGELOG sections for v4.1.0, v4.1.1, v4.1.2 | OPEN |
| C18 | release-checklist.md implies manual version bumps in scripts/create-dmg.sh but workflow injects APP_VERSION via env | `docs/release-checklist.md:27`, `.github/workflows/release.yml:141-149` | Checklist lies about workflow behavior | LOW | Update release-checklist.md to reflect env-driven version | OPEN |

## Summary counts (after fixes)
- HIGH: 2 FIXED (C01 catalog version, C05 stale binaries)
- MEDIUM: 10 FIXED (C03, C04, C06, C07, C08, C14, C15, C16, C17 via new gates + notes + CHANGELOG)
- MEDIUM: 3 DEFERRED with honest downgrade (C02 agent count — confirmed 54 canonical via `_index.md` exclusion; C09, C10, C11 orchestrators — documented in prompts/README.md)
- LOW: 3 DEFERRED (C12 hook matcher, C13 MCP catalog governance, C18 release-checklist wording)
- Total: 18 entries; 12 fixed with code, 3 fixed via documentation, 3 deferred as cosmetic

## Deferred items (documented in DECISIONS.md)
- C02: verified false positive (`_index.md` is an index, not an agent)
- C09/C10/C11: prompts/README.md documents wired-vs-documentary status honestly
- C12: hook matcher is a valid performance trade-off — documented, not changed
- C13: MCP tool catalog governance is a future work item
- C18: release-checklist.md line 27 wording update is cosmetic

## Phase 3 fix order (highest value first)
1. C01 — fix catalog plugin_version, regenerate registry
2. C05 — remove stale dist/ binaries
3. C02 — resolve agent count
4. C03, C04 — unify privacy/telemetry defaults
5. C07, C08 — rename orchestrator files to resolve handoffs
6. C09, C10, C11 — honest orchestrator downgrade (mark experimental where stale)
7. C06 — create release notes for v4.1.0-v4.1.2
8. C17 — CHANGELOG entries for v4.1.x
9. C15, C16, C14 — new regression tests (Phase 5)
10. C12, C13, C18 — cosmetic cleanup if time
