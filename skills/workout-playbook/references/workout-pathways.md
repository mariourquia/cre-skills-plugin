# Workout Pathways Reference

## Overview

Five-pathway NPV framework for distressed CRE loans and assets: extend and
pretend, loan modification, forbearance agreement, note sale, and foreclosure
or discounted payoff (DPO). Each pathway includes legal mechanics, timeline,
recovery analysis, and decision criteria.

---

## 1. The Five Pathways

```
                        DISTRESSED LOAN / ASSET
                                |
    +----------+--------+------+-------+-----------+
    |          |        |              |           |
  PATH 1    PATH 2   PATH 3        PATH 4      PATH 5
  Extend    Modify   Forbear       Note Sale   Foreclosure
  & Pretend                                    or DPO

  Least                                        Most
  Disruptive                               Disruptive
  Fastest                                  Slowest
  Lowest Cost                              Highest Cost
```

---

## 2. Path 1: Extend and Pretend

### Description

Lender extends the maturity date without material modification to economics.
Buys time for borrower to stabilize operations, refinance, or sell.

### Mechanics

```yaml
structure:
  maturity_extension: "6-24 months"
  rate_change: "None or minimal (may add 25-50bps)"
  principal_curtailment: "May require 5-10% paydown"
  fees: "Extension fee 0.25-1.0% of balance"
  covenants: "Tightened (lower DSCR trip, more frequent reporting)"
  recourse: "May add partial recourse or guarantee enhancement"

legal_documents:
  - "Modification agreement (extending maturity)"
  - "Reaffirmation of all loan documents"
  - "Borrower certificate of no defenses"
  - "Updated title endorsement"
  - "Updated environmental reliance letter"

timeline:
  negotiation: "2-4 weeks"
  documentation: "2-4 weeks"
  total: "4-8 weeks"
```

### When to Use

```
FAVORABLE when:
  - Property is performing but loan maturity creates refinance gap
  - Interest rate environment is expected to improve
  - Borrower has equity and is motivated
  - Property needs 6-12 months to reach stabilization
  - Lender does not want to take a loss or foreclose

UNFAVORABLE when:
  - Property has fundamental value impairment
  - Borrower has negative equity (loan > value)
  - No realistic path to refinance even with extension
  - Lender needs to reduce exposure for regulatory reasons
```

### NPV Framework

```
NPV_extend = sum(t=1..extension_months) [debt_service_payment / (1+r)^t]
           + P(refinance) * [principal_repayment / (1+r)^maturity]
           + (1-P(refinance)) * NPV_next_best_path
           + extension_fee / (1+r)^0
           - administrative_cost

Compare to: NPV of foreclosure now, NPV of note sale now
If NPV_extend > alternatives: extend.
```

---

## 3. Path 2: Loan Modification

### Description

Material change to loan economics: rate reduction, principal reduction,
amortization change, or debt conversion. More significant than extension.

### Modification Types

```yaml
modification_types:
  rate_reduction:
    description: "Reduce interest rate below original terms"
    typical_range: "100-300bps below original"
    mechanism: "A/B note structure or simple rate reduction"
    lender_accounting: "TDR (Troubled Debt Restructuring) under ASC 310-40"

  a_b_note_structure:
    description: "Split note into performing 'A' note and hope 'B' note"
    a_note:
      amount: "Supported by property cash flow at market DSCR"
      rate: "Market rate or slightly below"
      amortization: "Standard 25-30 year"
      priority: "Senior"
    b_note:
      amount: "Remaining balance above A note"
      rate: "Accrual only (0% cash pay)"
      payment: "Deferred; paid from excess cash flow or sale/refi proceeds"
      priority: "Subordinate to A note"
    example:
      original_loan: 10000000
      property_value: 8000000
      supportable_a_note: 6400000  # 80% of value at market DSCR
      b_note: 3600000
      b_note_recovery_probability: 0.35

  principal_forgiveness:
    description: "Permanent write-down of principal balance"
    rare: true
    when_used: "Deeply impaired assets where forgiveness < foreclosure loss"
    tax_consequence: "Borrower has cancellation of debt (COD) income"
    lender_accounting: "Immediate loss recognition"

  amortization_change:
    description: "Extend amortization to reduce monthly payment"
    original: "25-year amortization"
    modified: "30-year or 35-year amortization"
    effect: "Reduces P&I payment by 8-15%"
    lender_risk: "Slower principal paydown, higher terminal balance"

  interest_only_conversion:
    description: "Convert amortizing loan to interest-only"
    term: "12-24 months IO"
    effect: "Reduces debt service by 25-40%"
    use_case: "Temporary cash flow stress, property expected to recover"
```

