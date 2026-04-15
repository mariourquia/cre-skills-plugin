# Canonical Metrics

Every metric listed here conforms to `schemas/metric_contract.yaml`. A pack may reference a metric by slug; a pack may not silently redefine a metric. Overrides must be declared in an overlay's `overlay.yaml` under `overrides[].target_kind: metric_threshold | metric_target_band | metric_filters_default`.

When adding a metric, update `alias_registry.yaml` in the same commit.

---

## Property Operations family

### physical_occupancy

```yaml
name: Physical Occupancy
slug: physical_occupancy
description: |
  Share of rentable units physically occupied by a resident on a given date.
  Does not reflect whether the unit is leased or noticed.
family: property_operations
grain: property
time_basis: as_of_date
scenario: [actual, budget, forecast, underwriting]
unit: percent
numerator: count of units with status in [occupied, notice_occupied]
denominator: unit_count_rentable
filters_default:
  - exclude units with status in [model, employee, down, admin]
inclusions: []
exclusions: [model_units, employee_units, down_units, admin_units]
rollup_rule: weighted_by_unit_count_rentable
null_handling: |
  If unit statuses are missing, metric is undefined (not zero). Surface missing.
source_fields: [Unit.status, Unit.unit_count_rentable]
qa_rule: |
  physical_occupancy should be between 0 and 1. physical_occupancy > leased_occupancy by
  more than 3 pts is a QA flag (implies delayed leasing updates).
reconciliation_rule: |
  Reconciles to rent roll snapshot as of the same date. Variance > 1 pt requires investigation.
aliases: [occupancy_physical, actual_occupancy]
overlays_may_override: [target_band]
open_questions: []
```

### leased_occupancy

```yaml
name: Leased Occupancy
slug: leased_occupancy
description: |
  Share of rentable units covered by an in-effect or approved-to-move-in lease on a given date.
  Includes units where a lease has been executed but the resident has not yet moved in.
family: property_operations
grain: property
time_basis: as_of_date
scenario: [actual, budget, forecast, underwriting]
unit: percent
numerator: |
  count of units where a Lease exists with status in
  [executed, in_effect, renewing] and that lease covers the as_of_date (or starts within
  the preleased_window).
denominator: unit_count_rentable
filters_default: [exclude model, employee, down, admin]
inclusions: [units with signed lease not yet moved in, within preleased_window]
exclusions: [same as physical_occupancy]
rollup_rule: weighted_by_unit_count_rentable
null_handling: Surface missing.
source_fields: [Unit.status, Lease.status, Lease.start_date, Lease.end_date]
qa_rule: leased_occupancy should be >= physical_occupancy under normal operations.
reconciliation_rule: Reconciles to leasing pipeline report.
aliases: [occupancy_leased]
overlays_may_override: [target_band, inclusions]
open_questions:
  - preleased_window default is 30 days; confirm per org overlay.
```

### economic_occupancy

```yaml
name: Economic Occupancy
slug: economic_occupancy
description: |
  Share of gross potential rent collected as base rent in the period.
  Captures the combined impact of vacancy, concessions, loss-to-lease, delinquency, and bad debt.
family: property_operations
grain: property
time_basis: period_cumulative
time_basis_window: calendar_month
scenario: [actual, budget, forecast, underwriting]
unit: percent
numerator: base_rent_collected (net of concessions, bad_debt_writedowns, delinquency_writedowns)
denominator: gross_potential_rent (sum of asking_rent across all rentable units for the period)
filters_default: [exclude model, employee, down, admin]
inclusions: [base rent only; excludes fees]
exclusions: [pet_fees, utility_charges, late_fees, nsf_fees, damage_charges]
rollup_rule: weighted_by_gross_potential_rent
null_handling: Surface missing if gross_potential_rent or base_rent_collected unknown.
source_fields: [Charge.amount (rent/base_rent), Payment.amount, Unit.asking_rent]
qa_rule: economic_occupancy < physical_occupancy is expected. Deviation > 10 pts warrants review.
reconciliation_rule: Reconciles to GL base rent revenue line.
aliases: [econ_occ, collected_occupancy]
overlays_may_override: [target_band]
open_questions: []
```

### notice_exposure

```yaml
name: Notice Exposure
slug: notice_exposure
description: |
  Share of rentable units under a notice to vacate and not yet re-leased, as of date.
  Measures forward-looking risk to occupancy.
family: property_operations
grain: property
time_basis: as_of_date
scenario: [actual, forecast]
unit: percent
numerator: |
  count of units in status [notice_occupied, notice_unrented] without an executed lease starting
  within reoccupancy_window of notice.vacate_date.
denominator: unit_count_rentable
filters_default: [exclude model, employee, down, admin]
inclusions: []
exclusions: []
rollup_rule: weighted_by_unit_count_rentable
null_handling: Surface missing.
source_fields: [Unit.status, NoticeEvent.vacate_date, Lease.start_date, Lease.status]
qa_rule: notice_exposure + leased_occupancy should not exceed 1 + preleased_buffer.
reconciliation_rule: Reconciles to rollover schedule.
aliases: [exposure, open_exposure, ntv_exposure]
overlays_may_override: [target_band]
open_questions:
  - reoccupancy_window default is 30 days.
```

### preleased_occupancy

```yaml
name: Preleased Occupancy
slug: preleased_occupancy
description: |
  Share of rentable units covered by an executed lease whose start_date is in the future,
  within the preleased_window.
family: property_operations
grain: property
time_basis: as_of_date
scenario: [actual]
unit: percent
numerator: count of units with executed Lease where Lease.start_date > today and <= today + preleased_window.
denominator: unit_count_rentable
filters_default: [exclude model, employee, down, admin]
rollup_rule: weighted_by_unit_count_rentable
null_handling: Surface missing.
source_fields: [Unit.status, Lease.status, Lease.start_date]
qa_rule: Must be between 0 and 1.
reconciliation_rule: Reconciles to leasing pipeline.
aliases: [pre_leased]
overlays_may_override: [target_band]
open_questions:
  - preleased_window default is 30 days; lease_up overlay uses 60 days.
```

### lead_response_time

```yaml
name: Lead Response Time
slug: lead_response_time
description: |
  Minutes between lead creation (inquiry) and first outbound contact.
family: property_operations
grain: property
time_basis: rolling_window
time_basis_window: T30_days
scenario: [actual, benchmark]
unit: minutes
numerator: sum of (first_contact_ts - inquiry_ts) across leads in window
denominator: count of leads with first_contact_ts populated
filters_default: [exclude test_leads, exclude duplicates]
rollup_rule: weighted_by_lead_count
null_handling: Leads without first_contact_ts are excluded from numerator/denominator but counted as missed if first_contact_ts is null and inquiry_ts > 24h ago.
source_fields: [Lead.inquiry_date, Lead.first_contact_ts]
qa_rule: median should be < 4 hours; p95 < 24 hours.
reconciliation_rule: Reconciles to CRM lead log.
aliases: [response_time, lead_response]
overlays_may_override: [target_band]
open_questions: []
```

### tour_conversion

```yaml
name: Tour Conversion
slug: tour_conversion
description: |
  Share of tours that result in an application within 14 days.
family: property_operations
grain: property
time_basis: rolling_window
time_basis_window: T90_days
scenario: [actual, benchmark]
unit: percent
numerator: count of tours with an application within 14 days
denominator: count of tours (excluding no_shows)
filters_default: [exclude test_tours]
rollup_rule: weighted_by_tour_count
null_handling: Surface missing.
source_fields: [Tour.conducted_date, Tour.outcome, Application.applied_date, Application.lead_id]
qa_rule: Should be between 0 and 1.
reconciliation_rule: Reconciles to CRM funnel.
aliases: [tour_to_app, tour_to_application]
overlays_may_override: [target_band]
open_questions: []
```

### application_conversion

```yaml
name: Application Conversion
slug: application_conversion
description: Share of applications that reach approved status.
family: property_operations
grain: property
time_basis: rolling_window
time_basis_window: T90_days
scenario: [actual, benchmark]
unit: percent
numerator: count of applications with ApprovalOutcome.outcome in [approved, approved_with_conditions]
denominator: count of applications submitted
rollup_rule: weighted_by_application_count
null_handling: Surface missing.
source_fields: [Application.approval_status, ApprovalOutcome.outcome]
qa_rule: 0 to 1. Dips require review for screening policy issues.
reconciliation_rule: Reconciles to screening vendor report.
aliases: [app_conversion, approval_rate_applicant]
overlays_may_override: [target_band]
open_questions: []
```

### approval_rate

```yaml
name: Screening Approval Rate
slug: approval_rate
description: Share of completed applications approved under policy.
family: property_operations
grain: property
time_basis: rolling_window
time_basis_window: T90_days
scenario: [actual, benchmark]
unit: percent
numerator: count of applications approved
denominator: count of applications with final decision (approved + declined)
rollup_rule: weighted_by_application_count
null_handling: Surface missing.
source_fields: [ApprovalOutcome.outcome]
qa_rule: Watch for discrimination patterns vs. historical baseline; fair-housing review if >10pt swing.
reconciliation_rule: Reconciles to screening vendor.
aliases: [screening_approval_rate]
overlays_may_override: [target_band]
open_questions: []
```

### move_in_conversion

