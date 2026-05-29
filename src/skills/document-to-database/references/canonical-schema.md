# Canonical Schema: The Cash-Flow Spine, Fact Grains, and Provenance

The single internal vocabulary every `*-to-database` calculator reads from `src/calculators/ingest/schema.py` and `src/calculators/ingest/provenance.py`. It reuses the plugin's existing names (the data-room extractor's lease-economics taxonomy, the CAM-reconciliation recovery terms, the GL line-type entities) so the executable layer never forks the prose layer it sits beneath.

## The cash-flow spine

The whole family models one connected chain — never a single rent number. Every record sits somewhere on this spine, and the strategic value of the family is that contractual charges at the top tie to recognized account actuals at the bottom:

```
property
  -> unit / suite / space
    -> tenant (pseudonymized)
      -> lease
        -> lease_term
          -> charge_schedule (multiple concurrent lines)
            -> charge_code
              -> account_mapping (canonical chart of accounts)
                -> monthly contractual cash flow
                  -> T-12 / operating-statement account line
                    -> operating-statement category
                      -> NOI
```

The spine is bidirectional in use. Going down, a lease's charge schedule annualizes into contractual income. Coming back up, a T-12 account line is the recognized accrual that the contractual run-rate must reconcile against. The reconciliation step proves the rent roll supports the revenue that drives NOI.

## Distinct fact grains

A single document does not produce one flat table. The family preserves nine distinct fact grains, each at its own level of the spine, so a number is never recorded at the wrong resolution:

| Grain | One row per | Where it is produced |
|---|---|---|
| lease | lease | normalize (rent-roll path) |
| unit | unit / suite / space | normalize (rent-roll path) |
| tenant | pseudonymized tenant | normalize (rent-roll path) |
| charge | concurrent charge line within a lease | normalize (rent-roll path) |
| account | canonical chart-of-accounts entry | account mapping |
| monthly-cash-flow | contractual charge x month | charge schedule + frequency |
| T-12-actual | account x fiscal period | normalize (operating-statement path) |
| budget-reforecast | account x period x scenario (`line_type`) | normalize (operating-statement path) |
| derived-reconciled | tie-out dimension (rent roll vs T-12) | reconciliation |

Keeping these grains distinct is what lets the validator, the grader, and the tie-out each operate on the right object: rent arithmetic checks the charge grain, occupancy checks the unit grain, NOI consistency checks the account grain, and the EGI bridge checks the derived-reconciled grain.

## Canonical enums (the typed vocabulary)

- **Charge categories** (the charge grain): `base_rent`, `cam_recovery`, `tax_recovery`, `insurance_recovery`, `percentage_rent`, `parking`, `storage`, `other_recurring`, `one_time_amortized`.
- **Unit status** (not a binary vacant flag): `occupied`, `vacant_available`, `leased_not_occupied`, `down`, `model`, `admin`, `employee`, `owner_occupied`. The last five are excluded from occupancy and revenue denominators; `leased_not_occupied` may carry a future-dated charge schedule and zero current cash flow without being flagged as a contradiction.
- **Lease status**: `active`, `mtm`, `holdover`, `in_default`, `future_commencement`, `terminated`.
- **Recovery methods**: `nnn`, `modified_gross`, `full_service`, `base_year_stop`, `expense_stop`.
- **Line types** (operating statement): `actual`, `budget`, `reforecast`, `prior_year`, `underwritten`.
- **Statement sections** (keep capex/debt/distributions out of NOI): `revenue`, `operating_expense`, `below_the_line_noi`, `capex`, `debt_service`, `distribution`.

## The provenance bundle (a superset, not a fork)

Every emitted record carries a provenance bundle that is a strict SUPERSET of the existing 8-column warehouse provenance contract, so it joins cleanly with the data-room chain and the downstream warehouse pipeline. The eight inherited columns are preserved with identical names and allowed values:

`source_doc`, `locator`, `source_ref`, `extracted_by`, `classification`, `confidence`, `review_status`, `extracted_at`.

On top of those eight, the bundle adds:

- **Granular locator components** — `source_page`, `source_section`, `source_table_id`, `source_row_number`, `source_column_name`, `source_cell_address`, and (for non-PII fields only) `source_text_span`. These let a reviewer walk from any value back to the exact cell.
- **Run / skill / parser identity** — `extraction_run_id`, `skill_name`, `skill_version`, `parser_version`, `extraction_method`.
- **Quality + lifecycle** — `classification` (`source-fact` / `calculated` / `modeled-assumption` / `requires-review`), `confidence` band and a derived `confidence_score`, `validation_status`, and `created_at` / `updated_at` (both set to the caller-supplied `as_of`).
- **Tenancy + governance** — `tenant_id_or_workspace_id`, `pii_class` (`natural_person` / `identifier` / `contact` / `financial` / `aggregate_safe`), and `redaction_status` (`raw` / `pseudonymized` / `redacted` / `aggregate-only`).

## The `source_ref` form

The canonical join key back to the data room is:

```
data-room/<doc>#<anchor>
```

`<doc>` is the source document id and `<anchor>` is the in-document anchor (e.g. `charge`, a table id, a section). This is the same key the data-room extractor mints and the warehouse pipeline joins on, so a fact can be traced end-to-end across the chain without a separate lineage table.

## The locator-not-value rule

For a field classified as PII, the cell ADDRESS (`source_cell_address` / locator) is retained but the verbatim value is never stored — `source_text_span` is dropped and `redaction_status` becomes `redacted`. A verbatim span is retained only for aggregate-safe fields. This is what lets the audit trail prove provenance without ever exposing sensitive text. See `security-governance.md`.
