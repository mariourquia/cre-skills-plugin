# Change Log — pipeline_review

## 0.1.0 — 2026-04-15
- Wave-5 introduction. Authored as part of stack-specific operationalization.
- Status: draft. Authored_by: skill_factory_agent. Reviewed_by: pending.
- Scope: weekly pipeline scorecard composing Dealpath-normalized `deal`, `asset`, `deal_milestone`, and `deal_key_date` objects into a stage-by-stage review. Surfaces `dp_completeness_ic_record` and `dp_handoff_lag` blocking issues from `dq_rules.yaml` before any roll-up.
- Metrics: eight proposed deal-pipeline metric slugs introduced (`pipeline_velocity_days`, `stage_conversion_rate`, `stalled_deal_count`, `ic_prep_load_count`, `debt_term_sheet_variance`, `retrade_risk_count`, `closing_certainty_score`, `pipeline_weighted_capital_need`). All flagged `proposed: true` pending formal contract addition in `_core/metrics.md`.
- Cross-links: invokes `workflows/investment_committee_prep/` when IC within one cycle; invokes `workflows/pre_close_deal_tracking/` when closing-week deal surfaces on retrade screen.
- Open item: canonical `Deal`, `DealMilestone`, `DealKeyDate` objects referenced are pending ontology amendment (tracked under the deal_pipeline wave-4 extension).
