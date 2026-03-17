# Sensitivity & Stress Test Methodology

Frameworks and worked examples for sensitivity analysis, tornado charts, breakeven calculations, Monte Carlo reference, and lender covenant stress testing. All examples use a 100-unit multifamily property acquired for $18,000,000 with $11,700,000 debt (65% LTV) at 6.50%, 30-year amortization, 2-year IO.

---

## 1. Two-Way Sensitivity Grid

### Purpose

A two-way grid isolates the interaction of two key variables on a return metric. The standard grids for CRE:

```
Grid 1: Exit Cap Rate vs. Rent Growth         -> Levered IRR
Grid 2: Going-In Cap Rate vs. Interest Rate    -> Year 1 DSCR
Grid 3: Vacancy Rate vs. Exit Cap Rate         -> Equity Multiple
```

### Construction Method

1. Select two variables (row and column).
2. Define a range: base case +/- 2 increments (5x5 grid minimum, 7x7 for IC).
3. Hold all other variables constant at base case.
4. Compute the target metric at each intersection.
5. Highlight the base case cell and shade cells below hurdle/threshold.

### Worked Grid: Levered IRR (Exit Cap vs. Rent Growth)

Base case: 6.25% exit cap, 3.0% rent growth, 7-year hold.

```
                          Annual Rent Growth
Exit Cap    1.0%     2.0%     2.5%     3.0%     3.5%     4.0%     5.0%
  5.50%    15.2%    17.8%    19.1%    20.3%    21.6%    22.9%    25.4%
  5.75%    14.0%    16.5%    17.7%    18.9%    20.1%    21.4%    23.8%
  6.00%    12.8%    15.2%    16.4%    17.6%    18.8%    20.0%    22.3%
  6.25%    11.7%    14.0%    15.2%   [16.3%]   17.5%    18.7%    21.0%
  6.50%    10.7%    12.9%    14.0%    15.2%    16.3%    17.5%    19.7%
  6.75%     9.7%    11.9%    12.9%    14.0%    15.2%    16.3%    18.5%
  7.00%     8.8%    10.9%    11.9%    13.0%    14.1%    15.2%    17.3%

[16.3%] = base case cell
Cells below 12% hurdle rate shaded (lower-left region)
```

### Reading the Grid

- Moving right (higher rent growth): IRR increases ~130bps per 100bps of additional growth.
- Moving down (higher exit cap): IRR decreases ~100-120bps per 25bps of cap expansion.
- The exit cap has asymmetric impact: compression from 6.25% to 5.50% adds 400bps; expansion from 6.25% to 7.00% loses 330bps. This reflects the convexity of cap rate math (value = NOI / cap, so small cap changes at low cap rates produce larger value swings).

---

## 2. Tornado Chart Variable Ranking

### Purpose

A tornado chart ranks variables by their impact on the target metric, showing which assumptions matter most.

### Method

1. Define base case values for all variables.
2. For each variable, hold all others constant and swing +/- one standard deviation (or a defined range).
3. Record the resulting target metric (levered IRR) at each extreme.
4. Rank variables by total range (high value minus low value).

### Worked Example

Base case levered IRR: 16.3%

```
Variable               Low Swing     IRR at Low    High Swing    IRR at High   Range
Exit cap rate          +75bps (7.00%)   13.0%      -75bps (5.50%)   20.3%      7.3%
Rent growth            -2% (1.0%)       11.7%      +2% (5.0%)       21.0%      9.3%
Vacancy rate           +5% (10.0%)      12.8%      -2% (3.0%)       17.9%      5.1%
Interest rate          +150bps (8.0%)   14.1%      -150bps (5.0%)   18.8%      4.7%
Expense growth         +2% (5.0%)       14.5%      -1% (2.0%)       17.2%      2.7%
Going-in cap rate      +50bps (6.5%)    17.8%*     -50bps (5.5%)    14.9%*     2.9%
Capex overrun          +30%             15.5%      -20%             16.8%      1.3%
Selling costs          +1% (3.0%)       15.7%      -1% (1.0%)       16.9%      1.2%

* Going-in cap affects purchase price, which changes equity invested.
```

