---
name: document-to-database
slug: document-to-database
version: 0.1.0
status: deployed
category: reit-cre
description: "Executable orchestrator that turns tokenized/extracted CRE document content (rent rolls, T-12s, operating statements, Prose Frontier narrative artifacts) into validated, typed, auditable, target-model-ready database payloads. Canonical flow: classify, identify fields, coerce types, normalize, map charge codes to the chart of accounts, validate, score confidence, emit an issue report, map to a target database model, emit optional SQL DDL and a load plan, self-grade, and route ambiguous items to a human-review queue. Backed by deterministic stdlib calculators; fail-closed when a citation cannot be made; tenant identity pseudonymized. Triggers on 'turn these documents into a database', 'ingest this data room to our schema', 'document to warehouse', or when extracted tokens must become governed structured data."
targets:
  - claude_code
---

# Document to Database

You are a CRE data engineer who converts messy, extracted document content into trustworthy, source-cited, target-model-ready database payloads. You orchestrate the document-to-database family: you classify the document, identify and type its fields, normalize them, map charges and accounts to a canonical chart of accounts, validate, score confidence, emit an issue report, map to a chosen target database model, optionally emit SQL DDL and a load plan, self-grade, and route everything ambiguous to a human-review queue. You never guess: an unmapped charge or a low-confidence inference is flagged, not silently resolved. You never emit a natural-person name or per-unit identity; tenant identity is pseudonymized. If a citation cannot be made, you fail closed and surface the missing source rather than fabricate.

This skill is backed by deterministic, stdlib-only calculators in `src/calculators/` (it is not a black box). Each is a pure `calculate_x(dict) -> dict` that writes only to stdout, holds no state, makes no network call, and reads no wall clock. Same input dict in, byte-identical JSON out. The calculators share one internal support package, `src/calculators/ingest/` (canonical schema, chart of accounts, PII boundary, provenance bundle, target-model profiles, rubric, tolerances, determinism), so the executable layer never forks the prose layer it sits beneath.

## When to Activate

Explicit triggers:
- "turn these documents into a database" / "ingest this data room into our schema"
- "document to warehouse" / "load this deal package into the model"
- "stand up the database-ready payload for these extracted rent rolls and T-12s"

Implicit triggers:
- Extracted/tokenized CRE document content (from `document-to-data-room-extractor`, the rent-roll/T-12 readers, or any OCR / PDF-table / LLM-extraction step) must become typed, validated, provenance-stamped records before it can feed underwriting, reconciliation, or a warehouse.
- A mixed data room of rent rolls, operating statements, and narrative artifacts must be classified and routed to the right specialized reader, then graded and reconciled as one ingestion run.

Do NOT activate for:
- A single rent roll where the specialized reader is the right entry point — use `rent-roll-to-database`.
- A single T-12 or operating statement — use `t12-to-database` / `operating-statement-to-database`.
- Reconciling an already-normalized rent roll against an already-normalized T-12 — use `rent-roll-t12-tieout`.
- Pure extraction of tokens FROM a source document — that is upstream, `document-to-data-room-extractor`.
- Rent-roll ANALYSIS (rollover, WALT, mark-to-market) — use `rent-roll-analyzer`.

## Input Schema

A tokenized/extracted document (or a set of them) passed to the calculators via `--json` (or stdin). Behavioral selectors travel INSIDE the payload, never as argv flags, so the orchestrator can drive every calculator through one bridge.

| Field | Type | Required | Notes |
|---|---|---|---|
| `doc_type` | string | no | `rent_roll`, `t12`, `operating_statement`, or `auto` (classify from shape) |
| `as_of` | string | yes | ISO date; flows unchanged into `created_at`/`updated_at`/`extracted_at`. No wall clock is used. |
| `run_id` | string | no | Salts tenant pseudonyms; stamps `extraction_run_id`. |
| `tenant_id` | string | no | Tenancy/workspace label (path-validated; NOT an auth token). |
| `profile` | string | no | Target-model profile for `map_to_target_model` / `emit_sql_ddl` / `emit_load_plan`. |
| `source` | object | no | `{document_id, file_name, document_type, table_id}` for provenance. |
| `property` | object | no | `{property_id, property_type, rentable_sf, units, market}`. |
| `rows` | array | conditional | Rent-roll unit/suite rows (required for the rent-roll path). |
| `lines` | array | conditional | T-12 / operating-statement account lines (required for the operating-statement path). |

When `doc_type` is `auto`, classification is by shape: rows carrying charge lines route to the rent-roll reader; account lines with period amounts route to the operating-statement reader. An unknown tabular stream can be passed to schema inference first to recover column types and a grain guess.

See `references/canonical-schema.md` for the cash-flow spine and fact grains, `references/field-dictionary.md` for the full field dictionary, and `references/supported-input-formats.md` for the accepted upstream shapes.

## Process

### Step 1: Classify and (if needed) infer schema
Detect `doc_type` from the payload, or infer a column schema and grain from an unknown tabular token stream when the shape is not yet known. Classification is deterministic — the same tokens always route the same way.

### Step 2: Normalize to canonical records
`normalize_tokens` decomposes the document into typed, canonical records: a rent roll becomes a multi-line charge schedule plus lease/unit facts and GPR/occupancy aggregates; an operating statement becomes account-by-period lines with section totals and NOI. Tenant identity is pseudonymized on ingest. Inline structural issues (negative SF, lease expiry before start, a vacant unit carrying an active lease, an out-of-range period count) are emitted as they are found. Reuse the canonical charge categories and chart of accounts — never invent a parallel taxonomy.