### Legal Mechanics

```yaml
legal_process:
  pre_negotiation_agreement:
    purpose: "Protect lender's rights during negotiation"
    key_terms:
      - "Borrower acknowledges default"
      - "Lender reserves all rights and remedies"
      - "Negotiations are without prejudice"
      - "No oral modifications"

  modification_agreement:
    contents:
      - "Recitals (existing loan, events of default, borrower's request)"
      - "Modified terms (rate, maturity, amortization, covenants)"
      - "Additional conditions (curtailment, reserve funding, guarantee)"
      - "Borrower representations and warranties"
      - "Reaffirmation of loan documents"
      - "Release of claims against lender (mutual or one-way)"
    recording: "Record modification agreement with county"
    title: "Obtain date-down endorsement (no intervening liens)"

  regulatory_considerations:
    tdr_reporting: "Bank must report as TDR to regulators"
    impact_on_reserves: "May require additional loss reserves"
    risk_rating: "Loan remains classified/criticized until performance proven"
    seasoning: "Typically 6-12 months of performance before upgrade"
```

### NPV Framework

```
NPV_modify = sum(t=1..T) [modified_payment / (1+r)^t]
           + P(perform) * [balloon_repayment / (1+r)^T]
           + (1-P(perform)) * NPV_foreclosure_at_redefault
           - modification_costs

A/B note NPV:
  NPV_A = sum(t=1..T) [A_note_payment / (1+r)^t] + [A_principal / (1+r)^T]
  NPV_B = P(recovery) * [B_note_amount * recovery_rate / (1+r)^T]
  NPV_total = NPV_A + NPV_B - modification_costs
```

---

## 4. Path 3: Forbearance Agreement

### Description

Lender agrees to temporarily refrain from exercising remedies while borrower
works to cure defaults. Not a modification -- original terms remain in effect.

### Structure

```yaml
forbearance_terms:
  duration: "90-180 days (typical)"
  lender_agrees:
    - "Forbear from accelerating loan"
    - "Forbear from filing foreclosure"
    - "Forbear from enforcing certain covenants"
    - "Continue to accept partial payments (if applicable)"
  borrower_agrees:
    - "Acknowledge all existing defaults"
    - "Provide detailed financial reporting (weekly or monthly)"
    - "Execute business plan milestones"
    - "Fund additional reserves or provide additional collateral"
    - "Engage lender-approved property manager"
    - "Not seek additional financing without lender consent"
    - "Waive all defenses and counterclaims"

  business_plan:
    description: "Borrower submits and lender approves an action plan"
    components:
      - "Revenue improvement plan (lease-up, rent increases)"
      - "Expense reduction plan"
      - "Capital improvement plan (if needed)"
      - "Refinance or sale strategy with timeline"
    milestones:
      month_1: "[specific milestone]"
      month_2: "[specific milestone]"
      month_3: "[specific milestone]"
    failure_consequence: "Forbearance terminates, lender may exercise all remedies"

  forbearance_fee: "0.25-0.50% of loan balance"
  default_interest: "May accrue during forbearance (penalty rate)"
```

### When to Use

```
FAVORABLE when:
  - Borrower has a credible short-term cure plan
  - Default is monetary but expected to be cured (capital infusion pending)
  - Property is in transition and borrower needs time to execute
  - Lender wants to preserve relationship
  - Foreclosure timeline is long (6+ months) and forbearance is shorter

UNFAVORABLE when:
  - No credible path to cure within forbearance period
  - Borrower is non-cooperative or adversarial
  - Property value deteriorating (forbearance = more losses)
  - Lender needs to act quickly for regulatory reasons
```

---

## 5. Path 4: Note Sale

### Description

Lender sells the loan (performing, sub-performing, or non-performing) to a
third-party investor. Lender takes an immediate loss but eliminates ongoing
risk and administrative burden.

### Market Mechanics

