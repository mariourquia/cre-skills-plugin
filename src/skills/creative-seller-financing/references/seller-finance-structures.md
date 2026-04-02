# Seller Financing Structures Reference

## Overview

Comprehensive reference for seller financing in CRE transactions. Covers IRC 453
installment sale mechanics, vendor take-back (VTB) structures, seller carry
subordinate to senior debt, and assumption vs new financing strategies.

---

## 1. IRC 453 Installment Sale

### Mechanics

Under IRC Section 453, a seller who receives at least one payment after the tax
year of sale can report gain proportionally as payments are received, rather
than recognizing the full gain at closing.

```
Installment Sale Ratio = Gross Profit / Contract Price

Where:
  Gross Profit = Selling Price - Adjusted Basis - Selling Expenses
  Contract Price = Selling Price - Assumed Mortgage (if applicable)
                   + Excess Mortgage (if mortgage > basis)

Each payment is split:
  Taxable Gain = Payment * Installment Sale Ratio
  Return of Capital = Payment * (1 - Installment Sale Ratio)
  Interest Income = Interest portion (taxed as ordinary income)
```

### Worked Example

```yaml
property:
  selling_price: 5000000
  adjusted_basis: 2200000  # Original cost - depreciation
  selling_expenses: 150000  # Broker, legal, transfer tax
  existing_mortgage: 0  # Free and clear

installment_terms:
  down_payment: 1000000  # 20%
  seller_note: 4000000   # 80%
  interest_rate: 0.065   # 6.5% (must be >= AFR)
  amortization: 25_years
  balloon: 7_years
  monthly_payment: 27022  # P&I

tax_calculation:
  gross_profit: 2650000   # 5M - 2.2M - 150K
  contract_price: 5000000 # No mortgage assumption
  installment_ratio: 0.53 # 2.65M / 5M

  year_1:
    down_payment_received: 1000000
    principal_payments: 94264  # 12 months of amortization
    total_payments: 1094264
    taxable_gain: 579960  # 1,094,264 * 0.53
    return_of_capital: 514304
    interest_income: 230000  # Approximate Year 1 interest
    tax_at_20_cap_gains: 115992  # On gain portion
    tax_at_37_ordinary: 85100   # On interest portion
    total_tax: 201092

  lump_sum_alternative:
    full_gain: 2650000
    tax_at_20_cap_gains: 530000
    niit_3_8: 100700  # Net Investment Income Tax
    state_tax_estimate: 200000  # Varies by state
    total_tax_year_1: 830700

  tax_deferral_benefit: 629608  # $830,700 - $201,092 in Year 1
```

### Key Rules and Limitations

```yaml
rules:
  minimum_interest:
    description: "Seller note must charge at least the Applicable Federal Rate (AFR)"
    consequence: "If below AFR, IRS imputes interest, reducing principal payments"
    current_afr:  # Check IRS Rev Ruling monthly
      short_term: "Under 3 years"
      mid_term: "3-9 years"
      long_term: "Over 9 years"

  related_party:
    description: "IRC 453(e) -- resale by related buyer within 2 years triggers acceleration"
    related_parties: "Spouse, children, parents, entities >50% owned"
    consequence: "Remaining gain recognized in year of resale"

  depreciation_recapture:
    description: "IRC 1250 gain recognized in year of sale regardless of installment method"
    rate: 0.25  # 25% on unrecaptured Section 1250 gain
    exception: "Only applies to depreciation taken, not the installment portion"

  dealer_exclusion:
    description: "Dealers in real property cannot use installment method"
    test: "Property held primarily for sale to customers in ordinary course"
    exemption: "Property held for investment or used in trade/business"

  election_out:
    description: "Taxpayer can elect out of installment method on Form 4797"
    when_beneficial: "If expecting higher tax rates in future years"
    irrevocable: true

  pledging_rule:
    description: "IRC 453A -- pledging installment note as collateral = payment received"
    threshold: "Applies when aggregate installment obligations > $5M"
    consequence: "Deemed payment triggers gain recognition"
```

---

## 2. Vendor Take-Back (VTB) Structures

### Standard VTB

