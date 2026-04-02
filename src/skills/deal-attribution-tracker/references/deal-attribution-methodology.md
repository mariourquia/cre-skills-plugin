# Deal Attribution Methodology
# Reference for deal-attribution-tracker skill
# Defines frameworks for allocating GP carry to deal team members,
# vesting schedules, clawback treatment, and departure mechanics

---

## Overview

Deal attribution answers: who gets paid what carry, when, and under what conditions? In CRE private equity, carry allocation is either fund-level (pooled and distributed by a points schedule) or deal-level (each deal has its own allocation). The methodology affects retention incentives, recruiting economics, and legal enforceability of carry rights.

---

## Carry Allocation Structures

### Structure 1: Fund-Level Pooled Carry

The most common structure in CRE funds. All carry earned by the GP flows into a single pool, then distributed to team members according to a pre-agreed points schedule.

**Advantages:**
- Discourages deal hoarding (team members benefit from all deals, not just their own)
- Simplifies administration (one waterfall, one distribution event)
- Allows GP to reward non-deal professionals (CFO, operations, investor relations)

**Disadvantages:**
- Weak link between individual deal performance and individual compensation
- Underperformers benefit from overperformers' work
- Senior partners may dominate the points schedule, reducing junior motivation

**Points schedule mechanics:**

```
Total GP Carry Pool = carry_rate * fund_level_profit_above_pref

Each team member's allocation:
  Individual Carry = Total GP Carry Pool * (Individual Points / Total Points)
  Where: Total Points = sum of all team members' points (typically sums to 100)

Points are typically defined at fund formation and documented in:
  - Limited Partnership Agreement (Exhibit defining carry allocation) or
  - Separate carry allocation agreement among GP principals or
  - Employment/partnership agreements referencing the carry schedule

Example:
  Managing Partner (CIO):           35 points (35%)
  Senior MD (Acquisitions Head):    20 points (20%)
  Senior MD (Asset Management):     15 points (15%)
  VP (Acquisitions):                10 points (10%)
  VP (Asset Management):             8 points (8%)
  Associate (Senior):                5 points (5%)
  CFO / Finance:                     4 points (4%)
  Analyst Pool (2-3 analysts):       3 points (3%)
  TOTAL:                           100 points (100%)
```

### Structure 2: Deal-Level Attribution

Each deal has a designated originator, deal team lead, and supporting cast. Carry earned on each deal flows to the specific team members who worked on that deal.

**Advantages:**
- Direct link between deal success and individual reward
- Encourages accountability and deal ownership
- Transparent: each person knows exactly what they earn from each deal

**Disadvantages:**
- Can create internal competition and information hoarding
- Origination credit disputes (who sourced the deal?)
- Asset management credit disputes (credit goes to originator or person who executed?)
- Non-deal staff receive no carry

**Deal-level attribution mechanics:**

```
FOR EACH DEAL, a deal carry sheet defines:
  Origination Credit:       X%  (who found and/or underwrote the deal)
  Asset Management Credit:  Y%  (who managed the asset post-close)
  Fund Credit:              Z%  (retained by GP entity for pooled distribution)
  Where X + Y + Z = 100% of that deal's carry

Example Deal Attribution Sheet:
  Deal: Austin Warehouse (Deal 1 from worked example)
  GP Carry on Deal 1: $17.60M

  Origination Credit (25%):
    MD (Acquisitions):    15% * $17.60M = $2.64M
    VP (Acquisitions):    10% * $17.60M = $1.76M

  Asset Management Credit (35%):
    MD (Asset Mgmt):      20% * $17.60M = $3.52M
    Associate:            15% * $17.60M = $2.64M

  Fund Credit (40%):
    Managing Partner:     40% * $17.60M = $7.04M
    (distributed through pooled fund schedule)
```

### Structure 3: Hybrid

A hybrid allocates a portion of carry to specific deals (rewarding origination and deal execution) and a portion to the pooled fund (rewarding team-level contribution). Increasingly common in mid-to-large CRE firms.