```yaml
name: Move-In Conversion
slug: move_in_conversion
description: Share of approved applications that become executed leases and move in.
family: property_operations
grain: property
time_basis: rolling_window
time_basis_window: T90_days
scenario: [actual, benchmark]
unit: percent
numerator: count of approved applications with a corresponding move_in event
denominator: count of approved applications
rollup_rule: weighted_by_application_count
null_handling: Surface missing.
source_fields: [ApprovalOutcome.outcome, LeaseEvent.event_type (move_in)]
qa_rule: Gap vs. approval_rate flags lost-approvals issue.
reconciliation_rule: Reconciles to lease ledger.
aliases: [approved_to_moved_in]
overlays_may_override: [target_band]
open_questions: []
```

### renewal_offer_rate

```yaml
name: Renewal Offer Rate
slug: renewal_offer_rate
description: Share of expiring leases that receive a renewal offer before expiration window.
family: property_operations
grain: property
time_basis: rolling_window
time_basis_window: T90_days
scenario: [actual]
unit: percent
numerator: count of expiring leases with renewal_offered event at least renewal_offer_lead_time before end_date
denominator: count of expiring leases in the window
rollup_rule: weighted_by_lease_count
null_handling: Surface missing.
source_fields: [Lease.end_date, LeaseEvent.renewal_offered]
qa_rule: Target 100%. Any gap triggers process review.
reconciliation_rule: Reconciles to renewal log.
aliases: [renewal_reach_rate]
overlays_may_override: [target_band]
open_questions:
  - renewal_offer_lead_time default is 90 days.
```

### renewal_acceptance_rate

```yaml
name: Renewal Acceptance Rate
slug: renewal_acceptance_rate
description: Share of renewal offers accepted.
family: property_operations
grain: property
time_basis: rolling_window
time_basis_window: T90_days
scenario: [actual, benchmark]
unit: percent
numerator: count of LeaseEvents with event_type=renewal_accepted
denominator: count of LeaseEvents with event_type=renewal_offered
rollup_rule: weighted_by_offer_count
null_handling: Surface missing.
source_fields: [LeaseEvent.event_type]
qa_rule: Dips vs. benchmark trigger retention review.
reconciliation_rule: Reconciles to renewal log.
aliases: [renewal_conversion]
overlays_may_override: [target_band]
open_questions: []
```

### turnover_rate

```yaml
name: Turnover Rate
slug: turnover_rate
description: Annualized share of units that turn over in a period (move_out events / total units).
family: property_operations
grain: property
time_basis: rolling_window
time_basis_window: T12_months
scenario: [actual, benchmark]
unit: percent
numerator: count of move_out events in T12 months
denominator: unit_count_rentable
rollup_rule: weighted_by_unit_count_rentable
null_handling: Surface missing.
source_fields: [LeaseEvent.event_type (move_out), Unit.unit_count_rentable]
qa_rule: Expected 40-60% for middle-market stabilized. Outside triggers review.
reconciliation_rule: Reconciles to move-out log.
aliases: [unit_turnover]
overlays_may_override: [target_band]
open_questions:
  - "Definition of turnover for transferred residents: we exclude transfers (same household remains)."
```

### average_days_vacant

```yaml
name: Average Days Vacant
slug: average_days_vacant
description: Average number of days a unit is vacant per turn event.
family: property_operations
grain: property
time_basis: rolling_window
time_basis_window: T90_days
scenario: [actual, benchmark]
unit: days
numerator: sum of (lease.start_date - prior_move_out_date) across re-leased units
denominator: count of re-leased units in window
rollup_rule: weighted_by_turn_count
null_handling: Exclude units still vacant at window end.
source_fields: [LeaseEvent.move_out, Lease.start_date]
qa_rule: "> 30 days triggers turn/marketing review."
reconciliation_rule: Reconciles to turn log.
aliases: [days_vacant]
overlays_may_override: [target_band]
open_questions: []
```

### make_ready_days

```yaml
name: Make-Ready Days
slug: make_ready_days
description: Days from move-out to unit marked ready-to-show.
family: property_operations
grain: property
time_basis: rolling_window
time_basis_window: T90_days
scenario: [actual, benchmark]
unit: days
numerator: sum of (turn.actual_ready_date - turn.move_out_date)
denominator: count of completed turns in window
rollup_rule: weighted_by_turn_count
null_handling: Exclude turns not yet marked ready.
source_fields: [TurnProject.move_out_date, TurnProject.actual_ready_date]
qa_rule: p95 > 14 days triggers review.
reconciliation_rule: Reconciles to turn log.
aliases: [ready_days, turn_days]
overlays_may_override: [target_band]
open_questions:
  - Distinguish classic turn vs. classic-to-renovated turn (different target bands).
```

### open_work_orders

```yaml
name: Open Work Orders
slug: open_work_orders
description: Count of work orders in non-terminal status as of date.
family: property_operations
grain: property
time_basis: as_of_date
scenario: [actual]
unit: count
numerator: count of WorkOrders with status not in [completed, closed, deferred]
denominator: null
filters_default: [exclude pm_generated]
rollup_rule: sum
null_handling: Zero is valid.
source_fields: [WorkOrder.status]
qa_rule: Growth period-over-period triggers review.
reconciliation_rule: Reconciles to maintenance system.
aliases: [open_wos]
overlays_may_override: [target_band]
open_questions: []
```

### work_order_aging

```yaml
name: Work Order Aging
slug: work_order_aging
description: Age in days since reported for open work orders, bucketed.
family: property_operations
grain: property
time_basis: as_of_date
scenario: [actual]
unit: distribution
numerator: null
denominator: null
filters_default: [exclude pm_generated]
rollup_rule: not_rollupable (must be recomputed at target grain)
null_handling: Surface missing.
source_fields: [WorkOrder.reported_date, WorkOrder.status]
qa_rule: P1_safety in age bucket > 24h is critical.
reconciliation_rule: Reconciles to maintenance system.
aliases: [wo_aging]
overlays_may_override: [filters_default]
open_questions: []
```

### repeat_work_order_rate

```yaml
name: Repeat Work Order Rate
slug: repeat_work_order_rate
description: Share of closed work orders with a re-open for the same unit+category within 30 days.
family: property_operations
grain: property
time_basis: rolling_window
time_basis_window: T90_days
scenario: [actual, benchmark]
unit: percent
numerator: count of closed WOs with matching WO within 30 days (same unit, same category)
denominator: count of closed WOs
rollup_rule: weighted_by_wo_count
null_handling: Surface missing.
source_fields: [WorkOrder.unit_id, WorkOrder.category, WorkOrder.completed_date]
qa_rule: "> 8% triggers quality review."
reconciliation_rule: Reconciles to maintenance system.
aliases: [wo_rework_rate]
overlays_may_override: [target_band]
open_questions: []
```

### delinquency_rate_30plus

```yaml
name: Delinquency Rate 30+
slug: delinquency_rate_30plus
description: Share of occupied units with resident ledger balance aged 30+ days.
family: property_operations
grain: property
time_basis: as_of_date
scenario: [actual, benchmark]
unit: percent
numerator: count of occupied units with ledger balance aged 30+ days above delinquency_threshold_dollars
denominator: count of occupied units
filters_default: [exclude write-offs already processed]
rollup_rule: weighted_by_unit_count
null_handling: Surface missing.
source_fields: [DelinquencyCase.stage, ResidentAccount.ledger_balance]
qa_rule: Spike week-over-week flags collections review.
reconciliation_rule: Reconciles to AR aging.
aliases: [delinq_30]
overlays_may_override: [target_band]
open_questions:
  - delinquency_threshold_dollars default is $25 per org overlay.
```

### collections_rate

```yaml
name: Collections Rate
slug: collections_rate
description: Share of billed rent collected in the billing period.
family: property_operations
grain: property
time_basis: period_cumulative
time_basis_window: calendar_month
scenario: [actual, benchmark]
unit: percent
numerator: rent_collected_current_month (base rent portion only)
denominator: rent_billed_current_month
filters_default: []
rollup_rule: weighted_by_rent_billed
null_handling: Surface missing.
source_fields: [Charge.amount (rent), Payment.amount]
qa_rule: < 97% for middle-market triggers review.
reconciliation_rule: Reconciles to GL and bank deposits.
aliases: [rent_collection_rate]
overlays_may_override: [target_band]
open_questions: []
```

### bad_debt_rate

```yaml
name: Bad Debt Rate
slug: bad_debt_rate
description: Share of gross potential rent written off in the period.
family: property_operations
grain: property
time_basis: rolling_window
time_basis_window: T12_months
scenario: [actual, benchmark, budget]
unit: percent
numerator: write_offs_period (base rent portion only)
denominator: gross_potential_rent_period
rollup_rule: weighted_by_gross_potential_rent
null_handling: Surface missing.
source_fields: [Charge.amount (write_off), GPR]
qa_rule: "> 1% for middle-market triggers review."
reconciliation_rule: Reconciles to GL.
aliases: [write_off_rate]
overlays_may_override: [target_band]
open_questions: []
```

### concession_rate

```yaml
name: Concession Rate
slug: concession_rate
description: Concessions as a share of gross potential rent (new leases only by default).
family: property_operations
grain: property
time_basis: period_cumulative
time_basis_window: calendar_month
scenario: [actual, benchmark, budget]
unit: percent
numerator: sum of concessions on new leases executed in period
denominator: sum of gross_potential_rent on new leases executed in period
rollup_rule: weighted_by_gross_potential_rent
null_handling: Surface missing.
source_fields: [Lease.concessions_total, Lease.base_rent_monthly, Lease.term_months]
qa_rule: "> market benchmark + 2pt triggers pricing review."
reconciliation_rule: Reconciles to GL.
aliases: [concessions_pct]
overlays_may_override: [target_band]
open_questions:
  - Renewal concessions tracked separately via renewal_concession_rate (not yet defined; open TBD).
```

