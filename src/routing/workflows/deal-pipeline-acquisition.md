# Workflow Chain: Deal Pipeline -- Full Acquisition Lifecycle

## Purpose

End-to-end acquisition workflow from initial deal sourcing through post-close asset management. This is the core business process for any acquisitions-focused CRE shop. Each node represents a skill (or skill cluster) with defined inputs, outputs, and decision gates that determine whether the deal advances, dies, or loops back.

## Chain Diagram

```
sourcing-outreach-system --> deal-quick-screen --> [KILL or KEEP]
  |
  v [KEEP]
om-reverse-pricing --> rent-roll-analyzer --> tenant-credit-analyzer
  |                          |                         |
  v                          v                         v
submarket-truth-serum   acquisition-underwriting-engine --> sensitivity-stress-test
  |                          |
  v                          v
comp-snapshot + market-cycle-positioner --> ic-memo-generator
  |
  v
loi-offer-builder --> psa-redline-strategy --> dd-command-center
  |                         |                      |
  v                         v                      v
[FINANCING TRACK]   transfer-document-preparer  title-commitment-reviewer
loan-sizing-engine --> term-sheet-builder --> loan-document-reviewer
  |
  v
closing-checklist-tracker --> funds-flow-calculator --> [CLOSE]
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
| 4 | rent-roll-analyzer | Raw rent roll (PDF/Excel), lease abstracts | Cleaned rent roll, WALT, rollover schedule, mark-to-market gaps, tenant credit flags | None -- feeds underwriting and tenant credit | rent-roll-formatter, lease-abstract-extractor |
| 4a | tenant-credit-analyzer | Cleaned rent roll from step 4, tenant financials, guarantor docs | Tenant credit scores, default probability, guarantor coverage ratios, watch list | None -- informs underwriting assumptions and loan sizing | lease-abstract-extractor |
| 5 | acquisition-underwriting-engine | Cleaned rent roll, T12 financials, capex assumptions, market rents, financing terms, tenant credit summary | Full proforma (10-yr DCF), IRR/equity multiple, going-in/exit yields, return waterfall | Soft gate: does modeled return meet fund hurdle? If no, loop to step 3 to renegotiate or KILL | t12-normalizer, capex-estimator, closing-cost-calculator |
| 6 | sensitivity-stress-test | Base case proforma from step 5 | Tornado charts, scenario matrix (rent growth, exit cap, vacancy, rate changes), breakeven analysis | KILL: downside scenarios breach covenant or lose principal. KEEP: downside within tolerance | monte-carlo-runner |
| 7 | submarket-truth-serum | Property address, submarket boundaries | Supply pipeline, absorption trends, demographic drivers, employer concentration, infrastructure projects | Qualitative gate: does submarket thesis hold? | census-data-puller, costar-data-bridge |
| 8 | comp-snapshot | Property type, submarket, vintage | Recent sale comps, cap rate context, price-per-unit/SF benchmarks | None -- feeds IC memo | comp-scraper |
| 9 | market-cycle-positioner | Submarket data from step 7, macro indicators | Cycle phase diagnosis (expansion/hyper-supply/recession/recovery), timing recommendation | Advisory: proceed with caution if late-cycle | macro-indicator-tracker |
| 10 | ic-memo-generator | Proforma, sensitivity output, submarket analysis, comps, cycle position, rent roll summary | Investment Committee memo (PDF), executive summary, risk matrix, recommendation | IC VOTE: approve, reject, or revise terms. If reject, KILL. If revise, loop to step 5 | memo-template-engine |
| 11 | loi-offer-builder | Approved terms from IC, pricing from proforma, deal structure preferences | LOI document, key business terms summary, negotiation range matrix | Seller accepts, counters, or rejects. Counter: loop. Reject: KILL or re-bid | term-sheet-formatter |
| 12 | psa-redline-strategy | Executed LOI, standard PSA template, deal-specific risks | Redline priority list, fallback positions, key protective clauses | PSA execution or deal collapse | legal-clause-library |
| **FINANCING TRACK** | | | | | |
| 12a | loan-sizing-engine | Proforma NOI, purchase price, lender market conditions | Max loan proceeds, DSCR/LTV/DY sizing, agency vs bridge matrix | Financing feasible at target leverage? If no, adjust capital stack | t12-normalizer, debt-covenant-monitor |
| 12b | term-sheet-builder | Loan sizing output, capital stack structure, lender quotes | Lender term sheet comparison, rate/fee matrix, recommended lender | Acceptable terms exist? If no, explore mezz/pref equity alternatives | -- |
| 12c | loan-document-reviewer | Executed term sheet, draft loan documents (note, mortgage, guaranty) | Redline priority list, covenant map, cash management triggers, critical dates | Documents acceptable? Flag any covenant breach risks pre-close | debt-covenant-monitor |
| **DD + LEGAL TRACK** | | | | | |
| 13 | dd-command-center | Executed PSA, property data package, inspection reports, title/survey, environmental | DD checklist tracker, issue log, retrade justification (if needed), closing checklist | CLOSE: all DD clear. RETRADE: material issues found. WALK: fatal flaw discovered | inspection-tracker, title-review-helper, environmental-flag-checker |
| 13a | title-commitment-reviewer | Title commitment, Schedule B exceptions, survey, title insurance requirements | Exception analysis, curative actions required, insured endorsements needed, cleared-to-close status | Clear title exceptions before close. Material defects: RETRADE or WALK | -- |
| 13b | transfer-document-preparer | Executed PSA, title commitment, entity docs, assignment of leases | Deed draft, assignment of leases and contracts, bill of sale, entity authority docs | Documents executed by both parties before closing | legal-clause-library |
| **CLOSING** | | | | | |
| 14 | closing-checklist-tracker | All executed documents, title clearance, lender funding conditions, tenant notifications | Master closing checklist, open items log, closing timeline | All items cleared before funding | estoppel-certificate-generator |
| 14a | funds-flow-calculator | Purchase price, loan proceeds, prorations, closing costs, credits | Final settlement statement (HUD equivalent), wire amounts by party, net equity at close | Settlement statement agreed by all parties | closing-cost-calculator |
| **POST-CLOSE** | | | | | |
| 15 | annual-budget-engine | Closed deal financials, property management plan, capital plan | Year-1 operating budget, staffing plan, capital schedule | None -- operational handoff | budget-line-item-library |
| 16 | property-performance-dashboard | Monthly actuals, budget, proforma benchmarks | Variance reports, KPI dashboard, NOI tracking, occupancy trends | Ongoing monitoring. Triggers noi-sprint-plan if underperforming | monthly-reporting-automator |

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

### Step 4 -> 4a (Rent Roll to Tenant Credit -- parallel)
- **Payload**: `{cleaned_rent_roll, tenant_roster[], lease_abstracts[]}`
- **Parallel with step 3**

### Step 4a -> 5 (Tenant Credit to Underwriting)
- **Payload**: `{tenant_credit_scores{}, default_probabilities{}, guarantor_coverage_ratios{}, watch_list[]}`
- **Merge point**: tenant credit output feeds underwriting base case vacancy and credit loss assumptions

### Step 12 -> 12a (PSA to Loan Sizing -- parallel with DD)
- **Payload**: `{executed_psa, proforma_noi, purchase_price, property_type, market_conditions}`
- **Parallel track alongside DD**

### Step 12a -> 12b (Loan Sizing to Term Sheet)
- **Payload**: `{max_loan_proceeds, dscr, ltv, debt_yield, sizing_scenarios{}, lender_shortlist[]}`

### Step 12b -> 12c (Term Sheet to Loan Document Review)
- **Payload**: `{executed_term_sheet, draft_loan_documents[], lender_name, loan_amount, key_covenants{}}`

### Step 12 -> 13b (PSA to Transfer Docs -- parallel with DD)
- **Payload**: `{executed_psa, seller_entity_docs, title_commitment, assignment_schedule[]}`
- **Parallel with DD steps 13 and 13a**

### Step 13 -> 13a (DD to Title Review -- parallel)
- **Payload**: `{title_commitment, schedule_b_exceptions[], survey, property_address}`
- **Parallel with other DD workstreams**

### Steps 12c + 13 + 13a + 13b -> 14 (All tracks converge at Closing Checklist)
- **Payload**: `{loan_docs_executed, title_clearance_status, transfer_docs_executed, dd_findings[], open_items[]}`
- **Merge point**: all parallel tracks must clear before closing checklist is marked complete

### Step 14 -> 14a (Closing Checklist to Funds Flow)
- **Payload**: `{purchase_price, loan_proceeds, prorations{}, closing_costs{}, credits{}, escrow_amounts{}}`
- **Condition**: checklist fully cleared

### Step 14a -> 15 (Funds Flow to Budget -- post-close)
- **Payload**: `{final_closing_statement, actual_purchase_price, net_equity_at_close, dd_findings[], property_condition_report}`

### Step 15 -> 16 (Budget to Dashboard)
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
| Financing Feasibility | After step 12b | Acceptable lender terms exist (advance) or restructure capital stack |
| Loan Docs Acceptable | After step 12c | Proceed to close or renegotiate covenant terms |
| DD Clearance | After step 13 | Clear (CLOSE), retrade (renegotiate), or walk (KILL) |
| Title Clearance | After step 13a | Exceptions cured (advance) or material defect (RETRADE or WALK) |
| Funds Flow Agreed | After step 14a | All parties confirm wire amounts (advance to fund) |

## Exit Conditions

- **Success**: Property closed, transitioned to asset management (steps 15-16)
- **Kill**: Deal terminated at any decision gate. Log reason in deal-tracking CRM
- **Pause**: IC requests additional analysis. Chain pauses at step 10, loops back to steps 5-9

## Estimated Time Savings

| Phase | Manual | Automated Chain | Savings |
|-------|--------|-----------------|---------|
| Sourcing + Screen | 4-8 hrs/deal | 30-60 min | 80-90% |
| Underwriting + Analysis | 20-40 hrs | 4-8 hrs | 75-80% |
| Tenant Credit Analysis | 4-8 hrs | 1-2 hrs | 70-80% |
| IC Memo Prep | 8-16 hrs | 2-4 hrs | 70-80% |
| LOI + PSA Strategy | 4-8 hrs | 1-2 hrs | 70-80% |
| Financing (Term Sheet + Loan Docs) | 8-16 hrs | 2-4 hrs | 70-80% |
| DD Management | 40-80 hrs | 15-25 hrs | 50-65% |
| Title + Transfer Docs | 6-12 hrs | 2-3 hrs | 65-75% |
| Closing + Funds Flow | 4-8 hrs | 1-2 hrs | 70-80% |
| Post-Close Setup | 8-16 hrs | 2-4 hrs | 70-80% |
| **Total per deal** | **106-212 hrs** | **29-55 hrs** | **~72%** |
