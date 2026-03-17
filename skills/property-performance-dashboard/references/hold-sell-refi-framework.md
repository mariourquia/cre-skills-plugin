# Hold / Sell / Refinance Decision Framework

Marginal return on equity analysis, IRR-to-date methodology, mark-to-market NAV estimation, and cycle positioning overlay. Institutional decision framework with worked examples.

---

## 1. The Core Question: Marginal Return on Equity

The hold/sell/refi decision reduces to one question: **What is the expected return on the equity currently trapped in this asset, and can it be redeployed at a higher return?**

### Trapped Equity Calculation

```
Trapped equity = mark_to_market_value - outstanding_loan_balance - selling_costs

Mark-to-market value: current appraised value or broker opinion of value (BOV)
Outstanding loan balance: remaining principal after amortization
Selling costs: broker commission (1-3%) + transfer tax + legal + other (typically 2-4% total)
```

**Worked Example:**

```
Property: 200-unit MF, acquired 3 years ago at $32M
Current mark-to-market: $38,000,000 (based on T-12 NOI / market cap rate)
Loan balance: $20,200,000 (original $21M, 30yr amort, 3 years paid)
Selling costs: 3.0% of $38M = $1,140,000

Trapped equity = $38,000,000 - $20,200,000 - $1,140,000 = $16,660,000
```

### Marginal Return on Trapped Equity

```
Marginal return = forward_annual_BTCF / trapped_equity

Forward annual BTCF (before-tax cash flow):
  Forward NOI: $2,200,000 (Year 4 budget)
  Debt service: -$1,512,000 (annual P&I)
  Forward BTCF: $688,000

Marginal return = $688,000 / $16,660,000 = 4.13%
```

### Decision Rule

```
If marginal_return_on_trapped_equity > redeployment_hurdle_rate: HOLD
If marginal_return_on_trapped_equity < redeployment_hurdle_rate: SELL or REFI

Redeployment hurdle rate = expected levered CoC on the best available alternative investment
  Adjusted for: transaction costs, execution risk, deployment timeline (idle capital drag)
```

The comparison is NOT marginal return vs the property's original underwritten return. It is marginal return vs the best alternative use of that equity today.

---

## 2. IRR-to-Date

### Methodology

IRR-to-date treats the current mark-to-market value as a hypothetical reversion, calculating the IRR as if the property were sold today.

```
Cash flows for IRR-to-date:
  CF_0: -initial_equity (at acquisition)
  CF_1 through CF_t: actual annual BTCF received
  CF_t (terminal): mark_to_market_value - loan_balance - hypothetical_selling_costs

IRR-to-date = IRR of these cash flows
```

**Worked Example:**

```
Acquisition equity: -$11,480,000 (includes closing costs and capex reserves)
Year 1 BTCF: $285,000
Year 2 BTCF: $420,000
Year 3 BTCF: $580,000
Hypothetical net reversion (today): $16,660,000

CF stream: [-11,480,000, +285,000, +420,000, +580,000 + 16,660,000]
CF stream: [-11,480,000, +285,000, +420,000, +17,240,000]

NPV at 15%: -11,480,000 + 285,000/1.15 + 420,000/1.3225 + 17,240,000/1.5209
           = -11,480,000 + 247,826 + 317,615 + 11,335,067
           = +$420,508 (positive, IRR > 15%)

NPV at 18%: -11,480,000 + 285,000/1.18 + 420,000/1.3924 + 17,240,000/1.6430
           = -11,480,000 + 241,525 + 301,726 + 10,492,997
           = -$443,752 (negative, IRR < 18%)

Converges to IRR-to-date = 16.2%
```

### Interpreting IRR-to-Date

```
IRR-to-date vs original underwritten IRR:
  If IRR_to_date > underwritten_IRR: outperforming (value creation ahead of schedule)
  If IRR_to_date < underwritten_IRR: underperforming (may need course correction)

IRR-to-date vs going-forward IRR:
  If IRR_to_date > going_forward_IRR: the best returns are behind you (SELL signal)
  If IRR_to_date < going_forward_IRR: the best returns are ahead (HOLD signal)
```

### Going-Forward IRR

```
Going-forward IRR treats today's trapped equity as the initial investment:

CF_0: -trapped_equity (today's equity in the deal)
CF_1 through CF_n: projected forward BTCF
CF_n: projected net reversion at planned exit

This is the IRR on equity from this point forward.
```

**Worked Example (continuing):**

```
Trapped equity: -$16,660,000
Year 4 BTCF: $688,000
Year 5 BTCF: $730,000
Year 5 reversion (exit at 5.75% cap on Year 6 NOI of $2,350,000):
  $2,350,000 / 0.0575 = $40,869,565
  Less loan balance at Year 5: -$19,500,000
  Less selling costs (3%): -$1,226,087
  Net reversion: $20,143,478

CF stream: [-16,660,000, +688,000, +730,000 + 20,143,478]
CF stream: [-16,660,000, +688,000, +20,873,478]

NPV at 10%: -16,660,000 + 688,000/1.10 + 20,873,478/1.21
           = -16,660,000 + 625,455 + 17,250,808
           = +$1,216,263 (IRR > 10%)

NPV at 14%: -16,660,000 + 688,000/1.14 + 20,873,478/1.2996
           = -16,660,000 + 603,509 + 16,061,768
           = +$5,277 (IRR is approximately 14%)

Going-forward IRR: ~14.0%
```