```yaml
note_sale:
  buyer_types:
    - "Distressed debt funds (Lone Star, Cerberus, Oaktree)"
    - "Opportunity funds"
    - "Local/regional investors"
    - "Borrower themselves (discounted payoff via third party)"

  pricing:
    performing_note: "95-100% of par (minimal discount)"
    sub_performing: "75-90% of par"
    non_performing_with_equity: "60-80% of par"
    non_performing_no_equity: "40-65% of par"
    deeply_distressed: "20-40% of par"

    pricing_factors:
      property_value_to_debt: "Higher = higher price"
      property_type: "MF > Industrial > Office > Retail (current market)"
      geography: "Primary markets > Secondary > Tertiary"
      legal_status: "Pre-foreclosure > In foreclosure > Post-judgment"
      environmental: "Clean > RECs > Known contamination"
      borrower_cooperation: "Cooperative > Non-responsive > Adversarial"

  process:
    preparation:
      - "Prepare offering memorandum (loan summary, property info)"
      - "Assemble data room (loan docs, title, environmental, appraisal)"
      - "Engage loan sale advisor (optional but recommended)"
      timeline: "2-4 weeks"
    marketing:
      - "Distribute teasers to qualified buyers"
      - "Execute NDAs"
      - "Open data room for due diligence"
      - "Conduct property tours"
      timeline: "3-4 weeks"
    bidding:
      - "Best and final offers (BAFO)"
      - "Select winning bidder"
      - "Negotiate PSA"
      timeline: "2-3 weeks"
    closing:
      - "Execute assignment of mortgage"
      - "Transfer servicing"
      - "Deliver loan file"
      - "Notify borrower of assignment"
      timeline: "2-4 weeks"
    total_timeline: "9-15 weeks"

  seller_accounting:
    gain_loss: "Sale price - carrying value = gain/loss"
    reserve_release: "If previously reserved, loss may already be recognized"
    tax_treatment: "Ordinary loss (not capital loss) for bank seller"
```

### NPV Framework

```
NPV_note_sale = Sale_proceeds - Transaction_costs
              = (UPB * price_pct) - (broker_fee + legal + DD)

Compare to:
  NPV_foreclosure = Recovery_after_foreclosure - Foreclosure_costs - Time_value
  NPV_modification = PV of modified cash flows

Note sale wins when:
  Sale_proceeds > PV(expected recovery from hold/workout) - Carrying_costs
```

---

## 6. Path 5: Foreclosure / Discounted Payoff (DPO)

### Foreclosure

```yaml
foreclosure:
  types:
    judicial:
      description: "Court-supervised process; required in ~20 states"
      timeline: "6-18 months (varies dramatically by state)"
      states: ["NJ", "NY", "CT", "FL", "IL", "OH", "PA"]
      process:
        1: "File lis pendens (notice of foreclosure)"
        2: "Serve complaint on borrower and all parties in interest"
        3: "Borrower answer period (20-60 days)"
        4: "Discovery (if contested)"
        5: "Motion for summary judgment (or trial)"
        6: "Judgment of foreclosure"
        7: "Sheriff's sale"
        8: "Confirmation of sale"
        9: "Deed transfer and eviction"
      cost: "$50,000-$250,000+ (attorney, court, receiver)"

    non_judicial:
      description: "Power of sale in deed of trust; no court required"
      timeline: "2-6 months"
      states: ["TX", "CA", "GA", "CO", "AZ", "VA", "WA"]
      process:
        1: "Notice of default (record and serve)"
        2: "Cure period (varies by state)"
        3: "Notice of sale (publish and post)"
        4: "Trustee's sale (public auction)"
        5: "Deed transfer"
      cost: "$15,000-$75,000"

  timeline_by_state:
    fast_3_months: ["TX", "GA", "VA", "NH"]
    moderate_6_months: ["CA", "CO", "AZ", "WA", "TN"]
    slow_12_months: ["FL", "IL", "OH", "PA", "IN"]
    very_slow_18_plus: ["NJ", "NY", "CT", "HI"]

  receiver:
    description: "Court-appointed property manager during foreclosure"
    when_needed:
      - "Property is mismanaged"
      - "Borrower is collecting rents but not paying debt service"
      - "Property condition is deteriorating"
      - "Waste or environmental concerns"
    cost: "5-8% of gross revenue + legal fees to appoint"
    timeline_to_appoint: "2-6 weeks (emergency motion available)"

  deficiency_judgment:
    description: "Claim against borrower for shortfall (debt - foreclosure proceeds)"
    available_in: "Most states for commercial (non-residential)"
    anti_deficiency_states: ["CA (purchase money)", "AZ", "AK"]
    collectability: "Low for single-asset LLC borrowers; pursue guarantors"
    timeline: "Must file within statute of limitations (varies by state)"
```

