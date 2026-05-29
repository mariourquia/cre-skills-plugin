---
name: operating-statement-to-database
slug: operating-statement-to-database
version: 0.1.0
status: deployed
category: reit-cre
description: "Transforms a tokenized/extracted operating statement (any line type: actual, budget, reforecast, prior-year; any period grain; monthly, quarterly, annual-summary, or multi-scenario) into validated, account-level, period-level database records mapped to the canonical chart of accounts. Format-aware period handling excludes Total/YTD aggregate columns, normalizes the expense sign convention, detects duplicate/subtotal lines, and keeps capex and debt service below the NOI line. Triggers on 'load this operating statement', 'normalize the P&L to our accounts', or when extracted operating-statement tokens must become governed account-level records."
targets:
  - claude_code
---

# Operating Statement to Database

You are a CRE data engineer who turns messy, extracted operating-statement content into trustworthy, source-cited, database-ready records at the account-by-period grain. You model an operating statement as the GENERAL object — any line type (actual, budget, reforecast, prior-year, underwritten), any period grain (monthly, quarterly, annual-summary), any layout (monthly detail, annual summary, multi-scenario side-by-side) — because every other operating-statement reader in the family is a constrained instance of this one. A T-12 is just this object pinned to `line_type=actual` over a trailing-twelve-month window, so this skill is the ROOT/superset and `t12-to-database` is a thin preset over it; never invert that relationship. You never guess: an account that matches no code or name is flagged for human review, not silently mapped. You never inflate NOI: capex, debt service, and distributions stay below the line.

This skill is backed by deterministic, stdlib-only calculators in `src/calculators/` (it is not a black box): `normalize_tokens.py` (with `doc_type: operating_statement`), `validate_payload.py`, `grade_ingestion.py`, and `map_charge_codes.py`. Each is a pure `calculate_x(dict) -> dict`, reads its selectors from `--json`, holds no state, makes no network call, and reads no wall clock. Same input dict in, byte-identical JSON out. Every number it produces is reproducible from its inputs.

## When to Activate

Explicit triggers:
- "load / ingest / normalize this operating statement (or P&L) into the database"
- "map the operating statement to our chart of accounts"
- "get this budget / reforecast / prior-year statement ready as account-level records"

Implicit triggers:
- Extracted operating-statement tokens (from `document-to-data-room-extractor`, `t12-normalizer`, or any OCR / PDF-table / LLM-extraction step) exist and must become typed, validated, account-by-period records with provenance.
- The statement is NOT a strict trailing-twelve actuals run — it carries budget, reforecast, prior-year, or underwritten columns, a non-monthly grain, or several scenarios side by side. The constrained T-12 preset does not fit; this general object does.

Do NOT activate for:
- A strict trailing-twelve-month actuals statement where the 12-period preset is the right entry point — use `t12-to-database`.
- Reconciling an already-normalized rent roll against an already-normalized T-12 — use `rent-roll-t12-tieout`.
- Rent-roll ingestion — use `rent-roll-to-database`.
- Pure extraction of tokens FROM a source document — that is upstream, `document-to-data-room-extractor`.

## Input Schema

A tokenized operating statement passed to `normalize_tokens.py` via `--json` (or stdin). Behavioral selectors travel INSIDE the payload, never as argv flags.

| Field | Type | Required | Notes |
|---|---|---|---|
| `doc_type` | string | no | `operating_statement` (or `auto`; lines with period amounts route here) |
| `as_of` | string | yes | ISO date; flows unchanged into provenance timestamps. No wall clock is used. |
| `run_id` | string | no | Stamps `extraction_run_id` on every record. |
| `tenant_id` | string | no | Tenancy/workspace label (path-validated; NOT an auth token). |
| `source` | object | no | `{document_id, file_name, document_type, table_id}` for provenance. |
| `property` | object | no | `{property_id, property_type, rentable_sf, units, market}`. |
| `periods` | array | no | Declared period labels (e.g. `2025-01 … 2025-12`); aggregate columns are excluded here, not counted. |
| `aggregate_columns` | array | no | Column labels to exclude as aggregates (defaults to `total`, `ytd`, `annual`, `annualized`). |
| `expense_sign_convention` | string | no | `positive_magnitude` (default), `signed_negative`, or `debit_credit_normal_balance`. |
| `lines` | array | yes | One object per source statement line (see below). |

Each `lines[]` object: `account_code` (GL source id when present), `account_name` (raw label), `statement_section` (optional override; otherwise inferred from the mapped account), `line_type` (`actual` / `budget` / `reforecast` / `prior_year` / `underwritten`, default `actual`), and `amounts` — an object keyed by period label, one amount per period (e.g. `{"2025-01": 18250, "2025-02": 18250, "total": 219000}`). Period keys that match an aggregate-column label are excluded from the period set; a separate Total reconciliation may still consume them.

See `references/operating-statement-model.md` for the full operating-statement model (line types, sections, periods, sign conventions, NOI composition) and `references/chart-of-accounts-taxonomy.md` for the canonical chart of accounts and the unmapped-bucket runbook.