### rent_growth_new_lease

```yaml
name: Rent Growth — New Lease
slug: rent_growth_new_lease
description: |
  Year-over-year change in effective rent on new leases vs. the prior resident's effective rent for the same unit.
family: property_operations
grain: property
time_basis: rolling_window
time_basis_window: T90_days
scenario: [actual, budget, underwriting]
unit: percent
numerator: sum of (new_lease_effective_rent - prior_lease_effective_rent)
denominator: sum of prior_lease_effective_rent
filters_default: [exclude unit-type conversions, exclude renovated-to-classic or classic-to-renovated]
rollup_rule: weighted_by_prior_rent
null_handling: If prior lease missing (first lease-up), exclude.
source_fields: [Lease.base_rent_monthly, Lease.concessions_total, Lease.term_months]
qa_rule: Outside +/- 20% flags review.
reconciliation_rule: Reconciles to trade-out report.
aliases: [new_lease_trade_out, new_lease_rent_growth]
overlays_may_override: [target_band]
open_questions:
  - "Effective rent definition: base_rent - (concessions / term_months). Lock in alias_registry."
```

### rent_growth_renewal

```yaml
name: Rent Growth — Renewal
slug: rent_growth_renewal
description: YoY change in effective rent on renewal vs. prior lease effective rent, same resident.
family: property_operations
grain: property
time_basis: rolling_window
time_basis_window: T90_days
scenario: [actual, budget, underwriting]
unit: percent
numerator: sum of (renewal_effective_rent - prior_lease_effective_rent)
denominator: sum of prior_lease_effective_rent
filters_default: []
rollup_rule: weighted_by_prior_rent
null_handling: Surface missing.
source_fields: [Lease.base_rent_monthly, Lease.concessions_total, Lease.prior_lease_id]
qa_rule: Outside +/- 15% flags review.
reconciliation_rule: Reconciles to renewal log.
aliases: [renewal_trade_out, renewal_rent_growth]
overlays_may_override: [target_band]
open_questions: []
```

### blended_lease_trade_out

```yaml
name: Blended Lease Trade-Out
slug: blended_lease_trade_out
description: Weighted blend of new-lease and renewal rent growth.
family: property_operations
grain: property
time_basis: rolling_window
time_basis_window: T90_days
scenario: [actual, benchmark, budget, underwriting]
unit: percent
numerator: (new_lease_trade_out_$ + renewal_trade_out_$)
denominator: (new_lease_prior_rent_$ + renewal_prior_rent_$)
rollup_rule: weighted_by_prior_rent
null_handling: Surface missing.
source_fields: [Lease.base_rent_monthly, Lease.is_renewal, Lease.prior_lease_id, Lease.concessions_total]
qa_rule: Gap vs. rent_growth_new_lease > 5pt flags renewal strategy review.
reconciliation_rule: Reconciles to trade-out report.
aliases: [blended_rent_growth]
overlays_may_override: [target_band]
open_questions: []
```

### market_to_lease_gap

```yaml
name: Market-to-Lease Gap
slug: market_to_lease_gap
description: |
  Difference between market_rent (from reference) and in-place effective rent, as a percent of market rent.
family: property_operations
grain: property
time_basis: as_of_date
scenario: [actual]
unit: percent
numerator: (market_rent_weighted - effective_rent_in_place_weighted)
denominator: market_rent_weighted
filters_default: []
rollup_rule: weighted_by_unit_count
null_handling: Requires market_rent reference; surface missing reference if absent.
source_fields: [Lease.base_rent_monthly, Lease.concessions_total, reference/normalized/market_rents.csv]
qa_rule: Negative values flag possible market/rent pricing issue.
reconciliation_rule: Reconciles to market survey.
aliases: [rent_to_market_gap]
overlays_may_override: [target_band]
open_questions: []
```

### loss_to_lease

```yaml
name: Loss to Lease
slug: loss_to_lease
description: |
  (Gross potential rent at market - gross potential rent at in-place asking) / GPR at market.
  Captures revenue upside available at full rollover to market.
family: property_operations
grain: property
time_basis: as_of_date
scenario: [actual, underwriting]
unit: percent
numerator: (GPR_at_market - GPR_at_asking)
denominator: GPR_at_market
filters_default: [exclude model, employee, down, admin]
rollup_rule: weighted_by_gpr_at_market
null_handling: Requires market_rent reference.
source_fields: [Unit.asking_rent, reference/normalized/market_rents.csv]
qa_rule: Persistently negative values flag asking rents above market.
reconciliation_rule: Reconciles to rent roll and market survey.
aliases: [ltl]
overlays_may_override: [target_band]
open_questions: []
```

### payroll_per_unit

```yaml
name: Payroll per Unit
slug: payroll_per_unit
description: Annualized site payroll (salary + burden) per rentable unit.
family: property_operations
grain: property
time_basis: rolling_window
time_basis_window: T12_months
scenario: [actual, budget, forecast, benchmark]
unit: dollars_per_unit
numerator: site_payroll_t12 (salary + burden)
denominator: unit_count_rentable
filters_default: [exclude corporate allocations]
rollup_rule: weighted_by_unit_count_rentable
null_handling: Surface missing.
source_fields: [BudgetLine/ForecastLine with chart_ref=payroll, Property.unit_count_rentable]
qa_rule: Variance to benchmark > 15% flags staffing review.
reconciliation_rule: Reconciles to payroll register.
aliases: [payroll_per_door]
overlays_may_override: [target_band]
open_questions:
  - Burden rate from reference/normalized/payroll_assumptions.csv.
```

### rm_per_unit

```yaml
name: R&M per Unit
slug: rm_per_unit
description: Annualized repairs and maintenance expense per rentable unit.
family: property_operations
grain: property
time_basis: rolling_window
time_basis_window: T12_months
scenario: [actual, budget, forecast, benchmark]
unit: dollars_per_unit
numerator: rm_t12
denominator: unit_count_rentable
filters_default: [exclude capex]
rollup_rule: weighted_by_unit_count_rentable
null_handling: Surface missing.
source_fields: [BudgetLine/ForecastLine chart_ref=rm_*]
qa_rule: Variance to benchmark > 20% flags review.
reconciliation_rule: Reconciles to GL.
aliases: [rm_per_door]
overlays_may_override: [target_band]
open_questions: []
```

### utilities_per_unit

```yaml
name: Utilities per Unit
slug: utilities_per_unit
description: Annualized net utilities expense per rentable unit (after RUBS recovery).
family: property_operations
grain: property
time_basis: rolling_window
time_basis_window: T12_months
scenario: [actual, budget, forecast, benchmark]
unit: dollars_per_unit
numerator: utilities_expense_t12 - rubs_recovery_t12
denominator: unit_count_rentable
filters_default: []
rollup_rule: weighted_by_unit_count_rentable
null_handling: Surface missing.
source_fields: [BudgetLine/ForecastLine chart_ref=util_*, rubs]
qa_rule: Seasonal variance expected; YoY > 10% flags review.
reconciliation_rule: Reconciles to GL and utility bills.
aliases: [utils_per_door]
overlays_may_override: [target_band]
open_questions: []
```

### controllable_opex_per_unit

```yaml
name: Controllable Opex per Unit
slug: controllable_opex_per_unit
description: Site-controllable operating expense per rentable unit (excludes property tax, insurance, management fee).
family: property_operations
grain: property
time_basis: rolling_window
time_basis_window: T12_months
scenario: [actual, budget, forecast, benchmark]
unit: dollars_per_unit
numerator: (payroll + r_and_m + utilities_net + marketing + admin + contract_services) t12
denominator: unit_count_rentable
filters_default: [exclude property_tax, insurance, management_fee, debt_service, depreciation]
rollup_rule: weighted_by_unit_count_rentable
null_handling: Surface missing.
source_fields: [BudgetLine/ForecastLine subset]
qa_rule: Variance to benchmark > 15% flags review.
reconciliation_rule: Reconciles to GL.
aliases: [ctrl_opex_per_door]
overlays_may_override: [target_band]
open_questions:
  - Management fee treated as non-controllable at site level; treated as controllable at owner level.
```

---

## Asset Management family

### revenue_variance_to_budget

```yaml
name: Revenue Variance to Budget
slug: revenue_variance_to_budget
description: |
  (Actual revenue - budgeted revenue) for the period. Reported in dollars and as percent.
family: asset_management
grain: property
time_basis: period_cumulative
time_basis_window: calendar_month
scenario: [actual]
unit: dollars
numerator: revenue_actual - revenue_budget
denominator: null
rollup_rule: sum
null_handling: Surface missing.
source_fields: [BudgetLine, actual GL revenue]
qa_rule: MTD and YTD views should reconcile.
reconciliation_rule: Reconciles to GL.
aliases: [rev_var]
overlays_may_override: [target_band]
open_questions: []
```

### expense_variance_to_budget

```yaml
name: Expense Variance to Budget
slug: expense_variance_to_budget
description: (Actual expense - budgeted expense). Positive = over budget.
family: asset_management
grain: property
time_basis: period_cumulative
time_basis_window: calendar_month
scenario: [actual]
unit: dollars
numerator: expense_actual - expense_budget
denominator: null
rollup_rule: sum
null_handling: Surface missing.
source_fields: [BudgetLine, actual GL expense]
qa_rule: Drill down on variance > 5% or $10k.
reconciliation_rule: Reconciles to GL.
aliases: [opex_var]
overlays_may_override: [target_band]
open_questions: []
```

### noi

