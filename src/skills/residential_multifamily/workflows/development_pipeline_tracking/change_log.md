# Change Log — development_pipeline_tracking

## 0.1.0 — 2026-04-15
- Pack initialized.
- Wave-5 introduction. Authored as part of stack-specific operationalization.
- Weekly roll-up of active development pipeline across Dealpath (deal-stage),
  Procore (project-state + commitments), Intacct (capex spend). Aggregates by
  region and deal_lead. Flags critical-path slip beyond tolerance; cross-system
  reconciliation posture surfaced per `_core/stack_wave4/source_of_truth_matrix.md`.
  Cites blocking issues `dp_handoff_dev_lag` (warning) and
  `pc_recon_commitment_overdrawn` (blocker).
- Proposed metrics introduced: `critical_path_slip_days`,
  `draw_burn_rate_vs_plan`, `cco_to_first_lease_days`,
  `handoff_lag_dealpath_to_procore`, `commitment_exposure_forward_dollars`.
  Each flagged `proposed: true` in SKILL.md frontmatter; promotion to canonical
  metrics.md tracked separately.
- Canonical-object extensions (`deal`, `deal_milestone`, `commitment`) flagged
  for ontology amendment in a follow-up cycle per canonical change-control.
- Status: draft.