Seller provides financing as first-position mortgage. Most common when
institutional financing is difficult or when seller wants ongoing income.

```yaml
standard_vtb:
  typical_terms:
    ltv: "70-85%"
    rate: "AFR + 200-400 bps (typically 6-9%)"
    amortization: "20-30 years"
    term: "5-10 years with balloon"
    prepayment: "Lockout 1-2 years, then yield maintenance or declining penalty"
    recourse: "Full recourse to buyer (common in seller financing)"

  when_used:
    - "Property has condition issues making bank financing difficult"
    - "Buyer has insufficient equity or track record"
    - "Seller wants tax deferral via installment sale"
    - "Market conditions (high rates) make conventional financing prohibitive"
    - "Transitional asset (lease-up, renovation) not yet stabilized"

  seller_protections:
    - "First lien position on property"
    - "Personal/corporate guarantee from buyer"
    - "Assignment of rents and leases"
    - "Property insurance naming seller as mortgagee"
    - "Financial reporting covenants"
    - "Due-on-sale clause"
    - "Cross-default with other buyer obligations"
```

### Mezzanine VTB

Seller provides subordinate financing behind senior bank debt.

```yaml
mezzanine_vtb:
  capital_stack:
    senior_debt:
      provider: "Bank or CMBS"
      ltv: "55-65%"
      rate: "5.5-7.0%"
    seller_mezzanine:
      position: "Second lien or mezzanine"
      ltv_band: "65-80%"
      rate: "8-12%"
      payment: "Interest-only or partial amortization"
    buyer_equity:
      position: "First loss"
      ltv_band: "80-100%"
      amount: "20%+"

  intercreditor_issues:
    standstill: "Senior lender requires mezz to standstill for 90-180 days"
    cure_rights: "Seller/mezz gets right to cure senior default"
    buyout_right: "Seller can purchase senior note at par upon default"
    subordination: "Seller lien subordinate to senior in all respects"
    approval: "Senior lender must approve mezz financing (critical)"

  typical_terms:
    rate: "9-12% (premium over senior)"
    term: "Coterminous with senior or 1 year shorter"
    amortization: "Interest-only during term, balloon at maturity"
    prepayment: "Negotiated, often more flexible than institutional mezz"
    conversion: "Some structures include equity conversion option"
```

---

## 3. Seller Carry with Senior Debt

### Structure

Buyer obtains conventional senior debt AND seller provides subordinate
financing. Most complex structure; requires senior lender approval.

```
Capital Stack:
  [65% LTV]  Senior Mortgage  ---  Bank/Life Co/CMBS
  [15% LTV]  Seller Carry     ---  Subordinate note
  [20% LTV]  Buyer Equity     ---  Cash/1031 exchange

Total leverage: 80%
Buyer effective down payment: 20% (instead of 35% without seller carry)
```

### Senior Lender Considerations

```yaml
lender_requirements:
  disclosure: "Must disclose seller carry to senior lender (concealment = fraud)"
  maximum_combined_ltv: "75-80% (some lenders allow up to 85%)"
  dscr_test: "Combined debt service must clear 1.20x minimum"
  subordination_agreement:
    - "Seller note is fully subordinate to senior"
    - "No payments on seller note during senior default"
    - "No enforcement action without senior lender consent"
    - "Standstill period (90-180 days) before seller can foreclose"
  lender_types:
    banks: "Sometimes allow with subordination agreement"
    life_companies: "Rarely allow; clean capital stack preferred"
    cmbs: "Generally prohibited in pooling & servicing agreement"
    agency_mf: "Prohibited by Fannie/Freddie guidelines"
    debt_funds: "Most flexible; often allow seller carry"
```

### Payment Waterfall

```
Monthly cash flow priority:
  1. Operating expenses and reserves
  2. Senior debt service
  3. Seller carry debt service
  4. Equity distributions

Cash trap scenario (if DSCR < 1.25x on senior):
  1. Operating expenses
  2. Senior debt service
  3. Cash trapped in reserve (no seller carry payment)
  4. No equity distributions
```

### Seller Carry Term Sheet Template