```yaml
name: Net Operating Income
slug: noi
description: Operating revenue - operating expense. Excludes debt service, capex, non-operating items.
family: asset_management
grain: property
time_basis: rolling_window
time_basis_window: T12_months
scenario: [actual, budget, forecast, underwriting]
unit: dollars
numerator: total_revenue - operating_expense
denominator: null
filters_default: [exclude capex, debt_service, depreciation, non_operating]
rollup_rule: sum
null_handling: Surface missing.
source_fields: [BudgetLine, ForecastLine]
qa_rule: NOI margin < 40% for middle-market stabilized flags review.
reconciliation_rule: Reconciles to GL and bank reconciliation.
aliases: [net_operating_income]
overlays_may_override: []
open_questions: []
```

### noi_margin

```yaml
name: NOI Margin
slug: noi_margin
description: NOI / Total revenue.
family: asset_management
grain: property
time_basis: rolling_window
time_basis_window: T12_months
scenario: [actual, budget, forecast, underwriting]
unit: percent
numerator: noi
denominator: total_revenue
rollup_rule: weighted_by_total_revenue
null_handling: Surface missing.
source_fields: [noi, total_revenue]
qa_rule: See noi qa_rule.
reconciliation_rule: See noi.
aliases: []
overlays_may_override: [target_band]
open_questions: []
```

### dscr

```yaml
name: Debt Service Coverage Ratio
slug: dscr
description: NOI / debt service (interest + amortization) for the measurement window.
family: asset_management
grain: property
time_basis: rolling_window
time_basis_window: T12_months
scenario: [actual, forecast, underwriting]
unit: ratio
numerator: noi
denominator: debt_service
rollup_rule: weighted_by_debt_service
null_handling: Surface missing if debt_service unknown.
source_fields: [noi, debt_service]
qa_rule: < 1.20x for middle-market triggers covenant review.
reconciliation_rule: Reconciles to lender compliance certificate.
aliases: [debt_service_coverage]
overlays_may_override: [target_band]
open_questions:
  - "Amortization treatment: include principal; confirm per loan doc overlay."
```

### debt_yield

```yaml
name: Debt Yield
slug: debt_yield
description: NOI / debt balance.
family: asset_management
grain: property
time_basis: rolling_window
time_basis_window: T12_months
scenario: [actual, forecast]
unit: percent
numerator: noi
denominator: debt_balance_current
rollup_rule: weighted_by_debt_balance
null_handling: Surface missing.
source_fields: [noi, debt_balance]
qa_rule: < 8% for middle-market triggers covenant/refi review.
reconciliation_rule: Reconciles to lender statement.
aliases: [dy]
overlays_may_override: [target_band]
open_questions: []
```

### capex_spend_vs_plan

```yaml
name: Capex Spend vs. Plan
slug: capex_spend_vs_plan
description: Capex spend / approved capex plan, period cumulative.
family: asset_management
grain: property
time_basis: period_cumulative
time_basis_window: YTD
scenario: [actual]
unit: percent
numerator: capex_spent_ytd
denominator: capex_plan_ytd
rollup_rule: weighted_by_capex_plan
null_handling: Surface missing.
source_fields: [CapexProject.total_budget, actual capex GL]
qa_rule: "> 105% without change order trail flags review."
reconciliation_rule: Reconciles to GL capex.
aliases: [capex_attainment]
overlays_may_override: [target_band]
open_questions: []
```

### renovation_yield_on_cost

```yaml
name: Renovation Yield on Cost
slug: renovation_yield_on_cost
description: Annualized incremental NOI / renovation spend.
family: asset_management
grain: property
time_basis: as_of_date
scenario: [actual, underwriting]
unit: percent
numerator: incremental_noi_annualized
denominator: renovation_total_spend
rollup_rule: weighted_by_renovation_spend
null_handling: Surface missing if stabilized NOI uplift not yet available.
source_fields: [CapexProject, NOI pre- and post-]
qa_rule: < underwriting target - 200bp triggers program review.
reconciliation_rule: Reconciles to program tracker.
aliases: [reno_yoc]
overlays_may_override: [target_band]
open_questions: []
```

### stabilization_pace_vs_plan

```yaml
name: Stabilization Pace vs. Plan
slug: stabilization_pace_vs_plan
description: Actual leased occupancy pace vs. budgeted lease-up curve during lease_up stage.
family: asset_management
grain: property
time_basis: as_of_date
scenario: [actual]
unit: percent
numerator: leased_occupancy_actual_week - leased_occupancy_budget_week
denominator: null
filters_default: [lifecycle=lease_up]
rollup_rule: not_rollupable (must be recomputed at target grain)
null_handling: Surface missing.
source_fields: [leased_occupancy, lease_up_plan_ref]
qa_rule: "> 200bps behind plan for 4 weeks triggers pricing/marketing review."
reconciliation_rule: Reconciles to weekly leasing report.
aliases: [lease_up_pace]
overlays_may_override: [target_band]
open_questions: []
```

### renewal_rent_delta_dollars

```yaml
name: Renewal Rent Delta (Dollars)
slug: renewal_rent_delta_dollars
description: Dollar change per month between renewal rent and prior in-place rent.
family: asset_management
grain: lease
time_basis: event_stamped
scenario: [actual, underwriting]
unit: dollars
numerator: renewal_rent - prior_rent
denominator: null
rollup_rule: sum (for period) or average (for headline)
null_handling: Surface missing.
source_fields: [Lease.base_rent_monthly, prior_lease_id]
qa_rule: See rent_growth_renewal.
reconciliation_rule: See rent_growth_renewal.
aliases: [renewal_delta]
overlays_may_override: []
open_questions: []
```

### forecast_accuracy

```yaml
name: Forecast Accuracy
slug: forecast_accuracy
description: |
  1 - average absolute percent error of forecast vs. actual over the comparison window.
family: asset_management
grain: property
time_basis: rolling_window
time_basis_window: T6_months
scenario: [actual]
unit: percent
numerator: 1 - mean(|forecast - actual| / actual)
denominator: null
rollup_rule: average across properties
null_handling: Exclude periods where actual = 0.
source_fields: [ForecastLine, actual GL]
qa_rule: < 92% flags forecasting discipline review.
reconciliation_rule: Reconciles to forecast history.
aliases: [forecast_hit_rate]
overlays_may_override: [target_band]
open_questions: []
```

---

## Portfolio Management family

### same_store_noi_growth

```yaml
name: Same-Store NOI Growth
slug: same_store_noi_growth
description: |
  YoY NOI growth for properties owned through both comparison periods (same_store set).
family: portfolio_management
grain: portfolio
time_basis: rolling_window
time_basis_window: T12_months_vs_prior_T12
scenario: [actual, benchmark]
unit: percent
numerator: noi_current_t12 - noi_prior_t12 (same_store)
denominator: noi_prior_t12 (same_store)
rollup_rule: sum then divide
null_handling: Surface missing.
source_fields: [noi, same_store_set]
qa_rule: Negative trend flags portfolio review.
reconciliation_rule: Reconciles to property-level NOI.
aliases: [ss_noi_growth]
overlays_may_override: [target_band]
open_questions:
  - "Same-store definition: owned through both periods; excludes lease_up and recap_support."
```

### occupancy_by_market

```yaml
name: Occupancy by Market
slug: occupancy_by_market
description: Weighted physical occupancy across properties within a market.
family: portfolio_management
grain: market
time_basis: as_of_date
scenario: [actual, budget, forecast]
unit: percent
numerator: sum(physical_occupancy * unit_count_rentable) across market
denominator: sum(unit_count_rentable) across market
rollup_rule: weighted_by_unit_count_rentable
null_handling: Surface missing if any property missing.
source_fields: [Property.market, physical_occupancy, unit_count_rentable]
qa_rule: Deviation from market benchmark > 200bps flags review.
reconciliation_rule: Reconciles to portfolio rollup.
aliases: [market_occupancy]
overlays_may_override: [target_band]
open_questions: []
```

### delinquency_by_market

```yaml
name: Delinquency by Market
slug: delinquency_by_market
description: Weighted delinquency_rate_30plus across properties within a market.
family: portfolio_management
grain: market
time_basis: as_of_date
scenario: [actual, benchmark]
unit: percent
numerator: sum(delinquent_units) across market
denominator: sum(occupied_units) across market
rollup_rule: weighted_by_occupied_units
null_handling: Surface missing.
source_fields: [delinquency_rate_30plus, occupied_units]
qa_rule: Outliers flagged for collections review.
reconciliation_rule: Reconciles to property rollup.
aliases: [market_delinq]
overlays_may_override: [target_band]
open_questions: []
```

### turn_cost_by_market

```yaml
name: Turn Cost by Market
slug: turn_cost_by_market
description: Average turn cost per unit across properties within a market.
family: portfolio_management
grain: market
time_basis: rolling_window
time_basis_window: T12_months
scenario: [actual, benchmark]
unit: dollars
numerator: sum(turn_cost) across market
denominator: count of completed turns across market
rollup_rule: weighted_by_turn_count
null_handling: Surface missing.
source_fields: [TurnProject.actual_total]
qa_rule: Variance to reference turn_cost_library > 20% flags review.
reconciliation_rule: Reconciles to turn log.
aliases: []
overlays_may_override: [target_band]
open_questions: []
```

### portfolio_concentration_market

