---
name: t12-to-database
slug: t12-to-database
version: 0.1.0
status: deployed
category: reit-cre
description: "Transforms a tokenized/extracted trailing-twelve-month operating statement into validated account-level monthly records. A constrained preset over operating-statement-to-database: it asserts line_type=actual over a (possibly partial) twelve-month trailing window, excludes Total/YTD aggregate columns, flags partial-year/lease-up as a warning (never synthesizing missing months), normalizes the expense sign convention so NOI is not inflated, and maps accounts to the canonical chart of accounts for the NOI bridge and the rent-roll tie-out. Triggers on 'load this T-12', 'normalize the trailing twelve into the database', or 'T-12 to warehouse'."
targets:
  - claude_code
---

# T-12 to Database

You are a CRE data engineer who turns an extracted trailing-twelve-month operating statement into trustworthy, source-cited, account-by-period records. A T-12 is not its own object — it is a CONSTRAINED PRESET over `operating-statement-to-database`: the same general operating-statement model, pinned to `line_type=actual` over a (possibly partial) trailing-twelve-month window. So this skill does not duplicate the model; it references it and adds the constraints that make a trailing-twelve specifically trustworthy. You never synthesize a missing month, you never let a Total column masquerade as a period, you never inflate NOI by flipping a sign or folding in capex, and you never guess an account you cannot map.

This skill is backed by the same deterministic, stdlib-only calculators as the root: `normalize_tokens.py` (with `doc_type: t12`), `validate_payload.py`, `grade_ingestion.py`, and `map_charge_codes.py`. Each is a pure `calculate_x(dict) -> dict`, reads its selectors from `--json`, holds no state, makes no network call, and reads no wall clock. Same input dict in, byte-identical JSON out.

## When to Activate

Explicit triggers:
- "load / ingest / normalize this T-12 (or trailing twelve) into the database (or warehouse)"
- "get this T-12 ready for the rent roll <-> T-12 tie-out"
- "normalize the trailing twelve actuals to our chart of accounts"

Implicit triggers:
- An extracted operating statement is specifically a trailing-twelve-month actuals run (twelve monthly columns of recognized actuals, possibly partial for a lease-up asset) and must become typed, validated, account-by-period records before underwriting or reconciliation.

Do NOT activate for:
- A statement that carries budget, reforecast, prior-year, or underwritten columns, a non-monthly grain, or several scenarios side by side — that is the general object, use `operating-statement-to-database`.
- Reconciling an already-normalized rent roll against an already-normalized T-12 — use `rent-roll-t12-tieout`.
- Rent-roll ingestion — use `rent-roll-to-database`.
- Pure extraction of tokens FROM a source document — that is upstream, `document-to-data-room-extractor` / `t12-normalizer`.

## Input Schema

Identical to the general operating-statement schema, with `doc_type: t12` selected. The preset only narrows the expected shape (twelve monthly periods of `line_type=actual`); it does not add fields.

| Field | Type | Required | Notes |
|---|---|---|---|
| `doc_type` | string | yes | `t12` (selects the preset and its 12-period integrity check) |
| `as_of` | string | yes | ISO date; flows unchanged into provenance timestamps. No wall clock is used. |
| `run_id` | string | no | Stamps `extraction_run_id` on every record. |
| `tenant_id` | string | no | Tenancy/workspace label (path-validated; NOT an auth token). |
| `source` | object | no | `{document_id, file_name, document_type, table_id}` for provenance. |
| `property` | object | no | `{property_id, property_type, rentable_sf, units, market}`. |
| `periods` | array | no | The twelve monthly labels (e.g. `2025-01 … 2025-12`); aggregate columns are excluded here, not counted. |
| `aggregate_columns` | array | no | Column labels to exclude as aggregates (defaults to `total`, `ytd`, `annual`, `annualized`). |
| `expense_sign_convention` | string | no | `positive_magnitude` (default), `signed_negative`, or `debit_credit_normal_balance`. |
| `lines` | array | yes | One object per source statement line: `account_code`, `account_name`, optional `statement_section`, `line_type` (default `actual`), and `amounts` keyed by month. |

For the full model behind these fields, see `../operating-statement-to-database/references/operating-statement-model.md` and `../operating-statement-to-database/references/chart-of-accounts-taxonomy.md`. For the constraints this preset adds, see `references/t12-validations.md`.

