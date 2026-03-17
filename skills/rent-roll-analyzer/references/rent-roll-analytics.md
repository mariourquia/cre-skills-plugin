# Rent Roll Analytics Reference

Formulas, methodologies, and worked examples for rent roll analysis in CRE underwriting. All examples use a 30-tenant office/flex property with 150,000 SF of rentable area.

---

## 1. Loss-to-Lease Waterfall

Loss-to-lease (LTL) quantifies the gap between in-place contract rents and achievable market rents. It represents embedded upside (or downside, if negative).

### Definitions

```
Contract Rent:    The rent currently being paid per the lease agreement
Market Rent:      The rent achievable for comparable space in the submarket today
Loss-to-Lease:    Market Rent - Contract Rent  (positive = upside)
Gain-to-Lease:    Contract Rent - Market Rent  (positive = tenant overpaying)
Capture Rate:     Percentage of LTL realizable upon lease renewal or new lease
Capture Schedule: Timeline over which LTL is captured (aligned with lease expirations)
```

### Formula

```
Total LTL = sum_i [(market_rent_i - contract_rent_i) * SF_i]

for all tenants where market_rent_i > contract_rent_i

LTL as % of contract revenue = Total LTL / Total Contract Revenue
```

### Worked Waterfall

30-tenant rent roll (abbreviated to 6 representative tenants):

```
Tenant          SF      Contract    Market    LTL/SF    LTL Annual    Expiry
                        $/SF/yr     $/SF/yr
Tenant A     25,000      $28.00     $34.00     $6.00     $150,000     2026-09
Tenant B     18,000      $32.00     $34.00     $2.00      $36,000     2027-03
Tenant C     15,000      $35.00     $34.00    -$1.00     -$15,000     2028-06
Tenant D     12,000      $26.00     $34.00     $8.00      $96,000     2026-12
Tenant E     10,000      $30.00     $34.00     $4.00      $40,000     2027-09
Tenant F      8,000      $38.00     $34.00    -$4.00     -$32,000     2029-01
Remaining    62,000      $31.50     $34.00     $2.50     $155,000     various
TOTAL       150,000      $30.73     $34.00     $3.27     $430,000
```

```
Total Contract Revenue:  150,000 * $30.73 = $4,609,500
Total Market Revenue:    150,000 * $34.00 = $5,100,000
Gross LTL:               $490,500
Net LTL (excluding gain-to-lease tenants): $430,000 + $47,000 remaining = $477,000
LTL as % of contract revenue: $490,500 / $4,609,500 = 10.6%
```

### Capture Schedule

LTL is captured only as leases expire or tenants renew at market rates. Model the capture aligned with the rollover schedule:

```
Year 1 (2026):
  Tenant A expires (Sep): 25,000 SF * $6.00 * 3/12 partial year = $37,500
  Tenant D expires (Dec): 12,000 SF * $8.00 * 0/12 = $0 (captured in Year 2)
  Year 1 LTL captured: $37,500

Year 2 (2027):
  Tenant A full year: 25,000 * $6.00 = $150,000
  Tenant D full year: 12,000 * $8.00 = $96,000
  Tenant B expires (Mar): 18,000 * $2.00 * 9/12 = $27,000
  Tenant E expires (Sep): 10,000 * $4.00 * 3/12 = $10,000
  Year 2 LTL captured: $283,000

Year 3 (2028):
  Prior tenants full year carry-forward
  Tenant B full year: 18,000 * $2.00 = $36,000
  Tenant E full year: 10,000 * $4.00 = $40,000
  Year 3 incremental: $76,000
```

Apply a capture rate (typically 85-95% for strong markets, 70-85% for weak markets) to reflect renewal probability and potential concessions:

```
Adjusted capture = Gross capture * 90% capture rate
Year 1: $37,500 * 0.90 = $33,750
Year 2: $283,000 * 0.90 = $254,700
Year 3: $76,000 * 0.90 = $68,400
```

