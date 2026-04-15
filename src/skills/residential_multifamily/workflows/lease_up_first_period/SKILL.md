---
name: Lease-Up First Period
slug: lease_up_first_period
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Market concession benchmarks, rent-comp depth, marketing-channel mix assumptions,
  concession-vs-rent tradeoff overlays, and underwriting lease-up curves drift. AppFolio
  lease-status semantics (FutureActive vs InEffect) evolve with product releases; the
  adapter contract is the source of truth. Lender-reporting templates and equity-call
  schedules are loan- and fund-specific and overlay-driven. Every pace claim cites a
  reference; sample overlays must be replaced before any output is treated as an
  ownership-side commitment.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [lease_up]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [leasing_director, regional_ops_director, asset_mgmt_director, investments_lead, property_manager, leasing_manager, asset_manager, portfolio_manager]
  output_types: [kpi_review, operating_review, memo, dashboard]
  decision_severity_max: recommendation
references:
  reads:
    - reference/connectors/_core/stack_wave4/source_of_truth_matrix.md
    - reference/connectors/adapters/appfolio_pms/normalized_contract.yaml
    - reference/connectors/adapters/appfolio_pms/reconciliation_rules.md
    - reference/connectors/adapters/appfolio_pms/runbooks/appfolio_common_issues.md
    - reference/connectors/adapters/excel_market_surveys/normalized_contract.yaml
    - reference/connectors/adapters/excel_market_surveys/reconciliation_rules.md
    - reference/connectors/master_data/property_master_crosswalk.yaml
    - reference/connectors/master_data/lease_crosswalk.yaml
    - reference/connectors/master_data/resident_account_crosswalk.yaml
    - reference/connectors/master_data/market_crosswalk.yaml
    - reference/normalized/market_rents__{market}_mf.csv
    - reference/normalized/concession_benchmarks__{market}_mf.csv
    - reference/normalized/occupancy_benchmarks__{market}_mf.csv
    - reference/normalized/marketing_channel_mix__middle_market.csv
    - reference/normalized/schemas/reconciliation_tolerance_band.yaml
    - reference/normalized/approval_threshold_defaults.csv
    - reference/derived/funnel_conversion_benchmarks__middle_market.csv
    - reference/derived/role_kpi_targets.csv
  writes: []
metrics_used:
  - stabilization_pace_vs_plan         # canonical — _core/metrics.md (asset_management family)
  - lease_up_pace_post_delivery        # canonical — _core/metrics.md (development_construction family)
  - preleased_occupancy                # canonical
  - leased_occupancy                   # canonical
  - economic_occupancy                 # canonical
  - physical_occupancy                 # canonical
  - notice_exposure                    # canonical
  - lead_response_time                 # canonical
  - tour_conversion                    # canonical
  - application_conversion             # canonical
  - approval_rate                      # canonical
  - move_in_conversion                 # canonical
  - concession_rate                    # canonical
  - rent_growth_new_lease              # canonical
  - market_to_lease_gap                # canonical
  - renewal_offer_rate                 # canonical
  - renewal_acceptance_rate            # canonical
  - noi_margin                         # canonical
  - revenue_variance_to_budget         # canonical
  - expense_variance_to_budget         # canonical
  - lease_up_pace_vs_underwriting      # proposed: true — ratio of actual leased_occupancy_to_date to underwriting lease_up_plan_to_date at same week-post-TCO; extends stabilization_pace_vs_plan by explicit underwriting curve reference
  - concession_depth_vs_market         # proposed: true — difference in equivalent months off between property new-lease concessions and market concession_benchmark (avg_concession_dollars and pct_comps_offering); extends concession_rate with comp-set normalization
  - broker_assist_rate                 # proposed: true — share of executed leases in window where source_channel indicates broker assist; sub-cut of source-mix by Lead.source_channel
  - model_unit_tour_conversion         # proposed: true — tour_conversion filtered to tours that included a model unit walk; diagnostic for model-unit marketing performance
  - first_renewal_window_retention_readiness  # proposed: true — T60-days-ahead count of leases approaching first renewal with renewal_offer_issued / engaged / signed breakdown; early-warning analogue to renewal_acceptance_rate during lease-up -> stabilization transition
  - noi_ramp_vs_underwriting           # proposed: true — monthly NOI actual vs underwriting NOI ramp at same month-post-TCO; extends stabilization_pace_vs_plan to NOI-denominated view
  - lender_reporting_compliance_status # proposed: true — binary per lender-required leasing KPI submission that came due in the period (on_time, late, missed, waived)
  - equity_call_schedule_coverage      # proposed: true — forward-90-day equity-call plan per fund overlay, with (planned_amount, committed_amount, deployed_amount); not a percent, a state table
  - cco_to_first_lease_days            # proposed: true — days from certificate_of_occupancy_issued (CCO) to first_executed_lease; inherited from workflows/development_pipeline_tracking where available