### Ranking (by range, descending)

```
1. Rent growth           9.3%   ████████████████████████████
2. Exit cap rate         7.3%   ██████████████████████
3. Vacancy rate          5.1%   ███████████████
4. Interest rate         4.7%   ██████████████
5. Going-in cap rate     2.9%   █████████
6. Expense growth        2.7%   ████████
7. Capex overrun         1.3%   ████
8. Selling costs         1.2%   ████
```

Rent growth and exit cap dominate. Together they explain ~70% of total return variability. Focus diligence and negotiation on these two assumptions.

---

## 3. Breakeven Calculation

### Definition

The breakeven value for a variable is the level at which the target metric hits a defined threshold (typically 0% IRR for loss avoidance, or hurdle rate for go/no-go).

### Formulas

```
Breakeven exit cap (for 0% IRR):
  Find exit_cap such that NPV of equity cash flows = 0 at IRR = 0%
  This means: total cash returned = total equity invested
  Solve: reversion = equity - cumulative_BTCF
  Then: exit_cap = forward_NOI / (reversion + selling_costs + loan_balance)

Breakeven vacancy (for target DSCR):
  Find vacancy_rate such that NOI = debt_service * DSCR_min
  vacancy_rate = 1 - [(debt_service * DSCR_min + expenses) / (GPR + other_income)]

Breakeven rent decline (for 0% IRR):
  Find annual rent decline rate d such that NPV = 0
  Iterative: solve for d where equity multiple = 1.0x
```

### Worked Breakevens

Deal: $18M purchase, $6.3M equity, $11.7M loan at 6.50%.

```
Breakeven exit cap (0% IRR):
  Total equity invested: $6,300,000 + $400,000 capex = $6,700,000
  Cumulative BTCF years 1-7: ~$3,200,000 (base case)
  Required reversion proceeds: $6,700,000 - $3,200,000 = $3,500,000
  Required gross reversion: $3,500,000 + $234,000 costs + $10,935,000 loan = $14,669,000
  Forward NOI: $1,283,000
  Breakeven exit cap: $1,283,000 / $14,669,000 = 8.7%

  Current base exit cap: 6.25%
  Margin of safety: 245bps of cap expansion before total loss

Breakeven vacancy (1.25x DSCR, Year 3 amortizing):
  Annual debt service (amortizing): $887,328
  Required NOI: $887,328 * 1.25 = $1,109,160
  Year 3 expenses: $1,019,000
  Required EGI: $1,109,160 + $1,019,000 = $2,128,160
  Year 3 GPR + other: $2,864,000 + $92,000 = $2,956,000
  Max vacancy: 1 - ($2,128,160 / $2,956,000) = 28.0%

  Current base vacancy: 5%
  Margin: 23 percentage points before DSCR covenant breach

Breakeven rent decline (0% IRR):
  Iterative solution: rents can decline ~3.5% annually for 7 years
  before equity multiple falls below 1.0x.
  At -3.5% annual: Year 7 GPR = $2,700,000 * (1-0.035)^6 = $2,165,000
  Margin: Current base assumes +3.0% growth. Breakeven requires -3.5%.
  Swing: 650bps of rent growth deterioration.
```

---

## 4. Monte Carlo Reference

### When to Use

Monte Carlo simulation replaces deterministic scenario analysis with probabilistic distributions. Use it when:
- More than 3 variables interact
- Variable distributions are non-normal (rent growth has fat tails)
- You need a probability distribution of outcomes, not point estimates

### Variable Distributions

| Variable | Distribution | Parameters | Rationale |
|---|---|---|---|
| Rent growth | Normal, truncated | mu=3.0%, sigma=1.5%, min=-5%, max=8% | Symmetric around base; bounded |
| Vacancy rate | Beta | alpha=2, beta=8 (mean ~5%) | Bounded 0-100%; right-skewed |
| Exit cap rate | Normal | mu=6.25%, sigma=0.50% | Symmetric uncertainty |
| Expense growth | Normal | mu=3.0%, sigma=0.75% | Tight range |
| Interest rate | Normal | mu=6.50%, sigma=0.75% | Rate uncertainty |
| Capex overrun | Lognormal | mu=0, sigma=0.15 | Right-skewed (overruns more likely) |

