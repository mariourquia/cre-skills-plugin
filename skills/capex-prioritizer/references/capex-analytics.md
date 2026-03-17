# CapEx Prioritization Analytics Reference

Project-level IRR/NPV analysis, interaction effects for bundled projects, residual value at disposition, DSCR/LTV impact modeling, replacement cost benchmarking, and deferral cost quantification. Worked example: 5 projects totaling $800K.

---

## 1. Project-Level Return Analysis: IRR and NPV, Not ROI

### Why Not ROI

Simple ROI (gain / cost) ignores the time value of money. A $200K project that generates $50K/year in NOI improvement has a "5-year ROI" of 125%, but that ignores when the cash flows arrive. IRR and NPV account for timing.

### Project-Level NPV

```
NPV = sum_{t=0}^{n} CF_t / (1 + r)^t

Where:
  CF_0 = -project_cost (capex outlay)
  CF_t = incremental_NOI_improvement in year t (net of any ongoing maintenance cost)
  CF_n also includes residual_value_at_disposition (the capitalized value of the NOI improvement)
  r = discount rate (typically the property's levered cost of capital or target IRR, 8-12%)
```

### Project-Level IRR

```
IRR = rate where NPV = 0

For a single capex project:
  CF_0 = -capex
  CF_1 through CF_n = incremental annual NOI
  CF_n += residual_value = incremental_NOI_at_exit / exit_cap_rate
```

### Worked Example: Unit Interior Renovation

```
Project: Renovate 40 units (of 200), $15,000/unit
Total cost: $600,000
Renovation timeline: 6 months (staggered, 7 units/month)
Rent premium: $225/month per renovated unit
Annual incremental revenue: 40 * $225 * 12 = $108,000
Vacancy during renovation: 3 months avg per unit
  Lost rent: 40 * $1,475 * 3 / 12 = $14,750 (partial year, annualized across reno period)
Incremental opex (higher-quality finishes, slightly more maintenance): $400/unit/year = $16,000
Net annual NOI improvement (stabilized): $108,000 - $16,000 = $92,000
Year 1 NOI improvement (partial -- 6 months of lease-up): $46,000

Hold period remaining: 4 years
Exit cap rate: 5.75%
Discount rate: 10%

Cash flows:
  Year 0: -$600,000
  Year 1: +$46,000 (partial year)
  Year 2: +$92,000
  Year 3: +$92,000
  Year 4: +$92,000 + residual value

Residual value at Year 4:
  Incremental NOI at exit (Year 5 forward): $92,000 * 1.03 = $94,760 (3% growth)
  Capitalized value: $94,760 / 0.0575 = $1,648,000
  (This is the incremental value the renovation adds to the property at sale)

Year 4 total: $92,000 + $1,648,000 = $1,740,000

NPV at 10%:
  = -600,000 + 46,000/1.10 + 92,000/1.21 + 92,000/1.331 + 1,740,000/1.4641
  = -600,000 + 41,818 + 76,033 + 69,121 + 1,188,414
  = +$775,386

IRR: solve for rate where NPV = 0
  At 40%: -600,000 + 32,857 + 46,939 + 33,528 + 455,440 = -$31,236 (negative)
  At 38%: -600,000 + 33,333 + 48,295 + 35,010 + 483,632 = +$270 (approximately zero)
  Project IRR: ~38%
```

---

## 2. Interaction Effect Analysis for Bundled Projects

### The Problem

CapEx projects interact. Renovating unit interiors AND upgrading the fitness center AND improving curb appeal are not independent -- they compound to support higher rents that no single project would achieve alone. Conversely, some projects cannibalize each other's returns.

### Methodology

```
Step 1: Calculate standalone NPV for each project independently
Step 2: Calculate combined NPV for bundled projects (with interaction effects on rent premium)
Step 3: Interaction effect = combined_NPV - sum_of_standalone_NPVs

Positive interaction: combined > sum of parts (synergy)
Negative interaction: combined < sum of parts (diminishing returns)
```

### Worked Example: Three Interacting Projects