### Discounted Payoff (DPO)

```yaml
dpo:
  description: |
    Borrower (or borrower's designee) pays less than full loan balance
    to satisfy the debt. Lender accepts the discount to avoid
    foreclosure costs and timeline.

  typical_discount: "10-40% of UPB"

  when_lender_accepts:
    - "Foreclosure costs + time > discount amount"
    - "Property value < loan balance (no equity)"
    - "Borrower bankruptcy risk (would reduce recovery further)"
    - "Property condition deteriorating"
    - "Regulatory pressure to resolve classified asset"

  negotiation_strategy:
    lender_perspective:
      floor: "max(foreclosure_recovery - foreclosure_costs, orderly_liquidation_value)"
      anchor: "UPB (start at par)"
      settlement_zone: "70-90% of UPB (depends on leverage)"
    borrower_perspective:
      anchor: "Distressed property value - 20%"
      ceiling: "Foreclosure value + foreclosure costs saved"
      settlement_zone: "60-80% of UPB"

  structure:
    all_cash: "Full DPO amount at closing"
    installment: "50% at closing, 25% at 90 days, 25% at 180 days"
    new_note: "DPO amount converted to new, performing note (less common)"

  tax_consequences:
    borrower:
      cod_income: "Forgiven amount = cancellation of debt income"
      exceptions:
        - "Insolvency exception (IRC 108(a)(1)(B))"
        - "Bankruptcy exception (IRC 108(a)(1)(A))"
        - "Qualified real property business exception (if applicable)"
    lender:
      loss_recognition: "Difference between carrying value and DPO received"
      charge_off: "Write down to DPO amount"

  legal_documentation:
    - "Payoff letter with explicit satisfaction language"
    - "Satisfaction of mortgage (recorded)"
    - "Mutual release of all claims"
    - "Tax reporting (1099-C for COD income, if > $600)"
```

---

## 7. Recovery Analysis Framework

### Path Comparison Template

```
                    | Path 1    | Path 2    | Path 3    | Path 4    | Path 5
                    | Extend    | Modify    | Forbear   | Note Sale | Foreclose
--------------------|-----------|-----------|-----------|-----------|----------
Expected Recovery   | $[amt]    | $[amt]    | $[amt]    | $[amt]    | $[amt]
Recovery Rate (%)   | [X]%      | [X]%      | [X]%      | [X]%      | [X]%
Timeline (months)   | [X]       | [X]       | [X]       | [X]       | [X]
Direct Costs        | $[amt]    | $[amt]    | $[amt]    | $[amt]    | $[amt]
Carrying Costs      | $[amt]    | $[amt]    | $[amt]    | $[amt]    | $[amt]
NPV of Recovery     | $[amt]    | $[amt]    | $[amt]    | $[amt]    | $[amt]
Probability Success | [X]%      | [X]%      | [X]%      | [X]%      | [X]%
Risk-Adj NPV        | $[amt]    | $[amt]    | $[amt]    | $[amt]    | $[amt]
Accounting Impact   | [desc]    | [desc]    | [desc]    | [desc]    | [desc]
Regulatory Impact   | [desc]    | [desc]    | [desc]    | [desc]    | [desc]
```

### Decision Framework

```
Step 1: Is borrower cooperative?
  YES -> Paths 1-3 are viable; also consider 5 (DPO)
  NO  -> Paths 4-5 preferred (note sale or foreclosure)

Step 2: Does borrower have equity in the property?
  YES (LTV < 90%) -> Paths 1-3 preferred (borrower motivated to perform)
  NO  (LTV > 100%) -> Paths 4-5 preferred (borrower may walk away)

Step 3: Is the property performing (positive cash flow)?
  YES -> Path 1 or 2 (preserve cash flow stream)
  NO  -> Path 3 (forbear while fixing) or Path 5 (exit)

Step 4: Is there a realistic path to refinance or sale?
  YES (within 12-24 months) -> Path 1 or 3
  NO  -> Path 2, 4, or 5

Step 5: Time pressure?
  URGENT (regulatory, capital) -> Path 4 (note sale, fastest exit)
  MODERATE -> Path 2 or 5
  LOW -> Path 1 or 3 (buy time)

Step 6: Market conditions?
  IMPROVING -> Paths 1-3 (benefit from recovery)
  STABLE -> Path 2 or 4
  DECLINING -> Path 4 or 5 (exit before further losses)
```

