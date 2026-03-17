# Workflow Chain: Deal Pipeline -- Full Acquisition Lifecycle

## Purpose

End-to-end acquisition workflow from initial deal sourcing through post-close asset management. This is the core business process for any acquisitions-focused CRE shop. Each node represents a skill (or skill cluster) with defined inputs, outputs, and decision gates that determine whether the deal advances, dies, or loops back.

## Chain Diagram

```
sourcing-outreach-system --> deal-quick-screen --> [KILL or KEEP]
  |
  v [KEEP]
om-reverse-pricing --> rent-roll-analyzer --> acquisition-underwriting-engine
  |                                                      |
  v                                                      v
submarket-truth-serum                         sensitivity-stress-test
  |                                                      |
  v                                                      v
comp-snapshot + market-cycle-positioner --> ic-memo-generator
  |
  v
loi-offer-builder --> psa-redline-strategy --> dd-command-center --> [CLOSE]
  |
  v [POST-CLOSE]
annual-budget-engine --> property-performance-dashboard
```

## Entry Trigger Conditions

- New deal hits inbox (broker OM, off-market lead, auction listing)
- Sourcing campaign generates qualified lead via sourcing-outreach-system
- JV partner forwards opportunity
- Internal portfolio review identifies bolt-on acquisition target

## Step-by-Step Breakdown

| Step | Skill | Inputs | Outputs | Decision Gate | Daily-Ops Skills Used |
|------|-------|--------|---------|---------------|----------------------|
| 1 | sourcing-outreach-system | Target market criteria, property type filters, broker contact list | Qualified lead list, outreach log, response tracking | None -- feed-forward | broker-crm-tracker |
| 2 | deal-quick-screen | OM PDF or listing summary, fund investment criteria, target return thresholds | Pass/fail scorecard, red flag list, preliminary cap rate | KILL: score < threshold. KEEP: score >= threshold | om-parser, back-of-envelope-calc |
| 3 | om-reverse-pricing | Broker asking price, stated NOI, OM financials | Implied cap rate, broker assumptions exposed, adjusted pricing view | None -- informational input to underwriting | t12-normalizer |
| 4 | rent-roll-analyzer | Raw rent roll (PDF/Excel), lease abstracts | Cleaned rent roll, WALT, rollover schedule, mark-to-market gaps, tenant credit flags | None -- feeds underwriting | rent-roll-formatter, lease-abstract-extractor |
| 5 | acquisition-underwriting-engine | Cleaned rent roll, T12 financials, capex assumptions, market rents, financing terms | Full proforma (10-yr DCF), IRR/equity multiple, going-in/exit yields, return waterfall | Soft gate: does modeled return meet fund hurdle? If no, loop to step 3 to renegotiate or KILL | t12-normalizer, capex-estimator, closing-cost-calculator |
| 6 | sensitivity-stress-test | Base case proforma from step 5 | Tornado charts, scenario matrix (rent growth, exit cap, vacancy, rate changes), breakeven analysis | KILL: downside scenarios breach covenant or lose principal. KEEP: downside within tolerance | monte-carlo-runner |
| 7 | submarket-truth-serum | Property address, submarket boundaries | Supply pipeline, absorption trends, demographic drivers, employer concentration, infrastructure projects | Qualitative gate: does submarket thesis hold? | census-data-puller, costar-data-bridge |
| 8 | comp-snapshot | Property type, submarket, vintage | Recent sale comps, cap rate context, price-per-unit/SF benchmarks | None -- feeds IC memo | comp-scraper |
| 9 | market-cycle-positioner | Submarket data from step 7, macro indicators | Cycle phase diagnosis (expansion/hyper-supply/recession/recovery), timing recommendation | Advisory: proceed with caution if late-cycle | macro-indicator-tracker |
| 10 | ic-memo-generator | Proforma, sensitivity output, submarket analysis, comps, cycle position, rent roll summary | Investment Committee memo (PDF), executive summary, risk matrix, recommendation | IC VOTE: approve, reject, or revise terms. If reject, KILL. If revise, loop to step 5 | memo-template-engine |
| 11 | loi-offer-builder | Approved terms from IC, pricing from proforma, deal structure preferences | LOI document, key business terms summary, negotiation range matrix | Seller accepts, counters, or rejects. Counter: loop. Reject: KILL or re-bid | term-sheet-formatter |
| 12 | psa-redline-strategy | Executed LOI, standard PSA template, deal-specific risks | Redline priority list, fallback positions, key protective clauses | PSA execution or deal collapse | legal-clause-library |
| 13 | dd-command-center | Executed PSA, property data package, inspection reports, title/survey, environmental | DD checklist tracker, issue log, retrade justification (if needed), closing checklist | CLOSE: all DD clear. RETRADE: material issues found. WALK: fatal flaw discovered | inspection-tracker, title-review-helper, environmental-flag-checker |
| 14 | annual-budget-engine | Closed deal financials, property management plan, capital plan | Year-1 operating budget, staffing plan, capital schedule | None -- operational handoff | budget-line-item-library |
| 15 | property-performance-dashboard | Monthly actuals, budget, proforma benchmarks | Variance reports, KPI dashboard, NOI tracking, occupancy trends | Ongoing monitoring. Triggers noi-sprint-plan if underperforming | monthly-reporting-automator |

