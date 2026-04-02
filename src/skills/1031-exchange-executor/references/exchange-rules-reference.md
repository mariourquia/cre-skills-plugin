# 1031 Exchange Rules Reference

## Overview

Complete reference for IRC Section 1031 like-kind exchange mechanics, including
standard forward exchange, reverse exchange, improvement exchange, Delaware
Statutory Trust (DST) fallback, and Qualified Intermediary (QI) requirements.

---

## 1. Core 1031 Mechanics

### Statutory Requirements

```yaml
requirements:
  like_kind:
    definition: "Real property for real property held for investment or business use"
    qualifies:
      - "Office building for apartment complex"
      - "Raw land for retail center"
      - "Industrial warehouse for medical office"
      - "Domestic real estate for domestic real estate"
      - "Fee simple for leasehold (30+ years remaining)"
      - "TIC interest for whole property"
    does_not_qualify:
      - "US real estate for foreign real estate (post-TCJA 2017)"
      - "Real property for personal property (post-TCJA 2017)"
      - "Primary residence (Section 121 applies instead)"
      - "Inventory or dealer property"
      - "Partnership interests"

  held_for_requirement:
    description: "Property must be held for productive use in trade/business or investment"
    safe_harbor: "Hold for 24+ months (no statutory requirement, but IRS guidance)"
    risk_factors:
      - "Property flipped within 12 months of acquisition"
      - "Property listed for sale before exchange closes"
      - "Intent to sell at acquisition (dealer characterization)"

  boot:
    description: "Non-like-kind property received in exchange, taxable"
    types:
      cash_boot: "Cash received from exchange (including excess proceeds)"
      mortgage_boot: "Net debt relief (relinquished debt > replacement debt)"
      personal_property_boot: "Fixtures, equipment, inventory conveyed"
    calculation: |
      Taxable boot = max(0, boot_received - boot_given)
      Gain recognized = min(boot_received, total_realized_gain)
```

### Financial Requirements for Full Deferral

```
To defer 100% of gain, the exchanger must:

1. REINVEST ALL CASH
   Replacement value >= relinquished net sale proceeds
   Any cash not reinvested = taxable cash boot

2. REPLACE ALL DEBT (or add cash)
   Replacement debt >= relinquished debt
   OR increase cash equity to offset debt reduction
   Net debt relief = taxable mortgage boot

3. ACQUIRE EQUAL OR GREATER VALUE
   Replacement property value >= relinquished property value

Formula:
  Required replacement value >= Sale Price - Selling Costs
  Required replacement debt >= Relinquished mortgage payoff
  OR Required additional cash = Debt reduction amount
```

### Worked Example: Full Deferral

```yaml
relinquished_property:
  sale_price: 4500000
  adjusted_basis: 1800000
  mortgage_payoff: 2700000
  selling_costs: 225000  # 5% broker + legal + transfer
  net_proceeds_to_qi: 1575000  # 4.5M - 2.7M - 225K
  realized_gain: 2475000  # 4.5M - 1.8M - 225K

full_deferral_requirements:
  min_replacement_value: 4275000  # 4.5M - 225K
  min_replacement_debt: 2700000  # Or add cash to offset
  must_reinvest_all: 1575000  # Cash from QI

replacement_property:
  purchase_price: 5200000  # Exceeds minimum (good)
  new_mortgage: 3200000  # Exceeds relinquished (good)
  cash_from_qi: 1575000  # All cash reinvested (good)
  additional_cash: 425000  # Buyer adds equity to close gap
  boot: 0  # Full deferral achieved

new_basis:
  calculation: "Replacement value - deferred gain"
  new_basis: 2725000  # 5,200,000 - 2,475,000
  # Depreciation restarts at new basis for replacement property
```

---

## 2. Timeline Rules

### Critical Deadlines

```
Day 0:   Relinquished property closes (sale recorded)
         Clock starts on both periods

Day 45:  IDENTIFICATION DEADLINE
         Must identify replacement property(ies) in writing
         Signed by exchanger
         Delivered to QI (or other exchange party)
         CANNOT be extended (no exceptions, not even court order)
         Weekends and holidays count
         Exception: federally declared disaster zone

Day 180: EXCHANGE DEADLINE
         Must close on replacement property
         CANNOT be extended
         Note: if tax return due date falls before Day 180,
         must file extension to preserve full 180 days
         If filing April 15, Day 180 after October: file extension

Both deadlines are absolute and cannot be extended by:
  - Agreement of parties
  - Court order
  - QI delay
  - Title issues
  - Lender delays
```

### Identification Rules

