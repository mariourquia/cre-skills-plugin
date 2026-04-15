# Example — Lease-Up First Period (abridged)

**Prompt:** "Build the monthly lease-up review for South Fork, month 5 post-delivery. Include ramp vs underwriting, NOI ramp, lender reporting status, and first-renewal readiness."

**Inputs:** AppFolio rent roll + lease register + lease-event log + CRM funnel + charge/concession ledger + Excel rent comp + concession benchmark + underwriting lease-up plan + underwriting NOI ramp + loan covenant + reporting calendar + fund equity-call schedule + marketing-channel mix reference + property_master_crosswalk + lease_crosswalk + resident_account_crosswalk + market_crosswalk + reconciliation_tolerance_band + approval_threshold_defaults + funnel_conversion_benchmarks + role_kpi_targets.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: suburban_mid_rise
- lifecycle_stage: lease_up
- management_mode: self_managed
- market: Charlotte
- property_id: PROP_SOUTH_FORK
- org_id: (from overlay)
- loan_id: LOAN_SOUTH_FORK_CTP (construction-to-permanent)
- fund_id: FUND_CORE_II
- role: asset_manager
- output_type: dashboard + memo
- decision_severity: recommendation

## Expected packs loaded

- `workflows/lease_up_first_period/`
- `workflows/lead_to_lease_funnel_review/` (child — funnel + fair-housing branch; read-only here)
- `workflows/market_rent_refresh/` (child — conditional handoff for pricing question)
- `workflows/move_in_administration/` (child — move-in conversion context)
- `workflows/renewal_retention/` (child — first-renewal offer drafting, queued, not invoked)
- `workflows/executive_operating_summary_generation/` (downstream — lender submission composition if needed)
- `overlays/segments/middle_market/`

## Expected references

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
- `reference/normalized/market_rents__charlotte_mf.csv`
- `reference/normalized/concession_benchmarks__charlotte_mf.csv`
- `reference/normalized/marketing_channel_mix__middle_market.csv`
- `reference/normalized/schemas/reconciliation_tolerance_band.yaml`
- `reference/normalized/approval_threshold_defaults.csv`
- `reference/derived/funnel_conversion_benchmarks__middle_market.csv`
- `reference/derived/role_kpi_targets.csv`

## Gates potentially triggered (elsewhere)

- `workflows/lead_to_lease_funnel_review`: row 3 (fair-housing) — not triggered this run.
- Overlay concession governance: row 13 (policy-exceeding concession during lease-up) — not triggered this run; one lease at policy edge observed.
- `workflows/executive_operating_summary_generation`: row 14 (lender final submission) — not triggered; quarterly report on-time.
- `workflows/market_rent_refresh`: overlay gate for pricing/rent-schedule change — queued (second month ramp-below-band triggers re-pricing review).

## Expected output shape

- Lease-up pace dashboard: `lease_up_pace_vs_underwriting` (proposed),
  `stabilization_pace_vs_plan`, `lease_up_pace_post_delivery`,
  `preleased_occupancy`, `leased_occupancy`, `economic_occupancy`,
  `cco_to_first_lease_days` (proposed).
- Concession posture KPI table: `concession_rate`, `concession_depth_vs_market`
  (proposed), policy ceiling check.
- Funnel posture KPI table: `lead_response_time`, `tour_conversion`,
  `application_conversion`, `approval_rate`, `move_in_conversion`,
  `broker_assist_rate` (proposed), `model_unit_tour_conversion` (proposed).
- Traffic source mix: source-by-source funnel breakdown + executed-lease share.
- Model unit performance memo.
- First-renewal readiness KPI table (empty this run — earliest cohort not yet in
  T60 window).
- NOI ramp posture KPI table: `noi_ramp_vs_underwriting` (proposed),
  `noi_margin`, `revenue_variance_to_budget`, `expense_variance_to_budget`.
- Rent comp & market gap KPI table: `rent_growth_new_lease`, `market_to_lease_gap`.
- Lender-reporting compliance KPI table: per-submission
  `lender_reporting_compliance_status` (proposed).
- Equity-call schedule KPI table: forward 90-day
  `equity_call_schedule_coverage` (proposed).
- Stabilization crossover check memo.
- Narrative memo with top-3 watch items.

## Confidence banner pattern

