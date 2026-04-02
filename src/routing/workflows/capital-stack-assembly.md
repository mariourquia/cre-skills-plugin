# Workflow Chain: Capital Stack Assembly

## Purpose

Structures the complete capital stack for an acquisition or development deal. Runs after underwriting confirms the deal meets return thresholds. Sizes senior debt, layers in subordinate capital (mezz/pref), architects the JV equity structure, and optimizes the full stack. Also handles refinancing decisions at maturity or when market conditions create an opportunistic window.

## Chain Diagram

```
acquisition-underwriting-engine (deal economics)
  |
  +--> loan-sizing-engine (senior debt)
  |       |
  |       v
  +--> mezz-pref-structurer (subordinate capital)
  |       |
  |       v
  +--> jv-waterfall-architect (equity structure)
  |
  v
capital-stack-optimizer (synthesize all layers)
  |
  v
refi-decision-analyzer (at maturity or opportunistically)
```

## Entry Trigger Conditions

- Acquisition underwriting engine produces a base case proforma with return metrics
- IC approves deal economics and authorizes capital structuring
- Development proforma reaches feasibility threshold
- Existing asset triggers refinancing analysis (maturity within 12 months, rate environment shift, or NOI growth unlocks better terms)

## Step-by-Step Breakdown

| Step | Skill | Inputs | Outputs | Decision Gate | Daily-Ops Skills Used |
|------|-------|--------|---------|---------------|----------------------|
| 1 | acquisition-underwriting-engine | T12 financials, rent roll, market rents, capex plan | Base case proforma, unlevered IRR, stabilized NOI, value estimate | Must meet minimum unlevered return threshold to proceed | t12-normalizer, capex-estimator |
| 2a | loan-sizing-engine | Stabilized NOI, property value, asset type, borrower profile, rate environment | Max loan amount, LTV/DSCR/DY constraints, term sheet comparison matrix, interest reserve sizing | Constraint check: do lender terms leave enough equity return? If no, adjust structure or seek alternative lenders | rate-lock-tracker, lender-term-comparator |
| 2b | mezz-pref-structurer | Equity gap after senior debt, deal risk profile, target blended cost of capital | Mezz/pref sizing, coupon/rate, attachment/detachment points, intercreditor term flags | Is subordinate capital accretive to sponsor return? If no, skip layer | coupon-calculator, intercreditor-checklist |
| 2c | jv-waterfall-architect | Total equity required, GP/LP split preferences, promote structure, co-invest requirements | Waterfall model (preferred return, catch-up, splits), GP promote economics, clawback provisions | LP terms marketable? If no, adjust promote or seek different LP | waterfall-calculator, promote-sensitivity |
| 3 | capital-stack-optimizer | Senior debt terms, mezz/pref terms (if any), JV equity structure, total deal cost | Optimized stack diagram, blended cost of capital, levered IRR by position, coverage ratios, proceed recommendation | Final gate: does levered return to GP meet fund hurdle after all capital costs? PROCEED or RESTRUCTURE | weighted-avg-cost-calculator |
| 4 | refi-decision-analyzer | Current debt terms, remaining term, current NOI, rate environment, property value | Refi scenarios (rate/term, cash-out, supplemental), NPV of refi vs. hold, prepayment penalty analysis, breakeven timeline | REFI: net benefit positive. HOLD: prepayment penalty or rate environment unfavorable. SELL: if refi uneconomic and hold thesis broken | prepayment-penalty-calculator, rate-scenario-modeler |

## Data Handoff Specifications

### Step 1 -> 2a (Underwriting to Loan Sizing)
- **Payload**: `{stabilized_noi, property_value, asset_type, market, vintage, borrower_entity, proforma_cashflows[]}`
- **Notes**: Loan sizing needs the full cashflow stream for DSCR testing across the hold period

### Step 1 -> 2b (Underwriting to Mezz/Pref)
- **Payload**: `{total_cost_basis, senior_debt_amount, equity_gap, deal_risk_score, projected_cashflows_after_senior_debt[]}`
- **Dependency**: Requires step 2a output (senior debt amount) to size the equity gap. Runs sequentially after 2a despite parallel notation in diagram

### Step 1 -> 2c (Underwriting to JV Structure)
- **Payload**: `{total_equity_required, gp_coinvest_pct, fund_strategy, target_irr, hold_period}`
- **Dependency**: Requires step 2b output (if mezz/pref used) to know true equity requirement. Otherwise uses equity gap from 2a

### Steps 2a+2b+2c -> 3 (All Capital Layers to Optimizer)
- **Payload**: `{senior_debt{amount, rate, term, io_period, amort, covenants}, mezz_pref{amount, coupon, term, prepayment_terms} | null, jv_equity{total, gp_share, lp_share, waterfall_structure{}}, total_sources_uses{}}`
- **Merge point**: All three layers must be defined (or explicitly null) before optimization

### Step 3 -> 4 (Optimizer to Refi Analysis)
- **Payload**: `{current_capital_stack{}, remaining_loan_term, current_noi, current_property_value, rate_environment{}, prepayment_terms{}}`
- **Timing**: This handoff occurs during hold period, not at initial closing. The optimizer output becomes the baseline for future refi analysis

## Decision Gates Summary

| Gate | Location | Outcomes |
|------|----------|----------|
| Lender Constraint Check | After step 2a | Proceed (terms workable), seek alternatives (terms too tight), or restructure deal |
| Mezz Accretion Test | After step 2b | Include mezz (accretive to sponsor), exclude mezz (dilutive or unnecessary) |
| LP Marketability | After step 2c | Terms marketable (proceed), adjust (revise promote/pref), or change LP target |
| Final Stack Approval | After step 3 | PROCEED (levered returns meet hurdle), RESTRUCTURE (loop to 2a-2c), or KILL deal |
| Refi Decision | After step 4 | REFI (positive NPV), HOLD (stay with current debt), SELL (exit disposition chain) |

## Exit Conditions

- **Success**: Capital stack fully structured, all commitments secured, ready for closing
- **Restructure**: Returns insufficient at current terms. Loop back to loan sizing with adjusted parameters
- **Kill**: No capital structure produces acceptable returns. Deal dies
- **Refi Exit**: Refi analysis triggers disposition chain (sell) or loops back to loan sizing (new debt)

## Estimated Time Savings

| Phase | Manual | Automated Chain | Savings |
|-------|--------|-----------------|---------|
| Loan sizing + lender comparison | 8-12 hrs | 1-2 hrs | 80-85% |
| Mezz/pref structuring | 4-8 hrs | 30-60 min | 85-90% |
| JV waterfall modeling | 6-12 hrs | 1-2 hrs | 80-85% |
| Stack optimization + sensitivity | 4-8 hrs | 30-60 min | 85-90% |
| Refi analysis | 4-6 hrs | 30-60 min | 85-90% |
| **Total per deal** | **26-46 hrs** | **4-7 hrs** | **~83%** |
