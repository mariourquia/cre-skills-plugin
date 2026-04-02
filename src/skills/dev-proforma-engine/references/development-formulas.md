# Development Proforma Formula Reference

Complete derivations, worked examples, and benchmarks for ground-up CRE development. All examples use a baseline 250-unit multifamily development with structured parking in a secondary market.

---

## 1. Land Residual Analysis

### Definition

Land residual value is the maximum a developer can pay for land such that the project still meets the target return. It is derived by working backwards from the stabilized asset value.

### Formula

```
Land_residual = Stabilized_value - Hard_costs - Soft_costs - Financing_costs - Developer_profit

Where:
  Stabilized_value = Stabilized_NOI / Exit_cap_rate
  Developer_profit = Stabilized_value * Target_profit_margin (or target IRR on cost)
```

### Worked Example: 250-Unit Multifamily

```
Step 1: Estimate stabilized value
  Unit mix: 150 x 1BR @ $1,850/mo + 100 x 2BR @ $2,350/mo
  Gross potential rent: (150 * 1,850 * 12) + (100 * 2,350 * 12)
                      = $3,330,000 + $2,820,000 = $6,150,000
  Other income (parking, laundry, pet fees): $225,000
  Gross potential income: $6,375,000
  Vacancy & credit loss (5%): -$318,750
  Effective gross income: $6,056,250
  Operating expenses (40% of EGI): -$2,422,500
  Net operating income: $3,633,750

  Exit cap rate: 5.25%
  Stabilized value = $3,633,750 / 0.0525 = $69,214,286

Step 2: Estimate total development cost (TDC) excluding land
  Hard costs (see Section 6): $42,500,000
  Soft costs (18% of hard): $7,650,000
  Financing costs (interest carry + fees): $5,800,000
  Subtotal: $55,950,000

Step 3: Compute land residual
  Target profit margin: 15% on cost (developer's minimum)

  Method: Stabilized_value = TDC_with_land * (1 + profit_margin)
  69,214,286 = (55,950,000 + Land) * 1.15
  55,950,000 + Land = 69,214,286 / 1.15 = 60,186,336
  Land = 60,186,336 - 55,950,000 = $4,236,336

  Land residual: $4,236,336
  Per unit: $4,236,336 / 250 = $16,945/unit
  Per acre (assuming 3.5 acres): $1,210,382/acre
  Per buildable SF (assuming 275,000 GSF): $15.40/BSF

Step 4: Sensitivity check
  If exit cap widens to 5.75%:
  Stabilized value = $3,633,750 / 0.0575 = $63,195,652
  Land = 63,195,652 / 1.15 - 55,950,000 = -$977,392 (negative -- land is worthless at this cap rate)

  If exit cap tightens to 5.00%:
  Stabilized value = $3,633,750 / 0.05 = $72,675,000
  Land = 72,675,000 / 1.15 - 55,950,000 = $7,245,652
```

### Key Insight

Land residual is extremely sensitive to exit cap rate. A 50bps cap rate move swings land value by $4-8M on a 250-unit project. This is why developers negotiate land options (the right to purchase at a fixed price after entitlements are secured).

---

## 2. Monthly S-Curve Draw Schedule

### Definition

Construction spending follows an S-curve: slow start (mobilization, foundations), acceleration through vertical construction, then tapering during finishes and punch list. The cumulative draw schedule approximates a logistic function.

### S-Curve Formula (Logistic Approximation)

```
Cumulative_draw(t) = TDC_hard / (1 + e^(-k*(t - t_mid)))

Where:
  t = month of construction (0 to T)
  t_mid = midpoint month (typically T/2)
  k = steepness parameter (typically 0.15 to 0.25 for CRE)
  T = total construction duration in months

Monthly draw = Cumulative_draw(t) - Cumulative_draw(t-1)
```

### Worked Example: 24-Month Construction, $42.5M Hard Costs

