# Boot Minimization Strategies Reference

Reference for the 1031-pipeline-manager skill. Covers cash boot, mortgage boot, combined boot netting, and elimination strategies with worked examples and common traps.

---

## Boot Fundamentals

Boot is any non-like-kind property received in a 1031 exchange. Boot is taxable to the extent of the realized gain -- you cannot owe tax on boot exceeding your actual gain. The goal of a properly structured exchange is $0 boot.

```
Two types of boot in real estate exchanges:

1. CASH BOOT:
   Occurs when the exchanger receives cash or cash-equivalent
   from the exchange. Most common cause: replacement property
   value < relinquished property net sale proceeds.

   Taxable amount = lesser of (cash boot, realized gain)

2. MORTGAGE BOOT:
   Occurs when the debt on the replacement property is less
   than the debt retired on the relinquished property. The
   IRS treats the debt relief as equivalent to cash received.

   Taxable amount = lesser of (mortgage boot, realized gain)

3. COMBINED:
   Cash boot + mortgage boot are netted. Additional cash
   contributed by the exchanger can offset mortgage boot.
```

---

## Cash Boot: Detailed Analysis

### When Cash Boot Occurs

```
Scenario 1: Replacement price < Relinquished price
  Relinquished sold for: $5,000,000
  Replacement purchased for: $4,200,000
  Cash boot: $800,000

  Why: QI holds $5M in proceeds but only needs to deploy $4.2M.
  The $800K difference is boot unless otherwise deployed.

Scenario 2: Non-exchange expenses paid from QI funds
  If QI pays exchanger's personal expenses, tax obligations,
  or non-exchange costs from exchange proceeds, those payments
  are boot. QI should ONLY disburse to:
    - Title company for replacement property acquisition
    - Exchange-related transaction costs

Scenario 3: Earnest money returned to exchanger
  If a replacement candidate falls through and earnest money
  is returned to the exchanger (not to QI), that money is boot.
  Prevention: structure all earnest money deposits through QI.
```

### Cash Boot Elimination Strategies

```
Strategy 1: Acquire higher-value replacement property
  Cost: higher purchase price (but no wasted tax dollars)
  Feasibility: depends on available properties and exchanger's financing capacity
  Example:
    Relinquished: $5,000,000
    Originally targeting: $4,200,000 replacement
    Boot exposure: $800,000
    Tax on boot: ~$190,000 (federal + state)
    Solution: acquire $5,000,000+ replacement instead
    Net cost: $0 additional (just deploying more capital)

Strategy 2: Acquire additional replacement property
  If primary replacement doesn't fully absorb proceeds:
    Primary: $3,500,000
    Remaining QI proceeds: $1,500,000
    Second replacement: $1,500,000 NNN single-tenant property
    Total replacement value: $5,000,000 (matches relinquished)
    Boot: $0

  Requirements:
    - Second property must be identified on the Day 45 letter
    - Must close within 180-day window
    - Must be like-kind real property

Strategy 3: DST absorption of excess proceeds
  If primary replacement leaves $200K-$500K undeployed:
    DST minimum investment: typically $100,000
    DST closing timeline: 5-14 business days
    DST matches relinquished deadline easily
    Boot: $0

  Requirements:
    - DST must be identified on the Day 45 letter
    - DST sponsor must have available allocation
    - Exchanger accepts DST's illiquidity and fees

Strategy 4: Accept partial boot (conscious decision)
  Sometimes the tax cost of boot is less than the cost of
  eliminating it. Calculate both and present to exchanger.

  Example:
    Boot: $50,000
    Tax on boot: ~$12,000 (20% LTCG + 3.8% NIIT)
    Cost of DST to absorb $50K: $5,000-$8,000 in fees over 7-10 years
    Decision: DST is cost-effective IF DST return exceeds fee drag
    Alternative: pay $12K tax and keep liquidity
```

---

## Mortgage Boot: Detailed Analysis

### When Mortgage Boot Occurs

