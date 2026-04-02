# Loan Sizing Formula Reference

NCF normalization, simultaneous DSCR/LTV/DY sizing, binding constraint identification, rate sensitivity, and execution comparison. All examples use a baseline 150-unit multifamily property.

---

## 1. Net Cash Flow (NCF) Normalization for Lender Underwriting

### Lender NCF vs. Borrower NOI

Lenders use Net Cash Flow (NCF), not NOI, as the starting point for sizing. NCF deducts capital reserves and tenant improvement / leasing commission reserves from NOI.

```
NCF = NOI - Capital reserves - TI/LC reserves (commercial)

For multifamily:
  NCF = NOI - Replacement reserves

For office/retail:
  NCF = NOI - Capital reserves - TI reserves - LC reserves
```

### Worked Example: 150-Unit Multifamily

```
Gross potential rent: 150 units * $1,950/mo * 12 = $3,510,000
Other income (parking, laundry, fees): $165,000
Gross potential income: $3,675,000
Vacancy & credit loss (5%): ($183,750)
Effective gross income: $3,491,250

Operating expenses:
  Real estate taxes:       ($420,000)
  Insurance:               ($105,000)
  Management fee (3.5%):   ($122,194)
  Payroll:                 ($210,000)
  Repairs & maintenance:   ($195,000)
  Utilities:               ($156,000)
  Contract services:       ($78,000)
  Admin/marketing:         ($52,500)
Total operating expenses:  ($1,338,694)

NOI: $2,152,556

Replacement reserves: ($300/unit * 150) = ($45,000)

NCF: $2,152,556 - $45,000 = $2,107,556
```

### Lender Haircuts

Lenders typically apply their own underwriting adjustments on top of the borrower's NCF:

```
Common lender adjustments:
  - Vacancy: Lender may use 7-10% even if market is 5%
  - Rent growth: 0% in Year 1 (no credit for growth)
  - Expense inflation: 3% applied to all expenses
  - Management fee: Minimum 4-5% even if actual is lower
  - Reserves: $250-$400/unit minimum (agency), $300-$500 (bank)

Lender-underwritten NCF is typically 5-15% below borrower's NCF.
```

---

## 2. Simultaneous Constraint Sizing

### The Three Constraints

Every CRE loan is sized as the minimum of three calculations:

```
Loan_max = min(Loan_LTV, Loan_DSCR, Loan_DY)

Where:
  Loan_LTV  = Property_value * Max_LTV
  Loan_DSCR = NCF / (Min_DSCR * Debt_service_constant)
  Loan_DY   = NCF / Min_debt_yield
```

### Debt Service Constant

```
DSC = Annual debt service per dollar of loan principal

For amortizing loans:
  DSC = [r * (1+r)^n / ((1+r)^n - 1)] * 12

Where r = monthly rate, n = amortization months

For interest-only loans:
  DSC = annual_rate
```

### Worked Example: Simultaneous Sizing

```
Property: 150 units, $22,500,000 purchase price
NCF: $2,107,556
Lender terms: 6.50% rate, 30-year amortization, 2 years IO

Sizing parameters:
  Max LTV: 65%
  Min DSCR: 1.25x (on amortizing basis, even during IO period)
  Min Debt Yield: 8.0%

Step 1: Debt service constant
  r = 0.065 / 12 = 0.005417
  n = 360
  (1 + r)^n = (1.005417)^360 = 6.9917
  DSC = [0.005417 * 6.9917 / (6.9917 - 1)] * 12
      = [0.03788 / 5.9917] * 12
      = 0.006322 * 12 = 0.07587

Step 2: Size by each constraint

  LTV:  $22,500,000 * 0.65 = $14,625,000

  DSCR: $2,107,556 / (1.25 * 0.07587)
      = $2,107,556 / 0.09484
      = $22,222,000   [This exceeds property value -- not binding]

  DY:   $2,107,556 / 0.08
      = $26,344,450   [Also exceeds property value -- not binding]

Step 3: Binding constraint
  Loan = min($14,625,000, $22,222,000, $26,344,450) = $14,625,000

  BINDING CONSTRAINT: LTV (65%)

Step 4: Verify other metrics at sized loan
  Annual DS (amortizing): $14,625,000 * 0.07587 = $1,109,355
  DSCR: $2,107,556 / $1,109,355 = 1.90x  (passes 1.25x)
  DY: $2,107,556 / $14,625,000 = 14.41%  (passes 8.0%)

  All three constraints satisfied. LTV is the limiting factor.
```

### When Each Constraint Typically Binds

```
Environment            | Typical Binding | Why
-----------------------|-----------------|-----
Low rates (<5%)        | LTV             | Low DS constant means DSCR easily passes
Mid rates (5-7%)       | LTV or DSCR     | Depends on cap rate vs rate spread
High rates (>7%)       | DSCR            | High DS constant squeezes coverage
Low cap rate (<5%)     | LTV             | High value relative to income
High cap rate (>7%)    | DSCR or DY      | Low value but potentially thin coverage
```