```
Parameters: T=24, t_mid=12, k=0.20

Month | Cumulative %  | Cumulative $    | Monthly Draw
------|---------------|-----------------|-------------
  1   |   2.1%        |    $893,000     |    $893,000
  2   |   3.5%        |  $1,488,000     |    $595,000
  3   |   5.4%        |  $2,295,000     |    $807,000
  4   |   8.0%        |  $3,400,000     |  $1,105,000
  5   |  11.4%        |  $4,845,000     |  $1,445,000
  6   |  15.8%        |  $6,715,000     |  $1,870,000
  7   |  21.2%        |  $9,010,000     |  $2,295,000
  8   |  27.4%        | $11,645,000     |  $2,635,000
  9   |  34.3%        | $14,578,000     |  $2,933,000
 10   |  41.7%        | $17,723,000     |  $3,145,000
 11   |  49.3%        | $20,953,000     |  $3,230,000
 12   |  56.7%        | $24,098,000     |  $3,145,000
 13   |  63.7%        | $27,073,000     |  $2,975,000
 14   |  70.0%        | $29,750,000     |  $2,677,000
 15   |  75.6%        | $32,130,000     |  $2,380,000
 16   |  80.5%        | $34,213,000     |  $2,083,000
 17   |  84.6%        | $35,955,000     |  $1,742,000
 18   |  88.0%        | $37,400,000     |  $1,445,000
 19   |  90.8%        | $38,590,000     |  $1,190,000
 20   |  93.1%        | $39,568,000     |    $978,000
 21   |  94.9%        | $40,333,000     |    $765,000
 22   |  96.3%        | $40,928,000     |    $595,000
 23   |  97.4%        | $41,395,000     |    $467,000
 24   | 100.0%        | $42,500,000     |  $1,105,000

Peak monthly draw: Month 11 at $3,230,000
Peak construction period: Months 7-15 (60% of hard costs drawn)
```

---

## 3. Interest Carry on Drawn Balance

### Formula

Interest accrues only on the drawn (funded) balance, not the total commitment.

```
Monthly_interest_t = Drawn_balance_t * (annual_rate / 12)
Cumulative_interest = sum(Monthly_interest_1..T)
```

For a construction loan funded pro-rata with draws:

```
Drawn_balance_t = sum(draws_1..t) + sum(capitalized_interest_1..t)
```

Interest is typically capitalized (added to the loan balance) during construction, so interest accrues on interest.

### Worked Example: Interest Carry on $42.5M Draw Schedule

```
Construction loan: 65% of hard costs = $27,625,000 commitment
Rate: SOFR (4.50%) + 3.50% spread = 8.00%
Developer equity funds first 35% ($14,875,000), then loan draws begin.

Equity exhausted at approximately month 8 (cumulative draw = $14,875,000).
Loan draws begin month 9.

Month | Cumulative Draw | Loan Drawn    | Monthly Interest | Cumulative Interest
------|-----------------|---------------|------------------|--------------------
  9   | $14,578,000     | $0 (equity)   | $0               | $0
 10   | $17,723,000     | $2,848,000    | $18,987           | $18,987
 11   | $20,953,000     | $6,078,000    | $40,520           | $59,507
 12   | $24,098,000     | $9,223,000    | $61,487           | $120,994
 13   | $27,073,000     | $12,198,000   | $81,320           | $202,314
 14   | $29,750,000     | $14,875,000   | $99,167           | $301,481
 15   | $32,130,000     | $17,255,000   | $115,033          | $416,514
 16   | $34,213,000     | $19,338,000   | $128,920          | $545,434
 17   | $35,955,000     | $21,080,000   | $140,533          | $685,967
 18   | $37,400,000     | $22,525,000   | $150,167          | $836,134
 19   | $38,590,000     | $23,715,000   | $158,100          | $994,234
 20   | $39,568,000     | $24,693,000   | $164,620          | $1,158,854
 21   | $40,333,000     | $25,458,000   | $169,720          | $1,328,574
 22   | $40,928,000     | $26,053,000   | $173,687          | $1,502,261
 23   | $41,395,000     | $26,520,000   | $176,800          | $1,679,061
 24   | $42,500,000     | $27,625,000   | $184,167          | $1,863,228

Total capitalized interest: $1,863,228
Average drawn balance: approximately $17,200,000
Effective interest rate on commitment: $1,863,228 / $27,625,000 = 6.7% (vs 8.0% coupon)

The 6.7% effective rate reflects that the loan was only partially drawn for most of the period.
With interest capitalization, the final loan balance = $27,625,000 + $1,863,228 = $29,488,228.
```