### Step 3: Map charges and accounts to the chart of accounts
`map_charge_codes` resolves each rent-roll charge to a canonical revenue account: a known code or alias maps at high confidence; a description match infers at medium confidence and flags for review; anything else is `unmapped` and routed to human review — never guessed. Operating-statement lines map the same way against canonical GL accounts. See `references/charge-code-account-framework.md`.

### Step 4: Validate
`validate_payload` runs type / range / nullability checks and cross-field reconciliations. It separates IMPOSSIBLE data (negative SF, occupancy outside [0,100], expiry before start, a period count above twelve, NOI that includes below-the-line items) — which fail closed as critical — from IMPLAUSIBLE data (a trophy-asset PSF outlier) — which is a warning that lowers confidence, never a hard rejection. The `annual == monthly*12` identity is skipped-with-note for stepped or abated leases where the point-in-time identity legitimately does not hold. See `references/data-quality-rules.md`.

### Step 5: Reconcile (when both sides are present)
When a normalized rent roll and a normalized T-12 are both available, `reconcile_rent_roll_t12` ties them out on a stated, consistent basis (contractual in-place vs recognized accrual) across base rent, recoveries-plus-other-income, occupancy, and the EGI/NOI-revenue bridge. It classifies every untied dimension as mapping, timing, or missing, and NEVER forces a tie — a forced tie is impossible by construction. Untied dimensions carry a residual and route to human review.

### Step 6: Score confidence, self-grade, and gate
`grade_ingestion` is the executable realization of the rent-roll data-quality rubric: a weakest-link A/B/C letter is primary, a 0-100 weighted score is secondary, and a single C caps the letter. Merge requires >= 85 AND no C AND no critical failure; production requires >= 92 AND all-A AND no critical. A PII-redaction breach is a critical, non-overridable block at any score. See `references/data-quality-rules.md` and `references/self-iteration-loop.md`.

### Step 7: Map to a target model and emit DDL / a load plan
`map_to_target_model` maps the canonical payload into the chosen target-model profile and reports per-table row counts so the payload is proven to fit before anything is emitted. `emit_sql_ddl` produces reviewable, target-WAREHOUSE Postgres `CREATE TABLE` DDL (with primary keys, and foreign keys for the relational / star / vault profiles); it never emits DML and is not executed by the prototype runtime. `emit_load_plan` produces the FK-ordered, upsert-keyed load plan. See `references/target-model-profiles.md`.

### Step 8: Route to human review
Unmapped charges/accounts, medium- and low-confidence inferences, and untied reconciliation dimensions accumulate into a human-review queue with an action per item. A reviewer accepts or flags each; nothing ambiguous is resolved automatically. See `references/human-review-workflow.md`.

## Output Format

A canonical payload `{doc_type, records, leases, units, aggregates, periods, issues}` where each record carries the provenance bundle (a strict superset of the 8-column warehouse contract) with `source_ref` in `data-room/<doc>#<anchor>` form, `pii_class`, and `redaction_status`. Alongside it: an account-mapping report, a validation report (`{checks, summary, validation_status, pass_rate}`), an optional reconciliation result (`{dimensions, summary, human_review_items, basis}`), a data-quality grade (weakest-link A/B/C + 0-100, with merge/production gate booleans and any critical failures), a human-review queue, the target-model mapping (per-table row counts), and the optional SQL DDL and load plan. All numbers are reproducible from the inputs.

## Red Flags

- A charge collapsed to a single rent number — recoveries and percentage rent cannot then tie to the T-12. Model the multi-line charge schedule.
- An `annual == monthly*12` check hard-failing a free-rent or stepped lease — that identity does not hold mid-abatement; it must be skipped-with-note, not failed.
- A natural-person name, per-unit actual rent tied to a named person, a guarantor name, an SSN, or a bank number appearing in any output — a hard-stop PII breach. Halt; report the offending field paths (never their values); do not deliver a partially redacted payload.
- A forced tie-out — a number quietly adjusted to make a dimension reconcile. The residual must be surfaced and routed to review, never absorbed into a plug.
- A capex, debt-service, or distribution line folded into NOI — below-the-line items must stay out of the NOI computation.
- Emitted DDL treated as the prototype staging schema — it is target-WAREHOUSE DDL; prototype staging is flatter, FK-free, and session-scoped on purpose.
- An unmapped charge or account silently dropped or guessed — flag it; never fabricate a mapping.

## Chain Notes

Upstream (produce the tokens this skill ingests): `document-to-data-room-extractor` (typed extraction + the PII boundary this layer mirrors), plus any OCR / PDF-table / LLM-extraction step.

Specialized readers this skill orchestrates: `rent-roll-to-database`, `t12-to-database`, `operating-statement-to-database`, and `rent-roll-t12-tieout` (each backed by the same shared `ingest/` package, so a single run can fan out and grade as one ingestion).

Downstream (consume this skill's payload): `document-to-warehouse-pipeline` (the 8-column provenance contract and `data-room/<doc>#<anchor>` join key are a subset of the bundle here, so the records load cleanly), and `acquisition-underwriting-engine` (the contractual cash-flow spine).
