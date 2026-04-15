# Change Log — post_ic_property_setup

## 0.1.0 — 2026-04-15

- Pack initialized. Wave-5 introduction. Authored as part of stack-specific
  operationalization of `reference/connectors/_core/stack_wave4/lifecycle_handoffs.md`
  Handoff 1 (Dealpath -> approved acquisition) for the pre-close window.
- Pre-close setup checklist authored: property_id reservation, AppFolio
  placeholder property (`lifecycle_stage=pre_acquisition`), Intacct placeholder
  entity dim, legal-entity formation routing, tax-lot and assessment research,
  pre-acquisition insurance binder, placeholder `property_master_crosswalk` and
  `asset_crosswalk` row drafts, baton-pass payload for `acquisition_handoff`.
- Proposed metrics introduced: `pre_close_setup_completeness_score`,
  `placeholder_crosswalk_creation_lag_days`, `pre_close_insurance_binder_lead_days`,
  `legal_entity_formation_lag_days`, `tax_lot_research_completion_rate`,
  `handoff_baton_readiness_score`. To be lifted into `_core/metrics.md` before
  promotion beyond draft.
- Approval gates: row 7 (handoff lag), row 17 (pre-close sign-off, legal-entity
  formation delay, insurance binder gap), row 19 (legal-entity formation
  engagement contract).
- Blocking issue ids cited: `dp_completeness_ic_record`, `dp_handoff_lag`,
  `dp_one_deal_multiple_projects`.
- Baton-pass handoff to `workflows/acquisition_handoff` at close defined; the
  workflow never promotes the placeholder to operating (that is
  `acquisition_handoff`'s responsibility).
- Status: draft.
