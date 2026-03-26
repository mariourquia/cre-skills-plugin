# Option Valuation Methodology Reference

## Overview

Quantitative methods for valuing lease options from the landlord's perspective.
Covers termination fee calculation, renewal option value impact on cap rate,
ROFO vs. ROFR value comparison, and expansion/contraction fee benchmarks.
Every formula includes a worked example and common application errors.

---

## 1. Termination Fee Calculation Methodology

### Core Framework

A termination fee must make the landlord whole for the economic loss caused by early
termination. It has two floors -- use whichever is higher:

```
T_fee = max(hard_cost_recovery, NPV_breakeven)
```

### Hard Cost Recovery Floor

```
hard_cost_recovery = unamortized_TI
                   + unamortized_LC
                   + estimated_re_leasing_TI
                   + estimated_re_leasing_LC
                   + estimated_free_rent_cost

unamortized_TI = TI_psf * SF * (months_remaining / original_term_months)
unamortized_LC = LC_psf * SF * (months_remaining / original_term_months)

estimated_re_leasing_TI: use current market TI allowance for similar space
estimated_re_leasing_LC: use local market leasing commission benchmark
estimated_free_rent_cost: estimated months_of_free_rent * monthly_rent
```

### NPV Breakeven Floor

```
NPV_breakeven = NPV(remaining_in_place_rent) - NPV(projected_replacement_income)

NPV(remaining_in_place_rent):
  sum[t=1..T_remaining] [monthly_rent / (1+r/12)^t]

NPV(projected_replacement_income):
  - assumes N months of vacancy before new tenant occupies
  - new rent based on current market estimate
  sum[t=(N+1)..T_remaining] [new_monthly_rent / (1+r/12)^t]

Discount rate r: landlord's cost of capital (typically 7-9%)
```

### Worked Example

```
Property: 15,000 SF office lease
Remaining term: 48 months
In-place rent: $42/SF/year ($52,500/month)
Market rent today: $46/SF/year ($57,500/month)
TI at lease inception: $65/SF (total $975,000, original 10-year term)
LC at lease inception: $16/SF (total $240,000, original 10-year term)
Months elapsed: 72 of 120 months (60% complete)
Discount rate: 8%

Step 1: Hard cost recovery

  Unamortized TI:
    $975,000 * (48/120) = $390,000

  Unamortized LC:
    $240,000 * (48/120) = $96,000

  Re-leasing TI (current market, Class B office, 15K SF):
    $55/SF * 15,000 = $825,000

  Re-leasing LC (6% of aggregate rent, 5-year replacement):
    6% * $46 * 15,000 * 5 = $207,000

  Free rent cost (3 months estimated):
    3 * $57,500 = $172,500

  Hard cost recovery total: $390,000 + $96,000 + $825,000 + $207,000 + $172,500
                           = $1,690,500

Step 2: NPV breakeven

  NPV of remaining in-place rent (48 months at $52,500/month, 8% annual):
    Monthly rate r = 0.08/12 = 0.006667
    NPV = $52,500 * [(1 - (1.006667)^-48) / 0.006667]
        = $52,500 * 40.962
        = $2,150,505

  NPV of projected replacement income (6 months vacancy, then $57,500/month for 42):
    NPV_new = $57,500 * [(1 - (1.006667)^-42) / 0.006667] / (1.006667)^6
            = $57,500 * 36.605 / 1.0408
            = $57,500 * 35.169
            = $2,022,218

  NPV breakeven = $2,150,505 - $2,022,218 = $128,287

Step 3: Fee determination

  max($1,690,500, $128,287) = $1,690,500

  Minimum acceptable termination fee: $1,690,500
  Negotiating target: $1,690,500 (hard cost recovery dominates here)

Note: NPV breakeven is low because replacement rent > in-place rent.
In a tenant's market where replacement rent < in-place rent, NPV
breakeven would dominate and the fee would be significantly higher.
```

### Termination Fee Benchmarks by Lease Stage

```
| Stage of Termination       | Fee Range as % of Remaining Rent | Notes                    |
|----------------------------|----------------------------------|--------------------------|
| Early (first 30% of term)  | Not granted (or 80-100%)         | TI barely amortized      |
| Mid-term (30-70% of term)  | 40-60%                           | Most common window       |
| Late-term (last 30%)       | 15-30%                           | TI mostly amortized      |
| Last 24 months             | 0-10% (or just don't grant it)  | Tenant effectively won't renew |

Note: These are as % of gross remaining rent (face value, not NPV).
Always verify against the hard cost floor before accepting.
```