---

## 2. Weighted Average Lease Term (WALT)

WALT measures the average remaining lease duration, weighted by economic significance. Two methods serve different purposes.

### Rent-Weighted WALT

Weights by annual rent contribution. Tells you: "On average, how long is the rental income secured?"

```
WALT_rent = sum_i (remaining_term_i * annual_rent_i) / sum_i (annual_rent_i)
```

### SF-Weighted WALT

Weights by square footage. Tells you: "On average, how long is the space committed?"

```
WALT_sf = sum_i (remaining_term_i * SF_i) / sum_i (SF_i)
```

### Worked Example

Analysis date: 2026-01-01

```
Tenant     SF      Annual Rent    Expiry       Remaining (yrs)
A        25,000    $700,000       2026-09-30      0.75
B        18,000    $576,000       2027-03-31      1.25
C        15,000    $525,000       2028-06-30      2.50
D        12,000    $312,000       2026-12-31      1.00
E        10,000    $300,000       2027-09-30      1.75
F         8,000    $304,000       2029-01-31      3.08
Remaining 62,000  $1,953,000      various         3.50 (avg)
TOTAL    150,000  $4,670,000
```

Rent-weighted WALT:

```
WALT_rent = (0.75*700,000 + 1.25*576,000 + 2.50*525,000 + 1.00*312,000
           + 1.75*300,000 + 3.08*304,000 + 3.50*1,953,000) / 4,670,000

= (525,000 + 720,000 + 1,312,500 + 312,000 + 525,000 + 936,320 + 6,835,500)
  / 4,670,000

= 11,166,320 / 4,670,000

= 2.39 years
```

SF-weighted WALT:

```
WALT_sf = (0.75*25,000 + 1.25*18,000 + 2.50*15,000 + 1.00*12,000
          + 1.75*10,000 + 3.08*8,000 + 3.50*62,000) / 150,000

= (18,750 + 22,500 + 37,500 + 12,000 + 17,500 + 24,640 + 217,000) / 150,000

= 349,890 / 150,000

= 2.33 years
```

### Interpretation

When WALT_rent > WALT_sf: larger tenants (by rent) have longer leases. This is typically favorable -- anchor tenants provide stability.

When WALT_rent < WALT_sf: smaller spaces have longer terms, but larger rent-paying tenants expire sooner. Higher near-term rollover risk.

In this example, WALT_rent (2.39) > WALT_sf (2.33), indicating larger rent contributors have slightly longer remaining terms. Both values are relatively short -- significant rollover occurs within 2.5 years.

### WALT Benchmarks

| Property Type | Healthy WALT | Caution | Concern |
|---|---|---|---|
| Office (multi-tenant) | > 4.0 years | 2.5-4.0 | < 2.5 |
| Industrial | > 5.0 years | 3.0-5.0 | < 3.0 |
| Retail (anchored) | > 6.0 years | 4.0-6.0 | < 4.0 |
| Retail (strip/in-line) | > 3.0 years | 2.0-3.0 | < 2.0 |

---

## 3. Tenant Concentration Risk: Herfindahl-Hirschman Index (HHI)

### Formula

```
HHI = sum_i (s_i)^2

where s_i = tenant_i_share of total rent (as decimal, 0 to 1)

HHI range: 1/N (perfectly equal) to 1.0 (single tenant)
```

For practical CRE use, express shares as percentages and HHI on a 0-10,000 scale:

```
HHI = sum_i (s_i_pct)^2

where s_i_pct = tenant share as percentage (0 to 100)
HHI range: 10,000/N to 10,000
```

### Worked Example

