# Install Smoke-Test Matrix

This matrix lists every advertised install surface, the repeatable smoke test that covers it, and the scenarios that are **not** currently tested. Published alongside the internal-beta release so downstream users know what has been proven vs what has only been wired up.

Surfaces without a green cell for a given scenario must be exercised by a human (or avoided) until an automated test lands. New releases do not block on every cell turning green, but every regression of a green cell blocks the release.

## Matrix

Legend:
- **covered** = there is an automated smoke test or CI check that exercises this scenario and currently passes on `main`.
- **manual** = humans exercise this surface before each release; no automation yet.
- **gap** = the scenario is advertised but unexercised. File an issue before relying on it.

| Surface | Fresh install | Upgrade | Uninstall / reinstall | Corrupted-config recovery | Missing prereqs detected | Platform notes |
|---|---|---|---|---|---|---|
| **Claude Code marketplace (CLI)** | covered — `scripts/verify-install.sh`, `tests/test_plugin_integrity.py` | manual | manual | gap | partial (Node 18+ warning only) | relies on `claude plugin install` — the Claude Desktop "Add marketplace" dialog is intentionally not supported |
| **macOS DMG (`Install.command`)** | covered — `scripts/installer_smoke_test.py` | manual | manual | gap | partial (detects BOM via `utf-8-sig`; no remediation) | code-signed via Developer ID |
| **Windows EXE (`Install.ps1`)** | covered — `tests/test_installer_hardening.py` (BOM, argv, hooks scope) + `scripts/installer_smoke_test.py` | manual | manual | gap | gap (PowerShell logs versions but does not halt on missing Node/Python/npm) | defends against PowerShell 5.1 UTF-8 BOM footgun |
| **Cowork ZIP import** | manual | manual | manual | manual | n/a | ships `dist/cre-skills-cowork.zip` with skills + agents + commands only (no hooks, MCP, orchestrators, calculators); no automated Cowork simulator in the suite |
| **Manual MCP config (Claude Desktop Chat tab)** | covered — `test_plugin_integrity.py::TestMcpServer` (initialize, tools list, routing) + `node --check` on `mcp-server.mjs` | manual | manual | gap | partial (JSON parse check only) | `claude_desktop_config.json` hand-edit; 19 operational tools + 2 aliases |
| **`install.sh` one-liner** | partial — platform detection + dep checks run but no post-install assertion | gap | gap | gap | partial (checks Python 3, Node 18+, npm, git) | Darwin / Linux / WSL |
| **Local dev via `claude --plugin-dir`** | covered (implicit via `verify-install.sh`) | n/a (just re-pull) | n/a | n/a | n/a | symlink resolution |
| **Portable ZIP for Codex / Gemini / Grok / Manus** | structural — `tests/install_smoke/test_portable_zip.py` + `.github/workflows/portable-zip-smoke.yml` | gap | gap | gap | gap | structural coverage only: ZIP opens, skills tree matches source (minus the portable-excluded `residential_multifamily` subsystem), frontmatter contract is honored, and MCP / orchestrator / Python-calculator runtime files are absent. Cross-runtime invocation (a CLI like Codex / Gemini / Grok / Manus actually loading and running a skill from the extracted ZIP) remains a **gap** until a cross-CLI harness lands — see the Known Gaps section below. |

## Automated tests that back the matrix

- `scripts/verify-install.sh` — post-install checks for Claude Code marketplace installs (plugin registered, SKILL.md files present, reference files non-empty, Python calculators parse, `hooks.json` valid, Node hook scripts parse, `~/.cre-skills/` writable, `config.json` valid if present).
- `scripts/installer_smoke_test.py` — post-install checks for Claude Desktop (DMG + EXE): plugin cache, `installed_plugins.json`, `settings.json` `enabledPlugins` key, `claude_desktop_config.json` `mcpServers` key, `mcp-server.mjs` passes `node --check`, version consistency source ↔ cache ↔ registry.
- `tests/test_plugin_integrity.py` (root pytest suite) — covers catalog ≟ filesystem, MCP server, hook scripts, calculators, command list.
- `tests/test_installer_hardening.py` — covers PowerShell 5.1 UTF-8 BOM handling, Node `process.argv` indices, `PostToolUse` hook scope.
- `tests/test_release_hygiene.py` — no-binary-artifacts + release-notes coverage.
- `tests/test_e2e_skill_calculator.py` — end-to-end execution of one representative skill + calculator (`deal-quick-screen`).
- `tests/test_orchestrator_integrity.py` — orchestrator JSON schemas load + parse (does **not** exercise orchestrator execution).
- `tests/test_canonical_consistency.py` — catalog matches filesystem.
- `tests/install_smoke/test_portable_zip.py` (+ `.github/workflows/portable-zip-smoke.yml`) — structural smoke on the packaged `dist/cre-skills-portable.zip`: openable, skills tree mirrors `src/skills/` minus the portable-excluded `residential_multifamily` subsystem, each extracted `SKILL.md` carries the portable frontmatter contract (`name` + `description`; `slug` / `status` / `version` are stripped by design), no MCP server, no orchestrator runtime, no Python calculators leaked. Cross-runtime invocation is an explicit xfail until a cross-CLI harness exists.

## Known gaps and proposed next tests

These are intentionally listed as limitations rather than fixed in this pass:

1. **Upgrade smoke test** — install a previous release from `dist/releases/`, run `verify-install.sh`, upgrade to current, re-run `installer_smoke_test.py`, assert `~/.cre-skills/` state preserved. No such test today.
2. **Corrupted-config auto-recovery** — `scripts/diagnostic_report.py` exists but is not triggered on detection. Target: detect malformed `installed_plugins.json` / `claude_desktop_config.json` / BOM-prefixed JSON; back up + rewrite clean; re-run smoke test.
3. **Windows prereq halt** — `Install.ps1` currently logs dependency versions but does not halt with a remediation step when Node/Python/npm are missing from `%PATH%`. Target: add explicit `Fail-If-Missing` with install instructions.
4. **Cowork ZIP schema validator** — `scripts/cowork-schema-validator.py` (proposed). Validates SKILL.md format, agent YAML shape, command markdown for Cowork's stripped field set.
5. **Uninstall smoke test** — verify plugin removed from registry, `claude_desktop_config.json` `mcpServers` entry removed, user data in `~/.cre-skills/` preserved.
6. **Portable-ZIP cross-CLI smoke test** — structural coverage landed in v4.3 (`tests/install_smoke/test_portable_zip.py`), but actually spinning up Codex / Gemini / Grok / Manus in a container and confirming at least one skill loads (or documenting it as unsupported) still requires a cross-CLI harness. Structural ≠ cross-runtime — that gap remains open.
7. **Hook execution smoke test** — spawn `telemetry-init.mjs` via Node; confirm `~/.cre-skills/config.json` created; trigger a Read tool event; confirm `telemetry.jsonl` appended.

Any item in this section is a release caveat, not a blocker — surfaces with open gaps are labeled in [README Release Maturity](../README.md#release-maturity) so users can make an informed choice.