---

## 2. Renewal Option Value Impact on Cap Rate

### Mechanism

A renewal option does two things simultaneously:
1. It increases WALT certainty (value-positive)
2. If below-market, it reduces effective rent (value-negative)

The net impact on cap rate depends on which effect dominates.

### WALT Certainty Premium

```
A committed renewal option reduces re-leasing risk premium in cap rate:

WALT_extension = option_years * exercise_probability * (tenant_sf / total_nra)

Cap rate compression from WALT extension:
  +0.25 yrs WALT:  -3 to -5 bps
  +0.50 yrs WALT:  -5 to -10 bps
  +1.00 yr WALT:   -8 to -15 bps

Example:
  10,000 SF tenant, 1 renewal option (5 years), 60% exercise probability
  Building: 80,000 SF NRA
  WALT extension = 5 * 0.60 * (10,000/80,000) = 0.375 years
  Cap rate compression: -5 bps
```

### Below-Market Renewal Value Transfer

```
If renewal rate is fixed below projected FMV:

Annual NOI deficit (per year of renewal):
  = (projected_market_rent - fixed_renewal_rent) * SF

Value transfer to tenant (capitalized):
  = annual_NOI_deficit / in_place_cap_rate

Example:
  Fixed renewal rate: $45/SF
  Projected market rent at exercise (in 7 years): $54/SF (3% annual growth)
  Delta: $9/SF/year
  Tenant SF: 10,000
  Annual NOI delta: $90,000
  Capitalized value transfer: $90,000 / 0.055 = $1,636,364

  This transfer is CERTAIN if tenant exercises -- model it as a contingent liability.
```

### Net Cap Rate Impact by Renewal Type

```
Renewal Type                    Cap Rate Impact    Notes
------------------------------  ----------------   --------------------------
FMV with floor (no ceiling)     -5 to -8 bps       Best case for landlord
FMV bilateral (floor + ceiling) -3 to -5 bps       Balanced; acceptable
Fixed at market (current)       +5 to +15 bps      Risk rises as exercise approaches
Fixed below market (by >10%)    +10 to +25 bps     Significant value transfer
CPI-based                       -2 to +5 bps       Depends on CPI/market spread
Unlimited renewals              +20 to +40 bps     Creates effectively perpetual tenancy

Source: CBRE/JLL valuation guidelines; actual impact varies by appraiser judgment.
```

---

## 3. ROFO vs. ROFR Value Comparison

### Value to Tenant

```
ROFO (Right of First Offer):
  Tenant sees the space first, at landlord's initial offering price.
  Tenant can negotiate from that price.
  If tenant declines, landlord markets freely.
  Value to tenant: moderate -- they get first look and negotiating leverage.

ROFR (Right of First Refusal):
  Tenant can match any third-party offer, on identical terms.
  Effectively a veto on competing tenants for that space.
  Value to tenant: high -- they can wait for a specific price to emerge,
  then match it without negotiating.
```

### Cost to Landlord (NOI and Value)

```
ROFO cost:
  Marketing delay: landlord must deliver offer to tenant first (5-10 days).
  If tenant declines, landlord proceeds normally.
  Third-party deal probability: minimal impact (most deals not affected).
  Cap rate impact: +3 to +8 bps per ROFO on a major tenant.
  Qualifying note: impact higher if ROFO space = large % of building.

ROFR cost:
  Third-party market chill: parties considering adjacent space know a
  match right exists. Some walk away rather than negotiate for a space
  they may lose. This reduces competing offers and may depress pricing.
  Estimated market value impact: -5 to -15% of adjacent space value
  (because the space cannot be freely marketed).
  Cap rate impact: +8 to +18 bps per ROFR on adjacent space.
  For building sale ROFR: +15 to +30 bps (reduces buyer universe).
```

### Decision Framework for Asset Manager

```
Situation                                   Recommend
-----------------------------------------  ----------------------------------
Tenant is anchor or major (>20% NRA)       ROFO acceptable; ROFR negotiable
Tenant is small inline (<5% NRA)            No ROFO, no ROFR
Adjacent space is likely to be vacated      ROFO only; limit damage
Adjacent space is already leased            Grant ROFO (triggers only on vacancy)
Tenant market, retention critical           ROFR may be required to win deal
Building sale planned in 5-7 years         No building-sale ROFR without legal review
Lender-constrained property                 Confirm lender consent for any ROFR
```

---

## 4. Expansion and Contraction Fee Benchmarks by Market Tier

### Expansion Option Benchmarks

