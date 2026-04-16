# Workflow Activation Map - readable companion

Readable view of `workflow_activation_map.yaml`. One section per workflow,
grouped by audience. Each section states:

- What data the workflow needs.
- What happens in partial mode.
- What confidence warnings to surface.
- What remains human-gated.

Slugs match `workflows/<slug>/SKILL.md` and `_core/metrics.md`. Connectors
cited: `pms`, `gl`, `crm`, `ap`, `market_data`, `construction`, `hr_payroll`,
`manual_uploads`.

## Audience: executive

### executive_operating_summary_generation

- Needs: operating actuals (`pms`, `gl`), variance explanations, capex
  exposure. Optional: market and portfolio enrichment.
- Partial mode: produce the summary with a data-gap sidebar; mark each
  metric with its confidence label; cite the gap in the narrative.
- Confidence warnings: any missing variance explanation, missing budget
  alignment, stale capex snapshot.
- Human-gated: none by default; the summary is a read-out, not a decision.

## Audience: implementation_sponsor

### implementation_intake_signoff_builder

- Needs: the real source inventory plus whatever evidence exists from `pms`,
  `gl`, `construction`, `deal_pipeline`, and `manual_uploads`. It can begin
  before every artifact is attached, but it must label the gaps.
- Partial mode: produce the intake packet and leader sign-off draft with
  explicit assumptions, blockers, missing evidence, and reduced confidence.
  Do not present the packet as execution-ready until the named blockers and
  approvals are explicit.
- Confidence warnings: missing sample exports, unresolved source-of-truth
  conflicts, file-only third-party-manager evidence, missing approver
  identity, or any secret-storage refusal event.
- Human-gated: implementation scope sign-off, access provisioning sign-off,
  crosswalk approval, and final leader sign-off packet approval.

## Audience: regional_ops

### monthly_property_operating_review

- Needs: full property operating stack from `pms` and `gl`, plus
  manager-submitted scorecards from `manual_uploads` when the property is
  third-party-managed.
- Partial mode: produce the scorecard with gap annotations and a block
  labeling unavailable KPIs; drop the market-comparison panel when
  `market_rent_benchmark` is absent; flag to site-ops and regional-ops.
- Confidence warnings: any KPI computed from data below the staleness
  ceiling, any reconciliation warning, any approval override pending.
- Human-gated: concessions over policy, vendor awards over policy.

### lead_to_lease_funnel_review

- Needs: `crm` (lead and tour) joined with `pms` (application, approval,
  lease, lease event).
- Partial mode: compute the funnel from whatever stages are joinable; show
  an explicit label where join completeness falls below the floor.
- Confidence warnings: CRM-PMS join rate below floor, any stage with a
  null-critical field above tolerance.
- Human-gated: none; this is diagnostic.

### vendor_dispatch_sla_review

- Needs: `pms` (work order) joined with `ap` (vendor, vendor agreement).
- Partial mode: show SLA view per vendor for those with mapped agreements;
  list unmapped vendors at the top.
- Confidence warnings: any vendor agreement unmapped, any SLA rule
  undefined.
- Human-gated: vendor suspension.

### work_order_triage

- Needs: `pms` (work order, unit, lease).
- Partial mode: triage by available fields; escalate life-safety indicators
  immediately regardless of completeness.
- Confidence warnings: work order priority unmapped, repeat flag without
  history.
- Human-gated: life-safety escalation.

## Audience: asset_mgmt

### monthly_asset_management_review

- Needs: property-level operating stack (`pms`, `gl`), variance,
  forecast, capex.
- Partial mode: produce asset-level commentary; mark watchlist score stale
  if inputs lag; surface missing inputs at top.
- Confidence warnings: variance without explanation, forecast stale,
  budget alignment fail.
- Human-gated: capex reforecast over threshold; hold/sell recommendation.

### quarterly_portfolio_review

- Needs: portfolio roll-up inputs (`pms`, `gl`), same-store cohort
  membership, market aggregates.
- Partial mode: produce partial roll-up; flag properties with missing
  inputs and exclude from same-store cohort with rationale.
- Confidence warnings: same-store cohort undefined, cohort membership
  missing, stale submarket data.
- Human-gated: allocation shift recommendation.

### renewal_retention

- Needs: `pms` lease and lease-event history.
- Partial mode: limit analysis to leases with complete event sequences;
  annotate excluded leases; output retention bands with confidence labels.
- Confidence warnings: lease-event sequence gap, renewal window null, rent
  comp staleness.
- Human-gated: renewal offer over policy.

## Audience: finance_reporting

### delinquency_collections

- Needs: `pms` and `gl` resident account, charge, payment,
  delinquency case.
- Partial mode: produce aged schedule; exclude accounts where
  charge-payment tie-out fails; flag exceptions.
