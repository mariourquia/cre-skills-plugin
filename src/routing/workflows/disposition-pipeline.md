# Workflow Chain: Disposition Pipeline

## Purpose

Evaluates whether to sell, hold, or refinance a property, then executes the chosen path. Triggered by approaching hold period target, underperformance, portfolio rebalancing needs, or opportunistic market conditions. Branches into three distinct exit paths with potential 1031 exchange execution on the sell path.

## Chain Diagram

```
property-performance-dashboard
  |
  v
disposition-strategy-engine (sell vs. hold vs. refi)
  |
  +--> [HOLD] --> refi-decision-analyzer
  +--> [SELL] --> disposition-prep-kit --> 1031-exchange-executor
  +--> [REFI] --> loan-sizing-engine
```

## Entry Trigger Conditions

- Hold period reaches target year (typically year 3-5 for value-add, year 7-10 for core-plus)
- Asset consistently underperforms proforma with no credible path to recovery
- Portfolio review identifies strategic disposition candidate (sector rotation, geographic exit, capital recycling)
- Unsolicited offer received above current hold value
- Debt maturity within 18 months forces hold-vs-sell-vs-refi decision
- Fund approaching wind-down or liquidity event
- Market cycle positioner signals peak pricing window

## Step-by-Step Breakdown

| Step | Skill | Inputs | Outputs | Decision Gate | Daily-Ops Skills Used |
|------|-------|--------|---------|---------------|----------------------|
| 1 | property-performance-dashboard | Current financials, trailing 12 actuals, proforma benchmarks, occupancy data | Performance summary, NOI trend, value estimate range, hold-period return to date | None -- informational feed | monthly-reporting-automator, gl-import-mapper |
| 2 | disposition-strategy-engine | Performance summary, remaining hold period, current market conditions, debt maturity schedule, fund objectives, tax basis | Sell/hold/refi recommendation with supporting analysis, estimated proceeds (net of costs and taxes), opportunity cost of holding, IRR impact of each path | THREE-WAY GATE: SELL, HOLD, or REFI. Each triggers a different downstream path | tax-basis-calculator, opportunity-cost-modeler |
| 3a | refi-decision-analyzer (HOLD path) | Current debt terms, NOI trajectory, rate environment, property value, remaining hold thesis | Refi scenarios, NPV comparison, cash-out opportunity, covenant compliance forecast | REFI: proceed to loan-sizing-engine. HOLD CURRENT DEBT: no action, return to hold-period-management | prepayment-penalty-calculator, rate-scenario-modeler |
| 3b-i | disposition-prep-kit (SELL path) | Property data package, financials, capital improvement history, tenant roster, environmental/title status | Marketing package (OM), data room checklist, broker selection criteria, pricing guidance, timeline | Broker hired and marketing launched. If no acceptable offers after marketing period, reassess (return to step 2) | om-builder, data-room-organizer, broker-fee-calculator |
| 3b-ii | 1031-exchange-executor (SELL path, post-contract) | Sale proceeds estimate, tax basis, depreciation recapture, replacement property criteria | Exchange timeline, QI selection checklist, identification period tracking, replacement property screen, boot calculation | EXCHANGE: identify replacement property within 45 days. NO EXCHANGE: take taxable gain. FAILED EXCHANGE: contingency plan | exchange-deadline-tracker, boot-minimizer, replacement-property-screener |
| 3c | loan-sizing-engine (REFI path) | Current NOI, property value, borrower profile, target loan terms | Refi loan sizing, rate comparison, cash-out proceeds, new debt service coverage | Lender selected and term sheet executed. Proceed to closing | rate-lock-tracker, lender-term-comparator |

## Data Handoff Specifications

### Step 1 -> 2 (Dashboard to Strategy Engine)
- **Payload**: `{property_id, trailing_12_noi, occupancy_rate, noi_trend_direction, current_value_estimate, original_basis, accumulated_depreciation, debt_balance, debt_maturity_date, remaining_hold_target_years, fund_objectives}`
- **Notes**: Strategy engine needs both financial performance and strategic context (fund lifecycle, portfolio allocation)

