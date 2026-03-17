# Budget-to-Value Linkage Reference

How operating expense variances flow through to property value, reserve adequacy testing, and the IC presentation of opex risk. Every dollar of opex overrun destroys value at the inverse of the cap rate.

---

## 1. The Opex-to-Value Transmission Mechanism

### Core Identity

```
Property value = NOI / cap_rate
NOI = EGI - OpEx
```

Therefore:

```
dValue/dOpEx = -1 / cap_rate
```

A $1 increase in annual opex reduces property value by $1/cap_rate. This is the single most important relationship in asset management budgeting.

### Value Destruction Table

| Cap Rate | Value Impact per $1 OpEx Overrun | Value Impact per $1/SF OpEx Overrun (100K SF) |
|---|---|---|
| 4.0% | -$25.00 | -$2,500,000 |
| 4.5% | -$22.22 | -$2,222,222 |
| 5.0% | -$20.00 | -$2,000,000 |
| 5.5% | -$18.18 | -$1,818,182 |
| 6.0% | -$16.67 | -$1,666,667 |
| 6.5% | -$15.38 | -$1,538,462 |
| 7.0% | -$14.29 | -$1,428,571 |

### Worked Example: Insurance Overrun

```
Property: 200-unit multifamily, 185,000 SF
Cap rate: 5.5%
Budgeted insurance: $163,020 ($0.88/SF)
Actual insurance (post-renewal): $198,000 ($1.07/SF)
Variance: +$34,980 ($0.19/SF)

Value impact:
  $34,980 / 0.055 = -$636,000 of property value destroyed
  On a $26M property, that is a -2.4% value hit from one line item

Per-unit impact:
  $34,980 / 200 units = $175/unit opex overrun
  $175 / 0.055 = -$3,182/unit of value destroyed
```

### Cumulative Variance Impact

When multiple lines miss budget simultaneously (which they often do -- insurance, tax, and utilities tend to co-move in inflationary environments):

```
Scenario: 3 lines over budget
  Insurance: +$35,000
  Property tax: +$22,000
  Utilities: +$18,000
  Total overrun: +$75,000

Value destruction at 5.5% cap: $75,000 / 0.055 = -$1,363,636
On a $26M property: -5.2% value decline from opex alone
```

This is why institutional owners treat budget variance as a valuation event, not just an accounting exercise.

---

## 2. Opex Ratio as a Valuation Lever

### Definition

```
Opex ratio = total_operating_expenses / EGI
NOI margin = 1 - opex_ratio
```

### Sensitivity Analysis

For a property with $3,500,000 EGI at a 5.5% cap rate:

| Opex Ratio | NOI | Value | Value Change from 55% Base |
|---|---|---|---|
| 50% | $1,750,000 | $31,818,182 | +$3,181,818 |
| 52% | $1,680,000 | $30,545,455 | +$1,909,091 |
| 55% | $1,575,000 | $28,636,364 | -- (base) |
| 58% | $1,470,000 | $26,727,273 | -$1,909,091 |
| 60% | $1,400,000 | $25,454,545 | -$3,181,818 |

A 5-point swing in opex ratio moves value by $6.4M on a $28.6M property. This is why best-in-class operators obsess over controllable opex.

### Controllable vs Non-Controllable Split

```
Controllable opex: payroll, R&M, marketing, contracts, admin, management fee
  Operator can influence through staffing, vendor negotiation, efficiency
  Typical: 55-65% of total opex

Non-controllable opex: property tax, insurance, utilities (rate component)
  Driven by external forces
  Typical: 35-45% of total opex

Value creation focus: controllable opex.
  A 200bps improvement in controllable opex ratio on $3.5M EGI:
  = $3,500,000 * 0.02 = $70,000 NOI improvement
  = $70,000 / 0.055 = $1,272,727 value creation
```

---

## 3. Reserve Adequacy Testing

### ASHRAE Expected Useful Life (EUL) Tables -- Major Systems

