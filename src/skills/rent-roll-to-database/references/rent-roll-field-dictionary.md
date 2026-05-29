# Rent Roll Field Dictionary

Canonical rent-roll fields the `rent-roll-to-database` skill produces, with type, nullability, accepted range, and the existing-plugin vocabulary each reuses. Field names deliberately reuse `document-to-data-room-extractor/references/extraction-taxonomy.yaml` (lease_economics) and the `cam-reconciliation-calculator` tenant recovery-terms schema so the executable layer never forks the prose layer.

## Property / asset context

| Field | Type | Nullable | Range / format |
|---|---|---|---|
| `property_id` | string | no | stable id |
| `property_type` | enum | yes | multifamily, office, retail, industrial, mixed-use |
| `rentable_sf` | number | yes | >= 0 |
| `units` | integer | yes | >= 0 |
| `market` | string | yes | free text |
| `as_of` | date | no | ISO `YYYY-MM-DD`; rent-roll effective date, preserved |

## Space / unit / suite

| Field | Type | Nullable | Range / format |
|---|---|---|---|
| `unit_id` | string | no | unique within property |
| `building`, `floor`, `suite` | string | yes | |
| `unit_type` | string | yes | e.g. A1, 2BR |
| `rentable_sf` | number | yes | >= 0 (negative is CRITICAL) |
| `unit_status` | enum | no | occupied, vacant_available, leased_not_occupied, down, model, admin, employee, owner_occupied |

`down / model / admin / employee / owner_occupied` are EXCLUDED from occupancy and revenue denominators. `leased_not_occupied` (signed lease, future commencement) may carry a future-dated charge schedule and zero current cash flow — it is NOT flagged as vacant-with-active-lease.

## Tenant (pseudonymized)

| Field | Type | Nullable | Notes |
|---|---|---|---|
| `tenant_code` | string | yes | pseudonym (`Tenant XXXXXX`), salted by `run_id`. The raw `tenant_name` is consumed on ingest and NEVER emitted. |
| `industry` | string | yes | |

## Lease

| Field | Type | Nullable | Range / format |
|---|---|---|---|
| `lease_id` | string | no | |
| `lease_status` | enum | yes | active, mtm, holdover, in_default, future_commencement, terminated |
| `lease_type` | string | yes | gross, modified_gross, nnn |
| `lease_start`, `lease_expire` | date | yes | expiry must be >= start (else CRITICAL) |
| `recovery_method` | enum | yes | nnn, modified_gross, full_service, base_year_stop, expense_stop |
| `base_year` | integer | yes | required when recovery_method = base_year_stop |
| `expense_stop_psf` | number | yes | required when recovery_method = expense_stop |
| `free_rent_months` | number | yes | >= 0; presence skips the annual==monthly*12 identity |
| `escalation` | object | yes | `{escalation_type (fixed_pct/fixed_dollar/cpi/fmv/none), escalation_amount, escalation_frequency, next_escalation_date, cpi_index, cpi_base_month, cpi_floor, cpi_ceiling}` |
| `security_deposit` | number | yes | >= 0 |

## Charge schedule (the charge grain)

One row per concurrent charge line per lease.

| Field | Type | Nullable | Range / format |
|---|---|---|---|
| `charge_code` | string | yes | raw code; known aliases (RENT, CAM, RET, INS, PKG, STOR) map at high confidence |
| `charge_category` | enum | no | base_rent, cam_recovery, tax_recovery, insurance_recovery, percentage_rent, parking, storage, other_recurring, one_time_amortized |
| `canonical_account` | string | yes | canonical chart-of-accounts slug (e.g. revenue_base_rent) |
| `monthly_amount` | number | yes | |
| `annual_amount` | number | yes | should equal monthly*12 within $1 for flat, full-period leases |
| `frequency` | enum | yes | monthly, quarterly, annual, one_time |
| `is_recoverable` | boolean | yes | |
| `is_estimate` | boolean | yes | true for CAM estimates trued-up annually |
| `psf_basis` | number | yes | annual / rentable_sf (commercial) |

## Validation rules (see also `../../document-to-database/references/data-quality-rules.md`)

- `lease_expire >= lease_start` — else CRITICAL.
- `rentable_sf >= 0` — else CRITICAL.
- `annual == monthly*12` within $1 — SKIPPED for free-rent/abatement/in-period-step leases.
- `rent PSF == annual / rentable_sf` — commercial only; multifamily is per-unit.
- charge code maps to a category, or is flagged for human review (never guessed).
- `vacant_available` must not carry an active lease or in-place charges.
- occupancy in [0, 100]; GPR reconciliation anchors the base-rent tie-out.

## Known limitations

- Billed-vs-collected cash is out of scope (no AR feed); the rent roll is annualized CONTRACTUAL income.
- Percentage-rent breakpoints and co-tenancy/kick-out flags are carried where present but not modeled into contingent-rent projections.
- Prepaid rent and security-deposit-applied-to-rent are documented timing blind spots.