```yaml
name: Portfolio Concentration by Market
slug: portfolio_concentration_market
description: Share of unit_count (or GAV) by market.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual]
unit: percent
numerator: unit_count_by_market
denominator: unit_count_portfolio
rollup_rule: sum
null_handling: Surface missing.
source_fields: [Property.market, unit_count_rentable]
qa_rule: Concentration > policy threshold flags diversification review.
reconciliation_rule: Reconciles to property master.
aliases: [market_concentration]
overlays_may_override: [target_band]
open_questions:
  - Alternate denominator by GAV is supported; surface which is in use.
```

### asset_watchlist_score

```yaml
name: Asset Watchlist Score
slug: asset_watchlist_score
description: |
  Composite risk score combining DSCR cushion, occupancy variance, delinquency, turn speed,
  and forecast accuracy. Higher = more risk. Thresholds live in overlays.
family: portfolio_management
grain: property
time_basis: as_of_date
scenario: [actual]
unit: score
numerator: null
denominator: null
filters_default: []
rollup_rule: not_rollupable
null_handling: Missing inputs reduce score confidence; surface.
source_fields: [dscr, leased_occupancy variance, delinquency_rate_30plus, make_ready_days, forecast_accuracy]
qa_rule: Composite formula frozen in reference/normalized/watchlist_scoring.yaml.
reconciliation_rule: Reconciles to watchlist tracker.
aliases: [watchlist_score]
overlays_may_override: [target_band]
open_questions: []
```

### budget_attainment

```yaml
name: Budget Attainment
slug: budget_attainment
description: NOI actual / NOI budget, year-to-date.
family: portfolio_management
grain: property
time_basis: period_cumulative
time_basis_window: YTD
scenario: [actual]
unit: percent
numerator: noi_actual_ytd
denominator: noi_budget_ytd
rollup_rule: weighted_by_budget_noi
null_handling: Surface missing.
source_fields: [noi budget and actual]
qa_rule: < 95% flags asset review.
reconciliation_rule: Reconciles to GL.
aliases: [budget_hit_rate]
overlays_may_override: [target_band]
open_questions: []
```

---

## Development & Construction family

### dev_cost_per_unit

```yaml
name: Development Cost per Unit
slug: dev_cost_per_unit
description: Total development cost / unit count. Used for both current estimate and baseline.
family: development_construction
grain: project
time_basis: as_of_date
scenario: [actual, estimate, bid, underwriting]
unit: dollars_per_unit
numerator: total_dev_cost
denominator: unit_count_total
rollup_rule: sum
null_handling: Surface missing.
source_fields: [CapexProject/DevelopmentProject.total_budget, unit_count_total]
qa_rule: Variance to regional benchmark > 15% flags review.
reconciliation_rule: Reconciles to GC contract + soft costs.
aliases: [tdc_per_unit]
overlays_may_override: [target_band]
open_questions: []
```

### dev_cost_per_gsf

```yaml
name: Development Cost per Gross SF
slug: dev_cost_per_gsf
description: Total development cost / gross square feet.
family: development_construction
grain: project
time_basis: as_of_date
scenario: [actual, estimate, bid, underwriting]
unit: dollars_per_sf
numerator: total_dev_cost
denominator: gross_sf
rollup_rule: weighted_by_gross_sf
null_handling: Surface missing.
source_fields: [total_budget, gross_sf]
qa_rule: See dev_cost_per_unit.
reconciliation_rule: See dev_cost_per_unit.
aliases: [tdc_per_gsf]
overlays_may_override: [target_band]
open_questions: []
```

### dev_cost_per_nrsf

```yaml
name: Development Cost per NRSF
slug: dev_cost_per_nrsf
description: Total development cost / net rentable square feet.
family: development_construction
grain: project
time_basis: as_of_date
scenario: [actual, estimate, bid, underwriting]
unit: dollars_per_sf
numerator: total_dev_cost
denominator: nrsf_total
rollup_rule: weighted_by_nrsf
null_handling: Surface missing.
source_fields: [total_budget, nrsf_total]
qa_rule: See dev_cost_per_unit.
reconciliation_rule: See dev_cost_per_unit.
aliases: [tdc_per_nrsf]
overlays_may_override: [target_band]
open_questions: []
```

### contingency_remaining

```yaml
name: Contingency Remaining
slug: contingency_remaining
description: Unused contingency dollars remaining at as-of date.
family: development_construction
grain: project
time_basis: as_of_date
scenario: [actual]
unit: dollars
numerator: contingency_original - contingency_used
denominator: null
rollup_rule: sum
null_handling: Surface missing.
source_fields: [CapexProject.contingency_pct, change_orders]
qa_rule: < 20% of original contingency at percent_complete < 50% flags review.
reconciliation_rule: Reconciles to cost report.
aliases: [contingency_left]
overlays_may_override: []
open_questions: []
```

### contingency_burn_rate

```yaml
name: Contingency Burn Rate
slug: contingency_burn_rate
description: (Contingency used / Contingency original) / percent_complete_cost. > 1 is overburn.
family: development_construction
grain: project
time_basis: as_of_date
scenario: [actual]
unit: ratio
numerator: contingency_used / contingency_original
denominator: percent_complete_cost
rollup_rule: not_rollupable
null_handling: Surface missing.
source_fields: [contingency_used, contingency_original, percent_complete_cost]
qa_rule: "> 1.25 flags cost overrun review."
reconciliation_rule: Reconciles to cost report.
aliases: []
overlays_may_override: [target_band]
open_questions: []
```

### change_orders_pct_of_contract

```yaml
name: Change Orders % of Contract
slug: change_orders_pct_of_contract
description: Approved change orders / original GC contract amount.
family: development_construction
grain: project
time_basis: as_of_date
scenario: [actual]
unit: percent
numerator: sum(ChangeOrder.cost_delta where status=approved)
denominator: original_contract_amount
rollup_rule: not_rollupable
null_handling: Surface missing.
source_fields: [ChangeOrder, CapexProject.original_contract_amount]
qa_rule: "> 5% at percent_complete_cost < 80% flags review."
reconciliation_rule: Reconciles to GC cost report.
aliases: [co_pct]
overlays_may_override: [target_band]
open_questions: []
```

### cost_to_complete

```yaml
name: Cost to Complete
slug: cost_to_complete
description: Estimated dollars required to finish the project as of as-of date.
family: development_construction
grain: project
time_basis: as_of_date
scenario: [estimate]
unit: dollars
numerator: null
denominator: null
rollup_rule: sum
null_handling: Surface missing.
source_fields: [DrawRequest.cost_to_complete_estimate, schedule, change_orders]
qa_rule: Recompute at each draw; compare vs. prior.
reconciliation_rule: Reconciles to schedule and cost report.
aliases: [etc, ctc]
overlays_may_override: []
open_questions: []
```

### schedule_variance_days

```yaml
name: Schedule Variance (Days)
slug: schedule_variance_days
description: Current forecast completion date - baseline completion date.
family: development_construction
grain: project
time_basis: as_of_date
scenario: [actual, forecast]
unit: days
numerator: current_forecast_completion - baseline_completion
denominator: null
rollup_rule: not_rollupable
null_handling: Surface missing.
source_fields: [ScheduleMilestone.baseline_date, ScheduleMilestone.current_forecast_date]
qa_rule: "> 30 days flags review."
reconciliation_rule: Reconciles to schedule tracker.
aliases: [schedule_slip]
overlays_may_override: [target_band]
open_questions: []
```

### milestone_slippage_rate

```yaml
name: Milestone Slippage Rate
slug: milestone_slippage_rate
description: Share of milestones that slipped (forecast > baseline) as of date.
family: development_construction
grain: project
time_basis: as_of_date
scenario: [actual]
unit: percent
numerator: count of milestones with current_forecast_date > baseline_date
denominator: count of milestones
rollup_rule: not_rollupable
null_handling: Surface missing.
source_fields: [ScheduleMilestone]
qa_rule: "> 30% flags schedule review."
reconciliation_rule: Reconciles to schedule tracker.
aliases: []
overlays_may_override: [target_band]
open_questions: []
```

### trade_buyout_variance

```yaml
name: Trade Buyout Variance
slug: trade_buyout_variance
description: (Awarded bid - buyout budget) / buyout budget, per trade.
family: development_construction
grain: bid
time_basis: event_stamped
scenario: [actual]
unit: percent
numerator: awarded_bid - buyout_budget
denominator: buyout_budget
rollup_rule: weighted_by_buyout_budget
null_handling: Surface missing.
source_fields: [BidComparison.recommended_award, EstimateLineItem.extended_cost]
qa_rule: "> 10% per trade flags review."
reconciliation_rule: Reconciles to procurement log.
aliases: [buyout_delta]
overlays_may_override: [target_band]
open_questions: []
```

### draw_cycle_time

```yaml
name: Draw Cycle Time
slug: draw_cycle_time
description: Days from draw submission to lender funding.
family: development_construction
grain: project
time_basis: rolling_window
time_basis_window: T90_days
scenario: [actual]
unit: days
numerator: sum(funded_date - submitted_date)
denominator: count of draws
rollup_rule: weighted_by_draw_count
null_handling: Exclude draws still pending.
source_fields: [DrawRequest]
qa_rule: "> 21 days flags process review."
reconciliation_rule: Reconciles to lender statements.
aliases: []
overlays_may_override: [target_band]
open_questions: []
```

### punchlist_closeout_rate

```yaml
name: Punchlist Closeout Rate
slug: punchlist_closeout_rate
description: Share of punchlist items resolved within agreed SLA post-TCO.
family: development_construction
grain: project
time_basis: as_of_date
scenario: [actual]
unit: percent
numerator: count of punchlist items closed within SLA
denominator: count of punchlist items
rollup_rule: not_rollupable
null_handling: Surface missing.
source_fields: [punchlist_log]
qa_rule: < 90% at 60 days post-TCO flags review.
reconciliation_rule: Reconciles to punchlist log.
aliases: []
overlays_may_override: [target_band]
open_questions: []
```

