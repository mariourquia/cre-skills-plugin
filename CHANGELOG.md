# Changelog

## [2.0.0] - 2026-03-25

### Added
- 11 orchestrator gap skills (total: 91 skills, 88 unique skill directories)
- Python calculator scripts: debt_sizing, covenant_tester, npv_trade_out, option_valuation,
  proration_calculator, tenant_credit_scorer, waterfall_calculator
- PostToolUse hook (telemetry-capture.mjs) -- tracks skill invocations when telemetry is opt-in
- Stop hook (session-summary.mjs) -- writes session_end record and optional feedback prompt
- telemetry-init.mjs SessionStart hook -- initializes ~/.cre-skills/config.json on first run
- scripts/update.sh -- pulls latest, handles major version migration, preserves user data
- scripts/uninstall.sh -- clean removal with user data preservation prompt
- scripts/verify-install.sh -- full health check (skills, refs, calculators, hooks, data dir)
- docs/install-guide.md -- comprehensive installation guide for all platforms

### Changed
- License changed from MIT to Apache 2.0 (adds explicit patent grant)
- NOTICE file added for Apache 2.0 compliance
- scripts/install.sh updated for v2: Node.js/Python checks, v1->v2 migration, backup, calculators
- Install.command version string updated to v2.0.0
- README.md: updated skill count (91), license reference, DMG version string
- hooks/telemetry-capture.mjs: replaced /dev/stdin with fd 0 for Windows WSL compatibility

### Breaking Changes
- License: MIT -> Apache 2.0. Existing installations continue to function; license governs
  redistribution and use going forward.

---

## [1.0.0] - 2026-03-17

### Added
- 80 CRE skill packs across 16 subcategories
- 171 reference files (formulas, templates, frameworks, worked examples)
- 40 expert subagent definitions across 8 categories
- 6 workflow chain documents
- 3 plugin commands (cre-route, cre-workflows, cre-agents)
- SessionStart hook for context-efficient routing
- Machine-readable skill registry (registry.yaml)
- CRE routing index for skill discovery
- MIT license
