# Chart-of-Accounts Taxonomy

The canonical chart of accounts an operating-statement line maps to, plus the line-type and statement-section taxonomy that governs how each amount is classified. Implemented deterministically in `src/calculators/ingest/accounts.py`. The chart of accounts is REUSED from the residential-multifamily GL master data — it is not forked. The canonical slugs and their GL source ids come from `src/skills/residential_multifamily/reference/connectors/master_data/account_crosswalk.yaml`; the `account_type` / `normal_balance` enums come from the connectors' GL `schema.yaml`. Parity with those YAML files is enforced by `tests/test_ingestion_canonical_sources.py`, so a single source of truth holds while the calculators stay stdlib-only.

## Canonical chart of accounts

Every operating-statement line resolves to one of these canonical slugs (or to the `unmapped` bucket). The `statement_section` column is what keeps capex out of NOI: a capex slug never enters the revenue-minus-operating-expense computation.

| Canonical slug | account_type | normal_balance | statement_section |
|---|---|---|---|
| `revenue_base_rent` | revenue | credit | revenue |
| `revenue_other_rental` | revenue | credit | revenue |
| `revenue_other_non_rental` | revenue | credit | revenue |
| `expense_payroll` | expense | debit | operating_expense |
| `expense_contract_labor` | expense | debit | operating_expense |
| `expense_repairs_maintenance` | expense | debit | operating_expense |
| `expense_turn` | expense | debit | operating_expense |
| `capex_component_replacement` | capex | debit | capex |
| `capex_value_add` | capex | debit | capex |
| `capex_compliance_life_safety` | capex | debit | capex |

`account_type` is one of `{asset, liability, equity, revenue, expense, capex}`; `normal_balance` is one of `{debit, credit}`. These reuse the GL schema's chart-of-accounts entity exactly.

## Statement-section taxonomy

`statement_section` partitions every line into where it sits relative to NOI:

| Section | What it holds | In NOI? |
|---|---|---|
| `revenue` | base rent, other rental income, other non-rental income | yes (adds) |
| `operating_expense` | payroll, contract labor, R&M, turn, and other opex | yes (subtracts) |
| `below_the_line_noi` | items explicitly reported below the NOI line | no |
| `capex` | component replacement, value-add, compliance / life-safety | no |
| `debt_service` | interest and principal | no |
| `distribution` | partner / owner distributions | no |

`NOI = revenue - operating_expense`. The last four sections are below-the-line by definition and never enter that arithmetic. A line whose mapped account is a capex slug is assigned the `capex` section automatically; an explicit `statement_section` on the input line can override the inferred section but cannot move a capex slug into a revenue or operating-expense section without re-mapping the account.

## Line type and scenario

`line_type` reuses the GL schema's actual / budget / forecast entities, extended for the scenarios an operating statement carries:

| line_type | Reuses GL entity | Notes |
|---|---|---|
| `actual` | `actual` | recognized accruals; the ONLY type the NOI aggregates and the rent-roll tie-out read |
| `budget` | `budget` | approved or rebudget scenario |
| `reforecast` | `forecast` | a forecast vintage / reforecast |
| `prior_year` | `actual` (prior fiscal year) | comparative column |
| `underwritten` | (modeled) | acquisition / hold underwriting column |

The 12-period and reconciliation checks are scoped per `(property, scenario, fiscal_year)`, so a budget column and an actual column for the same months are graded as separate scenarios, not conflated. `fiscal_period` is `YYYY-MM` and reuses the monthly-actuals `period` field, so an account-by-period line lands directly on the GL `actual` / `budget` / `forecast` grain.

## The three-tier resolution ladder (accounts)

An operating-statement line becomes a canonical slug by a strict precedence ladder. The skill never guesses a mapping it cannot defend:

1. **Direct GL code (high confidence).** A known `account_code` (GL source id, e.g. `6100`) resolves straight to its canonical slug. No inference, no review.
2. **Account-name inference (medium confidence, flagged).** When no code matches, an ordered, most-specific-first keyword table infers from the line label (e.g. "gross potential rent" / "base rent" -> `revenue_base_rent`; "repairs" / "R&M" -> `expense_repairs_maintenance`; "life safety" / "ADA" / "fire" -> `capex_compliance_life_safety`). Medium confidence always routes the line to human review.
3. **Unmapped bucket.** A line that matches neither a code nor a name maps to `unmapped`: `needs_review` is true and the line goes to the human-review queue.

## Unmapped-bucket runbook

A line that matches none of the three tiers is **unmapped** — it is NEVER rejected at landing, recoded, or dropped. The dollars stay in the payload, attributed to the `unmapped` bucket, with `needs_review = true`. The reviewer maps it to a canonical slug (or confirms it as genuinely out of the canonical chart). This mirrors the connectors' unmapped-account-handling runbook: surface it for a controller to map, never silently lose the dollars. Account-mapping coverage (the share of distinct `(canonical_account, line_type)` keys that resolved out of the unmapped bucket) is a graded dimension, so a statement full of unmapped lines lowers the grade rather than passing quietly.

## Why direct is high and inference is medium

A GL code is an explicit operator declaration of what the account is, so it is trusted at high confidence and passes without review. A name match is a reasonable but defeasible reading of a free-text label, so it is medium confidence and always queued for a human to confirm. The confidence band flows into the provenance bundle and into the grade, so the chart of accounts the operating statement maps to is always auditable back to whether it was declared or inferred.
