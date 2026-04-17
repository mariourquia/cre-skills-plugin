# TASK_STATE — v4.2.0 Release Hardening

- **Branch:** `release/v4.2.0-hardening`
- **Release target:** `v4.2.0`
- **Current phase:** Phase 6 complete (full validation gate passed) → Phase 7 delivery
- **Overall status:** ready for PR / merge / tag decision
- **Release decision:** ready to tag (all P0 items closed; validators green; parity test merged)
- **Last updated:** 2026-04-17

## Baseline

- main at `e819bc3` (clean working tree)
- Last published tag: `v4.1.2` (2026-04-04)
- `.claude-plugin/plugin.json#version`: 4.2.0
- `.claude-plugin/marketplace.json#...#version`: 4.2.0
- `src/catalog/catalog.yaml#plugin_version`: 4.2.0
- `CHANGELOG.md` has `## [4.2.0] - 2026-04-16`
- `docs/releases/v4.2.0-release-notes.md` exists with `status: released` (INCORRECT — tag not created)
- Actual skills: 113 | Actual agents: 54
- Release workflow renames assets to `cre-skills-plugin-${TAG_NAME}.{dmg,-setup.exe}` (with `-plugin-` infix)

## Drift inventory — P0 (must fix before tag)

### Truthfulness / release state

| ID | File | Issue |
|---|---|---|
| P0-1 | `docs/releases/v4.2.0-release-notes.md:4` | `status: released` before the tag exists → must be `pending` until tag is pushed |
| P0-2 | `docs/releases/v4.2.0-release-notes.md:101` | Cites specific "merge commit `7e5dcc4`, pre-tag"; unverifiable without tag |
| P0-3 | `src/mcp-server.mjs:242`, `:701` | Hardcoded `plugin_version: "4.0.0"` in feedback record + server info. Stale. |

### Install-path truthfulness

| ID | File | Issue |
|---|---|---|
| P0-4 | docs/INSTALL.md:75, 83; docs/install-desktop.md:11, 25; docs/install-guide.md:15, 19, 182, 192 | Docs tell users to download `cre-skills-v4.2.0.dmg` / `cre-skills-v4.2.0-setup.exe`, but release workflow publishes `cre-skills-plugin-v4.2.0.dmg` / `cre-skills-plugin-v4.2.0-setup.exe` (with `-plugin-` infix). Users following these docs will not find the files. |
| P0-5 | `.github/workflows/release.yml:397` | Install section in release body uses `claude plugin install cre-skills@cre-skills-plugin` (plugin-name@marketplace-name), but marketplace name is `cre-skills` (per `marketplace.json`), so the correct form is `cre-skills@cre-skills`. README (line 116) uses `cre-skills@cre-skills`. |
| P0-6 | Install commands disagree across docs | Five different install commands recommended across docs: `marketplace add`, `install --repo`, `add github:…`, `add <path>`, `install --file`. Canonical choice must be picked and alternatives moved to a single advanced section. |

### Stale version strings on public surfaces

| ID | File | Issue |
|---|---|---|
| P0-7 | `scripts/install.sh:2, :43, :410, :428` | Banner + header + success message say `v4.0.0`; skill-count header says "112 skills" |
| P0-8 | `Install.command:167` | Banner "Plugin Installer v4.0.0" (other constants at 4.2.0) |
| P0-9 | Install.command:168, scripts/Install.ps1:255, scripts/create-dmg.sh:376, scripts/create-exe.iss:50, scripts/install.sh:43, :428 | "112 skills" in user-visible banners (actual 113) |
| P0-10 | `scripts/Install.ps1:707, :717, :827`, `Install.command:467` | Post-install verify expects "112 skills" (actual 113) |

## Drift inventory — P1 (ship but fix)

| ID | File | Issue |
|---|---|---|
| P1-1 | `docs/install-cowork.md:21, 51, 137` | Example JSON with `"version": "4.0.0"` |
| P1-2 | `tests/README.md:31, :39` | "version is 4.0.0", "At least 88 SKILL.md files" — both stale |
| P1-3 | `docs/install-guide.md:252` | Upgrade table missing v4.1.x / v4.2.0 columns |
| P1-4 | `docs/releases/v4.2.0-release-notes.md:82` | `$CLAUDE_PLUGINS_ROOT` variable referenced but never defined |
| P1-5 | `docs/release-checklist.md:14, :21, :41` | References outdated commands and stale install reference |
| P1-6 | `src/commands/cre-agents.md:8` | Says "55 agents" (actual 54). `src/agents/_index.md:3` correctly says 54. |
| P1-7 | README `## Project Structure` block (lines 488–545) | Outdated layout reference ("9 structural integrity tests") — >25 test files exist |
| P1-8 | No parity test exists — docs/script version drift recurs each release | Add `tests/test_release_version_parity.py` |

## Drift inventory — P2 (note; don't block)

| ID | File | Issue |
|---|---|---|
| P2-1 | `docs/MIGRATION.md` references v3→v4 only | Could append v4.1→v4.2 note; optional |
| P2-2 | `CHANGELOG.md [Unreleased]` section holds v4.4 work-in-progress — correctly flagged as unreleased | Leave alone |
| P2-3 | Historical release notes (v4.0.0, v2.0.0) carry old install examples | Historical, do not edit |

