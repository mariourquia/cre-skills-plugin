# NOI Bridge Waterfall Template

---

## Purpose

An NOI bridge shows how Net Operating Income moves from its current level to a target level, broken into specific, actionable components. It is the operational translation of an investment thesis: every dollar of projected NOI improvement must be traceable to a named initiative with a responsible owner, a timeline, and a measurable outcome.

**When to use**: Post-acquisition business planning, quarterly asset management reviews, IC presentations, investor reporting.

**Rule**: Every line in the NOI bridge must pass the "says who?" test. If you cannot name the data source, comparable, or signed contract behind a number, it does not belong in the bridge.

---

## Part 1: NOI Bridge Template

### 1.1 Standard Format

```
STARTING POINT
  In-Place NOI (T-12 Actual)                          $[X]

REVENUE IMPROVEMENTS
  + Organic rent growth (mark-to-market on renewals)   $[X]
  + Renovation rent premium (renovated units x premium) $[X]
  + Vacancy reduction (occupancy improvement)           $[X]
  + Loss-to-lease capture (new leases at market)        $[X]
  + Other income initiatives (parking, laundry, RUBS)   $[X]
  + Concession burn-off                                 $[X]
  = Total Revenue Improvement                           $[X]

EXPENSE CHANGES
  - Expense growth (inflation, market increases)        ($[X])
  + Expense savings (insurance rebid, tax appeal, etc.) $[X]
  + RUBS / utility recovery implementation              $[X]
  - New expenses from renovation (higher insurance, etc)($[X])
  = Net Expense Impact                                  $[X] or ($[X])

TARGET POINT
  Stabilized NOI                                        $[X]
  NOI Uplift ($)                                        $[X]
  NOI Uplift (%)                                        [X]%
  Timeline to Stabilization                             [X] months
```

### 1.2 Detailed Line Item Specifications

| Line Item | Calculation | Data Source | Confidence Level |
|-----------|------------|-------------|-----------------|
| In-place NOI | T-12 actual from financials | Seller financials, verified against bank stmts | High (verified) |
| Organic rent growth | (Market rent - in-place rent) x renewal probability x units | Rent comps + historical renewal rate | Medium |
| Renovation premium | Units to renovate x monthly premium x 12 x occupancy factor | Comparable renovated units | Medium-High |
| Vacancy reduction | (Target occ - current occ) x avg rent x 12 | Submarket vacancy data | Medium |
| Loss-to-lease | New lease rent - expiring lease rent, summed across expirations | Current rent roll vs. market | Medium-High |
| Other income | Specific initiative x revenue per unit x participating units | Market survey or vendor quote | Medium |
| Concession burn-off | Current concessions x probability of non-renewal at market | Lease-by-lease analysis | Medium |
| Expense inflation | Prior year expenses x assumed growth rate | CPI, historical trend, insurance market | Medium |
| Expense savings | Specific initiative x estimated annual savings | Insurance quotes, tax appeal estimate | Medium-Low |
| RUBS recovery | Recoverable utilities x recovery percentage x units | Utility bills + RUBS vendor quote | Medium |

---

## Part 2: Worked Example -- 200-Unit Multifamily

### Property Overview

| Field | Detail |
|-------|--------|
| Property | Riverdale Gardens, 200 units |
| Location | Paterson, NJ |
| Year Built | 1982 / Partial renovation 2015 |
| Unit Mix | 80 x 1BR, 80 x 2BR, 40 x 3BR |
| Current Occupancy | 91% (18 vacant) |
| Average In-Place Rent | $1,380/month |
| Market Rent (unrenovated) | $1,500/month |
| Market Rent (renovated) | $1,850/month |
| In-Place T-12 NOI | $1,920,000 |
| Target Stabilized NOI | $2,850,000 |
| Renovation Scope | 60 of 200 units at $22,000/unit |
| Timeline to Stabilization | 24 months |

### NOI Bridge