## Data Handoff Specifications

### Step 1 -> 2 (Sourcing to Screen)
- **Payload**: `{property_address, property_type, unit_count_or_sf, asking_price, broker_contact, om_url_or_pdf}`
- **Format**: JSON record per lead, or OM PDF attachment

### Step 2 -> 3 (Screen to Reverse Pricing)
- **Payload**: `{asking_price, stated_noi, stated_cap_rate, om_financials_extracted}`
- **Condition**: Only if deal passes quick screen (KEEP)

### Step 2 -> 4 (Screen to Rent Roll)
- **Payload**: `{rent_roll_file, lease_abstracts[], property_type}`
- **Parallel with step 3**

### Steps 3+4 -> 5 (Pricing + Rent Roll to Underwriting)
- **Payload**: `{adjusted_noi, cleaned_rent_roll, market_rents, capex_assumptions, financing_terms, reverse_pricing_output}`
- **Merge point**: both must complete before underwriting begins

### Step 5 -> 6 (Underwriting to Stress Test)
- **Payload**: `{base_case_proforma, key_assumptions{}, return_metrics{}}`

### Step 5 -> 7 (Underwriting to Submarket -- parallel with 6)
- **Payload**: `{property_address, submarket_id, property_type}`

### Steps 6+7+8+9 -> 10 (Analysis cluster to IC Memo)
- **Payload**: `{proforma, sensitivity_output, submarket_analysis, comp_set, cycle_position, deal_summary}`
- **Merge point**: all four must complete

### Step 10 -> 11 (IC Memo to LOI)
- **Payload**: `{approved_price, approved_terms{}, contingencies[], ic_conditions[]}`
- **Condition**: IC approval received

### Step 11 -> 12 (LOI to PSA)
- **Payload**: `{executed_loi, business_terms{}, negotiation_notes}`

### Step 12 -> 13 (PSA to DD)
- **Payload**: `{executed_psa, dd_period_days, key_contingencies[], inspection_scope}`

### Step 13 -> 14 (DD to Budget -- post-close)
- **Payload**: `{final_closing_statement, actual_purchase_price, dd_findings[], property_condition_report}`

### Step 14 -> 15 (Budget to Dashboard)
- **Payload**: `{approved_budget, capital_schedule, kpi_targets{}, reporting_cadence}`

## Decision Gates Summary

| Gate | Location | Outcomes |
|------|----------|----------|
| Quick Screen | After step 2 | KILL (fail) or KEEP (advance) |
| Return Hurdle | After step 5 | Meets hurdle (advance), below hurdle (renegotiate or KILL) |
| Stress Test | After step 6 | Downside acceptable (advance) or unacceptable (KILL) |
| Submarket Thesis | After step 7 | Thesis holds (advance) or broken (KILL) |
| IC Vote | After step 10 | Approve, revise terms (loop to 5), or reject (KILL) |
| Seller Response | After step 11 | Accept (advance), counter (loop), reject (KILL) |
| DD Clearance | After step 13 | Clear (CLOSE), retrade (renegotiate), or walk (KILL) |

## Exit Conditions

- **Success**: Property closed, transitioned to asset management (steps 14-15)
- **Kill**: Deal terminated at any decision gate. Log reason in deal-tracking CRM
- **Pause**: IC requests additional analysis. Chain pauses at step 10, loops back to steps 5-9

## Estimated Time Savings

| Phase | Manual | Automated Chain | Savings |
|-------|--------|-----------------|---------|
| Sourcing + Screen | 4-8 hrs/deal | 30-60 min | 80-90% |
| Underwriting + Analysis | 20-40 hrs | 4-8 hrs | 75-80% |
| IC Memo Prep | 8-16 hrs | 2-4 hrs | 70-80% |
| LOI + PSA Strategy | 4-8 hrs | 1-2 hrs | 70-80% |
| DD Management | 40-80 hrs | 15-25 hrs | 50-65% |
| Post-Close Setup | 8-16 hrs | 2-4 hrs | 70-80% |
| **Total per deal** | **84-168 hrs** | **25-45 hrs** | **~70%** |
