# Change Log — pre_close_deal_tracking

## 0.1.0 — 2026-04-15
- Wave-5 introduction. Authored as part of stack-specific operationalization.
- Status: draft. Authored_by: skill_factory_agent. Reviewed_by: pending.
- Scope: per-deal closing-discipline pack composing Dealpath-normalized `deal`,
  `deal_key_date`, and `deal_milestone` objects into a closing-week dashboard.
  Tracks PSA / financing key-date countdown (LOI expiry, PSA expiry, DD period
  end, financing contingency, close target, tax lookback), open contingencies
  and their evidence-of-removal, escrow funding status, and lender deliverable
  status. Runs weekly for all deals past `under_psa`; daily for deals inside
  the overlay-defined `close_window_days` band.
- DQ surface: evaluates Dealpath `dq_rules.yaml` on every run; `dp_freshness_deals`
  is a blocker for affected deals, `dp_handoff_lag` is surfaced as a warning
  for recently-closed deals pending property setup.
- Metrics: eight proposed pre-close metric slugs introduced
  (`key_date_breach_count`, `key_date_days_remaining`, `closing_certainty_score`,
  `open_contingency_count`, `lender_deliverable_status_score`,
  `escrow_funding_status`, `pre_close_cycle_time`, `days_to_close`). All flagged
  `proposed: true` pending formal contract addition in `_core/metrics.md`.
- Cross-links: consumes the retrade screen from `workflows/pipeline_review/`;
  hands off to `workflows/acquisition_handoff/` on close; shares IC-condition
  tracking with `workflows/investment_committee_prep/` for any deal where
  `ic_approved` conditions remain unresolved at the close window.
- Open item: canonical `Deal`, `DealKeyDate`, `DealMilestone` objects referenced
  are pending ontology amendment (tracked under the deal_pipeline wave-4
  extension).