- Confidence warnings: charge-payment tie-out fail, legal-sensitive
  eviction status (requires counsel).
- Human-gated: eviction filing, payment plan over policy.

### reforecast

- Needs: YTD actuals, budget, forecast lines, variance explanations.
- Partial mode: produce reforecast with annotated gaps; flag lines with
  stale inputs.
- Confidence warnings: YTD actuals missing, budget-to-actual gap, forecast
  accuracy low in prior period.
- Human-gated: reforecast adoption.

### budget_build

- Needs: `pms` (unit, lease, charge, payment), `gl` (budget line), `ap`
  (commitment), `hr_payroll` (staffing plan), `construction` (capex
  project), plus reference inputs across payroll, staffing, utility, and
  capex line items.
- Partial mode: build budget with explicit assumption citations for missing
  references; mark lines with confidence labels.
- Confidence warnings: unit count reconciliation fail, staffing plan
  missing, concession benchmark stale, capex library stale.
- Human-gated: budget adoption.

### owner_approval_routing

- Needs: `pms`, `gl`, `ap`, `construction` inputs for the requested
  approval kind; canonical approval matrix; org overlay thresholds;
  approver identity.
- Partial mode: do not route; surface missing threshold or approver with
  `dq_blocker` and wait.
- Confidence warnings: approval matrix not loaded, approver identity
  unresolved, policy violation.
- Human-gated: primary approver, backup approver.

## Audience: development_construction

### capital_project_intake_and_prioritization

- Needs: `construction` capex scope, `pms` (property, unit, work order).
- Partial mode: rank with available signals; mark ranking confidence as
  low when cost references are absent; surface missing inputs.
- Confidence warnings: scope undefined, capex library stale.
- Human-gated: capex approval over threshold.

### capex_estimate_generation

- Needs: `construction` capex scope, capex line item reference.
- Partial mode: produce estimate with explicit assumption citations;
  mark gaps.
- Confidence warnings: line item reference missing, labor or material
  rates stale.
- Human-gated: none; estimate is an input to approval workflow.

### schedule_risk_review

- Needs: `construction` schedule milestones.
- Partial mode: view milestones with complete data; exclude incomplete
  phases; flag gap.
- Confidence warnings: milestone sequence incomplete, baseline missing.
- Human-gated: none.

### cost_to_complete_review

- Needs: `construction` + `gl` + `ap` for commitments, change orders,
  draws.
- Partial mode: compute cost-to-complete for reconciled packages; surface
  unreconciled packages.
- Confidence warnings: commitment-CO-draw reconciliation fail, contingency
  burn rate accelerating.
- Human-gated: contingency release over threshold.

### change_order_review

- Needs: `construction` + `ap` (bid package, change order, draw).
- Partial mode: list change orders with confidence labels; isolate
  pending-approval items.
- Confidence warnings: scope unmapped, override pending.
- Human-gated: change order over threshold.

### draw_package_review

- Needs: `construction` + `ap` + `gl` (draw, capex, bid package, change
  order).
- Partial mode: produce draw package with missing-document checklist; do
  not route until completeness threshold met.
- Confidence warnings: commitment-CO-draw reconciliation fail, lien waiver
  missing.
- Human-gated: draw certification.

### bid_leveling_procurement_review

- Needs: `construction` + `ap` (bid package, vendor, vendor agreement,
  estimate line item).
- Partial mode: produce leveled view with non-comparable scope items
  flagged; require human sign-off.
- Confidence warnings: bid scope not comparable, vendor agreement
  unmapped.
- Human-gated: vendor award.

### construction_meeting_prep_and_action_tracking

- Needs: `construction` (capex, milestones, change orders, draws).
- Partial mode: produce agenda and open-action list from whatever is
  available; surface missing inputs.
- Confidence warnings: action tracker missing, prior-meeting minutes
  missing.
- Human-gated: none.

## Audience: compliance_risk

### third_party_manager_scorecard_review

- Needs: `pms` (operating), `gl` (variance, budget), `manual_uploads`
  (manager-submitted reports, attestations), `hr_payroll` (staffing plan).
- Partial mode: produce scorecard with `completeness_score` visible; list
  missing KPIs; do not compute composite until completeness threshold is
  met.
- Confidence warnings: TPM report feed missing, KPI completeness blocker,
  reporting aging over SLA, audit issues unresolved.
- Human-gated: TPM remediation plan, TPM contract action.

## Audience: site_ops

### move_in_administration

- Needs: `pms` + `crm` (application, approval, lease, lease event, unit,
  work order, turn).
- Partial mode: surface blockers and wait; produce punch list of items
  that must resolve before move-in can proceed.
- Confidence warnings: unit not ready, approval pending, fair-housing
  sensitive flag.