escalation_paths:
  - kind: lease_up_pace_behind_plan
    to: leasing_manager -> regional_ops_director -> asset_mgmt_director -> investments_lead
  - kind: concession_above_policy
    to: leasing_manager -> asset_manager -> approval_request(row 13 for policy-exceeding concession during lease-up)
  - kind: fair_housing_flag
    to: leasing_manager -> regional_ops_director -> approval_request(row 3)
  - kind: model_unit_readiness_gap
    to: construction_manager + leasing_manager -> asset_manager
  - kind: marketing_rentup_gap
    to: leasing_manager + marketing_lead -> regional_ops_director
  - kind: concession_rent_tradeoff_above_tolerance
    to: leasing_director + asset_mgmt_director -> investments_lead
  - kind: noi_ramp_behind_underwriting
    to: asset_mgmt_director -> investments_lead
  - kind: lender_reporting_compliance_miss
    to: asset_mgmt_director + reporting_finance_ops_lead -> approval_request(row 14 if response requires lender submission)
  - kind: equity_call_timing_drift
    to: cfo_finance_leader + portfolio_manager -> investments_lead
  - kind: first_renewal_window_risk_spike
    to: leasing_manager -> regional_ops_director
approvals_required: []
description: |
  Operationalize the first 12-18 months post-delivery of a new-construction or
  gut-renovation asset: monthly tracker of lease-up velocity vs underwriting, concession
  depth vs market, approval-rate posture, traffic-source mix, broker-assist rate,
  model-unit performance, first-renewal retention readiness, stabilization pace, NOI
  ramp vs underwriting, lender-reporting compliance, and equity-call scheduling for any
  unfunded reserves. Distinguishes from the steady-state
  `workflows/monthly_property_operating_review` by adding ramp-tracking metrics and by
  wiring the cross-system posture between AppFolio (leasing funnel + lease execution)
  and Excel (rent comp + concession benchmark) into a single lease-up narrative. Hands
  off to `workflows/monthly_property_operating_review` once the property crosses the
  lifecycle stabilization threshold.

  Narrative-first with a KPI dashboard. Informational to recommendation severity: this
  pack does not authorize concession policy exceptions, pricing shifts, or equity-call
  initiations — those gate through their owning workflows (`workflows/market_rent_refresh`,
  overlay concession governance, fund-level capital overlay). Child workflows invoked:
  `workflows/lead_to_lease_funnel_review`, `workflows/market_rent_refresh`,
  `workflows/move_in_administration`, `workflows/renewal_retention` (read-only, for
  first-renewal window).
---

# Lease-Up First Period

## Workflow purpose

Give the leasing_director, regional_ops_director, asset_mgmt_director, and
investments_lead a single monthly view of a new-construction or gut-renovation asset
during its first 12-18 months post-delivery — so that drift from the underwriting
lease-up curve, concession escalation beyond the comp set, model-unit or marketing-
channel underperformance, and lender-reporting or equity-call timing risk surface in
the same month they occur.

This pack is ramp-aware. It is not the steady-state monthly review. It preserves
lease-up-specific metrics (`lease_up_pace_vs_underwriting`, `concession_depth_vs_market`,
`noi_ramp_vs_underwriting`, `first_renewal_window_retention_readiness`) and explicitly
annotates when a property crosses the stabilization threshold and the ownership-side
review cadence hands off to `workflows/monthly_property_operating_review`.

The workflow is read-heavy across two primary source systems — AppFolio for the
leasing funnel and lease execution, Excel for rent comp + concession benchmark — with
secondary pulls from Intacct (NOI actuals) and Procore (CCO timestamp) where the
property came from ground-up development. Cross-system posture is declared in
`_core/stack_wave4/source_of_truth_matrix.md`.

## Trigger conditions

- **Explicit:** "monthly lease-up review", "lease-up scorecard", "lease-up pace",
  "how's the new asset performing", "South Fork lease-up tracker", "NOI ramp check".
- **Implicit:** property lifecycle enters `lease_up` (from TCO or CCO); property is
  within its overlay-defined lease-up window (typically 6-18 months post-delivery);
  `stabilization_pace_vs_plan` breaches overlay band; concession_rate crosses lease-up
  overlay ceiling; lender-reporting calendar event (quarterly or monthly per loan
  overlay) approaches; fund equity-call milestone approaches; first-renewal window
  (T60 days) opens for any lease-up-executed lease.