```
Project A: Unit interiors ($600K, $225/mo rent premium standalone)
Project B: Fitness center upgrade ($80K, $25/mo rent premium standalone)
Project C: Curb appeal / landscaping ($45K, $10/mo rent premium standalone)

Standalone rent premiums (per renovated unit):
  A only: $225/mo
  B only: $25/mo (applies to all 200 units)
  C only: $10/mo (applies to all 200 units)

Bundled rent premiums (interaction):
  A + B + C combined: $280/mo per renovated unit (not $260)
  The $20/mo synergy occurs because renovated interiors + new amenities + curb appeal
  collectively reposition the property to a higher submarket comp set.
  The premium on unrenovated units also rises to $40/mo (B + C effect, plus halo)

Standalone annual NOI improvements:
  A: $92,000 (40 renovated units * $225 * 12 - $16K opex)
  B: $60,000 (200 units * $25 * 12) -- minimal incremental opex
  C: $24,000 (200 units * $10 * 12)
  Standalone total: $176,000

Bundled annual NOI improvement:
  Renovated 40 units: $280/mo * 40 * 12 = $134,400
  Unrenovated 160 units: $40/mo * 160 * 12 = $76,800
  Less incremental opex: -$22,000 (interiors + gym + landscape maint)
  Bundled total: $189,200

Interaction effect (annual): $189,200 - $176,000 = +$13,200/year
Capitalized interaction value at 5.75%: $13,200 / 0.0575 = $229,565
```

---

## 3. Residual Value at Disposition

### The Critical Concept

For income properties, a CapEx project's value is NOT the cost of the improvement. It is the capitalized value of the NOI stream it creates. A $100K project that increases NOI by $8K/year is worth $8K/0.055 = $145K in property value at a 5.5% cap -- a 45% value creation above cost.

```
Residual value at disposition = incremental_NOI_at_exit / exit_cap_rate

Value creation = residual_value - project_cost
Value creation margin = (residual_value - project_cost) / project_cost
```

### Depreciation of CapEx Value

Not all CapEx maintains full residual value at disposition. The buyer will discount for remaining useful life.

```
Depreciation adjustment:
  If project EUL is 15 years and disposition is in 4 years:
  Remaining life at exit: 11 years
  Buyer's value = full_residual * (remaining_life / EUL) for short-lived items
  (This is approximate; a more precise calculation discounts the remaining useful cash flows)

Example: $80K fitness equipment upgrade, 10-year EUL, disposition in 4 years
  Remaining life at exit: 6 years
  Full residual (if new): $60,000/yr NOI improvement / 0.0575 = $1,043,478
  Adjusted residual: $1,043,478 * (6/10) = $626,087
  (Buyer knows they'll need to replace equipment in 6 years)
```

### Long-Lived vs Short-Lived CapEx

| CapEx Type | EUL | Residual Value at Exit (4yr hold) | Value Creation Potential |
|---|---|---|---|
| Roof replacement | 20-25 yr | High (16-21yr remaining) | Limited (maintenance capex, not value-add) |
| HVAC replacement | 15-20 yr | High (11-16yr remaining) | Limited (maintenance) |
| Unit renovation | 10-15 yr | Moderate (6-11yr remaining) | High (rent premium) |
| Fitness center | 8-12 yr | Moderate (4-8yr remaining) | Moderate |
| Appliances | 10-15 yr | Moderate | Moderate |
| Technology/access | 5-7 yr | Low (1-3yr remaining) | Moderate but short-lived |
| Cosmetic/paint | 3-5 yr | Low | Low (must be refreshed) |

---

## 4. DSCR and LTV Impact Pre/Post CapEx

### DSCR Impact

```
Pre-capex DSCR = current_NOI / annual_debt_service
Post-capex DSCR = (current_NOI + incremental_NOI) / annual_debt_service

If capex is debt-financed (draw on line of credit or supplemental loan):
  Post-capex DSCR = (current_NOI + incremental_NOI) / (existing_DS + new_DS)
```

### LTV Impact

```
Pre-capex LTV = loan_balance / (current_NOI / cap_rate)
Post-capex LTV = loan_balance / ((current_NOI + incremental_NOI) / cap_rate)

If capex is financed: numerator increases too.
  Post-capex LTV = (existing_loan + capex_loan) / ((current_NOI + incremental_NOI) / cap_rate)
```

**Worked Example:**