---

## 4. Development Yield and Spread

### Definitions

```
Development yield = Stabilized NOI / Total development cost (TDC)
Market cap rate = Stabilized NOI / Stabilized market value
Development spread = Development yield - Market cap rate
```

The development spread represents the value created by developing rather than buying a stabilized asset.

### Worked Example

```
Stabilized NOI: $3,633,750
TDC (including land): $55,950,000 + $4,236,336 = $60,186,336
Market cap rate: 5.25%

Development yield = $3,633,750 / $60,186,336 = 6.04%
Development spread = 6.04% - 5.25% = 79bps

Value created:
  Stabilized value: $69,214,286
  TDC: $60,186,336
  Profit: $9,027,950 (15.0% margin on cost)
```

### Minimum Spread Thresholds

| Market Conditions | Minimum Dev Spread | Rationale |
|---|---|---|
| Strong demand, low supply | 75-100bps | Lower risk justifies thinner spread |
| Balanced market | 100-150bps | Standard compensation for execution risk |
| Uncertain/softening | 150-200bps | Higher risk premium needed |
| Distressed | 200bps+ or do not proceed | Execution risk may not justify any spread |

If the development spread falls below 75bps, the risk-adjusted return of buying a stabilized asset likely exceeds development. The developer is taking construction, lease-up, and market timing risk for minimal incremental return.

---

## 5. TDC Per Unit Analysis

### Formula

```
TDC/unit = Total development cost / Number of units

Components:
  Land/unit
  Hard costs/unit
  Soft costs/unit
  Financing costs/unit
  Developer fee/unit (if any)
```

### Worked Example: 250-Unit Breakdown

```
Component                  | Total         | Per Unit
---------------------------|---------------|----------
Land                       | $4,236,336    | $16,945
Hard construction          | $42,500,000   | $170,000
Soft costs                 | $7,650,000    | $30,600
Financing (interest carry) | $1,863,228    | $7,453
Loan fees (1.5%)           | $414,375      | $1,658
Permits & impact fees      | $2,250,000    | $9,000
Developer fee (4% of hard) | $1,700,000    | $6,800
Contingency (5% of hard)   | $2,125,000    | $8,500
Operating reserve (3 mo)   | $605,625      | $2,423
Marketing/lease-up         | $500,000      | $2,000
---------------------------|---------------|----------
Total development cost     | $63,844,564   | $255,378

TDC/unit: $255,378
```

### Market Benchmarks (Secondary Market, 2025-2026)

| Product Type | TDC/Unit Range | TDC/SF Range |
|---|---|---|
| Garden-style MF (wood frame) | $180,000-$240,000 | $180-$240 |
| Mid-rise MF (5 stories, podium) | $250,000-$350,000 | $250-$350 |
| High-rise MF (20+ stories) | $400,000-$600,000 | $400-$600 |
| Student housing | $120,000-$180,000 | $160-$220 |
| Senior living (IL/AL) | $200,000-$300,000 | $250-$350 |
| Build-to-rent (SFR) | $250,000-$350,000 | $150-$200 |

Our 250-unit example at $255,378/unit falls within mid-rise podium construction range.

---

## 6. Development Sources and Uses

### Full 250-Unit Proforma

```
USES OF FUNDS
------------------------------------------------------------
Land acquisition                           $4,236,336
Hard construction costs                   $42,500,000
  Site work & foundations                   $4,250,000
  Vertical construction (structure)        $12,750,000
  Building envelope                         $5,100,000
  MEP (mechanical/electrical/plumbing)      $8,500,000
  Interior finishes                         $6,375,000
  Parking structure                         $3,400,000
  Common areas & amenities                  $2,125,000
Soft costs                                 $7,650,000
  Architecture & engineering                $2,550,000
  Legal                                       $425,000
  Accounting                                  $212,500
  Insurance (builder's risk)                  $637,500
  Property taxes during construction          $425,000
  Environmental/geotech                       $212,500
  Inspections & testing                       $425,000
  Soft cost contingency                     $2,762,000
Financing costs                            $2,277,603
  Construction loan interest carry          $1,863,228
  Loan origination fee (1.5%)                $414,375
Permits & impact fees                      $2,250,000
Developer fee                              $1,700,000
Hard cost contingency (5%)                 $2,125,000
Operating reserve (3 months)                 $605,625
Marketing & lease-up                         $500,000
------------------------------------------------------------
TOTAL USES                                $63,844,564

SOURCES OF FUNDS
------------------------------------------------------------
Construction loan (65% LTC)               $41,499,000
  Commitment: $41,499,000
  Drawn at completion: ~$29,488,228
  Unfunded reserve: ~$12,011,000
Developer equity (35% LTC)               $22,345,564
  GP co-invest (10% of equity)             $2,234,556
  LP equity (90% of equity)               $20,111,008
------------------------------------------------------------
TOTAL SOURCES                             $63,844,564
```