**Decision:**
- IRR-to-date: 16.2% (strong execution)
- Going-forward IRR: 14.0% (still attractive)
- Redeployment hurdle: 12% (market CoC for comparable value-add)
- Going-forward > hurdle: HOLD (marginal equity is still earning above alternatives)

---

## 3. Mark-to-Market NAV Estimation

### Three Approaches

**1. Income Approach (Primary)**

```
NAV = (T-12 NOI / market_cap_rate) - outstanding_debt

Market cap rate source: broker comp sales, CoStar analytics, appraisal
Use trailing NOI, NOT budgeted (conservative for reporting)
```

**2. Sales Comp Approach (Validation)**

```
NAV = (price_per_unit from comps * total_units) - outstanding_debt

Price/unit source: recent sales of comparable assets in same submarket
Adjust for: condition, vintage, unit mix, amenity package
```

**3. Replacement Cost Approach (Floor)**

```
NAV = (land_value + replacement_construction_cost - depreciation) - outstanding_debt

Useful as a floor: if income approach value < replacement cost, the asset is likely
undervalued (market is pricing below what it would cost to build new).
```

**Worked Example (all three):**

```
Income approach:
  T-12 NOI: $2,100,000
  Market cap rate (per CoStar, 3 recent comps): 5.50%
  Gross value: $2,100,000 / 0.055 = $38,181,818
  Less debt: -$20,200,000
  NAV (income): $17,981,818

Sales comp approach:
  Comp 1: 180-unit, 2010 vintage, sold at $195,000/unit
  Comp 2: 220-unit, 2006 vintage, sold at $182,000/unit
  Comp 3: 160-unit, 2012 vintage, sold at $205,000/unit
  Adjusted average (2008 vintage, Class B): $192,000/unit
  Gross value: 200 * $192,000 = $38,400,000
  Less debt: -$20,200,000
  NAV (comps): $18,200,000

Replacement cost approach:
  Land value (12 acres * $350,000/acre): $4,200,000
  Construction cost ($185/SF * 185,000 SF): $34,225,000
  Less depreciation (18/50 years straight-line): -$12,321,000
  Gross value: $26,104,000
  Less debt: -$20,200,000
  NAV (replacement): $5,904,000

Reconciliation:
  Income approach: $17,982K (primary -- most relevant for income property)
  Comp approach: $18,200K (validates income approach within 1.2%)
  Replacement cost: $5,904K (well below income value -- confirms no overvaluation risk
    relative to physical asset, and demonstrates significant value above replacement)

Reported NAV: $18,000,000 (midpoint of income and comp, rounded)
```

---

## 4. Cycle Positioning Overlay

### The Four Quadrants

```
                    Rising NOI
                        |
    EXPANSION           |           RECOVERY
    (Hold / Refi)       |           (Buy / Hold)
                        |
  ---- Falling Values --+-- Rising Values ----
                        |
    RECESSION           |           HYPER-SUPPLY
    (Hold / Buy distressed) |       (Sell / De-lever)
                        |
                    Falling NOI
```

### Cycle Phase Indicators

| Indicator | Recovery | Expansion | Hyper-Supply | Recession |
|---|---|---|---|---|
| Vacancy trend | Declining | Low/stable | Rising | High/stable |
| Rent growth | Accelerating | Positive, slowing | Decelerating/negative | Negative/flat |
| New supply | Low | Rising permits | Deliveries peaking | Supply halts |
| Cap rate trend | Compressing | Stable/tight | Expanding | Expanding |
| Debt availability | Loosening | Abundant | Tightening | Restrictive |

### Hold/Sell/Refi by Cycle Phase

**Recovery Phase: HOLD or BUY**
```
- NOI growth accelerating, cap rates compressing
- Going-forward IRR likely exceeds IRR-to-date
- Refinance to lock in low rates if available
- Do NOT sell into a recovery -- you are leaving money on the table
```

**Expansion Phase: HOLD or REFI**
```
- NOI growth positive but decelerating
- Cap rates at or near cycle lows
- Refi to harvest equity (cash-out refi) without selling
  Cash-out refi: lock in appreciation without triggering capital gains
  New loan proceeds = new_appraised_value * LTV - payoff of existing loan
- Monitor forward supply pipeline -- if >3% of stock under construction, prepare to sell
```