- **Recurring:** monthly per property while the property is in `lifecycle = lease_up`;
  escalates to weekly cadence if `lease_up_pace_vs_underwriting` falls more than
  overlay tolerance behind plan for two consecutive weeks.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| AppFolio rent roll snapshot | table | required | per `appfolio_pms` adapter |
| AppFolio lease register (all leases executed to date) | table | required | canonical `lease` |
| AppFolio lease-event log | table | required | canonical `lease_event` |
| AppFolio CRM funnel (leads, tours, applications, approvals) | table | required | `lead, tour, application, approval_outcome` |
| AppFolio charge + concession ledger | table | required | `charge, concession_record` |
| Excel market rent comp pack | table | required | per `excel_market_surveys` adapter |
| Excel concession benchmark pack | table | required | per `excel_market_surveys` adapter |
| Underwriting lease-up plan | table | required | weekly / monthly underwriting leased_occupancy curve; preserved per property on delivery |
| Underwriting NOI ramp | table | required | monthly underwriting NOI ramp |
| Loan covenant + lender-reporting calendar | yaml | required | per-loan overlay |
| Fund equity-call schedule | yaml | required | per-fund overlay (forward 90 days) |
| Marketing-channel mix reference | csv | required | segment-level; benchmark-only |
| Model-unit status + readiness log | log | optional | construction handoff artifact; used if ground-up |
| Broker assist identifier list | yaml | optional | Lead.source_channel values flagged broker-assist |
| Property_master_crosswalk | yaml | required | property_id resolution |
| Lease_crosswalk | yaml | required | lease_id resolution |
| Resident_account_crosswalk | yaml | required | resident_account_id resolution |
| Market_crosswalk | yaml | required | market scope resolution for rent comp + concession benchmark |
| Tolerance-band schema | yaml | required | `reconciliation_tolerance_band.yaml` |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Lease-up pace dashboard | `dashboard` | `lease_up_pace_vs_underwriting` (proposed), `stabilization_pace_vs_plan`, `lease_up_pace_post_delivery`, `preleased_occupancy`, `leased_occupancy`, `economic_occupancy`, `cco_to_first_lease_days` (proposed) |
| Concession posture | `kpi_review` | `concession_rate`, `concession_depth_vs_market` (proposed), policy ceiling check |
| Funnel posture | `kpi_review` | `lead_response_time`, `tour_conversion`, `application_conversion`, `approval_rate`, `move_in_conversion`, `broker_assist_rate` (proposed), `model_unit_tour_conversion` (proposed) |
| Traffic source mix | `kpi_review` | source-by-source lead volume, tour conv, application conv, executed-lease share |
| Model unit performance | `memo` | readiness status + `model_unit_tour_conversion` (proposed) contribution |
| First-renewal readiness | `kpi_review` | `first_renewal_window_retention_readiness` (proposed) for leases T60 days to first end_date |
| NOI ramp posture | `kpi_review` | `noi_ramp_vs_underwriting` (proposed), `noi_margin`, `revenue_variance_to_budget`, `expense_variance_to_budget` |
| Rent comp & market gap | `kpi_review` | `rent_growth_new_lease`, `market_to_lease_gap` |
| Lender-reporting compliance | `kpi_review` | `lender_reporting_compliance_status` (proposed) — per required submission |
| Equity-call schedule | `kpi_review` | `equity_call_schedule_coverage` (proposed) forward 90 days |
| Stabilization crossover check | `memo` | binary handoff indicator; cites overlay threshold |
| Narrative memo | `memo` | 3-5 paragraphs, cited metrics, top-3 watch items, handoff posture |
| Confidence banner | banner | reference `as_of_date` + `status` + sample-tag surfacing |

## Required context

Asset_class, segment, form_factor, lifecycle_stage (must be `lease_up`), management_mode,
market, property_id, org_id. Delivery date (TCO and, where distinct, CCO) must be known
— the workflow computes all ramp metrics against weeks-post-delivery. Loan_id is
required if the property carries construction-to-permanent or permanent debt with a
lease-up-stage covenant or reporting obligation. Fund_id is required if the pack
reports equity-call posture.

## Process

### Step 1. Delivery anchor and ramp-week computation

