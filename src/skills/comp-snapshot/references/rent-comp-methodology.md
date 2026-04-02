# Rent Comp Methodology

## Purpose

Determine achievable market rent for the subject property by analyzing comparable leases. Unlike sales comps, rent comps require understanding both face rent and the full concession package to arrive at effective rent -- the number that actually drives NOI.

## Effective Rent Calculation

### Formula
```
Monthly Effective Rent = (Monthly Face Rent x Lease Term - Total Concession Value) / Lease Term
```

### Concession Types and Valuation

| Concession | How to Value | Common Range |
|---|---|---|
| Free rent months | Face rent x free months | 0.5-3 months (MF), 2-12 months (office) |
| Reduced rent period | (Face - reduced) x reduced months | Varies |
| Move-in bonus/gift card | Dollar amount | $200-1,500 (MF) |
| Waived application fee | Dollar amount | $25-75 per applicant |
| Waived amenity fees | Monthly value x lease term | $25-150/month |
| Free parking | Monthly parking rate x lease term | $50-300/month |
| Free storage | Monthly storage rate x term | $25-100/month |
| Tenant improvement (commercial) | $/SF x leased SF | $15-75/SF (office) |
| Moving allowance (commercial) | Dollar amount | $1-5/SF |
| Early termination option | Option value estimate | 2-6% of total rent |

### Worked Example (Multifamily)
```
Unit type: 2BR/2BA, 950 SF
Face rent: $1,850/month
Lease term: 12 months
Concessions: 1 month free + waived $500 move-in fee

Effective Rent = ($1,850 x 12 - $1,850 - $500) / 12
              = ($22,200 - $1,850 - $500) / 12
              = $19,850 / 12
              = $1,654/month effective

Discount from face: ($1,850 - $1,654) / $1,850 = 10.6%
```

### Worked Example (Commercial Office)
```
Space: 5,000 SF
Face rent: $32.00/SF NNN
Lease term: 84 months (7 years)
Concessions: 6 months free rent + $45/SF TI allowance + $2/SF moving allowance

Free rent value: $32.00 x 5,000 / 12 x 6 = $80,000
TI value: $45.00 x 5,000 = $225,000
Moving allowance: $2.00 x 5,000 = $10,000
Total concessions: $315,000

Annual effective rent = ($32.00 x 5,000 x 7 - $315,000) / 7 / 5,000
                     = ($1,120,000 - $315,000) / 7 / 5,000
                     = $805,000 / 35,000
                     = $23.00/SF effective

Discount from face: ($32.00 - $23.00) / $32.00 = 28.1%
```

## Amenity Valuation

Amenities drive rent premiums. Quantify them to make valid comp adjustments.

### Amenity Premium Benchmarks (Multifamily)

| Amenity | Monthly Premium | Confidence | Notes |
|---|---|---|---|
| In-unit washer/dryer | $50-100 | High | Most universally valued amenity |
| Dishwasher | $15-30 | High | Standard in Class A, premium in Class B/C |
| Central HVAC (vs window) | $25-60 | Medium | Climate-dependent |
| Updated kitchen (granite, SS) | $75-150 | High | Core value-add driver |
| Updated bathroom | $40-80 | Medium | Secondary to kitchen |
| Hardwood/LVP flooring | $25-50 | Medium | vs carpet |
| Private balcony/patio | $30-75 | Medium | Market-dependent |
| Garage parking (vs surface) | $75-200 | High | Climate and density dependent |
| EV charging | $25-50 | Low | Emerging; limited data |
| Smart home package | $20-40 | Low | Lock, thermostat, lighting |
| Pet-friendly (with pet rent) | $25-75 | Medium | Revenue line, not rent premium |
| Fitness center | $15-30 | Medium | Expected in Class A, premium in B |
| Pool | $20-40 | Medium | Seasonal markets: lower premium |
| Coworking/business center | $10-25 | Low | Post-COVID premium increasing |
| Package lockers | $5-15 | Medium | Increasingly expected, not premium |

### Deriving Premiums from Market Data

When benchmarks are unavailable, derive from paired comps:

```
Premium = Avg Rent (properties with amenity) - Avg Rent (properties without)
        - Adjustment for other differences

Example:
Avg rent, buildings with in-unit W/D: $1,450 (n=8 comps)
Avg rent, buildings without: $1,370 (n=6 comps)
Raw premium: $80/month
Adjusted for avg vintage difference (2 yrs newer): $80 - $20 = $60/month
```

