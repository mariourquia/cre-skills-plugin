# Operating Statement Model

The general operating-statement object the `operating-statement-to-database` skill normalizes, and the rules that turn an arbitrary P&L layout into clean account-by-period records. Implemented deterministically in `src/calculators/normalize_tokens.py` (the `operating_statement` path) and `src/calculators/ingest/schema.py`. Field names reuse the GL `schema.yaml` actual / budget / forecast entities and the monthly-actuals below-the-line structure, so the executable layer never forks the prose layer it sits beneath.

## The general object (and why it is the root)

An OPERATING STATEMENT is the GENERAL object: any line type, any period grain, any layout. A T-12 is a CONSTRAINED INSTANCE of it — `line_type=actual` over a (possibly partial) trailing-twelve-month window. Because the T-12 is a special case of the operating statement and not the other way around, this model is the ROOT/superset and `t12-to-database` is a thin preset over it. Everything below applies to the general object; the preset only narrows it.

The object spans these dimensions:

- **Line type**: `actual`, `budget`, `reforecast`, `prior_year`, `underwritten`.
- **Period grain**: monthly, quarterly, annual-summary, or a partial-year window.
- **Layout**: monthly detail, annual summary, quarterly, or multi-scenario columns side by side.

## Line type

`line_type` reuses the GL schema's actual / budget / forecast entities:

| line_type | Meaning | Reads into NOI aggregates? |
|---|---|---|
| `actual` | recognized accruals | yes — the ONLY type summed into `revenue_actual` / `operating_expense_actual` / `noi_actual` |
| `budget` | approved or rebudget scenario | no (graded as a separate scenario) |
| `reforecast` | a forecast vintage | no |
| `prior_year` | prior fiscal-year comparative | no |
| `underwritten` | acquisition / hold model column | no |

A line whose `line_type` is unrecognized is flagged (`line_type_unknown`, a warning) but still carried. The 12-period and reconciliation checks are scoped per `(property, scenario, fiscal_year)`, so an actual column and a budget column for the same months are never conflated.

## Fiscal period

`fiscal_period` is `YYYY-MM` and reuses the monthly-actuals `period` field, so each account-by-period line lands directly on the GL `actual` / `budget` / `forecast` grain. The `amounts` object on each input line is keyed by period label; one record is emitted per `(line, period)` that carries a numeric amount. A period whose amount is null or blank is skipped (no zero is fabricated).

## Statement section and NOI composition

`statement_section` partitions every line relative to the NOI line: `revenue`, `operating_expense`, `below_the_line_noi`, `capex`, `debt_service`, `distribution`. NOI is computed from the `actual` line_type only:

```
NOI = revenue_actual - operating_expense_actual
```

`capex`, `debt_service`, and `distribution` are below-the-line by definition and MUST be excluded — NOI never includes them. The validator recomputes this identity and raises `noi_includes_below_the_line` (CRITICAL) if a below-the-line line leaked into the revenue or operating-expense sections. The mapped canonical account fixes the section (a capex slug -> the `capex` section), so a capex line cannot silently inflate NOI.

## Format-aware period handling

Period validation is FORMAT-AWARE, not a blind `count == 12`:

- **Aggregate-column exclusion.** Labels in `aggregate_columns` (default `total`, `ytd`, `annual`, `annualized`) are detected and EXCLUDED from the period set, so a Total or YTD column is never counted as a period or summed into the per-period totals. The `Total == sum of months` reconciliation is run as a SEPARATE check against the excluded column, not folded into the period totals.
- **Partial-year / lease-up.** Fewer periods than expected (a partial-year or lease-up statement) emits a WARNING and carries the gap forward. It is NEVER a hard fail, and a partial month is NEVER multiplied up to a full year.
- **Annual-summary and quarterly grains.** One period (annual summary) or four periods (quarterly) are legitimate grains, not deficiencies — the format determines the expected count, not a hardcoded twelve.
- **Too many periods.** More periods than the grain allows (the strict T-12 preset treats this as the 12-period ceiling) indicates an aggregate column was not excluded — handled by the preset as a CRITICAL. See `../t12-to-database/references/t12-validations.md`.

## Sign-convention detection

`expense_sign_convention` is one of:

| Convention | How expenses arrive | Normalization |
|---|---|---|
| `positive_magnitude` | expenses as positive numbers | already canonical |
| `signed_negative` | expenses as negative numbers (incl. bracketed `(1,234)`) | take the magnitude of opex / capex / debt / distribution |
| `debit_credit_normal_balance` | by normal balance | take the magnitude |

The normalizer converts every amount to ONE canonical convention — revenue positive, and expense / capex / debt-service / distribution as positive magnitudes (subtracted downstream). This is why `NOI = revenue - operating_expense` is correct and why a bracketed-negative expense column does not flip an expense into revenue. Bracketed negatives are parsed to a signed number before the magnitude is taken, and currency symbols and thousands separators are stripped.

## Duplicate / subtotal detection

An account that appears more than once per `(canonical_account, line_type)` is flagged (`duplicate_account_line`, a warning) as a probable subtotal re-counted as a detail line. NOI and the section totals are computed from DETAIL lines only, so the flag guards against doubling a section. A subtotal recognized as such is excluded from the detail-line sum; an ambiguous repeat is surfaced for review rather than silently summed.

## Known limitations

- Accrual vs cash basis is taken as declared; the model does not re-derive a cash statement from an accrual one or vice versa.
- Allocations and management-fee eliminations across a portfolio statement are carried as supplied, not re-allocated.
- A statement with no `actual` line_type produces no NOI aggregate (there is nothing to recognize); the reconciliation dimension is then N/A by construction, not scored zero.