### Correlation Matrix

Variables are correlated. Ignore correlation and you understate tail risk.

```
              Rent    Vacancy  ExitCap  ExpGrow  IntRate  Capex
Rent Growth    1.00   -0.40    -0.30     0.20     0.10    0.00
Vacancy       -0.40    1.00     0.50    -0.10     0.20    0.00
Exit Cap      -0.30    0.50     1.00     0.10     0.60    0.00
Exp Growth     0.20   -0.10     0.10     1.00     0.30    0.10
Int Rate       0.10    0.20     0.60     0.30     1.00    0.00
Capex          0.00    0.00     0.00     0.10     0.00    1.00
```

Key correlations: exit cap and interest rate (+0.60), vacancy and exit cap (+0.50), rent growth and vacancy (-0.40). These reflect the macro linkage: recessions raise rates, vacancies, and cap rates simultaneously.

### Output Interpretation

After 10,000 simulations:

```
Levered IRR distribution:
  5th percentile:    8.2%    (downside tail)
  25th percentile:  12.8%    (lower quartile)
  Median (50th):    16.5%    (close to deterministic base case)
  75th percentile:  20.4%    (upper quartile)
  95th percentile:  26.1%    (upside tail)
  Mean:             16.8%
  Std deviation:     5.4%

Probability of IRR > 12% hurdle:  78%
Probability of loss (multiple < 1.0x):  2.3%
```

### Implementation Note

Monte Carlo is not standard in acquisition memos. It is used for portfolio-level analysis, fund modeling, and IC appendices at sophisticated shops. The three-scenario framework is the primary presentation tool; Monte Carlo validates the scenario probability assignments.

---

## 5. Lender Stress Test: Rate Shock

### The +200bps Stress

Lenders stress the deal at origination rate + 200bps to ensure the borrower can service debt if rates rise at refinance.

```
Origination rate:     6.50%
Stressed rate:        8.50%
Loan balance at Y7:   $10,935,000

Current annual DS:    $887,328  (6.50%, 30yr amort)
Stressed annual DS:   $1,094,580  (8.50%, 25yr amort -- shorter refi term)

Year 7 NOI:           $1,245,739
Current DSCR:         1.40x
Stressed DSCR:        1.14x   (below 1.25x covenant)
```

### Rate Sensitivity Grid

```
Interest Rate    Annual DS      DSCR (Y7 NOI)    Pass 1.25x?
5.50%           $797,100        1.56x             Yes
6.00%           $841,200        1.48x             Yes
6.50%           $887,328        1.40x             Yes
7.00%           $935,520        1.33x             Yes
7.50%           $985,680        1.26x             Barely
8.00%          $1,038,000       1.20x             No
8.50%          $1,094,580       1.14x             No
9.00%          $1,153,200       1.08x             No
```

Breakeven rate for 1.25x DSCR: approximately 7.45%. Above this rate, the deal fails the standard debt service coverage test at refinance.

---

## 6. Covenant Cascade

### DSCR Covenant Levels

Loan documents define escalating consequences as DSCR deteriorates:

```
DSCR Level     Covenant Status          Typical Consequence
> 1.25x        Compliant                No restrictions
1.10x - 1.25x  Soft trigger / lockbox   Cash sweep into lender-controlled reserve
1.00x - 1.10x  Hard trigger             Cash sweep + no distributions to equity
< 1.00x        Default / payment breach Potential acceleration of loan maturity
```

### Worked Cascade

Starting NOI: $1,080,000 (Year 1, 100-unit MF)
Annual debt service (amortizing): $887,328
Base DSCR: 1.22x

