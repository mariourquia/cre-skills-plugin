# Cost Segregation Methodology Reference

Complete reclassification rules, depreciation schedules, tax savings calculations, and recapture analysis. Worked example: $10M multifamily acquisition.

---

## 1. Component Reclassification Rules

### Recovery Period Categories

| Recovery Period | Asset Class | Examples | Method |
|---|---|---|---|
| 5-year | Personal property (1245) | Appliances, carpeting, cabinetry, window treatments, signage, security systems, decorative lighting | 200% DB / HY |
| 7-year | Personal property (1245) | Office furniture, fitness equipment, laundry machines, specialty HVAC units | 200% DB / HY |
| 15-year | Land improvements (1250) | Parking lots, sidewalks, landscaping, fencing, site lighting, stormwater systems, retaining walls | 150% DB / HY |
| 27.5-year | Residential real property (1250) | Structural components: walls, roof, foundation, plumbing risers, HVAC ductwork, electrical panels, elevators | SL / MM |
| 39-year | Nonresidential real property (1250) | Same as 27.5 but for office, retail, industrial, hospitality | SL / MM |

DB = Declining Balance. HY = Half-Year convention. SL = Straight-Line. MM = Mid-Month convention.

### Typical Reclassification Percentages by Property Type

| Property Type | 5-Year | 7-Year | 15-Year | 27.5/39-Year | Land |
|---|---|---|---|---|---|
| Multifamily (garden) | 10-15% | 2-4% | 8-12% | 55-65% | 15-20% |
| Multifamily (high-rise) | 8-12% | 2-3% | 5-8% | 62-70% | 12-18% |
| Office | 8-12% | 3-5% | 5-10% | 60-70% | 10-15% |
| Retail (strip) | 8-15% | 2-4% | 10-15% | 50-60% | 15-20% |
| Industrial/warehouse | 5-8% | 2-3% | 12-18% | 55-65% | 12-18% |
| Hospitality | 15-25% | 5-8% | 8-12% | 45-55% | 10-15% |

### Classification Decision Tree

```
Is the component structural (walls, roof, foundation)?
  YES -> 27.5/39-year
  NO -> Is it affixed to the building and integral to its operation?
    YES -> Is it a land improvement (exterior, below grade, site work)?
      YES -> 15-year
      NO -> Is it a building system (HVAC, plumbing, electrical)?
        YES -> Generally 27.5/39-year (but specialized components may qualify as 1245)
        NO -> 5 or 7-year personal property
    NO -> 5 or 7-year personal property
```

---

## 2. Bonus Depreciation Phase-Down Schedule

### Current Schedule (Tax Cuts and Jobs Act of 2017, as amended)

| Tax Year | Bonus Depreciation Rate | Applies To |
|---|---|---|
| 2017-2022 | 100% | 5, 7, 15-year property (new and used) |
| 2023 | 80% | 5, 7, 15-year property |
| 2024 | 60% | 5, 7, 15-year property |
| 2025 | 40% | 5, 7, 15-year property |
| 2026 | 20% | 5, 7, 15-year property |
| 2027+ | 0% | Bonus fully phased out |

### Impact on Year-1 Deduction

```
Year-1 deduction with bonus = (bonus_rate * reclassified_basis) + (regular_depreciation on remaining basis)

Regular first-year depreciation (half-year convention):
  5-year: 20.00% (200% DB)
  7-year: 14.29% (200% DB)
  15-year: 5.00% (150% DB)

Example with 60% bonus (2024):
  $1,000,000 of 5-year property:
    Bonus: $1,000,000 * 60% = $600,000
    Regular on remaining $400,000: $400,000 * 20% = $80,000
    Year-1 total: $680,000 (68% of basis)

  Without cost seg (all 27.5-year):
    $1,000,000 / 27.5 * (11.5/12) = $34,848  (mid-month convention, assuming July acquisition)
    Year-1 total: $34,848 (3.5% of basis)

  Acceleration factor: $680,000 / $34,848 = 19.5x
```

---

## 3. Year-by-Year Tax Savings Calculation

### Worked Example: $10M Multifamily Acquisition

**Assumptions:**
- Purchase price: $10,000,000
- Land value: 15% ($1,500,000, non-depreciable)
- Depreciable basis: $8,500,000
- Acquisition date: January 2025 (40% bonus depreciation)
- Marginal tax rate: 37% (federal ordinary) + 3.8% NIIT on passive income = 40.8% effective
- Hold period: 7 years

**Cost Segregation Study Results:**

```
Component              Basis          Recovery   % of Total
5-year property        $1,100,000     5-year     11.0%
7-year property        $300,000       7-year     3.0%
15-year property       $900,000       15-year    9.0%
27.5-year property     $6,200,000     27.5-year  62.0%
Land                   $1,500,000     N/A        15.0%
Total                  $10,000,000               100.0%
```

### Depreciation Schedule WITH Cost Segregation (40% Bonus, 2025)

