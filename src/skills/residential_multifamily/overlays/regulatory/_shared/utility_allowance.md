# Utility Allowance

Status: stub. Placeholder for the utility-allowance (UA) schedule
concept used to split gross rent between tenant-paid and owner-paid
utilities.

## Concept

Utility allowance schedules publish the imputed cost a resident bears for
utilities paid directly to a provider (electricity, gas, water / sewer,
trash, etc.). The schedule is subtracted from the gross-rent limit to
derive the maximum rent the owner can charge as tenant portion. Schedules
are published by a PHA (for voucher / HAP programs), by HUD (for some
HUD-insured programs), by the state HFA (for LIHTC), or by the owner
following a program-approved methodology (utility-company method, HUD
methodology, or energy-consumption model). Refresh cadence is typically
annual but varies.

## Target keys the overlay will populate

- Interacts with `rent_limits.md` to derive the allowable tenant portion.
- `reporting_emphasis` -> adds UA-reconciliation status and publisher-lag
  tracking.
- Adds:
  - `utility_allowance_schedule`
  - `ua_reconciliation_status`
  - `ua_publisher_lag_days`

## Schedule structure

Each row in `reference/normalized/utility_allowance__{program}__{market}.csv`:

- program
- publisher (pha_id or hud or state_hfa or owner_methodology)
- bedroom_count
- utility_component (electricity / gas / water_sewer / trash / other)
- effective_start, effective_end
- amount (numeric, lives in reference, not here)

## Publisher and refresh cadence

- PHA schedule: published by the local public housing agency; typically
  updated annually.
- HUD: published centrally; updated on program calendar.
- State HFA: typically updates LIHTC UA annually.
- Owner methodology: owner re-runs on a program-specified cadence and
  submits to the agency.

The overlay tracks publisher-lag: days since the most recent UA update
was ingested. Stale UA drives a compliance-calendar alert.

## Mapping to utility_benchmark reference

Tenant-paid utilities on the UA schedule are reconciled against the
property's actual utility cost benchmarks in `reference/normalized/
utility_benchmark.csv`. Large deviations trigger a methodology review.

## Phase 1 does not implement

- Populated UA tables.
- Publisher-lag SLA bands.
- Methodology-switch workflow.
