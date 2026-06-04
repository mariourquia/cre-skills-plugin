# TASK_STATE — v5.0.0 Release Readiness

- **Branch:** `release/v5-skill-modernization`
- **Release target:** `v5.0.0` (single consolidating release)
- **Current phase:** version bump + regeneration + release-notes authoring complete; full validation gate passed
- **Overall status:** ready for commit / PR / merge / tag decision (orchestrator owns commit + tag)
- **Last updated:** 2026-06-03

## Context

Source was version-stamped to 4.4.0 then 4.5.0, but **neither tag was ever cut** —
the last published git tag is `v4.3.0`. v5.0.0 consolidates both never-tagged
releases (v4.4.0 document→warehouse→deck chain; v4.5.0 document-to-database
ingestion family + the orchestrator-engine work) plus the v5 trust-hardening and
micro-skill governance architecture into one honest tagged release.

The v4.4.0 and v4.5.0 release-note files **stay `status: pending`** (no tag ever
existed for either); they are narrated inside `docs/releases/v5.0.0-release-notes.md`.

## Baseline

- Last published tag: `v4.3.0`
- Catalog counts (unchanged from 4.5.0 source): **127 skills | 54 agents | 21 MCP tools | 10 orchestrators | 6 workflow chains** | 279 reference files
- Zero new stub skills added in the v5 modernization

## Version / parity ledger

| Surface | Before | After |
|---|---|---|
| `.claude-plugin/plugin.json#version` | 4.5.0 | **5.0.0** |
| `.claude-plugin/marketplace.json` plugin version | 4.5.0 | **5.0.0** |
| `src/catalog/catalog.yaml#plugin_version` (regenerated) | 4.5.0 | **5.0.0** |
| `src/hooks/telemetry-init.mjs` default-config version | 4.5.0 | **5.0.0** |
| `Install.command` const + banner + fallback | 4.5.0 | **5.0.0** |
| `scripts/Install.ps1` const + banner + fallback | 4.5.0 | **5.0.0** |
| `scripts/install.sh` header + banner + fallback + success | 4.5.0 | **5.0.0** |
| `PRIVACY.md` banner | 4.5.0 | **5.0.0** |
| `docs/install-guide.md` Version line | 4.5.0 | **5.0.0** |
| `docs/INSTALL.md` / `docs/install-desktop.md` DMG/EXE filenames | 4.5.0 | **5.0.0** |
| `docs/integrations/amos-skill-manifest.sample.json` plugin_version | 4.5.0 | **5.0.0** |

`src/mcp-server.mjs` reads its version dynamically from plugin.json — no edit
needed. Installer skill/agent/MCP COUNTS were already corrected to 127/54/21 in a
prior v5 commit; only version strings changed in this pass.

## What shipped in v5.0.0

1. **Trust hardening (WS-1a/WS-1b/WS-2).** OZ / cost-seg / climate corrected to
   current law (OBBBA + IFRS S2/ISSB); calculator typed-refusal envelope +
   waterfall catch-up fix; privacy feedback-default reconciled to the true
   `ask_each_time`; installer/doc count corrections.
2. **v5 micro-skill architecture (C-1/C-2/C-3/C-4).** Classification taxonomy +
   governance metadata + jsonschema validator; v5 skill contract standard; AMOS
   skill-manifest export; 8 mega-skills reclassified; DATA_GRADES + connector
   capability matrix + known-limitations docs.
3. **Consolidated v4.4.0 + v4.5.0** (chain + ingestion family + orchestrator engine).

## Validation ledger (captured 2026-06-03, post-bump)

- `python3 scripts/version_check.py` → **PASS** (expected 5.0.0; all 3 installer fallbacks 5.0.0)
- `python3 -m pytest tests/ -q` → **413 passed, 12 skipped, 9 xfailed, 32 subtests passed**
  - skips = build artifacts not present locally (portable/cowork ZIP); xfails = pre-existing documented install_smoke gaps
- `python3 scripts/catalog-generate.py --check` → **zero drift** (README, hooks.json, plugin.json, CRE-ROUTING.md, registry.yaml all ok)
- `bash scripts/validate-marketplace.sh` → **all checks passed** (version consistency marketplace=5.0.0, plugin=5.0.0)
- `python3 scripts/registry-validator.py` → **8/8 categories clean, STATUS PASS**

### Validator note (no test weakened)

`scripts/registry-validator.py` had two pre-existing false positives on this
branch, both fixed without masking real drift:

- The legacy-plan-doc release check now **skips git-ignored files**. `docs/plans/`
  is git-ignored (local-only design docs per `.gitignore`); those working files
  would never ship and do not exist in a fresh CI checkout. A non-ignored plan doc
  is still flagged (fail-closed if git is unavailable).
- `docs/known-limitations.md` added to the prior-version exempt list for its RMF
  `v1.0.0-rc1` reference + the v4.5.0→v5.0.0 migration pointer — the identical
  pattern already applied to `README.md` and `docs/ROADMAP.md`.

## Out of scope this pass (orchestrator / later)

- No git / tag / push / release (orchestrator commits and tags).
- No `build.sh` / `builds/` regeneration (later packaging step; `builds/` is gitignored).
- Windows `.exe` is CI/Windows-only (not locally buildable on macOS).

## Deferred to v5.1 (tracked in docs/ROADMAP.md)

Full 127-skill v5-contract conformance sweep; the four canonical connector
contract schemas (`debt`, `entity`, `valuation`, `funds` promotion) with
enforced `source_class` + `max_staleness`; the generalized cross-skill governance
scanner; and the first valuation + investor-reporting connectors.

## Final readiness

- **Go / no-go:** GO. Version SoT bumped, surfaces regenerated with zero drift,
  release notes authored (`status: pending` pre-tag), CHANGELOG + ROADMAP +
  TASK_STATE updated, all validators + the full test suite green.
- **Post-tag follow-up:** after `release.yml` publishes, flip
  `docs/releases/v5.0.0-release-notes.md` frontmatter `status: pending` →
  `status: released`. Leave the v4.4.0 / v4.5.0 notes at `status: pending`
  (no tag exists for either).