```
Tenant     Annual Rent    Share (%)    Share^2
A           $700,000       14.99%       224.7
B           $576,000       12.33%       152.0
C           $525,000       11.24%       126.3
D           $312,000        6.68%        44.6
E           $300,000        6.42%        41.2
F           $304,000        6.51%        42.4
Remaining   $1,953,000     41.82%       --*
TOTAL       $4,670,000     100.00%

*For the "remaining" 62,000 SF, break into individual tenants.
Assume 15 tenants averaging $130,200 each (2.79% share each):
  Per tenant: (2.79)^2 = 7.78
  15 tenants: 15 * 7.78 = 116.7

HHI = 224.7 + 152.0 + 126.3 + 44.6 + 41.2 + 42.4 + 116.7 = 747.9
```

### HHI Interpretation

| HHI Range | Concentration | Implication |
|---|---|---|
| < 500 | Low | Well-diversified; no single tenant dominates |
| 500-1,000 | Moderate | Manageable; 2-3 tenants matter but not critical |
| 1,000-1,500 | Elevated | Top 1-2 tenants are significant; credit analysis required |
| 1,500-2,500 | High | Approaching single-tenant risk profile |
| > 2,500 | Very High | Essentially single-tenant net lease |

Our example at 748 is moderate concentration. Tenant A (15.0%) and B (12.3%) are the primary concentration sources. Losing either would create meaningful vacancy but not catastrophic loss.

### Top-Tenant Credit Overlay

For tenants exceeding 10% of rent, always assess:

```
- Credit rating (if public) or financial statement review (if private)
- Industry exposure (cyclical vs. defensive)
- Lease guaranty structure (corporate vs. individual vs. none)
- Remaining term relative to WALT
- Renewal likelihood based on fit-out investment and alternatives
```

---

## 4. Rollover Schedule Construction

### Methodology

Group lease expirations by year. Calculate total SF and rent rolling in each year.

```
Year    SF Expiring    % of Total SF    Rent Expiring    % of Total Rent
2026      37,000          24.7%           $1,012,000        21.7%
2027      28,000          18.7%           $876,000          18.8%
2028      15,000          10.0%           $525,000          11.2%
2029      20,000          13.3%           $658,000          14.1%
2030      18,000          12.0%           $594,000          12.7%
2031+     32,000          21.3%           $1,005,000        21.5%
TOTAL    150,000         100.0%          $4,670,000        100.0%
```

### Rollover Risk Assessment

Flag any year with >20% of total rent expiring as a concentration year.

```
2026: 21.7% of rent expires -- ELEVATED RISK
  Tenant A ($700,000) and Tenant D ($312,000) both expire
  Combined: 37,000 SF at risk of vacancy or re-leasing below market

Mitigation analysis:
  - Tenant A: 25,000 SF, below market by $6.00/SF. High renewal probability
    (embedded loss-to-lease provides negotiation room).
  - Tenant D: 12,000 SF, below market by $8.00/SF. Good space, should renew.
  - Estimated renewal probability: 75-80% for both.
  - Worst case: 37,000 SF vacant for 6-9 months = $600K-$900K revenue loss.
```

### Leasing Cost Assumptions for Rollover

When tenants expire, budget for leasing costs whether they renew or not:

```
Renewal:
  Leasing commission: $1.00-$2.00/SF (one-time)
  TI allowance: $5.00-$15.00/SF (office renewal)
  Free rent: 0-2 months

New lease (replacement tenant):
  Leasing commission: $3.00-$5.00/SF (one-time)
  TI allowance: $20.00-$50.00/SF (office new tenant)
  Free rent: 2-6 months
  Downtime: 3-12 months vacant

For 2026 rollover (37,000 SF), assuming 75% renew, 25% turn over:
  Renewals (27,750 SF):
    Commissions: 27,750 * $1.50 = $41,625
    TI: 27,750 * $10.00 = $277,500
  New leases (9,250 SF):
    Commissions: 9,250 * $4.00 = $37,000
    TI: 9,250 * $35.00 = $323,750
    Vacancy loss (6 months): 9,250 * $34.00 / 2 = $157,250
  Total 2026 rollover cost: $837,125
```

---

## 5. Effective Rent Calculation

### Gross vs. Net Effective Rent