---

## 3. Rate Sensitivity Analysis

### Impact of Rate Changes on Sizing

```
Base case: 6.50% rate, NCF = $2,107,556, Value = $22,500,000

Rate   | DSC      | Loan(LTV) | Loan(DSCR)  | Loan(DY)   | Sized Loan | Binding
-------|----------|-----------|-------------|------------|------------|--------
5.50%  | 0.06810  | $14.625M  | $24.765M    | $26.344M   | $14.625M   | LTV
6.00%  | 0.07195  | $14.625M  | $23.436M    | $26.344M   | $14.625M   | LTV
6.50%  | 0.07587  | $14.625M  | $22.222M    | $26.344M   | $14.625M   | LTV
7.00%  | 0.07984  | $14.625M  | $21.113M    | $26.344M   | $14.625M   | LTV
7.50%  | 0.08386  | $14.625M  | $20.098M    | $26.344M   | $14.625M   | LTV
8.00%  | 0.08793  | $14.625M  | $19.168M    | $26.344M   | $14.625M   | LTV
8.50%  | 0.09203  | $14.625M  | $18.313M    | $26.344M   | $14.625M   | LTV
9.00%  | 0.09617  | $14.625M  | $17.527M    | $26.344M   | $14.625M   | LTV

At all rates tested, LTV remains binding for this deal because the property's
9.36% cap rate (NCF/Value) is high relative to the DSCR and DY thresholds.
```

### Low Cap Rate Scenario (Different Property)

```
Trophy property: Value = $45,000,000, NCF = $1,800,000 (4.0% cap)
Same lender terms: 65% LTV, 1.25x DSCR, 8.0% DY, 6.50% rate

  LTV:  $45,000,000 * 0.65 = $29,250,000
  DSCR: $1,800,000 / (1.25 * 0.07587) = $18,979,000
  DY:   $1,800,000 / 0.08 = $22,500,000

  Sized loan: min($29.25M, $18.98M, $22.50M) = $18,979,000
  BINDING: DSCR (actual LTV = 42.2%)

  At 7.50% rate:
  DSCR: $1,800,000 / (1.25 * 0.08386) = $17,170,000
  LTV equivalent: 38.2%

  This is a common scenario for low-cap-rate properties: the lender would
  approve 65% LTV but DSCR restricts to 38-42% LTV. The borrower must bring
  significantly more equity or use IO to improve the sizing.
```

### IO Impact on Sizing

```
Same trophy property at 6.50%, but with IO:
  IO debt service constant = 0.065 (rate only, no amortization)

  DSCR with IO: $1,800,000 / (1.25 * 0.065) = $22,154,000
  DSCR with amort: $1,800,000 / (1.25 * 0.07587) = $18,979,000

  IO adds: $22,154,000 - $18,979,000 = $3,175,000 of sizing (16.7% more)

  But: most lenders size to the amortizing DSCR, not IO DSCR.
  Agency lenders (Fannie/Freddie) size on a stressed amortizing basis.
  Bridge lenders and CMBS may size on IO DSCR, which is more aggressive.
```

---

## 4. Agency vs. CMBS vs. Bank Comparison

### Agency (Fannie Mae DUS / Freddie Mac Optigo)

```
LTV:          Up to 80% (standard), 65-75% (typical)
DSCR:         1.25x (standard), 1.20x (with IO)
Debt yield:   Not a primary metric (but implied by LTV/DSCR)
Rate:         Fixed, typically SOFR swap + 150-250bps
Term:         5, 7, 10, 12 years
Amortization: 30 years
IO:           1-5 years available (increases spread by 5-15bps)
Prepayment:   Yield maintenance or defeasance (expensive to exit early)
Sizing note:  Sized on 30-year amortizing DSCR, stressed rate
Pros:         Best rates, highest leverage, non-recourse
Cons:         Multifamily only, slow process, supplemental loan restrictions
```

### CMBS (Conduit)

```
LTV:          Up to 75% (conduit), 65-70% (typical)
DSCR:         1.25x (standard), DY 8-10%
Debt yield:   Primary sizing metric (NCF / loan)
Rate:         Fixed, benchmark Treasury + 150-300bps
Term:         5, 7, 10 years
Amortization: 25-30 years (some IO)
IO:           Common (full-term IO available for strong assets)
Prepayment:   Defeasance or yield maintenance (lock-out first 2 years)
Sizing note:  Debt yield is often binding (8-10% minimum)
Pros:         Non-recourse, all property types, assumable
Cons:         Inflexible (SPE requirements, cash management), servicer issues
```

### Bank / Credit Union

```
LTV:          55-70% (conservative)
DSCR:         1.30-1.50x (higher than agency/CMBS)
Debt yield:   8-12% (varies by bank)
Rate:         Floating (SOFR + 200-350bps) or short-term fixed
Term:         3-7 years (shorter than agency/CMBS)
Amortization: 25-30 years
IO:           Less common (banks prefer amortization)
Prepayment:   Flexible (step-down or small fee)
Recourse:     Partial or full recourse common
Sizing note:  Global cash flow and borrower financial strength considered
Pros:         Flexible terms, relationship-driven, faster closing
Cons:         Recourse, shorter terms, lower leverage, rate risk at maturity
```

