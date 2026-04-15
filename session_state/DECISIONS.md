# Decisions

## D01
- Date: 2026-04-15
- Topic: Stay on feature/calculator-correctness-tests as the hardening branch
- Decision: Add hardening commits on top of existing calculator-tests commit; single PR to main
- Reason: Calculator tests are already a regression gate (Phase 5 requirement); bundling avoids stacked-branch overhead for a one-session effort
- Files affected: None (branch decision)
- Follow-up needed: None

## D02
- Date: 2026-04-15
- Topic: Restore half-finished WIP deletions
- Decision: Restored 11 SKILL.md files, 5 orchestrator prompts, and 19 reference files
- Reason: Deletions conflicted with canonical 112-skill claim in plugin.json/registry.yaml/README/docs; removing them would require a massive cascade of doc/registry edits
- Files affected: src/skills/**, src/orchestrators/prompts/**, src/orchestrators/configs/**, src/orchestrators/engine/**
- Follow-up needed: None

## D03
- Date: 2026-04-15
- Topic: Duplicate plugin.json at `.claude-plugin/plugin.json` and `src/plugin/plugin.json`
- Decision: Keep both files, sync them to identical content; do not delete either
- Reason: 10+ shell/Python scripts reference src/plugin/plugin.json. Deleting would require updating all of them; out of scope for this session. Syncing closes the drift risk.
- Files affected: `.claude-plugin/plugin.json`, `src/plugin/plugin.json`
- Follow-up needed: Future session — update catalog-build.py and shell scripts to read `.claude-plugin/plugin.json` as the single source, then delete src/plugin/plugin.json

## D04
- Date: 2026-04-15
- Topic: Feedback mode default reconciliation
- Decision: plugin.json default set to `ask_each_time` (was `local_only`)
- Reason: The hook's defaultConfig (telemetry-init.mjs line 23) uses `ask_each_time`, the integrity test asserts `ask_each_time`, and PRIVACY.md+README describe an opt-in-with-prompt model. Plugin.json was the outlier and had to move.
- Files affected: `.claude-plugin/plugin.json`, `src/plugin/plugin.json`
- Follow-up needed: None

## D05
- Date: 2026-04-15
- Topic: Orchestrator 8-prompts-without-configs honesty problem
- Decision: Kept the 8 orphan prompts in place; added `src/orchestrators/prompts/README.md` that explicitly documents which 8 prompts are WIRED (have configs, counted in 10) and which 8 are DOCUMENTARY (not loaded by engine, not in catalog, not counted).
- Reason: Deletion would lose design-reference value; silent retention would inflate apparent capability. Documentation is the honest middle path and is cheap.
- Files affected: `src/orchestrators/prompts/README.md` (new)
- Follow-up needed: Future session — either wire each documentary prompt into a config OR delete if no longer valuable

## D06
- Date: 2026-04-15
- Topic: Stale schema file deletions not restored
- Decision: Let unstaged deletions of 4 schema files persist:
  - src/schemas/financial-planning/business-plan.schema.json
  - src/schemas/phases/disposition-closing-data.schema.json
  - src/schemas/phases/lp-terms-data.schema.json
  - src/schemas/pm/adapter-interface.schema.json
- Reason: grep across src/, scripts/, tests/, docs/ found zero references. They are unused stale artifacts. Tests pass without them. Aligns with "prefer deletion over expansion".
- Files affected: 4 schema JSON files
- Follow-up needed: None

## D07
- Date: 2026-04-15
- Topic: Handoff registry cleanup strategy
- Decision: Renamed 2 mismatched orchestrator IDs (investment-strategy-formulator → investment-strategy-orchestrator; market-research-intelligence → research-intelligence-orchestrator) and dropped 2 handoffs referencing non-existent pm-operations-orchestrator
- Reason: 17 handoffs down to 15; remaining handoffs reference only the 9 orchestrators that actually participate in chains (10th, lp-intelligence, is directly invoked). All passing regression test assertions.
- Files affected: `src/orchestrators/handoff-registry.json`
- Follow-up needed: None (if pm-operations coordination is needed in the future, create a config first, then add handoffs)

## D08
- Date: 2026-04-15
- Topic: Scope of regression gates
- Decision: 3 new test files, 14 new tests, covering: version sync, count sync, source_path integrity, orchestrator handoff/config/skill integrity, dist binary hygiene, release notes coverage
- Reason: These are the minimum set that prevents every HIGH and MEDIUM contradiction from re-emerging undetected. Each test maps 1:1 to a matrix entry.
- Files affected: tests/test_canonical_consistency.py, tests/test_orchestrator_integrity.py, tests/test_release_hygiene.py
- Follow-up needed: None (existing ci.yml already runs `pytest tests/` which picks them up automatically)
