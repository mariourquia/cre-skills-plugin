# Income Limits

Status: stub. Placeholder for the income-limit schedule concept that
regulated housing tests household eligibility against.

## Concept

Income limits define the maximum household income that qualifies for a
regulated unit at a given set-aside band (e.g., a LIHTC AMI-banded
set-aside, HUD very-low-income). Limits are published by an external authority (HUD, state
HFA, USDA) on a cadence (typically annual) and vary by program, geography,
and household size. The overlay does NOT embed numeric limits in prose; it
points at reference tables that carry the current and historical schedule.

## Target keys the overlay will populate

- `reporting_emphasis` -> adds income-band compliance as a tracked report.
- Adds:
  - `income_limit_schedule` (reference to the current table row)
  - `income_band_compliance_rate`

## Schedule structure

Each row in `reference/normalized/income_limits__{program}__{market}.csv`
carries:

- program (slug)
- set_aside_band (slug)
- geography (market or submarket or MSA identifier)
- household_size (integer)
- effective_start (date)
- effective_end (date or open)
- source (publisher identifier)

## Interaction with rent testing

Rent tests (see `rent_limits.md`) frequently cite the income-limit schedule
as their denominator. Example: the LIHTC AMI-banded rent limit for a
two-bedroom unit references the corresponding AMI-banded income limit for a
household size derived from the unit's bedroom count by a program-specific
imputation rule. The imputation
rule itself is a shared concept, not a numeric constant; it lives in the
program overlay that owns the rule.

## Phase 1 does not implement

- Populated limit tables.
- Imputation rules per program.
- Cross-period comparison logic for determining whether a reduction is
  binding or held-harmless.
- Average-income test (LIHTC) set design logic.
