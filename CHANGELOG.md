# Changelog

## [4.0.0] - 2026-04-02

### Added
- Canonical catalog system: catalog/catalog.yaml as single source of truth for all
  plugin metadata (196 items: 105 skills, 54 agents, 9 commands, 12 calculators,
  10 orchestrators, 6 workflows)
- Catalog schema: catalog/catalog.schema.json
- Build script: scripts/catalog-build.py (scan repo -> catalog.yaml + dist/catalog.json)
- Generator script: scripts/catalog-generate.py (catalog -> README, hooks, plugin.json,
  routing, registry)
- Catalog-driven router: routing/skill-dispatcher.mjs now reads dist/catalog.json with
  artifact-aware matching, confidence scoring, downstream recommendations, and markdown fallback
- Output styles: output-styles/ with 5 format templates (exec-brief, ic-memo,
  pm-action-list, lender-brief, lp-update)
- userConfig in plugin.json: primary_asset_types, preferred_markets, default_output_style,
  feedback_mode, brand_name
- ADR: docs/adr/0001-catalog-source-of-truth.md
- Migration guide: docs/MIGRATION.md
- Release checklist: docs/release-checklist.md
- Workspace entrypoints: 7 top-level skills (deal-intake, lease-strategy-papering,
  asset-ops-cockpit, capital-projects-development, fund-lp-reporting, navigator, plugin-admin)
- Persistent workspace state: local JSON storage for session continuity
- Next-best-action footer: mandatory structured output for workspace skills

### Changed
- Feedback default mode: ask_each_time -> local_only (privacy-first)
- Feedback backend_url default: pre-configured -> empty (opt-in remote submission)
- registry.yaml: manually maintained -> generated from catalog
- Router: markdown-table parsing -> catalog-driven with fallback
- README Key Stats: hardcoded -> generated from catalog (18 categories)
- Plugin version: 3.0.0 -> 4.0.0
- Stale doc references: added notices to USER-GUIDE.md for unimplemented CLI scripts

### Fixed
- PRIVACY.md: claimed remote submission was "Future -- Not Available Yet" when code
  had it active by default. Now accurately describes it as available but opt-in.
- docs/feedback-system.md: contradicted itself on default feedback mode
- feedback-summary command: now reads both feedback.jsonl and feedback-log.jsonl
- Hooks.json SessionStart prompt: counts now generated from catalog

## [3.0.0] - 2026-04-01

### Added
- Feedback system: /cre-skills:send-feedback and /cre-skills:report-problem commands for
  structured feedback intake without leaving the session
- Remote feedback submission via Vercel Function + Supabase backend at
  cre-skills-feedback-api.vercel.app (default mode: ask_each_time, user confirms each send)
- Automatic redaction of file paths, emails, digit sequences, and env vars from feedback
  text before storage (scripts/redact-feedback.mjs, 38 behavioral tests)
- Weekly feedback prompt: non-intrusive reminder at session end after 7+ days of use,
  shown once per 7 days, only when CRE skills were used in the session
- Feedback schemas: feedback-submission.schema.json, feedback-config.schema.json
- Architecture documentation: docs/feedback-system.md
- 38 redaction tests (tests/test-redaction.mjs) + 4 new structural integrity tests
- firstRunAt timestamp tracking for install age calculation

### Changed
- Total commands: 7 -> 9 (added send-feedback, report-problem)
- Config model: added feedback block (mode, include_context, backend_url, last_prompt_shown_at)
- hooks/hooks.json: SessionStart prompt updated with new commands
- hooks/telemetry-init.mjs: feedback config initialization + backfill for existing installs
- hooks/session-summary.mjs: weekly feedback prompt logic
- PRIVACY.md: documented structured feedback data flow, redaction rules, remote submission
- README.md: feedback section, updated stats (9 commands), project structure

## [2.5.0] - 2026-03-28

### Added
- construction-cost-estimator: full CSI MasterFormat cost estimation with 11 workflows including
  visual input (floor plans/drawings), generative output (ASCII mockups), and co-creation design
  loops. Includes construction_estimator.py calculator (zero dependencies), 925-line CSI cost
  database, 60+ city regional cost factors, and soft cost benchmarks reference.
- property-management-orchestrator: deep PM command center with 10 workflows across all asset
  types. Routes to downstream skills (building-systems, work-order-triage, PM operations, etc.).
  Includes 8 asset-type module stubs (multifamily through hospitality) for v3.0 deep-dive,
  IREM/BOMA KPI benchmarks, monthly report template, and vendor management framework.
- space-planning-redesign-orchestrator: multi-agent orchestrator for space redesign ideation
  with 5 specialist subagents (space programmer, design visualizer, cost estimator, market
  validator, ROI analyst). Includes amenity cost benchmarks, tenant survey templates,
  competitive audit framework, and ROI model template. Status: stub (full orchestration in v3.0).
- Windows .exe installer via Inno Setup (no admin privileges, auto-detects Claude Code + Desktop)
- GitHub Actions workflow for building Windows installer on windows-latest runner
- 12th Python calculator: construction_estimator.py

### Changed
- Total skills: 99 -> 105 (6 new)
- Total reference files: 225 -> 247 (22 new)
- routing/CRE-ROUTING.md updated with 3 new skill routing triggers
- hooks/hooks.json SessionStart prompt updated to 102 skills, 55 agents
- Install.ps1 added for Windows post-install configuration

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
