# Task Board (final)

| ID | Task | Priority | Owner | Status | Definition of Done |
|----|------|----------|-------|--------|--------------------|
| P0-01 | Create branch / confirm working branch | P0 | Manager | DONE | feature/calculator-correctness-tests active |
| P0-02 | Restore incomplete deletions | P0 | Manager | DONE | SKILL.md + orchestrator files restored |
| P0-03 | Write session state seed files | P0 | Manager | DONE | 5 session_state files created |
| P1-01 | Map repo structure and claim surfaces | P1 | Mapper | DONE | See SESSION_STATUS baseline facts |
| P2-01 | Canonical metadata audit | P1 | Truth Auditor | DONE | 18 contradictions identified |
| P2-02 | Install/support matrix audit | P1 | Truth Auditor | DONE | All claimed targets have artifacts |
| P2-03 | Privacy/telemetry audit | P1 | Truth Auditor | DONE | C03, C04 found and fixed |
| P2-04 | Orchestrator honesty audit | P1 | Workflow Auditor | DONE | 10 canonical + 8 documentary prompts |
| P2-05 | CRE workflow credibility audit | P1 | Workflow Auditor | DONE | 6 workflows proofed via calculator tests |
| P3-01 | Canonical source-of-truth cleanup | P1 | Implementer | DONE | catalog.yaml v4.1.2; dual plugin.json synced; registry regenerated |
| P3-02 | Unify support matrix | P1 | Implementer | NOT_NEEDED | Audit found support matrix already consistent |
| P3-03 | Privacy/telemetry contract unification | P1 | Implementer | DONE | plugin.json default + hook default aligned (ask_each_time) |
| P3-04 | Release surface cleanup | P1 | Implementer | DONE | v2.0.0 binaries untracked; release notes filled for v1/v3/v4.1.x |
| P3-05 | Orchestrator triage fixes | P1 | Implementer | DONE | handoff-registry fixed; prompts/README.md documents wiring honestly |
| P4-01 | Workflow proof pack (5-7 workflows) | P2 | Implementer+Validator | DONE | Calculator correctness tests prove 6 workflows at math layer; orchestrator integrity tests prove routing/config layer |
| P5-01 | Regression gate: route -> skill | P1 | Implementer | DONE | TestRouterBehavior (existing) + TestOrchestratorConfigReferences (new) |
| P5-02 | Regression gate: calculator invocation | P1 | Implementer | DONE | Calculator correctness test validates each calculator; catalog source_path test validates wiring |
| P5-03 | Regression gate: docs/support/install/privacy consistency | P1 | Implementer | DONE | TestCountConsistency + TestVersionConsistency + TestFeedbackConfigParity (existing) |
| P5-04 | Release packaging integrity gate | P1 | Implementer | DONE | release.yml now blocks on release notes; TestReleaseNotesCoverage + TestDistCleanliness |
| P6-01 | Commit hardening work | P0 | Manager | TODO | Logical commit with clear message |
| P6-02 | Push branch to origin | P0 | Manager | TODO | origin/feature/calculator-correctness-tests reflects work |
| P6-03 | Open PR with summary | P0 | Manager | TODO | PR URL returned |
| P6-04 | Merge PR to main | P0 | Manager | TODO | PR state = merged |
| P6-05 | Verify origin/main | P0 | Manager | TODO | main HEAD contains merge commit |

## Counts
- P0 (bootstrap + git): 3 DONE, 5 TODO
- P1 (map + audits + fixes): 14 DONE, 0 TODO (1 NOT_NEEDED)
- P2 (proof + gates): 5 DONE, 0 TODO

**Phase 6 remaining: commit, push, PR, merge, verify.**
