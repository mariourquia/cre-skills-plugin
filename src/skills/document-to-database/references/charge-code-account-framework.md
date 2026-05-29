# Charge-Code / Account Mapping Framework

How a raw rent-roll charge or a raw operating-statement line becomes a canonical chart-of-accounts entry. Implemented deterministically in `src/calculators/ingest/accounts.py`. The chart of accounts is REUSED from the residential-multifamily GL master data — it is not forked — and parity with that source is enforced by `tests/test_ingestion_canonical_sources.py`, so a single source of truth (ADR-0001) holds while the calculators stay stdlib-only.

## Canonical chart of accounts

The canonical slugs and their GL source ids come from `src/skills/residential_multifamily/reference/connectors/master_data/account_crosswalk.yaml`; the `account_type` / `normal_balance` enums come from the connectors' GL `schema.yaml`.

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

`account_type` is one of `{asset, liability, equity, revenue, expense, capex}`; `normal_balance` is one of `{debit, credit}`. The `statement_section` mapping is what keeps capex out of NOI: a capex line never enters the revenue-minus-operating-expense computation.

## Charge categories and where they post

A rent roll is decomposed into charge categories, each of which posts to a canonical revenue account:

| Charge category | Posts to |
|---|---|
| `base_rent` | `revenue_base_rent` |
| `cam_recovery` | `revenue_other_rental` |
| `tax_recovery` | `revenue_other_rental` |
| `insurance_recovery` | `revenue_other_rental` |
| `percentage_rent` | `revenue_other_rental` |
| `parking` | `revenue_other_rental` |
| `storage` | `revenue_other_rental` |
| `other_recurring` | `revenue_other_rental` |
| `one_time_amortized` | `revenue_other_non_rental` |

The recoveries (CAM, tax, insurance) and the ancillary categories combine into the single `revenue_other_rental` account on purpose, because the canonical chart does not split them. The reconciliation step keeps the rent-roll-side breakdown (recoveries vs other income) visible while comparing the combined total against the T-12 — see `data-quality-rules.md` and the tie-out skill.

## The three-tier resolution ladder (charges)

Mapping is a strict precedence ladder. The skill never guesses a category it cannot defend:

1. **Direct code match (high confidence).** The supplied `charge_code` already IS a known canonical category (e.g. the code is literally `base_rent`). No inference.
2. **Charge-code alias (high confidence).** A real-world code or short label matches a known alias. The alias table maps the codes operators actually use:
   - base rent: `rent`, `base`, `base rent`, `br`, `rnt`, `min rent`, `minimum rent`, `fixed rent`
   - CAM recovery: `cam`, `oe`, `opex`, `cam rec`, `camrec`, `common area`
   - tax recovery: `ret`, `tax`, `re tax`, `ret rec`, `tax rec`
   - insurance recovery: `ins`, `insurance`, `ins rec`
   - percentage rent: `pct`, `percent`, `overage`, `pct rent`, `% rent`
   - parking: `pkg`, `park`, `parking`, `garage`
   - storage: `stor`, `storage`, `locker`
3. **Description inference (medium confidence, flagged for review).** When no code matches but a free-text description does, an ordered, most-specific-first keyword table infers the category (e.g. "common area" -> CAM recovery, "overage" -> percentage rent, "amortized" / "TI repayment" -> one-time amortized, "pet" / "utility" / "late fee" -> other recurring). Medium confidence routes the line to human review.

Anything that matches none of the three is **unmapped**: `charge_category` is null, `needs_review` is true, and the line goes to the human-review queue. It is never silently dropped and never guessed.

## Operating-statement account mapping

T-12 / operating-statement lines map the same way, against the canonical GL accounts:

1. **Direct GL code (high confidence).** A known `account_code` (GL source id) resolves straight to its canonical slug.
2. **Account-name inference (medium confidence, flagged).** An ordered keyword table infers from the line label (e.g. "gross potential rent" / "base rent" -> `revenue_base_rent`; "repairs" / "R&M" -> `expense_repairs_maintenance`; "life safety" / "ADA" / "fire" -> `capex_compliance_life_safety`).
3. **Unmapped bucket.** A line that matches neither accumulates to an `unmapped` bucket and is flagged — never rejected and never recoded. This mirrors the connectors' unmapped-account-handling runbook: surface it for a controller to map, do not drop the dollars.

## Why direct/alias is high and inference is medium

A code or alias is an explicit operator declaration of what the charge is, so it is trusted at high confidence and passes without review. A description match is a reasonable but defeasible reading of free text, so it is medium confidence and always queued for a human to confirm. The confidence band flows into the provenance bundle and into the grade — coverage of high-confidence mappings is a graded dimension. See `data-quality-rules.md`.
