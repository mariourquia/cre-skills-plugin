# Migration Guide: v3.0.0 -> v4.0.0

## Breaking Changes

### 1. Feedback default mode changed

**Before:** `feedback.mode` defaulted to `ask_each_time` with a pre-configured backend URL.
**After:** `feedback.mode` defaults to `local_only` with an empty backend URL.

**Impact:** Existing installs that relied on the default `ask_each_time` behavior will stop prompting for remote submission. Users who want remote submission must explicitly configure it.

**Action:** If you want remote feedback submission:
```json
{
  "feedback": {
    "mode": "ask_each_time",
    "backend_url": "https://cre-skills-feedback-api.vercel.app/api/feedback"
  }
}
```

### 2. registry.yaml is now generated

**Before:** `registry.yaml` was manually maintained.
**After:** `registry.yaml` is generated from `src/catalog/catalog.yaml` by `scripts/catalog-generate.py`.

**Impact:** Manual edits to registry.yaml will be overwritten on next generation run.

**Action:** Edit `src/catalog/catalog.yaml` instead. Run `python scripts/catalog-generate.py` to propagate changes.

### 3. Router reads catalog instead of markdown

**Before:** `src/routing/skill-dispatcher.mjs` parsed `src/routing/CRE-ROUTING.md` markdown tables.
**After:** Router reads `dist/catalog.json` (with markdown fallback if catalog is missing).

**Impact:** The router now supports artifact-aware routing (`--artifact`), hidden item filtering (`--include-hidden`), and structured recommendations with downstream skill suggestions.

**Action:** No action needed. The CLI interface is backward compatible. The `--list` flag still works.

### 4. Plugin version bumped to 4.0.0

**Action:** Update any version checks or references.

## New Files

| File | Purpose |
|------|---------|
| `src/catalog/catalog.schema.json` | JSON Schema for catalog items |
| `src/catalog/catalog.yaml` | Canonical source of truth for all metadata |
| `dist/catalog.json` | Generated JSON catalog for runtime use |
| `scripts/catalog-build.py` | Build catalog from repo structure |
| `scripts/catalog-generate.py` | Generate public surfaces from catalog |
| `src/templates/output-styles/*.md` | Output format templates (exec-brief, ic-memo, pm-action-list, lender-brief, lp-update) |
| `docs/adr/0001-catalog-source-of-truth.md` | Architecture decision record |
| `docs/MIGRATION.md` | This file |
| `docs/release-checklist.md` | Release checklist for maintainers |

## Removed / Deprecated

| Item | Status |
|------|--------|
| Hardcoded counts in README, plugin.json, hooks.json | Replaced by catalog-generated values |
| Manual registry.yaml editing | Replaced by catalog.yaml -> generate workflow |
| `feedback.mode: ask_each_time` as default | Changed to `local_only` |

## Verification

After upgrading:
1. Run `python scripts/catalog-build.py --validate` to verify catalog integrity
2. Run `python scripts/catalog-generate.py --check` to verify all surfaces are up to date
3. Run `node src/routing/skill-dispatcher.mjs --list` to verify router loads catalog
4. Run `pytest tests/` to verify structural integrity