### Step 2 -> 3a (Strategy to Refi Analyzer -- HOLD path)
- **Payload**: `{current_loan{balance, rate, maturity, prepayment_terms}, property_value, current_noi, noi_growth_projection, hold_extension_years, rate_environment{}}`
- **Condition**: Disposition strategy engine recommends HOLD

### Step 2 -> 3b-i (Strategy to Disposition Prep -- SELL path)
- **Payload**: `{property_data_package{}, financials{t12, budget, proforma}, pricing_guidance{target_price, min_acceptable, cap_rate_range}, sale_timeline_target, tax_implications{basis, depreciation_recapture, capital_gains}}`
- **Condition**: Disposition strategy engine recommends SELL

### Step 3a -> loan-sizing-engine (Refi Analyzer to Loan Sizing -- if refi confirmed)
- **Payload**: `{property_value, stabilized_noi, target_loan_amount, target_term, cash_out_desired, borrower_entity}`
- **Condition**: Refi NPV positive and decision confirmed
- **Notes**: This hands off to the capital-stack-assembly chain (step 2a)

### Step 3b-i -> 3b-ii (Disposition Prep to 1031 Exchange)
- **Payload**: `{estimated_net_proceeds, closing_date_estimate, tax_basis, depreciation_recapture_amount, replacement_property_criteria{type, geography, price_range, yield_target}}`
- **Condition**: Seller elects 1031 exchange treatment (vs. taxable sale)
- **Notes**: 1031 executor must engage qualified intermediary before closing. 45-day identification and 180-day closing deadlines are absolute

## Decision Gates Summary

| Gate | Location | Outcomes |
|------|----------|----------|
| Disposition Strategy | After step 2 | SELL (enter sell path), HOLD (enter hold/refi path), REFI (enter refi path) |
| Refi Viability | After step 3a | REFI (proceed to loan sizing), HOLD CURRENT DEBT (return to hold-period-management), SELL (pivot to sell path) |
| Marketing Response | After step 3b-i | Offers received (proceed to negotiation/closing), no acceptable offers (return to step 2 or adjust pricing) |
| 1031 Election | Before step 3b-ii | EXCHANGE (engage QI, start clock), TAXABLE SALE (skip exchange, take gain) |
| Replacement ID | 45 days post-close | Identified (proceed to acquire replacement), failed to ID (exchange collapses, recognize gain) |

## Branch Path Details

### SELL Path: Full Execution Sequence
1. Disposition prep kit builds marketing materials and data room
2. Select and engage listing broker
3. Marketing period (typically 30-60 days for marketed deal, or negotiate directly if off-market)
4. Best-and-final offers, select buyer
5. PSA negotiation and execution
6. Buyer due diligence period
7. If 1031 elected: engage QI, structure exchange before closing
8. Close sale, distribute proceeds
9. If 1031: 45-day identification, 180-day acquisition of replacement

### HOLD Path: Re-evaluation Sequence
1. Refi analyzer evaluates current debt vs. available terms
2. If refi attractive: execute refi via loan-sizing-engine (capital-stack-assembly chain)
3. If refi not attractive: hold current debt, continue hold-period-management chain
4. Reset disposition analysis trigger for next review cycle (typically annual)

### REFI Path: Direct to Capital Markets
1. Loan sizing engine sizes new loan
2. Lender selection and term sheet negotiation
3. Refi closing, payoff existing debt
4. Cash-out proceeds distributed or reinvested
5. Return to hold-period-management chain with new debt terms

## Exit Conditions

- **SELL complete**: Property sold, proceeds distributed, 1031 exchange executed (if applicable). Asset exits portfolio
- **HOLD confirmed**: Return to hold-period-management chain. Schedule next disposition review
- **REFI complete**: New loan in place. Return to hold-period-management chain with updated capital structure

## Estimated Time Savings

| Phase | Manual | Automated Chain | Savings |
|-------|--------|-----------------|---------|
| Sell/hold/refi analysis | 10-20 hrs | 2-4 hrs | 80% |
| Disposition prep (OM, data room) | 20-40 hrs | 5-10 hrs | 70-75% |
| 1031 exchange management | 10-20 hrs | 3-5 hrs | 70-75% |
| Refi analysis + sizing | 8-12 hrs | 1-2 hrs | 85% |
| **Total per disposition event** | **48-92 hrs** | **11-21 hrs** | **~77%** |