```
Expansion Right Type      Gateway         Secondary       Tertiary
---------------------    ----------      -----------     ----------
Must-take (committed)    Rent premium    No premium      Discount possible
                         +3-5%           Market          Market - 5%
ROFO response window     10 days         15 days         20 days
ROFR response window     5 days          7-10 days       10 days
ROFR match precision     Identical terms Identical terms Minor deviations ok

TI for expansion space:
  New lease expansion:   Full market TI ($45-85/SF office; $10-30/SF industrial)
  Renewal expansion:     Refresh TI ($15-30/SF office; $5-10/SF industrial)
  Must-take at lease:    Committed TI in original lease (market rate at commencement)
```

### Contraction Right Fee Benchmarks

```
Market Tier    Typical Contraction Fee Formula                    Notice Period
-----------    -----------------------------------------------   ---------------
Gateway        Unamortized TI + LC + 6 months rent               15-18 months
Secondary      Unamortized TI + LC + 3-6 months rent             12-15 months
Tertiary       Unamortized TI + LC (no rent penalty common)      12 months

Maximum % of space contractible by type:
  Office:      25-33% of tenant's NRA (floor-by-floor basis)
  Retail:      Not typical (anchor space not divisible)
  Industrial:  20-30% of tenant's NRA (dock door allocation)
  Medical:     Rarely granted (specialized buildout)

Timing (earliest the right can be exercised):
  Standard:    After 40% of lease term has elapsed
  Tenant mkt:  After 30% of lease term
  Landlord mkt: After 50-60% of lease term (or not at all)
```

### Termination Right Fee Benchmarks by Market Tier and Timing

```
Market Tier    Mid-Term Termination Fee           Late-Term Termination Fee
-----------    --------------------------------   ---------------------------------
Gateway        Unamortized TI+LC + 12 mo rent    Unamortized TI+LC + 6 mo rent
Secondary      Unamortized TI+LC + 9 mo rent     Unamortized TI+LC + 3-6 mo rent
Tertiary       Unamortized TI+LC + 6 mo rent     Unamortized TI+LC only

Note: In tenant markets, fees compress 20-40% below these benchmarks.
In landlord markets, termination rights may not be granted at all.
Always calculate against the hard cost floor regardless of market benchmarks.
```

### Purchase Option Benchmarks

```
Purchase Option Type             Terms                         When to Accept
------------------------------  ----------------------------  -----------------
FMV at exercise (appraisal)     Preferred. Landlord picks     Always acceptable
                                 appraiser from approved list.
FMV with tenant right to match   Bilateral FMV determination  Acceptable if process
                                 with dispute to arbitration   is defined
Fixed price (at lease signing)  Almost never acceptable.      Only in single-tenant
                                 Locks in today's value for   net lease with minimal
                                 a future exercise.            capital deployed

Exercise window:
  Standard: during the last 2 years of the initial term or any renewal term
  Avoid: right to purchase at any time (creates perpetual option)
  Avoid: right to purchase upon lease expiration without clear process

Lender requirement: any purchase option requires lender consent.
  Lenders may prohibit or require subordination to mortgage.
  Always confirm before granting.
```

---

## 5. Quick Reference: Option Value Summary Table

```
Option Type      Value to Tenant    Cost to Landlord    Cap Rate Impact
-------------    ---------------    ----------------    ----------------
Renewal (FMV)    High               Low                 -5 to -10 bps
Renewal (fixed   Very High          Moderate-High       +5 to +25 bps
 below market)
Renewal (fixed   Moderate           Moderate            +3 to +10 bps
 at market)
ROFO (space)     Moderate           Low                 +3 to +8 bps
ROFR (space)     High               Moderate            +8 to +18 bps
ROFO (building)  Moderate           Low                 +5 to +10 bps
ROFR (building)  Very High          High                +15 to +30 bps
Expansion ROFO   Moderate           Low                 +3 to +5 bps
Expansion commit Very High          High                +10 to +20 bps
Contraction      High               Moderate            +8 to +15 bps
Termination      Very High          High                +15 to +30 bps
Purchase (FMV)   High               Low-Moderate        +5 to +15 bps
Purchase (fixed) Very High          Very High           +20 to +50 bps
Exclusive use    Moderate-High      Moderate            +5 to +15 bps
Relocation (LL)  None (risk)        Low                 Neutral
```

Note: Cap rate impacts are incremental, per option. Multiple options stack.
A tenant with renewal + termination + contraction + ROFO can add 40+ bps
to effective cap rate, materially reducing property value.