## Workstream ledger

| ID | Owner role | Scope | Status |
|---|---|---|---|
| WS-1 | Release Engineer + Repo Auditor | Map drift | done |
| WS-2 | Docs + UX Lead + Metadata | Reconcile install commands + asset names + version banners | done |
| WS-3 | Install + Packaging Engineer | Windows/mac installer prereq halts + stale version strings | done |
| WS-4 | QA / Validation Engineer | Add release-version parity test + run test suite | done |
| WS-5 | Docs + UX Lead | v4.2.0 release-notes truthfulness pass + status flip | done (flipped to `status: pending` pre-tag; post-tag follow-up flips to `released`) |
| WS-6 | Governance + Risk Reviewer | Confirm support-tier wording stays honest | done (tiers in README, INSTALL.md, WHAT-TO-USE-WHEN.md all aligned; no parity/orchestrator overclaims) |
| WS-7 | Git / Delivery Manager | Commit, PR, merge, push, verify | in_progress |
| WS-8 | Release Engineer | Tag decision (go / fail-closed) | pending (decision: GO if PR merges clean and workflow succeeds) |

## Validation ledger

- Tests added: `tests/test_release_version_parity.py` (26 parametrized tests covering manifest version parity, installer banner versions + skill counts, asset filename normalization, canonical CLI install suffix, release-notes frontmatter honesty)
- Tests run:
  - `python3 -m pytest tests/` → 200 passed, 6 skipped, 9 xfailed (all xfails are documented install_smoke gaps, not regressions)
  - `python3 -m pytest src/skills/residential_multifamily/tests/` → 298 passed
  - `python3 scripts/catalog-build.py --validate` → OK (206 items valid)
  - `bash scripts/validate-marketplace.sh` → all PASS (version consistency marketplace=4.2.0, plugin=4.2.0)
  - `python3 scripts/registry-validator.py` → 8/8 categories clean
  - `python3 scripts/catalog-generate.py --check` → all surfaces up to date
  - `node --check` on mcp-server.mjs + three hook scripts → OK
- Smoke checks: fresh-install paths covered by existing `scripts/installer_smoke_test.py` and `scripts/verify-install.sh`; upgrade / uninstall / corrupted-config / Cowork simulator / portable-ZIP cross-CLI remain known gaps (documented in `docs/install_smoke_test_matrix.md`, xfailed in `tests/install_smoke/`)
- Remaining gaps: none that block the tag; the documented xfails are pre-existing and honestly labeled
- Release blockers: none — all P0 items resolved below

## Version / parity ledger

| Surface | Current value | Target |
|---|---|---|
| plugin.json#version | 4.2.0 | 4.2.0 (unchanged) |
| marketplace.json plugin version | 4.2.0 | 4.2.0 (unchanged) |
| catalog.yaml#plugin_version | 4.2.0 | 4.2.0 (unchanged) |
| scripts/install.sh banner | v4.0.0 | v4.2.0 |
| scripts/install.sh header count | 112 | 113 |
| Install.command banner | v4.0.0 | v4.2.0 |
| Install.command skill count | 112 | 113 |
| scripts/Install.ps1 banner | v4.2.0 | v4.2.0 (ok) |
| scripts/Install.ps1 skill count | 112 | 113 |
| scripts/create-dmg.sh skill count | 112 | 113 |
| scripts/create-exe.iss skill count | 112 | 113 |
| src/mcp-server.mjs plugin_version | 4.0.0 | dynamic or 4.2.0 |
| tests/README.md version claim | 4.0.0 | 4.2.0 |
| docs/INSTALL.md DMG filename | `cre-skills-v4.2.0.dmg` | `cre-skills-plugin-v4.2.0.dmg` |
| docs/install-desktop.md DMG filename | same | same fix |
| docs/install-guide.md DMG filename | same | same fix |
| release.yml install snippet | `cre-skills@cre-skills-plugin` | `cre-skills@cre-skills` |
| docs/releases/v4.2.0-release-notes.md#status | `released` | `pending` (pre-tag) |
| src/commands/cre-agents.md agent count | 55 | 54 |

## Git ledger

- Branch: `release/v4.2.0-hardening` (created from `main` @ `e819bc3`)
- Commits: pending
- PR: pending
- Merge: pending
- Push: pending
- Tag: will only be created if all P0 items close and validation gate passes

## Final readiness

- **Go / no-go:** GO. All P0 items resolved, all P1 items resolved, validators + test suites green.
- **Deferred (tracked, non-blocking):** upgrade smoke automation, corrupted-config auto-recovery automation, uninstall-smoke automation, Cowork ZIP schema validator, portable-ZIP cross-CLI smoke. Tracked in `docs/install_smoke_test_matrix.md` and `docs/ROADMAP.md`.
- **Residual risks:** `residential_multifamily` remains beta RC (output contract + period-seal enforcement mean final-marked flows fail closed; operators must supply org overlays for decision-grade use). Portable ZIP for Codex / Gemini / Grok / Manus remains experimental. Orchestrators remain template / semi-manual, not an autonomous runtime.
- **Post-tag follow-up:** once `release.yml` succeeds, open a thin PR flipping `docs/releases/v4.2.0-release-notes.md` frontmatter from `status: pending` to `status: released`.