```
Example hybrid:
  25% of deal carry = deal-specific attribution (as above)
  75% of deal carry = pooled fund, distributed per points schedule

This aligns incentives at both the deal level (originator is rewarded) and
fund level (team collaboration is rewarded).
```

---

## Vesting Schedules

Vesting governs when a team member's carry entitlement becomes non-forfeitable. Unvested carry can be clawed back by the GP upon departure.

### Standard Vesting Schedule Types

**Cliff vesting:**
```
0% vested until the cliff date, then 100% vests at once.
Rarely used for full carry pools; may apply to individual deal carry.

Example: 5-year cliff from fund closing
  Years 0-4:  0% vested
  Year 5+:    100% vested
```

**Cliff + annual (most common in CRE):**
```
Partial vesting after initial cliff, then annual increments.

Example: 3-year cliff, then 20% per year:
  Years 0-2:  0% vested
  Year 3:     20% vested
  Year 4:     40% vested
  Year 5:     60% vested
  Year 6:     80% vested
  Year 7+:    100% vested

Example: 5-year cliff, then 10% per year:
  Years 0-4:  0% vested
  Year 5:     50% (immediate 50% vest at cliff)
  Year 6:     60%
  Year 7:     70%
  Year 8:     80%
  Year 9:     90%
  Year 10+:   100%
```

**Annual vesting from day one (less common, LP-favorable for GP retention):**
```
Vesting begins immediately, pro-rated annually.

Example: 10% per year from fund closing:
  Year 1:  10%
  Year 2:  20%
  ...
  Year 10: 100%
```

### Vesting Clock Mechanics

```
VESTING START DATE:
  Option A: Fund final closing date (most common)
  Option B: Individual's hire date (disadvantages founders vs later hires)
  Option C: First capital call date

ACCELERATION:
  Single-trigger acceleration: vesting accelerates 100% upon:
    - Fund sale, merger, or transfer of GP entity
    - Change of control of managing partner
  Double-trigger acceleration: vesting accelerates 100% only if:
    - Change of control occurs AND
    - Team member is terminated without cause within 12-24 months

EXTENSION FOR FUND LIFE:
  If fund extends beyond its stated term (e.g., from 10 to 12 years),
  vesting schedule typically extends proportionally or vests fully at
  original end date. This is deal-specific; confirm in LPA/carry agreement.
```

### Vesting Calculation

```
As of any valuation date:

Vested Carry Entitlement = Total Carry Earned to Date * Vesting % (at valuation date)

Example:
  Team member: VP, 8 carry points (8% of GP pool)
  Fund total carry earned to date: $20M
  VP's gross carry: 8% * $20M = $1.6M
  Vesting % at Year 4 (3-year cliff + 20%/year): 20%
  Vested carry: $1.6M * 20% = $320,000

  If VP departs today as a Good Leaver:
    Entitled to: $320,000 (vested)
    Forfeited: $1.28M (unvested, returns to GP pool)
```

---

## Good Leaver / Bad Leaver Provisions

Departure classification determines what carry a departing team member retains.

### Good Leaver

Definition (market standard):
- Voluntary resignation after minimum tenure (often 5+ years)
- Retirement (age 65+ or per LPA definition)
- Death or permanent disability
- Termination without cause by GP entity
- Mutual separation (agreed severance)
- Non-renewal of employment agreement

**Good Leaver carry treatment:**

```
OPTION A (LP-favorable / GP-favorable for retention):
  Retain vested carry entitlement
  Forfeit all unvested carry
  Distribution timing: at realization events, same as active team members
  Ongoing right to fund information: limited (typically distribution notices only)

OPTION B (negotiated):
  Retain vested carry entitlement
  Receive pro-rated unvested carry based on service period at departure
  Example: 4 years of service on 5-year cliff = 80% credit; 20% forfeited
  Distribution timing: same as above

OPTION C (most GP-favorable):
  Retain vested carry
  All unvested carry bought out at fair value by GP entity at departure
  Allows clean separation; departing member gets liquidity, GP retains full pool
```

### Bad Leaver