```
Pre-capex:
  NOI: $2,100,000
  Debt service: $1,512,000
  Loan balance: $20,200,000
  Property value: $2,100,000 / 0.055 = $38,181,818
  DSCR: 1.389x
  LTV: 52.9%

Post-capex ($725K total, funded from reserves/equity):
  Incremental NOI: $189,200 (bundled projects)
  New NOI: $2,289,200
  Debt service: $1,512,000 (unchanged -- funded from equity)
  Property value: $2,289,200 / 0.055 = $41,621,818
  DSCR: 1.514x (improved)
  LTV: 48.5% (improved)

Post-capex ($725K financed via supplemental loan at 7.5%, 10yr amort):
  New debt: $725,000
  New annual debt service: $725,000 * 0.1424 = $103,240 (debt constant for 10yr, 7.5%)
  Total debt service: $1,512,000 + $103,240 = $1,615,240
  DSCR: $2,289,200 / $1,615,240 = 1.417x (still improved)
  LTV: ($20,200,000 + $725,000) / $41,621,818 = 50.3%
```

---

## 5. Replacement Cost Benchmarking

### Methodology

Compare proposed capex cost to current market replacement costs using RSMeans, Marshall & Swift, or contractor bids.

```
Replacement cost ratio = proposed_cost / market_benchmark_cost

< 0.85: potentially under-scoped or low-quality materials
0.85-1.10: reasonable range
1.10-1.25: premium pricing, justify with quality or timeline
> 1.25: overpaying -- rebid or value-engineer
```

### Benchmark Costs (2025-2026, National Average)

| Project Type | Cost Per Unit (MF) | Cost Per SF (Office) | Source |
|---|---|---|---|
| Unit interior renovation (mid) | $12,000-18,000 | N/A | NAA, actual portfolios |
| Unit interior renovation (high) | $20,000-30,000 | N/A | NAA |
| HVAC replacement (packaged) | $4,500-7,000 | $12-22 | RSMeans |
| Roof replacement (TPO) | N/A | $8-15 | RSMeans |
| Roof replacement (per unit equiv) | $1,800-3,000 | N/A | contractor bids |
| Fitness center buildout | $40-80/SF | $40-80/SF | design-build bids |
| Parking lot resurface | $3-6/SF | $3-6/SF | RSMeans |
| Elevator modernization | $150,000-250,000/cab | $150,000-250,000/cab | KONE/Otis bids |
| Common area renovation | $30-60/SF | $30-60/SF | GC bids |
| Landscaping upgrade | $8,000-15,000/acre | N/A | landscape contractor bids |
| Smart lock/access system | $350-600/unit | $8-15/SF | vendor quotes |
| In-unit washer/dryer | $1,800-2,500/unit | N/A | appliance suppliers |

---

## 6. "Do Nothing" Deferral Cost Quantification

### The Hidden Cost of Deferral

Every year a needed capex project is deferred, three costs accumulate:

```
Total deferral cost = lost_NOI + accelerated_deterioration + disposition_discount

1. Lost NOI:
   Foregone rent premium that the improvement would generate.
   For unit renovations: $225/mo * 40 units * 12 = $108,000/year

2. Accelerated deterioration:
   Aging systems fail more frequently, increasing R&M.
   Rule of thumb: R&M increases 8-15% per year for systems past EUL.
   HVAC past EUL: additional $400-800/unit/year in emergency repairs.

3. Disposition discount:
   Buyer deducts deferred capex from offer price, often at 1.2-1.5x the actual cost
   (to account for execution risk, timeline disruption, and their required return on capex).
   $600K renovation cost deducted at 1.3x = $780K price reduction.
```

### Deferral Cost Worked Example

```
Project: 40-unit interior renovation, $600K cost, deferred 2 years

Year 1 deferral costs:
  Lost rent premium: 40 * $225 * 12 = $108,000
  Avoided capex: +$600,000 (cash not spent)
  Net Year 1: saved $600K but lost $108K income

Year 2 deferral costs:
  Lost rent premium: $108,000 (another year)
  Increased R&M (aging interiors): $200/unit * 40 = $8,000
  Total Year 2 loss: $116,000

Cumulative 2-year deferral impact:
  Total lost income: $108,000 + $116,000 = $224,000
  Capitalized lost income: $224,000 is 2 years of NOI gap
  Value impact: $108,000 (stabilized annual loss) / 0.055 = $1,963,636
    The property is worth $1.96M less EACH YEAR the renovation is deferred

  But: you retained $600K cash for 2 years. At 5% reinvestment rate: $600K * 1.05^2 - $600K = $61,500

  Net cost of 2-year deferral: $224,000 - $61,500 = $162,500 in lost cash flow
  Plus: value destruction of $1.96M (ongoing until renovated)
```