Establish the anchor date. Pull `property.acquired_date` where applicable; for ground-up
projects pull CCO (certificate_of_occupancy_issued) from the Procore side per the
handoff posture declared in `source_of_truth_matrix.md` (Procore primary for
`construction_project` and `schedule_milestone`). If CCO differs from TCO, use CCO as
the first-lease anchor per loan overlay convention and annotate the gap via
`cco_to_first_lease_days` (proposed). Every pace metric in subsequent steps is
computed as "week N post-delivery" so the underwriting curve and actuals align at the
same x-axis.

### Step 2. Lease-up pace vs underwriting

Compute:

- `leased_occupancy` at property grain per `appfolio_pms/normalized_contract.yaml`
  semantics (lease status in {executed, in_effect} with preleased window per overlay).
- `preleased_occupancy` for future-start executed leases within the preleased_window
  (lease_up overlay typically widens to 60 days — cite the overlay).
- `lease_up_pace_post_delivery` (canonical): weekly rolling units-leased count.
- `stabilization_pace_vs_plan` (canonical): actual leased occupancy minus budget
  leased occupancy at the same ramp-week.
- `lease_up_pace_vs_underwriting` (proposed): ratio of actual-to-date to
  underwriting-to-date at current ramp-week. The underwriting curve is frozen at
  property delivery; any change in the underwriting curve is logged separately via
  fund overlay and this pack annotates the change.

Flag any ramp-week where `lease_up_pace_vs_underwriting` (proposed) is more than the
overlay tolerance (cite `reconciliation_tolerance_band.yaml::lease_up_pace_band`)
behind plan. Two consecutive flags escalate cadence to weekly per trigger policy.

### Step 3. Concession posture vs market

Compute:

- `concession_rate` (canonical) on new leases executed in the window.
- `concession_depth_vs_market` (proposed): equivalent months off on the property's
  new-lease average versus `concession_benchmarks__{market}_mf.csv` row matched on
  segment + form_factor + lifecycle_stage=lease_up. Surface both the absolute gap and
  the `pct_comps_offering` delta.

Flag:

- Any lease where concession > lease-up overlay ceiling — route to overlay concession
  governance; open or verify `approval_request` row 13 for policy-exceeding
  concessions during lease-up.
- Any period where `concession_depth_vs_market` (proposed) exceeds overlay tolerance
  (cite `reconciliation_tolerance_band.yaml::concession_depth_band`). This is the
  concession-vs-rent tradeoff sentinel — escalate to leasing_director + asset_mgmt_director.

Every concession comparison cites the Excel comp source `as_of_date` and `status`
(sample / starter / live).

### Step 4. Application approval rate + fair-housing guardrail

Compute:

- `approval_rate` (canonical) over the window. Lease-up overlay applies its own target
  band — the lease-up population is often demographically distinct from stabilized,
  so the pack uses the lease-up-scoped band.
- Compare to T90-day trailing baseline. Statistically meaningful disparity triggers a
  fair-housing flag — route to `workflows/lead_to_lease_funnel_review`'s fair-housing
  branch (row 3) rather than asserting here.
- Confirm every `approval_outcome` cites a `policy_ref`. Missing `policy_ref` is a
  screening-drift finding; annotate but do not propose a screening change.

Fair-housing scanning is delegated to `workflows/lead_to_lease_funnel_review`; this
pack references the findings, not authors them.

### Step 5. Traffic source mix and broker-assist posture

Group leads, tours, applications, and executed leases by `Lead.source_channel`.
Compute per-source:

- Lead volume share.
- Tour conversion.
- Application conversion.
- Executed-lease share.
- Cost-per-lease (if marketing spend is available from the marketing_channel_mix
  reference plus property-level spend overlay; else annotate gap and skip).

Separately compute `broker_assist_rate` (proposed): share of executed leases whose
`source_channel` is in the broker-assist identifier list (optional overlay input). A
high broker-assist rate during lease-up is not a flag by itself — compare to
`marketing_channel_mix__middle_market.csv` benchmark to classify as within / above /
below expected for segment + market.

If there is a marketing rentup gap (i.e., total lead volume + conversion pace cannot
produce enough executed leases to track plan), route to leasing_manager + marketing_lead.

### Step 6. Model unit performance

If ground-up with a model unit program:

- Pull model-unit readiness status (construction handoff artifact).
- Compute `model_unit_tour_conversion` (proposed): tour_conversion filtered to tours
  whose record indicates a model-unit walk.
- Compare to overall tour_conversion and to `funnel_conversion_benchmarks__middle_market.csv`.

If the model unit is not ready (finishes incomplete, staging not complete, utilities
not live), flag as `model_unit_readiness_gap` — route to construction_manager +
leasing_manager. Do not propose a pricing change to compensate; surface the gap as a
non-pricing remediation.

### Step 7. First-renewal window retention readiness