### lease_up_pace_post_delivery

```yaml
name: Lease-Up Pace Post-Delivery
slug: lease_up_pace_post_delivery
description: Units leased per week after TCO, until stabilization.
family: development_construction
grain: project
time_basis: rolling_window
time_basis_window: T4_weeks
scenario: [actual, underwriting]
unit: count
numerator: units_leased_in_window
denominator: null
rollup_rule: sum
null_handling: Surface missing.
source_fields: [Lease.executed in lease_up stage]
qa_rule: See stabilization_pace_vs_plan.
reconciliation_rule: See stabilization_pace_vs_plan.
aliases: []
overlays_may_override: [target_band]
open_questions: []
```

---

## TPM Oversight family

### report_timeliness

```yaml
name: Report Timeliness
slug: report_timeliness
description: Share of reports delivered on or before the contractual due date.
family: tpm_oversight
grain: property
time_basis: rolling_window
time_basis_window: T6_months
scenario: [actual]
unit: percent
numerator: count of reports delivered on or before due_date
denominator: count of reports due
rollup_rule: weighted_by_report_count
null_handling: Surface missing.
source_fields: [report_delivery_log]
qa_rule: < 95% flags TPM review.
reconciliation_rule: Reconciles to reporting calendar.
aliases: []
overlays_may_override: [target_band]
open_questions: []
```

### kpi_completeness

```yaml
name: KPI Completeness
slug: kpi_completeness
description: Share of required KPIs with non-null values in owner report.
family: tpm_oversight
grain: property
time_basis: period_cumulative
time_basis_window: calendar_month
scenario: [actual]
unit: percent
numerator: count of KPIs populated
denominator: count of KPIs required by PMA
rollup_rule: weighted_by_kpi_count
null_handling: Missing = 0.
source_fields: [owner_report, PMA]
qa_rule: < 100% flags review.
reconciliation_rule: Reconciles to PMA required-KPI list.
aliases: []
overlays_may_override: []
open_questions: []
```

### variance_explanation_completeness

```yaml
name: Variance Explanation Completeness
slug: variance_explanation_completeness
description: Share of material variances with a completed VarianceExplanation.
family: tpm_oversight
grain: property
time_basis: period_cumulative
time_basis_window: calendar_month
scenario: [actual]
unit: percent
numerator: count of material variances with VarianceExplanation
denominator: count of material variances
filters_default: [material = |variance| > 5% or $10k]
rollup_rule: weighted_by_variance_count
null_handling: Missing = 0.
source_fields: [VarianceExplanation, BudgetLine, actual GL]
qa_rule: < 95% flags review.
reconciliation_rule: Reconciles to variance schedule.
aliases: []
overlays_may_override: [filters_default]
open_questions: []
```

### budget_adherence

```yaml
name: Budget Adherence (TPM)
slug: budget_adherence_tpm
description: Share of controllable line items within budget tolerance.
family: tpm_oversight
grain: property
time_basis: period_cumulative
time_basis_window: YTD
scenario: [actual]
unit: percent
numerator: count of controllable lines within tolerance
denominator: count of controllable lines
filters_default: [tolerance = +/- 5%]
rollup_rule: weighted_by_line_count
null_handling: Missing = 0.
source_fields: [BudgetLine, actual GL]
qa_rule: < 80% flags TPM review.
reconciliation_rule: Reconciles to GL.
aliases: []
overlays_may_override: [filters_default, target_band]
open_questions: []
```

### staffing_vacancy_rate_tpm

```yaml
name: Staffing Vacancy Rate (TPM)
slug: staffing_vacancy_rate_tpm
description: Share of approved site positions vacant longer than vacancy_threshold_days.
family: tpm_oversight
grain: property
time_basis: as_of_date
scenario: [actual]
unit: percent
numerator: count of positions vacant > vacancy_threshold_days
denominator: count of approved positions
rollup_rule: weighted_by_position_count
null_handling: Surface missing.
source_fields: [StaffingPlan, site_roster]
qa_rule: "> 10% flags TPM review."
reconciliation_rule: Reconciles to HRIS.
aliases: []
overlays_may_override: [filters_default, target_band]
open_questions:
  - vacancy_threshold_days default is 21 days.
```

### tpm_collections_performance

```yaml
name: TPM Collections Performance
slug: tpm_collections_performance
description: Property-level collections_rate vs. market benchmark, used for TPM scorecard.
family: tpm_oversight
grain: property
time_basis: period_cumulative
time_basis_window: calendar_month
scenario: [actual]
unit: percent
numerator: collections_rate (property)
denominator: collections_rate_benchmark (market)
rollup_rule: not_rollupable
null_handling: Surface missing.
source_fields: [collections_rate, reference/normalized/collections_benchmarks.csv]
qa_rule: < 0.95 of benchmark for 2 consecutive months flags TPM review.
reconciliation_rule: Reconciles to GL and benchmark.
aliases: []
overlays_may_override: [target_band]
open_questions: []
```

### tpm_turn_performance

```yaml
name: TPM Turn Performance
slug: tpm_turn_performance
description: Property-level make_ready_days vs. benchmark, used for TPM scorecard.
family: tpm_oversight
grain: property
time_basis: rolling_window
time_basis_window: T90_days
scenario: [actual]
unit: ratio
numerator: make_ready_days (property)
denominator: make_ready_days_benchmark (market)
rollup_rule: not_rollupable
null_handling: Surface missing.
source_fields: [make_ready_days, reference/normalized/turn_benchmarks.csv]
qa_rule: "> 1.15 flags TPM review."
reconciliation_rule: Reconciles to turn log and benchmark.
aliases: []
overlays_may_override: [target_band]
open_questions: []
```

### service_level_adherence

```yaml
name: Service Level Adherence
slug: service_level_adherence
description: Share of service SLAs met over the window (response times, completion times, reporting).
family: tpm_oversight
grain: property
time_basis: rolling_window
time_basis_window: T90_days
scenario: [actual]
unit: percent
numerator: count of SLA events met
denominator: count of SLA events
rollup_rule: weighted_by_event_count
null_handling: Missing = 0.
source_fields: [SLA definitions in PMA, event log]
qa_rule: < 90% flags TPM review.
reconciliation_rule: Reconciles to PMA and event log.
aliases: []
overlays_may_override: [target_band]
open_questions: []
```

### approval_response_time_tpm

```yaml
name: Approval Response Time (TPM)
slug: approval_response_time_tpm
description: Owner-side days from TPM approval request to owner decision.
family: tpm_oversight
grain: org
time_basis: rolling_window
time_basis_window: T90_days
scenario: [actual]
unit: days
numerator: sum(decided_at - created_at)
denominator: count of approval requests
rollup_rule: weighted_by_request_count
null_handling: Exclude pending.
source_fields: [ApprovalRequest]
qa_rule: Median > 3 business days flags owner-side process review.
reconciliation_rule: Reconciles to approval log.
aliases: []
overlays_may_override: [target_band]
open_questions: []
```

### audit_issue_count_and_severity

```yaml
name: Audit Issue Count and Severity
slug: audit_issue_count_and_severity
description: Open audit findings by severity (low/medium/high/critical).
family: tpm_oversight
grain: property
time_basis: as_of_date
scenario: [actual]
unit: distribution
numerator: null
denominator: null
rollup_rule: not_rollupable
null_handling: Zero allowed.
source_fields: [audit_log]
qa_rule: Any critical open > 30 days flags escalation.
reconciliation_rule: Reconciles to audit tracker.
aliases: []
overlays_may_override: []
open_questions: []
```

---

## Extension slots (reserved, not yet defined)

The following metric slugs are reserved for future definitions. Do not reuse these names for other meanings.

- `rent_growth_same_store`, `rent_growth_new_supply`, `absorption_rate`, `lease_exposure_by_month`, `rubs_recovery_rate`, `insurance_claim_frequency`, `capex_deferred_to_life_safety_ratio`, `tenant_satisfaction_index`, `vendor_scorecard_index`.

Each will follow the full metric contract when added.
---

## Pipeline / Pre-Close / IC / Handoff family (wave-5; status: proposed)

Wave-5 introduced these metrics through the pipeline_review, pre_close_deal_tracking, investment_committee_prep, acquisition_handoff, post_ic_property_setup, development_pipeline_tracking, lease_up_first_period, delivery_handoff, and executive_pipeline_summary workflow packs. Each ships at `status: proposed` until the operationalization run promotes it. Source-of-record per metric is documented inline; reconciliation bands cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.

### pipeline_velocity_days

```yaml
name: Pipeline Velocity Days
slug: pipeline_velocity_days
description: |
  Pipeline Velocity Days — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: rolling_window
time_basis_window: T12
scenario: [actual, forecast]
unit: days
rollup_rule: weighted_by_deal_dollars
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### stage_conversion_rate

```yaml
name: Stage Conversion Rate
slug: stage_conversion_rate
description: |
  Stage Conversion Rate — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: rolling_window
time_basis_window: T12
scenario: [actual, forecast]
unit: percent
rollup_rule: weighted_by_deal_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### stalled_deal_count

```yaml
name: Stalled Deal Count
slug: stalled_deal_count
description: |
  Stalled Deal Count — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: count
rollup_rule: sum
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### ic_prep_load_count

```yaml
name: IC Prep Load Count
slug: ic_prep_load_count
description: |
  IC Prep Load Count — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: count