### Sizing Comparison: 150-Unit MF at $22.5M

```
NCF: $2,107,556

Execution   | Rate  | LTV Limit | DSCR Limit | DY Limit  | Sized Loan | Binding
------------|-------|-----------|------------|-----------|------------|--------
Agency      | 5.75% | $16.875M  | $24.9M     | n/a       | $16.875M   | LTV
CMBS        | 6.25% | $15.750M  | $22.8M     | $23.4M    | $15.750M   | LTV
Bank        | 7.00% | $13.500M  | $17.7M     | $19.2M    | $13.500M   | LTV

Agency provides $3.4M more leverage than bank. The rate advantage
compounds: lower rate means lower debt service constant, which means
DSCR is more easily satisfied, allowing higher leverage.

Net equity required:
  Agency: $22.5M - $16.875M = $5.625M (25.0%)
  CMBS:   $22.5M - $15.750M = $6.750M (30.0%)
  Bank:   $22.5M - $13.500M = $9.000M (40.0%)
```

---

## 5. DSCR Stress Testing

### Lender Stress Test Convention

Many lenders underwrite to a stressed rate (typically +200bps above the note rate or a minimum floor rate) to ensure the loan can withstand rate increases at maturity.

```
Note rate: 6.50%
Stress rate: max(8.50%, note_rate + 200bps) = 8.50%

Stressed DSC at 8.50%, 30yr amort: 0.09203
Stressed DSCR = $2,107,556 / ($14,625,000 * 0.09203) = 1.57x

If lender requires 1.25x stressed: $2,107,556 / (1.25 * 0.09203) = $18,322,000
If lender requires 1.15x stressed: $2,107,556 / (1.15 * 0.09203) = $19,909,000

Stress testing may reduce the sized loan below the unstressed DSCR constraint.
```

### Breakeven Occupancy

```
Breakeven occupancy = (Operating expenses + Debt service) / Gross potential income

= ($1,338,694 + $1,109,355) / $3,675,000
= $2,448,049 / $3,675,000
= 66.6%

The property can sustain a vacancy of 33.4% before it cannot cover operating
expenses and debt service. This is a strong margin of safety.

Lenders typically want breakeven occupancy below 80%.
```

---

## 6. Supplemental / Subordinate Financing

### When to Use

Borrowers may seek supplemental or subordinate financing when:
- Property has appreciated since original loan (value-add execution)
- NOI has increased, creating DSCR headroom
- Borrower needs to pull equity for another investment
- Original loan has a yield maintenance prepayment penalty (cheaper to supplement than refinance)

### Agency Supplemental Sizing

```
Original loan: $14,625,000 at 5.50% (originated 3 years ago)
Current value: $26,000,000 (NOI increased to $2,400,000)
Current NCF: $2,355,000

Combined sizing constraints:
  Max combined LTV: 75% (agency supplemental allows higher than original)
  Min combined DSCR: 1.25x (stressed basis)

  Max combined debt (LTV): $26,000,000 * 0.75 = $19,500,000

  Original loan balance: $14,200,000 (after 3 years amortization)
  Original DS: $14,625,000 * 0.06810 = $995,768 (at 5.50%)

  Max supplemental (DSCR):
    Max combined DS = $2,355,000 / 1.25 = $1,884,000
    Available for supplemental DS = $1,884,000 - $995,768 = $888,232
    Supplemental DSC at 6.50%: 0.07587
    Max supplemental loan = $888,232 / 0.07587 = $11,706,000

  Max supplemental (LTV): $19,500,000 - $14,200,000 = $5,300,000

  Supplemental loan = min($5,300,000, $11,706,000) = $5,300,000 (LTV binding)

  Total debt: $14,200,000 + $5,300,000 = $19,500,000
  Blended rate: weighted average of original and supplemental
  Combined DSCR: $2,355,000 / ($995,768 + $5,300,000 * 0.07587)
               = $2,355,000 / ($995,768 + $402,111) = 1.69x (passes)
```

---

## 7. Quick-Reference Sizing Formulas

```
Max loan by LTV:
  Loan = Value * Max_LTV

Max loan by DSCR:
  Loan = NCF / (Min_DSCR * DSC)

Max loan by DY:
  Loan = NCF / Min_DY

Debt service constant (amortizing):
  DSC = [r(1+r)^n / ((1+r)^n - 1)] * 12
  where r = monthly rate, n = amort months

Debt service constant (IO):
  DSC = annual_rate

Breakeven occupancy:
  BEO = (OpEx + DS) / GPI

Cash-on-cash:
  CoC = (NCF - DS) / Equity

Loan-to-cost (for construction):
  LTC = Loan / Total development cost
```
