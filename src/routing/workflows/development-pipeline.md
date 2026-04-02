# Workflow Chain: Development Pipeline

## Purpose

Covers the full ground-up or major redevelopment lifecycle from land analysis and entitlement through construction, lease-up, stabilization, and permanent financing or sale. Differs from the acquisition chain in that value is created through construction rather than purchase, introducing unique risks (entitlement, construction cost, lease-up absorption) and a distinct capital structure (construction loan converting to permanent).

## Chain Diagram

```
land-residual-hbu-analyzer + entitlement-feasibility (parallel)
  |
  v
dev-proforma-engine --> construction-budget-gc-analyzer
  |
  v
loan-sizing-engine (construction) --> capital-stack-optimizer --> ic-memo-generator
  |
  v
[CONSTRUCTION] --> [CO] --> lease-up-war-room --> [STABILIZATION]
  |
  v
refi-decision-analyzer (perm takeout) or disposition-strategy-engine (sell)
```

## Entry Trigger Conditions

- Land site identified through sourcing-outreach-system or off-market relationship
- Existing asset earmarked for demolition and redevelopment
- Portfolio strategy calls for development allocation
- JV partner brings entitled or shovel-ready site
- Adaptive reuse opportunity identified (office-to-resi, warehouse-to-industrial, etc.)

## Step-by-Step Breakdown

| Step | Skill | Inputs | Outputs | Decision Gate | Daily-Ops Skills Used |
|------|-------|--------|---------|---------------|----------------------|
| 1a | land-residual-hbu-analyzer | Site location, zoning, buildable area, market rents by use, construction cost estimates | Highest and best use determination, land residual value by use type, supportable land price | Land price within residual range? If asking price > residual, negotiate or KILL | zoning-code-parser, density-calculator |
| 1b | entitlement-feasibility | Zoning code, comp plan, community context, precedent approvals, site constraints | Entitlement risk score, timeline estimate, required variances/special permits, community opposition risk, estimated soft costs for entitlement | Entitlement risk acceptable? HIGH risk with uncertain timeline may KILL deal or require price adjustment | municipal-meeting-tracker, community-sentiment-scorer |
| 2 | dev-proforma-engine | HBU from 1a, entitlement parameters from 1b, construction costs, market rents, absorption schedule, financing assumptions | Full development proforma (total development cost, construction timeline, lease-up schedule, stabilized value, development spread, IRR/multiple) | Development spread meets minimum threshold (typically 150-200+ bps)? If no, adjust program or KILL | hard-cost-estimator, soft-cost-estimator, absorption-schedule-builder |
| 3 | construction-budget-gc-analyzer | Preliminary proforma, design documents, site conditions, GC bids | Detailed construction budget, GC bid comparison, contingency adequacy test, value engineering opportunities, schedule risk assessment | Budget within proforma assumptions? If overrun >5-10%, value engineer or adjust proforma. Fatal overrun: KILL | bid-leveling-tool, contingency-stress-tester, schedule-risk-modeler |
| 4 | loan-sizing-engine (construction) | Total development cost, equity contribution, projected stabilized value, construction timeline, pre-leasing status | Construction loan sizing (LTC basis), interest reserve, draw schedule, completion guaranty requirements, conversion triggers | Lender terms achievable? If LTC too low or guaranty too onerous, seek alternative lenders or increase equity | draw-schedule-builder, interest-reserve-calculator |
| 5 | capital-stack-optimizer | Construction loan terms, equity structure, mezz (if any), total development cost | Optimized development capital stack, blended cost, equity return by scenario, construction-period interest expense | IC gate: full capital stack and returns acceptable? PROCEED to IC memo or RESTRUCTURE | weighted-avg-cost-calculator |
| 6 | ic-memo-generator | Development proforma, capital stack, construction budget, entitlement status, market analysis, risk matrix | IC memo for development approval, construction start authorization, capital call schedule | IC VOTE: approve (break ground), conditional (address items), reject (KILL) | memo-template-engine |
| 7 | [CONSTRUCTION PHASE] | Approved plans, GC contract, construction loan | Monthly draw requests, progress reports, change order log, budget tracking | Ongoing: change orders within contingency? Schedule on track? Material cost overruns trigger re-evaluation | draw-request-processor, change-order-tracker, construction-progress-reporter |
| 8 | lease-up-war-room | Completed/near-complete units, market rents, competitor inventory, marketing plan | Leasing campaign, broker incentives, concession matrix, absorption tracking, weekly velocity | Absorption on pace with proforma? If behind, adjust concessions or rents. If significantly behind, evaluate construction loan extension risk | marketing-spend-tracker, showing-traffic-analyzer, pre-leasing-tracker |
| 9 | refi-decision-analyzer (perm takeout) | Stabilized NOI, property value at stabilization, construction loan balance, perm loan market | Permanent loan sizing, construction loan payoff, excess proceeds, perm loan terms comparison | REFI to perm (standard exit from construction). If value below expectation, may need to extend construction loan or bring additional equity | rate-lock-tracker, construction-to-perm-bridge |
| 9-alt | disposition-strategy-engine (sell at stabilization) | Stabilized financials, development cost basis, market comps, fund strategy | Sale analysis, broker selection, pricing guidance | SELL: if development-for-sale strategy or if market pricing exceeds hold value. HOLD: enter hold-period-management chain | broker-fee-calculator, gain-on-sale-calculator |