Definition (market standard):
- Termination for cause (fraud, material breach, criminal conviction)
- Voluntary resignation before minimum tenure
- Joining a competitor within restricted period (non-compete violation)
- Material breach of confidentiality, non-solicitation, or LPA covenants

**Bad Leaver carry treatment:**

```
Option A (most common -- full forfeiture):
  Forfeit ALL carry, including vested carry
  All carry returns to GP pool for redistribution or reduction

Option B (partial forfeiture):
  Forfeit all unvested carry
  Retain vested carry minus a penalty
  Penalty typically: 25-50% of vested carry forfeited as liquidated damages

Option C (least common -- same as Good Leaver):
  Some LPAs treat all voluntary departures equally (no bad leaver distinction)
  Less common in institutional CRE funds
```

### Departing Member Calculation Template

```
DEPARTING TEAM MEMBER ANALYSIS:

Member Name:            [Name]
Departure Date:         [Date]
Fund Closing Date:      [Date]
Years of Service:       [X] years
Departure Type:         [Good Leaver / Bad Leaver]
Carry Points:           [X]% of GP pool
Vesting Status:         [X]% vested per schedule

Fund Carry Metrics (at departure date):
  Total GP Carry Earned (realized only): $[X]M
  Total GP Carry Accrued (unrealized at marks): $[X]M
  Total GP Carry Accrued (combined): $[X]M

Member Gross Carry (pre-vesting):
  Points % * Total Carry = [X]% * $[X]M = $[X]

Vested Carry Entitlement:
  Member Gross Carry * Vesting % = $[X]M * [X]% = $[X]M

Unvested Carry (forfeited or pro-rated per LPA):
  Member Gross Carry * (1 - Vesting %) = $[X]M

Distribution Rights on Vested Carry:
  Realized carry: payable within [X] days of departure (per LPA)
  Unrealized accrued carry: paid at realization events as they occur
  Estimated timing: [X] years until full distribution

Reallocation of Forfeited Unvested:
  Forfeited carry points: [X]%
  Reallocation per LPA: [describe -- pro-rata to remaining team, or GP discretion]
  New points schedule after departure: [attach updated schedule]
```

---

## Return Attribution to Deals and Team Members

### Deal-Level Return Attribution Matrix

For each team member, identify the deals they worked on and quantify the carry attributable to their deal contributions.

```
ATTRIBUTION MATRIX:

            | Deal 1 | Deal 2 | Deal 3 | Deal 4 | Deal 5 | Fund Pool | TOTAL
------------|--------|--------|--------|--------|--------|-----------|------
GP Carry    | $17.6M | $22.0M | $0     | $0     | $21.4M | (pooled)  | $61M

Carry Attribution:
             Deal 1  | Deal 2 | Deal 3 | Deal 4 | Deal 5 | Pool  | Total
MP (40%)     $7.04M  | $8.80M | $0     | $0     | $8.56M | $24.4M| $24.4M
Sr MD A(20%) $3.52M  | $4.40M | $0     | $0     | $4.28M | $12.2M| $12.2M
Sr MD B(15%) $2.64M  | $3.30M | $0     | $0     | $3.21M | $9.15M| $9.15M
VP (10%)     $1.76M  | $2.20M | $0     | $0     | $2.14M | $6.10M| $6.10M
Assoc (8%)   $1.41M  | $1.76M | $0     | $0     | $1.71M | $4.88M| $4.88M
Other (7%)   $1.23M  | $1.54M | $0     | $0     | $1.50M | $4.27M| $4.27M
TOTAL        $17.60M | $22.0M | $0     | $0     | $21.4M | $61M  | $61M
```

### Deal-Level Alpha Attribution

Beyond carry dollars, attribute deal-level returns to specific team member contributions for performance review purposes.

