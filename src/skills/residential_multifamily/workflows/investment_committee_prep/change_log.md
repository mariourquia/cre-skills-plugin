# Change Log — investment_committee_prep

## 0.1.0 — 2026-04-15
- Wave-5 introduction. Authored as part of stack-specific operationalization.
- Status: draft. Authored_by: skill_factory_agent. Reviewed_by: pending.
- Scope: bi-weekly / event-driven IC packet-assembly pack composing Dealpath-
  normalized `deal`, `deal_milestone`, and `investment_committee_review` objects
  plus canonical `asset` master into an IC docket, per-deal memo cross-reference,
  prior-cycle condition tracking, sensitivity / stress-test posture, comp-evidence
  freshness scan, debt term sheet cross-link (from `pipeline_review`), and LP
  capital-coverage check. `decision_severity_max: action_requires_approval`
  — the pack is the IC input; the committee owns the gated decision via
  `ic_committee_approval`.
- DQ surface: refuses to publish any IC-approved roll-up while
  `dp_completeness_ic_record` or `dp_conformance_stage_enum` blockers are open;
  evaluates `dp_freshness_deals` on every run.
- Metrics: ten proposed IC metric slugs introduced (`ic_approval_rate`,
  `ic_deferral_rate`, `ic_decline_rate`, `ic_condition_completion_rate`,
  `ic_condition_aging_days`, `ic_docket_load_count`, `sensitivity_test_pass_rate`,
  `comp_evidence_freshness_days`, `lp_capital_coverage_ratio`, `ic_cycle_time_days`).
  All flagged `proposed: true` pending formal contract addition in
  `_core/metrics.md`.
- Cross-links: consumes sensitivity output from `skills/sensitivity_stress_test`;
  consumes debt variance state from `workflows/pipeline_review/`; shares IC
  condition tracking with `workflows/pre_close_deal_tracking/` for deals inside
  the close window; hands off to `workflows/acquisition_handoff/` on close.
- Open item: canonical `Deal`, `DealMilestone`, `InvestmentCommitteeReview`
  objects referenced are pending ontology amendment (tracked under the
  deal_pipeline wave-4 extension).