## Data Handoff Specifications

### Steps 1a+1b -> 2 (Land Analysis + Entitlement to Proforma)
- **Payload**: `{highest_best_use, supportable_land_price, buildable_program{units_or_sf, floors, parking, amenities}, entitlement_risk_score, entitlement_timeline_months, soft_cost_estimate_entitlement, zoning_constraints[]}`
- **Merge point**: Both 1a and 1b must complete. If entitlement kills the deal, no need for proforma

### Step 2 -> 3 (Proforma to Construction Budget)
- **Payload**: `{preliminary_hard_cost_budget, building_program{}, site_conditions{}, design_stage, target_delivery_date}`
- **Notes**: Proforma uses preliminary construction costs. Step 3 refines with actual GC bids

### Step 3 -> 2 (Feedback loop: Budget back to Proforma)
- **Payload**: `{final_hard_cost_budget, value_engineering_savings, schedule_adjustment, contingency_revised}`
- **Notes**: If GC bids differ materially from proforma assumptions, proforma must be updated before proceeding

### Step 2 (updated) -> 4 (Proforma to Construction Loan Sizing)
- **Payload**: `{total_development_cost, equity_contribution, construction_timeline_months, projected_stabilized_value, pre_leasing_status, borrower_entity, site_address}`

### Step 4 -> 5 (Loan Sizing to Stack Optimizer)
- **Payload**: `{construction_loan{amount, ltc, rate, term, extension_options, guaranty_type, conversion_terms}, equity_required, mezz_terms{} | null, total_sources_uses{}}`

### Step 5 -> 6 (Stack to IC Memo)
- **Payload**: `{development_proforma, capital_stack{}, construction_budget{}, entitlement_status, market_analysis{}, risk_matrix{}, development_timeline}`

### Step 6 -> 7 (IC Approval to Construction)
- **Payload**: `{approved_budget, gc_contract_terms, draw_schedule, milestone_targets[], contingency_amount, reporting_requirements}`
- **Condition**: IC approval received

### Step 7 -> 8 (Construction to Lease-Up)
- **Payload**: `{completed_units[], delivery_schedule, actual_construction_cost_to_date, remaining_budget, certificate_of_occupancy_date}`
- **Trigger**: First units receive CO, or pre-leasing begins during construction

### Step 8 -> 9 (Lease-Up to Perm Takeout)
- **Payload**: `{stabilized_noi, occupancy_rate, actual_rents_achieved, construction_loan_balance, construction_loan_maturity, property_value_estimate}`
- **Trigger**: Property reaches stabilization threshold (typically 90-95% occupied, 3-6 months seasoning)

## Decision Gates Summary

| Gate | Location | Outcomes |
|------|----------|----------|
| Land Price | After step 1a | Within residual (proceed), above residual (negotiate or KILL) |
| Entitlement Risk | After step 1b | Acceptable (proceed), high (price adjustment or KILL) |
| Development Spread | After step 2 | Meets threshold (proceed), below threshold (value engineer or KILL) |
| Construction Budget | After step 3 | Within proforma (proceed), overrun (value engineer, loop to step 2, or KILL) |
| Lender Terms | After step 4 | Achievable (proceed), too restrictive (seek alternatives or increase equity) |
| IC Vote | After step 6 | Approve (break ground), conditional (address items), reject (KILL) |
| Change Orders | During step 7 | Within contingency (continue), exhausted contingency (emergency review) |
| Lease-Up Velocity | During step 8 | On pace (continue), behind (adjust strategy), critically behind (loan extension risk) |
| Stabilization | After step 8 | Stabilized (refi or sell), not stabilized (extend lease-up, address issues) |

## Exit Conditions

- **Perm Takeout**: Construction loan refinanced to permanent debt. Asset enters hold-period-management chain
- **Sell at Stabilization**: Asset sold upon reaching stabilization. Proceeds distributed. Exit portfolio
- **Kill**: Deal terminated pre-construction at any gate. Recover soft costs where possible
- **Distress**: Construction cost overrun or lease-up failure forces recapitalization, sale, or deed-in-lieu

## Estimated Time Savings

| Phase | Manual | Automated Chain | Savings |
|-------|--------|-----------------|---------|
| Land analysis + HBU | 10-20 hrs | 2-4 hrs | 80% |
| Entitlement feasibility | 8-16 hrs | 2-4 hrs | 70-75% |
| Development proforma | 20-40 hrs | 4-8 hrs | 75-80% |
| Construction budget analysis | 10-20 hrs | 3-5 hrs | 70-75% |
| Capital structuring + IC memo | 16-30 hrs | 4-7 hrs | 75% |
| Construction monitoring (monthly) | 8-12 hrs/mo | 2-4 hrs/mo | 70% |
| Lease-up management | 10-15 hrs/wk | 3-5 hrs/wk | 65-70% |
| Perm takeout / disposition | 10-20 hrs | 2-4 hrs | 80% |
| **Total per development** | **~300-550 hrs** | **~75-150 hrs** | **~73%** |
