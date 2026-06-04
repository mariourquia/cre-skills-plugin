# Data Grades — Canonical Taxonomy and Crosswalk

> Status: released (v5.0.0)
> Owner: Mario Urquia
> Last reviewed: 2026-06-03
> Source-of-truth code this doc describes:
> - `src/skills/residential_multifamily/_core/executive_output_contract.md` (RMF executive source-class tags)
> - `src/skills/residential_multifamily/_core/runtime/fallback_resolver.py` (the `overlay:fallback` class)
> - `src/calculators/ingest/provenance.py` (the ingestion `classification` enum)
> - `docs/connectors/CAPABILITY-MATRIX.md` (the connector `source_class` vocabulary, v5.1)
> - `CONTRIBUTING.md` (the v5 skill standard — `## Refusal Behavior` / `## Confidence and Provenance`)

This is the **single canonical data-grade ladder** for the plugin. Before v5 the
words *sample / starter / illustrative / placeholder / overlay / decision-grade /
advisory* were scattered across the CHANGELOG, README, `ASSUMPTIONS.md`,
`PREVIEW_MODE.md`, and per-subsystem prose, and an enterprise reviewer could not
answer "is this output safe to act on?" from one place. This document fixes that.
It does **not** introduce a fifth source-class enum; it **reconciles** the four
vocabularies that are already deployed into one ladder, and states which grades
may back a decision-grade (final-marked) output and which must refuse.

The new v5 frontmatter fields `confidence_default` and `source_ref_policy`
reference this ladder. The skill-body sections `## Refusal Behavior` and
`## Confidence and Provenance` (CONTRIBUTING.md, v5 skill standard) cite it.

---

## 1. The canonical ladder (six grades)

Ordered from least to most trustworthy. Each grade names what it is, where it
lives in the repo today, the banner/label it should carry, and the **"safe to act
on?"** verdict.

| Grade | What it is | Where it lives today | Banner / label | Safe to act on? |
|-------|-----------|----------------------|----------------|-----------------|
| **sample** | Synthetic, clearly-fictional fixtures committed to the repo for illustration and tests | `examples/`, ingestion test payloads, fixtures | example `status: sample`; ingestion uses fictional fixtures only | **No.** Illustration only. |
| **starter** | Placeholder curves, thresholds, and org-overlay defaults shipped for *shape*, not truth | `residential_multifamily/**` reference files, `ASSUMPTIONS.md` | `status: starter` / `illustrative` / `placeholder` | **No.** Must be replaced by an org overlay. |
| **overlay** | Operator-supplied real thresholds / curves / approvers from the tailoring interview, or an org/market/loan overlay applied at runtime | produced by `tailoring/` → org overlay; runtime overlays | `[overlay]` source-class tag (RMF today) | **Conditionally** — once validated by the org. |
| **production** | Real deal / property / tenant data the operator chooses to process | never persisted by the plugin; ingestion is in-memory / ZDR | PII fail-closed block; no telemetry/feedback capture | **Operator-owned.** The plugin does not retain it; the operator bears liability for its use. |
| **decision-grade** | Verdict-first, source-class-tagged, refusal-on-missing-input, period-sealed *final* output | **enforced today only in** `residential_multifamily` final-marked workflows; elsewhere it is the *target contract* (the named decision-grade slugs + the finance placeholder guard) | executive output contract; no preview banner once `stable` | **Yes, within `residential_multifamily`** after operator overlay + shakedown. Elsewhere: only when every load-bearing cell is `overlay`/`production`-class and no `placeholder`/`$X` remains. |
| **advisory** | Everything else: methodology output an operator must validate; any `beta_rc` / `experimental` skill | all other top-level skills; any preview-status output | `PREVIEW / STAGING` stamp; advisory; "not legal/tax advice / not an appraisal" where applicable | **No** — screening / advisory only; the operator bears liability. |

**Honest-scope note (v5.0.0):** *decision-grade* enforcement (source-class
tagging, refusal-on-missing-input, period-seal, the placeholder scanner) is fully
implemented inside the `residential_multifamily` subsystem. Across the rest of the
corpus, v5.0.0 ships the `final_marked` selector plus a **targeted** finance
placeholder guard on a named allowlist (see §4); a fully-generalized corpus-wide
runtime data scanner is a **v5.1** item. No skill outside RMF should imply that
decision-grade enforcement is universal.

