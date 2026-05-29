# Document-to-Database Ingestion

The entry point to the document-to-database family: the prose skills that turn a CRE deal's documents into validated, typed, source-cited, database-ready records, and the deterministic calculator layer beneath them. This index is the map; each topic below links to the skill or reference that owns the detail.

The family's posture is set by [ADR-0002: Document-to-Database Ingestion](../adr/0002-document-to-database-ingestion.md): an executable, stdlib-only calculator layer sits *beneath* the prose skills (the prose guides; the calculators run deterministically), it *reuses* the plugin's existing sources of truth rather than forking them, and the rent-roll ↔ T-12 tie-out never forces a tie. The single-source-of-truth principle it builds on is [ADR-0001: Catalog as Single Source of Truth](../adr/0001-catalog-source-of-truth.md).

## The skills

| Skill | Role | Reference detail |
|---|---|---|
| [`rent-roll-to-database`](../../src/skills/rent-roll-to-database/SKILL.md) | Normalizes an extracted rent roll into a typed charge schedule, mapped accounts, aggregates, a data-quality grade, and a load plan. | [rent-roll-field-dictionary.md](../../src/skills/rent-roll-to-database/references/rent-roll-field-dictionary.md) |
| `t12-to-database` / `operating-statement-to-database` | Normalizes an operating statement into account-mapped revenue/expense line items with provenance. (Underwriting restatement: [`t12-normalizer`](../../src/skills/t12-normalizer/SKILL.md).) | [normalization-rules.md](../../src/skills/t12-normalizer/references/normalization-rules.md) |
| [`rent-roll-t12-tieout`](../../src/skills/rent-roll-t12-tieout/SKILL.md) | Reconciles the normalized rent roll against the normalized T-12 on a stated basis; classifies and surfaces every gap; never forces a tie. | [tie-out-methodology.md](../../src/skills/rent-roll-t12-tieout/references/tie-out-methodology.md), [noi-bridge-inputs.md](../../src/skills/rent-roll-t12-tieout/references/noi-bridge-inputs.md) |
| `document-to-database` | Orchestrates the family end to end (extract → normalize → reconcile → grade → emit) and owns the cross-leg human-review queue and target-model emission. | [charge-code-account-framework.md](../../src/skills/document-to-database/references/charge-code-account-framework.md) |

The records this family consumes are produced upstream by the [`document-to-data-room-extractor`](../../src/skills/document-to-data-room-extractor/SKILL.md) and the analysis skills [`rent-roll-analyzer`](../../src/skills/rent-roll-analyzer/SKILL.md) and [`rent-roll-formatter`](../../src/skills/rent-roll-formatter/SKILL.md). The warehouse conventions every record honors live in [`document-to-warehouse-pipeline`](../../src/skills/document-to-warehouse-pipeline/SKILL.md).

## Topics

### 1. Overview
This document. The family takes documents in, emits validated database-ready records out, and keeps every number reproducible and every figure cited. Start here, then follow the link for whichever leg you are working on.

### 2. Supported input formats
The family ingests the tokenized/extracted output of the [`document-to-data-room-extractor`](../../src/skills/document-to-data-room-extractor/SKILL.md) — rent rolls, trailing-12 operating statements, offering memoranda, leases, agency quotes, PCAs, and ALTA/title documents — passed as an input dict, never as argv flags. Each skill states its own expected payload shape in its Input Schema section.

### 3. Canonical schema
The target datasets, their grains, and the warehouse table-naming convention are defined in [warehouse-schema-conventions.md](../../src/skills/document-to-warehouse-pipeline/references/warehouse-schema-conventions.md). Every emitted record carries the canonical provenance bundle described there and in [ADR-0002](../adr/0002-document-to-database-ingestion.md) decision (c) — a strict superset of the eight-column warehouse provenance contract.

