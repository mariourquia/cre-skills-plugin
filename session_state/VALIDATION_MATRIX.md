# Validation Matrix

| Check | Scope | Pass Criteria | Status | Notes |
|-------|-------|---------------|--------|-------|
| Calculator value correctness | tests/test_calculator_correctness.py | All 12 calculators return expected values within tolerance | PASS | 31 tests pass |
| Plugin integrity (original) | tests/test_plugin_integrity.py | Manifests valid, no orphans, router + MCP work | PASS | 53 tests pass |
| Version consistency (new) | tests/test_canonical_consistency.py::TestVersionConsistency | plugin.json version == catalog.yaml plugin_version; valid semver | PASS | 2 tests |
| Count consistency (new) | tests/test_canonical_consistency.py::TestCountConsistency | Every numeric claim in plugin.json description matches catalog+filesystem | PASS | 2 tests (skills/agents/calc/orch/workflows + reference files) |
| Source-path integrity (new) | tests/test_canonical_consistency.py::TestCatalogIntegrity | Every catalog source_path resolves to a file on disk | PASS | 1 test |
| Handoff integrity (new) | tests/test_orchestrator_integrity.py::TestHandoffRegistryIntegrity | Every handoff source/target references a real orchestrator config; no duplicate IDs | PASS | 3 tests |
| Orchestrator skill refs (new) | tests/test_orchestrator_integrity.py::TestOrchestratorConfigReferences | Every skill referenced by an orchestrator config is deployed | PASS | 1 test |
| Orchestrator count (new) | tests/test_orchestrator_integrity.py::TestOrchestratorCountMatchesCatalog | 10 configs = 10 catalog orchestrator entries = claim | PASS | 2 tests |
| Dist cleanliness (new) | tests/test_release_hygiene.py::TestDistCleanliness | No binary release artifacts tracked in git | PASS | 1 test |
| Release notes coverage (new) | tests/test_release_hygiene.py::TestReleaseNotesCoverage | Current version + every CHANGELOG entry has release notes | PASS | 2 tests |
| CI catalog drift check | .github/workflows/ci.yml "Rebuild catalog and check for drift" | Regenerating catalog produces no diff | EXPECTED_PASS | runs in CI |
| Release `/release-engineer` gate | .github/workflows/release.yml (modified) | Release fails if no docs/releases/v{tag}-release-notes.md present | ENFORCED | uncommitted session change |

## Summary
- 98/98 pytest tests pass locally
- 3 new test files, 14 new tests added
- 1 CI step already enforces catalog drift detection (catalog-generate.py --check)
- Release workflow now gates on `/release-engineer` notes file presence

## Gates that will block future regressions
1. Plugin version drift → canonical consistency test
2. Headline count drift (skills / agents / calcs / orchs / workflows / refs) → canonical consistency test
3. Catalog source_paths pointing to missing files → canonical consistency test
4. Orchestrator handoff referencing non-existent config → orchestrator integrity test
5. Orchestrator config referencing non-existent skill → orchestrator integrity test
6. Binary artifact accidentally committed to dist/ → release hygiene test
7. Tagged version without release notes → release hygiene test AND release.yml gate
