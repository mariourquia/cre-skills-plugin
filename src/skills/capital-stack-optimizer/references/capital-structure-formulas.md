# Capital Structure Formula Reference

Complete derivations, WACC across layers, equity IRR sensitivity to leverage, mezz/pref cost comparison, and hedging instrument overview. All examples use a baseline $30,000,000 multifamily acquisition.

---

## 1. Weighted Average Cost of Capital (WACC) Across Layers

### Notation

| Symbol | Definition |
|---|---|
| V | Total asset value (purchase price) |
| D_s | Senior debt amount |
| D_m | Mezzanine debt amount |
| E_p | Preferred equity amount |
| E_c | Common equity amount |
| r_s | Senior debt rate (coupon) |
| r_m | Mezz debt rate (coupon) |
| r_p | Preferred equity rate |
| r_c | Common equity required return (target IRR) |
| LTV_s | Senior loan-to-value = D_s / V |
| LTV_m | Combined LTV = (D_s + D_m) / V |

### Formula

```
WACC = (D_s/V)*r_s + (D_m/V)*r_m + (E_p/V)*r_p + (E_c/V)*r_c
```

For a simplified two-layer stack (senior debt + common equity):

```
WACC = LTV*r_s + (1-LTV)*r_c
```

### Worked Example: $30M Deal, 4-Layer Stack

```
Capital Stack:
  Senior debt:     $19,500,000  (65% LTV)    at 6.50%
  Mezzanine:       $3,000,000   (10%)        at 12.00%
  Preferred equity: $2,250,000  (7.5%)       at 9.00%
  Common equity:    $5,250,000  (17.5%)      target 18.00% IRR

WACC = (19,500,000/30,000,000)*0.065
     + (3,000,000/30,000,000)*0.12
     + (2,250,000/30,000,000)*0.09
     + (5,250,000/30,000,000)*0.18

WACC = 0.650*0.065 + 0.100*0.12 + 0.075*0.09 + 0.175*0.18
     = 0.04225 + 0.01200 + 0.00675 + 0.03150
     = 0.09250 = 9.25%
```

### Interpretation

The 9.25% WACC represents the blended cost of all capital. If the unlevered asset return (cap rate + appreciation) exceeds 9.25%, the deal creates value for common equity holders. If it falls below, common equity is destroyed.

The going-in cap rate of the $30M deal only needs to be checked against the senior debt cost for positive leverage analysis, but the full WACC determines whether the deal makes economic sense across all capital layers.

---

## 2. Equity IRR Sensitivity to Leverage

### The Leverage Amplification Formula

For a simplified annual model:

```
Levered_return = Unlevered_return + (Unlevered_return - cost_of_debt) * (D/E)

Where D/E = debt-to-equity ratio
```

This is the Modigliani-Miller leverage effect for real assets (ignoring taxes for clarity).

### Worked Example: Leverage Sensitivity Table

Base case: $30M deal, 6.0% going-in cap, 3% annual NOI growth, 5-year hold, exit cap 6.25%.

```
Unlevered IRR = 7.8% (cap rate + growth - exit cap expansion drag)

Scenario     | LTV  | Rate  | D/E    | Leverage Effect      | Levered IRR
-------------|------|-------|--------|----------------------|------------
No leverage  | 0%   | --    | 0.00   | 0                    | 7.8%
Conservative | 50%  | 6.00% | 1.00   | (7.8% - 6.0%)*1.00  | 9.6%
Standard     | 65%  | 6.50% | 1.86   | (7.8% - 6.5%)*1.86  | 10.2%
Aggressive   | 75%  | 7.00% | 3.00   | (7.8% - 7.0%)*3.00  | 10.2%
Max leverage | 80%  | 7.50% | 4.00   | (7.8% - 7.5%)*4.00  | 9.0%
Negative lev | 80%  | 8.00% | 4.00   | (7.8% - 8.0%)*4.00  | 7.0%
```

### Key Observations

1. **Diminishing returns**: Going from 0% to 50% LTV adds 1.8% IRR. Going from 50% to 65% adds only 0.6%.
2. **Optimal leverage point**: Around 65-75% LTV for this deal, depending on the rate environment. Beyond that, higher rates offset the amplification benefit.
3. **Negative leverage**: At 80% LTV with 8.0% rate, leverage destroys 0.8% of return. The deal would be better unlevered.
4. **Nonlinearity**: The relationship is not perfectly linear because of amortization, exit proceeds allocation, and compounding over the hold period. The formula above is a first-order approximation.

### Monte Carlo Sensitivity Grid

For IC presentations, build a 2D grid: LTV on one axis, rate on the other.

