# Workflow Chain: Hold Period Management

## Purpose

Governs ongoing asset management from post-close through disposition or refinance. This is not a one-shot chain but a recurring operational loop. The annual-budget-engine sets targets, the property-performance-dashboard monitors actuals, and satellite skills fire when specific conditions arise (capital needs, lease issues, vacancy, NOI shortfall). The chain runs continuously throughout the hold period.

## Chain Diagram

```
annual-budget-engine --> property-performance-dashboard (monthly)
  |
  +--> capex-prioritizer (capital needs)
  +--> lease-compliance-auditor (quarterly/annual)
  +--> tenant-delinquency-workout (tenant issues)
  +--> tenant-retention-engine (approaching expirations)
  |       |
  |       v
  |   rent-optimization-planner --> lease-up-war-room (if vacancy)
  |
  v
noi-sprint-plan (when NOI improvement needed)
```

## Entry Trigger Conditions

- Property closes and transitions from deal-pipeline-acquisition chain (step 13 -> 14)
- New fiscal year begins (annual budget cycle reset)
- Ownership change or management transition on existing asset
- Asset added to portfolio via entity-level acquisition

## Step-by-Step Breakdown

| Step | Skill | Inputs | Outputs | Decision Gate | Daily-Ops Skills Used |
|------|-------|--------|---------|---------------|----------------------|
| 1 | annual-budget-engine | Prior year actuals, proforma assumptions, capital plan, market rent comps, tax/insurance projections | Line-item operating budget, capital budget, staffing plan, revenue projections by unit/suite | Budget approval by asset manager/IC. Reject: revise assumptions | budget-line-item-library, tax-projection-helper, insurance-renewal-tracker |
| 2 | property-performance-dashboard | Monthly actuals (GL export), approved budget, proforma benchmarks | Variance report ($ and %), NOI tracking, occupancy/collections KPIs, trailing 3/6/12 trends | Soft gate: variance > threshold triggers investigation. Persistent underperformance triggers noi-sprint-plan | monthly-reporting-automator, gl-import-mapper |
| 3a | capex-prioritizer | Property condition report, capital reserve balance, tenant improvement pipeline, deferred maintenance log | Prioritized capex schedule, ROI ranking, fund/unfund recommendations, reserve adequacy test | Approve capital spend above threshold. Defer or reject low-ROI items | capex-estimator, vendor-bid-comparator |
| 3b | lease-compliance-auditor | Lease abstracts, tenant financial statements, CAM reconciliation data, insurance certificates | Compliance scorecard, CAM reconciliation output, co-tenancy/kick-out clause status, insurance gap flags | Escalate non-compliance to legal. Waive minor items. Trigger tenant-delinquency-workout if financial default | lease-abstract-extractor, cam-reconciliation-engine |
| 3c | tenant-delinquency-workout | Delinquency report, lease terms, tenant financials, legal options | Workout strategy (payment plan, lease modification, eviction timeline), collection probability, reserve impact | RESOLVE: tenant cures. MODIFY: restructure lease. EVICT: begin legal process. WRITE-OFF: bad debt reserve | collections-tracker, legal-notice-generator |
| 3d | tenant-retention-engine | Lease expiration schedule, tenant satisfaction data, market rents, renewal cost vs. re-tenant cost | Retention priority ranking, renewal offer terms, early renewal incentive packages | RENEW: tenant accepts terms. NEGOTIATE: counter-offer loop. VACATE: tenant declines, trigger lease-up | renewal-offer-generator, tenant-satisfaction-surveyor |
| 4 | rent-optimization-planner | Market rent comps, current in-place rents, lease expiration schedule, demand indicators | Optimal rent schedule by unit/suite, concession strategy, loss-to-lease reduction plan | None -- advisory output feeds into retention offers and new leasing | comp-scraper, concession-analyzer |
| 5 | lease-up-war-room | Vacant unit inventory, market rents, competitor concessions, marketing budget | Leasing campaign plan, broker incentive structure, concession matrix, absorption forecast, weekly velocity targets | Velocity gate: if leasing pace below target for 4+ weeks, escalate (increase concessions, change brokers, or adjust rents) | marketing-spend-tracker, showing-traffic-analyzer |
| 6 | noi-sprint-plan | Current NOI vs. budget/proforma, expense breakdown, revenue shortfall analysis | 90-day action plan with specific NOI improvement initiatives, assigned owners, target impact per initiative | Quarterly review: on-track (continue), behind (escalate), achieved (exit sprint) | expense-reduction-finder, revenue-enhancement-tracker |

## Data Handoff Specifications

### Step 1 -> 2 (Budget to Dashboard)
- **Payload**: `{approved_budget{revenue_lines[], expense_lines[], capital_lines[]}, kpi_targets{occupancy, collections, noi_margin}, reporting_cadence: "monthly"}`
- **Timing**: Annual, with mid-year reforecast option