| Component | EUL (Years) | Replacement Cost (per unit, MF) | Replacement Cost (per SF, office) |
|---|---|---|---|
| Roof (built-up/TPO) | 20-25 | $1,500-2,500 | $8-15 |
| HVAC -- packaged units | 15-20 | $4,000-6,000 | $12-20 |
| HVAC -- central plant chiller | 20-25 | N/A | $15-25 |
| HVAC -- boiler | 25-35 | $2,000-3,500 | $8-15 |
| Elevator (hydraulic) | 20-25 | N/A | $150,000-250,000 per cab |
| Elevator (traction) | 25-30 | N/A | $200,000-350,000 per cab |
| Parking lot (asphalt) | 15-20 | $800-1,200 | $3-5 |
| Parking structure | 30-40 | N/A | $15-25 per stall |
| Plumbing -- risers/mains | 40-50 | $3,000-5,000 | $5-10 |
| Plumbing -- fixtures | 20-25 | $1,200-2,000 | $3-6 |
| Electrical -- switchgear | 30-40 | N/A | $5-10 |
| Windows (commercial) | 25-35 | $2,000-3,500 | $15-30 |
| Exterior envelope/siding | 25-40 | $1,500-3,000 | $8-15 |
| Flooring (common area) | 7-12 | $500-1,000 | $3-8 |
| Appliances (MF) | 10-15 | $2,500-4,000 | N/A |
| Fire suppression/alarm | 20-25 | $800-1,500 | $3-6 |

### Reserve Calculation Methodology

Two approaches: straight-line and present-value.

**Straight-Line (Simple)**

```
Annual reserve per component = replacement_cost / EUL

Example: 200-unit MF, built 2008 (18 years old in 2026)

Roof (200 units, 185,000 SF):
  Replacement cost: $1,850,000
  EUL: 22 years
  Age: 18 years
  Remaining life: 4 years
  Annual reserve: $1,850,000 / 22 = $84,091/year
  CRITICAL: Only 4 years remaining. Reserve should already hold:
    $84,091 * 18 = $1,513,636
  If actual reserve is $600,000, shortfall = $913,636

HVAC (200 packaged units):
  Replacement cost: $5,000/unit * 200 = $1,000,000
  EUL: 18 years
  Age: 18 years (at end of life)
  Annual reserve: $1,000,000 / 18 = $55,556/year
  Status: REPLACEMENT IMMINENT -- should be fully funded

Appliances:
  Replacement cost: $3,200/unit * 200 = $640,000
  EUL: 12 years
  Age: assume 6 years avg (staggered replacement)
  Annual reserve: $640,000 / 12 = $53,333/year

Total annual reserve (all components):
  Roof:        $84,091
  HVAC:        $55,556
  Appliances:  $53,333
  Plumbing:    $35,000
  Parking:     $22,000
  Flooring:    $18,000
  Fire/safety: $14,000
  Total:      $281,980/year ($1,410/unit)
```

**Present-Value (Institutional)**

```
PV reserve = replacement_cost / (1 + discount_rate)^years_to_replacement

Example: Roof replacement in 4 years at 6% discount rate
  PV = $1,850,000 / (1.06)^4 = $1,850,000 / 1.2625 = $1,465,347

Required annual contribution to fully fund:
  PMT = FV * r / [(1+r)^n - 1]
  PMT = $1,850,000 * 0.06 / [(1.06)^4 - 1]
  PMT = $111,000 / 0.2625
  PMT = $422,857/year for 4 years

This is materially higher than the straight-line $84,091 because the roof is near end-of-life.
The straight-line method is adequate for young assets; the PV method is required for aging assets with near-term replacements.
```

---

## 4. Reserve-to-Valuation Relationship

### How Underfunded Reserves Destroy Value

Underfunded reserves are a hidden liability. A buyer performing due diligence will deduct the reserve shortfall from the offer price, effectively capitalizing deferred maintenance at a 1:1 ratio (not at the cap rate, because it is a certain near-term cost, not an ongoing income stream).

```
Offer price adjustment:
  Stabilized value (income approach): $26,000,000
  Reserve shortfall (per PCA): -$1,200,000
  Adjusted offer: $24,800,000

Note: the shortfall is deducted dollar-for-dollar, NOT capitalized.
This is worse than an opex overrun, which is capitalized at 1/cap_rate.
A $1 reserve shortfall costs exactly $1 of value.
A $1 opex overrun costs $16-25 of value.
```