---

## 2. Crosswalk — reconciling the four deployed vocabularies

Four source-class vocabularies are already in the repo. They were authored
independently for different subsystems. They are **not forked** by this doc; they
map onto the one ladder above. The mapping is intentionally lossy in the safe
direction: when a source vocabulary is coarser than the ladder, the crosswalk
picks the **lower** (less trusting) grade.

| Ladder grade | RMF executive tag (`executive_output_contract.md`) | fallback_resolver class | Ingestion `classification` (`provenance.py`) | Connector `source_class` (v5.1, `CAPABILITY-MATRIX.md`) |
|--------------|----------------------------------------------------|-------------------------|----------------------------------------------|---------------------------------------------------------|
| **sample** | `[placeholder]` (illustrative fixture) | `placeholder` | `requires-review` (until resolved) / sample fixture | `reference_illustrative`, `connector_sample` |
| **starter** | `[placeholder]` / `[benchmark]` (shipped-for-shape) | `placeholder` | `modeled-assumption` (shipped default) | `reference_illustrative` |
| **overlay** | `[overlay]`, `[overlay:fallback]`* | `overlay:fallback`*, operator-applied overlay | (n/a — ingestion does not apply overlays) | `operator_supplied` |
| **production** | `[operator]` | `operator` (raw payload found) | `source-fact` | `document_extracted`, `connector_live`, `operator_supplied` |
| **decision-grade** | `[derived]` over `[operator]`/`[overlay]` inputs, no `[placeholder]` present | resolved `operator` + `[derived]` with no `placeholder` cell | `calculated` derived from `source-fact` inputs | `document_extracted` / `connector_live` / `operator_supplied` only |
| **advisory** | any cell still `[placeholder]`; mixed/uncited | `placeholder` (refuse/escalate path) | `requires-review`, unresolved `modeled-assumption` | `connector_sample`, `reference_illustrative`, `modeled_assumption` |

\* `overlay:fallback` is the RMF runtime's **soft-fallback** class
(`fallback_resolver.py`): a value was supplied by an org/market/loan overlay *as a
documented fallback* when the raw operator payload was absent. It is an `overlay`
grade — **conditionally** trustworthy — and it carries a confidence downgrade and a
`[overlay:fallback]` cell tag per `executive_output_contract.md` rule 2. It is
**never** `production` and **never** silently promoted to decision-grade.

### Reading the source vocabularies

- **RMF executive source-class tags** — `[operator] [derived] [benchmark]
  [overlay] [placeholder]`, applied per numeric cell. A `[placeholder]` cell
  **blocks final submission** (rule 2 of the executive output contract). `[derived]`
  inherits the most-permissive (lowest-trust) upstream class for refusal purposes.
- **fallback_resolver classes** — `operator` (raw payload found),
  `overlay:fallback` (soft fallback applied), `placeholder` (refuse / escalate;
  value is `None`). These are the **runtime** outcomes of resolving a required
  input in RMF.
- **Ingestion `classification`** — `source-fact` (a cited cell from a document),
  `calculated` (derived from cited facts), `modeled-assumption` (assumed, not
  observed), `requires-review` (flagged for a human). Every normalized row carries
  one, alongside the 8-column provenance bundle and a cell-level `source_ref`.
- **Connector `source_class`** (v5.1) — `connector_live`, `document_extracted`,
  `operator_supplied`, `connector_sample`, `reference_illustrative`,
  `modeled_assumption`. This vocabulary is **specified** in the v5 connector
  analysis and the capability matrix; the connector *runtime* that emits it is a
  v5.1 deliverable. No live adapter emits `connector_live` today.

---

## 3. Which grades may back a decision-grade / final-marked output

A **final-marked** output (an IC memo, valuation, LP / investor report, lender
package, or waterfall — anything a board / IC / LP / lender acts on) has a hard
admissibility rule:

**A final-marked output MUST be backed only by `production`, `overlay`, or
`decision-grade` source cells. It MUST refuse (fail closed) if any load-bearing
cell is `sample`, `starter`, or `advisory`, or carries an unresolved
`[placeholder]` / `$X` token.**

| Source grade of a load-bearing cell | Final-marked (IC / LP / lender / board / valuation) | Non-final (advisory / draft) |
|--------------------------------------|------------------------------------------------------|------------------------------|
| `sample` | **Refuse** | Allowed, labeled `illustrative` |
| `starter` | **Refuse** | Allowed, labeled `illustrative`; must be replaced by overlay |
| `overlay` | Allowed **once validated by the org**; `overlay:fallback` downgrades confidence one band and tags the cell | Allowed |
| `production` | **Allowed** | Allowed |
| `decision-grade` | **Allowed** | Allowed |
| `advisory` (uncited / mixed / preview) | **Refuse** | Allowed with the `PREVIEW / STAGING` + advisory stamp |
| any cell still showing `[placeholder]` / `$X` / TBD | **Refuse** (non-overridable on a final path) | Allowed in a draft, tagged `[placeholder]` |

Equivalently, in the deployed vocabularies:

- **Must back a final output:** RMF `[operator]` / validated `[overlay]` /
  `[derived]`-over-clean-inputs; ingestion `source-fact` / `calculated`; connector
  `document_extracted` / `connector_live` / `operator_supplied`.
- **Must refuse a final output:** any RMF `[placeholder]` cell; fallback_resolver
  `placeholder` (a `None` value on a required input); ingestion `requires-review`
  or unresolved `modeled-assumption`; connector `connector_sample` /
  `reference_illustrative` / `modeled_assumption` on a load-bearing figure.
- **`overlay:fallback` is conditional:** permitted on a final path only with the
  documented confidence downgrade and the `[overlay:fallback]` cell tag — never
  silently.

This rule is **enforced at runtime today only inside `residential_multifamily`**
(the executive output contract + `fallback_resolver.py` + the period-seal gate).
Outside RMF, v5.0.0 enforces the *placeholder* leg of this rule on the named
decision-grade slugs via the finance placeholder guard (§4); the remaining legs
are the v5.1 generalized scanner.

---

## 4. The targeted finance placeholder guard (v5.0.0)

`tests/test_finance_placeholder_guard.py` is an honest, **targeted** discipline
check — a presence-of-discipline assertion over a named allowlist, **not** a
runtime scanner. The allowlist is the finance-critical, decision-grade set:

```
acquisition-underwriting-engine, ic-memo-generator, comp-snapshot,
fund-lp-reporting, jv-waterfall-architect, opportunity-zone-underwriter,
cost-segregation-analyzer
```

For each listed skill the guard asserts the SKILL.md body:

1. carries a `## Refusal Behavior` section; and
2. states explicitly that unresolved `$X` / placeholder tokens MUST NOT appear in
   a final-marked output (the cell must resolve to a `production` / `overlay` /
   `decision-grade` value, or the output refuses).

The valuation / comp skills (`comp-snapshot`, `om-reverse-pricing`,
`acquisition-underwriting-engine`) additionally carry the **"estimate, not an
appraisal"** stamp in `## Confidence and Provenance` (or body), per the 2026 case
law distinguishing AI valuation estimates from professional appraisals.

The fully-generalized, corpus-wide runtime data scanner (every cell of every
skill checked at emit time) remains a **v5.1** item. v5.0.0 ships RMF's deployed
runtime enforcement plus this named-allowlist discipline guard, and is honest that
the two together are not yet universal enforcement.

---

## 5. Where this is linked

- `CONTRIBUTING.md` — the v5 skill standard points `## Refusal Behavior` and
  `## Confidence and Provenance` at this ladder.
- `README.md` — the classification-taxonomy paragraph and Known Limitations
  reference the grade vocabulary.
- `docs/connectors/CAPABILITY-MATRIX.md` — the connector `source_class` column of
  the crosswalk (§2) is the v5.1 connector contract this doc reconciles.
- `docs/PREVIEW_MODE.md` — the `advisory` grade's `PREVIEW / STAGING` banner.