Headline rent is not the economic rent. Concessions, TI, and free rent reduce the landlord's effective yield.

```
Net Effective Rent = (Total Rent Collected - Concessions - TI Amortized - Free Rent Value)
                     / (Lease Term in Years * SF)
```

### Worked Example

Tenant B: 18,000 SF, 5-year lease, $32.00/SF/yr headline

```
Gross rent over term:     18,000 * $32.00 * 5 = $2,880,000
Less: 2 months free rent: 18,000 * $32.00 * 2/12 = -$96,000
Less: TI allowance:       18,000 * $20.00 = -$360,000
Less: leasing commission: 18,000 * $3.00 = -$54,000

Net landlord proceeds:    $2,370,000
Net effective rent:       $2,370,000 / (5 * 18,000) = $26.33/SF/yr
Effective discount:       ($32.00 - $26.33) / $32.00 = 17.7%
```

The headline rent of $32.00 overstates the actual economic yield by $5.67/SF (17.7%). When comparing tenant rents to market, always compare on a net effective basis.

---

## 6. Occupancy Metrics

### Physical vs. Economic Occupancy

```
Physical occupancy = occupied_SF / total_rentable_SF
Economic occupancy = actual_collected_rent / (total_rentable_SF * market_rent)
```

Economic occupancy is always lower than or equal to physical occupancy because it captures:
- Below-market in-place rents
- Free rent periods
- Non-paying tenants
- Concessions

```
Example:
  Physical occupancy: 150,000 / 150,000 = 100%
  Contract rent collected: $4,609,500
  Market rent potential: $5,100,000
  Economic occupancy: $4,609,500 / $5,100,000 = 90.4%
```

A 9.6% gap between physical and economic occupancy is entirely due to loss-to-lease. This is the embedded revenue upside in the rent roll.

---

## 7. Common Errors

1. **Using asking rents instead of achieved rents for market**: Asking rents are aspirational. Achieved (effective) rents, adjusted for concessions, are the correct market benchmark. In soft markets, the gap between asking and effective can be 10-20%.

2. **Ignoring below-grade or storage SF**: Rent rolls sometimes include basement storage or mezzanine space at nominal rents. These inflate physical occupancy without proportional revenue. Separate rentable office/retail SF from ancillary space.

3. **Treating month-to-month as vacant**: Month-to-month tenants are occupied and paying rent, but their term is effectively zero. Include them in occupancy but flag them as rollover risk with 0.0 years remaining in WALT.

4. **Using average rent instead of weighted average**: Simple average rent (sum of $/SF divided by tenant count) gives equal weight to a 500 SF tenant and a 50,000 SF tenant. Always weight by SF or by annual rent.

5. **Miscounting remaining term**: Remaining term should be calculated from the analysis date, not the lease commencement date. A lease signed 3 years ago with a 5-year term has 2 years remaining, not 5.

6. **Ignoring tenant options**: Renewal options, expansion options, and early termination rights materially affect rollover risk. A tenant with a 2-year remaining term and two 5-year renewal options has a different risk profile than one with 2 years and no options.

7. **Not adjusting for CPI escalators**: Leases with annual CPI escalations will produce different contract rents next year than they show today. Incorporate scheduled escalations into the rent roll projection.

---

## 8. Quick-Reference Formulas

```
Loss-to-Lease (total) = sum[(market_rent - contract_rent) * SF] for all tenants
LTL %                  = Total LTL / Total Contract Revenue
WALT (rent-weighted)   = sum(remaining_term * annual_rent) / sum(annual_rent)
WALT (SF-weighted)     = sum(remaining_term * SF) / sum(SF)
HHI                    = sum(share_pct^2)
Physical Occupancy     = occupied_SF / rentable_SF
Economic Occupancy     = collected_rent / (rentable_SF * market_rent)
Net Effective Rent     = (gross_rent - free_rent - TI - commission) / (term * SF)
Rollover Exposure      = expiring_rent_year_n / total_rent
```