```
Levered IRR Grid (5-year hold, 6.0% cap, 3% growth, 6.25% exit cap):

Rate \ LTV |  50%  |  60%  |  65%  |  70%  |  75%  |
-----------|-------|-------|-------|-------|-------|
5.50%      | 10.8% | 11.9% | 12.6% | 13.5% | 14.8% |
6.00%      | 9.6%  | 10.3% | 10.8% | 11.4% | 12.2% |
6.50%      | 8.6%  | 9.0%  | 9.2%  | 9.5%  | 9.8%  |
7.00%      | 7.7%  | 7.8%  | 7.8%  | 7.7%  | 7.5%  |
7.50%      | 6.9%  | 6.7%  | 6.4%  | 6.1%  | 5.4%  |
```

The "ridge" where leverage contribution turns negative runs diagonally. At 7.0%, leverage is approximately neutral at 65-70% LTV. Above 7.0%, you want less leverage, not more.

---

## 3. Mezzanine vs. Preferred Equity Comparison

### Structural Differences

| Feature | Mezzanine Debt | Preferred Equity |
|---|---|---|
| Position in stack | Junior to senior, senior to equity | Junior to all debt, senior to common equity |
| Security | Second lien or intercreditor agreement | No lien; equity interest with priority |
| Foreclosure rights | Can foreclose (subject to intercreditor) | Cannot foreclose; must use equity remedies |
| Tax treatment | Interest is tax-deductible | Returns are not deductible (equity distribution) |
| Financial covenants | Common (DSCR, LTV triggers) | Less common; governance rights instead |
| Typical rate | 10-15% (current pay or PIK) | 8-12% (current pay preferred) |
| Maturity | Co-terminus with senior or +1 year | Redeemable at sale or refinance |
| Senior lender view | May require consent; increases combined LTV | Does not increase LTV; treated as equity |

### Cost Comparison: $3M Tranche

```
Scenario: $3M of capital needed between senior debt and common equity.

Option A: Mezzanine at 12% (interest-only, current pay)
  Annual cost: $3,000,000 * 0.12 = $360,000
  Tax shield (assuming 25% effective rate): $360,000 * 0.25 = $90,000
  After-tax cost: $270,000/year
  After-tax rate: 9.0%

Option B: Preferred equity at 9% (current pay, cumulative)
  Annual cost: $3,000,000 * 0.09 = $270,000
  Tax shield: $0 (equity, not deductible)
  After-tax cost: $270,000/year
  After-tax rate: 9.0%

Net result: At these rates, after-tax cost is identical.
Breakeven: Mezz rate * (1 - tax_rate) = Pref rate
           12% * (1 - 0.25) = 9.0%. Match.
```

### When to Choose Mezz vs. Pref

```
Choose mezzanine when:
  - Tax deductibility is valuable (taxable entity, positive taxable income)
  - You need to maintain control (debt covenants vs governance rights)
  - Senior lender will consent to the intercreditor
  - Shorter hold period (mezz has fixed maturity)

Choose preferred equity when:
  - Senior lender prohibits subordinate debt (common in agency loans)
  - You want to keep LTV low for refinancing flexibility
  - Entity structure makes tax deduction irrelevant (REIT, tax-exempt LP)
  - Pref equity provider brings strategic value (operating partner, co-developer)
```

### PIK (Payment-in-Kind) Mezz

Some mezz structures allow PIK interest: unpaid interest accrues and compounds rather than being paid current. This preserves cash flow but increases the mezz balance.

```
$3M mezz at 12%, 100% PIK for 3 years:
  Year 1: Balance grows to 3,000,000 * 1.12 = $3,360,000
  Year 2: Balance grows to 3,360,000 * 1.12 = $3,763,200
  Year 3: Balance grows to 3,763,200 * 1.12 = $4,214,784

Total owed at year 3: $4,214,784 (40.5% more than original)
Effective cost: $1,214,784 of accrued interest
```

PIK is cash-flow friendly during renovation/lease-up but dramatically increases exit breakeven.

---

## 4. Capital Stack Optimization Framework

### The Optimization Problem

Minimize WACC subject to:
1. Senior lender constraints (max LTV, min DSCR, min DY)
2. Mezz/pref provider constraints (min coverage, max combined leverage)
3. Common equity minimum return threshold
4. Cash flow sufficiency (all current-pay obligations must be met from NOI)

### Worked Example: $30M Deal Optimization

