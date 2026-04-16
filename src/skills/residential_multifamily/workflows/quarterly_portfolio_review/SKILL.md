---
name: Quarterly Portfolio Review
slug: quarterly_portfolio_review
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Market trend references, concentration thresholds, benchmark sets, watchlist scoring
  weights, and fund-level target returns drift. Every trend statement cites a reference.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [stabilized, renovation, lease_up, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [asset_manager, portfolio_manager, coo_operations_leader, cfo_finance_leader, ceo_executive_leader]
  output_types: [operating_review, kpi_review, memo, dashboard]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/derived/role_kpi_targets.csv
    - reference/normalized/occupancy_benchmarks__{market}_mf.csv
    - reference/normalized/collections_benchmarks__{region}_mf.csv
    - reference/normalized/watchlist_scoring.yaml
    - reference/derived/same_store_set__{org}.yaml
    - reference/normalized/approval_threshold_defaults.csv
  writes: []
metrics_used:
  - same_store_noi_growth
  - occupancy_by_market
  - delinquency_by_market
  - turn_cost_by_market
  - portfolio_concentration_market
  - asset_watchlist_score
  - budget_attainment
  - forecast_accuracy
  - noi
  - noi_margin
  - dscr
  - debt_yield
  - blended_lease_trade_out
  - capex_spend_vs_plan
  - renovation_yield_on_cost
  - stabilization_pace_vs_plan
escalation_paths:
  - kind: portfolio_risk_concentration
    to: portfolio_manager -> executive
  - kind: fund_covenant_breach_risk
    to: portfolio_manager -> cfo_finance_leader
  - kind: board_submission
    to: executive + finance/reporting lead -> approval_request(row 16)
approvals_required:
  - board_final_submission
  - investor_quarterly_final_submission
description: |
  Portfolio-level quarterly review covering same-store trend, market concentration,
  watchlist distribution, capex progress, lease-up status, forecast discipline, covenant
  posture, and fund-level context. Produces the board and investor narrative drafts.
---

# Quarterly Portfolio Review

## Workflow purpose

Roll the monthly AM outputs into a quarterly portfolio view. Narrative, not transactional. Provides the portfolio_manager, COO, CFO, and CEO with a view of trend, concentration, risk, and the board / investor story for the quarter.

## Trigger conditions

- **Explicit:** "quarterly portfolio review", "Q2 portfolio pack", "board packet", "LP quarterly".
- **Implicit:** quarter close; fund calendar; watchlist distribution shift; concentration threshold crossed.
- **Recurring:** quarterly.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| AM reviews (3 months) | packs | required | from `workflows/monthly_asset_management_review` |
| Same-store set definition | yaml | required | frozen per quarter |
| Market references | csv | required | trend views |
| Watchlist scoring | yaml | required | |
| Fund-level debt schedule | yaml | required | for fund covenant view |
| Investor report template | md | required | overlay-driven |
| Board packet template | md | required | overlay-driven |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Portfolio KPI dashboard | `dashboard` | same-store, market, watchlist, covenant |
| Trend narrative | `memo` | quarter over quarter, year over year |
| Concentration review | `memo` | market, segment, vintage |
| Watchlist movers | `kpi_review` | top movers up / down |
| Capex program summary | `kpi_review` | portfolio `capex_spend_vs_plan`, `renovation_yield_on_cost` |
| Board packet draft | `operating_review` | |
| Investor / LP draft | `memo` | |

## Output contract

Final-marked output MUST follow `_core/executive_output_contract.md`:
verdict-first block (recommendation, 3-bullet rationale, confidence,
materiality, next action), source-class labels on every numeric cell
(`[operator]` / `[derived]` / `[benchmark]` / `[overlay]` /
`[placeholder]`), and refusal-artifact shape when a required reference
is absent. Period-seal gate: `required_period_seal.minimum_close_status
= hard_close` (see `reference_manifest.yaml`); this workflow refuses
if close_status is soft or draft at run time.

## Required context

Asset_class, segment, market concentration, loan context.

## Process

1. **Inherit AM outputs.** Roll 3 months of AM reviews. Flag any missing.
2. **Same-store trend.** `same_store_noi_growth` quarter and trailing 4 quarters.
3. **Concentration.** `portfolio_concentration_market`; segment and vintage concentration.
4. **Watchlist distribution.** Count by color and movers; top risk drivers.
5. **Covenant posture (fund-level).** DSCR / DY cushion across loans; any breach runway?
6. **Capex.** Portfolio `capex_spend_vs_plan`; program-level `renovation_yield_on_cost`.
7. **Lease-up status.** Any asset still in lease-up; `stabilization_pace_vs_plan`.
8. **Forecast discipline.** Portfolio `forecast_accuracy`; systematic bias review.
9. **Market trend commentary.** Pull from `workflows/market_rent_refresh` outputs where available.
10. **Board and investor drafts.** Compose per overlay templates; open `approval_request` rows 15 / 16 for final submissions.
11. **Confidence banner.** All references surfaced with `as_of_date` and `status`.

## Metrics used

See frontmatter.

## Reference files used

- `reference/derived/role_kpi_targets.csv`
- `reference/normalized/occupancy_benchmarks__{market}_mf.csv`
- `reference/normalized/collections_benchmarks__{region}_mf.csv`
- `reference/normalized/watchlist_scoring.yaml`
- `reference/derived/same_store_set__{org}.yaml`
- `reference/normalized/approval_threshold_defaults.csv`

## Escalation points

- Portfolio concentration above threshold -> portfolio_manager -> executive.
- Fund-level covenant breach risk -> CFO.
- Board submission -> row 16.

## Required approvals

- Board final submission (row 16).
- Investor / LP quarterly final submission (row 15).

## Failure modes

1. Quarterly narrative without citing trend references. Fix: every trend statement cites the source.
2. Same-store set shifting quarter to quarter without note. Fix: same-store set versioned and frozen; any change logged.
3. Board packet without approval. Fix: row 16 gate.
4. Watchlist distribution without drivers. Fix: top risk drivers in every watchlist section.

## Edge cases

- **Fund mid-capital-raise:** context note on capital deployment pace; does not alter operating narrative.
- **Recent acquisition or disposition:** same-store treatment per overlay; explicit exclusion note.
- **Fund nearing harvest:** disposition sensitivity view; pairs with `workflows/capital_project_intake_and_prioritization` for any late-cycle capex.
- **Debt maturity wave in coming 12 months:** refi runway table.

## Example invocations

1. "Run the Q2 2026 portfolio review; include watchlist movers and concentration."
2. "Build the LP quarterly packet for the core fund."
3. "Board packet for the residential portfolio, Q1 2026."

## Example outputs

### Output — Portfolio review (abridged, Q1 2026)

**Same-store NOI growth.** Within overlay band trailing 4 quarters.

**Concentration.** Charlotte weight within overlay threshold; other markets diversified per fund mandate.

**Watchlist.** Distribution by color; movers detailed with top drivers.

**Covenant posture.** Fund-level cushion adequate across loans; one loan on refi runway.

**Capex program.** Portfolio `capex_spend_vs_plan` within band; `renovation_yield_on_cost` at or above underwriting.

**Lease-up.** One asset in lease-up; `stabilization_pace_vs_plan` within band.

**Forecast discipline.** Portfolio `forecast_accuracy` within overlay band; no systematic bias flagged.

**Board / LP.** Draft prepared; `approval_request` row 15 and row 16 queued.

**Confidence banner.** References cited with `as_of_date` and `status`.
