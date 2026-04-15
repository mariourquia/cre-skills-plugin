---
name: Monthly Asset Management Review
slug: monthly_asset_management_review
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Asset watchlist scoring weights, covenant cushion bands, same-store set definitions,
  and variance materiality thresholds are overlay-driven. Lender compliance test
  definitions come from per-loan overlays and drift. Every forward-looking number cites
  a source; sample references are surfaced.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [stabilized, renovation, lease_up, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [asset_manager, portfolio_manager, regional_manager, reporting_finance_ops_lead, coo_operations_leader, cfo_finance_leader]
  output_types: [operating_review, kpi_review, memo, dashboard]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/derived/role_kpi_targets.csv
    - reference/normalized/collections_benchmarks__{region}_mf.csv
    - reference/normalized/market_rents__{market}_mf.csv
    - reference/normalized/concession_benchmarks__{market}_mf.csv
    - reference/normalized/occupancy_benchmarks__{market}_mf.csv
    - reference/normalized/watchlist_scoring.yaml
    - reference/normalized/covenant_definitions__{loan}.yaml
    - reference/normalized/approval_threshold_defaults.csv
  writes: []
metrics_used:
  - noi
  - noi_margin
  - dscr
  - debt_yield
  - economic_occupancy
  - physical_occupancy
  - leased_occupancy
  - notice_exposure
  - collections_rate
  - delinquency_rate_30plus
  - bad_debt_rate
  - concession_rate
  - rent_growth_new_lease
  - rent_growth_renewal
  - blended_lease_trade_out
  - market_to_lease_gap
  - loss_to_lease
  - turnover_rate
  - make_ready_days
  - average_days_vacant
  - controllable_opex_per_unit
  - payroll_per_unit
  - rm_per_unit
  - utilities_per_unit
  - revenue_variance_to_budget
  - expense_variance_to_budget
  - budget_attainment
  - forecast_accuracy
  - capex_spend_vs_plan
  - renovation_yield_on_cost
  - stabilization_pace_vs_plan
  - asset_watchlist_score
  - same_store_noi_growth
escalation_paths:
  - kind: covenant_cushion_breach_risk
    to: asset_manager -> portfolio_manager -> cfo_finance_leader
  - kind: material_variance_pattern
    to: asset_manager -> regional_manager -> portfolio_manager
  - kind: watchlist_escalation
    to: asset_manager -> portfolio_manager -> executive
  - kind: capex_plan_deviation
    to: construction_manager -> asset_manager -> approval_request(rows 8-11 per threshold)
  - kind: lender_final_submission
    to: asset_manager -> finance/reporting lead -> approval_request(row 14)
approvals_required:
  - capex_plan_deviation_above_threshold
  - lender_final_submission
  - investor_final_submission
description: |
  Ownership-side monthly review. Synthesizes property-level operating output into asset
  plan reality check: variance to budget and reforecast, covenant view with cushion and
  breach risk, watchlist scoring, rent-growth and trade-out, capex progress and yield,
  stabilization pace for lease-up, same-store rollup. Produces the AM agenda for PM and
  regional conversations, the lender compliance scaffold, and the investor-facing draft.
---

# Monthly Asset Management Review

## Workflow purpose

Turn property-level operating data into ownership-grade insight. At the close of each month, this review produces a property-by-property and portfolio-level view that answers: are we on plan, where is the risk, what is the next decision, and do we have an approval gate coming.

This pack is flagship-depth. It is the layer where `economic_occupancy`, `blended_lease_trade_out`, `controllable_opex_per_unit`, `capex_spend_vs_plan`, `renovation_yield_on_cost`, `stabilization_pace_vs_plan`, `dscr`, `debt_yield`, `forecast_accuracy`, `same_store_noi_growth`, and `asset_watchlist_score` come together. It is also the layer where ownership decisions begin to route: covenant cushion, capex deviations, lender submissions, investor submissions.

## Trigger conditions

- **Explicit:** "monthly AM review", "asset management review for March", "asset plan reality check", "watchlist update", "covenant cushion review", "same-store rollup".
- **Implicit:** month close; AM calendar event; material variance pattern across assets; covenant cushion bar approaching breach per overlay; capex spend above plan materiality; watchlist score crossing band.
- **Recurring:** monthly per asset; portfolio rollup monthly per organization.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Property monthly operating reviews | packs | required | from `workflows/monthly_property_operating_review` |
| T12 and current-month GL | table | required | per asset |
| Reforecast | table | required | from `workflows/reforecast` |
| Approved budget | table | required | anchor |
| Debt schedule + covenant definitions | yaml | required | per loan |
| Capex plan vs. actual | table | required | per asset |
| Renovation program tracker (if applicable) | table | required | for `renovation_yield_on_cost` |
| Lease-up plan (if applicable) | table | required | for `stabilization_pace_vs_plan` |
| Same-store set definition | yaml | required | portfolio overlay |
| Watchlist scoring config | yaml | required | overlay |
| Market references | csv | required | for market-relative context |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Per-asset AM review | `operating_review` | KPIs, variance, covenants, capex, watchlist |
| Portfolio rollup | `kpi_review` | same-store, market concentration, watchlist distribution |
| Covenant view | `kpi_review` | DSCR / DY cushion per loan, breach risk |
| Watchlist scoring table | `dashboard` | per asset, composite score, drivers |
| AM agenda for property | `memo` | talking points with PM and regional |
| Lender compliance scaffold | `memo` | compliance certificate draft if due |
| Investor draft | `memo` | investor-facing narrative if due |
| Approval request bundle | list | capex deviations, lender/investor submissions |

## Required context

Asset_class, segment, form_factor, lifecycle_stage, management_mode, market, loan context (for covenant view). Portfolio-level rollups require same-store set.

## Process

### Step 1. Inherit property-level outputs.

Pull each asset's `workflows/monthly_property_operating_review` result. The AM review does not recompute property-level KPIs; it consumes them. If any property's review is not yet closed, the AM review flags the gap and holds the portfolio rollup until resolved.

### Step 2. Variance lattice.

For each asset and each material line:

- Actuals vs. budget (MTD, YTD).
- Actuals vs. prior reforecast.
- Variance classification: volume (occupancy / collections), price (trade-out / loss-to-lease), mix (unit-type / renovation split), or assumption (tax, insurance, utilities).
- Material variance is overlay-defined (dollar or percent thresholds). Anything above materiality carries a variance explanation; missing explanations flag.

### Step 3. Covenant view (by loan).

For each loan:

- Pull covenant definitions from `reference/normalized/covenant_definitions__{loan}.yaml`.
- Recompute `dscr`, `debt_yield`, LTV per loan definition (follow the lender's NOI and debt-service conventions, not the generic canonical metric unless loan docs match). Use the per-loan overlay for NOI normalizations (e.g., straight-line adjustments, capex reserves, ground rent).
- Compute cushion vs. covenant: current vs. test level, trend over trailing 3 and 6 months.
- Cushion below overlay warning band -> `covenant_cushion_breach_risk` escalation: AM -> PM -> CFO. Runway table produced (when does current trend cross the test line).

If a lender compliance certificate is due (per lender calendar), produce the scaffold and open `approval_request` row 14 for final submission.

### Step 4. Rent-growth and trade-out.

- `rent_growth_new_lease`, `rent_growth_renewal`, `blended_lease_trade_out` by asset and portfolio.
- `market_to_lease_gap` and `loss_to_lease` by asset: where is upside, where is exposure.
- Gap vs. market benchmarks cited with reference `as_of_date` and `status`.
- Signal on properties where `blended_lease_trade_out` is materially below band; route to regional and PM for pricing / retention review via `workflows/renewal_retention`.

### Step 5. Operating discipline.

- `economic_occupancy` trend; drivers decomposed (physical occupancy, concessions, delinquency, bad debt).
- `collections_rate`, `delinquency_rate_30plus`, `bad_debt_rate` reviewed against overlay bands; pre-legal and legal-stage case volume surfaced from `workflows/delinquency_collections`.
- `turnover_rate`, `make_ready_days`, `average_days_vacant` trend.
- Controllable opex per unit: `payroll_per_unit`, `rm_per_unit`, `utilities_per_unit`, `controllable_opex_per_unit`.
- Non-controllable opex: insurance, property tax, management fee; call out known pending renewals or reassessments.

### Step 6. Capex and renovation.

- `capex_spend_vs_plan` per project and per asset.
- Any project with spend trending above plan above overlay materiality opens a deviation view and routes to `workflows/change_order_review` and `workflows/cost_to_complete_review`.
- `renovation_yield_on_cost` vs. underwriting target for each renovation program in play. Below underwriting - overlay threshold opens a program review.
- Capex plan deviation above overlay threshold routes for approval per matrix rows 8-11 depending on dollar.

### Step 7. Lease-up progression.

For any asset in `lifecycle_stage=lease_up`:

- `stabilization_pace_vs_plan` weekly sparkline embedded in monthly pack.
- `leased_occupancy` vs. budgeted lease-up curve; `preleased_occupancy` view.
- Concession posture vs. lease-up overlay.
- Next trigger points: when to step pricing, when to cut concessions, when to claim stabilization per overlay definition.

### Step 8. Forecast discipline.

- `forecast_accuracy` trailing 6 months per asset.
- Systematic bias (e.g., consistently optimistic on other income) flagged.
- Input to the next `workflows/reforecast` cycle; material bias loops back as a calibration item.

### Step 9. Same-store rollup.

- Apply same-store set per overlay definition (owned through both periods; excludes lease-up and recap_support by default).
- Compute `same_store_noi_growth`, same-store `economic_occupancy`, same-store `blended_lease_trade_out`.
- Portfolio trend vs. benchmark and vs. internal target.

### Step 10. Watchlist scoring.

- Apply `reference/normalized/watchlist_scoring.yaml` weights.
- Compute `asset_watchlist_score` per asset. Distribution surfaced; movers from green to yellow or yellow to red detailed.
- Watchlist escalation path: score above overlay threshold for N consecutive months -> asset_manager -> portfolio_manager -> executive review.

### Step 11. AM agenda for each property.

For each asset, produce a short agenda the AM will run with the PM and regional:

- Three to five talking points grounded in the data.
- Open approvals awaiting decisions.
- Known risks (covenant, capex, renovation yield, collections).
- Specific asks (data gaps, policy questions).

### Step 12. Lender and investor submission paths.

- If lender compliance certificate is due, the scaffold is drafted and opens `approval_request` row 14.
- If investor or LP monthly update is due, the narrative is drafted and opens `approval_request` row 15 (asset) or row 16 (board / regulator view).
- All submissions are `draft_for_review`; nothing sends without an approved record.

### Step 13. Fair-housing surface-up.

Any fair-housing flag surfaced in child workflows is surfaced at the AM review. The AM review does not "close" fair-housing flags; it verifies they are on approved-request paths (row 3) and visible to ownership.

### Step 14. Confidence banner.

Every reference cited with `as_of_date` and `status`. Sample or starter references never presented as operating fact without the tag. Stale references (> overlay staleness threshold) marked stale.

## Metrics used

See frontmatter `metrics_used` — the full asset-management family plus relevant operating slugs.

## Reference files used

- `reference/derived/role_kpi_targets.csv`
- `reference/normalized/collections_benchmarks__{region}_mf.csv`
- `reference/normalized/market_rents__{market}_mf.csv`
- `reference/normalized/concession_benchmarks__{market}_mf.csv`
- `reference/normalized/occupancy_benchmarks__{market}_mf.csv`
- `reference/normalized/watchlist_scoring.yaml`
- `reference/normalized/covenant_definitions__{loan}.yaml`
- `reference/normalized/approval_threshold_defaults.csv`
- `reference/derived/same_store_set__{org}.yaml`

## Escalation points

- Covenant cushion approaching breach -> AM -> PM -> CFO.
- Watchlist score escalation -> AM -> PM -> executive.
- Capex plan deviation above materiality -> construction_manager + AM -> approval rows 8-11 per dollar.
- Lender compliance certificate due -> approval row 14.
- Investor or LP submission due -> approval row 15 or 16.
- Fair-housing flag surfaced from children -> verified on row 3 path.
- Material variance pattern across assets -> AM -> PM -> portfolio_manager.

## Required approvals

- Capex plan deviation above threshold (rows 8-11).
- Lender compliance submission (row 14).
- Investor / board submission (rows 15 / 16).
- Any action flagged `human_approval_required` by overlay.

## Failure modes

1. Recomputing property-level KPIs with slightly different defaults than the property review. Fix: AM review consumes property output; it never recomputes property-level.
2. Covenant view using generic metric defaults instead of loan-doc definitions. Fix: covenant view is per-loan overlay-driven.
3. Same-store rollup without freezing the set. Fix: same-store set is an overlay reference, versioned.
4. Watchlist scoring without surfacing drivers. Fix: scoring always reports the top three drivers.
5. Capex deviation not routed for approval. Fix: automatic approval routing by dollar threshold.
6. Silent sample-data usage. Fix: confidence banner.
7. Lender submission without approval. Fix: row 14 gate.
8. Fair-housing flag buried in a property review and not surfaced to ownership. Fix: AM review echoes every child fair-housing flag.

## Edge cases

- **Asset transferred mid-period (acquisition or disposition):** same-store exclusion; variance calc starts at ownership date; operating narrative scoped.
- **Loan maturity within 12 months:** refi runway view embedded; sensitivity to current rate environment.
- **Single-asset portfolio:** portfolio rollup collapses to asset view; same-store rollup suppressed.
- **TPM-managed asset:** child `workflows/third_party_manager_scorecard_review` invoked; TPM performance surfaced alongside asset performance.
- **Property mid-renovation with partial stabilization:** hybrid view; renovation pro-forma vs. classic operating separately; `renovation_yield_on_cost` computed on completed units only.
- **Lender compliance certificate waived (non-event month):** scaffold not produced; runway view still updated.
- **Reforecast behind schedule:** AM review explicitly notes reforecast asof and impact on forward view.

## Example invocations

1. "Run the monthly AM review for the South End portfolio. Include covenant cushion, watchlist, and same-store rollup."
2. "Build the April AM pack for Ashford Park with investor draft."
3. "Watchlist scoring update for the portfolio; call out movers and drivers."

## Example outputs

### Output — Monthly AM review (abridged, Ashford Park, March 2026)

**Headline.** Budget attainment within overlay band. `blended_lease_trade_out` within band. `economic_occupancy` within band. No covenant cushion at risk this month.

**Variance lattice.** Revenue variance within overlay materiality; driver breakdown attached. Expense variance: utilities above materiality (driver: seasonal, pattern-consistent); insurance within band; tax within band pending reassessment.

**Covenant view.** Per-loan `dscr` and `debt_yield` with cushion; trend over trailing 3 and 6 months; no warning band breach.

**Rent-growth and trade-out.** `rent_growth_new_lease`, `rent_growth_renewal` within bands; `blended_lease_trade_out` within overlay; `market_to_lease_gap` modest positive; `loss_to_lease` consistent with prior month.

**Operating discipline.** `collections_rate` within band; `delinquency_rate_30plus` within band; two legal-notice approvals open (verified on row 1 path). `turnover_rate` and `make_ready_days` within band. Controllable opex per unit within band; `utilities_per_unit` elevated per seasonal.

**Capex and renovation.** `capex_spend_vs_plan` within band. Renovation program `renovation_yield_on_cost` at or above underwriting target on completed units.

**Lease-up progression.** N/A (asset is stabilized).

**Forecast discipline.** `forecast_accuracy` trailing 6 months within overlay band; no systematic bias flagged.

**Same-store rollup.** Ashford Park is in the same-store set; contributing to portfolio `same_store_noi_growth` within overlay band.

**Watchlist.** `asset_watchlist_score` green; drivers: covenant cushion, occupancy stability, forecast accuracy.

**AM agenda for PM / regional.** Three talking points enumerated; one approval awaiting decision; one data gap in `market_rents__charlotte_mf.csv` (sample status, override pending); one renewal-retention memo requested via `workflows/renewal_retention`.

**Submissions.** Lender compliance certificate due in 15 days; scaffold drafted; `approval_request` row 14 queued.

**Fair-housing flags echoed.** None this month.

**Confidence banner.** `covenant_definitions__loan_ashford@2026-01-15, status=sample (loan doc overlay pending)`. `watchlist_scoring@2026-03-31, status=starter`. `market_rents__charlotte_mf@2026-03-31, status=sample`. `role_kpi_targets@2026-03-31, status=starter`.

### Output — Portfolio rollup view (abridged, South End portfolio, March 2026)

**Same-store NOI growth.** Within overlay band.

**Market concentration.** Charlotte weight surfaced against overlay threshold.

**Watchlist distribution.** Count by color; movers month over month listed with drivers.

**Covenant posture.** Loan-by-loan cushion summary.

**Capex progress.** Aggregate `capex_spend_vs_plan`; flagged projects.

**Approvals queue.** Open rows 8-11 / 14 / 15 / 16.

**Confidence banner.** All references surfaced with `as_of_date` and `status`.
