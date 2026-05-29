# T-12 Validations

The validations the `t12-to-database` preset adds on top of the general operating-statement model. Implemented deterministically in `src/calculators/validate_payload.py` (the `t12` branch) and `src/calculators/normalize_tokens.py` (the `operating_statement` path with `doc_type: t12`). These are the constraints that make a trailing-twelve specifically trustworthy; the underlying model (line types, sections, sign conventions, NOI composition) lives in `../operating-statement-to-database/references/operating-statement-model.md` and is not repeated here.

## Period integrity (the signature constraint)

A T-12 is twelve monthly columns of recognized actuals. The period check is FORMAT-AWARE — it asserts twelve MONTHLY periods after aggregate columns are excluded, never a blind `count == 12` over raw columns:

| Periods present (after exclusion) | Verdict | Why |
|---|---|---|
| exactly 12 | PASS | a complete trailing twelve |
| fewer than 12 | WARNING (`partial_year`) | partial-year / lease-up; the gap is carried, not filled |
| more than 12 | CRITICAL (`t12_period_count_invalid`) | an aggregate column was not excluded |

The count is taken AFTER aggregate-column exclusion (next section), so a clean twelve-month statement with a Total column reads as twelve periods, not thirteen.

## Aggregate-column exclusion

Before the period count is taken, every label in `aggregate_columns` (default `total`, `ytd`, `annual`, `annualized`) is detected and EXCLUDED from the period set. A Total / YTD / annualized column is never counted as a period and never summed into the per-period totals. If an aggregate column slips through unexcluded, it surfaces as the >12-period CRITICAL above — the count check is the backstop for a missed exclusion.

## Partial-year / lease-up handling

Fewer than twelve periods is legitimate for a lease-up or partially-operated asset. The preset:

- emits a WARNING (`partial_year`) and carries the gap forward in `aggregates.periods_present`;
- NEVER synthesizes the missing months;
- NEVER multiplies a partial month (or a partial-year sum) up to a full year.

Annualization is a downstream modeling decision, not an ingestion act — the preset records exactly the months that exist and flags the shortfall so the consumer annualizes explicitly if they choose to.

## Sign-convention checks

The preset normalizes the expense sign convention exactly as the root does. `expense_sign_convention` is one of `positive_magnitude` (default), `signed_negative`, or `debit_credit_normal_balance`; the normalizer converts every amount to one canonical convention (revenue positive; operating expense, capex, debt service, and distribution as positive magnitudes). Bracketed negatives (`(1,234)`) are parsed to a signed number before the magnitude is taken, and currency symbols and separators are stripped. This guarantees a bracketed-negative or signed-negative expense column does not flip an expense into revenue and inflate the trailing-twelve NOI.

## Duplicate / subtotal detection

An account that appears more than once per `(canonical_account, line_type)` is flagged (`duplicate_account_line`, a warning) as a probable subtotal re-counted as a detail line. NOI and the section totals are computed from DETAIL lines only, so the flag guards against doubling a section. An ambiguous repeat is surfaced for review rather than silently summed.

## NOI = revenue - opex (below-the-line excluded)

`validate_payload` recomputes the NOI identity from the `actual` line_type:

```
NOI == revenue_actual - operating_expense_actual
```

If the reported `noi_actual` does not equal `revenue_actual - operating_expense_actual` within rounding, the check raises `noi_includes_below_the_line` (CRITICAL): a `capex`, `debt_service`, or `distribution` line has leaked into the revenue or operating-expense sections. Below-the-line items MUST stay out of the NOI computation. Because the mapped canonical account fixes the `statement_section` (a capex slug -> the `capex` section), a capex line cannot silently inflate NOI without tripping this check.

## Total == sum-of-months reconciliation

When a Total / annual column was excluded as an aggregate, it is reconciled SEPARATELY against the sum of the twelve monthly periods. This is a distinct check from the period totals — the excluded aggregate is never summed INTO the periods, it is summed AGAINST them. A material mismatch between the stated Total and the month-by-month sum surfaces for review (the extracted Total and the extracted months disagree), rather than being silently absorbed.

## Grading dimensions (preset)

`grade_ingestion` scores the T-12 on its operating-statement dimensions as a weakest-link A/B/C letter (a single C caps the grade) plus a 0-100 secondary score:

| Dimension | Drops below A when |
|---|---|
| period integrity | partial-year warning (B) or >12-period critical (C) |
| account-mapping coverage | distinct `(canonical_account, line_type)` keys fall to the `unmapped` bucket |
| sign convention | the validator flags a sign flip |
| NOI classification consistency | a below-the-line item leaked into NOI (C) |
| duplicate / subtotal detection | a duplicate account line is flagged (B) |
| provenance | the run is unstamped or accounts are unmapped |

Gates: merge requires the score to clear the merge threshold (>= 85) AND no C AND no critical failure; production requires the higher threshold (>= 92) AND all-A AND no critical. The reconciliation grading dimension is N/A — re-weighted out, NEVER scored zero — when no paired rent roll is present, so a standalone T-12 is not penalized for the absence of a tie-out it was never given.

## Known limitations

- The preset assumes a monthly grain; a quarterly or annual-summary statement is the general object's territory (`operating-statement-to-database`), not this preset.
- Accrual vs cash basis is taken as declared; the preset does not re-derive one from the other.
- A T-12 with no `actual` line_type produces no NOI aggregate and a N/A reconciliation dimension by construction — it is not scored zero, but it is also not a usable trailing-twelve until actuals are present.
