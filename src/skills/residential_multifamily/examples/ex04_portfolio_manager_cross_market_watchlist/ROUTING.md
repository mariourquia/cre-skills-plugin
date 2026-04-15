# Example 04 — ROUTING

## Matched rules

- Fallback-rank match: no specific portfolio-manager rule exists; closest match is `r002_asset_manager_monthly_review` (role-adjacent) and `r009_direct_workflow` with `workflow=quarterly_portfolio_review` OR ad-hoc portfolio watchlist.
- The request is sub-quarterly (weekly cadence), so the router treats it as a direct-workflow call with `role=portfolio_manager`.

## Axis resolution

| Axis | Resolved to | Source |
|---|---|---|
| `asset_class` | `residential_multifamily` | default |
| `segment` | `middle_market` | portfolio scope asserted |
| `form_factor` | mixed — not pinned | portfolio-level roll-up |
| `lifecycle_stage` | `stabilized` (with `renovation` sub-list) | portfolio mix |
| `management_mode` | mixed (`self_managed` + `third_party_managed`) | portfolio mix |
| `role` | `portfolio_manager` | session context |
| `workflow` | `quarterly_portfolio_review` (adapted to weekly cadence) | inferred |
| `market` | all 6 markets in-scope | portfolio scope |
| `output_type` | `dashboard` + `memo` | request text |
| `decision_severity` | `recommendation` | review only |
| `org_id` | `examples_org` | session |

## Packs loaded

- Role pack: `roles/portfolio_manager/` (primary).
- Workflow pack: `workflows/quarterly_portfolio_review/` (adapted for weekly watchlist ask).
- Segment overlay: `overlays/segments/middle_market/`.
- Lifecycle overlay: `overlays/lifecycle/stabilized/` (plus `overlays/lifecycle/renovation/` for Greenbriar).
- Management-mode overlays: `overlays/management_mode/self_managed/` + `overlays/management_mode/third_party_managed/` + `overlays/management_mode/owner_oversight/` (loaded owner-side because portfolio includes TPM-managed assets).
- Org overlay: `overlays/org/examples_org/`.

## References loaded

| Path | Category | as-of | Status |
|---|---|---|---|
| `reference/normalized/market_rents__charlotte_mf.csv` | market_rent_benchmark | 2026-03-31 | sample |
| `reference/normalized/market_rents__nashville_mf.csv` | market_rent_benchmark | 2026-03-31 | sample |
| `reference/normalized/market_rents__dallas_mf.csv` | market_rent_benchmark | 2026-03-31 | sample |
| `reference/normalized/market_rents__phoenix_mf.csv` | market_rent_benchmark | 2026-03-31 | sample |
| `reference/normalized/market_rents__atlanta_mf.csv` | market_rent_benchmark | 2026-03-31 | sample |
| `reference/normalized/market_rents__tampa_mf.csv` | market_rent_benchmark | 2026-03-31 | sample |
| `reference/normalized/concession_benchmarks__*.csv` | concession_benchmark | 2026-03-31 | sample |
| `reference/normalized/occupancy_benchmarks__*.csv` | occupancy_benchmark | 2026-03-31 | sample |
| `reference/derived/role_kpi_targets.csv` | occupancy_benchmark | 2026-01-15 | starter |

## Metrics engaged

- Portfolio: `same_store_noi_growth`, `occupancy_by_market`, `delinquency_by_market`, `portfolio_concentration_market`, `asset_watchlist_score`, `budget_attainment`.
- Property-roll-up: weighted `physical_occupancy`, weighted `economic_occupancy`, weighted `delinquency_rate_30plus`, weighted `blended_lease_trade_out`.
- Context: `notice_exposure` (rollover risk), `turnover_rate`.

## Gates

- None opened by the watchlist itself.
- Property-level escalations may open gated actions (row 1/2 at the property level) — those live in each asset's own workflow.

## Templates selected

- `templates/quarterly_portfolio/quarterly_portfolio_review_outline.md` (backbone, trimmed for weekly cadence).
- `templates/quarterly_portfolio/quarterly_market_cycle_snapshot.md` (cycle read).
- `templates/executive/executive_weekly_operating_summary.md` (for cross-ref).

## Output shape

- One-paragraph portfolio headline.
- Weighted portfolio KPI table with trend.
- Market heat map with driver narrative.
- Watchlist table: property, market, status, drivers, corrective actions, exit criteria.
- Concentration read: is weakness one-market or portfolio-wide?
- Action list for next week with owner and gates where applicable.