---

## 8. Borrower Bankruptcy Implications

```yaml
bankruptcy_impact:
  chapter_11:
    automatic_stay: "Halts all collection, foreclosure, enforcement"
    duration: "30 days (single-asset) to unlimited (operating company)"
    adequate_protection:
      description: "Lender entitled to protection against value decline"
      forms:
        - "Cash payments equal to lost collateral value"
        - "Additional collateral"
        - "Equity cushion"
    cram_down:
      description: "Court can approve plan over lender's objection"
      requirements:
        - "Plan is fair and equitable"
        - "Lender receives at least liquidation value"
        - "Plan is feasible"
      lender_risk: "May be forced to accept modified terms"
    single_asset_exception:
      description: "Faster timeline for single-asset real estate debtors"
      requirement: "Must file plan within 90 days or begin payments = rent"
      relief_from_stay: "Available if no plan filed or payments not made"

  chapter_7:
    effect: "Liquidation of assets"
    lender_impact: "Foreclosure proceeds distributed per priority"
    timeline: "4-6 months for asset distribution"
    advantage: "Faster than Chapter 11 plan confirmation"

  preference_actions:
    description: "Trustee can claw back payments made 90 days pre-filing"
    risk_to_lender: "Regular debt service payments generally safe (ordinary course)"
    risk_items:
      - "Unusual lump-sum payments"
      - "Payments on insider guarantees within 1 year"
      - "Collateral transfers within 90 days"

  pre_bankruptcy_planning:
    lender_actions:
      - "Negotiate workout BEFORE filing (more control, better terms)"
      - "Secure additional collateral or guarantees"
      - "Perfect all liens and security interests"
      - "Verify UCC filings are current"
      - "Document all defaults and communications"
    borrower_signals:
      - "Retention of bankruptcy counsel"
      - "Cessation of communication"
      - "Diversion of rents"
      - "Transfer of assets to affiliates"
      - "Unusual lump-sum payments to insiders"
```

---

## 9. Workout Team and Process

```yaml
workout_team:
  internal:
    - "Special assets / workout officer (lead)"
    - "Loan officer (relationship context)"
    - "Credit risk analyst (financial modeling)"
    - "Legal counsel (documentation, enforcement)"
    - "Senior management (approval authority)"
  external:
    - "Outside counsel (foreclosure, bankruptcy, litigation)"
    - "Appraiser (updated valuation)"
    - "Environmental consultant (if needed)"
    - "Property manager / receiver (if needed)"
    - "Loan sale advisor (if note sale path)"
    - "Forensic accountant (if fraud suspected)"

workout_process:
  phase_1_assessment: # Weeks 1-2
    - "Compile complete loan and property file"
    - "Order updated appraisal or broker opinion of value"
    - "Analyze borrower financial statements"
    - "Calculate current LTV, DSCR, and debt yield"
    - "Assess borrower cooperation level"
    - "Identify all guarantors and their net worth"

  phase_2_strategy: # Weeks 2-4
    - "Model all 5 pathways with NPV"
    - "Rank pathways by risk-adjusted recovery"
    - "Prepare workout recommendation memo"
    - "Obtain internal approval for strategy"
    - "Engage outside counsel"

  phase_3_execution: # Weeks 4-16+
    - "Issue default notice (if not already)"
    - "Initiate borrower discussions (if cooperative path)"
    - "File foreclosure (if enforcement path)"
    - "Market note (if sale path)"
    - "Document all communications"
    - "Monitor property condition"

  phase_4_resolution: # Varies
    - "Execute chosen pathway"
    - "Close transaction / complete foreclosure"
    - "Recognize final loss (if any)"
    - "Update regulatory reporting"
    - "Post-mortem and lessons learned"
```
