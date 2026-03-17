# Scenario Weighting Methodology

Base/upside/downside framework for probability-weighted return analysis in CRE acquisition underwriting. All examples use a 50-unit multifamily acquisition at $12,000,000.

---

## 1. Purpose

Single-point underwriting produces one IRR and one equity multiple. This is misleading: it implies false precision. Scenario analysis produces a range of outcomes weighted by likelihood, yielding an expected IRR that accounts for asymmetric risk.

Investment committee presentations at institutional shops (Blackstone, Brookfield, Starwood) always present three scenarios minimum. The expected return is the probability-weighted average, not the base case.

---

## 2. Scenario Definitions

### Standard Three-Scenario Framework

| Scenario | Probability | Characteristics |
|---|---|---|
| Downside | 20-30% | Recession, vacancy spike, rent decline, cap rate expansion |
| Base | 40-60% | Market consensus growth, stabilized operations |
| Upside | 15-25% | Outperformance on rents, below-market vacancy, cap compression |

Probabilities must sum to 100%. The base case should be the most likely single outcome, not the average.

### Expanded Five-Scenario Framework

For deals with higher complexity or IC scrutiny:

| Scenario | Probability | Description |
|---|---|---|
| Severe downside | 5-10% | Deep recession, 2008-style distress |
| Downside | 15-20% | Moderate stress |
| Base | 40-50% | Expected path |
| Upside | 15-20% | Favorable conditions |
| Strong upside | 5-10% | Exceptional execution, market tailwind |

---

## 3. Variable Adjustments by Scenario

### Multifamily Variable Grid

| Variable | Downside | Base | Upside |
|---|---|---|---|
| Rent growth (annual) | 1.0% | 3.0% | 4.5% |
| Vacancy rate | 8.0% | 5.0% | 3.5% |
| Expense growth | 4.0% | 3.0% | 2.5% |
| Exit cap rate | 6.75% (+75bps) | 6.25% (+25bps) | 5.75% (-25bps) |
| Capex overrun | +20% | 0% | -10% |
| Lease-up timeline | +6 months | On schedule | -3 months |

### Correlation Logic

Variables are not independent. In a recession:
- Vacancy rises AND rent growth slows AND cap rates expand
- These compound negatively on equity returns
- The downside scenario must reflect correlated stress, not independent bad outcomes applied simultaneously

In practice, this means the downside is not "worst case on every variable." It is a coherent economic scenario where multiple variables deteriorate together in a plausible way.

---

## 4. Worked Example: Three Scenarios

### Deal Parameters (Constant Across Scenarios)

```
Purchase price:    $12,000,000
Loan:              $7,800,000 (65% LTV, 6.50%, 30yr amort, 2yr IO)
Equity:            $4,500,000 (includes $300K capex)
Hold period:       7 years
Year 1 GPR:        $1,800,000
Year 1 expenses:   $680,000 (base)
```

### Downside Scenario (25% probability)

```
Assumptions:
  Rent growth:     1.0%/year
  Vacancy:         8.0% stabilized (starts at 10%)
  Expense growth:  4.0%/year
  Exit cap:        6.75%
  Capex overrun:   +20% ($360,000 total vs $300,000 base)

Year-by-Year NOI:
  Year 1:  GPR $1,800,000 * (1-0.10) + $60,000 other - $707,200 exp = $872,800
  Year 2:  GPR $1,818,000 * (1-0.08) + $61,200 - $735,488 = $998,272
  Year 3:  GPR $1,836,180 * (1-0.08) + $62,424 - $764,908 = $986,802
  Year 4:  GPR $1,854,542 * (1-0.08) + $63,672 - $795,504 = $974,346
  Year 5:  GPR $1,873,087 * (1-0.08) + $64,946 - $827,325 = $960,861
  Year 6:  GPR $1,891,818 * (1-0.08) + $66,245 - $860,418 = $946,299
  Year 7:  GPR $1,910,736 * (1-0.08) + $67,570 - $894,835 = $930,613

Reversion:
  Year 8 forward NOI = $930,613 * 1.01 = $939,919
  Gross reversion = $939,919 / 0.0675 = $13,924,726
  Less selling costs (2.0%): -$278,495
  Less loan balance: -$7,291,000
  Net equity reversion: $6,355,231

Cash flow stream:
  Year 0:  -$4,560,000  (extra capex)
  Year 1:   +$305,800
  Year 2:   +$431,272
  Year 3:   +$377,750
  Year 4:   +$365,294
  Year 5:   +$351,809
  Year 6:   +$337,247
  Year 7:   +$321,561 + $6,355,231 = $6,676,792

Levered IRR:    12.1%
Equity Multiple: 2.05x
```