For any executed lease with `end_date` within T60 days of the run date:

- Compute `first_renewal_window_retention_readiness` (proposed): count by state
  (renewal_offer_issued, engaged, signed, declined, notice_given, unresponsive).
- Compare to `renewal_uplift_bands__middle_market.csv` where available.
- Annotate any lease that was executed with a lease-up concession — the first renewal
  is structurally different from a stabilized renewal because the prior rent may have
  been concession-burdened. Cite the overlay's first-renewal rent policy.

This is read-only for the steady-state renewal workflow: it surfaces the queue but
does not draft offers. Offer drafting lives in `workflows/renewal_retention`.

### Step 8. NOI ramp posture

Pull monthly NOI from Intacct (per `sage_intacct_gl` adapter; Intacct is primary for
`actual_line`). Compute:

- `noi` (canonical) at property grain, month-post-delivery.
- `noi_margin` (canonical).
- `noi_ramp_vs_underwriting` (proposed): ratio of actual NOI to underwriting NOI at
  same month-post-delivery. Underwriting NOI ramp is frozen at delivery.
- `revenue_variance_to_budget` and `expense_variance_to_budget` (canonical) against
  the lease-up-stage budget.

Flag any month where `noi_ramp_vs_underwriting` (proposed) is more than overlay
tolerance behind underwriting. Two consecutive flags escalate to investments_lead.

### Step 9. Rent comp and market-to-lease gap

- `rent_growth_new_lease` (canonical) over the window.
- `market_to_lease_gap` (canonical) using `market_rents__{market}_mf.csv`.

Surface the gap explicitly so the Excel comp `as_of_date` and `status` appear in the
confidence banner — market-to-lease-gap claims are among the most stale-data-sensitive
in the pack.

### Step 10. Lender-reporting compliance

For each loan with a lease-up-stage reporting obligation (per loan overlay
reporting calendar):

- Compute `lender_reporting_compliance_status` (proposed) per required submission in
  the period: `on_time`, `late`, `missed`, `waived`.
- Flag any `missed` or `waived` without documented waiver — route to
  asset_mgmt_director + reporting_finance_ops_lead. If a response requires a lender
  submission, open `approval_request` row 14 (lender final submission gate).

This pack does not author lender submissions; it flags compliance posture. Submission
composition is in `workflows/executive_operating_summary_generation` when lender
output is needed.

### Step 11. Equity-call schedule (unfunded reserves)

If the fund overlay declares equity-call schedule posture applies:

- Pull forward 90-day equity-call plan from the fund overlay.
- Compute `equity_call_schedule_coverage` (proposed) per scheduled call:
  `planned_amount`, `committed_amount`, `deployed_amount`, `due_date`.
- Flag any call whose `due_date` is within 30 days and whose `committed_amount` is
  below `planned_amount` by more than overlay tolerance.

This pack does not initiate calls; it reports posture. Call initiation lives in
fund-level capital overlay.

### Step 12. Stabilization crossover check

Compute whether the property has crossed the stabilization threshold (per overlay,
typically a sustained `leased_occupancy` above overlay-defined band for N consecutive
months). If crossed:

- Annotate the stabilization crossover date.
- Flag the handoff from `lease_up_first_period` to
  `workflows/monthly_property_operating_review` as the primary monthly cadence going
  forward.
- The first renewal window may still straddle the crossover; retention readiness
  continues to be tracked here until the first-cohort renewals conclude.

The handoff is ownership-side signaled, not auto-executed. This pack surfaces the
signal; `workflows/monthly_asset_management_review` confirms and adjusts cadence.

### Step 13. Top-3 watch items

Narrative synthesis. Name the three most consequential lease-up watch items this
month. Each watch item cites: property, metric slug, tolerance band reference, owning
workflow, proposed next action.

### Step 14. Confidence banner

Every reference surfaced with `as_of_date` and `status`. Any sample-tagged reference
is explicit. Cross-system posture summary: AppFolio primary for leasing funnel + lease
execution; Excel primary for rent comp + concession benchmark; Intacct primary for
NOI actuals post-close; Procore primary for CCO timestamp where applicable.

### Decision points and branches

- `lease_up_pace_vs_underwriting` (proposed) behind band two weeks running: cadence
  escalates to weekly; hand off to leasing_director + asset_mgmt_director. Do not
  propose pricing change here — route to `workflows/market_rent_refresh` for
  re-pricing analysis.
- `concession_depth_vs_market` (proposed) above tolerance: concession-vs-rent tradeoff
  sentinel — escalate to leasing_director + asset_mgmt_director. Do not propose a
  policy exception here — overlay governs.