**5-Year Property ($1,100,000):**
```
Bonus (40%): $1,100,000 * 0.40 = $440,000 (Year 1)
Remaining basis: $660,000

Year   MACRS Rate   Depreciation   Bonus    Total
1      20.00%       $132,000       $440,000 $572,000
2      32.00%       $211,200       --       $211,200
3      19.20%       $126,720       --       $126,720
4      11.52%       $76,032        --       $76,032
5      11.52%       $76,032        --       $76,032
6      5.76%        $38,016        --       $38,016
Total                                       $1,100,000
```

**7-Year Property ($300,000):**
```
Bonus (40%): $300,000 * 0.40 = $120,000 (Year 1)
Remaining basis: $180,000

Year   MACRS Rate   Depreciation   Bonus    Total
1      14.29%       $25,722        $120,000 $145,722
2      24.49%       $44,082        --       $44,082
3      17.49%       $31,482        --       $31,482
4      12.49%       $22,482        --       $22,482
5      8.93%        $16,074        --       $16,074
6      8.92%        $16,056        --       $16,056
7      8.93%        $16,074        --       $16,074
8      4.46%        $8,028         --       $8,028
Total                                       $300,000
```

**15-Year Property ($900,000):**
```
Bonus (40%): $900,000 * 0.40 = $360,000 (Year 1)
Remaining basis: $540,000

Year   MACRS Rate   Depreciation   Bonus    Total
1      5.00%        $27,000        $360,000 $387,000
2      9.50%        $51,300        --       $51,300
3      8.55%        $46,170        --       $46,170
4      7.70%        $41,580        --       $41,580
5      6.93%        $37,422        --       $37,422
6      6.23%        $33,642        --       $33,642
7      5.90%        $31,860        --       $31,860
(continues through year 16)
```

**27.5-Year Property ($6,200,000):**
```
Annual straight-line: $6,200,000 / 27.5 = $225,455
Year 1 (mid-month, Jan acquisition): $225,455 * (11.5/12) = $215,978
Years 2-27: $225,455
Year 28: $225,455 * (0.5/12) = $9,394
```

### Combined Depreciation Schedule

| Year | 5-Yr | 7-Yr | 15-Yr | 27.5-Yr | Total Depr | Tax Savings (40.8%) |
|---|---|---|---|---|---|---|
| 1 | $572,000 | $145,722 | $387,000 | $215,978 | $1,320,700 | $538,846 |
| 2 | $211,200 | $44,082 | $51,300 | $225,455 | $532,037 | $217,071 |
| 3 | $126,720 | $31,482 | $46,170 | $225,455 | $429,827 | $175,369 |
| 4 | $76,032 | $22,482 | $41,580 | $225,455 | $365,549 | $149,144 |
| 5 | $76,032 | $16,074 | $37,422 | $225,455 | $354,983 | $144,833 |
| 6 | $38,016 | $16,056 | $33,642 | $225,455 | $313,169 | $127,773 |
| 7 | $0 | $16,074 | $31,860 | $225,455 | $273,389 | $111,543 |

**7-Year cumulative depreciation: $3,589,654**
**7-Year cumulative tax savings: $1,464,579**

### WITHOUT Cost Segregation (All 27.5-Year)

```
Depreciable basis: $8,500,000
Annual depreciation: $8,500,000 / 27.5 = $309,091
Year 1 (mid-month): $296,212
Years 2-7: $309,091/year

7-year cumulative: $296,212 + (6 * $309,091) = $2,150,758
7-year cumulative tax savings: $2,150,758 * 40.8% = $877,509
```

### Incremental Benefit of Cost Segregation

```
Incremental depreciation (7 years): $3,589,654 - $2,150,758 = $1,438,896
Incremental tax savings (7 years): $1,464,579 - $877,509 = $587,070
Cost of study: ~$12,000

NPV of incremental savings (at 8% discount rate):
  Year 1: ($538,846 - $120,855) / 1.08 = $386,928
  Year 2: ($217,071 - $126,109) / 1.08^2 = $77,967
  Year 3: ($175,369 - $126,109) / 1.08^3 = $39,074
  Year 4: ($149,144 - $126,109) / 1.08^4 = $16,936
  Year 5: ($144,833 - $126,109) / 1.08^5 = $12,744
  Year 6: ($127,773 - $126,109) / 1.08^6 = $1,048
  Year 7: ($111,543 - $126,109) / 1.08^7 = -$8,503
  NPV: $526,194 (net of $12,000 study cost = $514,194)
```

The cost seg study generates $514K in NPV from accelerated tax timing, far exceeding the $12K study cost. Note: total depreciation over the full asset life is the same with or without cost seg. The benefit is purely from time value of earlier deductions.

---

## 4. Depreciation Recapture at Disposition

### Section 1245 Recapture (5-Year and 7-Year Property)

All gain on Section 1245 property is recaptured as ordinary income up to the amount of depreciation taken.

```
Section 1245 recapture = min(gain_on_1245_property, total_1245_depreciation_taken)
Tax rate: 37% (ordinary income rate)
```

### Section 1250 Recapture (15-Year and 27.5/39-Year Property)

For real property, "unrecaptured Section 1250 gain" is taxed at 25% (not ordinary rates).

