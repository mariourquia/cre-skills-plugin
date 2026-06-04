# Migration Guide: v4.5.0 -> v5.0.0

> The v3.0.0 -> v4.0.0 guide follows below and is retained for historical
> reference. This section covers the v4.5.0 -> v5.0.0 upgrade.

v5.0.0 is primarily a **metadata + validation + export** release. It is not a
content rewrite and ships **0 new stub skills** — every "candidate micro-skill"
is either an existing skill reclassified or a documented backlog item. Most of the
change is additive and non-breaking. The items below are what an integrator or
operator should know.

## What changed

### 1. Classification taxonomy (additive, non-breaking)

Every catalog item now carries a `classification`
(`micro | normal | orchestrator | workspace | agent | calculator`) and a
`runtime_role`. For the priority/pilot skills these are explicit in SKILL.md
frontmatter; for the rest they are **derived** by `scripts/catalog-build.py`
(zero-edit). The decision-grade and AMOS-facing skills additionally carry
`final_marked`, `human_gate`, `source_ref_policy`, `amos_surface`,
`decomposes_to`, and `composed_from`.

- **Impact:** all new fields are optional with defaults; the catalog schema's
  `additionalProperties:false` was extended, not removed, so existing consumers
  keep working. `dist/catalog.json` now contains the governance keys on every
  item.
- **Action:** none required. If you read `dist/catalog.json`, you may now key on
  `classification` / `decision_grade` / `human_gate`. See
  [architecture/v5-micro-skill-architecture.md](architecture/v5-micro-skill-architecture.md).

### 2. AMOS skill-manifest export (new artifact)

The plugin publishes `dist/amos-skill-manifest.json` — a superset of the catalog
carrying the governance fields plus the `amos_signoff` and `demoStatus`
projections — with a documented contract at
[integrations/amos-skill-manifest.md](integrations/amos-skill-manifest.md) and a
checked-in `dist/amos-skill-manifest.sample.json` excerpt.

- **Impact:** regenerating the catalog (`python3 scripts/catalog-generate.py`)
  now also regenerates the manifest.
- **Action:** none required unless you consume the manifest. It is a **static
  generated artifact with no live coupling** — no skill is marked live-connected.

### 3. Calculator typed-refusal behavior change

Calculators now return a **typed refusal dict** — `{"error": ..., "refused":
true, "code": ...}` — for degenerate / impossible inputs (e.g. negative or zero
NOI, zero property value) instead of returning a wrong-signed or nonsensical
result. This is enforced by `tests/test_calculator_behavior_debt_sizing_refusal.py`.

- **Impact:** if you call a calculator directly and previously assumed it always
  returned a result object, you must now branch on `out.get("refused") is True`.
- **Action:** check for the refusal shape before reading result fields.

### 4. Feedback default-mode clarification (doc correction, no behavior change)

The feedback default is **`ask_each_time`** — the plugin prompts for consent
before each remote send and transmits **nothing** without explicit per-submission
approval. The runtime falls back to `local_only` when no feedback key is present.
Earlier prose in places described the posture loosely; this is the clarified,
accurate statement.

- **Impact:** none — behavior is unchanged from v4.x. `ask_each_time` was, and
  remains, the default.
- **Action:** to suppress all remote sends entirely, set
  `{"feedback": {"mode": "local_only"}}` in `~/.cre-skills/config.json`.

### 5. Connector `source_class` hardening — framed as v5.1

The connector `source_class` provenance field
(`connector_live | document_extracted | operator_supplied | connector_sample |
reference_illustrative | modeled_assumption`) and the `max_staleness`
consume-time refusal are **specified** and crosswalked in
[DATA_GRADES.md](DATA_GRADES.md) §2, but the connector **runtime** that emits and
enforces them — together with the four canonical contract schemas (debt / entity /
valuation / funds) — is a **v5.1** deliverable. **No connector is live in v5.0.0.**

- **Impact:** none today; this is a forward-looking contract. See
  [connectors/CAPABILITY-MATRIX.md](connectors/CAPABILITY-MATRIX.md) for the
  honest per-vendor state.
- **Action:** do not build against a live connector; none exists.

### 6. Regulatory corrections (OZ / cost-seg / climate)

Factual corrections already landed in WS-1a (commit `8b55a75`): the Opportunity
Zone skill models **both** OZ regimes keyed on investment date (pre-2027 OZ 1.0
with the fixed 12/31/2026 inclusion, and the post-2026 permanent OZ 2.0 regime
introduced by OBBBA — rolling 5-year deferral, restored 10% basis step-up, 30%
for rural QOFs, decennial redesignation); `cost-segregation-analyzer` reflects the
OBBBA permanent 100% bonus vs. the TCJA phase-down keyed on placed-in-service
date; climate/regulatory regime references were corrected. These skills carry a
`statute_review` block (re-verified 2026-06-03) and an advisory "not tax/legal
advice" stamp.

- **Impact:** OZ / cost-seg output now depends on a regime / placed-in-service
  date; the skills **refuse** a final recommendation if that date is unspecified.
- **Action:** supply the QOF investment date (OZ) / placed-in-service date
  (cost-seg) for a final-marked result.

## Verification

After upgrading to v5.0.0:

1. `python3 scripts/catalog-build.py --validate` — catalog integrity.
2. `python3 scripts/catalog-generate.py --check` — zero surface drift (README,
   registry, plugin.json, hooks, routing, AMOS manifest).
3. `python3 -m pytest tests/test_skill_classification.py -q` — taxonomy +
   governance rules.
4. `python3 -m pytest tests/test_finance_placeholder_guard.py -q` — the targeted
   finance-placeholder discipline guard.
5. `python3 -m pytest tests/ -q` — full structural suite.

---

# Migration Guide: v3.0.0 -> v4.0.0

## Breaking Changes

### 1. Feedback default mode

**Default:** `feedback.mode` is `ask_each_time` — the plugin prompts for consent before each remote send and sends nothing without explicit per-submission approval.

**Impact:** No remote data is sent without the user's explicit approval on each submission. This is the default in both v3 and v4; no migration action is required.

**Action:** If you want to suppress all remote sends entirely:
```json
{
  "feedback": {
    "mode": "local_only"
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
| Manual `feedback.mode` prompts | Default remains `ask_each_time`; set `local_only` to suppress all remote sends |

## Verification

After upgrading:
1. Run `python scripts/catalog-build.py --validate` to verify catalog integrity
2. Run `python scripts/catalog-generate.py --check` to verify all surfaces are up to date
3. Run `node src/routing/skill-dispatcher.mjs --list` to verify router loads catalog
4. Run `pytest tests/` to verify structural integrity
