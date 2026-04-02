# Tenant Retention NPV Model

---

## Purpose

This reference provides the quantitative framework for evaluating whether to retain a tenant (via concession, TI, or rent reduction) versus letting them vacate and re-leasing the space. The decision should be NPV-driven, not instinct-driven. A GP who automatically fights every vacancy is leaving money on the table; a GP who lets good tenants walk is destroying value.

**Core question**: Is the net present value of retaining this tenant higher than the NPV of the vacancy + re-leasing scenario?

---

## Part 1: Retention NPV Formula

### 1.1 Basic Framework

```
NPV(Retain) = PV of renewal cash flows - PV of retention costs

NPV(Vacate & Re-Lease) = PV of new tenant cash flows - PV of vacancy costs
                          - PV of re-leasing costs

Retention is positive NPV when: NPV(Retain) > NPV(Vacate & Re-Lease)
```

### 1.2 Detailed Formula

**NPV of Retention**:

```
NPV_retain = SUM[ (Renewal_Rent_t - OpEx_t) / (1 + r)^t ] for t = 1 to T
             - TI_concession (upfront)
             - Free_rent_cost (months 1-N)
             - Broker_commission (if applicable)
```

**NPV of Vacancy + Re-Lease**:

```
NPV_vacate = - SUM[ (Carrying_Cost_t) / (1 + r)^t ] for t = 1 to V  (vacancy period)
             - Make_Ready_Cost (upfront)
             - TI_for_New_Tenant (upfront)
             - Broker_Commission_New (upfront)
             + SUM[ (New_Rent_t - OpEx_t) / (1 + r)^t ] for t = V+1 to T
```

### 1.3 Key Variables

| Variable | Definition | Typical Range | Data Source |
|----------|-----------|---------------|------------|
| r | Discount rate | 8-12% | Fund hurdle rate or WACC |
| T | Analysis period (years) | Match to new lease term (5-10 yrs) | |
| Renewal_Rent | Monthly/annual rent under renewal | In-place + escalation | Negotiation |
| New_Rent | Monthly/annual rent from new tenant | Market rent | Broker/comps |
| V | Vacancy months before re-lease | 3-18 months | Market-dependent |
| Carrying_Cost | Monthly cost of vacant space | Taxes + insurance + CAM + utilities + debt service | Actual expenses |
| TI_retain | Tenant improvement allowance for renewal | $0-15/SF (office); $0-5K/unit (MF) | Negotiation |
| TI_new | TI for new tenant | $15-60/SF (office); $5-25K/unit (MF) | Market standard |
| Make_Ready | Cost to prepare space for new tenant | $2-10/SF (office); $2-8K/unit (MF) | PM estimate |
| Commission_retain | Leasing commission on renewal | 2-4% of lease value | Broker agreement |
| Commission_new | Leasing commission on new lease | 4-6% of lease value | Broker agreement |

---

## Part 2: WALT Impact Analysis

### 2.1 What is WALT?

Weighted Average Lease Term (WALT) is the average remaining lease term weighted by each tenant's rent contribution. It measures portfolio cash flow durability.

```
WALT = SUM(Rent_i x Remaining_Term_i) / SUM(Rent_i)
```

### 2.2 Why WALT Matters for Retention

- **Buyers price WALT**: A property with a 6-year WALT commands a tighter cap rate than one with a 2-year WALT. Each year of WALT typically adds 15-30bps of cap rate compression for investment-grade tenants.
- **Lenders underwrite WALT**: Shorter WALT increases rollover risk, which reduces available leverage or increases rates.
- **Retention extends WALT**: Renewing a tenant for 5 years extends that tenant's WALT contribution immediately.

### 2.3 WALT Impact Calculation

**Before renewal** (tenant at expiration):
```
Property has 10 tenants, total rent = $1,000,000/yr
Tenant A: $150,000/yr rent, 0 years remaining
Other 9 tenants: $850,000/yr weighted avg 4.5 years remaining

WALT_before = ($150,000 x 0 + $850,000 x 4.5) / $1,000,000
            = 3.83 years
```

**After renewal** (Tenant A signs 5-year renewal):
```
WALT_after = ($150,000 x 5.0 + $850,000 x 4.5) / $1,000,000
           = 4.58 years
```

**WALT improvement**: +0.75 years

**Cap rate impact** (at 20bps per year of WALT):
```
Value at 5.50% cap (WALT 3.83): $1,000,000 / 0.055 = $18,182,000
Value at 5.35% cap (WALT 4.58): $1,000,000 / 0.0535 = $18,692,000
Value uplift: +$510,000
```

