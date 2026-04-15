# Example 05 — INPUT

## User prompt

> "Pull my weekly operating summary across the middle-market portfolio. I want a one-paragraph headline, the weighted KPIs vs. band, the top 5 items needing executive attention, and any cross-market themes. I'm presenting to the board risk committee Monday."

## Session context

- asker.role: `coo_operations_leader`
- asker.org_id: `examples_org`
- Portfolio scope: middle-market book (27 properties, 6 markets).
- Cadence: standing weekly executive operating summary. Board risk committee on Monday adds attention to escalation-ready items.

## Known rolled-up data points (from the portfolio-manager and AM feeds this week)

- Weighted `physical_occupancy`: 93.2%.
- Weighted `leased_occupancy`: 95.1%.
- Weighted `delinquency_rate_30plus`: 4.8%.
- Weighted `blended_lease_trade_out` (MTD): +1.8%.
- Portfolio `budget_attainment` (MTD): 97.1%.
- Watchlist: 4 amber (Liberty, The Standard, Park 412, Magnolia Oaks); 1 renovation-track watch (Greenbriar).
- Open executive items this week: Greenbriar flooring CO (Option B, major tier, pending approval); Liberty watchlist recovery; Nashville concentration risk; two Atlanta delinquency audits in progress; an off-cycle refi candidate review (Atlanta, Park 412) scheduled for next month.

## Reference availability

- All property and market references loaded per prior examples; everything stamped as-of 2026-03-31 for market refs and 2026-01-15 for KPI targets; all sample / starter.

## Decision / autonomy context

- decision_severity expected: `recommendation`.
- No gated actions open directly from this summary. The Greenbriar CO and any refi candidate progression carry their own gates.
- If a `final` board-submission version is requested, it routes per approval matrix.