### Base Scenario (50% probability)

```
Assumptions:
  Rent growth:     3.0%/year
  Vacancy:         5.0% stabilized
  Expense growth:  3.0%/year
  Exit cap:        6.25%
  Capex:           On budget ($300,000)

Year 7 NOI: $1,245,739 (from proforma-construction.md)

Reversion:
  Year 8 forward NOI = $1,283,111
  Gross reversion = $20,529,776
  Net equity reversion: $12,828,180

Levered IRR:    22.3%
Equity Multiple: 3.67x
```

### Upside Scenario (25% probability)

```
Assumptions:
  Rent growth:     4.5%/year
  Vacancy:         3.5% stabilized
  Expense growth:  2.5%/year
  Exit cap:        5.75%
  Capex:           -10% ($270,000)

Year-by-Year NOI:
  Year 1:  GPR $1,800,000 * (1-0.05) + $60,000 - $663,000 = $1,107,000
  Year 2:  GPR $1,881,000 * (1-0.035) + $61,200 - $679,575 = $1,196,190
  Year 3:  GPR $1,965,645 * (1-0.035) + $62,424 - $696,564 = $1,262,609
  Year 4:  GPR $2,054,099 * (1-0.035) + $63,672 - $713,978 = $1,332,899
  Year 5:  GPR $2,146,533 * (1-0.035) + $64,946 - $731,828 = $1,405,519
  Year 6:  GPR $2,243,127 * (1-0.035) + $66,245 - $750,123 = $1,480,739
  Year 7:  GPR $2,344,068 * (1-0.035) + $67,570 - $768,876 = $1,561,721

Reversion:
  Year 8 forward NOI = $1,561,721 * 1.045 = $1,632,998
  Gross reversion = $1,632,998 / 0.0575 = $28,400,000
  Less selling costs (2.0%): -$568,000
  Less loan balance: -$7,291,000
  Net equity reversion: $20,541,000

Cash flow stream:
  Year 0:  -$4,470,000
  Year 1:   +$540,000
  Year 2:   +$629,190
  Year 3:   +$653,557
  Year 4:   +$723,847
  Year 5:   +$796,467
  Year 6:   +$871,687
  Year 7:   +$952,669 + $20,541,000 = $21,493,669

Levered IRR:    31.8%
Equity Multiple: 5.95x
```

---

## 5. Probability-Weighted Expected Return

### Calculation

```
Expected IRR = sum(probability_i * IRR_i)

E[IRR] = 0.25 * 12.1% + 0.50 * 22.3% + 0.25 * 31.8%
E[IRR] = 3.025% + 11.15% + 7.95%
E[IRR] = 22.1%

E[Multiple] = 0.25 * 2.05x + 0.50 * 3.67x + 0.25 * 5.95x
E[Multiple] = 0.5125 + 1.835 + 1.4875
E[Multiple] = 3.84x
```

### Presentation Format for IC

```
                 Probability    Levered IRR    Equity Multiple    MOIC
Downside (25%)      25%           12.1%           2.05x          2.05x
Base (50%)          50%           22.3%           3.67x          3.67x
Upside (25%)        25%           31.8%           5.95x          5.95x
                                  ------          ------
Expected                          22.1%           3.84x
```

---

## 6. Interpreting the Results

### Return Dispersion

```
Range = Upside IRR - Downside IRR = 31.8% - 12.1% = 19.7%
Standard deviation (approx) = Range / 4 = ~4.9%
Coefficient of variation = StdDev / E[IRR] = 4.9 / 22.1 = 0.22
```

A CV below 0.30 indicates moderate return dispersion -- the deal performs reasonably even in downside. A CV above 0.50 indicates high uncertainty; the deal's return profile is wide.

### Downside Floor Test

Key question: Is the downside acceptable?

