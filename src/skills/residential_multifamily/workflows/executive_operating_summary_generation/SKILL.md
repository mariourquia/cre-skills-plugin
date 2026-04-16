---
name: Executive Operating Summary Generation
slug: executive_operating_summary_generation
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Executive-level thresholds, board-packet templates, LP narrative tone, lender submission
  formats, and investor-report layouts live in overlays. No financial thresholds, time
  windows, or target bands live in skill prose.
applies_to:
  segment: [middle_market, affordable, luxury]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise, high_rise]
  lifecycle: [stabilized, renovation, lease_up, recap_support, development, construction]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [coo_operations_leader, cfo_finance_leader, ceo_executive_leader, portfolio_manager, asset_manager, reporting_finance_ops_lead]
  output_types: [operating_review, memo, dashboard, kpi_review]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/derived/role_kpi_targets.csv
    - reference/normalized/watchlist_scoring.yaml
    - reference/derived/same_store_set__{org}.yaml
    - reference/normalized/board_packet_template__{org}.md
    - reference/normalized/investor_report_template__{org}.md
    - reference/normalized/lender_report_template__{loan}.md
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
  - revenue_variance_to_budget
  - expense_variance_to_budget
escalation_paths:
  - kind: board_submission
    to: executive + finance/reporting lead -> approval_request(row 16)
  - kind: investor_submission
    to: asset_manager or portfolio_manager + executive -> approval_request(row 15)
  - kind: lender_submission
    to: asset_manager + finance/reporting lead -> approval_request(row 14)
  - kind: material_risk_signal
    to: executive review (risk, covenant, watchlist)
approvals_required:
  - board_final_submission
  - investor_final_submission
  - lender_final_submission
description: |
  Composes executive-grade operating summaries for board, LP, lender, and internal
  executive consumption. Synthesizes property, asset, and portfolio outputs into a
  narrative-first document with attached KPI dashboard, covenant posture, watchlist
  distribution, capex program, lease-up status, and forecast discipline. Every final
  submission is gated. Never sends autonomously.
---

# Executive Operating Summary Generation

## Workflow purpose

Produce the executive layer's operating summary: the document that leaves the operator-owner and goes to a board, an LP, a lender, or an internal executive audience. The summary is narrative-first, grounded in cited metrics, and carries the confidence and audit posture required at the top of the pyramid.

This pack is flagship-depth. It is the last stop before any final-marked submission leaves the org. Approval rows 14 (lender), 15 (investor), and 16 (board) live here. The workflow never sends and never signs.

## Trigger conditions

- **Explicit:** "build the board pack", "LP quarterly narrative", "lender annual summary", "executive operating summary", "CEO one-pager".
- **Implicit:** board / LP / lender calendar; material risk signal requiring executive review; fund event (capital call, distribution, reporting deadline); month- or quarter-close with executive deliverable due.
- **Recurring:** monthly executive internal summary; quarterly LP and board; per lender calendar.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| AM reviews (month or quarter) | packs | required | from `workflows/monthly_asset_management_review` |
| Portfolio review (quarterly) | pack | required | from `workflows/quarterly_portfolio_review` if quarterly |
| Same-store set definition | yaml | required | versioned |
| Watchlist scoring | yaml | required | distribution + movers |
| Fund and loan-level debt schedule | yaml | required | covenants |
| Capex program summary | table | required | portfolio level |
| Board / investor / lender template | md | required | overlay-driven |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Narrative summary | `memo` | 1-3 pages, cited metrics |
| KPI dashboard | `dashboard` | 1 page |
| Covenant posture | `kpi_review` | loan-by-loan cushion |
| Watchlist distribution | `kpi_review` | movers + top drivers |
| Capex program summary | `kpi_review` | portfolio `capex_spend_vs_plan`, `renovation_yield_on_cost` |
| Draft submission package | bundle | board / LP / lender |
| Approval request bundle | list | rows 14 / 15 / 16 |
| Confidence banner | banner | all references surfaced |

## Output contract

Final-marked output MUST follow `_core/executive_output_contract.md`:
verdict-first block (recommendation, 3-bullet rationale, confidence,
materiality, next action), source-class labels on every numeric cell
(`[operator]` / `[derived]` / `[benchmark]` / `[overlay]` /
`[placeholder]`), and refusal-artifact shape when a required reference
input is absent. See the worked example at
`examples/ex01_executive_operating_summary_generation.md` for the
canonical structure. Any `[placeholder]`-tagged cell blocks the
approval-request bundle (rows 14 / 15 / 16).

## Required context

Asset_class, segment, audience (board / LP / lender / internal), org, period. Audience governs template and approval row.

## Process

### Step 1. Audience resolution.

Decide the audience; load the overlay template. Audience determines tone, depth, required disclosures, and approval row.

### Step 2. Inherit layered outputs.

From AM and portfolio workflows. Do not recompute. If the period requires a quarterly portfolio view and one is not closed, refuse to compose until closed.

### Step 3. Narrative synthesis.

Compose narrative anchored to cited metrics. Structure per overlay template (typical: headline, operating performance, capital / capex, portfolio posture, risk, forward view).

- Reference every claim to a metric slug.
- Surface variance drivers.
- Cite references with `as_of_date` and `status`.
- Do not assert improvement or deterioration without a trend window.

### Step 4. KPI dashboard compose.

Per template: same-store, market, watchlist, covenant, capex, lease-up, forecast accuracy.

### Step 5. Covenant posture.

Loan-by-loan cushion view; trend trailing 3 and 6 months; any runway flag lit.

### Step 6. Watchlist posture.

Distribution by color; top movers with drivers; any red asset has an explicit ownership-side plan.

### Step 7. Capex and renovation program.

