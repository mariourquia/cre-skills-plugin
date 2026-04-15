# Example 05 — ROUTING

## Matched rule

- `r008_executive` — primary match (role in `[coo_operations_leader, cfo_finance_leader, ceo_executive_leader]`).
- `r009_direct_workflow` — workflow `executive_operating_summary_generation`.

## Axis resolution

| Axis | Resolved to | Source |
|---|---|---|
| `asset_class` | `residential_multifamily` | default |
| `segment` | `middle_market` | portfolio scope |
| `form_factor` | mixed | portfolio |
| `lifecycle_stage` | `stabilized` + `renovation` | portfolio (Greenbriar is the renovation asset) |
| `management_mode` | mixed | portfolio |
| `role` | `coo_operations_leader` | session context |
| `workflow` | `executive_operating_summary_generation` | inferred |
| `market` | all 6 | portfolio |
| `output_type` | `operating_review` (summary form) | request |
| `decision_severity` | `recommendation` | board-read, not `final` external |
| `org_id` | `examples_org` | session |

## Packs loaded

- Role pack: `roles/coo_operations_leader/` (primary).
- Workflow pack: `workflows/executive_operating_summary_generation/` + `workflows/quarterly_portfolio_review/` (for weighted KPI roll-up).
- Segment overlay: `overlays/segments/middle_market/`.
- Lifecycle overlays: `stabilized` + `renovation`.
- Management-mode overlays: all three, because portfolio is mixed and the COO consumes each.
- Org overlay: `overlays/org/examples_org/`.

## References loaded

- Portfolio-manager pack feeds the weighted roll-ups; COO summary cites them rather than recomputing.
- `reference/derived/role_kpi_targets.csv` — as-of 2026-01-15 (status: starter).
- Market benchmarks across all 6 markets — as-of 2026-03-31 (status: sample).
- Org overlay approval matrix — as-of 2026-04-01 (status: approved).

## Metrics engaged

- Weighted `physical_occupancy`, weighted `leased_occupancy`, weighted `delinquency_rate_30plus`, weighted `blended_lease_trade_out`, portfolio `budget_attainment`, `same_store_noi_growth` (contextual).
- Watchlist: `asset_watchlist_score`.
- Development / renovation: `cost_to_complete`, `contingency_remaining`, `trade_buyout_variance`.

## Gates surfaced

- None opened by this summary.
- Existing open approval requests referenced for transparency: Greenbriar flooring CO (row 11), potential future row 20 if a `final` board-submission version is requested.

## Templates selected

- `templates/executive/executive_weekly_operating_summary.md` (primary).
- Cross-references: `quarterly_portfolio_review_outline.md`, `monthly_asset_management_memo.md`, `change_order_review_sheet.md`.

## Output shape

- Short headline paragraph.
- Weighted portfolio KPI table with trend + flag.
- Red / amber / green property heatmap for most-watched assets.
- Top 5 items for executive attention.
- Cross-portfolio themes.
- Capital / development headline.
- Risks and watch-outs.