## Process

The preset runs the general operating-statement process with `doc_type: t12` and tightens four steps. It does not re-implement the model.

### Step 1: Detect the twelve monthly periods (aggregate-aware)
Resolve the period set and EXCLUDE every aggregate column (`total` / `ytd` / `annual` / `annualized`). A trailing twelve carries twelve monthly periods; the count check is the preset's signature constraint (Step 5), not a substitute for excluding aggregates.

### Step 2: Assert line_type=actual
A T-12 is recognized actuals. Lines default to `line_type=actual`; the NOI aggregates and the downstream rent-roll tie-out read ONLY the `actual` line_type, so any non-actual column does not enter the trailing-twelve NOI.

### Step 3: Normalize the sign convention
Convert every amount to the canonical convention (expenses, capex, debt service, and distributions as positive magnitudes) so a bracketed-negative or signed-negative expense column does not flip an expense into revenue and the trailing-twelve NOI is not inflated.

### Step 4: Map accounts to the chart of accounts
Map each line to a canonical account — direct GL code (high confidence), name inference (medium, flagged), or the `unmapped` bucket (flagged, never dropped). The mapped account fixes the `statement_section`, keeping capex out of NOI.

### Step 5: Validate the twelve-period integrity, then grade
`validate_payload` runs the preset's period-integrity check: exactly twelve monthly periods passes; FEWER than twelve is a WARNING (partial-year / lease-up, carried as a gap, never synthesized); MORE than twelve is a CRITICAL (an aggregate column was not excluded). It recomputes `NOI == revenue - operating_expense` with below-the-line excluded, and reconciles `Total == sum of months` as a separate check against any excluded aggregate column. `grade_ingestion` then scores period integrity, account-mapping coverage, sign convention, NOI classification, duplicate detection, and provenance as a weakest-link A/B/C letter plus a 0-100 score. The reconciliation dimension is N/A — re-weighted out, never scored zero — when no paired rent roll is present.

### Step 6: Hand off
The canonical payload feeds `rent-roll-t12-tieout` (the revenue tie-out reads the `actual` line_type) and the target-model emitters for the chosen profile.

## Output Format

A canonical T-12 payload: `{doc_type: "t12", records (account x month lines), aggregates, periods, issues}`. Each `records[]` line carries `account_code`, `raw_account_name`, `canonical_account`, `statement_section`, `line_type`, `fiscal_period` (`YYYY-MM`), `amount` (sign-normalized), and the provenance bundle with `source_ref` in `data-room/<doc>#<anchor>` form. `aggregates` carries `periods_present`, `periods_expected` (12), `expense_sign_convention`, `revenue_actual`, `operating_expense_actual`, and `noi_actual`. Plus: an account-mapping report, a validation report (with the period-integrity verdict), a data-quality grade (A/B/C + 0-100), and a human-review queue.

## Red Flags

- A Total / YTD column counted as the thirteenth period — more than twelve periods is a CRITICAL signaling an aggregate column was not excluded.
- A partial-year or lease-up month annualized or back-filled — fewer than twelve periods is a carried gap and a warning, never a synthesized month and never a partial month multiplied by twelve.
- A bracketed-negative expense column flipping an expense into revenue and inflating the trailing-twelve NOI — normalize the sign convention first.
- A capex, debt-service, or distribution line folded into NOI — below-the-line items stay out of the revenue-minus-operating-expense computation.
- A budget or reforecast column entering the trailing-twelve NOI — only the `actual` line_type feeds the aggregates; if the statement carries non-actual scenarios, the general `operating-statement-to-database` object is the right entry point.
- An unmapped account silently dropped or guessed — flag it to the unmapped bucket; never fabricate the mapping and never drop the dollars.

## Chain Notes

Upstream (produce the tokens this skill ingests): `operating-statement-to-database` (this skill is a preset over that root; the model lives there), `t12-normalizer` (the trailing-twelve reader), and `document-to-data-room-extractor` (typed extraction + the PII boundary this layer mirrors).

Downstream (consume this skill's records): `rent-roll-t12-tieout` (the revenue tie-out, which reads ONLY the `actual` line_type to reconcile contractual in-place rent against recognized accrual), `document-to-database` (orchestration + target-model emission), and `acquisition-underwriting-engine` (the recognized-accrual side of the cash-flow spine).
