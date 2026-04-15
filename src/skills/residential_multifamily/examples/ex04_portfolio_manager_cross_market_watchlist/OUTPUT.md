# Example 04 — OUTPUT

## Cross-Market Watchlist — Middle-Market Book (27 properties)

**Prepared by.** Portfolio Manager (`roles/portfolio_manager`) via `workflows/quarterly_portfolio_review` adapted for weekly cadence.
**Week ending.** 2026-04-12

## Confidence banner

- Market rent / concession / occupancy benchmarks across 6 markets as-of: 2026-03-31 (status: sample)
- Role KPI targets as-of: 2026-01-15 (status: starter)
- Org overlay (examples_org) active.

## Headline

Portfolio is still inside band on all four weighted headline KPIs, but weakness is concentrated in Nashville (attainment slipping at two assets) and Atlanta (delinquency drift at two assets). Phoenix carries a renovation that is on track on operating metrics but flagged separately for trade-buyout variance on flooring (see Example 03). This is not yet a portfolio-wide problem; it is a two-market concentration with two specific properties pulling each market.

## Portfolio weighted KPIs

| Metric | This week | Prior week | 4-week trend | Target band |
|---|---|---|---|---|
| Weighted `physical_occupancy` | 93.2% | 93.4% | flat | in band |
| Weighted `economic_occupancy` | 89.7% | 89.9% | flat | in band |
| Weighted `delinquency_rate_30plus` | 4.8% | 4.6% | worsening | top of band |
| Weighted `blended_lease_trade_out` (MTD) | +1.8% | +1.9% | flat | in band |
| Portfolio `budget_attainment` | 97.1% | 97.3% | flat | bottom of band |
| `same_store_noi_growth` T12 | +2.3% | +2.3% | stable | in band |

## Market heat map

| Market | Units weight | Occ. weighted | Delinq. weighted | Trade-out | Heat | Driver narrative |
|---|---|---|---|---|---|---|
| Charlotte | 28% | above band | below band | above band | green | Ashford Park (see Example 01) is an exception; balance of portfolio healthy. |
| Nashville | 22% | below band | near top of band | below band | amber | Liberty Apartments and The Standard both slipping on attainment; concessions creeping vs. Nashville comp reference. |
| Dallas | 18% | above band | below band | above band | green | Strongest market this quarter. |
| Phoenix | 14% | in band | in band | in band | green | Greenbriar in renovation; no operating read flags. |
| Atlanta | 12% | in band | above top of band | in band | amber | Park 412 and Magnolia Oaks both drifting on 30+; playbook execution inconsistent. |
| Tampa | 6% | above band | in band | above band | green | Small footprint, no issues. |

## Watchlist (this week)

| Property | Market | Status | Weeks on | Drivers | Corrective actions | Exit criteria |
|---|---|---|---|---|---|---|
| Liberty Apartments | Nashville | amber | 3 | Budget attainment below band 2 consecutive months; delinquency above band | Variance commentary discipline with TPM; delinquency playbook re-execution | 2 consecutive months attainment at/above band AND delinquency back in band |
| The Standard | Nashville | new this week (amber) | 1 | Occupancy 150 bps below band; concessions rising | Re-price vs. Nashville comps; run `market_rent_refresh` | Occupancy in band for 4 consecutive weeks |
| Park 412 | Atlanta | amber | 2 | Delinquency 110 bps above band; Day 6-15 stage lag | Playbook re-training at site; TPM approval-response-time tighter | Delinquency in band for 4 consecutive weeks |
| Magnolia Oaks | Atlanta | amber | 2 | Delinquency drifting; payment plan compliance down | PM + Regional joint delinquency review; vendor-of-record for collections | Plan compliance >=90% for 4 weeks AND delinquency in band |
| Greenbriar | Phoenix | watch (non-op) | — | Trade-buyout variance on flooring (renovation project, separate track) | Resolution path in Example 03 | CO resolved + contingency burn <1.0 vs % complete |

No additions; no removals this week. Liberty Apartments remains the closest to formal "on watchlist with quarterly recovery plan" status if next month does not recover.

## Concentration read

- Nashville is overweight relative to the portfolio on weakness this week: 22% units, but 2 of 5 amber / watch properties. If concessions continue to creep in Nashville, this becomes a market read, not a property read, and calls for market-wide pricing and retention adjustment.
- Atlanta's weakness is delinquency-specific, not pricing or demand. Playbook-execution driven. Correctable.
- Dallas, Charlotte, Phoenix, Tampa are not dragging the portfolio.

## Cycle context

- Nashville comp reference (sample) shows concessions rising 25 bps MoM and deliveries elevated in The Gulch; consistent with Liberty's economic occupancy slip.
- Atlanta comp reference (sample) shows concessions flat, rents modestly positive — Atlanta weakness is operating-execution, not market-cycle.
- Other markets: comp reference stable; no cycle read suggests portfolio-wide action this week.

## Action list for next week

| # | Action | Owner | Due | Gate |
|---|---|---|---|---|
| 1 | Drive Nashville pricing and retention refresh (The Standard + Liberty) | AM (Nashville book) | 2026-04-19 | none |
| 2 | Run `market_rent_refresh` workflow in Nashville | Regional | 2026-04-19 | none |
| 3 | Joint delinquency playbook audit at Park 412 + Magnolia Oaks | AM (Atlanta book) + TPM | 2026-04-17 | none; property-level escalations may open row 1 / 2 |
| 4 | Add The Standard to watchlist formally if this week's pricing actions don't lift leased occupancy | PM | End of week | none |
| 5 | Brief COO in weekly operating summary on Nashville concentration risk | Portfolio Manager | 2026-04-15 | none |
| 6 | Track Greenbriar CO resolution (cross-ref Example 03) | CM + AM | 2026-04-18 | row 11 pending |

## Confidence

Medium-high on property-level reads (weekly operating data). Medium on market cycle read (comp references are sample-tagged). Low-confidence on any cross-market pricing conclusion until market_rent_refresh is complete in Nashville.

---

*Output status: starter. No `final` external submission is generated here; this is an internal portfolio review.*