---

## 7. Worked Example: 5-Project Prioritization ($800K Total)

### Project Summary

| ID | Project | Cost | Incremental NOI | Standalone IRR | Standalone NPV (10%) |
|---|---|---|---|---|---|
| A | Unit interiors (40 units) | $600,000 | $92,000/yr | 38% | $775,386 |
| B | Fitness center upgrade | $80,000 | $60,000/yr | 85% | $682,000 |
| C | Curb appeal / landscaping | $45,000 | $24,000/yr | 62% | $265,000 |
| D | Smart lock system (200 units) | $90,000 | $18,000/yr | 24% | $148,000 |
| E | Parking lot resurface | $75,000 | $0/yr (maintenance) | N/A | -$75,000 |
| | **Total** | **$890,000** | | | |

Budget constraint: $800,000. Must choose a subset.

### Step 1: Rank by NPV (Not IRR)

IRR ranking: B > C > A > D > E
NPV ranking: A > B > C > D > E

IRR favors small, high-return projects. NPV favors total value creation. For wealth maximization with a fixed budget, use NPV.

### Step 2: Check Interactions

A + B + C bundled NPV: $775,386 + $682,000 + $265,000 + interaction = $1,722,386 + $229,565 = $1,951,951
Cost: $725,000

A + B + C + D bundled: additional $18K/yr NOI, but smart locks also reduce turnover cost by $5K/yr
Adjusted D standalone NPV with A: $148,000 + $45,000 (turnover interaction) = $193,000
Bundle A+B+C+D cost: $815,000 (over budget by $15K)

### Step 3: Check Mandatory Projects

Project E (parking resurface) has zero NOI impact but is a safety/liability issue. If deferred:
- Pothole claims: $5,000-15,000/year in liability exposure
- Disposition deduction: buyer will deduct $75K * 1.3 = $97,500 from offer

If parking is mandatory, remaining budget: $800K - $75K = $725K.

### Step 4: Optimal Bundle

```
Option 1: A + B + C + E = $600K + $80K + $45K + $75K = $800K
  Combined NPV: $1,951,951 + (-$75,000) = $1,876,951
  Bundled NOI improvement: $189,200

Option 2: A + B + D + E = $600K + $80K + $90K + $75K = $845K (over budget)

Option 3: A + B + C (skip E, accept parking risk) = $725K
  Combined NPV: $1,951,951
  Remaining budget: $75K for contingency

Recommendation: Option 1 -- all value-add projects plus mandatory parking.
  Total investment: $800,000
  Annual NOI improvement: $189,200
  Value creation: $189,200 / 0.055 = $3,440,000
  Investment multiple: $3,440,000 / $800,000 = 4.3x
  Post-capex DSCR improvement: +12.5bps (from 1.389x to 1.514x)
```

---

## 8. Common Errors

| Error | Impact | Correction |
|---|---|---|
| Using simple ROI instead of IRR/NPV | Ignores time value, renovation downtime, and residual value. Overstates returns on slow projects, understates fast ones. | Always use NPV for ranking and IRR for communication. |
| Ranking by IRR instead of NPV | Small, high-IRR projects ($10K at 100% IRR) are ranked above large value-creation projects ($600K at 38% IRR). | Rank by NPV for capital allocation. Use IRR as a secondary metric. |
| Ignoring interaction effects | Understates value of complementary projects and may lead to suboptimal bundle selection. | Model bundled rent premiums from comp analysis, not sum of standalone premiums. |
| Omitting residual value at disposition | Treats capex as a pure cost recovery exercise. Misses the capitalization multiplier. | Always include residual value: incremental NOI / exit cap rate. |
| Treating maintenance capex as value-add | Roof replacement preserves value but does not create it. Claiming a "return" on maintenance capex is misleading. | Separate maintenance capex (preserves NOI) from value-add capex (increases NOI). Maintenance capex has no IRR. |
| Ignoring deferral cost of "do nothing" | Makes deferral look free. It is not -- lost NOI, accelerated R&M, and disposition discount are real costs. | Quantify the "do nothing" scenario as a negative-NPV alternative. |
| Using annual averages for renovation downtime | Understates Year 1 negative carry. A 6-month reno has zero NOI improvement for months 1-6 and full improvement for months 7-12. | Model monthly cash flows during renovation period, then annualize for Year 2 onward. |
