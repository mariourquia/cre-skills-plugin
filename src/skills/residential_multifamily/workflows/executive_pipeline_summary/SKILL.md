---
name: Executive Pipeline Summary
slug: executive_pipeline_summary
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Deal pipeline stage semantics, IC calendar, capital-deployment-pace targets,
  JV-partner concentration thresholds, geographic and segment concentration
  thresholds, debt market context, and board-packet templates live in overlays
  and drift. Dealpath stage-to-canonical mapping is the Dealpath adapter
  contract. Procore project-state semantics evolve with the construction-platform
  release cycle. Intacct capex commitment exposure is period-sensitive and
  supersedes prior loads once the period closes. Declined-deal resurrection
  probability is an overlay construct; confidence bands on every metric are
  explicit and sample overlays must be replaced before any output is treated as
  a board-ready commitment.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [development, construction, lease_up, stabilized, renovation, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [executive, ic_members, ceo_executive_leader, coo_operations_leader, cfo_finance_leader, investments_lead, portfolio_manager, asset_mgmt_director, development_lead]
  output_types: [dashboard, memo, operating_review, kpi_review]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/connectors/_core/stack_wave4/source_of_truth_matrix.md
    - reference/connectors/adapters/dealpath_deal_pipeline/normalized_contract.yaml
    - reference/connectors/adapters/dealpath_deal_pipeline/reconciliation_rules.md
    - reference/connectors/adapters/dealpath_deal_pipeline/runbooks/dealpath_common_issues.md
    - reference/connectors/adapters/dealpath_deal_pipeline/dq_rules.yaml
    - reference/connectors/adapters/procore_construction/reconciliation_checks.yaml
    - reference/connectors/adapters/procore_construction/runbooks/procore_common_issues.md
    - reference/connectors/adapters/sage_intacct_gl/reconciliation_rules.md
    - reference/connectors/master_data/asset_crosswalk.yaml
    - reference/connectors/master_data/market_crosswalk.yaml
    - reference/connectors/master_data/dev_project_crosswalk.yaml
    - reference/connectors/master_data/capex_project_crosswalk.yaml
    - reference/normalized/schemas/reconciliation_tolerance_band.yaml
    - reference/normalized/approval_threshold_defaults.csv
    - reference/derived/portfolio_concentration_targets.csv
    - reference/derived/role_kpi_targets.csv
  writes: []
metrics_used:
  - portfolio_concentration_market     # canonical — _core/metrics.md (portfolio_management)
  - asset_watchlist_score              # canonical — inherited context only
  - budget_attainment                  # canonical — inherited context only
  - forecast_accuracy                  # canonical — inherited context only
  - capex_spend_vs_plan                # canonical — inherited context only
  - pipeline_stage_committed_dollars        # proposed: true — sum(deal.deal_size) by Dealpath stage bucket at run date; stage taxonomy per dealpath adapter normalized_contract
  - expected_close_by_month                 # proposed: true — forward-by-month count + dollars of deals with deal.expected_close_date in month N
  - ic_docket_forward_90d                   # proposed: true — count + dollars of deals with deal_milestone.ic_scheduled_date within 90 days
  - capex_commitment_forward_exposure_dollars  # proposed: true — sum(open_commitment.remaining) forward 12 months across Procore active projects; inherited from workflows/development_pipeline_tracking
  - debt_market_context_band                # proposed: true — categorical (tight, neutral, loose) per debt-market overlay; cited, not computed
  - capital_deployment_pace_vs_target       # proposed: true — (capital_deployed_ytd / capital_deployment_target_ytd) per fund overlay
  - declined_deal_hit_rate                  # proposed: true — (declined_deals_that_transacted_elsewhere_within_12mo / total_declined_deals_in_period); backtests IC decision discipline
  - top_of_funnel_sourcing_health           # proposed: true — composite of (new_deals_added_T30, broker_sourced_share, repeat_broker_share, direct_sourced_share) per sourcing overlay
  - jv_partner_concentration                # proposed: true — sum(deal_size) by jv_partner / total_pipeline_dollars; pipeline + owned mix per overlay
  - geographic_concentration_pipeline       # proposed: true — equivalent of portfolio_concentration_market but computed across pipeline_stage_committed_dollars
  - segment_concentration_pipeline          # proposed: true — segment share of pipeline_stage_committed_dollars
  - confidence_band_per_metric              # proposed: true — per-metric (low, medium, high) confidence derived from reference staleness + source posture; board-ready output decoration
escalation_paths:
  - kind: board_submission
    to: executive + cfo_finance_leader + investments_lead -> approval_request(row 16)
  - kind: ic_submission
    to: investments_lead + executive -> approval_request(row 17 if required by overlay; else advisory)
  - kind: capital_deployment_pace_below_target
    to: cfo_finance_leader + investments_lead -> executive
  - kind: concentration_threshold_crossed
    to: portfolio_manager + investments_lead -> executive (market / segment / jv_partner)
  - kind: declined_deal_resurrection
    to: investments_lead -> executive; audit trail required per overlay
  - kind: dq_blocker_from_dealpath
    to: data_platform_team -> investments_lead
  - kind: dq_blocker_from_procore
    to: data_platform_team -> construction_manager + asset_mgmt_director; cite pc_recon_commitment_overdrawn / pc_recon_commitment_vs_posted_spend
  - kind: dealpath_procore_handoff_lag
    to: development_lead -> asset_mgmt_director; cite dp_handoff_dev_lag
approvals_required:
  - board_final_submission
description: |
  Monthly executive rollup of pipeline state for the residential_multifamily
  subsystem. Aggregates Dealpath (deal pipeline), Procore (active development
  pipeline), and Intacct (capex commitment exposure) into a board-ready or
  IC-ready summary. Designed for the executive and IC audiences with
  per-metric confidence bands.

  Scope: dollars committed at each pipeline stage, expected close by month,
  IC docket forward 90 days, capex commitment exposure forward 12 months,
  debt market context band, capital deployment pace vs target, declined deal
  hit-rate, top-of-funnel sourcing health, JV partner concentration,
  geographic concentration, segment concentration. Every metric declares a
  confidence band.

  Decision severity `gated`: the pack is board-ready. Any final-marked
  external submission (board packet, IC advance read) is gated. The workflow
  never sends autonomously; composition of the formal submission bundle lives
  in `workflows/executive_operating_summary_generation`.
---

# Executive Pipeline Summary

## Workflow purpose

Produce the monthly executive-grade pipeline summary: the document that leaves
the investments and development teams and goes to the executive and to the IC.
The pack is a cross-system rollup, synthesizing deal-pipeline posture
(Dealpath), active development pipeline posture (Procore), and posted capex
commitment exposure (Intacct) into a narrative-first board-ready or IC-ready
document.

The pack composes the pipeline layer of the executive story. It sits alongside
`workflows/executive_operating_summary_generation` (operating posture) and
`workflows/quarterly_portfolio_review` (portfolio trend). Together these three
packs cover the three executive narrative arcs: operating, portfolio, pipeline.

This pack is gated. Any final-marked external submission (board packet, IC
advance read, capital-partner memo) requires row 16 (board) or row 17 (IC
advance read, if the overlay requires IC gating) before transmission. The
formal submission bundle composition lives in
`workflows/executive_operating_summary_generation`; this pack stops at the
narrative + dashboard and an opened approval request.

## Trigger conditions

- **Explicit:** "monthly executive pipeline summary", "board pipeline
  summary", "IC docket summary", "capital deployment pace update", "pipeline
  concentration check", "declined deal hit rate report".
- **Implicit:** month close; board calendar approaching; IC calendar approaching
  (forward 90-day docket becomes active); Dealpath stage transition volume
  crosses overlay band; Procore commitment exposure crosses overlay band;
  concentration threshold (market / segment / JV partner) crossed; capital
  deployment pace ytd drifts below target band; material debt-market shift
  flagged.
- **Recurring:** monthly at month close; board-calendar-driven for board
  packet submission; IC-calendar-driven for IC advance-read composition.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Dealpath deal register | table | required | stage in {sourced, loi_signed, psa_signed, ic_approved, debt_term_sheet, close, funded, declined, on_hold} |
| Dealpath deal-milestone log | table | required | per-deal milestone state; ic_scheduled_date, expected_close_date |
| Dealpath IC decision log | table | required | approved, declined, deferred |
| Procore project roster | table | required | all active construction_projects + development_projects |
| Procore commitment register | table | required | open commitments + remaining exposure + retention |
| Intacct capex actuals feed | table | required | posted spend by capex_project dimension |
| Fund capital-deployment plan | yaml | required | per-fund ytd target and forward plan |
| Debt market context overlay | yaml | required | categorical band; update cadence per overlay |
| JV partner register | yaml | required | per-partner pipeline + owned dollar exposure |
| Portfolio concentration targets | csv | required | market / segment / jv partner thresholds |
| Sourcing funnel log | table | required | top-of-funnel additions T30 + broker / repeat-broker / direct flags |
| Declined deal register + outcomes | table | required | declined deals with transacted-elsewhere flag T12m |
| Asset_crosswalk | yaml | required | asset resolution |
| Market_crosswalk | yaml | required | geographic concentration resolution |
| Dev_project_crosswalk | yaml | required | dealpath deal <-> procore project <-> intacct project |
| Capex_project_crosswalk | yaml | required | procore project <-> intacct project |
| Tolerance-band schema | yaml | required | `reconciliation_tolerance_band.yaml` |
| Board packet template | md | conditional | required if audience = board |
| IC advance-read template | md | conditional | required if audience = ic |
| Quarterly portfolio review | pack | optional | for cross-linkage in narrative |
| Executive operating summary | pack | optional | for cross-linkage in narrative |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Pipeline stage rollup | `dashboard` | `pipeline_stage_committed_dollars` (proposed) by stage; counts + dollars |
| Expected close schedule | `kpi_review` | `expected_close_by_month` (proposed) forward 12 months |
| IC docket forward 90 days | `kpi_review` | `ic_docket_forward_90d` (proposed); per-deal row |
| Capex commitment exposure | `kpi_review` | `capex_commitment_forward_exposure_dollars` (proposed) forward 12 months |
| Debt market context | `memo` | `debt_market_context_band` (proposed) + overlay citation |
| Capital deployment pace | `kpi_review` | `capital_deployment_pace_vs_target` (proposed) ytd |
| Declined deal hit rate | `kpi_review` | `declined_deal_hit_rate` (proposed) + cohort detail |
| Top-of-funnel sourcing health | `kpi_review` | `top_of_funnel_sourcing_health` (proposed) composite |
| JV partner concentration | `kpi_review` | `jv_partner_concentration` (proposed) per partner |
| Geographic concentration | `kpi_review` | `geographic_concentration_pipeline` (proposed) + owned context |
| Segment concentration | `kpi_review` | `segment_concentration_pipeline` (proposed) + owned context |
| Confidence bands | appendix | `confidence_band_per_metric` (proposed) — low/medium/high per metric |
| Narrative summary | `memo` | 1-2 pages, cited metrics, top-3 pipeline watch items |
| Draft board packet section | `operating_review` | if audience = board |
| Draft IC advance read | `operating_review` | if audience = ic |
| Approval request | object | row 16 (board) or row 17 (IC) opened on final |
| Confidence banner | banner | reference `as_of_date` + `status` + sample-tag surfacing |

## Output contract

Final-marked output MUST follow `_core/executive_output_contract.md`:
verdict-first block (recommendation, 3-bullet rationale, confidence,
materiality, next action), source-class labels on every numeric cell
(`[operator]` / `[derived]` / `[benchmark]` / `[overlay]` /
`[placeholder]`), and refusal-artifact shape when a required reference
is absent. Any `[placeholder]`-tagged cell blocks board / IC approval
request assembly (rows 16 / 17).

## Required context

Asset_class, segment (one or many), audience (`board`, `ic`, `internal_executive`),
org_id, period (month). Audience governs template and approval row. Fund_id is
required if the pack reports capital-deployment pace at fund grain. Board
calendar date is required if audience is `board`. IC calendar date is required
if audience is `ic`.

## Process

### Step 1. Audience resolution and period anchor

Resolve audience (`board`, `ic`, `internal_executive`). Load the corresponding
template and approval row:

- `board`: row 16, board packet template.
- `ic`: row 17 (if overlay requires IC gating; else advisory), IC advance-read
  template.
- `internal_executive`: advisory; overlay governs whether gated.

Anchor the period (typically prior-month close). Every forward-looking metric
is computed relative to the anchor.

### Step 2. Pipeline stage rollup

Pull the Dealpath deal register (per `dealpath_deal_pipeline/normalized_contract.yaml`
— Dealpath is primary for `deal` and `asset` through close per
`source_of_truth_matrix.md`). Bucket deals by stage:

- `sourced`
- `loi_signed`
- `psa_signed`
- `ic_approved`
- `debt_term_sheet`
- `close`
- `funded`
- `declined`
- `on_hold`

Compute `pipeline_stage_committed_dollars` (proposed) per bucket: sum of
`deal.deal_size` (or whatever canonical field carries dollar commitment,
resolved via the Dealpath adapter contract). Counts + dollars.

If any deal fails the Dealpath DQ check (`dp_completeness_ic_record`,
`dp_handoff_lag`, other), surface as a blocker line in the reconciliation
posture section. Do not silently exclude.

### Step 3. Expected close by month

For every deal with `deal.expected_close_date` populated, bucket by
forward month. Compute `expected_close_by_month` (proposed): forward 12
months, counts + dollars. Annotate any deal whose expected_close_date is in
the past and whose stage is not `close` / `funded` / `declined` —
stage-mapping inconsistency routes to development/investments data hygiene.

### Step 4. IC docket forward 90 days

Pull `deal_milestone.ic_scheduled_date` across open deals within the next 90
days. Compute `ic_docket_forward_90d` (proposed): per-deal row with deal_size,
stage, jv_partner, market, segment, and ic_scheduled_date. Sort by
ic_scheduled_date.

For each deal on the docket, annotate readiness state (per overlay: diligence
complete, debt term sheet status, committee materials ready). Readiness drift
is advisory here; IC-prep orchestration lives in
`workflows/pre_close_deal_tracking` and related packs.

### Step 5. Capex commitment exposure forward 12 months

Pull the Procore commitment register per the active development pipeline.
Compute `capex_commitment_forward_exposure_dollars` (proposed): sum of
`open_commitment.remaining` forward 12 months across all active projects. This
metric is inherited from `workflows/development_pipeline_tracking`; reuse the
computed value rather than recomputing unless the development pipeline tracker
has not run within the overlay-defined freshness window.

For each commitment, check `pc_recon_commitment_overdrawn`. Any overdrawn
commitment is surfaced here as a material blocker in the pipeline-to-posted-spend
reconciliation — route to Procore runbook `commitment_overdrawn`. Do not
propose capex reallocation here; that is
`workflows/cost_to_complete_review` + capex capital overlay.

Cross-system reconciliation posture cited: `pc_recon_commitment_vs_posted_spend`
(Procore vs Intacct), `pc_recon_commitment_overdrawn`, `dp_handoff_dev_lag`
(Dealpath-to-Procore handoff).

### Step 6. Debt market context band

Read `debt_market_context_band` (proposed) from debt-market overlay. This is
a categorical band (`tight`, `neutral`, `loose`), cited not computed. The
overlay carries the update cadence and the reasoning for the current band;
the pack surfaces both.

Forward implications: any band shift changes the close-certainty commentary on
deals in `debt_term_sheet` stage. Annotate the linkage; do not re-underwrite
deals here.

### Step 7. Capital deployment pace vs target

Read fund capital-deployment plan. Compute `capital_deployment_pace_vs_target`
(proposed): (capital_deployed_ytd / capital_deployment_target_ytd) per fund
overlay. capital_deployed_ytd is the sum of equity-call deployments ytd per
the fund's capital overlay; capital_deployment_target_ytd is the fund's ytd
deployment plan frozen at fund start or at the most recent approved plan
amendment.

Flag any fund where `capital_deployment_pace_vs_target` (proposed) is below
the overlay band (typically 0.85 floor) — escalate to cfo_finance_leader +
investments_lead. Do not propose a re-calibration here; that is fund-level
capital overlay.

### Step 8. Declined deal hit rate

Pull declined-deal register for the trailing 12 months. For each declined
deal, check whether the same asset (via `asset_crosswalk`) or substantially
similar asset transacted elsewhere within 12 months. Compute
`declined_deal_hit_rate` (proposed): (declined_deals_that_transacted_elsewhere /
total_declined_deals_in_period).

Attribution categories: priced-out (competitor paid above our underwriting),
diligence-findings (we declined for a discoverable risk), market-timing
(declined pre-market-move), stale-pipeline (declined and not transacted).
Cohort the hit rate by attribution category.

This metric backtests IC decision discipline. Not a proxy for
"should we have bought it" in isolation — overlay commentary governs
interpretation.

### Step 9. Top-of-funnel sourcing health

Compute `top_of_funnel_sourcing_health` (proposed): composite of
(new_deals_added_T30, broker_sourced_share, repeat_broker_share,
direct_sourced_share) from the sourcing funnel log. Compare to sourcing
overlay targets.

Low direct-sourced share or rising share from a small number of repeat
brokers is a concentration signal — route to development_lead for sourcing
coverage review.

### Step 10. JV partner concentration

Compute `jv_partner_concentration` (proposed): per-partner dollar exposure
across pipeline + owned. Compare to `portfolio_concentration_targets.csv`
(partner thresholds) and to the owned-asset JV mix.

Flag any partner whose combined pipeline + owned exposure crosses overlay
threshold — escalate to portfolio_manager + investments_lead.

### Step 11. Geographic and segment concentration

Compute:

- `geographic_concentration_pipeline` (proposed): market share of
  `pipeline_stage_committed_dollars` (proposed).
- `segment_concentration_pipeline` (proposed): segment share of
  `pipeline_stage_committed_dollars` (proposed).

Compare to `portfolio_concentration_targets.csv` and to owned-asset
concentration from `portfolio_concentration_market` (canonical). The narrative
covers both pipeline and owned, so concentration movement across the
pipeline-to-owned bridge surfaces.

Flag any crossing of overlay threshold — escalate to portfolio_manager +
investments_lead.

### Step 12. Confidence bands per metric

For every metric surfaced, compute `confidence_band_per_metric` (proposed):
categorical (low, medium, high) derived from:

- Reference freshness (per `reference_manifest.yaml` `as_of_expectation`).
- Source posture (sample / starter / live per
  `source_of_truth_matrix.md`).
- Cross-system reconciliation status (any blocker fires low confidence).

Confidence bands are prominent on the board-ready output. No metric is
surfaced without its band.

### Step 13. Reconciliation posture summary

Cite and surface the following cross-system reconciliation findings:

- `dp_completeness_ic_record`, `dp_handoff_lag`, `dp_handoff_dev_lag`
  (Dealpath dq + recon).
- `pc_recon_commitment_overdrawn`, `pc_recon_commitment_vs_posted_spend`,
  `pc_recon_co_approved_vs_invoice_posted`, `pc_recon_draw_approved_vs_cash_funded`
  (Procore recon).
- Any Intacct posting lag affecting capex commitment exposure.

Any blocker reduces the affected metric to `low` confidence and surfaces in
the reconciliation memo with runbook pointer.

### Step 14. Narrative synthesis

Compose narrative anchored to cited metrics. Structure per template
(typical: headline, pipeline state, capital deployment, concentration posture,
IC docket, declined-deal discipline, sourcing health, forward view).

- Reference every claim to a metric slug.
- Cite every reference with `as_of_date` and `status`.
- Annotate every metric with its confidence band.
- Surface any concentration, deployment, or declined-deal-resurrection
  signal as an explicit executive decision point — do not bury.

### Step 15. Draft package assembly

- **Board audience:** board packet section draft per overlay template.
- **IC audience:** IC advance-read draft per overlay template.
- **Internal executive audience:** condensed two-page summary.

The pack composes the draft and opens the approval request; it does not send.

### Step 16. Approval routing

- Row 16 (board final) for board audience.
- Row 17 (IC advance-read) for IC audience if overlay requires IC gating.
- Internal executive: advisory; overlay governs whether gated. Usually
  `draft_for_review`.

The workflow never releases a submission marked `final` without an approved
row. Transmission composition lives in
`workflows/executive_operating_summary_generation`.

### Step 17. Confidence banner

Every reference surfaced with `as_of_date` and `status`. Proposed metrics
flagged. Cross-system posture summary: Dealpath primary for deal pipeline;
Procore primary for active development + commitments; Intacct primary for
posted capex spend + capital deployment (where applicable). Per-metric
confidence bands are surfaced prominently; the board-ready output carries a
dedicated confidence section.

### Decision points and branches

- Concentration threshold crossed (market / segment / JV partner): escalate to
  portfolio_manager + investments_lead -> executive.
- Capital deployment pace below target band: escalate to cfo_finance_leader +
  investments_lead.
- Declined deal resurrection pattern: escalate to investments_lead; audit
  trail required per overlay; narrative covers attribution cohort.
- Dealpath DQ blocker: route to data_platform_team -> investments_lead.
- Procore recon blocker (commitment overdrawn): route to
  `workflows/cost_to_complete_review` + Procore runbook; capex commitment
  exposure metric drops to `low` confidence until resolved.
- Dealpath-Procore handoff lag: route to development_lead -> asset_mgmt_director.
- Board audience + final-marked: open `approval_request` row 16 before any
  transmission pathway.
- IC audience + final-marked + overlay requires gating: open
  `approval_request` row 17.

## Metrics used

See frontmatter. The pack primarily introduces pipeline-specific proposed
metrics (`pipeline_stage_committed_dollars`, `expected_close_by_month`,
`ic_docket_forward_90d`, `debt_market_context_band`,
`capital_deployment_pace_vs_target`, `declined_deal_hit_rate`,
`top_of_funnel_sourcing_health`, `jv_partner_concentration`,
`geographic_concentration_pipeline`, `segment_concentration_pipeline`,
`confidence_band_per_metric`). `capex_commitment_forward_exposure_dollars` is
inherited from `workflows/development_pipeline_tracking`. Canonical metrics
(`portfolio_concentration_market`, `asset_watchlist_score`, `budget_attainment`,
`forecast_accuracy`, `capex_spend_vs_plan`) are inherited-context only; not
recomputed here.

## Reference files used

- `reference/connectors/_core/stack_wave4/source_of_truth_matrix.md`
- `reference/connectors/adapters/dealpath_deal_pipeline/normalized_contract.yaml`
- `reference/connectors/adapters/dealpath_deal_pipeline/reconciliation_rules.md`
- `reference/connectors/adapters/dealpath_deal_pipeline/runbooks/dealpath_common_issues.md`
- `reference/connectors/adapters/dealpath_deal_pipeline/dq_rules.yaml`
- `reference/connectors/adapters/procore_construction/reconciliation_checks.yaml`
- `reference/connectors/adapters/procore_construction/runbooks/procore_common_issues.md`
- `reference/connectors/adapters/sage_intacct_gl/reconciliation_rules.md`
- `reference/connectors/master_data/asset_crosswalk.yaml`
- `reference/connectors/master_data/market_crosswalk.yaml`
- `reference/connectors/master_data/dev_project_crosswalk.yaml`
- `reference/connectors/master_data/capex_project_crosswalk.yaml`
- `reference/normalized/schemas/reconciliation_tolerance_band.yaml`
- `reference/normalized/approval_threshold_defaults.csv`
- `reference/derived/portfolio_concentration_targets.csv`
- `reference/derived/role_kpi_targets.csv`

## Escalation points

- Board submission: row 16. Final composition in
  `workflows/executive_operating_summary_generation`.
- IC submission: row 17 if overlay requires IC gating.
- Capital deployment pace below target: cfo_finance_leader + investments_lead
  -> executive.
- Concentration threshold (market / segment / JV partner) crossed:
  portfolio_manager + investments_lead -> executive.
- Declined deal resurrection pattern: investments_lead -> executive.
- Dealpath DQ blocker: data_platform_team -> investments_lead.
- Procore recon blocker (commitment overdrawn): data_platform_team ->
  construction_manager + asset_mgmt_director.
- Dealpath-Procore handoff lag: development_lead -> asset_mgmt_director.

## Required approvals

- Row 16 (board final submission) for board-audience finals.
- Row 17 (IC advance-read) for IC-audience finals where overlay requires
  IC gating.
- Internal executive summaries are advisory; overlay governs. Default is
  `draft_for_review`.
- No autonomous release of any final-marked external document. Transmission
  pathway composition lives in `workflows/executive_operating_summary_generation`.

## Failure modes

1. Reporting pipeline dollars without confidence bands. Fix: every metric
   carries a `confidence_band_per_metric` (proposed); board-ready output
   surfaces the band.
2. Silently excluding deals failing Dealpath DQ. Fix: DQ blockers are cited
   as a blocker line; affected metrics are not silently reduced.
3. Recomputing capex commitment forward exposure. Fix: inherit from
   `workflows/development_pipeline_tracking`; only recompute if the tracker
   has not run within freshness window.
4. Authoring pricing or re-underwriting language in the debt market context
   section. Fix: debt market context is a cited categorical band; individual
   deal re-underwriting lives in deal-level packs.
5. Proposing capital deployment pace corrections. Fix: fund-level capital
   overlay governs; this pack reports posture only.
6. Proposing a JV partner / market / segment concentration cap change. Fix:
   `portfolio_concentration_targets.csv` is overlay-driven; this pack reports
   breach and escalates.
7. Treating declined_deal_hit_rate as "should we have bought it". Fix:
   overlay commentary governs interpretation; cohort attribution is required.
8. Sending the board packet. Fix: transmission is gated at row 16.
9. Missing IC docket readiness drift because IC-prep orchestration is
   downstream. Fix: surface readiness drift as advisory; do not attempt to
   orchestrate IC prep here.
10. Sample overlay used as authoritative debt market context. Fix: debt
    market context band carries its own `as_of_date` + `status`; sample is
    surfaced explicitly.
11. Letting a Procore commitment-overdrawn finding silently pass into the
    capex commitment exposure metric. Fix: `pc_recon_commitment_overdrawn`
    downgrades the metric to `low` confidence and appears in the
    reconciliation memo.

## Edge cases

- **Declined deal resurrection.** A previously-declined deal re-enters the
  pipeline (new sponsor group, re-offering, recapitalization). The pack
  flags the resurrection with an audit trail citation to the original
  decline and attribution category. Any re-engagement requires an explicit
  executive decision — do not default to pipeline inclusion without
  investments_lead confirmation.
- **Multi-asset closing in same period.** Two or more closings land in the
  same month; `pipeline_stage_committed_dollars` (proposed) swings
  materially between `close` and `funded`. Narrative distinguishes between
  scheduled close and actual funded to avoid double-counting. Forward
  capex commitment exposure steps up once Procore projects execute —
  `dp_handoff_dev_lag` watch begins immediately for each new closing.
- **Board-meeting freeze.** Board-calendar freeze window bans in-flight
  changes to the pipeline narrative. Pack behavior: if invoked during
  freeze, produce the narrative + dashboard but defer `approval_request`
  row 16 opening until freeze lifts; annotate the freeze in the output.
- **IC docket shift mid-month.** An IC meeting moves forward or back
  within the 90-day window. Recompute `ic_docket_forward_90d` (proposed)
  at each invocation — do not cache across invocations.
- **JV partner with multiple deal vehicles.** A single partner holds
  positions across multiple fund vehicles. Aggregate per-partner exposure
  across vehicles for `jv_partner_concentration` (proposed); annotate the
  cross-fund concentration per overlay.
- **Fund mid-close.** A fund closes mid-period; capital_deployment_target_ytd
  shifts. Use the most recently approved plan as the denominator; annotate
  the amendment date.
- **Debt market overlay stale.** Debt market context band not updated
  within overlay freshness window. Surface the stale as explicit; the
  metric drops to `low` confidence; narrative does not assert market
  direction.
- **Declined pool concentration on a single attribution category.** If the
  share of declines attributed to a single category exceeds the
  `declined_pool_attribution_concentration_band` from
  `reference/normalized/schemas/reconciliation_tolerance_band.yaml`, the
  narrative surfaces the concentration as a sourcing / underwriting signal
  — escalate to investments_lead for discipline review.
- **Pre-close deal with no expected_close_date.** Deal lacks
  `deal.expected_close_date` in Dealpath. Annotate as a Dealpath DQ gap;
  do not impute. Affects `expected_close_by_month` (proposed) confidence.
- **Pipeline asset crosswalk ambiguity.** `asset_crosswalk.yaml` does not
  resolve the pipeline asset to a single canonical asset_id (duplicate
  match or no match). Flag; do not collapse. Declined-deal hit rate
  computation excludes the ambiguous row until resolved.

## Example invocations

1. "Build the monthly executive pipeline summary for April 2026; audience board."
2. "IC docket forward 90 days; include readiness drift annotations."
3. "Capital deployment pace vs target for the core fund this month."
4. "Concentration check — pipeline + owned — by market and JV partner."
5. "Declined deal hit rate for Q1 2026 with attribution cohorts."
6. "Top-of-funnel sourcing health check this month."

## Example outputs

### Output — Monthly executive pipeline summary (abridged, April 2026, audience: board)

**Audience.** Board. Row 16 approval will open on final.

**Pipeline stage rollup.**

| Stage | Count | Dollars | Confidence |
|---|---|---|---|
| sourced | 18 | $485M | medium |
| loi_signed | 6 | $210M | medium |
| psa_signed | 4 | $165M | high |
| ic_approved | 2 | $92M | high |
| debt_term_sheet | 3 | $118M | medium |
| close | 1 | $48M | high |
| funded | 2 (April) | $86M | high |
| declined (T30) | 7 | $305M | high |
| on_hold | 3 | $110M | medium |

`pipeline_stage_committed_dollars` (proposed) aggregated above. Two deals
funded April; three deals in debt_term_sheet stage are exposed to
`debt_market_context_band` (proposed) = `neutral` per overlay.

**Expected close by month.** `expected_close_by_month` (proposed):

| Month | Count | Dollars |
|---|---|---|
| May | 1 | $48M |
| June | 2 | $88M |
| July | 1 | $45M |
| Aug | 0 | $0 |
| Sep | 1 | $35M |
| Oct-Mar | 6 | $240M |

**IC docket forward 90 days.** `ic_docket_forward_90d` (proposed):

| IC date | Deal | Deal size | Stage | JV partner | Market | Readiness |
|---|---|---|---|---|---|---|
| 2026-05-12 | Highland Mill | $48M | psa_signed | None | Charlotte | ready |
| 2026-05-12 | Glenwood Flats | $52M | loi_signed | Partner_B | Nashville | diligence_gap |
| 2026-06-09 | Ridge Park | $40M | loi_signed | None | Dallas | ready |
| 2026-07-14 | Brookline | $38M | psa_signed | Partner_A | Atlanta | debt_term_sheet_pending |

**Capex commitment forward 12 months.**
`capex_commitment_forward_exposure_dollars` (proposed) = $312M across 11 active
construction projects. Inherited from `workflows/development_pipeline_tracking`
run 2026-04-10 (within freshness window). Two commitments overdrawn on
Riverbend (cite `pc_recon_commitment_overdrawn`); metric confidence band =
`medium` until resolved.

**Debt market context.** `debt_market_context_band` (proposed) = `neutral`
per debt_market overlay as-of 2026-03-31 (sample). Overlay staleness within
tolerance; confidence = `medium`.

**Capital deployment pace.** Core fund:
`capital_deployment_pace_vs_target` (proposed) = 0.94 ytd. Within band (0.85
floor). Confidence = `high`.

**Declined deal hit rate.** T12m `declined_deal_hit_rate` (proposed) = 24%.
Attribution cohorts: priced-out 62%, diligence-findings 14%, market-timing
8%, stale-pipeline 16%. Confidence = `high`. No single-category concentration
>50%; investments discipline within overlay band.

**Top-of-funnel sourcing health.** `top_of_funnel_sourcing_health` (proposed):
T30 new deals = 9; broker-sourced share 72%; repeat-broker share 48%;
direct-sourced share 28%. Repeat-broker share above overlay target — route
to development_lead for broker-coverage review. Confidence = `medium`.

**JV partner concentration.** `jv_partner_concentration` (proposed):
Partner_A combined pipeline + owned 14.2%; Partner_B 9.6%; Partner_C 7.1%;
others <5% each. All within overlay threshold (15% cap). Partner_A approaching
cap — watch-item. Confidence = `high`.

**Geographic concentration.** `geographic_concentration_pipeline` (proposed):
Southeast 58% of pipeline dollars; pipeline + owned aggregate 56% (above
55% overlay target but within tolerance band). Confidence = `high`.

**Segment concentration.** `segment_concentration_pipeline` (proposed):
middle_market 92%; luxury 8%. Within overlay mandate. Confidence = `high`.

**Confidence bands summary.** Per-metric confidence ranges from `medium`
(pipeline stage dollars at `sourced` / `loi_signed`, debt market context,
commitment exposure due to Riverbend recon blocker) to `high` (closed /
funded dollars, declined hit rate, concentration rollups). No `low`
confidence metric surfaced without explicit narrative treatment.

**Reconciliation posture.** Two Procore commitments overdrawn on Riverbend
(`pc_recon_commitment_overdrawn` blocker) — runbook pointer surfaced;
capex commitment exposure confidence = `medium` until resolved. One Dealpath
DQ warning (`dp_handoff_lag`) on a Q1 closed deal — development_lead
notified. No Intacct posting-lag blockers.

**Top-3 pipeline watch items.**

1. Riverbend commitment overdrawn — construction + asset_mgmt priority;
   capex commitment exposure confidence = `medium` until resolved.
2. Repeat-broker share above overlay — route to development_lead for
   broker-coverage review; no sourcing blocker yet but trending.
3. Partner_A JV concentration at 14.2% vs 15% cap — watch-item; next
   month's board update if Partner_A's May deal closes.

**Draft board packet section.** Composed per overlay template; cited
metrics; confidence bands per metric surfaced prominently; reconciliation
memo included as appendix.

**Approval request.** `approval_request` row 16 opened; pending board final
submission. Transmission pathway through
`workflows/executive_operating_summary_generation`.

**Confidence banner.**
```
References: source_of_truth_matrix@wave_4_authoritative,
dealpath_deal_pipeline/normalized_contract@2026-04-08 (starter),
dealpath_deal_pipeline/dq_rules@2026-04-08 (starter),
procore_construction/reconciliation_checks@2026-04-08 (starter),
sage_intacct_gl/reconciliation_rules@2026-04-08 (starter),
asset_crosswalk@2026-04-08 (starter),
market_crosswalk@2026-04-08 (starter),
dev_project_crosswalk@2026-04-08 (starter),
capex_project_crosswalk@2026-04-08 (starter),
reconciliation_tolerance_band@2026-03-31 (sample),
approval_threshold_defaults@2026-03-31 (starter),
portfolio_concentration_targets@2026-03-31 (starter),
role_kpi_targets@2026-03-31 (starter).
Proposed metrics (flagged): pipeline_stage_committed_dollars,
expected_close_by_month, ic_docket_forward_90d,
capex_commitment_forward_exposure_dollars (inherited),
debt_market_context_band, capital_deployment_pace_vs_target,
declined_deal_hit_rate, top_of_funnel_sourcing_health,
jv_partner_concentration, geographic_concentration_pipeline,
segment_concentration_pipeline, confidence_band_per_metric.
Canonical extensions required: deal, deal_milestone, commitment
(tracked separately under canonical change-control).
Cross-system posture: Dealpath primary for deal pipeline;
Procore primary for active development + commitments; Intacct
primary for posted capex spend.
```