### 4. Field dictionary
The canonical rent-roll fields — names, types, nullability, accepted ranges, and the existing-plugin vocabulary each reuses — are in the [rent-roll field dictionary](../../src/skills/rent-roll-to-database/references/rent-roll-field-dictionary.md). It deliberately reuses the extractor's taxonomy and the CAM recovery-terms schema so the executable layer never forks the prose layer.

### 5. CRE data types
The family models a rent roll as a contract- and charge-level cash-flow source (not a single rent number) and a T-12 as an account-level statement. The typed charge categories (base rent, recoveries, parking, storage, percentage rent, …) and lease/unit/space facts are enumerated in the [field dictionary](../../src/skills/rent-roll-to-database/references/rent-roll-field-dictionary.md).

### 6. Nullability
Which fields are required and which may be absent is specified per field in the [field dictionary](../../src/skills/rent-roll-to-database/references/rent-roll-field-dictionary.md) (the *Nullable* column). The schema distinguishes a legitimately empty field from a missing-and-required one; the latter lowers the data-quality grade.

### 7. Accepted ranges
Range and format constraints (non-negative SF, occupancy in `[0, 100]`, ISO dates, expiry ≥ start, …) are in the [field dictionary](../../src/skills/rent-roll-to-database/references/rent-roll-field-dictionary.md). Impossible values are critical failures; implausible-but-possible values are warnings that lower confidence, never hard rejections.

### 8. Expected formats
Date, money, and identifier formats are stated alongside each field in the [field dictionary](../../src/skills/rent-roll-to-database/references/rent-roll-field-dictionary.md). The canonical join key back to the data room — `data-room/<doc>#<anchor>` — is defined in [warehouse-schema-conventions.md](../../src/skills/document-to-warehouse-pipeline/references/warehouse-schema-conventions.md).

### 9. Data-quality rules
The validation rules (arithmetic identities, PSF/per-unit reconciliation, date consistency, vacancy contradictions) are summarized in the [field dictionary](../../src/skills/rent-roll-to-database/references/rent-roll-field-dictionary.md) and detailed in [data-quality-rules.md](../../src/skills/document-to-database/references/data-quality-rules.md). The grade itself mirrors the rent-roll [`data-quality-rubric.yaml`](../../src/skills/rent-roll-analyzer/references/data-quality-rubric.yaml) — same dimensions, weights, and weakest-link A/B/C verdict (see [ADR-0002](../adr/0002-document-to-database-ingestion.md) decision (b)).

### 10. Charge-code / account framework
How raw charge codes and account names map to the canonical chart of accounts — and how unknown codes are inferred at medium confidence or routed to review (never guessed) — is in the [charge-code / account framework](../../src/skills/document-to-database/references/charge-code-account-framework.md). The chart of accounts mirrors the residential-multifamily GL crosswalk and schema rather than forking a second one.

### 11. The rent-roll skill
[`rent-roll-to-database`](../../src/skills/rent-roll-to-database/SKILL.md) turns extracted rent-roll tokens into a multi-line charge schedule, lease and unit facts, GPR and occupancy aggregates, a grade, and a load plan. It models the charge grain because that is what lets contractual charges tie to T-12 actuals downstream.

### 12. The T-12 / operating-statement skill
`t12-to-database` / `operating-statement-to-database` normalizes an operating statement into account-mapped, provenance-bearing revenue and expense line items. For the acquisition-underwriting *restatement* (one-time removals, market re-pricing, reassessment, gross-up), see [`t12-normalizer`](../../src/skills/t12-normalizer/SKILL.md) and its [normalization rules](../../src/skills/t12-normalizer/references/normalization-rules.md).

### 13. The rent-roll ↔ T-12 tie-out
[`rent-roll-t12-tieout`](../../src/skills/rent-roll-t12-tieout/SKILL.md) reconciles the two normalized payloads on a stated, consistent basis and **never forces a tie**. The basis, the dimension-specific tolerances, and the deterministic mapping/timing/missing decision tree are in [tie-out-methodology.md](../../src/skills/rent-roll-t12-tieout/references/tie-out-methodology.md); how the reconciled revenue feeds an NOI bridge is in [noi-bridge-inputs.md](../../src/skills/rent-roll-t12-tieout/references/noi-bridge-inputs.md).