```yaml
identification_rules:
  three_property_rule:
    description: "Identify up to 3 properties regardless of value"
    limit: 3
    most_common: true
    example: "Identify Property A ($3M), Property B ($2.5M), Property C ($4M)"

  200_percent_rule:
    description: "Identify any number of properties if total FMV <= 200% of relinquished"
    formula: "Sum of identified values <= 2 * relinquished sale price"
    example: "Relinquished sold for $4.5M; can identify up to $9M total"

  95_percent_rule:
    description: "Identify any number if exchanger acquires 95%+ of identified value"
    risk: "Must close on substantially all identified properties"
    rarely_used: true
    use_case: "Portfolio exchanges where buyer expects to close all"

  identification_format:
    required_elements:
      - "Street address"
      - "Legal description OR other unambiguous description"
      - "Signed by exchanger"
      - "Delivered to QI or other non-disqualified party"
    delivery_methods:
      - "Hand delivery with acknowledgment"
      - "Certified mail (postmarked by Day 45)"
      - "Email to QI (confirm receipt)"
      - "Fax (retain confirmation)"
    best_practice: "Identify 3 properties under 3-property rule, ranked by preference"
```

---

## 3. Reverse Exchange (Revenue Procedure 2000-37)

### When Used

Exchanger needs to acquire replacement property BEFORE selling relinquished
property. Common when: replacement is available now, relinquished needs time
to sell, or competitive market for replacement.

### Structure

```
Standard Exchange: Sell first, buy second
Reverse Exchange:  Buy first, sell second (using EAT)

Exchange Accommodation Titleholder (EAT):
  - Takes title to either replacement or relinquished property
  - Holds for up to 180 days
  - Not the same as QI (different entity)
  - Must be genuine titleholder (economic risk)
```

### Reverse Exchange Timeline

```
Day 0:   EAT acquires parked property (replacement or relinquished)
Day 45:  Exchanger identifies the property to be exchanged
Day 180: Exchange must be completed
         - If EAT holds replacement: relinquished must be sold
         - If EAT holds relinquished: must transfer to buyer

Parking arrangements:
  Option 1: EAT holds REPLACEMENT property
    - EAT acquires replacement with exchanger's funds or loan
    - Exchanger sells relinquished through QI
    - QI directs proceeds to EAT
    - EAT transfers replacement to exchanger

  Option 2: EAT holds RELINQUISHED property
    - EAT takes title to relinquished from exchanger
    - Exchanger acquires replacement directly
    - EAT sells relinquished to third party
    - Proceeds flow to complete exchange
```

### Cost

```yaml
reverse_exchange_costs:
  eat_fee: "1.0-2.0% of parked property value"
  legal: "$15,000-$35,000"
  title_insurance: "Standard rates (additional policy for EAT)"
  loan_costs: "If EAT borrows, origination + interest during holding"
  qi_fee: "$1,500-$5,000"
  total_typical: "$50,000-$150,000+ depending on value"
  premium_over_forward: "3-5x cost of standard forward exchange"
```

---

## 4. Improvement Exchange (Build-to-Suit)

### Structure

Exchanger identifies land or improved property and uses exchange funds to
construct improvements before taking title.

```
Timeline:
  Day 0:    Sell relinquished property
  Day 1-45: Identify replacement property (land or improved)
  Day 1-180: EAT acquires replacement, uses exchange funds for improvements
  Day 180:  EAT transfers improved property to exchanger

Key rule: improvements must be in place and owned by EAT at transfer.
The exchanger's basis includes the value of improvements.
```

### Requirements

```yaml
improvement_exchange:
  eat_required: true  # EAT must hold title during construction
  construction_must_be_on_eat_property: true
  exchanger_cannot_hold_title_during_construction: true
  all_improvements_must_be_real_property: true
  timeline: "180 days from relinquished sale to replacement acquisition"

  practical_challenges:
    - "180 days is very tight for construction"
    - "Must identify specific improvements by Day 45"
    - "Unused exchange funds at Day 180 = taxable boot"
    - "EAT must manage construction (or contract exchanger as contractor)"
    - "Cost overruns: if improvements cost more than exchange funds, exchanger adds cash"
    - "If construction not complete by Day 180: only completed improvements count"
```

---

## 5. Delaware Statutory Trust (DST) Fallback

### When Used

DST is a passive 1031-eligible investment used when the exchanger cannot
find suitable replacement property before the 45-day deadline. Also used for
estate planning and portfolio diversification.

```yaml
dst_overview:
  legal_structure: "Statutory trust under Delaware law"
  tax_treatment: "Each beneficial interest is real property (Rev Ruling 2004-86)"
  1031_eligible: true
  investment_type: "Passive fractional ownership of institutional CRE"
  typical_properties: "NNN retail, multifamily, industrial, medical office"
  minimum_investment: "$100,000-$250,000"
  hold_period: "5-10 years (illiquid, no early redemption)"

  advantages:
    - "1031-eligible with no management responsibility"
    - "Diversification across property types and geographies"
    - "Institutional-quality assets (single-tenant NNN, Class A MF)"
    - "Professional management"
    - "Estate planning: stepped-up basis at death"
    - "Backup identification: always available before Day 45"

  disadvantages:
    - "No control over property management or disposition"
    - "Illiquid (no secondary market)"
    - "Fees: 10-15% of invested capital (sponsor fees, commissions)"
    - "Cannot refinance, add tenants, or make material changes"
    - "7 Deadly Sins: DST cannot renegotiate leases, borrow, etc."
    - "Returns: typically 4-6% cash-on-cash (lower than direct)"

  seven_deadly_sins:
    description: "IRS restrictions on DST activities (maintain tax treatment)"
    prohibited:
      1: "No new capital contributions (no capital calls)"
      2: "No renegotiation of existing loans"
      3: "No new loans"
      4: "No reinvestment of sale proceeds"
      5: "No renegotiation of leases"
      6: "No new leases"
      7: "No capital expenditures beyond normal maintenance"
```