```
References: source_of_truth_matrix@wave_4_authoritative,
appfolio_pms/normalized_contract@2026-04-08 (starter),
excel_market_surveys/normalized_contract@2026-04-08 (starter),
market_rents__charlotte_mf@2026-03-31 (starter),
concession_benchmarks__charlotte_mf@2026-03-31 (starter),
funnel_conversion_benchmarks__middle_market@2026-03-31 (sample),
marketing_channel_mix__middle_market@2026-03-31 (starter),
reconciliation_tolerance_band@2026-03-31 (sample),
approval_threshold_defaults@2026-03-31 (starter),
role_kpi_targets@2026-03-31 (starter),
property_master_crosswalk@2026-04-08 (starter),
lease_crosswalk@2026-04-08 (starter),
market_crosswalk@2026-04-08 (starter).
Proposed metrics (flagged): lease_up_pace_vs_underwriting,
concession_depth_vs_market, broker_assist_rate,
model_unit_tour_conversion, first_renewal_window_retention_readiness,
noi_ramp_vs_underwriting, lender_reporting_compliance_status,
equity_call_schedule_coverage, cco_to_first_lease_days.
Canonical extensions required (none for this pack; lease_up_plan_ref
already declared on DevelopmentProject in ontology.md).
Cross-system posture: AppFolio primary for funnel+lease execution;
Excel primary for rent comp+concession benchmark; Intacct primary
for NOI actuals post-close; Procore primary for CCO timestamp.
```

## Example narrative excerpt

South Fork has crossed the halfway mark of its lease-up window. Month 5 ramp
posture shows `lease_up_pace_vs_underwriting` (proposed) = 0.88 — a second
consecutive month below the 0.90 overlay tolerance floor per
`reconciliation_tolerance_band.yaml::lease_up_pace_band`. The weekly cadence
escalates per trigger policy; the leasing_director and asset_mgmt_director are
brought into the monthly review rhythm, and the pricing question is routed to
`workflows/market_rent_refresh` for re-pricing analysis. This pack does not
propose a price change here.

Concession posture sits within band but is trending. `concession_rate` at 62%
of new leases; `concession_depth_vs_market` (proposed) +0.4 months above the
market benchmark of 1.2 months (Excel comp as-of 2026-03-31 starter). The
concession-vs-rent tradeoff sentinel is armed but not tripped — narrative flags
the trajectory and the forward linkage into
`noi_ramp_vs_underwriting` (proposed), currently at 0.61, and into first-renewal
posture when the first cohort begins T60 notice in month 12.

Funnel posture is clean. Response time, tour conversion, application
conversion, approval rate, and move-in conversion are all within band. The
`approval_rate` trailing-90-day disparity scan is clean — no fair-housing flag
echoed from `workflows/lead_to_lease_funnel_review` this run. Every
`approval_outcome` in the sample cites a `policy_ref`.

Traffic source mix shows paid search + broker-assist carrying 68% of executed
leases; `broker_assist_rate` (proposed) = 31%, above segment benchmark ~18%.
The model unit has been ready since month 2; `model_unit_tour_conversion`
(proposed) runs above overall tour conversion, confirming the model is an
above-average converter. No marketing rentup gap flagged — total lead volume is
tracking plan, the friction is pricing-side not volume-side.

NOI ramp is behind underwriting; month 5 actual NOI at 61% of the
underwriting ramp at month 5. Concession depth and operating-expense ramp are
the primary contributors per the variance narrative on `revenue_variance_to_budget`
and `expense_variance_to_budget`. Not yet escalated — escalation to
investments_lead requires two consecutive months below, which is the next
decision point.

Lender-reporting compliance is clean: the quarterly lease-up report due
2026-04-15 was submitted 2026-04-02 on-time. Forward equity-call posture is
within band: one call scheduled 2026-06-10 at $4.2M planned,
committed_amount = planned_amount. The fund is tracking to deploy.

Stabilization crossover is not reached. The overlay threshold is sustained
`leased_occupancy` >= 92% for 3 consecutive months; South Fork is at 48.3%.
The handoff to `workflows/monthly_property_operating_review` is deferred;
`lease_up_first_period` remains the primary monthly cadence.

Top-3 watch items this month: (1) `lease_up_pace_vs_underwriting` below
tolerance two months running — weekly cadence begins, pricing question routed;
(2) `concession_depth_vs_market` trending above comp-set benchmark — the
concession-vs-rent tradeoff is the forward risk to NOI ramp and first-renewal
posture; (3) `noi_ramp_vs_underwriting` at 0.61 — watched; second-month flag
will trigger escalation to investments_lead.