This $510K of value creation from WALT extension should be factored into the retention NPV analysis for assets held for disposition.

---

## Part 3: Worked Example -- 3-Tenant Office Asset

### Scenario Setup

**Property**: 45,000 SF Class B office, suburban NJ
**Total annual rent**: $1,350,000 ($30/SF avg)
**Three tenants** with upcoming lease decisions:

| Tenant | SF | Rent/SF | Annual Rent | % of NR | Lease Expiry | Renewal Likelihood |
|--------|-----|---------|-------------|---------|-------------|-------------------|
| Tenant A (Law Firm) | 20,000 | $32 | $640,000 | 47% | 12 months | High -- embedded in space |
| Tenant B (Insurance Co) | 15,000 | $28 | $420,000 | 31% | 6 months | Medium -- exploring options |
| Tenant C (Tech Startup) | 10,000 | $29 | $290,000 | 21% | 18 months | Low -- outgrowing space |

### Tenant A: Law Firm (20,000 SF) -- Retention Recommended

**Retention offer**: 5-year renewal at $33/SF (3.1% increase), $10/SF TI, 1 month free rent

```
NPV ANALYSIS (r = 9%, T = 5 years)

NPV(Retain):
  Year 1: ($33 x 20,000 - $10/SF TI x 20,000 - 1 month free rent)
           = $660,000 - $200,000 TI - $55,000 free rent = $405,000 (Year 1 net)
  Years 2-5: $660,000/yr + 2.5% annual escalation
  Commission: 3% x $3,462,000 (5yr rent) = $103,860
  PV of 5-year cash flows:                  $2,418,000
  Less TI:                                  -$200,000
  Less free rent:                           -$55,000
  Less commission:                          -$103,860
  NPV(Retain) =                             $2,059,140

NPV(Vacate & Re-Lease):
  Vacancy: 9 months (office vacancy in this submarket = 14.2%)
  Make-ready: $8/SF x 20,000 = $160,000
  New TI: $35/SF x 20,000 = $700,000
  New commission: 5% x $3,600,000 (5yr at $36/SF) = $180,000
  Carrying cost during vacancy: $12/SF x 20,000 / 12 x 9 = $180,000
  New rent: $36/SF (market for new lease)
  PV of new tenant cash flows (starting month 10): $2,280,000
  Less vacancy carrying:                           -$180,000
  Less make-ready:                                 -$160,000
  Less new TI:                                     -$700,000
  Less new commission:                             -$180,000
  NPV(Vacate & Re-Lease) =                        $1,060,000

RETENTION PREMIUM = $2,059,140 - $1,060,000 = $999,140

DECISION: RETAIN. NPV advantage of $999K. Retention is strongly positive.
Even if renewal rent is reduced to $31/SF (flat), NPV(Retain) = $1,850K,
still $790K above NPV(Vacate).
```

### Tenant B: Insurance Company (15,000 SF) -- Retention with Conditions

**Situation**: Tenant is exploring a move to a newer building offering $40/SF TI. Current space needs refresh. Tenant would stay if TI is competitive.

```
NPV ANALYSIS (r = 9%, T = 5 years)

Option 1: Retain at $29/SF with $20/SF TI and 2 months free rent
  PV of cash flows:          $1,631,000
  Less TI ($20 x 15,000):   -$300,000
  Less free rent (2 months): -$72,500
  Less commission (3%):      -$66,000
  NPV(Retain) =              $1,192,500

Option 2: Vacate and re-lease
  Vacancy: 12 months (large block in soft market)
  Make-ready: $10/SF x 15,000 = $150,000
  New TI: $40/SF x 15,000 = $600,000
  New commission: 5% x $2,475,000 = $123,750
  Carrying cost: 12 months x $15,000/mo = $180,000
  New rent: $33/SF (market for new lease, larger block discount)
  PV of new tenant cash flows:  $1,560,000
  Less all costs:               -$1,053,750
  NPV(Vacate) =                 $506,250

RETENTION PREMIUM = $1,192,500 - $506,250 = $686,250

DECISION: RETAIN. But condition the TI on a 7-year renewal term to
improve NPV and WALT. At 7 years, NPV(Retain) increases to $1,780K.
```

### Tenant C: Tech Startup (10,000 SF) -- Let Vacate

**Situation**: Tenant is outgrowing space and needs 18,000 SF. No contiguous space available. Tenant has given informal notice they will not renew.