- `model_unit_readiness_gap`: route to construction_manager + leasing_manager.
- First-renewal window risk spike (notice-given share above baseline): route to
  `workflows/renewal_retention`.
- `noi_ramp_vs_underwriting` (proposed) behind band two months running: escalate to
  investments_lead.
- Lender-reporting miss: route to asset_mgmt_director + reporting_finance_ops_lead;
  lender response composition through `workflows/executive_operating_summary_generation`.
- Equity-call timing drift: route to cfo_finance_leader + portfolio_manager.
- Stabilization crossover signaled: annotate handoff to
  `workflows/monthly_property_operating_review`.

## Metrics used

See frontmatter. Canonical metrics are inherited from the property-operations and
asset-management families. The proposed metrics (`lease_up_pace_vs_underwriting`,
`concession_depth_vs_market`, `broker_assist_rate`, `model_unit_tour_conversion`,
`first_renewal_window_retention_readiness`, `noi_ramp_vs_underwriting`,
`lender_reporting_compliance_status`, `equity_call_schedule_coverage`,
`cco_to_first_lease_days`) are lease-up-specific aggregations; formal promotion to
`_core/metrics.md` happens via a canonical change-control cycle. `cco_to_first_lease_days`
is shared with `workflows/development_pipeline_tracking`.

## Reference files used

- `reference/connectors/_core/stack_wave4/source_of_truth_matrix.md`
- `reference/connectors/adapters/appfolio_pms/normalized_contract.yaml`
- `reference/connectors/adapters/appfolio_pms/reconciliation_rules.md`
- `reference/connectors/adapters/appfolio_pms/runbooks/appfolio_common_issues.md`
- `reference/connectors/adapters/excel_market_surveys/normalized_contract.yaml`
- `reference/connectors/adapters/excel_market_surveys/reconciliation_rules.md`
- `reference/connectors/master_data/property_master_crosswalk.yaml`
- `reference/connectors/master_data/lease_crosswalk.yaml`
- `reference/connectors/master_data/resident_account_crosswalk.yaml`
- `reference/connectors/master_data/market_crosswalk.yaml`
- `reference/normalized/market_rents__{market}_mf.csv`
- `reference/normalized/concession_benchmarks__{market}_mf.csv`
- `reference/normalized/occupancy_benchmarks__{market}_mf.csv`
- `reference/normalized/marketing_channel_mix__middle_market.csv`
- `reference/normalized/schemas/reconciliation_tolerance_band.yaml`
- `reference/normalized/approval_threshold_defaults.csv`
- `reference/derived/funnel_conversion_benchmarks__middle_market.csv`
- `reference/derived/role_kpi_targets.csv`

## Escalation points

- Lease-up pace behind plan: leasing_manager -> regional_ops_director -> asset_mgmt_director
  -> investments_lead. Route pricing question to `workflows/market_rent_refresh`.
- Concession above policy during lease-up (row 13): leasing_manager -> asset_manager.
- Concession depth vs market beyond tolerance (concession-vs-rent tradeoff sentinel):
  leasing_director + asset_mgmt_director.
- Model unit readiness gap: construction_manager + leasing_manager -> asset_manager.
- Marketing rentup gap: leasing_manager + marketing_lead -> regional_ops_director.
- NOI ramp behind underwriting two months running: asset_mgmt_director -> investments_lead.
- Lender reporting compliance miss: asset_mgmt_director + reporting_finance_ops_lead;
  row 14 for any lender submission.
- Equity-call timing drift: cfo_finance_leader + portfolio_manager -> investments_lead.
- First-renewal window risk spike: leasing_manager -> regional_ops_director; route
  offer drafting to `workflows/renewal_retention`.
- Fair-housing flag (echoed from `workflows/lead_to_lease_funnel_review`): row 3.

## Required approvals

None for the tracker itself (informational / recommendation severity). Downstream
owning workflows carry their own gates:

- Policy-exceeding concession during lease-up (row 13).
- Fair-housing-flagged response (row 3).
- Lender final submission (row 14), composed in
  `workflows/executive_operating_summary_generation`.
- Pricing / rent-schedule change via `workflows/market_rent_refresh` overlay gate.
- Equity-call initiation via fund capital overlay.

## Failure modes

1. Conflating TCO with CCO for the ramp anchor. Fix: anchor is CCO when both exist
   and differ; annotate `cco_to_first_lease_days` (proposed) when CCO is the anchor.
2. Comparing actual lease-up pace against a changing underwriting curve. Fix: the
   underwriting curve is frozen at delivery; any change is logged via fund overlay
   and annotated explicitly.