---

## 7. Lease-Up and Stabilization

### Absorption Rate

```
Monthly absorption = Total units * Absorption rate per month

Typical MF absorption: 15-25 units/month in strong markets, 8-15 in moderate markets.

250 units at 20 units/month:
  Time to 95% occupancy (238 units): 238 / 20 = 11.9 months ≈ 12 months
  Add 2-3 months for certificate of occupancy phasing
  Total lease-up: 14-15 months from first unit delivery
```

### Lease-Up NOI Ramp

```
Month | Occupied | EGI (monthly)  | OpEx (monthly) | NOI (monthly)
------|----------|----------------|----------------|---------------
  1   |    20    |    $43,500     |   $130,000     |  -$86,500
  3   |    60    |   $130,500     |   $155,000     |  -$24,500
  6   |   120    |   $261,000     |   $185,000     |   $76,000
  9   |   180    |   $391,500     |   $195,000     |  $196,500
 12   |   238    |   $517,350     |   $200,000     |  $317,350
 15   |   238    |   $517,350     |   $202,000     |  $315,350

Note: OpEx has a large fixed component (property management, insurance, taxes)
that does not scale linearly with occupancy. This creates negative NOI during
early lease-up even with occupied units paying rent.

Stabilized monthly NOI (at 95% occupancy): ~$303,000
Stabilized annual NOI: $3,633,750
```

### Concessions During Lease-Up

```
Typical lease-up concessions:
  1-2 months free rent on 12-month leases
  Reduced security deposits
  Free parking or amenity credits

Impact on effective rent:
  Gross rent: $1,850/month
  1 month free on 12-month lease: $1,850 / 12 = $154 concession/month
  Effective rent: $1,850 - $154 = $1,696/month (8.3% discount)

Concessions typically burn off as occupancy reaches 85-90%.
Total concession cost for 250-unit lease-up: approximately $350,000-$500,000.
```

---

## 8. Return Metrics Summary

### Developer IRR Calculation

```
Cash flow timeline:
  Month 0:       -$22,345,564 (equity invested)
  Months 1-24:   $0 (construction period, all costs funded by loan + equity)
  Months 25-36:  Lease-up period. Net CF after debt service: -$150K to +$100K/month
  Months 37-60:  Stabilized. Net CF: ~$120K/month after perm loan DS
  Month 60:      Reversion (sale at 5.25% cap on forward NOI)

  Forward NOI (year 6): $3,633,750 * 1.03^2 = $3,856,068
  Sale price: $3,856,068 / 0.0525 = $73,449,000
  Less selling costs (2%): -$1,469,000
  Less perm loan payoff: -$42,000,000 (approx)
  Net reversion to equity: $29,980,000

  Developer levered IRR: approximately 15-18% (depending on lease-up pace)
  Equity multiple: $29,980,000 + ~$3,500,000 CF / $22,345,564 = 1.50x
```

### Yield-on-Cost vs. Development Spread

```
Yield on cost = Stabilized NOI / TDC = $3,633,750 / $63,844,564 = 5.69%
Market cap rate: 5.25%
Development spread: 44bps (thinner than the 79bps calculated earlier because
  TDC now includes developer fee, contingency, and reserves)

This spread is below the 75bps minimum threshold for strong markets.
The developer should either:
  (a) Reduce land cost (negotiate harder)
  (b) Value-engineer hard costs
  (c) Increase rents (better amenities, location premium)
  (d) Walk away if none of the above are achievable
```
