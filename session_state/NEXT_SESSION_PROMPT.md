# Next Session Handoff

Follow-up items deferred from the 2026-04-15 hardening session. Pick any subset; none are blocking.

## Low-priority cleanup

1. **Consolidate duplicate plugin.json.** Currently `.claude-plugin/plugin.json` and `src/plugin/plugin.json` are kept in sync manually. 10+ scripts read `src/plugin/plugin.json`. Update them to read `.claude-plugin/plugin.json` as the single source, then delete `src/plugin/plugin.json`. Affected scripts: catalog-build.py, catalog-generate.py, install.sh, update.sh, uninstall.sh, verify-install.sh, validate-marketplace.sh, registry-validator.py, version_check.py, tests/test_plugin_integrity.py.

2. **Add MCP tool governance to catalog.** The 21 MCP tools are defined in `src/mcp-server.mjs` but not in `src/catalog/catalog.yaml`. Add a `mcp_tools` section to catalog so that the README claim of 21 MCP tools has a single source of truth.

3. **Tighten hooks.json PostToolUse matcher.** Currently `matcher: "Read"` fires on every Read call. The filter in `telemetry-capture.mjs` handles this correctly, but a more specific matcher (e.g., regex on skills/**/SKILL.md paths) would reduce hook firing noise. Low priority — no correctness bug.

4. **Update release-checklist.md** line 27 (implies manual version bumps in scripts/create-dmg.sh) to reflect that release.yml now injects APP_VERSION via env. Cosmetic doc alignment.

5. **Orchestrator prompt cleanup.** `src/orchestrators/prompts/README.md` documents 8 orphan prompts. Decide per prompt: wire into a config + catalog entry OR delete. Current state is documented-honest but not consolidated.

## Regression-gate follow-ups (if appetite)

6. **End-to-end skill→calculator test.** Current coverage asserts calculator math. Add a test that invokes a skill via the router and confirms it reaches its declared calculator.

7. **Release artifact checksum verification.** After release.yml publishes artifacts, add a post-release job that downloads them, re-computes sha256, and asserts match against published SHA256SUMS.

8. **Network isolation test for local_only mode.** Validate via code inspection or a fake network mock that `feedback_mode: local_only` never calls `fetch` to any remote endpoint.

## Starting position

- Branch: main (after this PR merges)
- Last session PR: [insert after merge]
- Session state: `session_state/` has the full context
- Current version: 4.1.2
- 98 of 98 tests passing (84 original + 14 new regression gates)