### DST as Backup Identification Strategy

```
Day 1-40:  Actively pursue direct replacement property
Day 41-44: If direct property not secured:
           - Identify 2 direct properties + 1 DST (under 3-property rule)
           - OR identify 1 direct property + 2 DSTs
Day 45:    Identification deadline met with DST as safety net
Day 46-180: Continue pursuing direct property
            If direct closes: acquire direct, DST identification unused
            If direct falls through: acquire DST, exchange preserved
```

---

## 6. Qualified Intermediary (QI) Requirements

### Role

QI holds exchange proceeds between sale of relinquished and purchase of
replacement property. Exchanger cannot touch funds or exchange fails.

```yaml
qi_requirements:
  cannot_be:
    - "Exchanger or disqualified person"
    - "Agent of exchanger (attorney, CPA, broker who acted in past 2 years)"
    - "Employee of exchanger"
    - "Related party (family, >10% owned entity)"

  must_do:
    - "Hold exchange proceeds in segregated account"
    - "Enter written exchange agreement before closing"
    - "Receive proceeds directly from closing"
    - "Disburse funds only for replacement property acquisition"
    - "Maintain records of all transactions"

  fund_security:
    description: "QI insolvency is the #1 risk in 1031 exchanges"
    protections:
      - "Segregated accounts (not commingled with QI operating funds)"
      - "Qualified escrow or trust (funds held by third-party bank)"
      - "Fidelity bond / errors & omissions insurance ($5M+ coverage)"
      - "State licensing (if required: NV, WA, OR, CT, CO, ID, ME, VA)"
      - "FDIC insurance on cash deposits (up to $250K per account)"
    best_practices:
      - "Use QI affiliated with major title company or financial institution"
      - "Require segregated, FDIC-insured accounts"
      - "Verify fidelity bond coverage"
      - "Check QI membership in FEA (Federation of Exchange Accommodators)"
      - "Never use exchanger's attorney or CPA as QI"

  fees:
    basic_forward_exchange: "$750-$2,500"
    reverse_exchange: "$5,000-$15,000"
    improvement_exchange: "$5,000-$15,000"
    additional_per_property: "$250-$500"
    wire_fees: "$25-$50 per wire"
    interest_earned: "Typically split or retained by QI (negotiate)"
```

### Constructive Receipt Traps

```yaml
constructive_receipt:
  description: "If exchanger has actual or constructive receipt of funds, exchange fails"
  common_traps:
    - "Exchange agreement allows exchanger to demand funds before Day 180"
    - "Exchanger receives interest directly from QI account"
    - "QI deposits funds in exchanger's account"
    - "Exchange agreement lacks required 'safe harbors'"
    - "Exchanger directs QI to pay personal obligations from proceeds"

  safe_harbors:
    g4_restrictions: |
      Exchange agreement must limit exchanger's right to receive funds.
      Funds released only:
      (a) After Day 180
      (b) Upon acquisition of replacement property
      (c) Upon material breach by QI
    qualified_escrow: "Funds held by third-party escrow agent"
    qualified_trust: "Funds held by trustee"
```

---

## 7. Special Situations

### Partial Exchange

```
If replacement value < relinquished value:
  Boot = Relinquished value - Replacement value - Costs
  Gain recognized = min(Boot, Total realized gain)
  Remaining gain deferred

Example:
  Relinquished: $4.5M sale, $2.475M gain
  Replacement: $3.5M purchase
  Boot: $4.5M - $3.5M - $225K costs = $775K
  Gain recognized: $775K (less than total gain)
  Gain deferred: $2.475M - $775K = $1.7M
```

### Multiple Replacement Properties

```
Can acquire 2+ replacement properties:
  - Must be identified under 3-property or 200% rule
  - Combined value should meet or exceed relinquished
  - Common for portfolio diversification

Example:
  Sell: 1 property at $5M
  Buy: Property A ($2.5M) + Property B ($1.5M) + Property C ($1.5M)
  Total replacement: $5.5M > $5M (full deferral if debt also replaced)
```

### Related Party Exchanges

```yaml
related_party:
  definition: "IRC 267(b) -- family members, >50% owned entities"
  restriction: "If related party sells within 2 years, gain is recognized"
  exception: "Disposition due to death, involuntary conversion, or non-tax-motivated"
  planning: "Exchange with related party is permissible if both hold for 2+ years"
```

### Death of Exchanger During Exchange

```
If exchanger dies during 45/180 day period:
  - Exchange can be completed by estate/executor
  - Heirs receive stepped-up basis (Section 1014)
  - If exchange completes: stepped-up basis on replacement property
  - If exchange fails: stepped-up basis on relinquished (if not yet sold)
    or on cash proceeds (if sold)

Planning note: stepped-up basis at death eliminates ALL deferred gain.
For elderly exchangers, consider whether 1031 is even necessary.
```
