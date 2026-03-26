# Changelog

## [2.0.0] - 2026-03-25

### Added
- 19 new skills (total: 99 skills): title-commitment-reviewer, tenant-credit-analyzer,
  term-sheet-builder, loan-document-reviewer, transfer-document-preparer, funds-flow-calculator,
  lease-option-structurer, lease-trade-out-analyzer, gp-performance-evaluator, fund-terms-comparator,
  lp-data-request-generator, sec-reg-d-compliance, monte-carlo-return-simulator,
  property-management-operations, distribution-notice-generator, 1031-pipeline-manager,
  deal-attribution-tracker, emerging-manager-evaluator, fund-raise-negotiation-engine
- 11 Python calculator scripts (zero dependencies): debt_sizing, covenant_tester, npv_trade_out,
  option_valuation, proration_calculator, quick_screen, tenant_credit_scorer, transfer_tax,
  waterfall_calculator, monte_carlo_simulator, fund_fee_modeler
- Orchestration engine: 10 multi-agent pipelines (acquisition, capital-stack, hold-period,
  disposition, development, fund-management, research, strategy, portfolio, lp-intelligence)
  with 10 JSON configs, 16 prompt files, 8 investor profiles, strategy matrix, challenge layer,
  disagreement/reversal schemas, and cross-chain handoff registry
- 14 lifecycle agents across research, strategy, asset-management, portfolio, fund, disposition,
  and LP intelligence categories (total: 54 agents)
- 225 reference files (up from 171 in v1.0.0)
- Brand guidelines system: auto-loads from ~/.cre-skills/brand-guidelines.json for 8 deliverable skills
- PostToolUse hook (telemetry-capture.mjs) -- tracks skill invocations when telemetry is opt-in
- Stop hook (session-summary.mjs) -- writes session_end record and optional feedback prompt
- telemetry-init.mjs SessionStart hook -- initializes ~/.cre-skills/config.json on first run
- 4 new commands: brand-config, orchestrate, usage-stats, feedback-summary (total: 7 commands)
- scripts/update.sh -- pulls latest, handles major version migration, preserves user data
- scripts/uninstall.sh -- clean removal with user data preservation prompt
- scripts/verify-install.sh -- full health check (skills, refs, calculators, hooks, data dir)
- docs/install-guide.md -- comprehensive installation guide for all platforms
- PRIVACY.md, SECURITY.md

### Changed
- License changed from MIT to Apache 2.0 (adds explicit patent grant)
- NOTICE file added for Apache 2.0 compliance with Avi Hacker attribution
- scripts/install.sh updated for v2: Node.js/Python checks, v1->v2 migration, backup, calculators
- Install.command version string updated to v2.0.0
- README.md rewritten for v2.0.0 with full skill catalog, workflow chains, calculators, brand guidelines
- hooks/telemetry-capture.mjs: replaced /dev/stdin with fd 0 for Windows WSL compatibility
- verify-install.sh: counts all reference files (*.md + *.yaml), not just *.md


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