Portfolio-level `capex_spend_vs_plan`; `renovation_yield_on_cost` per program; any program off-plan has a plan reference.

### Step 8. Lease-up status.

Any asset in lease-up; `stabilization_pace_vs_plan`.

### Step 9. Forecast discipline.

Portfolio `forecast_accuracy`; bias direction if any; calibration commitment to next cycle.

### Step 10. Risk surface-up.

Any fair-housing flag, compliance finding, safety pattern, regulatory exposure, or LP / lender relationship risk surfaced clearly (but without confidential detail in external packets; counsel leads sensitive disclosures).

### Step 11. Forward view.

Overlay-defined horizon (3 / 6 / 12 months). What the org is watching, what could change, what decisions are coming up.

### Step 12. Draft package assembly.

Board: board packet template. LP: investor narrative + financial statements + distribution commentary. Lender: compliance certificate + NOI normalization + covenant tests + narrative. Internal executive: condensed one-pager with dashboard.

### Step 13. Approval routing.

- Row 14 for lender submissions.
- Row 15 for investor / LP submissions.
- Row 16 for board submissions.
- Internal executive summaries are `draft_for_review` but not always gated; overlay governs.
- The workflow never releases a submission marked `final` without an approved row.

### Step 14. Fair-housing / compliance echo.

Any child-workflow fair-housing flag surfaced. Detail is counsel-led; workflow does not author public-facing FHA / compliance language.

### Step 15. Confidence banner.

Every reference cited with `as_of_date` and `status`. Board and LP packets carry a prominent confidence section with source freshness notes.

## Metrics used

See frontmatter. Full executive metric set.

## Reference files used

- `reference/derived/role_kpi_targets.csv`
- `reference/normalized/watchlist_scoring.yaml`
- `reference/derived/same_store_set__{org}.yaml`
- `reference/normalized/board_packet_template__{org}.md`
- `reference/normalized/investor_report_template__{org}.md`
- `reference/normalized/lender_report_template__{loan}.md`
- `reference/normalized/approval_threshold_defaults.csv`

## Escalation points

- Board submission: row 16.
- Investor submission: row 15.
- Lender submission: row 14.
- Material risk signal: executive review (operational).
- FHA / compliance disclosure exposure: counsel leads; row 3 if public-facing response needed.

## Required approvals

- Row 14 (lender final).
- Row 15 (investor / LP final).
- Row 16 (board final).
- Any action explicitly flagged `human_approval_required` by overlay.

## Failure modes

1. Narrative without cited metrics. Fix: every claim anchored to a slug.
2. Using sample data as operating fact in an external packet. Fix: confidence banner surfaces; overlay may refuse external use of sample data.
3. Authoring FHA / compliance disclosures without counsel. Fix: counsel-led; workflow refuses to author public-facing sensitive language.
4. Recomputing property-level KPIs differently than AM review. Fix: consume AM outputs.
5. Sending without approval. Fix: transmission gated.
6. Forward view without horizon. Fix: horizon explicit per overlay.
7. Covenant claim without trend window. Fix: trailing 3 and 6 months required.
8. Watchlist without drivers. Fix: top drivers required.
9. Missing approval row. Fix: row selected from audience.

## Edge cases

- **Dual-audience packet (board + LP):** audience overlays stack; most conservative disclosure; counsel review.
- **Special-situation asset in portfolio (workout, receivership):** separate treatment in narrative; counsel typically involved.
- **Mid-fundraise executive summary:** marketing overlay applies; review for securities-law exposure; counsel-led.
- **Fund anniversary / GP promote calculation context:** separate workflow typically; this pack defers.
- **Property disposed mid-period:** closed-asset treatment; gain / loss per overlay; LP reporting impact.
- **Board member request for ad hoc data (outside calendar):** executive governance overlay governs; ad hoc is not auto-generated.
- **Lender with bespoke format:** loan overlay; no inferred formatting outside overlay.

## Example invocations

1. "Build the Q1 2026 board packet for the residential portfolio."
2. "Compose the LP quarterly narrative for the core fund."
3. "Prepare the monthly internal executive summary for the COO and CFO."

## Example outputs

### Output — Board packet narrative (abridged, Q1 2026)

**Headline.** Portfolio operating within plan; same-store within overlay band; watchlist distribution acceptable; one asset on refi runway.

**Operating performance.** Same-store NOI growth within band; `noi_margin` stable; `blended_lease_trade_out` within band; `economic_occupancy` within band.

**Capital / capex.** Portfolio `capex_spend_vs_plan` within band; `renovation_yield_on_cost` at or above underwriting on completed units.

**Portfolio posture.** Concentration within fund mandate. Watchlist distribution with top two movers explained.

**Risk.** Covenant cushion adequate across loans; one loan on refi runway with plan. No fair-housing or compliance findings this quarter (echoed from child workflows).

**Forward view.** 6-month horizon; watch items enumerated.

**Approvals.** `approval_request` row 16 opened; pending board final submission.

**Confidence banner.** `watchlist_scoring@2026-03-31 (starter)`, `same_store_set@2026-03-31 (starter)`, `board_packet_template@2026-03-31 (starter)`. External-use notation for any sample-tagged reference.

### Output — LP quarterly narrative (abridged)

**Narrative structure.** Headline, operating performance, portfolio posture, capital activity, forward view.

**Cited metrics.** As above.

**Disclosures.** Per overlay and counsel.

**Approvals.** `approval_request` row 15 opened; pending LP final submission.

**Confidence banner.** As above.

### Output — Monthly internal executive summary (abridged)

**One-pager.** Dashboard + three narrative paragraphs (operating, portfolio, watch list).

**Approvals.** Internal; overlay governs whether gated.

**Confidence banner.** References surfaced.