## Worked 5-Comp Rent Comparison

**Subject Property:**
- 80-unit Class B multifamily, 1997 vintage, partial renovation (40 units done)
- Dallas, TX -- Lake Highlands submarket
- Unit mix: 40x 1BR/1BA (725 SF), 40x 2BR/2BA (1,050 SF)
- Renovated units: quartz counters, SS appliances, LVP flooring, updated bath
- Unrenovated units: original laminate, white appliances, carpet, original bath
- Current asking: $1,175 (1BR reno), $1,025 (1BR classic), $1,525 (2BR reno), $1,350 (2BR classic)

### Comp Grid

```
                    Comp 1          Comp 2          Comp 3          Comp 4          Comp 5
Property          Lakewood Villas  Highland Oaks   Greenville Xing  Royal Lane Apts  Skillman Place
Distance          0.4 mi          0.8 mi          1.2 mi          0.3 mi          1.5 mi
Units             120             64              200             96              72
Vintage           2000            1994            2018            1995            2003
Class             B               B-              A-              B               B+
Renovation        Fully reno 2023 Unrenovated     N/A (new)       Partial (60%)   Fully reno 2024
Occupancy         95%             88%             97%             93%             96%

1BR Asking        $1,210          $995            $1,425          $1,150          $1,250
1BR SF            750             700             780             720             740
1BR $/SF          $1.61           $1.42           $1.83           $1.60           $1.69

2BR Asking        $1,575          $1,295          $1,825          $1,490          $1,610
2BR SF            1,075           980             1,100           1,040           1,060
2BR $/SF          $1.47           $1.32           $1.66           $1.43           $1.52

Concessions       None            1 mo free       $500 gift card  None            Waived admin
                                                                                  ($150)
In-unit W/D       Yes             No              Yes             50% of units    Yes
Kitchen Quality   Quartz, SS      Original        Quartz, SS      Mixed           Quartz, SS
Flooring          LVP             Carpet          LVP             Mixed           LVP
Fitness           Yes             No              Yes (premium)   Yes             Yes
Pool              Yes             Yes (dated)     Resort-style    No              Yes
Parking           Garage avail    Surface only    Garage incl     Surface only    Garage avail
```

### Concession-Adjusted Effective Rents

```
                    Comp 1      Comp 2          Comp 3          Comp 4      Comp 5
1BR Face            $1,210      $995            $1,425          $1,150      $1,250
Concession/mo       $0          $83 (1 mo/12)   $42 ($500/12)   $0          $13 ($150/12)
1BR Effective       $1,210      $912            $1,383          $1,150      $1,237

2BR Face            $1,575      $1,295          $1,825          $1,490      $1,610
Concession/mo       $0          $108 (1 mo/12)  $42             $0          $13
2BR Effective       $1,575      $1,187          $1,783          $1,490      $1,597
```

### Amenity Adjustments to Subject

Adjustments bring each comp to subject-equivalent basis. Positive = comp has amenity subject lacks (adjust comp DOWN). Negative = subject has amenity comp lacks (adjust comp UP).

```
                        Comp 1      Comp 2      Comp 3      Comp 4      Comp 5
In-unit W/D             $0          +$75        $0          +$35        $0
  (Subject reno has;    (has)       (no: +$75)  (has)       (50%: +$35) (has)
   unreno does not)

Kitchen (reno units)    $0          +$100       $0          $0          $0
  (Subject reno =       (same)      (inferior)  (same)      (same)      (same)
   quartz/SS)

Kitchen (classic units) -$100       $0          -$100       -$50        -$100
  (Subject classic =    (superior)  (same)      (superior)  (mixed)     (superior)
   original)

Vintage/Condition       +$15        +$30        -$80        +$20        -$10
  (Age/quality diff)

Pool                    $0          +$10        -$30        +$30        $0
  (Subject has           (same)     (dated)     (resort)    (no pool)   (same)
   standard pool)

Parking                 -$40        +$40        -$75        +$40        -$40
  (Subject: surface;    (garage)    (surface)   (incl gar)  (surface)   (garage)
   adj for garage
   availability)

Size (per SF)           Minor       +$20        Minor       Minor       Minor
  (Normalize for SF     (similar)   (smaller)   (similar)   (similar)   (similar)
   differential)

Net Amenity Adj (reno)  -$25        +$275       -$185       +$125       -$50
Net Amenity Adj (class) -$125       +$175       -$285       +$75        -$150
```