```
STARTING POINT
  In-Place NOI (T-12 Actual)                            $1,920,000

REVENUE IMPROVEMENTS

  1. Organic Rent Growth on Renewals                     +$129,600
     - 140 unrenovated units retained x $1,380 avg rent
     - Target 4.0% increase on renewals ($55/month avg)
     - 70% renewal probability = 98 units renewing
     - 98 units x $55/mo x 12 = $64,680 (Year 1)
     - Assume similar in Year 2 with compounding
     - 2-year total annualized: $129,600

  2. Renovation Rent Premium                             +$378,000
     - 60 units renovated at $22,000/unit
     - Premium: $1,850 - $1,380 = $470/month per unit
     - $470 x 60 units x 12 months = $338,400
     - Apply 93% occupancy factor on renovated: $314,712
     - Plus mark-to-market on remaining renovated at Year 2:
       $470 x 60 x 3% growth x 12 = +$10,152
     - Plus lease-up ramp (units come online over 18 months):
       Weighted average = ~$378,000 at full stabilization

  3. Vacancy Reduction                                   +$148,800
     - Current: 91% occupancy (18 vacant)
     - Target: 95% occupancy (10 vacant)
     - 8 additional occupied units x $1,550 avg blended rent x 12
     - $1,550 x 8 x 12 = $148,800

  4. Loss-to-Lease Capture                               +$72,000
     - 40 units with leases $150+/month below market
     - At expiration, re-lease at market
     - 40 x $150 x 12 = $72,000
     - Phased over 24 months as leases expire

  5. Other Income Initiatives                            +$96,000
     - RUBS (utility recovery): 200 units x $25/mo = $60,000/yr
     - Parking fee increase: 80 spaces x $25/mo increase = $24,000/yr
     - Laundry contract renegotiation: +$6,000/yr
     - Pet fees (new policy): 40 pets x $50/mo = $24,000/yr
     - Storage unit monetization: 20 units x $75/mo = $18,000/yr
     - Less: implementation costs and phase-in = -$36,000
     - Net other income at stabilization: $96,000

  6. Concession Burn-Off                                 +$36,000
     - Current concessions: 12 units with 1-month free rent
     - Annualized concession value: 12 x $1,380 = $16,560
     - Plus move-in specials ($500 each on 39 units): $19,500
     - Total concession burn-off at stabilization: ~$36,000

  TOTAL REVENUE IMPROVEMENT                              +$860,400

EXPENSE CHANGES

  7. Expense Inflation                                   -$134,400
     - Year 1: $1,680,000 base x 3.5% = +$58,800
     - Year 2: $1,738,800 x 3.5% = +$60,858
     - Insurance spike (NJ market: +18% Year 1): +$32,400
     - Property tax (2% annual reassessment): +$14,400
     - Total 2-year expense growth: ~$134,400
     - Note: Insurance assumed to normalize in Year 3

  8. Expense Savings Initiatives                         +$78,000
     - Insurance rebid (switch carrier): -$18,000/yr savings
     - Property tax appeal (Paterson reassessment challenge):
       -$25,000/yr if successful (60% probability = $15,000 expected)
     - Vendor contract renegotiation (landscaping, cleaning,
       pest control): -$12,000/yr
     - Staffing optimization (eliminate 1 FTE via technology):
       -$45,000/yr savings
     - Less: technology implementation cost amortized: +$12,000/yr
     - Net expense savings: $78,000

  9. RUBS Utility Recovery (Expense Side)                +$60,000
     - Already counted in revenue; this is the offset
     - Owner utility expense: $180,000/yr
     - RUBS recovery target: 33% = $60,000/yr
     - Net utility expense reduction: $60,000

  10. New Expenses from Renovation Program               -$24,000
      - Higher property insurance (renovated units valued higher):
        +$8,000/yr
      - Increased common area maintenance (upgraded amenities):
        +$6,000/yr
      - Marketing cost during lease-up: +$10,000/yr
      - Total new expenses: $24,000

  NET EXPENSE IMPACT                                     -$20,400

TARGET POINT
  Stabilized NOI                                         $2,760,000
  NOI Uplift ($)                                         $840,000
  NOI Uplift (%)                                         43.8%
  Timeline to Stabilization                              24 months
```

### Reconciliation Check

```
Starting NOI:           $1,920,000
Revenue improvement:    +$860,400
Net expense impact:     -$20,400
Implied stabilized NOI: $2,760,000
Target NOI:             $2,850,000
Gap:                    -$90,000 (3.2% below target)
```

**Gap analysis**: The $90K shortfall vs. $2.85M target comes from conservative assumptions on renovation lease-up pace and RUBS adoption rate. To close the gap, the asset manager can: (1) push renovation completion from 18 to 15 months (accelerate revenue), (2) increase RUBS recovery from 33% to 40%, or (3) pursue additional other income (cell tower lease, storage expansion). Each of these produces $25-40K annually and is achievable.

---

## Part 3: NOI Bridge Sensitivity

### Revenue-Side Sensitivity

| Scenario | Reno Premium | Vacancy | Rent Growth | Stabilized NOI | vs. Base |
|----------|-------------|---------|-------------|---------------|---------|
| Bull | $500/mo | 96% | 5.0% | $3,020,000 | +9.4% |
| Base | $470/mo | 95% | 4.0% | $2,760,000 | -- |
| Conservative | $400/mo | 94% | 2.5% | $2,520,000 | -8.7% |
| Stress | $350/mo | 92% | 1.0% | $2,280,000 | -17.4% |

### Expense-Side Sensitivity

| Scenario | Expense Growth | Insurance | Tax Appeal | Stabilized NOI | vs. Base |
|----------|---------------|-----------|-----------|---------------|---------|
| Favorable | 2.5% | Flat | Won | $2,880,000 | +4.3% |
| Base | 3.5% | +18% Y1 | 60% prob | $2,760,000 | -- |
| Adverse | 4.5% | +25% Y1 | Lost | $2,640,000 | -4.3% |

---

## Part 4: NOI Bridge Presentation Rules

### Do

- Show every line item with a named data source
- Include a reconciliation check (does the bridge foot?)
- Present sensitivity on the 3 most impactful variables
- Include a timeline showing when each initiative kicks in
- Assign an owner to each initiative
- Update the bridge quarterly with actuals vs. plan

### Do Not

- Aggregate multiple initiatives into a single "operational improvement" line
- Assume 100% execution on every initiative simultaneously
- Use projected market rents without citing comparable properties by address
- Ignore expense growth (expenses always grow; it is never zero)
- Present the bridge without a sensitivity showing the downside case
- Claim RUBS recovery without a vendor quote and implementation timeline

### Confidence Tiering

Label each bridge line item with a confidence tier:

| Tier | Confidence | Criteria | Example |
|------|-----------|----------|---------|
| A | High (>80%) | Supported by signed contract, historical data, or verified comp | Renovation premium backed by 5+ comp leases |
| B | Medium (50-80%) | Supported by market data or vendor estimate, but not contracted | Insurance rebid based on broker quote, not policy |
| C | Low (<50%) | Supported by assumption or analogous market, not direct evidence | Tax appeal success rate based on county statistics |

For the worked example:
- Renovation premium: Tier A (5 comparable renovated units within 0.5 miles)
- Vacancy reduction: Tier B (submarket data supports 95%, but asset-specific factors may vary)
- Tax appeal: Tier C (county-level success rate, not asset-specific opinion)
- RUBS implementation: Tier B (vendor quote received, tenant adoption rate assumed)