```
Downside IRR:      12.1%  (above cost of equity? typically 8-10% hurdle)
Downside Multiple: 2.05x  (above 1.0x -- no loss of principal)
Downside DSCR:     Check that NOI covers debt service in all years
```

If the downside scenario shows levered IRR below the hurdle rate or equity multiple below 1.5x, the deal's risk-adjusted return may not justify the investment.

### Asymmetry Check

```
Upside gap: 31.8% - 22.3% = 9.5%
Downside gap: 22.3% - 12.1% = 10.2%
```

The downside gap exceeds the upside gap, indicating slight negative skew. This is typical for leveraged real estate: leverage amplifies both directions, but downside scenarios tend to have compounding effects (rising vacancy + rising expenses + expanding cap rates).

---

## 7. Advanced: Expected Loss and Breakeven Probability

### Maximum Loss Scenario

Determine the probability of loss (equity multiple below 1.0x):

```
For this deal, even the downside returns 2.05x. Loss of principal requires:
  - Extended vacancy above 15%
  - Rent decline of -5% annually
  - Exit cap above 8.0%

This is a severe recession scenario with <5% probability for stabilized MF.
If we assign 3% probability to a -5% IRR (partial loss) scenario:

E[IRR] adjusted = 0.03 * (-5%) + 0.22 * 12.1% + 0.50 * 22.3% + 0.25 * 31.8%
                = -0.15% + 2.66% + 11.15% + 7.95% = 21.6%
```

The severe downside barely moves the expected return but changes the risk narrative.

### Breakeven Assumption Identification

Find the single variable value that produces 0% IRR (return of capital only):

```
Breakeven exit cap (all else base):
  At what exit cap does levered IRR = 0%?
  Gross reversion needed = equity + cumulative debt service - cumulative CF
  Solve for: exit_cap = forward_NOI / required_reversion

Breakeven vacancy (all else base):
  At what stabilized vacancy does IRR = 0%?
  Solve iteratively or by inspection.

For this deal:
  Breakeven exit cap: ~9.5% (far outside plausible range)
  Breakeven vacancy: ~22% stabilized (distress level)
```

These breakevens demonstrate substantial margin of safety.

---

## 8. Common Errors

1. **Probabilities that do not sum to 100%**: Every scenario framework must sum exactly. A common mistake is assigning 30/40/30 to downside/base/upside without verification.

2. **Independent variable stress**: Modeling downside as "worst rent growth AND worst vacancy AND worst exit cap AND worst expenses" simultaneously produces an unrealistically severe scenario. Use coherent, correlated scenarios that reflect real economic conditions.

3. **Symmetric probability assignment**: Assigning equal probability to upside and downside ignores base rates. In a rising rate environment, downside probability should exceed upside. In a supply-constrained market, the reverse may hold.

4. **Averaging IRRs directly**: The probability-weighted average of IRRs is an approximation. Strictly, you should probability-weight the cash flows and compute a single IRR from the expected cash flow stream. For CRE deals with similar timing, the approximation is within 25-50bps of the exact method.

5. **Ignoring path dependency**: A scenario with 2 years of stress followed by 5 years of recovery produces a different IRR than 5 years of moderate performance followed by 2 years of stress, even if total NOI is identical. Model the timing, not just the average.

6. **Presenting only the base case to IC**: If the base case is the only scenario presented, the investment committee cannot assess risk-adjusted returns. Always present all scenarios with probabilities.

7. **Not stress-testing the exit cap**: The exit cap is the largest single driver of reversion value. A 50bps change in exit cap on a $20M reversion is $1.5M+ in equity value. Run the exit cap sensitivity separately from the scenario analysis.

---

## 9. Scenario Documentation Template

For each scenario, document:

```
Scenario: [Name]
Probability: [X%]
Economic narrative: [1-2 sentences describing the macro/local conditions]
Key variable assumptions:
  - Rent growth: X%
  - Vacancy: X%
  - Expense growth: X%
  - Exit cap: X%
  - Capex adjustment: X%
  - Lease-up timeline adjustment: X months
Resulting metrics:
  - Levered IRR: X%
  - Equity multiple: X.Xx
  - Year 1 DSCR: X.Xx
  - Average cash-on-cash: X%
  - Peak equity exposure: $X
```

This structured documentation ensures comparability and auditability across deals in the pipeline.
