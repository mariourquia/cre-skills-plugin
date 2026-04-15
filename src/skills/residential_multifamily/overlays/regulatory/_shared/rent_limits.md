# Rent Limits

Status: stub. Placeholder for the rent-limit schedule concept that
regulated housing tests in-place rents against.

## Concept

Rent limits cap the maximum rent a regulated unit can charge at a given
set-aside band and bedroom count. The effective cap a resident pays is a
function of three values: the gross-rent limit published by the program,
the utility allowance charged to the resident for tenant-paid utilities,
and the contract rent or HAP subsidy where a subsidy contract applies.
The overlay does NOT embed numeric limits in prose; it points at reference
tables.

## Target keys the overlay will populate

- `metric_target_band` -> `_core/metrics.md#rent_growth_new_lease`
  gets capped at the program's maximum allowable rent growth, not the
  segment's market-driven growth band.
- `metric_target_band` -> `_core/metrics.md#rent_growth_renewal` same cap.
- `reporting_emphasis` -> adds a rent-limit-compliance waterfall.
- Adds:
  - `rent_limit_schedule` (reference to table)
  - `rent_limit_compliance_rate`
  - `gross_to_tenant_rent_reconciliation`

## Schedule structure

Each row in `reference/normalized/rent_limits__{program}__{market}.csv`:

- program
- set_aside_band
- bedroom_count
- geography
- gross_rent_limit (numeric, lives in reference, not here)
- effective_start, effective_end
- source

## Gross vs. tenant-portion vs. contract-rent

Three related but distinct concepts:

- Gross rent: program-allowed rent for the unit, inclusive of tenant-paid
  utilities imputed via the utility allowance schedule.
- Tenant portion: the dollar amount the resident actually pays, net of any
  subsidy payment and net of any utilities paid directly by the resident to
  a utility provider.
- Contract rent: the dollar amount the owner receives for the unit,
  combining the tenant portion and any subsidy payment (e.g., HAP).

The overlay's rent-limit compliance test is against the gross-rent limit.
Collections and delinquency metrics operate on the tenant portion. Revenue
recognition operates on the contract rent. These three ledgers must be
reconciled by the overlay's reporting emphasis.

## Phase 1 does not implement

- Populated limit tables.
- UA integration logic.
- Held-harmless determination.
- LIHTC average-income test multi-unit aggregation logic.
