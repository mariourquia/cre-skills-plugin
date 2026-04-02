# Sales Comp Adjustment Methodology

## Purpose

Translate raw sales comparables into an adjusted value indication for the subject property. Every comp is imperfect. Adjustments quantify the imperfections so the final value opinion has defensible support.

## Adjustment Categories

Adjustments are applied sequentially in this order (sequence matters because each builds on the prior adjusted price):

### 1. Property Rights Conveyed
- Fee simple vs leasehold
- Adjust if comp sold with different bundle of rights
- Example: leasehold sale adjusted upward to fee simple equivalent
- Typical range: 0% to +15%

### 2. Financing Terms
- Cash equivalent adjustment for below-market or seller financing
- Discount the favorable financing benefit to present value and subtract from sale price
- Example: Seller provided 5-year interest-only loan at 4% when market was 7%. PV of rate differential over term = adjustment.
- Typical range: -5% to 0%

### 3. Conditions of Sale (Motivation)
- Arms-length vs distressed, related-party, 1031 exchange pressure
- REO sales: typically +10-20% adjustment to reflect market pricing
- 1031 buyers: may overpay 3-8% due to exchange timeline pressure
- Related-party: exclude from analysis if adjustment is speculative
- Typical range: -10% to +20%

### 4. Market Conditions (Time)
- Adjust for market movement between comp sale date and valuation date
- Use repeat-sales index, cap rate trend, or paired-sales analysis
- Formula: `Adjusted Price = Sale Price x (1 + monthly appreciation rate x months)`
- Industrial and multifamily: 0.3-0.5%/month appreciation in growth markets (2023-2025 vintage -- verify current)
- Office: flat to negative in many markets
- Typical range: -15% to +20% depending on time gap

### 5. Location
- Submarket quality, highway access, demographics, school district, flood zone
- Paired-sales analysis is ideal (same building type, different locations)
- When paired sales unavailable, use rent differential as proxy:
  - `Location Adj = (Subject Submarket Rent - Comp Submarket Rent) / Comp Submarket Rent`
- Typical range: -20% to +20%

### 6. Physical Characteristics

**Size:**
- Larger properties trade at lower per-unit/per-SF prices (economies of scale, thinner buyer pool)
- Adjustment derived from regression or paired sales
- Rule of thumb: 10% size difference = 2-4% price/unit adjustment (inverse)
- Apply only when size differential exceeds 15-20%

**Age/Condition:**
- Effective age, not chronological age
- Estimate deferred maintenance cost differential
- Formula: `Condition Adj = (Comp Deferred Maintenance - Subject Deferred Maintenance) / Comp Sale Price`
- Recently renovated comp vs unrenovated subject: adjust comp downward by renovation cost

**Quality/Amenities:**
- Unit mix (studio-heavy vs family-sized), parking ratio, fitness center, pool, elevator
- Amenity package valuation: estimate rent premium from amenity, capitalize at market cap rate
- Example: Pool generates $15/unit/month premium x 100 units x 12 / 6.0% cap = $300k value differential

**Building systems:**
- HVAC type, roof age, elevator, sprinkler, electrical capacity
- Adjust by estimated remaining useful life differential and replacement cost

### 7. Economic Characteristics
- Rent levels, expense ratios, management intensity
- Typically captured in NOI-based analysis, but relevant for per-unit/per-SF sales comps
- Adjust if comp has materially different in-place NOI vs market
- Below-market leases: adjust comp upward (buyer paid for below-market income, market value is higher)

### 8. Non-Realty Components
- FF&E, business value, excess land
- Subtract value of non-realty items included in sale price
- Common in hospitality (furniture), self-storage (management contracts), senior housing (licenses)

## Confidence Scoring

Each comp receives a confidence score (1-5) based on:

| Score | Label | Criteria |
|---|---|---|
| 1 | Poor | >3 major adjustments needed, total net adjustment >30%, unreliable data |
| 2 | Below Avg | 2-3 major adjustments, total net 20-30%, some data gaps |
| 3 | Adequate | 1-2 moderate adjustments, total net 10-20%, verified data |
| 4 | Good | Minor adjustments only, total net 5-10%, confirmed arms-length |
| 5 | Excellent | Minimal adjustment, total net <5%, recent sale, same submarket, verified |

**Adjustment thresholds:**
- Individual adjustment > 15%: Flag for review -- may be too dissimilar
- Net adjustment (sum of all) > 25%: Comp is marginal -- low confidence
- Gross adjustment (absolute sum) > 40%: Comp should be excluded or heavily discounted

## Worked Example: 5-Comp Sales Grid

**Subject Property:**
- 120-unit multifamily, 1995 vintage, Class B, Atlanta (Decatur submarket)
- 92% occupied, avg rent $1,280/unit, T12 NOI $1,620,000
- Recently renovated (2024): new roofs, HVAC, unit interiors 60% complete
- Valuation date: March 2026

### Comp Grid