```
The debt replacement rule: exchanger must take on debt at least
equal to the debt retired on the relinquished property.

Scenario 1: Lower LTV on replacement
  Relinquished:
    Value: $5,000,000
    Debt: $3,500,000 (70% LTV)
    Equity: $1,500,000

  Replacement:
    Value: $5,200,000
    Debt: $2,600,000 (50% LTV)
    Equity: $2,600,000

  Cash boot: $0 (replacement value > relinquished value)
  Mortgage boot: $900,000 ($3,500,000 - $2,600,000)
  This is taxable boot even though the replacement is more valuable.

Scenario 2: All-cash replacement when relinquished had debt
  Relinquished: $5,000,000 value, $3,000,000 debt
  Replacement: $5,500,000 all-cash purchase
  Cash boot: $0
  Mortgage boot: $3,000,000 (full amount of retired debt)
  Tax: substantial -- up to $3M of gain is recognized

Scenario 3: Partial debt replacement
  Relinquished debt: $4,000,000
  Replacement debt: $3,200,000
  Mortgage boot: $800,000
  Exchanger must either increase replacement debt by $800K
  or contribute $800K additional cash to avoid boot.
```

### Mortgage Boot Elimination Strategies

```
Strategy 1: Increase replacement loan amount
  Request higher LTV from lender
  Feasibility: depends on property value, DSCR, and lender appetite
  Example:
    Need: $3,500,000 replacement debt (to match relinquished)
    Current offer: $2,600,000 (50% LTV on $5.2M property)
    Solution: request 67% LTV = $3,484,000
    Remaining mortgage boot: $16,000 (minimal)
    Consideration: higher debt increases debt service and reduces cash flow

Strategy 2: Add cash to offset mortgage boot
  Exchanger contributes additional cash equal to the debt shortfall
  The additional cash is treated as part of the exchange consideration
  Example:
    Mortgage boot: $900,000
    Exchanger contributes: $900,000 additional cash at closing
    Net boot: $0
    Cash outlay: $900,000 (non-taxable exchange consideration)
  vs. Tax cost of $900K boot: ~$215,000
  Decision: contribute cash if available; if not, explore other strategies

Strategy 3: Seller carryback note
  Seller of replacement property provides financing to exchanger
  Creates a debt obligation on the replacement property
  Example:
    Purchase price: $5,200,000
    Senior loan: $2,600,000
    Seller carryback: $900,000 (second lien)
    Total replacement debt: $3,500,000 (matches relinquished)
    Mortgage boot: $0

  Considerations:
    - Seller must agree to provide financing
    - Senior lender must approve second lien (subordination agreement)
    - Seller carryback rate and terms negotiable
    - Typical terms: 3-5 years, interest-only, 6-8% rate
    - This is a real debt obligation -- not a paper transaction

Strategy 4: Cross-collateralization
  Exchanger pledges another owned property as additional collateral
  Lender provides higher loan amount based on combined collateral
  Example:
    Replacement property: $5,200,000
    Other owned property: $2,000,000 (free and clear)
    Blanket mortgage: $4,200,000 across both properties
    Mortgage boot eliminated: $4,200,000 > $3,500,000 relinquished debt

  Considerations:
    - Not all lenders offer cross-collateralization
    - Puts the other property at risk
    - More complex loan documents and release provisions
    - Must negotiate partial release clause for future property sales

Strategy 5: Supplemental financing
  Obtain separate supplemental or bridge financing
  Mezzanine loan, preferred equity, or HELOC on other assets
  Example:
    Senior loan: $2,600,000
    Supplemental mezz: $900,000
    Total debt: $3,500,000 (matches relinquished)
    Mortgage boot: $0

  Considerations:
    - Mezz/preferred equity has higher cost (12-18% typical)
    - May be temporary: refinance into single senior loan post-close
    - Intercreditor agreement needed between senior and mezz
    - Increases cost of capital and reduces cash-on-cash return
```

---

## Combined Boot: Netting Rules