3. Treating `concession_rate` and `concession_depth_vs_market` (proposed) as
   equivalent. Fix: `concession_rate` is an internal ledger metric; `concession_depth_vs_market`
   (proposed) is the comp-set-normalized tradeoff sentinel. Both are required.
4. Drafting renewal offers from within this pack. Fix: offer drafting is delegated to
   `workflows/renewal_retention`; this pack surfaces the queue only.
5. Authoring lender submissions. Fix: lender output is composed in
   `workflows/executive_operating_summary_generation` and gated at row 14.
6. Initiating or adjusting equity calls. Fix: call initiation is fund overlay; this
   pack reports posture only.
7. Proposing concession-policy exceptions. Fix: overlay concession governance; row 13.
8. Proposing screening-policy changes to close an approval_rate disparity. Fix:
   screening policy is overlay; fair-housing findings route through
   `workflows/lead_to_lease_funnel_review` at row 3.
9. Reporting ramp pace without a frozen underwriting curve. Fix: if underwriting curve
   is missing, refuse to compute `lease_up_pace_vs_underwriting` (proposed) and
   `noi_ramp_vs_underwriting` (proposed); surface the gap.
10. Sample overlay treated as authoritative rent comp or concession benchmark. Fix:
    confidence banner surfaces sample-tag explicitly; Excel-sourced references are
    the most stale-data-sensitive inputs in this pack.

## Edge cases

- **Model unit not ready at first-lease week.** Anchor (CCO) may have been achieved
  but the model unit finishes or staging are incomplete. Flag as
  `model_unit_readiness_gap` — route to construction_manager + leasing_manager.
  Do not propose a pricing offset. Traffic is expected to underperform until the
  model is usable; ramp-pace variance in this window is flagged with an explicit
  cause attribution so it does not trigger spurious
  `lease_up_pace_vs_underwriting` (proposed) alarms without context.
- **Marketing rentup gap.** Marketing launch is delayed or underfunded vs the
  underwriting assumption; total lead volume cannot produce the required executed
  leases at the planned conversion. Flag as `marketing_rentup_gap` — route to
  leasing_manager + marketing_lead; escalate to regional_ops_director if unresolved
  after one period. Do not infer the gap from pace alone; require cross-reference
  against the marketing_channel_mix benchmark + available spend data, else annotate
  as an attribution gap.
- **Concession-vs-rent tradeoff above tolerance.** Property is achieving headline
  leased_occupancy in-line with underwriting but at concession depth exceeding the
  comp-set benchmark — i.e., velocity is bought with concession dollars. Flag as
  `concession_rent_tradeoff_above_tolerance` — escalate to leasing_director +
  asset_mgmt_director -> investments_lead. The forward impact is on
  `noi_ramp_vs_underwriting` (proposed) and on first-renewal retention; annotate the
  linkage in the narrative.
- **First-renewal window straddles stabilization crossover.** Property crosses
  stabilization before the first-cohort leases renew. Continue tracking first-renewal
  retention here until the first-cohort renewals conclude, then hand off entirely.
- **Property delivered in phases.** Multi-building delivery with staggered CCO dates.
  Anchor is earliest CCO for aggregate pace; per-building anchors preserved in the
  narrative for per-building variance. Overlay governs whether the underwriting curve
  is phased or aggregate.
- **Lease-up capital reserve fully drawn.** Unfunded reserve drawn to zero while the
  property is still ramping; equity-call posture becomes operational rather than
  schedule-only. Escalate via equity_call_timing_drift path.
- **Lender reporting waiver in place.** Any `waived` status requires documented waiver
  pointer; missing waiver documentation flips status to `missed` for the operator
  view regardless of the lender-calendar marking.
- **Ground-up property with no prior operating history.** All T30/T90 baselines fall
  back to segment benchmark (`funnel_conversion_benchmarks__middle_market.csv`) with
  `confidence: low` annotation.
- **Post-delivery unit count change.** Final certified unit count differs from
  underwriting (e.g., combined unit, converted amenity space). Pace metrics rebase
  to certified unit count; underwriting curve is marked for fund-overlay
  reconciliation separately.

## Example invocations

1. "Run the monthly lease-up review for South Fork, month 4 post-delivery. Flag ramp pace vs underwriting."
2. "Concession depth vs market check for Willow Creek lease-up this month."
3. "Build the lease-up scorecard for South Fork; include NOI ramp, lender reporting status, and first-renewal readiness."
4. "What's the traffic source mix at Atlantic Grove this month? Include broker-assist rate."
5. "Is South Fork ready to hand off to steady-state monthly ops review?"

