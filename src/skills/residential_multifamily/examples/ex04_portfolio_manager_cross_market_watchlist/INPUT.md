# Example 04 — INPUT

## User prompt

> "I need a cross-market watchlist for the middle-market book. Which assets are weakest and why. I want to know if this is portfolio-wide or concentrated in one or two markets. Give me exit criteria per asset and the action list for next week."

## Session context

- asker.role: `portfolio_manager`
- asker.org_id: `examples_org`
- Portfolio scope: "middle_market book" — 27 properties across 6 markets.
- Market exposure (units): Charlotte 28%, Nashville 22%, Dallas 18%, Phoenix 14%, Atlanta 12%, Tampa 6%.
- Reporting cadence: weekly portfolio watchlist (this request is ad-hoc inside the weekly rhythm).

## Known data points (roll-up)

- Weighted `physical_occupancy`: 93.2% (target: band).
- Weighted `delinquency_rate_30plus`: 4.8% (target: band).
- Weighted `blended_lease_trade_out` (MTD): +1.8% (target: band).
- Portfolio `budget_attainment`: 97.1% (target: band).
- `same_store_noi_growth` (T12): +2.3%.
- Market heat map (from prior week): Charlotte green, Nashville amber (attainment slipping), Dallas green, Phoenix green, Atlanta amber (delinquency drifting), Tampa green.

## Current watchlist (prior week)

- Liberty Apartments (Nashville) — amber, 2 months attainment below band.
- Park 412 (Atlanta) — amber, delinquency above band T30.
- Greenbriar (Phoenix) — green but under renovation (separate review track).

## Reference availability snapshot

- `reference/normalized/market_rents__*.csv` for each market — present, status: sample, as_of 2026-03-31.
- `reference/normalized/concession_benchmarks__*.csv` for each market — present, status: sample, as_of 2026-03-31.
- `reference/normalized/occupancy_benchmarks__*.csv` for each market — present, status: sample, as_of 2026-03-31.
- `reference/derived/role_kpi_targets.csv` — present, status: starter, as_of 2026-01-15.

## Decision / autonomy context

- decision_severity expected: `recommendation`.
- No gated actions directly opened by this review.
- Outcome may prompt gated actions at the property level (e.g., delinquency escalation, pricing changes) — those route through their own workflows.