```
                        Comp 1          Comp 2          Comp 3          Comp 4          Comp 5
Property              Maple Ridge     Oak Terrace     Pine Creek      Cedar Hills     Elm Crossing
Location              Decatur         Avondale Est    Tucker          Decatur         Scottdale
Units                 100             150             90              130             110
Vintage               1998            1992            2001            1996            1994
Sale Date             Dec 2025        Sep 2025        Jun 2025        Jan 2026        Nov 2025
Sale Price            $13,500,000     $20,250,000     $11,700,000     $17,550,000     $14,300,000
Price/Unit            $135,000        $135,000        $130,000        $135,000        $130,000
Cap Rate (actual)     5.8%            6.0%            6.2%            5.7%            6.1%
Condition             Unrenovated     Partial reno    Good, newer     Renovated 2023  Unrenovated
Occupancy at Sale     94%             91%             96%             95%             89%
```

### Adjustment Analysis

```
                        Comp 1      Comp 2      Comp 3      Comp 4      Comp 5
Base Price/Unit         $135,000    $135,000    $130,000    $135,000    $130,000

Property Rights         0%          0%          0%          0%          0%
  (all fee simple)

Financing               0%          0%          -3%         0%          0%
  (Comp 3: seller       $0          $0          -$3,900     $0          $0
   financing at
   below-market rate)

Conditions of Sale      0%          0%          0%          0%          +5%
  (Comp 5: estate       $0          $0          $0          $0          +$6,500
   sale, slight
   motivation discount)

Market Conditions       +1.5%       +3.0%       +4.5%       +1.0%       +2.0%
  (Time adj @ 0.5%/mo)  +$2,025     +$4,050     +$5,850     +$1,350     +$2,600

Location                0%          -3%         -5%         0%          -4%
  (Decatur=subject,     $0          -$4,050     -$6,500     $0          -$5,200
   Avondale -3%,
   Tucker -5%,
   Scottdale -4%)

Size                    -2%         +3%         -3%         +1%         -1%
  (120 units=subject,   -$2,700     +$4,050     -$3,900     +$1,350     -$1,300
   smaller=higher
   $/unit)

Condition/Quality       +8%         +4%         +2%         -2%         +8%
  (Subject partially    +$10,800    +$5,400     +$2,600     -$2,700     +$10,400
   renovated; Comp 1,5
   unrenovated; Comp 4
   fully renovated)

Age/Vintage             +1%         +2%         -2%         +1%         +1%
  (Subject 1995,        +$1,350     +$2,700     -$2,600     +$1,350     +$1,300
   newer=negative adj)

Net Adjustments         +$11,475    +$12,150    -$8,450     +$1,350     +$14,300
Net Adj %               +8.5%       +9.0%       -6.5%       +1.0%       +11.0%
Gross Adj %             12.5%       16.0%       17.5%       5.0%        21.5%

Adjusted Price/Unit     $146,475    $147,150    $121,550    $136,350    $144,300

Confidence Score        4           3           3           5           3
```

### Reconciliation

```
                        Adj $/Unit      Confidence    Weight
Comp 4 (Cedar Hills)   $136,350        5             35%
Comp 1 (Maple Ridge)   $146,475        4             25%
Comp 2 (Oak Terrace)   $147,150        3             15%
Comp 5 (Elm Crossing)  $144,300        3             15%
Comp 3 (Pine Creek)    $121,550        3             10%

Weighted Avg:           $140,743/unit
Indicated Value:        $140,743 x 120 = $16,889,160
Rounded:                $16,900,000
```

**Reconciliation notes:**
- Comp 4 receives highest weight: same submarket, minimal net adjustment (1.0%), most recent sale, similar renovation profile
- Comp 3 receives lowest weight: below-market financing, different submarket, largest gross adjustment
- Range of adjusted values ($121k-$147k) is 21% spread -- acceptable for Class B multifamily with varying renovation status
- Value supported by income approach: $1,620,000 NOI / 5.9% market cap = $16,875,000 (within 0.2% of sales comparison)

## Key Principles

1. **Sequence matters.** Apply adjustments in the order listed. Each builds on the prior adjusted base.
2. **Direction convention.** Positive adjustment = comp is inferior to subject (adjust UP). Negative = comp is superior (adjust DOWN). Always from the comp's perspective toward the subject.
3. **Paired sales are gold.** When you can isolate a single variable (two identical buildings in different submarkets), that paired sale is the best adjustment evidence.
4. **Less is more.** If you need more than 5 adjustments exceeding 5% each, the comp is too dissimilar. Find a better comp.
5. **Gross vs net.** Net adjustment can hide offsetting errors. A comp with +15% and -15% adjustments (net 0%, gross 30%) is less reliable than one with +5% net and gross.
6. **Time kills accuracy.** Prefer comps within 6 months. Beyond 12 months, time adjustment uncertainty dominates.
7. **Verify everything.** Call the broker. Pull the deed. Confirm the unit count, sale price, and conditions. Public records have errors.