### 14. Target database model adapters
Target-model emission is driven by declarative profiles — raw landing, normalized relational, star schema, data vault, and a recommended hybrid composition — each a table catalog (grain, primary key, typed columns, foreign keys, load order). They describe a target warehouse and are owned by the [`document-to-database`](../../src/skills/document-to-database/SKILL.md) orchestration; see [ADR-0002](../adr/0002-document-to-database-ingestion.md) decision (f).

### 15. AMOS integration
The amos-prototype repo consumes this family's records into its session-scoped staging tables. Those staging tables are a deliberately flatter, foreign-key-free subset of the target-model profiles (the prototype's serverless Postgres driver runs one statement per round-trip and the house schema carries no foreign keys), so a consumer maps *down* from a profile to the flat staging shape. The integration and its schema live in the **amos-prototype** repo, not here; see [ADR-0002](../adr/0002-document-to-database-ingestion.md) decision (f) and its Consequences for the boundary.

### 16. Prose Frontier integration
The Prose Frontier IC surface consumes the reconciled, governed figures this family produces (the rent-roll charge schedule, the tie-out's EGI bridge and residuals) as source-cited inputs to its model room and memo, honoring the same `data-room/<doc>#<anchor>` provenance join key. As with AMOS, the Prose Frontier surface itself lives in the consuming product repo; this family supplies the governed records it reads.

### 17. Human-review workflow
Nothing uncertain is closed silently. Unmapped charge codes, low-confidence inferences, validation warnings, and — critically — every untied tie-out dimension (with its `residual_unexplained` and difference type) are appended to a human-review queue owned by the [`document-to-database`](../../src/skills/document-to-database/SKILL.md) orchestration. The tie-out's contribution to that queue is described in [tie-out-methodology.md](../../src/skills/rent-roll-t12-tieout/references/tie-out-methodology.md).

### 18. Self-iteration loop
A run grades itself against the [data-quality rubric](../../src/skills/rent-roll-analyzer/references/data-quality-rubric.yaml): the weakest-link letter grade is primary and a single failing dimension caps the grade, with a numeric readout as a secondary signal. A grade below the merge gate, or any critical failure, sends the run back for correction rather than forward to load. The loop is deterministic, so the same inputs always yield the same verdict.

### 19. Security / governance
Tenant and unit grain is preserved but natural-person identity is not: identities are pseudonymized, the cell *address* (locator) is kept for PII fields while the value is never stored, and a verbatim source span is retained only for aggregate-safe fields. A redaction breach is a non-overridable critical gate that halts delivery. The boundary mirrors the data-room extractor's [`pii-redaction-policy.yaml`](../../src/skills/document-to-data-room-extractor/references/pii-redaction-policy.yaml); see [ADR-0002](../adr/0002-document-to-database-ingestion.md) decisions (d) and (e). The calculators are pure — stdlib only, no network, stdout-only, and no wall clock (`as_of` is injected) — which makes the family reproducible and zero-data-retention friendly.

### 20. Known limitations
- Billed-vs-collected cash is out of scope — there is no AR feed, so the rent roll is annualized *contractual* income and the tie-out's collected-cash basis is explicitly not available.
- Recoveries and other income are reconciled *jointly* (the canonical chart combines them), with the rent-roll-side breakdown reported rather than independently tied.
- Occupancy is one-sided and not reconciled when the T-12 carries no occupancy metric.
- Percentage-rent breakpoints, co-tenancy / kick-out flags, prepaid rent, and security-deposit-applied-to-rent are carried where present but are documented timing/contingency blind spots. The per-skill limitations are listed in each skill's reference (for example, the [field dictionary](../../src/skills/rent-roll-to-database/references/rent-roll-field-dictionary.md)).