```
Unrecaptured 1250 gain = min(gain_on_1250_property, total_1250_depreciation_taken)
Tax rate: 25%

Any gain above accumulated depreciation = long-term capital gain at 20% + 3.8% NIIT
```

### Worked Example: Disposition After 7-Year Hold

Sale price: $13,000,000
Original purchase price: $10,000,000
Selling costs (3%): $390,000
Net sale proceeds: $12,610,000

```
Adjusted basis calculation:
  Original basis: $10,000,000
  Less: accumulated depreciation (7 years, with cost seg): $3,589,654
  Adjusted basis: $6,410,346

Total gain: $12,610,000 - $6,410,346 = $6,199,654

Gain allocation by component:

1245 Property (5-year + 7-year):
  Original basis: $1,400,000
  Depreciation taken: $1,187,722  (all of 5-yr fully depreciated + 7-yr mostly)
  Remaining basis: $212,278
  Allocated sale proceeds (pro-rata): $1,400,000 * ($13M/$10M) = $1,820,000
  Gain: $1,820,000 - $212,278 = $1,607,722
  1245 recapture (ordinary): min($1,607,722, $1,187,722) = $1,187,722 at 37% = $439,457
  Remaining gain: $1,607,722 - $1,187,722 = $420,000 at 20% + 3.8% = $99,960

1250 Property (15-year + 27.5-year):
  Original basis: $7,100,000
  Depreciation taken: $2,401,932
  Remaining basis: $4,698,068
  Allocated sale proceeds: $7,100,000 * ($13M/$10M) = $9,230,000
  Gain: $9,230,000 - $4,698,068 = $4,531,932
  Unrecaptured 1250 (25%): min($4,531,932, $2,401,932) = $2,401,932 at 25% = $600,483
  Remaining gain: $4,531,932 - $2,401,932 = $2,130,000 at 23.8% = $506,940

Land:
  Basis: $1,500,000
  Allocated proceeds: $1,500,000 * 1.3 = $1,950,000
  Gain: $450,000 at 23.8% = $107,100

Total tax at disposition:
  1245 recapture (ordinary):         $439,457
  1245 excess (LTCG):                $99,960
  1250 recapture (25%):              $600,483
  1250 excess (LTCG):                $506,940
  Land gain (LTCG):                  $107,100
  TOTAL TAX:                         $1,753,940
```

### Recapture Tax WITHOUT Cost Segregation

```
All 27.5-year property: $8,500,000 basis, $2,150,758 depreciation taken
Adjusted basis: $10,000,000 - $2,150,758 = $7,849,242
Total gain: $12,610,000 - $7,849,242 = $4,760,758

  1250 recapture: $2,150,758 at 25% = $537,690
  Excess gain: $2,610,000 at 23.8% = $621,180
  Total tax: $1,158,870
```

### Net Benefit of Cost Segregation Over Full Hold

```
Incremental tax savings during hold: $587,070
Additional recapture tax at sale: $1,753,940 - $1,158,870 = $595,070
Net nominal difference: $587,070 - $595,070 = -$8,000

But the time value matters:
  Tax savings received in years 1-7 (PV at 8%): ~$526,194
  Additional recapture paid in year 7 (PV at 8%): $595,070 / 1.08^7 = $347,134
  Net PV benefit: $526,194 - $347,134 = $179,060
```

The cost seg study is NPV-positive even after recapture, because the tax savings come early and the recapture is paid later.

---

## 5. Breakeven Hold Period

### Definition

The minimum hold period at which the NPV of cost segregation tax acceleration (net of incremental recapture) is positive.

### Formula

```
Breakeven: find t where NPV(incremental_savings[1..t]) = PV(incremental_recapture[t])
```

### Rules of Thumb

| Bonus Depreciation Rate | Breakeven Hold Period |
|---|---|
| 100% (2022) | 1-2 years |
| 80% (2023) | 2-3 years |
| 60% (2024) | 2-3 years |
| 40% (2025) | 3-4 years |
| 20% (2026) | 4-5 years |
| 0% (2027+) | 5-7 years |

For the $10M multifamily example at 40% bonus, the breakeven is approximately 3 years. Holds shorter than 3 years may not benefit from cost seg after recapture.

---

## 6. Common Errors

| Error | Consequence |
|---|---|
| Applying bonus depreciation to 27.5/39-year property | Bonus only applies to 5, 7, and 15-year property; real property is excluded (unless QIP at 15 years) |
| Ignoring recapture in after-tax return models | Overstates after-tax IRR by 50-200bp depending on hold period and reclassification percentage |
| Using cost seg on short holds without NPV analysis | The acceleration benefit may not exceed incremental recapture tax on a present-value basis for holds under 3 years |
| Forgetting state tax conformity | Not all states conform to federal bonus depreciation; California, for example, does not allow bonus |
| Treating land improvements as personal property | 15-year land improvements are Section 1250 property (25% recapture), not 1245 (37% recapture) |
| Applying residential rate (27.5yr) to commercial property | Commercial is 39 years; using 27.5 for a non-residential property accelerates depreciation improperly |
| Ignoring QIP eligibility | Qualified Improvement Property (interior, non-structural) qualifies for 15-year / bonus treatment since the CARES Act correction |
