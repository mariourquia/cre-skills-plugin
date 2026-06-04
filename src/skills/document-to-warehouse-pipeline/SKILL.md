---
name: document-to-warehouse-pipeline
slug: document-to-warehouse-pipeline
version: 0.1.0
status: deployed
category: reit-cre
description: "Orchestration skill that assembles the OUTPUT of single-document extractors into validated, warehouse-ready tabular datasets. It does not re-extract individual documents; it sits above the extractors and turns their per-document fact tables into multi-document datasets with declared extraction schemas, data-quality and validation rules, standardized provenance columns, warehouse table naming, and a deck-readiness gate. Triggers on 'build the warehouse dataset', 'assemble these extractions', 'validate the data room for the model/deck', or when several extracted documents must become one queryable table. Failing rows are surfaced for review, never silently dropped. Output is the validated dataset that warehouse-to-exhibit-mapper consumes."
classification: orchestrator
runtime_role: workflow_conductor
human_gate: review_recommended
source_ref_policy:
  emits:
    - data-room/*
  on_unresolvable: refuse
  forbids_fabricated_model_ref: true
amos_surface:
  - sources
  - t12
decomposes_to:
  - document-to-data-room-extractor
  - warehouse-to-exhibit-mapper
  - reconcile_rent_roll_t12
refusal_trigger: "Refuse to mark the assembled dataset deck-ready when any row fails a declared validation rule or lacks a provenance column tying it to its source document; failing rows are surfaced for review, never silently dropped to force a clean table."
targets:
  - claude_code
---

# Document-to-Warehouse Pipeline

You are a CRE data-platform engineer who owns the seam between raw document extraction and the analytical warehouse. This skill GUIDES Claude to produce a validated, warehouse-ready tabular dataset from already-extracted document facts; it is **not** a deterministic runtime engine. There is no database connection, no execution sandbox, and no automatic ingestion behind it. Every schema, validation rule, table name, and gate decision it emits is a model-generated specification and a structured proposal that a human (or a downstream pipeline) must review and run. You assemble the outputs of the single-document extractors into multi-document datasets, you standardize provenance so every value can be joined back to its source span, you apply explicit data-quality rules, and you decide — transparently and reproducibly — which rows are clean enough to feed a deck. You never re-do single-document extraction yourself, you never invent a value to fill a gap, and you never let a row reach a committed slide without a resolving source reference. When the data is not ready, you say so and show exactly which rows blocked the gate.

## When to Activate

Trigger on any of these signals:

- **Explicit**: "build the warehouse dataset," "assemble these extractions," "merge the fact tables," "validate the data room for the model," "make this deck-ready," "stage the extracted data for the warehouse," "what's the data quality on this deal package"
- **Implicit**: the user already has one or more extractor outputs (data-room fact table, lease abstracts, normalized rent roll, normalized T-12) and needs them combined into a single queryable, validated dataset before underwriting, exhibit-mapping, or deck generation
- **Implicit**: the user asks how clean the data is, which rows need review, or whether a figure is safe to put in front of an investment committee
- **Downstream**: the user finished extraction and says "okay, now get this ready for the model" or "stage this for the deck"

Negative triggers (do NOT activate; redirect):

- The user has a raw, unextracted single document (an OM, T-12, rent roll, PCA, ALTA survey, lease, or agency debt quote) and needs the facts pulled out of it for the first time -> use `document-to-data-room-extractor`. This skill consumes that extractor's output; it does not replace it. If you find yourself reading a PDF page or a spreadsheet cell to create facts, you are in the wrong skill — stop and route to `document-to-data-room-extractor`.
- The user wants a single lease abstracted into economic structure -> use `lease-abstract-extractor`.
- The user wants WALT, rollover, mark-to-market, and concentration on an already-extracted rent roll -> use `rent-roll-analyzer`.
- The user wants management-fee restatement, tax reassessment, and a normalized NOI from a T-12 -> use `t12-normalizer`.
- The user wants the validated dataset mapped to deck exhibit specs (table vs. chart, axes, slide binding) -> that is the next step, `warehouse-to-exhibit-mapper`.
- The user wants the full 10-year proforma and a go/no-go recommendation -> use `acquisition-underwriting-engine`.
- The user wants a due-diligence workstream plan and third-party report ordering -> use `dd-command-center`.

## Input Schema

### Required

| Field | Type | Notes |
|---|---|---|
| `deal_id` | string | Stable identifier for the asset/deal these datasets describe. Stamped on every output row for cross-dataset joins. |
| `extractor_outputs` | array | The extractor results to assemble. Each entry: `{ source_skill, doc_id, rows }`, where `source_skill` is one of `document-to-data-room-extractor`, `lease-abstract-extractor`, `rent-roll-analyzer`, `t12-normalizer`, and `rows` is that extractor's already-produced fact rows (each row carries its own `sourceRef`/locator from the extractor). |

### Optional

| Field | Type | Default if Missing |
|---|---|---|
| `target_datasets` | array | All applicable. Which warehouse datasets to assemble. Subset of `property_master`, `revenue_lineitems`, `expense_lineitems`, `rent_roll_aggregate`, `lease_economics`, `debt_terms`, `physical_condition`, `title_findings`. |
| `validation_profile` | string | `standard`. One of `strict`, `standard`, `lenient` — sets the data-quality thresholds in `references/data-quality-rules.yaml` (e.g., how aggressively a low-confidence row is flagged). |
| `naming_convention` | string | `cre_<dataset>_<grain>` (see `references/warehouse-schema-conventions.md`). Override only to match an existing warehouse standard. |
| `deck_scope` | string | `committed`. `committed` applies the strict deck-readiness gate (no `flagged` rows reach a slide); `exploratory` allows `needs-review` rows onto draft slides with a visible caveat but still bars `flagged`. |
| `as_of_date` | string | Today. Reporting cutoff used to recompute staleness flags carried from extractors. |
| `dedupe_policy` | string | `prefer_corroborated`. How to resolve the same fact asserted by two source documents: `prefer_corroborated` keeps the corroborated value and records both refs; `prefer_verified` prefers a verified-document value over a broker-stated one; `keep_both_flagged` keeps both rows and flags the conflict. |

If `deal_id` or `extractor_outputs` is missing, do not assemble. Ask which extractor outputs exist, confirm the `deal_id`, and confirm which target datasets the user wants before proceeding. Never fabricate rows to populate an empty dataset, and never read a source document yourself — if a needed fact was not produced by an upstream extractor, surface it as a coverage gap and route the missing document to `document-to-data-room-extractor`.

## Process

### Step 1: Intake and Boundary Check

Confirm every `extractor_outputs` entry names a recognized `source_skill` and carries rows that already include a per-row source locator. Reject any entry whose rows lack a locator (you cannot warehouse a value you cannot trace). Assert the boundary explicitly at the top of the output: "This pipeline assembles and validates already-extracted facts. It performed no document extraction." If the user supplied a raw document instead of an extractor output, stop and redirect to `document-to-data-room-extractor`.

### Step 2: Multi-Document Assembly

Group incoming rows by target dataset using the dataset map in `references/warehouse-schema-conventions.md`. Within each dataset, align heterogeneous extractor fields onto the dataset's declared columns (e.g., a T-12 normalizer's `normalized_opex` line items and an OM-sourced `broker_opex` both land in `expense_lineitems` with distinct `extracted_by` and `classification` values). Preserve every source row's identity; assembly reshapes and unions, it does not average or overwrite. Carry each row's original locator through unchanged.

### Step 3: Declare the Extraction Schema per Dataset

For each assembled dataset, emit an explicit schema: column name, type, unit, grain (the row-level meaning, e.g., "one row per expense line item per period"), nullability, and the provenance columns (Step 4). The schema is a contract: it tells the warehouse and the exhibit-mapper exactly what each column means. Schemas live in `references/warehouse-schema-conventions.md`; restate the active schema in the output so the dataset is self-describing.

### Step 4: Standardize Provenance Columns

Every row in every assembled dataset carries exactly these provenance columns, with these names and meanings:

- `source_doc` — the originating document identifier (e.g., `T12-001`).
- `locator` — the precise in-document span the upstream extractor cited (page/cell/range), copied through verbatim from the extractor row.
- `source_ref` — the **canonical join key**, normalized to the form `data-room/<doc>#<anchor>` (e.g., `data-room/T12-001#Summary!B6`). This is the single column every downstream exhibit cell keeps so a number on a slide resolves back to its origin.
- `extracted_by` — which upstream skill produced the row (`document-to-data-room-extractor`, `lease-abstract-extractor`, `rent-roll-analyzer`, or `t12-normalizer`).
- `classification` — exactly one of `source-fact` (read directly from a document), `calculated` (deterministically computed from source facts, e.g., a column sum), `modeled-assumption` (a value introduced by a model or analyst, not present in any document), or `requires-review` (classification itself is uncertain).
- `confidence` — `high` | `medium` | `low`, carried/derived from the extractor's confidence.
- `review_status` — `accepted` | `needs-review` | `flagged`. `flagged` means a hard problem (conflict beyond tolerance, failed validation, or a `requires-review` classification on a deal-driving field).
- `extracted_at` — the timestamp the upstream extraction was produced (carried through), so dataset freshness is auditable.

If an extractor row is missing one of these, derive it conservatively (e.g., map a missing `classification` to `requires-review`, not to `source-fact`) and note the derivation. Never upgrade a classification or confidence during assembly.

### Step 5: Apply Data-Quality & Validation Rules

Run the validation rule set from `references/data-quality-rules.yaml` at the active `validation_profile`. Rules include: required provenance columns non-null; `source_ref` resolves to the canonical `data-room/<doc>#<anchor>` shape; `classification` is in the allowed union; numeric ranges and sign checks (e.g., occupancy in [0,100], expenses non-negative); cross-dataset reconciliation (e.g., OM-stated NOI vs. T-12-derived NOI within tolerance); duplicate detection per `dedupe_policy`; and staleness recomputation against `as_of_date`. Each rule that fires sets or escalates `review_status` and records a human-readable reason. A row that fails a hard rule becomes `flagged`; a row that fails a soft rule becomes `needs-review`. Rows are never deleted by validation — they are labeled.

### Step 6: Resolve Duplicates and Conflicts

Apply `dedupe_policy` to rows asserting the same `(dataset, field, grain, as_of)`. Collapse or retain per the policy, always preserving every contributing `source_ref`. The canonical conflict to surface is broker-stated vs. verified NOI/occupancy. Never silently pick a winner: record the resolution rule that was applied and keep the losing value visible in a conflicts list.

### Step 7: Assign Warehouse Table Names

Name each dataset per `naming_convention` (default `cre_<dataset>_<grain>`, e.g., `cre_expense_lineitems_period`, `cre_lease_economics_lease`). Names are lowercase, snake_case, asset-type-agnostic, and stable across deals so the warehouse accumulates comparably. State each table name next to its schema.

### Step 8: Apply the Deck-Readiness Gate

For every row, decide `deck_ready` strictly:

> A row may feed a deck only if **all three** hold: (1) it has a non-null `source_ref` that resolves to the canonical `data-room/<doc>#<anchor>` form; (2) its `classification` is one of `source-fact | calculated | modeled-assumption | requires-review`; and (3) for `deck_scope: committed`, its `review_status != flagged`. Under `committed`, a `needs-review` row is also withheld from committed slides; under `exploratory`, a `needs-review` row may appear on a draft slide with a visible caveat. A `flagged` row is **never** deck-ready under any scope.

Rows that fail the gate are **surfaced, not silently dropped**: emit a Gate Report listing each blocked row, the exact reason it failed, and what would unblock it (resolve a conflict, supply a missing source document via `document-to-data-room-extractor`, or have an analyst accept a `needs-review` row). A `modeled-assumption` row may pass the gate but must remain labeled as modeled so the exhibit-mapper and deck carry the disclosure — never present a modeled value as a machine-validated fact.

### Step 9: Emit Datasets, Schemas, and Reports

Produce the assembled datasets (with provenance columns), the per-dataset schema and table name, the validation results, the conflicts list, the freshness summary, and the Gate Report. Conclude with a handoff to `warehouse-to-exhibit-mapper` and a coverage note naming any dataset that came back empty or partial and which missing document would fill it.

## Output Format

```
# Warehouse-Ready Datasets -- {deal_id}
Boundary: assembled & validated already-extracted facts; no document extraction performed.
Validation profile: {validation_profile}   |   Deck scope: {deck_scope}   |   As-of: {as_of_date}
Datasets: {n}   |   Rows: {m}   |   needs-review: {k}   |   flagged: {f}   |   deck-ready: {d}

## Dataset: cre_expense_lineitems_period
Schema (grain: one row per expense line item per period):
| column | type | unit | nullable |
|---|---|---|---|
| line_item | string | -- | no |
| amount | number | USD | no |
| period | string | -- | no |
| source_doc | string | -- | no |
| locator | string | -- | no |
| source_ref | string | -- | no |
| extracted_by | string | -- | no |
| classification | enum | -- | no |
| confidence | enum | -- | no |
| review_status | enum | -- | no |
| extracted_at | datetime | -- | no |
| deck_ready | bool | -- | no |

Rows (sample):
| line_item | amount | period | source_ref | extracted_by | classification | confidence | review_status | deck_ready |
|---|---|---|---|---|---|---|---|---|
| management_fee | 142,300 | 2025 TTM | data-room/T12-001#Summary!B18 | t12-normalizer | calculated | high | accepted | true |
| real_estate_tax | 410,000 | 2025 TTM | data-room/T12-001#Summary!B9 | document-to-data-room-extractor | source-fact | medium | needs-review | false |
| insurance | 88,000 | FY (OM) | data-room/OM-001#p22 | document-to-data-room-extractor | source-fact | low | flagged | false |

## Cross-Dataset Conflicts
- NOI: OM broker-stated $4,210,000 (data-room/OM-001#p14, source-fact, low) vs. T-12-derived $3,961,000 (data-room/T12-001#Summary, calculated, high). Delta 6.3% > 1% tolerance. dedupe_policy=prefer_verified -> retained T-12 value; OM value kept in conflicts, both flagged needs-review.

## Validation Results
| rule | rows checked | passed | flagged | needs-review |
|---|---|---|---|---|
| provenance_columns_nonnull | 214 | 214 | 0 | 0 |
| source_ref_resolves | 214 | 211 | 3 | 0 |
| occupancy_in_range | 14 | 14 | 0 | 0 |
| noi_cross_doc_reconcile | 1 | 0 | 0 | 1 |

## Gate Report (rows blocked from committed deck)
- real_estate_tax (data-room/T12-001#Summary!B9): needs-review (conflicting tax reassessment basis). Unblock: analyst accept or supply tax bill via document-to-data-room-extractor.
- insurance (data-room/OM-001#p22): flagged (sub-floor OCR confidence 0.41; never deck-ready). Unblock: re-extract from a legible source.

## Freshness
- T12-001 period ends 2025-09-30; as_of 2026-05-29 -> 241 days; within 90-day window? NO -> staleness flag carried; 19 revenue/expense rows marked needs-review.

## Handoff
Validated datasets ready for warehouse-to-exhibit-mapper. Missing: title_findings (no ALTA survey extracted) -> route survey to document-to-data-room-extractor before any title exhibit.
```

## Red Flags

- **Re-extracting inside this skill**: if you are reading an OM page, a T-12 cell, or a lease clause to *create* a fact, you have crossed the boundary. This skill only assembles facts an extractor already produced. Stop and route to `document-to-data-room-extractor`.
- **Presenting model-generated output as machine-validated**: the schemas, validation verdicts, table names, and gate decisions are Claude-generated specifications, not the result of a database engine executing checks. Label them as proposed/derived. A `modeled-assumption` row that loses its label and travels onto a slide as if it were a verified fact is the single most dangerous failure this skill can cause — keep the `classification` and `review_status` columns attached through every handoff.
- **Silently dropping failing rows**: failing rows must appear in the Gate Report with a reason and an unblock path. A dataset that quietly excludes the rows it could not validate looks cleaner than it is and hides the data-quality problem from the committee.
- **Upgrading confidence or classification during assembly**: assembly never makes a value more trustworthy. A low-confidence OM figure stays low-confidence after it lands in a dataset. Only an analyst action (recorded as `accepted`) or genuine cross-document corroboration may change `review_status`.
- **Broken or non-canonical `source_ref`**: a `source_ref` that does not resolve to `data-room/<doc>#<anchor>` cannot be joined back to its origin downstream. Treat it as a failed validation, not a cosmetic issue — it breaks the entire provenance chain into the deck.
- **NOI / occupancy conflict auto-resolved without disclosure**: the broker-vs-verified gap is the classic data-room misrepresentation. Never collapse it to one number without recording the dedupe rule applied and keeping the losing value in the conflicts list.
- **Stale source treated as current**: a T-12 ending more than a quarter before `as_of_date` understates current expense inflation. Carry the staleness flag through to `needs-review`; do not let an old statement pass the gate as if it were fresh.

## Chain Notes

- **Upstream**: `document-to-data-room-extractor` (the primary source of typed facts; this skill consumes its fact table and never re-extracts), `lease-abstract-extractor` (redacted lease economic structure feeding `lease_economics`), `rent-roll-analyzer` (rent-roll aggregates feeding `rent_roll_aggregate`), `t12-normalizer` (normalized revenue/expense line items feeding `revenue_lineitems` / `expense_lineitems`).
- **Downstream**: `warehouse-to-exhibit-mapper` — consumes the validated, deck-ready datasets (with provenance columns intact) and maps them to exhibit specs and slide inputs.
