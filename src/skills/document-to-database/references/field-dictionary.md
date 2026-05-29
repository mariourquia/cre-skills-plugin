# CRE Field Dictionary

The canonical fields the document-to-database family produces across the cash-flow spine, with CRE data type, nullability standard, accepted range, and expected format. Field names deliberately reuse the plugin's existing vocabulary (`document-to-data-room-extractor`'s lease-economics taxonomy and the `cam-reconciliation-calculator` tenant recovery-terms schema) so the executable layer never forks the prose layer. Enums are defined in `src/calculators/ingest/schema.py`; tolerances in `src/calculators/ingest/tolerances.py`.

Nullability standard: a field marked **no** must be present for the record to be usable; a field marked **yes** is optional but, where economically required (e.g. `base_year` under a base-year stop), its absence is a completeness signal that lowers the grade.

## Property / asset context

| Field | Type | Nullable | Range / format |
|---|---|---|---|
| `property_id` | string | no | stable id |
| `property_type` | enum | yes | multifamily, office, retail, industrial, mixed-use |
| `rentable_sf` | number | yes | >= 0 (negative is impossible -> critical) |
| `units` | integer | yes | >= 0 |
| `market` | string | yes | free text |
| `as_of` | date | no | ISO `YYYY-MM-DD`; the document effective date, preserved unchanged |

## Unit / suite / space (the unit grain)

| Field | Type | Nullable | Range / format |
|---|---|---|---|
| `unit_id` | string | no | unique within property |
| `building`, `floor`, `suite` | string | yes | structural location |
| `unit_type` | string | yes | e.g. A1, 2BR, suite class |
| `rentable_sf` | number | yes | >= 0 (negative is critical) |
| `unit_status` | enum | no | occupied, vacant_available, leased_not_occupied, down, model, admin, employee, owner_occupied |

`down / model / admin / employee / owner_occupied` are excluded from occupancy and revenue denominators. `leased_not_occupied` (signed lease, future commencement) may carry a future-dated charge schedule with zero current cash flow and is NOT flagged as vacant-with-active-lease.

## Tenant (the tenant grain, pseudonymized)

| Field | Type | Nullable | Notes |
|---|---|---|---|
| `tenant_code` | string | yes | salted pseudonym (`Tenant XXXXXX`), stable within a `run_id`. The raw natural-person name is consumed on ingest and NEVER emitted. |
| `industry` | string | yes | commercial sector, where present |

## Lease (the lease grain)

| Field | Type | Nullable | Range / format |
|---|---|---|---|
| `lease_id` | string | no | stable id |
| `lease_status` | enum | yes | active, mtm, holdover, in_default, future_commencement, terminated |
| `lease_type` | string | yes | gross, modified_gross, nnn |
| `lease_start`, `lease_expire` | date | yes | expiry must be >= start (else critical) |
| `recovery_method` | enum | yes | nnn, modified_gross, full_service, base_year_stop, expense_stop |
| `base_year` | integer | yes | economically required when recovery_method = base_year_stop |
| `expense_stop_psf` | number | yes | economically required when recovery_method = expense_stop |
| `free_rent_months` | number | yes | >= 0; presence skips the annual==monthly*12 identity for that lease |
| `security_deposit` | number | yes | >= 0 |
| `escalation` | object | yes | `{escalation_type (fixed_pct/fixed_dollar/cpi/fmv/none), escalation_amount, escalation_frequency, next_escalation_date, cpi_index, cpi_base_month, cpi_floor, cpi_ceiling}` |

## Charge schedule (the charge grain)

One row per concurrent charge line per lease. A lease carries multiple lines, not a single rent figure.

| Field | Type | Nullable | Range / format |
|---|---|---|---|
| `charge_code` | string | yes | raw code; known aliases map at high confidence |
| `charge_category` | enum | no | base_rent, cam_recovery, tax_recovery, insurance_recovery, percentage_rent, parking, storage, other_recurring, one_time_amortized |
| `canonical_account` | string | yes | canonical chart-of-accounts slug (e.g. revenue_base_rent) |
| `monthly_amount` | number | yes | currency; parsed from `$`, commas, and `(parens)` negatives |
| `annual_amount` | number | yes | should equal monthly*12 within $1 for flat, full-period leases |
| `frequency` | enum | yes | monthly, quarterly, annual, one_time |
| `is_recoverable` | boolean | yes | recoverable expense pass-through flag |
| `is_estimate` | boolean | yes | true for CAM estimates trued-up annually |
| `psf_basis` | number | yes | annual / rentable_sf (commercial); per-unit for multifamily |

## Account x period (the T-12-actual and budget-reforecast grains)

| Field | Type | Nullable | Range / format |
|---|---|---|---|
| `account_code` | string | yes | raw source GL code |
| `raw_account_name` | string | yes | source line label, preserved verbatim |
| `canonical_account` | string | yes | canonical slug, or `unmapped` (routed to review) |
| `statement_section` | enum | yes | revenue, operating_expense, below_the_line_noi, capex, debt_service, distribution |
| `line_type` | enum | yes | actual, budget, reforecast, prior_year, underwritten |
| `fiscal_period` | string | yes | `YYYY-MM` (reuses the monthly-actuals period key) |
| `amount` | number | yes | normalized to a canonical sign (revenue positive; expense/capex/debt as positive magnitudes) |

## Type coercion conventions

- **Currency strings** are coerced by stripping `$` and thousands separators and reading `(1,234)` as `-1234`.
- **Periods** are `YYYY-MM`; **dates** are `YYYY-MM-DD`. A schema-inference pass distinguishes the two when a column's shape is unknown.
- **Booleans** accept `true/false`, `yes/no`, `y/n`.
- A blank or `None` value is null, not zero — the validator and grader treat a missing required field as a completeness gap, never as a silent zero.

## Accepted ranges and reconciliation tolerances

- `lease_expire >= lease_start`; `rentable_sf >= 0`; occupancy in `[0, 100]`. Violations are impossible data — critical.
- `annual == monthly*12` within **$1** for flat, full-period leases; SKIPPED-with-note for free-rent / abatement / in-period-step leases.
- Base-rent PSF outside `[0, 500]` on a commercial lease is implausible — a warning that lowers confidence, not a rejection.
- Reconciliation is dimension-aware (fraction of the larger side): base rent ties tight (1%), recoveries float wider (15%, reflecting the CAM estimate-vs-true-up cycle), occupancy ties tight on a count basis (1%), and the EGI bridge holds to 3%.

See `data-quality-rules.md` for the full rule set and the impossible-vs-implausible split, and `charge-code-account-framework.md` for how `charge_code` resolves to `canonical_account`.
