# Runbook: Schema Drift Escalation

status_tag: reference

Upstream source schema changes and the break has reached downstream workflows. Use this runbook after `source_schema_change.md` determined the change is escalate-class or after a schema change slipped through detection and is already impacting consumers.

## 1. Trigger

- A schema change identified in `source_schema_change.md` was classified as escalate-class.
- A workflow reports "data unavailable" or "metric contract broken" and the root cause is a schema change.
- A metric contract in `_core/metrics.md` references a field that no longer lands from the source.
- Multiple runbooks fire in sequence because a single schema change rippled.

## 2. Symptoms

- `dq_blocker` exceptions cluster for one domain.
- Reconciliation `null_critical_field` flips to fail for a required metric input.
- Workflow activation map flags one or more workflows as `workflow_blocked` for the affected inputs.
- Executive-facing output shows a gap.

## 3. Likely causes (ranked)

1. Vendor removed a field required by a metric contract; mitigation requires either re-derivation from alternate inputs or metric-contract change.
2. Vendor renamed a field and tolerate-class remap was insufficient because downstream behavior depends on the old semantic.
3. Type change (for example, numeric to string, or different unit) that silently broke downstream math.
4. Enum domain change that retired a value a metric filter depended on.
5. New upstream required field that the adapter is not yet emitting.

## 4. Immediate actions (minute-by-minute, numbered)

1. Build the impact map. Starting from the changed field, walk downstream:
   - Normalized entities that read the field (`schema.yaml` `dependents` comment helps).
   - Reference-category outputs that depend on the normalized entity.
   - Metric slugs in `_core/metrics.md` whose numerator, denominator, or filter reference the field.
   - Workflows in `../../workflows/` whose inputs include affected metrics or entities.
   - Skill packs with `reference_manifest.yaml` reads on the affected outputs.
2. Classify each affected workflow:
   - **Blockable**: must not run until the gap is closed. Flag as `workflow_blocked`.
   - **Degradable**: can run with fallback inputs or reduced scope; flag as degraded.
   - **Unaffected**: the workflow's required inputs are unchanged.
3. Communicate the impact map to each audience whose workflows are affected. Use the restricted channel for `fair_housing_sensitive` or `legal_sensitive` overlap; otherwise route through the audience default channel per `../monitoring/alert_channel_design.md`.
4. Choose the mitigation. Options, ranked by preference:
   - **Override**: short-term mapping override per `manual_override_approval.md` to synthesize the missing field from another source or compute it from adjacent data.
   - **Backfill**: re-pull historical data from the source with the new shape and reprocess.
   - **Degraded mode**: operate without the field; update affected skill packs to surface the gap to users.
   - **Metric-contract change**: update `_core/metrics.md` to a revised contract that the new schema can satisfy. This is high-impact and requires approval per `_core/approval_matrix.md` row 20.
5. Implement the chosen mitigation under approval. Connector, crosswalk, mapping, or metric changes all require the appropriate approvals per `_core/approval_matrix.md`.
6. Communicate recovery. Tell affected audiences when the mitigation is live and which workflows resume normal operation.
7. Track the gap until permanent resolution. An override is a bridge to either backfill or metric-contract change; it is never the final answer for escalate-class drift.

## 5. Escalation path

- `technical_owner` and `data_owner` for the source.
- Primary consumer audience(s) whose workflows are impacted.
- `finance_reporting` for any metric-contract change.
- `compliance_risk` for regulatory-program impact.
- `executive` for impact on board, lender, investor, or regulator-facing outputs.
- `legal_counsel` if the schema change touches contractual or litigable data.
- Subsystem maintainer plus designated reviewer for canonical-data changes (matrix row 20).

## 6. Affected workflows

Driven by the impact map. Common cases:

- pms field removal affecting `delinquency_collections`, `renewal_retention`, or `lead_to_lease_funnel_review`.
- gl field removal affecting `monthly_property_operating_review`, `reforecast`, `budget_build`, `executive_operating_summary_generation`, `quarterly_portfolio_review`.
- market_data field removal affecting `market_rent_refresh`, `rent_comp_intake`.
- construction field removal affecting `draw_package_review`, `change_order_review`, `cost_to_complete_review`, `schedule_risk_review`, `capex_estimate_generation`, `construction_meeting_prep_and_action_tracking`, `bid_leveling_procurement_review`, `capital_project_intake_and_prioritization`.
- crm field removal affecting `lead_to_lease_funnel_review`.
- ap field removal affecting `vendor_dispatch_sla_review`, `bid_leveling_procurement_review`, and ap-driven slices of `monthly_property_operating_review`.

## 7. Recovery steps

- Apply the chosen mitigation.
- Replay affected raw landings through normalization.
- Recompute derived benchmarks.
- Lift `workflow_blocked` and `degraded_mode` flags as dependencies return to green.
- If a metric contract was changed, publish the change to every skill pack's `metrics_used` list through `reference_manifest.yaml` updates and, where needed, pack-level `metrics.md` text.

## 8. Verification steps

- Impact map resolved, every affected workflow has a status of green or an open permanent-fix ticket.
- Reconciliation green across the affected domain.
- No residual `dq_blocker` exceptions tied to the schema change.
- If a metric contract was changed, all tests under `tests/test_metric_contract_uniqueness.py` (and adjacent metric tests) pass.
- Approvals for changes are archived.

## 9. Post-incident review hooks

- Schema-drift incidents above a severity band are reviewed at the next monthly operations review.
- Metric-contract changes are logged in `_core/change_log_conventions.md` format.
- Chronic drift from a single vendor family escalates to a vendor-health review with `executive` and `finance_reporting`.
- Any drift that crossed `fair_housing_sensitive` or `legal_sensitive` data also flows through `fair_housing_sensitive_flag.md`.
- `../monitoring/slo_definitions.md` tracks schema-drift impact as a freshness and workflow-activation SLO component.