```
NPV ANALYSIS (r = 9%, T = 5 years)

Option 1: Retain at reduced rent ($26/SF) to fill the space
  PV of cash flows:          $935,000
  Less TI ($5/SF):           -$50,000
  Less commission:           -$39,000
  NPV(Retain) =              $846,000

Option 2: Vacate and re-lease at market
  Vacancy: 6 months (smaller block, easier to fill)
  Make-ready: $6/SF x 10,000 = $60,000
  New TI: $25/SF x 10,000 = $250,000
  New commission: 5% x $1,650,000 = $82,500
  Carrying cost: 6 months x $10,000/mo = $60,000
  New rent: $33/SF (market rate; smaller block = tighter pricing)
  PV of new tenant cash flows:  $1,320,000
  Less all costs:               -$452,500
  NPV(Vacate) =                 $867,500

RETENTION PREMIUM = $846,000 - $867,500 = -$21,500

DECISION: LET VACATE. NPV(Vacate) exceeds NPV(Retain) by $21.5K.
Re-leasing at market rent ($33/SF vs. $26/SF retention) more than
offsets vacancy and re-leasing costs. Additionally, a market-rate
tenant improves the rent roll quality for disposition.
```

### Summary Decision Matrix

| Tenant | SF | % NR | Renewal Rent | Retention NPV | Vacancy NPV | Decision | Retention Premium |
|--------|-----|------|-------------|---------------|-------------|----------|------------------|
| A (Law) | 20K | 47% | $33/SF | $2,059K | $1,060K | Retain | +$999K |
| B (Ins) | 15K | 31% | $29/SF | $1,193K | $506K | Retain (7yr) | +$686K |
| C (Tech) | 10K | 21% | $26/SF | $846K | $868K | Let vacate | -$22K |

**Portfolio WALT impact**:
- If A and B renew (5yr and 7yr): WALT increases from 1.2 years to 4.8 years
- Cap rate impact at 20bps/year: ~70bps compression, +$1.2M estimated value
- Total retention value (NPV premium + WALT value): ~$2.9M

---

## Part 4: Decision Framework

### When to Retain (NPV-Positive Indicators)

| Indicator | Why It Favors Retention |
|-----------|----------------------|
| High vacancy in submarket (>12%) | Vacancy period will be long; carrying cost is high |
| Large space (>10,000 SF) | Harder to fill; fewer qualified tenants |
| Tenant has significant buildout | Tenant is embedded; TI for new tenant would be expensive |
| Short remaining hold period | Cannot afford vacancy before disposition |
| Tenant is credit-worthy | Strengthens rent roll for disposition or refinancing |
| Market rents are flat or declining | New lease may not achieve a premium over renewal |

### When to Let Vacate (NPV-Negative Indicators)

| Indicator | Why It Favors Vacancy |
|-----------|---------------------|
| Market rents significantly above in-place | New lease captures mark-to-market |
| Small space (<5,000 SF) | Quick to re-lease; many tenants in the market |
| Tenant is credit-impaired | Replacing with stronger tenant improves rent roll |
| Long remaining hold period | Time to absorb vacancy and lease at market |
| Space needs reconfiguration | Vacancy allows reposition for higher-value use |
| Tenant demanding excessive TI | Retention cost exceeds re-leasing cost |

### Break-Even Vacancy Period

The maximum vacancy months where NPV(Vacate) still exceeds NPV(Retain):

```
Break-Even Vacancy = (NPV_Retain - NPV_Vacate_at_0_months) / Monthly_Carrying_Cost
```

If the market suggests vacancy will be shorter than this break-even, let the tenant go. If longer, retain.

---

## Part 5: Sensitivity Analysis Template

For each retention decision, run sensitivity on 3 variables:

| Variable | Low | Base | High |
|----------|-----|------|------|
| Vacancy period (months) | [X] | [X] | [X] |
| New lease rent ($/SF) | [X] | [X] | [X] |
| New tenant TI ($/SF) | [X] | [X] | [X] |

| Scenario | NPV(Retain) | NPV(Vacate) | Decision |
|----------|------------|-------------|----------|
| Base case | $[X] | $[X] | [Retain/Vacate] |
| Long vacancy + low rent | $[X] | $[X] | [Retain/Vacate] |
| Short vacancy + high rent | $[X] | $[X] | [Retain/Vacate] |
| Long vacancy + high TI | $[X] | $[X] | [Retain/Vacate] |

The decision should be robust across scenarios. If the answer flips under plausible stress cases, the decision is marginal -- default to retention for risk-averse portfolios.