```yaml
term_sheet:
  property: "[address]"
  purchase_price: 5000000
  senior_debt: 3250000  # 65% LTV
  seller_carry:
    amount: 750000  # 15% LTV
    interest_rate: 0.085  # 8.5% fixed
    payment_type: "Interest-only"
    monthly_payment: 5312  # $750K * 8.5% / 12
    term_months: 60  # 5 years
    maturity: "Balloon at maturity"
    prepayment: "No penalty after Year 2"
    collateral: "Second deed of trust on property"
    guarantee: "Personal guarantee of buyer principal(s)"
    subordination: "Fully subordinate to senior mortgage per intercreditor agreement"
    default_remedies:
      - "90-day standstill behind senior"
      - "Cure right on senior default (within 30 days)"
      - "Foreclosure only with senior lender consent"
    covenants:
      - "DSCR on combined debt > 1.15x"
      - "Annual property financial statements within 90 days"
      - "No additional debt without seller consent"
      - "Maintain property insurance with seller as additional insured"
```

---

## 4. Assumption vs New Financing

### Loan Assumption Analysis

When the seller has an existing loan with favorable terms, buyer may assume
rather than originate new financing.

```yaml
assumption_economics:
  when_assumption_wins:
    - "Existing rate significantly below current market"
    - "Prepayment penalty is prohibitive (yield maintenance, defeasance)"
    - "Loan has favorable terms (IO period remaining, flexible covenants)"
    - "CMBS loan where defeasance cost exceeds assumption cost"

  assumption_costs:
    assumption_fee: "0.5-1.0% of loan balance"
    legal_fees: "Buyer and seller counsel, $15K-$50K"
    lender_legal: "Buyer typically pays lender's counsel, $10K-$30K"
    appraisal: "$5K-$15K"
    engineering_report: "$5K-$10K"
    environmental: "$3K-$8K"
    total_typical: "$50K-$150K"

  timeline:
    cmbs: "45-90 days (servicer approval required)"
    life_company: "30-60 days"
    bank: "30-45 days"
    agency_mf: "30-60 days (Fannie/Freddie standard process)"
```

### Assumption vs New Financing NPV Comparison

```
Existing loan: $3M balance, 4.5% rate, 22 years remaining, CMBS
Current market rate: 6.5%
Defeasance cost estimate: $350,000

Option A: Assume existing loan
  Monthly payment: $18,754 (on existing schedule)
  Assumption costs: $80,000
  Annual debt service: $225,048
  Remaining term value of below-market rate:
    Market payment at 6.5%: $22,481/month
    Savings: $3,727/month = $44,724/year
    PV of savings over 22 years: ~$520,000

Option B: Defease and originate new loan
  Defeasance cost: $350,000
  New loan origination: $3M at 6.5%, 30-year am
  Origination costs: $45,000 (1.5%)
  Monthly payment: $18,960
  Total upfront cost: $395,000

Option C: New loan (larger) with seller carry gap
  New loan: $3.5M at 6.5%, 30-year am
  Origination: $52,500
  Monthly payment: $22,120
  Additional proceeds: $500K (higher leverage)

Comparison:
  Option A NPV advantage: $520K - $80K = $440K
  Option A is superior if: rate savings PV > assumption costs
  Breakeven: assumption wins whenever existing rate is >100bps below market
```

### Decision Framework

```
START: Is existing loan assumable?
  |
  +-- NO: New financing required. Skip to origination.
  |
  +-- YES: Calculate rate differential
        |
        +-- Existing rate within 50bps of market: New loan (more flexibility)
        |
        +-- Existing rate 50-150bps below market:
        |     Calculate assumption costs vs rate savings NPV
        |     If NPV positive: assume
        |     Consider: remaining IO, covenant flexibility
        |
        +-- Existing rate >150bps below market: Almost always assume
              Exception: if loan balance is too small for acquisition
              Solution: assume + seller carry for gap financing
```

---

## 5. Seller Financing Pricing

### Rate Setting Framework