**Hyper-Supply Phase: SELL**
```
- New deliveries competing for tenants
- Rent growth flattening or declining
- Cap rates beginning to expand
- Going-forward IRR declining; IRR-to-date likely peaked
- Decision: sell to crystallize gains before cap rate expansion erodes value
- If selling costs are too high or tax exposure too large: hold but de-lever
  (pay down debt to protect DSCR and reduce default risk)
```

**Recession Phase: HOLD or BUY DISTRESSED**
```
- Vacancies elevated, rents declining
- Cap rates expanded (values down)
- Selling now locks in losses
- Hold through the cycle if DSCR is adequate and no covenant breaches
- Deploy capital to buy distressed assets at wide cap rates
- Refinance only if covenant breach is imminent (extend and pretend)
```

---

## 5. Refinance Analysis

### Cash-Out Refi as an Alternative to Sale

```
Refi proceeds = new_appraised_value * new_LTV - existing_loan_payoff - refi_costs

Advantages vs sale:
  1. No capital gains tax (deferred until eventual sale)
  2. No depreciation recapture
  3. Retain property upside
  4. Refi proceeds are tax-free (they are loan proceeds, not income)

Disadvantages vs sale:
  1. Higher debt service reduces forward cash flow
  2. Property risk retained (concentration)
  3. Refi costs: 1-2% of new loan (origination, legal, appraisal, title)
  4. Rate risk if variable rate
```

**Worked Example:**

```
Current mark-to-market: $38,000,000
Existing loan: $20,200,000 at 6.25%, IO, 2 years remaining
New loan terms: 65% LTV, 6.75%, 30yr amort, 5yr term

New loan amount: $38,000,000 * 0.65 = $24,700,000
Cash-out: $24,700,000 - $20,200,000 = $4,500,000
Refi costs: $24,700,000 * 0.015 = $370,500
Net cash-out: $4,129,500

Tax comparison vs sale:
  Sale proceeds (net of costs): $16,660,000
  Capital gains tax (federal + state, ~25%): -$3,080,000
  Depreciation recapture (25% of $1,047,000): -$261,750
  After-tax proceeds from sale: $13,318,250

  Refi cash-out (tax-free): $4,129,500
  Retained equity in property: $13,300,000
  Total: $17,429,500

  Advantage of refi: $4,111,250 in deferred tax value
  (present value depends on assumed tax rate and time to eventual sale)

Post-refi DSCR check:
  Forward NOI: $2,200,000
  New annual debt service: monthly payment * 12
    r = 0.0675/12 = 0.005625
    M = $24,700,000 * [0.005625 * (1.005625)^360] / [(1.005625)^360 - 1]
    M = $24,700,000 * 0.006489 = $160,279/month
    Annual DS = $1,923,348
  DSCR = $2,200,000 / $1,923,348 = 1.144x

  At 1.14x DSCR, this refi is tight. Most lenders require 1.20-1.25x.
  Options: reduce LTV to 60% ($22,800,000 loan, $2,600,000 cash-out,
  DSCR = 1.24x) or negotiate IO period.
```

---

## 6. Decision Tree Summary

```
Step 1: Calculate trapped equity
Step 2: Calculate marginal return on trapped equity (forward CoC)
Step 3: Calculate going-forward IRR (full hold through planned exit)
Step 4: Compare going-forward IRR to redeployment hurdle rate
Step 5: Determine cycle phase
Step 6: Apply decision matrix:

  Going-forward IRR > hurdle AND (Recovery or Expansion): HOLD
  Going-forward IRR > hurdle AND (Hyper-Supply): HOLD but prepare sell package
  Going-forward IRR < hurdle AND (Recovery): HOLD (cycle will improve returns)
  Going-forward IRR < hurdle AND (Expansion): REFI to harvest equity, hold asset
  Going-forward IRR < hurdle AND (Hyper-Supply): SELL
  Going-forward IRR < hurdle AND (Recession): HOLD (selling locks in losses)
  DSCR < 1.15x in any phase: REFI or SELL (survival mode)
```

---

## 7. Common Errors

| Error | Impact | Correction |
|---|---|---|
| Comparing marginal return to original underwritten IRR | Irrelevant comparison -- the original return was earned on original equity, not current trapped equity | Compare to redeployment hurdle rate on current equity |
| Ignoring selling costs in trapped equity calc | Overstates trapped equity by 2-4%, making marginal returns look worse than they are | Always deduct selling costs (2-4% of gross value) |
| Using budgeted NOI for mark-to-market | Overstates NAV if budget is aspirational | Use T-12 actual NOI for NAV calculation; show budget as sensitivity |
| Ignoring tax on sale when comparing to refi | Sale triggers 20-30% in taxes; refi is tax-free. Apples-to-oranges comparison | Always compare after-tax proceeds from sale to tax-free refi cash-out |
| Selling during recession because "returns are low" | Crystallizes losses. The same equity redeployed earns similar low returns in a recession. | Hold through recession unless covenant breach is imminent |
| Refi without DSCR stress test | New, higher debt service may trigger covenant breach in a downturn | Stress-test post-refi DSCR at 200bps above current rates before proceeding |
