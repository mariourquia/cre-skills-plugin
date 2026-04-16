# Change Log — lease_up_first_period

## 0.1.0 — 2026-04-15
- Pack initialized.
- Wave-5 introduction. Authored as part of stack-specific operationalization.
- Monthly lease-up tracker for the first 12-18 months post-delivery. AppFolio
  primary for leasing funnel + lease execution; Excel primary for rent comp +
  concession benchmark; Intacct primary for NOI actuals post-close; Procore
  primary for CCO timestamp (ground-up). Hands off to
  `workflows/monthly_property_operating_review` on stabilization crossover.
- Proposed metrics introduced: `lease_up_pace_vs_underwriting`,
  `concession_depth_vs_market`, `broker_assist_rate`,
  `model_unit_tour_conversion`, `first_renewal_window_retention_readiness`,
  `noi_ramp_vs_underwriting`, `lender_reporting_compliance_status`,
  `equity_call_schedule_coverage`, `cco_to_first_lease_days` (shared with
  `workflows/development_pipeline_tracking`). Each flagged `proposed: true`;
  promotion to canonical metrics.md tracked separately under canonical
  change-control.
- Edge cases declared: model unit not ready, marketing rentup gap,
  concession-vs-rent tradeoff above tolerance, first-renewal window straddling
  stabilization crossover, phased delivery, reserve fully drawn, lender waiver
  without documentation, ground-up with no prior history, post-delivery unit
  count change.
- Status: draft.
