# ADR 0002: Document-to-Database Ingestion

**Status:** Accepted
**Date:** 2026-05-31
**Decision makers:** Mario Urquia

## Context

The plugin already had a prose skill chain for turning a deal's documents into structured, source-cited data: a data-room extractor, a warehouse-conventions reference, and the rent-roll and T-12 prose skills. That chain GUIDES Claude — it tells the model how to extract, classify, and cite — but the numeric work (decomposing a rent roll into a typed charge schedule, mapping charges to accounts, validating arithmetic, grading data quality, reconciling the rent roll to the T-12) was being done by the model inline, with no reproducible, auditable floor beneath it.

For an institutional CRE audience the gap matters. A reconciliation an IC can challenge has to be deterministic: the same inputs must produce the same numbers, the basis of every comparison must be stated, and a variance must be a classified finding rather than a forced tie. The same is true of the data-quality grade that gates a load and of the PII boundary that protects per-unit tenant identity.

At the same time, the plugin already maintains canonical sources of truth for the chart of accounts (the residential-multifamily GL crosswalk and GL schema), for rent-roll data quality (the `data-quality-rubric.yaml`), and for the PII boundary (the data-room extractor's `pii-redaction-policy.yaml`). Building a second copy of any of these inside a calculator layer would reintroduce exactly the drift ADR-0001 eliminated for catalog metadata.

We also need to be honest about the target: the calculators describe a TARGET WAREHOUSE schema for a downstream pipeline to implement, but the amos-prototype runtime that this work feeds uses a deliberately flatter, foreign-key-free, session-scoped staging schema (its Neon HTTP driver runs one statement per round-trip). The two are not the same and should not be conflated.

## Decision

Introduce an **executable, stdlib-only calculator layer beneath the prose document-to-warehouse skills.** The prose skills continue to guide; the calculators run deterministically and produce the numbers the prose layer cites. The two layers are paired, not redundant: each prose skill names its backing calculators, and each calculator names the skill it serves.

Specific decisions:

**(a) Calculators sit beneath prose, not beside it.** The document-to-database family of prose skills (`rent-roll-to-database`, `t12-to-database` / `operating-statement-to-database`, `rent-roll-t12-tieout`, and the `document-to-database` orchestration) is the guidance layer. Beneath it, a set of pure functions (`normalize_tokens`, `map_charge_codes`, `validate_payload`, `grade_ingestion`, `reconcile_rent_roll_t12`, `map_to_target_model`, `emit_sql_ddl`, `emit_load_plan`, and the shared `ingest/` helpers) does the deterministic numeric work. A skill is not a black box: it can show exactly how each number was produced.

**(b) Reuse, do not fork, the canonical sources of truth.** The calculator layer mirrors — and never re-authors — the existing sources of truth:
- the canonical chart of accounts mirrors the residential-multifamily GL crosswalk and GL schema;
- the data-quality grade mirrors the rent-roll `data-quality-rubric.yaml` (its dimensions, weights, weakest-link semantics, and A/B/C verdict);
- the PII boundary mirrors the data-room extractor's `pii-redaction-policy.yaml` (the never-emit set and the hard-stop semantics).
Parity is enforced by a **sync test** that loads each YAML and fails if the calculator constants drift from it. This keeps the single-source-of-truth posture of ADR-0001 while letting the calculators stay dependency-free.

**(c) Provenance is a strict superset of the warehouse contract.** Every emitted record carries the existing eight-column warehouse provenance contract (`source_doc, locator, source_ref, extracted_by, classification, confidence, review_status, extracted_at`) with the same allowed values and the same canonical `data-room/<doc>#<anchor>` join key — and adds the granular locator components (page / section / table / row / column / cell), the run/skill/parser identity, the tenancy label, and two governance fields (`pii_class`, `redaction_status`). Because it is a superset, the new layer joins cleanly with the existing prose chain; assembly never upgrades a classification.

**(d) PII boundary: pseudonymized trust tier, locator-not-value.** Unit and tenant grain is preserved, but natural-person identity is not. Tenant identity is pseudonymized (a salted token); for any PII-classified field the cell address (locator) is kept and the value is never stored, while a verbatim source span is retained only for aggregate-safe (non-PII) fields. A detected redaction breach is a **non-overridable critical gate**: it cannot be bought back by a high numeric score, and it halts delivery rather than emitting a partially redacted payload.

**(e) Determinism / ZDR.** The calculators are pure: stdlib only, no network, stdout-only output, and **no wall clock** — `as_of` is injected by the caller and flows unchanged into `created_at` / `updated_at`. The only field that legitimately varies a record's identity between runs is `run_id`, and tests assert that two runs differing only in `run_id` differ only in run-id-bearing fields. This makes the layer reproducible and zero-data-retention friendly.

**(f) Five target-model profiles.** Target-model emission is driven by five declarative profiles — `raw_landing`, `normalized_relational`, `star_schema`, `data_vault`, and a `hybrid_recommended` composition — each a table catalog (grain, primary key, typed columns, foreign keys, load order) consumed by `map_to_target_model`, `emit_sql_ddl`, and `emit_load_plan`. These describe a target warehouse, not the prototype runtime.

**(g) The rent-roll ↔ T-12 tie-out never forces a tie.** Reconciliation is on a stated, consistent basis (annualized contractual vs recognized accrual; collected cash out of scope). `tie_status` is only `tied | untied`; nothing adjusts a value to make a dimension tie; every untied dimension surfaces `residual_unexplained == |variance|` and routes to human review. Differences are classified mapping / timing / missing on a deterministic signature keyed on whether the EGI total reconciles. See ADR detail in `src/skills/rent-roll-t12-tieout/references/tie-out-methodology.md`.

## Consequences

### Positive

- Every number the prose layer cites is reproducible from its inputs; an IC can be shown the derivation, not asked to trust it.
- The chart of accounts, the data-quality rubric, and the PII policy each remain a single source of truth; the sync test makes drift a test failure rather than a latent inconsistency.
- The provenance superset means the new records join the existing data-room chain and the AMOS source manifest without a translation step.
- The PII boundary is enforced in code with the same hard-stop a human would apply, and a breach cannot be overridden by a good score.
- Reproducibility and the no-wall-clock rule make the layer safe to run in a zero-data-retention posture.
- A target warehouse can be emitted in whichever of the five shapes a consumer needs, from raw audit landing through enterprise data-vault lineage.

### Negative

- The calculator surface grows the plugin's calculator inventory, which is now another set of artifacts the catalog must track and keep in parity (a cost ADR-0001's generated-catalog approach already absorbs, but a cost nonetheless).
- Parity between the calculators and the YAML sources of truth must be actively maintained; the sync test catches drift, but a source-of-truth change now requires a coordinated update on both sides.
- The five target-model profiles describe a target warehouse that is intentionally **richer** than what the amos-prototype runtime uses: the AMOS staging tables are a flatter, foreign-key-free, session-scoped subset (the Neon HTTP driver runs one statement per round-trip and the house schema carries no foreign keys). The two schemas are deliberately different, and anyone wiring the calculators to the prototype must map down from the profile to the flat staging shape rather than assuming they match.
- Staying stdlib-only means the calculators re-implement small amounts of parsing and tolerance logic that a library would otherwise provide, in exchange for zero dependencies and deterministic output.