## Example outputs

### Output — Monthly lease-up review (abridged, South Fork, month 5 post-delivery, April 2026)

**Delivery anchor.** CCO 2025-11-18; month 5 post-delivery; `cco_to_first_lease_days`
(proposed) actual 14 days. Underwriting curve frozen at delivery.

**Lease-up pace.** `leased_occupancy` 48.3%; underwriting target at month 5 is 55.0%.
`lease_up_pace_vs_underwriting` (proposed) = 0.88. Below overlay tolerance band (0.90
floor per `reconciliation_tolerance_band.yaml::lease_up_pace_band`). Second
consecutive month below band; cadence escalates to weekly per trigger policy; hand off
to leasing_director + asset_mgmt_director.

**Concession posture.** `concession_rate` 62% of new leases carry a concession.
`concession_depth_vs_market` (proposed) +0.4 months offered vs market benchmark of
1.2 months (comp: `concession_benchmarks__charlotte_mf.csv@2026-03-31 (starter)`).
Within overlay tolerance this month but trending toward the concession-vs-rent
tradeoff ceiling.

**Funnel.** `lead_response_time` p50 within band. `tour_conversion` within band.
`application_conversion` within band. `approval_rate` within band; no fair-housing
disparity flag. `move_in_conversion` within band.

**Traffic source mix.** Paid search + broker-assist together carry 68% of executed
leases. `broker_assist_rate` (proposed) = 31%, above segment benchmark of ~18%.
Narrative: broker-assist overperforming; paid-search CPL rising. Marketing rentup
gap not yet flagged but watched.

**Model unit performance.** Ready since month 2. `model_unit_tour_conversion`
(proposed) = 46%, above overall `tour_conversion` of 38%. Model unit is an
above-average converter; no readiness gap.

**First-renewal readiness.** No leases yet in T60 first-renewal window (earliest
cohort first-renewal in month 12).

**NOI ramp.** Month 5 NOI at 61% of underwriting NOI ramp at month 5.
`noi_ramp_vs_underwriting` (proposed) = 0.61. Behind underwriting; concession depth
and operating expense ramp both contributing. Not yet escalated (requires two
consecutive months below); watched.

**Rent comp & market gap.** `market_to_lease_gap` within comp-set expected range;
headline rents in-line with comp set of stabilized product. Comp: `market_rents__charlotte_mf.csv@2026-03-31 (starter)`.

**Lender-reporting compliance.** Quarterly lease-up report due 2026-04-15.
`lender_reporting_compliance_status` (proposed) = `on_time` for the March report
submitted 2026-04-02. No misses.

**Equity-call schedule.** Forward 90-day: one call scheduled 2026-06-10 at
planned_amount $4.2M; committed_amount $4.2M. Coverage within band; no drift.

**Stabilization crossover.** Not reached. Overlay threshold is `leased_occupancy` >=
92% for 3 consecutive months. Handoff to `workflows/monthly_property_operating_review`
deferred.

**Top-3 watch items.**

1. `lease_up_pace_vs_underwriting` (proposed) = 0.88 second month running — weekly
   cadence begins; route pricing question to `workflows/market_rent_refresh`.
2. `concession_depth_vs_market` (proposed) +0.4 months above market — within
   tolerance but trending; narrative flags tradeoff risk.
3. `noi_ramp_vs_underwriting` (proposed) = 0.61 — watched; second-month flag triggers
   escalation to investments_lead.

**Confidence banner.**
```
References: source_of_truth_matrix@wave_4_authoritative,
appfolio_pms/normalized_contract@2026-04-08 (starter),
market_rents__charlotte_mf@2026-03-31 (starter),
concession_benchmarks__charlotte_mf@2026-03-31 (starter),
funnel_conversion_benchmarks__middle_market@2026-03-31 (sample),
marketing_channel_mix__middle_market@2026-03-31 (starter),
reconciliation_tolerance_band@2026-03-31 (sample),
role_kpi_targets@2026-03-31 (starter).
Proposed metrics (flagged): lease_up_pace_vs_underwriting,
concession_depth_vs_market, broker_assist_rate,
model_unit_tour_conversion, first_renewal_window_retention_readiness,
noi_ramp_vs_underwriting, lender_reporting_compliance_status,
equity_call_schedule_coverage, cco_to_first_lease_days.
Cross-system posture: AppFolio primary for funnel+lease execution;
Excel primary for rent comp+concession benchmark; Intacct primary
for NOI actuals post-close; Procore primary for CCO timestamp.
```