### Step 2 -> 3a (Dashboard to Capex)
- **Payload**: `{capital_reserve_balance, deferred_maintenance_items[], ti_pipeline[], property_condition_flags[]}`
- **Trigger**: Capital request submitted, or annual capital planning cycle

### Step 2 -> 3b (Dashboard to Lease Compliance)
- **Payload**: `{tenant_roster[], lease_abstracts[], cam_pool_data{}, insurance_certificates[]}`
- **Trigger**: Quarterly compliance review cycle, or annual CAM reconciliation

### Step 2 -> 3c (Dashboard to Delinquency)
- **Payload**: `{delinquent_tenants[{tenant_id, lease_id, amount_owed, days_past_due, payment_history[]}]}`
- **Trigger**: Tenant hits 30+ days past due, or collections rate drops below threshold

### Step 2 -> 3d (Dashboard to Retention)
- **Payload**: `{expiring_leases_12mo[{tenant_id, lease_id, expiration_date, current_rent, market_rent, tenant_quality_score}]}`
- **Trigger**: Lease expiration within 9-12 months (early engagement window)

### Step 3d -> 4 (Retention to Rent Optimization)
- **Payload**: `{renewal_candidates[], market_rent_comps[], loss_to_lease_by_unit[]}`
- **Notes**: Rent optimization informs the renewal offer terms

### Step 4 -> 5 (Rent Optimization to Lease-Up)
- **Payload**: `{vacant_units[], optimal_asking_rents[], concession_budget, competitor_concessions[], absorption_assumptions}`
- **Trigger**: Vacancy exceeds target threshold (e.g., >10% economic vacancy)

### Step 2 -> 6 (Dashboard to NOI Sprint)
- **Payload**: `{current_noi, budget_noi, proforma_noi, variance_drivers[], expense_breakdown{}, revenue_shortfall_detail{}}`
- **Trigger**: NOI trails budget by >5% for 2+ consecutive months, or trails proforma by >10%

## Decision Gates Summary

| Gate | Location | Outcomes |
|------|----------|----------|
| Budget Approval | After step 1 | Approve, revise, or override specific line items |
| Variance Investigation | Step 2 ongoing | Within tolerance (no action), investigate (dig into drivers), escalate (trigger sprint) |
| Capital Approval | Step 3a | Approve spend, defer, or reject |
| Compliance Escalation | Step 3b | Compliant (no action), minor issue (waive/cure), material default (legal/workout) |
| Delinquency Resolution | Step 3c | Cure, modify, evict, or write-off |
| Retention Negotiation | Step 3d | Renew, negotiate, or vacate (triggers lease-up) |
| Leasing Velocity | Step 5 | On-pace (continue), behind (escalate tactics), achieved (exit war room) |
| NOI Sprint Review | Step 6 | On-track, behind (escalate), or target achieved (exit) |

## Recurring Cadence

| Cycle | Frequency | Skills Involved |
|-------|-----------|-----------------|
| Budget setting | Annual (Q4 for following year) | annual-budget-engine |
| Performance review | Monthly | property-performance-dashboard |
| Lease compliance | Quarterly (full audit annual) | lease-compliance-auditor |
| Retention outreach | Rolling (9-12 months pre-expiration) | tenant-retention-engine |
| Capex planning | Annual + ad-hoc | capex-prioritizer |
| NOI sprint | As-needed (triggered by underperformance) | noi-sprint-plan |

## Exit Conditions

- **Ongoing**: This chain runs for the life of the hold. No terminal exit during ownership
- **Transition to Disposition**: When hold period nears target or performance triggers sale analysis, hand off to disposition-pipeline chain
- **Transition to Refi**: When debt maturity approaches or NOI growth creates refi opportunity, hand off to capital-stack-assembly chain (step 4)

## Estimated Time Savings

| Activity | Manual (per month) | Automated Chain | Savings |
|----------|-------------------|-----------------|---------|
| Monthly reporting + variance analysis | 8-12 hrs | 1-2 hrs | 80-85% |
| Annual budgeting | 20-40 hrs (per asset) | 4-8 hrs | 75-80% |
| Lease compliance audit | 6-10 hrs (quarterly) | 1-2 hrs | 80-85% |
| Delinquency workout | 4-8 hrs per case | 1-2 hrs per case | 70-75% |
| Retention/renewal process | 3-5 hrs per tenant | 30-60 min per tenant | 80-85% |
| Lease-up campaign management | 10-15 hrs/week | 3-5 hrs/week | 65-70% |
| NOI sprint planning | 8-12 hrs to build plan | 2-3 hrs | 75% |
| **Annual per asset** | **~400-700 hrs** | **~100-180 hrs** | **~73%** |