```
Property NOI: $1,800,000 (6.0% cap)
NOI growth: 3%/year
Exit cap: 6.25%, Year 5
Target common equity IRR: 18%+

Step 1: Max senior debt
  Agency lender terms: 65% LTV, 1.25x DSCR, 7.0% min DY, 6.50% rate, 30yr amort

  By LTV: $30M * 0.65 = $19,500,000
  Debt service constant at 6.50%, 30yr = 0.07585
  Annual DS = $19,500,000 * 0.07585 = $1,479,075
  DSCR = $1,800,000 / $1,479,075 = 1.217x  < 1.25x. DSCR binds.

  Max loan by DSCR: $1,800,000 / (1.25 * 0.07585) = $18,987,000
  DY check: $1,800,000 / $18,987,000 = 9.48% > 7.0%. Passes.

  Senior debt = $18,987,000 (63.3% LTV, DSCR-constrained)
  Annual DS = $18,987,000 * 0.07585 = $1,440,164

Step 2: Determine equity gap
  Total equity needed: $30,000,000 - $18,987,000 = $11,013,000

Step 3: Test mezz layer
  Mezz lender: 75% combined LTV max, 1.10x combined DSCR, 12% rate (IO)

  Max combined debt: $30M * 0.75 = $22,500,000
  Max mezz: $22,500,000 - $18,987,000 = $3,513,000
  Mezz DS: $3,513,000 * 0.12 = $421,560
  Combined DS: $1,440,164 + $421,560 = $1,861,724
  Combined DSCR: $1,800,000 / $1,861,724 = 0.967x < 1.10x. Fails.

  Max mezz by combined DSCR:
  Max combined DS = $1,800,000 / 1.10 = $1,636,364
  Max mezz DS = $1,636,364 - $1,440,164 = $196,200
  Max mezz = $196,200 / 0.12 = $1,635,000

  Mezz = $1,635,000 (combined LTV = 68.7%)

Step 4: Common equity residual
  Common equity = $30,000,000 - $18,987,000 - $1,635,000 = $9,378,000

Step 5: Compute WACC and check equity IRR
  WACC = (18,987/30,000)*0.065 + (1,635/30,000)*0.12 + (9,378/30,000)*r_c

  If target r_c = 18%:
  WACC = 0.6329*0.065 + 0.0545*0.12 + 0.3126*0.18
        = 0.04114 + 0.00654 + 0.05627 = 0.10395 = 10.4%

Step 6: Verify cash flow sufficiency
  Year 1 NOI:           $1,800,000
  Senior DS:            -$1,440,164
  Mezz interest:        -$196,200
  Net CF to equity:     $163,636
  Cash-on-cash:         $163,636 / $9,378,000 = 1.7%

  Year 1 CoC is thin. The deal relies on NOI growth and exit appreciation.
  By year 5: NOI = $1,800,000 * 1.03^4 = $2,025,876
  Year 5 CF to equity: $2,025,876 - $1,440,164 - $196,200 = $389,512 (4.2% CoC)
```

### Optimization Summary

```
Final Stack:
  Senior debt:   $18,987,000  (63.3%)  at 6.50%
  Mezzanine:     $1,635,000   (5.5%)   at 12.00%
  Common equity: $9,378,000   (31.3%)  target 18.00%
  WACC: 10.4%

Binding constraints: DSCR on senior (1.25x), combined DSCR on mezz (1.10x)
Non-binding: LTV (63.3% vs 65% max senior, 68.7% vs 75% max combined)
```

---

## 5. Equity IRR Decomposition

### Return Sources

```
Equity IRR = f(Cash-on-Cash, NOI Growth, Cap Rate Change, Leverage, Amortization)

Approximate decomposition:
  Unlevered yield:      Cap rate                        = 6.0%
  NOI growth:           g * hold_years / hold_years     = 3.0%
  Cap rate expansion:   -(exit_cap - entry_cap) * k     = -0.5% (6.25 vs 6.00)
  Unlevered IRR:                                        ≈ 8.5%
  Leverage contribution: (Unlev_IRR - r_s) * D/E        = (8.5% - 6.5%) * 1.72 = 3.4%
  Amortization benefit:  principal_paydown / equity / n  ≈ 0.8%
  Levered IRR:                                          ≈ 12.7%
```

The decomposition shows that at these rates, leverage contributes 3.4% of the 12.7% levered IRR. Without leverage, the deal returns only 8.5%. The deal is viable only because positive leverage exists (cap rate > debt cost).

---

## 6. Stress Testing the Stack

### Rate Sensitivity on $30M Deal

```
Base case: Senior at 6.50%, Mezz at 12.00%

Scenario         | Senior Rate | Mezz Rate | Equity CF Y1 | Equity IRR
-----------------|-------------|-----------|--------------|----------
Rates -100bps    | 5.50%       | 11.00%    | $355,000     | 16.2%
Base case        | 6.50%       | 12.00%    | $163,636     | 12.7%
Rates +100bps    | 7.50%       | 13.00%    | -$33,000     | 9.3%
Rates +200bps    | 8.50%       | 14.00%    | -$230,000    | 5.8%
Rates +300bps    | 9.50%       | 15.00%    | -$427,000    | 2.1%
```

At +100bps, year 1 cash flow turns negative. The deal requires reserves or an equity call. At +200bps, the deal is marginally viable. At +300bps, the deal should not proceed.

### Hedging Implication

If the senior loan is floating-rate (SOFR + spread), a 200bps rate increase destroys the deal. The capital stack optimizer must incorporate hedging costs or recommend fixed-rate execution. See `hedging-guide.md` for instrument details.