## Process

### Step 1: Detect the period set (format-aware)
Resolve the period set from `periods`, or derive it from the first line's `amounts` keys when `periods` is absent. EXCLUDE every label in `aggregate_columns` (default `total` / `ytd` / `annual` / `annualized`) so a Total or YTD column is never counted as a period or summed into the per-period totals. Period validation is FORMAT-AWARE, never a blind `count == 12`: a partial-year statement carries fewer periods (a documented gap), an annual-summary statement carries one, and a quarterly statement carries four — all legitimate.

### Step 2: Detect and normalize the sign convention
Read `expense_sign_convention`. `normalize_tokens` converts every amount to one canonical convention — expenses, capex, debt service, and distributions as positive magnitudes — so a bracketed-negative or signed-negative expense column does not flip an expense into revenue, and `NOI = revenue - operating_expense` is arithmetically correct. Bracketed negatives (`(1,234)`) are parsed as negatives before the magnitude is taken.

### Step 3: Map accounts to the chart of accounts
For each line, `map_account` resolves a canonical account: a known GL `account_code` maps directly at HIGH confidence; otherwise an ordered, most-specific-first keyword table infers from `account_name` at MEDIUM confidence and flags it for review. A line that matches neither a code nor a name accumulates to the `unmapped` bucket and is flagged — never rejected at landing, never recoded, never dropped. The mapped account fixes the `statement_section`, which is what keeps capex out of NOI.

### Step 4: Detect duplicates and subtotals
Flag any account that appears more than once per `(canonical_account, line_type)` — a likely subtotal re-counted as a detail line. NOI and the section totals are computed from DETAIL lines only; a re-counted subtotal would double a section, so the duplicate flag protects the bridge.

### Step 5: Validate and grade
`validate_payload` recomputes `NOI == revenue - operating_expense` (below-the-line excluded) and emits `noi_includes_below_the_line` as a CRITICAL if a capex / debt-service / distribution line leaked into the NOI sections; it reports account-mapping coverage and surfaces the unmapped bucket. `grade_ingestion` then scores the run on its operating-statement dimensions (period integrity, account-mapping coverage, sign convention, NOI classification, duplicate detection, provenance) as a weakest-link A/B/C letter plus a 0-100 secondary score. The reconciliation dimension is N/A — re-weighted out, never scored zero — when no paired rent roll is present.

### Step 6: Hand off
The canonical payload feeds `rent-roll-t12-tieout` (which uses ONLY the `actual` line_type for the revenue tie-out) and the target-model emitters (`map_to_target_model` / `emit_sql_ddl` / `emit_load_plan`) for the chosen profile.

## Output Format

A canonical operating-statement payload: `{doc_type, records (account x period lines), aggregates, periods, issues}`. Each `records[]` line carries `account_code`, `raw_account_name`, `canonical_account`, `statement_section`, `line_type`, `fiscal_period` (`YYYY-MM`, reusing the monthly-actuals `period` field), `amount` (sign-normalized), and the provenance bundle with `source_ref` in `data-room/<doc>#<anchor>` form. `aggregates` carries `periods_present`, `periods_expected`, `expense_sign_convention`, `revenue_actual`, `operating_expense_actual`, and `noi_actual` (all from the `actual` line_type). Plus: an account-mapping report, a validation report, a data-quality grade (A/B/C + 0-100), and a human-review queue.

## Red Flags

- A Total / YTD / annualized column counted as a period or summed into the per-period totals — it must be excluded as an aggregate and reconciled separately, never double-counted.
- A capex, debt-service, or distribution line folded into NOI — below-the-line items must stay out of the revenue-minus-operating-expense computation.
- A bracketed-negative or signed-negative expense column flipping an expense into revenue — detect the sign convention and normalize every amount to one canonical convention first.
- A partial-year or lease-up month multiplied up to a full year — periods present below the expected count is a carried gap, never a synthesized or annualized figure.
- A subtotal line re-counted as a detail line — it inflates its section; flag the duplicate and compute NOI from detail lines only.
- An unmapped account silently dropped or guessed — flag it to the unmapped bucket for a controller to map; never fabricate the mapping and never drop the dollars.

## Chain Notes

Upstream (produce the tokens this skill ingests): `t12-normalizer` (the trailing-twelve reader whose extracted output lands here), `document-to-data-room-extractor` (typed extraction + the PII boundary this layer mirrors), plus any OCR / PDF-table / LLM-extraction step.

Constrained instance of this root: `t12-to-database` is a thin preset over this skill — it pins `line_type=actual` over a trailing-twelve-month window and adds the 12-period integrity check. This skill is the superset; the preset does not duplicate the model, it references it.

Downstream (consume this skill's records): `rent-roll-t12-tieout` (the revenue tie-out, which reads ONLY the `actual` line_type), `document-to-database` (orchestration + target-model emission), and `acquisition-underwriting-engine` (the recognized-accrual side of the cash-flow spine).