- Human-gated: screening approval, reasonable accommodation decision.

### move_out_administration

- Needs: `pms` + `gl` (lease, lease event, unit, work order, turn,
  charge, payment, resident account).
- Partial mode: produce move-out packet with clearly-marked pending items;
  flag security-deposit accounting gaps.
- Confidence warnings: final account statement missing, termination
  reason unmapped.
- Human-gated: security deposit withholding over threshold.

### unit_turn_make_ready

- Needs: `pms` + `ap` (work order, turn project, unit, lease, vendor).
- Partial mode: produce turn dashboard for linked units; flag unresolved
  linkages.
- Confidence warnings: turn-to-unit link unresolved, scope change, cost
  variance.
- Human-gated: turn scope over threshold.

## Audience: portfolio_market_analytics

### market_rent_refresh

- Needs: `market_data` (rent comp, market rent benchmark), `pms` (unit,
  unit type, lease).
- Partial mode: refresh the subset of units with matched comps; flag
  units without comps.
- Confidence warnings: rent comp scope mismatch, stale source.
- Human-gated: market rent change over threshold.

### rent_comp_intake

- Needs: `market_data` rent comp, property master.
- Partial mode: accept comps with higher confidence; flag proposed
  identities for human review.
- Confidence warnings: comp identity unresolved, stale source, provenance
  weak.
- Human-gated: rent comp canonicalization.

## Confidence warnings - shared rules

Every workflow surfaces a confidence label on its output:

- `high` - all required inputs present, all blocking issues clear, all
  reference assumptions current.
- `medium` - all required inputs present, blocking issues clear, one or
  more reference assumptions stale or proposed.
- `low` - required inputs present but partial, or one or more reconciliation
  warnings active.
- `refuse` - blocking issue active; the workflow declines to produce output
  and surfaces the blocker.

The mapping from activation state to confidence label is deterministic.
The YAML view is the contract; the prose above is the guide.

## Human-gated approvals - shared rules

When a workflow names a `human_approvals_required` slug, the orchestration
layer routes the relevant decision to the org-scoped approval matrix. The
approval matrix lives in `overlays/org/<org_id>/approval_matrix.yaml` and
defaults from canonical `_core/approval_matrix.md`. The integration layer
never decides an approval without a routing match.

## Wave-5 workflow activations

The 9 wave-5 workflow packs surface the Dealpath / Procore / Intacct stack at the orchestration layer. The YAML view above is canonical; this section is the readable companion.

| Workflow | Domains | Primary source | Cadence | Audience |
|---|---|---|---|---|
| `pipeline_review` | deal_pipeline | Dealpath | weekly | investments_lead, asset_mgmt_director, executive |
| `pre_close_deal_tracking` | deal_pipeline | Dealpath | weekly / closing-week daily | investments_lead, deal_team_lead |
| `investment_committee_prep` | deal_pipeline | Dealpath | bi-weekly / per-IC | ic_members, executive, investments_lead |
| `acquisition_handoff` | deal_pipeline + pms + gl | Dealpath -> AppFolio + Intacct | event-driven (close) | asset_mgmt_director, regional_ops_director, finance_systems_team, data_platform_team |
| `post_ic_property_setup` | deal_pipeline + pms + gl | Dealpath -> AppFolio + Intacct (placeholder) | event-driven (IC approval) | data_platform_team, regional_ops_director |
| `delivery_handoff` | construction + pms + gl | Procore -> AppFolio + Intacct | event-driven (TCO) | development_lead, asset_mgmt_director, regional_ops_director, leasing_director |
| `development_pipeline_tracking` | deal_pipeline + construction + gl | Dealpath + Procore + Intacct | weekly | development_lead, construction_lead, asset_mgmt_director, executive |
| `lease_up_first_period` | pms + market_data | AppFolio + Excel | monthly during 6-18mo ramp | leasing_director, regional_ops_director, asset_mgmt_director, investments_lead |
| `executive_pipeline_summary` | deal_pipeline + construction + gl | Dealpath + Procore + Intacct | monthly | executive, ic_members |

Each workflow declares blocking dq rule ids in the YAML (e.g. `dp_handoff_lag`, `pc_recon_commitment_overdrawn`, `af_freshness_leases`); these resolve against the per-adapter `dq_rules.yaml` files. Approval gate slugs (e.g. `handoff_signoff`, `ic_committee_approval`, `board_pack_submission`) resolve against the org-scoped approval matrix.

`acquisition_handoff`, `post_ic_property_setup`, and `delivery_handoff` write to master_data crosswalks (`property_master_crosswalk.yaml`, `dev_project_crosswalk.yaml`, etc.) under `propose_then_approve` gating per `_core/schemas/reference_manifest.yaml`. No crosswalk row merges to canonical without the named human_approval slug closing.