```
Seller financing rate should reflect:

  Rate = Risk-Free Rate (UST) + Credit Spread + Illiquidity Premium + Admin Premium

Components:
  UST (matched maturity):  ~4.0-5.0% (varies)
  Credit spread:           1.5-3.0% (based on LTV and buyer credit)
  Illiquidity premium:     0.5-1.5% (seller note is illiquid)
  Admin/servicing:         0.25-0.50%

Typical range: 6.5-10.0%

Below AFR: prohibited (IRS imputes interest)
Above market: buyer should seek conventional financing
Sweet spot: 100-200bps above conventional bank rate
  Justifies seller's risk while giving buyer access to capital
```

### Rate Comparison by Structure

| Structure                    | Typical Rate | LTV    | Amortization |
|------------------------------|-------------|--------|--------------|
| Seller first mortgage (VTB)  | 6.5-8.5%   | 70-85% | 20-30 yr     |
| Seller second (behind bank)  | 8.0-12.0%  | 65-80% | IO or 25 yr  |
| Seller mezzanine             | 9.0-14.0%  | 70-85% | IO           |
| Land contract / contract for deed | 6.0-8.0% | 75-90% | 25-30 yr  |
| Master lease with purchase option | Implicit in rent | N/A | N/A    |

---

## 6. Alternative Structures

### Contract for Deed (Land Contract)

```yaml
land_contract:
  description: |
    Seller retains legal title until contract is paid in full or
    specified milestone met. Buyer gets equitable title and possession.
  advantages_seller:
    - "Retains title (easier to recover on default vs foreclosure)"
    - "Installment sale treatment for tax purposes"
    - "No transfer tax until title transfers"
  advantages_buyer:
    - "Lower closing costs (no mortgage origination)"
    - "Faster closing (no lender approval)"
    - "Lower qualification bar"
  risks:
    - "Buyer: seller bankruptcy could cloud title"
    - "Buyer: no title insurance until deed transfers"
    - "Seller: some states treat as mortgage (full foreclosure required)"
    - "Both: title recording issues"
  states_favorable: ["TX", "MI", "MN", "IN", "OH"]
  states_unfavorable: ["CA", "NY", "FL"]  # Treat as mortgage
```

### Master Lease with Purchase Option

```yaml
master_lease:
  description: |
    Buyer leases entire property with option to purchase at predetermined
    price. Rent credits may apply toward purchase price.
  structure:
    lease_term: "3-5 years"
    rent: "Approximates debt service on purchase price"
    purchase_option: "Fixed price or formula (cap rate on trailing NOI)"
    rent_credit: "25-50% of rent applied to purchase price"
    option_fee: "1-3% of purchase price (non-refundable, applied to price)"
  when_used:
    - "Buyer needs time to secure financing"
    - "Property is transitional (needs lease-up or renovation)"
    - "Buyer wants to prove concept before committing"
    - "Zoning or entitlement contingencies"
    - "Seller wants above-market income during option period"
  tax_treatment:
    seller: "Rental income during lease; gain recognized at exercise"
    buyer: "Rent is deductible expense; rent credits are purchase price adjustment"
    risk: "If option terms too favorable, IRS may recharacterize as installment sale"
```

### Wraparound Mortgage

```yaml
wraparound:
  description: |
    Seller creates new note that wraps around existing mortgage. Buyer
    makes payments to seller; seller continues paying underlying loan.
  structure:
    existing_mortgage: 2000000  # at 4.5%
    wrap_note: 3500000  # at 7.0%
    buyer_payment: 23287  # Monthly on $3.5M at 7%
    seller_pays_underlying: 10132  # Monthly on $2M at 4.5%
    seller_spread: 13155  # Monthly profit
    seller_effective_yield: "~10.5% on $1.5M at risk"
  risks:
    - "Due-on-sale clause in underlying mortgage (most have it)"
    - "If buyer defaults, seller must continue underlying payments"
    - "If seller diverts buyer payments, underlying defaults"
    - "Title issues: buyer has equitable title, seller has legal title"
  mitigation:
    - "Escrow arrangement: third-party collects and distributes"
    - "Title insurance with wrap endorsement"
    - "Due-on-sale risk: only viable if lender unlikely to enforce"
```
