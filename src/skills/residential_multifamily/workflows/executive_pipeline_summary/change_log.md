# Change Log — executive_pipeline_summary

## 0.1.0 — 2026-04-15
- Pack initialized.
- Wave-5 introduction. Authored as part of stack-specific operationalization.
- Monthly executive rollup of pipeline state across Dealpath (deal pipeline),
  Procore (active development pipeline), and Intacct (capex commitment
  exposure). Board-ready + IC-ready output with per-metric confidence bands.
  Decision severity `gated`: row 16 (board final) and row 17 (IC advance-read,
  overlay-dependent); transmission composition remains in
  `workflows/executive_operating_summary_generation`.
- Proposed metrics introduced: `pipeline_stage_committed_dollars`,
  `expected_close_by_month`, `ic_docket_forward_90d`, `debt_market_context_band`,
  `capital_deployment_pace_vs_target`, `declined_deal_hit_rate`,
  `top_of_funnel_sourcing_health`, `jv_partner_concentration`,
  `geographic_concentration_pipeline`, `segment_concentration_pipeline`,
  `confidence_band_per_metric`. `capex_commitment_forward_exposure_dollars`
  inherited from `workflows/development_pipeline_tracking`. Each flagged
  `proposed: true`; promotion to canonical metrics.md tracked separately under
  canonical change-control.
- Canonical-object extensions (`deal`, `deal_milestone`, `commitment`) flagged
  for ontology amendment in a follow-up cycle — same scope as wave-5 tracked
  in `workflows/development_pipeline_tracking`.
- Edge cases declared: declined deal resurrection, multi-asset closing in
  same period, board-meeting freeze, IC docket shift mid-month, JV partner
  with multiple deal vehicles, fund mid-close, debt market overlay stale,
  declined-pool concentration on single attribution category, pre-close deal
  with no expected_close_date, pipeline asset crosswalk ambiguity.
- Status: draft.
