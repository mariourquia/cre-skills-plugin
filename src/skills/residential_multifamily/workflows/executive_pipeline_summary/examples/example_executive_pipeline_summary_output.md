# Example — Executive Pipeline Summary (abridged)

**Prompt:** "Build the monthly executive pipeline summary for April 2026, audience board. Include capital deployment pace, concentration posture, IC docket forward 90 days, and declined-deal hit rate."

**Inputs:** Dealpath deal register + deal-milestone log + IC decision log + Procore project roster + commitment register + Intacct capex actuals + fund capital-deployment plan + debt market context overlay + JV partner register + portfolio concentration targets + sourcing funnel log + declined deal register with outcomes + asset_crosswalk + market_crosswalk + dev_project_crosswalk + capex_project_crosswalk + reconciliation_tolerance_band + approval_threshold_defaults + role_kpi_targets + board packet template.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- audience: board
- org_id: (from overlay)
- period: 2026-04 (prior-month close anchor)
- fund_id: FUND_CORE_II
- role: executive
- market: n/a (rollup across all)
- output_type: dashboard + memo + operating_review
- decision_severity: gated

## Expected packs loaded

- `workflows/executive_pipeline_summary/`
- `workflows/development_pipeline_tracking/` (inherited — capex commitment forward exposure)
- `workflows/pipeline_review/` (inherited — deal-pipeline context)
- `workflows/pre_close_deal_tracking/` (inherited — IC docket readiness drift context)
- `workflows/executive_operating_summary_generation/` (downstream — transmission composition)
- `workflows/quarterly_portfolio_review/` (cross-link — portfolio trend context)
- `overlays/segments/middle_market/`

## Expected references

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

## Gates potentially triggered (elsewhere)

- Row 16 (board final submission) — opened by this pack on final; composition in `workflows/executive_operating_summary_generation`.
- Row 17 (IC advance-read) — conditional on overlay; not triggered this run (board audience).
- `workflows/cost_to_complete_review`: capex reallocation approval — Riverbend commitment-overdrawn finding echoed in this summary.
- `workflows/pipeline_review`: no gated actions; context inherited.

## Expected output shape

- Pipeline stage dashboard with counts + dollars per stage and confidence band.
- Expected close schedule forward 12 months.
- IC docket forward 90 days per-deal row (ic_scheduled_date, deal size, stage,
  JV partner, market, readiness state).
- Capex commitment exposure forward 12 months, inherited from development
  pipeline tracking.
- Debt market context band + overlay citation.
- Capital deployment pace ytd vs target.
- Declined deal hit rate with attribution cohorts.
- Top-of-funnel sourcing health composite (T30 adds, broker share, repeat-broker
  share, direct share).
- JV partner concentration per partner.
- Geographic concentration pipeline (+ owned context).
- Segment concentration pipeline (+ owned context).
- Confidence bands appendix per metric.
- Reconciliation posture memo (Dealpath DQ, Procore recon, Intacct posting
  lag).
- Narrative summary with top-3 pipeline watch items.
- Draft board packet section.
- `approval_request` row 16 opened on final.

## Confidence banner pattern

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

## Example narrative excerpt

The April 2026 pipeline view carries 25 deals under active investments-side
management against $1.3B committed capital at various stages.
`pipeline_stage_committed_dollars` (proposed) shows the largest stage-bucket
concentration sitting at `sourced` ($485M across 18 deals) and `declined`
($305M across 7 deals, T30). Two deals funded in April ($86M combined); three
deals are in `debt_term_sheet` stage ($118M) and carry forward sensitivity to
`debt_market_context_band` (proposed), currently at `neutral` per overlay.

Forward IC docket shows four deals scheduled over the next 90 days for
$178M combined. `ic_docket_forward_90d` (proposed) flags Glenwood Flats with
a diligence-gap readiness state — asset_mgmt_director briefed via
`workflows/pre_close_deal_tracking`; IC-prep orchestration remains in that
pack.

Forward 12-month capex commitment exposure sits at $312M inherited from
`workflows/development_pipeline_tracking` run 2026-04-10. Two commitments
overdrawn on Riverbend sitework (`pc_recon_commitment_overdrawn`) hold the
metric confidence at `medium` until resolved. The procore runbook
`commitment_overdrawn` is active; capex reallocation question belongs to
`workflows/cost_to_complete_review` and is out of scope for this pack.

Capital deployment pace for the core fund runs at 0.94 ytd —
`capital_deployment_pace_vs_target` (proposed) — within the overlay floor
(0.85). No escalation warranted. The next two months' close schedule ($136M
combined) is the primary driver for maintaining pace; if either Highland Mill
(May) or the Ridge Park / Glenwood Flats cluster slips, the pace drifts
toward the floor and `capital_deployment_pace_vs_target` (proposed) becomes
a board watch-item.

Concentration posture is broadly within mandate. Southeast geographic share
sits at 58% of pipeline dollars (pipeline + owned aggregate 56%), just above
the 55% overlay target but within tolerance. Segment concentration at 92%
middle_market / 8% luxury is squarely within overlay mandate. JV partner
concentration: Partner_A approaching the 15% cap at 14.2% combined pipeline
+ owned — watch-item surfaced for next month if Partner_A's May deal closes
on plan. `jv_partner_concentration` (proposed) per partner is in the appendix.

Declined-deal discipline is healthy. Trailing-12-month
`declined_deal_hit_rate` (proposed) = 24%. Attribution cohorts: priced-out
62%, diligence-findings 14%, market-timing 8%, stale-pipeline 16%. No
single-category concentration above 50%. Diligence-findings cohort remains
the most defensible — deals we declined for a discoverable risk, and we did
not over-pay to win them. Narrative avoids hindsight-bias framing per overlay
interpretation commentary.

Top-of-funnel sourcing health is the lone amber line. T30 new-deal adds at 9
deals, broker-sourced share 72%, repeat-broker share 48%, direct-sourced
share 28%. Repeat-broker share above overlay target — route to
development_lead for broker-coverage review. Not a blocker; a trend worth
watching.

Per-metric confidence bands are surfaced throughout. Funded-dollar metrics
and closed-deal counts run `high`; sourced-stage dollars and
commitment-exposure run `medium` due to the Riverbend recon finding. Debt
market context band is `medium` (overlay freshness within window but sample
status). No metric surfaced at `low` confidence without explicit narrative
treatment.

Top-3 pipeline watch items: (1) Riverbend commitment overdrawn — construction
+ asset_mgmt priority; (2) repeat-broker share above overlay — route to
development_lead; (3) Partner_A JV concentration approaching cap — next-month
board update if the May deal closes.

The board packet section draft follows the overlay template and is
attached; `approval_request` row 16 is opened pending board final submission.
Transmission composition pathway remains in
`workflows/executive_operating_summary_generation`. Board meeting freeze
window does not apply this cycle.