### Adjusted Rents -- Renovated Units

```
                    Comp 1      Comp 2      Comp 3      Comp 4      Comp 5
1BR Effective       $1,210      $912        $1,383      $1,150      $1,237
Amenity Adj (reno)  -$25        +$275       -$185       +$125       -$50
Adjusted 1BR        $1,185      $1,187      $1,198      $1,275      $1,187
  (reno-equivalent)

2BR Effective       $1,575      $1,187      $1,783      $1,490      $1,597
Amenity Adj (reno)  -$25        +$275       -$185       +$125       -$50
Adjusted 2BR        $1,550      $1,462      $1,598      $1,615      $1,547
  (reno-equivalent)
```

### Adjusted Rents -- Classic (Unrenovated) Units

```
                    Comp 1      Comp 2      Comp 3      Comp 4      Comp 5
1BR Effective       $1,210      $912        $1,383      $1,150      $1,237
Amenity Adj (class) -$125       +$175       -$285       +$75        -$150
Adjusted 1BR        $1,085      $1,087      $1,098      $1,225      $1,087
  (classic-equiv)

2BR Effective       $1,575      $1,187      $1,783      $1,490      $1,597
Amenity Adj (class) -$125       +$175       -$285       +$75        -$150
Adjusted 2BR        $1,450      $1,362      $1,498      $1,565      $1,447
  (classic-equiv)
```

### Reconciliation

**Weighting by relevance (proximity, recency, similarity):**

| Comp | Weight | Rationale |
|---|---|---|
| Comp 4 (Royal Lane) | 30% | Closest (0.3 mi), same vintage, partial reno like subject |
| Comp 1 (Lakewood) | 25% | Very close (0.4 mi), same class, fully renovated baseline |
| Comp 5 (Skillman) | 20% | Recent reno, similar class, slightly farther |
| Comp 2 (Highland) | 15% | Unrenovated baseline useful for classic unit pricing |
| Comp 3 (Greenville) | 10% | Newest vintage, most dissimilar, largest adjustments |

**Indicated Market Rents:**

```
Renovated 1BR:  $1,275(.30) + $1,185(.25) + $1,187(.20) + $1,187(.15) + $1,198(.10) = $1,211
Renovated 2BR:  $1,615(.30) + $1,550(.25) + $1,547(.20) + $1,462(.15) + $1,598(.10) = $1,560
Classic 1BR:    $1,225(.30) + $1,085(.25) + $1,087(.20) + $1,087(.15) + $1,098(.10) = $1,126
Classic 2BR:    $1,565(.30) + $1,450(.25) + $1,447(.20) + $1,362(.15) + $1,498(.10) = $1,472

Subject Asking vs Market:
Renovated 1BR: $1,175 asking vs $1,211 market = 3.0% loss-to-lease (room to push)
Renovated 2BR: $1,525 asking vs $1,560 market = 2.2% loss-to-lease
Classic 1BR:   $1,025 asking vs $1,126 market = 9.0% loss-to-lease (significant upside)
Classic 2BR:   $1,350 asking vs $1,472 market = 8.3% loss-to-lease

Renovation premium derived:
1BR: $1,211 - $1,126 = $85/month (rent multiple on $8k reno cost = 8.5x annual = 9.4-yr payback)
2BR: $1,560 - $1,472 = $88/month (rent multiple on $10k reno cost = 10.6x annual = 9.5-yr payback)
```

## Key Principles

1. **Effective rent is the only rent that matters.** Face rent comparisons without concession adjustment are misleading. Always convert to effective.
2. **Concession discovery requires effort.** Databases capture 60-70% of concessions. Call leasing offices, mystery-shop, check websites weekly.
3. **Amenity adjustments are subjective.** Use paired-comp derivation when possible. When using benchmarks, apply conservatively and document assumptions.
4. **Occupancy signals pricing power.** A comp at 97% with no concessions is pricing below market. A comp at 88% with 2 months free is pricing above market. Adjust accordingly.
5. **Vintage is not condition.** A 2000-vintage fully renovated building may command higher rents than a 2015-vintage with deferred maintenance. Adjust for effective age.
6. **Loss-to-lease is your upside.** The gap between in-place and market effective rent is the organic growth runway. It requires no capital, just lease management discipline.
7. **Renovation premium payback under 8x annual is strong.** Above 12x is marginal. This ratio drives your unit renovation budget and scope decisions.