```
RETURN DRIVER ATTRIBUTION:
For each deal, identify primary value creation driver:

Deal 1 (Warehouse, 2.20x):
  Origination alpha: off-market source, 50 bps below market at entry cap
  Asset management: extended 3 leases early at above-market rent
  Exit timing: sold before logistics cap rate expansion
  Attribution: Origination + AM team (dual credit)

Deal 2 (Apartment, 2.00x):
  Origination: broadly marketed (no origination alpha)
  Asset management: executed $4M renovation, 18% rent increase
  Exit: hit market cycle peak
  Attribution: primarily AM team

Deal 3 (Office, 1.11x):
  Origination: mid-market sourced
  Asset management: struggled with 2019-2021 office market headwinds
  Exit: forced sale at compressed MOIC due to lease rollover
  Attribution: difficult to assign skill; market conditions primary driver

Deal 4 (Retail, 0.80x):
  Origination: anchor tenant risk not fully modeled at underwriting
  Asset management: limited options after anchor vacated
  Attribution: Underwriting error (originator); market timing (market)

Deal 5 (Industrial, 2.14x):
  Origination: programmatic relationship sourcing
  Asset management: 24-month lease-up to full occupancy
  Exit: sale-leaseback transaction at premium
  Attribution: origination and AM both strong

SKILL SCORE BY MEMBER (qualitative):
  MD Acquisitions: 3 deals above expectations (Deal 1, 2, 5); 1 underwriting error (Deal 4)
    Score: 3.5 / 5.0 -- solid performance with one significant miss
  MD Asset Mgmt: strong execution on Deals 1 and 5; limited options on 3 and 4
    Score: 4.0 / 5.0 -- good asset management skills; deal selection not their call
```

---

## Clawback Distribution Rules

When a clawback is triggered, the GP must recover carry from team members proportional to what they received.

### Individual Clawback Liability

```
INDIVIDUAL CLAWBACK OBLIGATION:
  If total GP clawback = $X (from fund-level calculation):
  Individual clawback = Total clawback * (Individual Points / 100)

  Unless the LPA specifies other allocation (e.g., senior partners bear more)

PRACTICAL CLAWBACK MECHANICS:
  Step 1: Confirm total clawback amount from waterfall recalculation
  Step 2: Allocate clawback to current and former team members pro-rata by points
  Step 3: Former team members who received carry distributions are personally liable
  Step 4: If former member has already spent carry, GP must pursue collection
  Step 5: Escrow funds are applied first; residual from individual members

GROSS-UP FOR TAXES:
  If team members paid income tax on carry distributions, the clawback is
  technically a return of after-tax income. Some LPAs provide a tax gross-up
  (GP entity contributes additional cash to cover team members' tax cost).
  Market standard: no gross-up; team member bears tax risk.
  LP-favorable: tax gross-up required (rare but negotiable).
```

### Clawback Reserve

```
CLAWBACK RESERVE SIZING:
  Conservative: reserve 100% of carry distributed on deals where unrealized
    deals have negative mark-to-market at current interest rates
  Market standard: reserve 30-50% of carry distributed while unrealized
    positions remain (American waterfall funds only)
  Aggressive (GP-favorable): reserve only the escrow requirement per LPA (20%)

RESERVE RELEASE:
  Release reserve when: fund is fully realized and final waterfall computed
  Partial release: acceptable when realized portfolio covers hurdle and
    remaining unrealized positions are de minimis (< 5% of fund value)
```

---

## Deal-Level Attribution Summary Report Template

```
DEAL ATTRIBUTION REPORT
Fund: [Name] | As of: [Date] | Waterfall: [Type]

SECTION 1: FUND CARRY SUMMARY
  Total GP Carry Earned (realized): $[X]M
  Total GP Carry Accrued (unrealized): $[X]M
  Total GP Carry (combined): $[X]M
  Carry Distributed to Date: $[X]M
  Remaining to Distribute: $[X]M
  Clawback Exposure (at current marks): $[X]M

SECTION 2: TEAM ATTRIBUTION
  [Attribution matrix as above]

SECTION 3: VESTING STATUS BY MEMBER
  [Vested / unvested / distributable carry per member]

SECTION 4: DEPARTING MEMBER STATUS
  [List any departed team members and their carry entitlement]

SECTION 5: CLAWBACK RESERVE
  Required reserve (per LPA): $[X]M
  Current escrow balance: $[X]M
  Gap (if any): $[X]M
  Recommendation: [Fund / reduce / maintain]
```