### Lender Reserve Requirements

| Lender Type | Reserve Requirement | Typical Amount | Escrow? |
|---|---|---|---|
| Agency (Fannie/Freddie) | Replacement reserves | $250-350/unit/year | Yes, monthly escrow |
| CMBS | Replacement + TI/LC (office) | $300-500/unit or $0.25-0.50/SF | Yes, monthly escrow |
| Bank | Often negotiable | $200-400/unit | Sometimes |
| Bridge/mezzanine | Varies, often none | Negotiated | Rare |
| Life company | Conservative | $300-450/unit | Yes |

### Adequacy Test

```
Reserve adequacy ratio = funded_reserves / total_PV_of_near_term_replacements

Where near_term = components with remaining life < 5 years

Interpretation:
  > 1.0x: fully funded (rare -- indicates conservative prior management)
  0.7-1.0x: adequate (normal range for well-managed assets)
  0.5-0.7x: underfunded (needs catch-up contributions or capex line item)
  < 0.5x: critically underfunded (DD red flag, price adjustment required)

Worked example (200-unit MF):
  Near-term replacements (< 5 years):
    Roof: $1,850,000 (4 years)
    HVAC (50 units end-of-life): $250,000 (1-2 years)
    Parking resurface: $180,000 (3 years)
    Total: $2,280,000

  Funded reserves: $1,100,000
  Adequacy ratio: $1,100,000 / $2,280,000 = 0.48x (critically underfunded)

  Action: Budget $400K+/year in catch-up reserves or model as Year 1-3 capex
```

---

## 5. Budget Variance and Disposition Timing

### The Compounding Effect

Budget misses compound because buyers underwrite forward NOI. If T-12 NOI is depressed by opex overruns, the buyer's broker-estimated value drops by the overrun capitalized at exit cap.

```
Scenario: planned disposition in 18 months

Budgeted NOI: $1,430,000
Actual NOI (T-12): $1,355,000 (opex overruns of $75,000)
Exit cap rate: 5.75%

Value at budgeted NOI: $1,430,000 / 0.0575 = $24,869,565
Value at actual NOI:   $1,355,000 / 0.0575 = $23,565,217
Value gap: -$1,304,348

The $75,000 annual opex overrun cost $1.3M at disposition.
This is the leverage of the cap rate on operating performance.
```

### Pre-Disposition Budget Strategy

12-18 months before planned sale:
1. Shift discretionary R&M to capex (below the NOI line)
2. Accelerate lease renewals to lock in higher rents
3. Reduce vacancy through concessions (temporary hit to effective rent, but higher occupancy improves T-12 NOI)
4. Renegotiate contracts expiring in the window
5. Ensure reserves are at lender-required minimums (buyer's lender will check)

---

## 6. Common Errors

| Error | Impact | Correction |
|---|---|---|
| Treating opex variance as a P&L issue only | Misses the 15-25x capitalization effect on value | Present variance as both a cash flow AND valuation event |
| Straight-line reserves on aging assets | Understates near-term capital needs by 3-5x | Use PV method for any component with <5yr remaining life |
| Ignoring reserve shortfall in acquisition pricing | Overpays by the shortfall amount | Deduct reserve shortfall dollar-for-dollar from offer |
| Budgeting reserves at lender minimum only | Lender minimums ($250-350/unit) rarely cover actual replacement needs ($500-800/unit for aging stock) | Budget reserves to PCA-indicated need, not lender floor |
| Classifying capex as opex (or vice versa) | Opex hits NOI and value; capex does not. Misclassification distorts both NOI and reserve balances | Follow GAAP capitalization threshold ($5K-15K per item, extends useful life by >1 year) |
| Presenting budget variance without value context | IC/LP sees "$75K overrun" as modest; misses that it implies $1.3M value destruction | Always translate variance to value impact: variance / cap_rate |
| Assuming reserves earn 0% return | Overstates required contributions | Model reserve fund earning money market rate (4-5% in 2025) |