```
Stress event: 15% vacancy spike (base 5% to 20%) due to local employer closure

Stressed NOI calculation:
  GPR: $2,700,000
  Vacancy at 20%: -$540,000
  Other income: $90,000
  EGI: $2,250,000
  Expenses: $1,080,000
  Stressed NOI: $1,170,000

Wait -- this NOI is higher than base. Recalculate with correct base.

Base case:
  GPR: $2,700,000
  Vacancy at 5%: -$135,000
  Other income: $90,000
  EGI: $2,655,000
  Expenses: $1,575,000
  NOI: $1,080,000
  DSCR: $1,080,000 / $887,328 = 1.22x

Stressed (20% vacancy):
  GPR: $2,700,000
  Vacancy at 20%: -$540,000
  Other income: $72,000  (reduced proportionally)
  EGI: $2,232,000
  Expenses: $1,510,000  (partially variable, reduced 4%)
  NOI: $722,000
  DSCR: $722,000 / $887,328 = 0.81x  -- DEFAULT

Cascade:
  1.22x -> covenant compliant (starting point)
  At 10% vacancy: NOI = $919,000, DSCR = 1.04x -> hard lockbox triggered
  At 13% vacancy: NOI = $835,000, DSCR = 0.94x -> payment default
  At 20% vacancy: NOI = $722,000, DSCR = 0.81x -> deep default, acceleration risk
```

### Lender Remedies at Each Level

```
Soft trigger (DSCR 1.10-1.25x):
  - Excess cash flow swept to lender reserve
  - Borrower must submit remediation plan within 30 days
  - No equity distributions permitted
  - Cure: maintain DSCR > 1.25x for 2 consecutive quarters

Hard trigger (DSCR 1.00-1.10x):
  - Full cash sweep (100% of excess cash to lender)
  - Lender may require property management change
  - Additional reporting requirements (monthly P&L)
  - Cure: maintain DSCR > 1.25x for 4 consecutive quarters

Default (DSCR < 1.00x):
  - Event of default under loan documents
  - Lender may accelerate maturity (call the loan)
  - Lender may pursue foreclosure (judicial or non-judicial)
  - Borrower may negotiate forbearance or modification
  - Cure: full repayment or negotiated restructuring
```

---

## 7. Presenting Sensitivity Results

### IC Presentation Hierarchy

1. **Base case return metrics** (IRR, multiple, CoC, DSCR)
2. **Two-way grid** (exit cap vs. rent growth on IRR)
3. **Tornado chart** (variable ranking)
4. **Breakeven analysis** (margin of safety on each key variable)
5. **Scenario-weighted return** (base/upside/downside with expected IRR)
6. **Lender stress test** (rate shock DSCR)

### What IC Members Look For

- Is the downside IRR above the hurdle rate?
- How much can the exit cap expand before loss of principal?
- What vacancy level triggers covenant breach?
- Is the deal robust to correlated stress (rate + vacancy + expense)?

---

## 8. Common Errors

1. **Varying one variable while ignoring correlation**: A 200bps rate increase does not happen in isolation. It typically coincides with higher cap rates and slower rent growth. One-way sensitivities understate true downside risk. Supplement with correlated stress scenarios.

2. **Using symmetric ranges**: Upside and downside are not symmetric. Cap rates can expand 200bps in a crisis but rarely compress 200bps from current levels. Use asymmetric ranges reflecting current market position.

3. **Ignoring the IO-to-amortization cliff**: Sensitivity grids that use a single debt service figure miss the jump when IO burns off. Run separate grids for IO-period DSCR and amortizing-period DSCR.

4. **Presenting sensitivity without breakevens**: A grid shows the range but does not highlight the threshold. Always annotate the breakeven value (the line where IRR crosses the hurdle rate or DSCR crosses 1.25x).

5. **Overfitting Monte Carlo**: Running 100,000 simulations with precise distribution parameters implies false confidence in the inputs. The output is only as good as the assumed distributions and correlations. Garbage in, garbage out with extra decimal places.

6. **Forgetting selling costs in breakeven exit cap**: When computing breakeven exit cap for 0% IRR, the gross reversion must cover the loan balance, selling costs, and remaining equity shortfall. Omitting selling costs understates the breakeven by 15-25bps.

7. **Stressing debt service without adjusting amortization**: At refinance, the new lender may require a shorter amortization (25 years instead of 30). Stressing only the rate while keeping 30-year amort understates the debt service impact by 5-8%.