rollup_rule: sum
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### debt_term_sheet_variance

```yaml
name: Debt Term Sheet Variance
slug: debt_term_sheet_variance
description: |
  Debt Term Sheet Variance — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: percent
rollup_rule: weighted_by_deal_dollars
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### retrade_risk_count

```yaml
name: Retrade Risk Count
slug: retrade_risk_count
description: |
  Retrade Risk Count — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: count
rollup_rule: sum
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### closing_certainty_score

```yaml
name: Closing Certainty Score
slug: closing_certainty_score
description: |
  Closing Certainty Score — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: ratio
rollup_rule: weighted_by_deal_dollars
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### pipeline_weighted_capital_need

```yaml
name: Pipeline Weighted Capital Need
slug: pipeline_weighted_capital_need
description: |
  Pipeline Weighted Capital Need — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: dollars
rollup_rule: sum
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### pipeline_stage_committed_dollars

```yaml
name: Pipeline Stage Committed Dollars
slug: pipeline_stage_committed_dollars
description: |
  Pipeline Stage Committed Dollars — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: dollars
rollup_rule: sum
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### expected_close_by_month

```yaml
name: Expected Close By Month
slug: expected_close_by_month
description: |
  Expected Close By Month — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: rolling_window
time_basis_window: T12
scenario: [actual, forecast]
unit: dollars
rollup_rule: sum
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### key_date_breach_count

```yaml
name: Key Date Breach Count
slug: key_date_breach_count
description: |
  Key Date Breach Count — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: count
rollup_rule: sum
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### key_date_days_remaining

```yaml
name: Key Date Days Remaining
slug: key_date_days_remaining
description: |
  Key Date Days Remaining — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: days
rollup_rule: not_rollupable (must be recomputed at target grain)
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### open_contingency_count

```yaml
name: Open Contingency Count
slug: open_contingency_count
description: |
  Open Contingency Count — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: count
rollup_rule: sum
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### lender_deliverable_status_score

```yaml
name: Lender Deliverable Status Score
slug: lender_deliverable_status_score
description: |
  Lender Deliverable Status Score — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: ratio
rollup_rule: weighted_by_deal_dollars
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### escrow_funding_status

```yaml
name: Escrow Funding Status
slug: escrow_funding_status
description: |
  Escrow Funding Status — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: ratio
rollup_rule: weighted_by_deal_dollars
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### pre_close_cycle_time

```yaml
name: Pre-Close Cycle Time
slug: pre_close_cycle_time
description: |
  Pre-Close Cycle Time — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: rolling_window
time_basis_window: T12
scenario: [actual, forecast]
unit: days
rollup_rule: weighted_by_deal_dollars
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### days_to_close

```yaml
name: Days To Close
slug: days_to_close
description: |
  Days To Close — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: days
rollup_rule: not_rollupable (must be recomputed at target grain)
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### ic_approval_rate

```yaml
name: IC Approval Rate
slug: ic_approval_rate
description: |
  IC Approval Rate — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: rolling_window
time_basis_window: T12
scenario: [actual, forecast]
unit: percent
rollup_rule: weighted_by_deal_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### ic_deferral_rate

```yaml
name: IC Deferral Rate
slug: ic_deferral_rate
description: |
  IC Deferral Rate — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: rolling_window
time_basis_window: T12
scenario: [actual, forecast]
unit: percent
rollup_rule: weighted_by_deal_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### ic_decline_rate

```yaml
name: IC Decline Rate
slug: ic_decline_rate
description: |
  IC Decline Rate — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: rolling_window
time_basis_window: T12
scenario: [actual, forecast]
unit: percent
rollup_rule: weighted_by_deal_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### ic_condition_completion_rate

```yaml
name: IC Condition Completion Rate
slug: ic_condition_completion_rate
description: |
  IC Condition Completion Rate — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: percent
rollup_rule: weighted_by_deal_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### ic_condition_aging_days

```yaml
name: IC Condition Aging Days
slug: ic_condition_aging_days
description: |
  IC Condition Aging Days — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: days
rollup_rule: weighted_by_deal_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### ic_docket_load_count

```yaml
name: IC Docket Load Count
slug: ic_docket_load_count
description: |
  IC Docket Load Count — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: count
rollup_rule: sum
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### ic_docket_forward_90d

```yaml
name: IC Docket Forward 90 Days
slug: ic_docket_forward_90d
description: |
  IC Docket Forward 90 Days — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: rolling_window
time_basis_window: T12
scenario: [actual, forecast]
unit: count
rollup_rule: sum
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### sensitivity_test_pass_rate

```yaml
name: Sensitivity Test Pass Rate
slug: sensitivity_test_pass_rate
description: |
  Sensitivity Test Pass Rate — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: percent
rollup_rule: weighted_by_deal_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### comp_evidence_freshness_days

```yaml
name: Comp Evidence Freshness Days
slug: comp_evidence_freshness_days
description: |
  Comp Evidence Freshness Days — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: days
rollup_rule: weighted_by_deal_dollars
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### lp_capital_coverage_ratio

```yaml
name: LP Capital Coverage Ratio
slug: lp_capital_coverage_ratio
description: |
  LP Capital Coverage Ratio — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: ratio
rollup_rule: sum
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### ic_cycle_time_days

```yaml
name: IC Cycle Time Days
slug: ic_cycle_time_days
description: |
  IC Cycle Time Days — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: rolling_window
time_basis_window: T12
scenario: [actual, forecast]
unit: days
rollup_rule: weighted_by_deal_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### handoff_completeness_score

```yaml
name: Handoff Completeness Score
slug: handoff_completeness_score
description: |
  Handoff Completeness Score — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: asset_management
grain: property
time_basis: as_of_date
scenario: [actual, forecast]
unit: ratio
rollup_rule: weighted_by_unit_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### handoff_lag_days

```yaml
name: Handoff Lag Days
slug: handoff_lag_days
description: |
  Handoff Lag Days — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: asset_management
grain: property
time_basis: as_of_date
scenario: [actual, forecast]
unit: days
rollup_rule: weighted_by_unit_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### vendor_rationalization_count

```yaml
name: Vendor Rationalization Count
slug: vendor_rationalization_count
description: |
  Vendor Rationalization Count — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: asset_management
grain: property
time_basis: as_of_date
scenario: [actual, forecast]
unit: count
rollup_rule: sum
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### opening_rent_roll_reconciliation_variance

```yaml
name: Opening Rent Roll Reconciliation Variance
slug: opening_rent_roll_reconciliation_variance
description: |
  Opening Rent Roll Reconciliation Variance — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: asset_management
grain: property
time_basis: as_of_date
scenario: [actual, forecast]
unit: percent
rollup_rule: weighted_by_unit_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### pma_execution_lag_days

```yaml
name: PMA Execution Lag Days
slug: pma_execution_lag_days
description: |
  PMA Execution Lag Days — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: asset_management
grain: property
time_basis: as_of_date
scenario: [actual, forecast]
unit: days
rollup_rule: weighted_by_unit_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### crosswalk_row_creation_lag_days

```yaml
name: Crosswalk Row Creation Lag Days
slug: crosswalk_row_creation_lag_days
description: |
  Crosswalk Row Creation Lag Days — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: asset_management
grain: property
time_basis: as_of_date
scenario: [actual, forecast]
unit: days
rollup_rule: weighted_by_unit_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### pre_close_setup_completeness_score

```yaml
name: Pre-Close Setup Completeness Score
slug: pre_close_setup_completeness_score
description: |
  Pre-Close Setup Completeness Score — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: asset_management
grain: property
time_basis: as_of_date
scenario: [actual, forecast]
unit: ratio
rollup_rule: weighted_by_unit_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### placeholder_crosswalk_creation_lag_days

```yaml
name: Placeholder Crosswalk Creation Lag Days
slug: placeholder_crosswalk_creation_lag_days
description: |
  Placeholder Crosswalk Creation Lag Days — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: asset_management
grain: property
time_basis: as_of_date
scenario: [actual, forecast]
unit: days
rollup_rule: weighted_by_unit_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### pre_close_insurance_binder_lead_days

```yaml
name: Pre-Close Insurance Binder Lead Days
slug: pre_close_insurance_binder_lead_days
description: |
  Pre-Close Insurance Binder Lead Days — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: asset_management
grain: property
time_basis: as_of_date
scenario: [actual, forecast]
unit: days
rollup_rule: weighted_by_unit_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### legal_entity_formation_lag_days

```yaml
name: Legal Entity Formation Lag Days
slug: legal_entity_formation_lag_days
description: |
  Legal Entity Formation Lag Days — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: asset_management
grain: property
time_basis: as_of_date
scenario: [actual, forecast]
unit: days
rollup_rule: weighted_by_unit_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### tax_lot_research_completion_rate

```yaml
name: Tax Lot Research Completion Rate
slug: tax_lot_research_completion_rate
description: |
  Tax Lot Research Completion Rate — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: asset_management
grain: property
time_basis: as_of_date
scenario: [actual, forecast]
unit: percent
rollup_rule: weighted_by_unit_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### handoff_baton_readiness_score

```yaml
name: Handoff Baton Readiness Score
slug: handoff_baton_readiness_score
description: |
  Handoff Baton Readiness Score — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: asset_management
grain: property
time_basis: as_of_date
scenario: [actual, forecast]
unit: ratio
rollup_rule: weighted_by_unit_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### handoff_lag_dealpath_to_procore