```
IRS netting rule for cash boot and mortgage boot:

RULE: Additional cash contributed by the exchanger can offset
mortgage boot. But additional debt does NOT offset cash boot.

In other words:
  - Cash offsets mortgage boot: YES
  - Debt offsets cash boot: NO

Example 1: Cash offsets mortgage boot
  Relinquished: $5M value, $3.5M debt, $1.5M QI proceeds
  Replacement: $5.2M value, $2.8M debt

  Cash boot: $0 (replacement value $5.2M > relinquished $5M)
  Mortgage boot: $700K ($3.5M relinquished - $2.8M replacement)

  Exchanger contributes $700K additional cash at closing:
    Total equity: $1.5M QI proceeds + $700K new cash = $2.2M
    Total equity needed: $5.2M - $2.8M = $2.4M
    Gap: $200K (this is the $200K price premium)
    Wait -- let me recalculate:
      Purchase price: $5,200,000
      Debt: $2,800,000
      Equity needed: $2,400,000
      QI proceeds: $1,500,000 (after $3.5M debt payoff from $5M sale)
      Additional cash: $2,400,000 - $1,500,000 = $900,000
      Of this $900K: $700K offsets mortgage boot, $200K covers price premium

  Net boot: $0 (all mortgage boot offset by additional cash)

Example 2: Debt does NOT offset cash boot
  Relinquished: $5M value, $2M debt
  Replacement: $4M value, $3M debt

  Cash boot: $1,000,000 ($5M - $4M)
  Mortgage boot: $0 ($3M replacement > $2M relinquished)

  The excess replacement debt ($1M) does NOT offset the cash boot.
  Boot recognized: $1,000,000
  This is taxable even though the exchanger took on more debt.

Example 3: Both types present, partial offset
  Relinquished: $5M value, $3.5M debt
  Replacement: $4.8M value, $3.0M debt

  Cash boot: $200,000 ($5M - $4.8M)
  Mortgage boot: $500,000 ($3.5M - $3.0M)

  Exchanger contributes $500K additional cash:
    $500K cash offsets $500K mortgage boot -> mortgage boot = $0
    Cash boot remains: $200,000 (not offset by anything)
    Total taxable boot: $200,000

  To eliminate all boot:
    Either increase replacement value by $200K (buy at $5M+)
    Or increase replacement debt by $500K and add no cash
      (only works if you also solve the cash boot separately)
```

---

## Common Boot Traps

```
TRAP 1: Forgetting that selling costs reduce net proceeds but not boot calculation
  Boot is calculated on gross values and debt, not net proceeds.
  Selling costs reduce what the QI holds, but the boot math uses sale price.
  If relinquished sells for $5M with $200K in costs:
    QI holds: $5M - $3.5M debt - $200K costs = $1.3M
    Boot analysis still uses $5M as the relinquished value
    Replacement must be >= $5M to avoid cash boot

TRAP 2: Personal property received as part of the exchange
  If the replacement property includes personal property (furniture, equipment,
  fixtures not permanently attached), the personal property is boot.
  Example: buying a hotel with $500K in FF&E -> $500K boot unless
  FF&E is excluded from the exchange and paid for separately.

TRAP 3: Closing cost allocation creating boot
  If exchange funds are used to pay non-exchange expenses (exchanger's
  taxes, personal obligations, unrelated business debts), those payments
  are boot. Ensure QI only disburses for exchange-related costs.

TRAP 4: Security deposit liability assumed without corresponding credit
  When buying replacement property: security deposits held by seller
  are credited to buyer (buyer assumes the liability). This credit
  reduces the net amount buyer needs to pay, but the purchase price
  for boot calculation is the gross contract price, not the net amount.
  This is not a trap per se, but it confuses boot calculations.

TRAP 5: Earnest money on failed replacement returned to exchanger
  If a replacement deal falls through and earnest money is returned
  to the exchanger (not to QI), the returned money is boot.
  Prevention: all earnest money should be deposited by QI or routed
  back to QI if returned.

TRAP 6: Exchange proceeds used for improvements on relinquished property
  After Day 0, exchange proceeds cannot be used to improve the
  relinquished property (it has already been sold). In an improvement
  exchange, proceeds can only improve the replacement property
  through the EAT structure.
```

---

## Decision Framework: Accept Boot vs. Eliminate Boot

```
When to accept partial boot (conscious decision):

Calculate:
  A = Tax cost of boot ($boot * effective_tax_rate)
  B = Cost of eliminating boot (DST fees, higher interest, seller carryback cost, etc.)
  C = Opportunity cost of deploying additional cash to eliminate boot

If A < B + C: Accept the boot. Simpler, more liquid, lower total cost.
If A > B + C: Eliminate the boot. The exchange is worth preserving.

Rules of thumb:
  - Boot under $50,000: usually cheaper to accept (tax ~$12K)
  - Boot $50K-$200K: case-by-case analysis
  - Boot over $200K: usually worth eliminating (tax >$48K exceeds most elimination costs)
  - Always compare to DST option as a clean fallback
```