```yaml
name: Handoff Lag Dealpath To Procore
slug: handoff_lag_dealpath_to_procore
description: |
  Handoff Lag Dealpath To Procore — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: asset_management
grain: project
time_basis: as_of_date
scenario: [actual, forecast]
unit: days
rollup_rule: weighted_by_project_dollars
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### tco_to_first_unit_ready_days

```yaml
name: TCO To First Unit Ready Days
slug: tco_to_first_unit_ready_days
description: |
  TCO To First Unit Ready Days — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: development_construction
grain: project
time_basis: as_of_date
scenario: [actual, forecast]
unit: days
rollup_rule: not_rollupable (must be recomputed at target grain)
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### delivery_handoff_completeness_score

```yaml
name: Delivery Handoff Completeness Score
slug: delivery_handoff_completeness_score
description: |
  Delivery Handoff Completeness Score — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: development_construction
grain: project
time_basis: as_of_date
scenario: [actual, forecast]
unit: ratio
rollup_rule: weighted_by_unit_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### retainage_release_lag_days

```yaml
name: Retainage Release Lag Days
slug: retainage_release_lag_days
description: |
  Retainage Release Lag Days — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: development_construction
grain: project
time_basis: as_of_date
scenario: [actual, forecast]
unit: days
rollup_rule: weighted_by_project_dollars
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### warranty_package_completeness

```yaml
name: Warranty Package Completeness
slug: warranty_package_completeness
description: |
  Warranty Package Completeness — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: development_construction
grain: project
time_basis: as_of_date
scenario: [actual, forecast]
unit: percent
rollup_rule: weighted_by_project_dollars
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### as_built_doc_completeness

```yaml
name: As-Built Doc Completeness
slug: as_built_doc_completeness
description: |
  As-Built Doc Completeness — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: development_construction
grain: project
time_basis: as_of_date
scenario: [actual, forecast]
unit: percent
rollup_rule: weighted_by_project_dollars
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### capex_closeout_lag_days

```yaml
name: Capex Closeout Lag Days
slug: capex_closeout_lag_days
description: |
  Capex Closeout Lag Days — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: development_construction
grain: project
time_basis: as_of_date
scenario: [actual, forecast]
unit: days
rollup_rule: weighted_by_project_dollars
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### dev_project_crosswalk_closure_lag_days

```yaml
name: Dev Project Crosswalk Closure Lag Days
slug: dev_project_crosswalk_closure_lag_days
description: |
  Dev Project Crosswalk Closure Lag Days — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: asset_management
grain: project
time_basis: as_of_date
scenario: [actual, forecast]
unit: days
rollup_rule: weighted_by_project_dollars
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### cco_to_first_lease_days

```yaml
name: CCO To First Lease Days
slug: cco_to_first_lease_days
description: |
  CCO To First Lease Days — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: asset_management
grain: property
time_basis: as_of_date
scenario: [actual, forecast]
unit: days
rollup_rule: not_rollupable (must be recomputed at target grain)
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### critical_path_slip_days

```yaml
name: Critical Path Slip Days
slug: critical_path_slip_days
description: |
  Critical Path Slip Days — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: development_construction
grain: project
time_basis: as_of_date
scenario: [actual, forecast]
unit: days
rollup_rule: not_rollupable (must be recomputed at target grain)
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### draw_burn_rate_vs_plan

```yaml
name: Draw Burn Rate vs Plan
slug: draw_burn_rate_vs_plan
description: |
  Draw Burn Rate vs Plan — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: development_construction
grain: project
time_basis: rolling_window
time_basis_window: T12
scenario: [actual, forecast]
unit: ratio
rollup_rule: weighted_by_project_dollars
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### commitment_exposure_forward_dollars

```yaml
name: Commitment Exposure Forward Dollars
slug: commitment_exposure_forward_dollars
description: |
  Commitment Exposure Forward Dollars — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: development_construction
grain: project
time_basis: as_of_date
scenario: [actual, forecast]
unit: dollars
rollup_rule: sum
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### capex_commitment_forward_exposure_dollars

```yaml
name: Capex Commitment Forward Exposure Dollars
slug: capex_commitment_forward_exposure_dollars
description: |
  Capex Commitment Forward Exposure Dollars — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: dollars
rollup_rule: sum
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### lease_up_pace_vs_underwriting

```yaml
name: Lease-Up Pace vs Underwriting
slug: lease_up_pace_vs_underwriting
description: |
  Lease-Up Pace vs Underwriting — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: asset_management
grain: property
time_basis: rolling_window
time_basis_window: T12
scenario: [actual, forecast]
unit: percent
rollup_rule: weighted_by_unit_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### concession_depth_vs_market

```yaml
name: Concession Depth vs Market
slug: concession_depth_vs_market
description: |
  Concession Depth vs Market — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: property_operations
grain: property
time_basis: as_of_date
scenario: [actual, forecast]
unit: percent
rollup_rule: weighted_by_unit_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### broker_assist_rate

```yaml
name: Broker Assist Rate
slug: broker_assist_rate
description: |
  Broker Assist Rate — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: property_operations
grain: property
time_basis: rolling_window
time_basis_window: T12
scenario: [actual, forecast]
unit: percent
rollup_rule: weighted_by_lease_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### model_unit_tour_conversion

```yaml
name: Model Unit Tour Conversion
slug: model_unit_tour_conversion
description: |
  Model Unit Tour Conversion — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: property_operations
grain: property
time_basis: rolling_window
time_basis_window: T12
scenario: [actual, forecast]
unit: percent
rollup_rule: weighted_by_tour_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### first_renewal_window_retention_readiness

```yaml
name: First Renewal Window Retention Readiness
slug: first_renewal_window_retention_readiness
description: |
  First Renewal Window Retention Readiness — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: asset_management
grain: property
time_basis: as_of_date
scenario: [actual, forecast]
unit: ratio
rollup_rule: weighted_by_unit_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### noi_ramp_vs_underwriting

```yaml
name: NOI Ramp vs Underwriting
slug: noi_ramp_vs_underwriting
description: |
  NOI Ramp vs Underwriting — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: asset_management
grain: property
time_basis: as_of_date
scenario: [actual, forecast]
unit: percent
rollup_rule: weighted_by_unit_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### lender_reporting_compliance_status

```yaml
name: Lender Reporting Compliance Status
slug: lender_reporting_compliance_status
description: |
  Lender Reporting Compliance Status — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: asset_management
grain: property
time_basis: as_of_date
scenario: [actual, forecast]
unit: ratio
rollup_rule: weighted_by_property_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### equity_call_schedule_coverage

```yaml
name: Equity Call Schedule Coverage
slug: equity_call_schedule_coverage
description: |
  Equity Call Schedule Coverage — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: ratio
rollup_rule: sum
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### capital_deployment_pace_vs_target

```yaml
name: Capital Deployment Pace vs Target
slug: capital_deployment_pace_vs_target
description: |
  Capital Deployment Pace vs Target — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: rolling_window
time_basis_window: T12
scenario: [actual, forecast]
unit: percent
rollup_rule: sum
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### declined_deal_hit_rate

```yaml
name: Declined Deal Hit Rate
slug: declined_deal_hit_rate
description: |
  Declined Deal Hit Rate — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: rolling_window
time_basis_window: T12
scenario: [actual, forecast]
unit: percent
rollup_rule: weighted_by_deal_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### top_of_funnel_sourcing_health

```yaml
name: Top-of-Funnel Sourcing Health
slug: top_of_funnel_sourcing_health
description: |
  Top-of-Funnel Sourcing Health — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: ratio
rollup_rule: weighted_by_deal_count
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### jv_partner_concentration

```yaml
name: JV Partner Concentration
slug: jv_partner_concentration
description: |
  JV Partner Concentration — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: ratio
rollup_rule: sum
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### geographic_concentration_pipeline

```yaml
name: Geographic Concentration (Pipeline)
slug: geographic_concentration_pipeline
description: |
  Geographic Concentration (Pipeline) — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: ratio
rollup_rule: sum
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### segment_concentration_pipeline

```yaml
name: Segment Concentration (Pipeline)
slug: segment_concentration_pipeline
description: |
  Segment Concentration (Pipeline) — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: percent
rollup_rule: sum
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### debt_market_context_band

```yaml
name: Debt Market Context Band
slug: debt_market_context_band
description: |
  Debt Market Context Band — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: ratio
rollup_rule: not_rollupable (must be recomputed at target grain)
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

### confidence_band_per_metric

```yaml
name: Confidence Band Per Metric
slug: confidence_band_per_metric
description: |
  Confidence Band Per Metric — wave-5 proposed metric supporting the deal-pipeline, IC, handoff, development, lease-up, and executive-summary workflows.
  Status: proposed (wave-5). Promote when operationalization run validates the metric's bands and reconciliation against canonical source.
family: portfolio_management
grain: portfolio
time_basis: as_of_date
scenario: [actual, forecast]
unit: ratio
rollup_rule: not_rollupable (must be recomputed at target grain)
null_handling: |
  If required upstream feed (Dealpath / Procore / Intacct / AppFolio) is stale or carries a blocking dq issue, surface metric as `unavailable`. Do not impute.
source_fields: [adapter_normalized_contract, master_data_crosswalks, reference_normalized_reconciliation_tolerance_band]
qa_rule: |
  Confidence reduced to medium when source feed has any open warning-severity dq rule; metric refused when blocker-severity dq rule is open.
reconciliation_rule: |
  Reconciles against the source-of-truth row in `_core/stack_wave4/source_of_truth_matrix.md` for the underlying canonical object. Discrepancies above the named band cite `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
overlays_may_override: [target_band, threshold]
open_questions:
  - Promote from proposed status; lift bands into reference/normalized/ overlays.
```

