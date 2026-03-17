# Performance Attribution Methodology Reference

Return decomposition, gross-to-net fee bridge, alpha attribution, and NCREIF/ODCE benchmarking. Full worked example with a 5-year value-add fund.

---

## 1. Return Decomposition Framework

### Total Return Components

CRE total return decomposes into income return and appreciation return:

```
Total return = Income return + Appreciation return

Income return = NOI / Beginning market value
Appreciation return = (Ending value - Beginning value - Capex) / Beginning value
```

### Finer Decomposition (5 Components)

```
Total return = Income + NOI growth + Cap rate change + Leverage effect + Amortization

Where:
  Income:        Cash-on-cash yield (levered)
  NOI growth:    Contribution from operating improvement
  Cap rate:      Contribution from market pricing change
  Leverage:      Amplification (positive or negative) from debt
  Amortization:  Principal paydown benefit to equity
```

### Formula for Each Component

```
1. Income contribution:
   Inc = (NOI - Debt_service) / Equity_invested
   This is the cash-on-cash return, the yield earned annually.

2. NOI growth contribution:
   NOI_growth = (NOI_exit - NOI_entry) / Cap_rate_exit / Equity_invested / Hold_years
   This captures the value created by increasing NOI through rent growth,
   expense reduction, or occupancy improvement.

3. Cap rate contribution:
   Cap_effect = NOI_exit * (1/Cap_exit - 1/Cap_entry) / Equity_invested / Hold_years
   Positive when cap rates compress (value increases). Negative when they expand.

4. Leverage contribution:
   Lev_effect = (Unlev_return - Cost_of_debt) * (Debt / Equity)
   Positive when unlevered return exceeds debt cost.

5. Amortization contribution:
   Amort = Principal_paydown / Equity_invested / Hold_years
   The forced savings from amortizing debt service.
```

---

## 2. Worked Example: 5-Year Value-Add Fund

### Fund Overview

```
Fund: Valor CRE Value-Add Fund II
Vintage: 2021
Strategy: Acquire underperforming multifamily, renovate, stabilize, sell
Investment period: 2021-2023 (3 years)
Harvest period: 2024-2026 (2 years, all dispositions by 2026)
Total committed capital: $150,000,000
Total called capital: $142,500,000
Management fee: 1.5% on committed (investment period), 1.5% on invested (harvest)
Promote: 8% pref, 80/20 above pref
```

### Portfolio Summary (5 Assets)

```
Asset          | Acq Price | Equity   | Capex   | Exit Price | Hold
---------------|-----------|----------|---------|------------|------
Denver 250u    | $42.0M    | $16.8M   | $3.5M   | $58.0M     | 4.5yr
Austin 180u    | $35.0M    | $14.0M   | $2.8M   | $44.5M     | 4.0yr
Phoenix Ind.   | $28.0M    | $11.2M   | $1.2M   | $35.0M     | 3.5yr
Nashville 120u | $22.0M    | $8.8M    | $2.0M   | $28.5M     | 5.0yr
Tampa Retail   | $16.0M    | $6.4M    | $0.8M   | $19.0M     | 3.0yr
---------------|-----------|----------|---------|------------|------
Total          | $143.0M   | $57.2M   | $10.3M  | $185.0M    | avg 4.0yr
```

### Asset-Level Return Decomposition: Denver 250u

```
Acquisition (Q2 2021):
  Purchase price:    $42,000,000
  Senior debt:       $25,200,000 (60% LTV) at 4.50%, 30yr amort, 3yr IO
  Equity:            $16,800,000
  Entry NOI:         $2,100,000 (5.0% cap)
  Entry NCF:         $2,025,000

Renovation (2021-2022):
  Capex: $3,500,000 ($14,000/unit interior, common area upgrades)
  Funded: 50% from operating reserves, 50% from capital call

Stabilization (2023):
  Stabilized NOI:    $3,200,000 (rent growth from $1,400 to $1,850 avg)
  Stabilized cap:    5.50% (as-stabilized appraised)
  Appraised value:   $58,182,000

Disposition (Q4 2025):
  Exit price:        $58,000,000
  Exit NOI:          $3,350,000 (continued 3% growth post-stabilization)
  Exit cap:          5.78% (3,350,000 / 58,000,000)
  Going-in cap:      5.00%
  Selling costs:     $1,160,000 (2%)
  Net reversion:     $56,840,000
  Loan payoff:       $24,100,000 (after 1.5yr amortization post-IO)
  Equity reversion:  $32,740,000

Cash flows to equity:
  Year 0 (Q2 2021):   -$16,800,000 (equity)
  Year 0.5-1.5:       -$1,750,000 (capex calls, net of operating CF)
  Year 2:             +$450,000 (NOI - IO DS, partial stabilization)
  Year 3:             +$820,000 (stabilized NOI - amortizing DS)
  Year 4:             +$870,000
  Year 4.5 (Q4 2025): +$870,000 * 0.5 + $32,740,000 = $33,175,000

Gross asset IRR: 17.2%
Equity multiple: ($33,175,000 + $2,140,000 CF) / $18,550,000 = 1.90x
```

### Decomposition of Denver Returns

```
Component          | Calculation                                    | Contribution
-------------------|------------------------------------------------|------------
Income (cash flow) | Cumulative CF / equity / 4.5yr                 | 2.6%
                   | ($2,140,000 / $18,550,000 / 4.5)              |
                   |                                                |
NOI growth         | (NOI_exit - NOI_entry) / cap_exit / equity / n | 6.3%
                   | ($3,350,000 - $2,100,000) / 0.0578 /          |
                   | $18,550,000 / 4.5                              |
                   | = $21,626,000 / $18,550,000 / 4.5             |
                   |                                                |
Cap rate effect    | NOI_exit * (1/cap_exit - 1/cap_entry) / eq / n | -3.2%
                   | $3,350,000 * (1/0.0578 - 1/0.05) /            |
                   | $18,550,000 / 4.5                              |
                   | = $3,350,000 * (17.30 - 20.00) / 83,475,000   |
                   | = $3,350,000 * (-2.70) / 83,475,000           |
                   | = -$9,045,000 / 83,475,000                    |
                   |                                                |
Leverage effect    | (Unlev_IRR - cost_debt) * D/E                  | 8.5%
                   | Unlevered IRR ≈ 10.8%                          |
                   | (10.8% - 4.50%) * (25,200/18,550) * adj       |
                   |                                                |
Amortization       | Principal_paydown / equity / n                 | 3.0%
                   | $1,100,000 / $18,550,000 / 4.5                |
                   | (1.5 years of amortization after 3yr IO)       |
                   |                                                |
TOTAL              |                                                | 17.2%

Key insight: NOI growth contributed +6.3% (the value-add thesis worked).
Cap rate expansion detracted -3.2% (2021 entry at 5.0% vs 5.78% exit).
Leverage contributed +8.5% (positive leverage at 4.50% debt cost).
Without leverage, the deal returns ~10.8%. Leverage nearly doubled the return.
```

---

## 3. Fund-Level Gross-to-Net Fee Bridge

### Fee Waterfall

```
Gross fund return (portfolio-level):
  Gross IRR: 15.8%
  Gross equity multiple: 1.72x

DEDUCTIONS:

1. Management fee:
   Investment period (2021-2023): $150M * 1.5% * 3 = $6,750,000
   Harvest period (2024-2026):
     2024: $142.5M * 1.5% = $2,137,500
     2025: $85.0M * 1.5% = $1,275,000 (capital returned from exits)
     2026: $20.0M * 1.5% = $300,000
   Total mgmt fee: $10,462,500
   Fee drag on IRR: approximately -1.8%

2. Fund expenses (legal, audit, admin):
   $500,000/year * 5 = $2,500,000
   Fee drag: approximately -0.3%

3. GP promote:
   LP return before promote: 13.7% IRR
   8% pref on $142.5M LP equity: $11,400,000/year * 5 = $57,000,000 (cumulative)
   Above-pref distributions: fund total - ROC - pref
   Total distributions: $142.5M * 1.72 = $245.1M
   Above pref: $245.1M - $142.5M - $57.0M = $45.6M
   Catch-up: $57.0M * 0.20/0.80 = $14.25M (to GP)
   Remaining: $45.6M - $14.25M = $31.35M
   GP promote share: $14.25M + $31.35M * 0.20 = $20.52M
   Promote drag on LP IRR: approximately -2.4%

FEE BRIDGE:
  Gross IRR:              15.8%
  Less management fee:    -1.8%
  Less fund expenses:     -0.3%
  Less GP promote:        -2.4%
  -------------------------
  Net LP IRR:             11.3%

  Gross multiple:         1.72x
  Net LP multiple:        1.49x

Fee impact: 4.5% IRR drag (28.5% of gross return consumed by fees)
```

### Fee Analysis Benchmarks

```
Fee drag as % of gross return:
  <20%:  Efficient fee structure (institutional, large fund)
  20-30%: Standard (mid-market value-add)
  30-40%: Expensive (small fund, high promote, high expenses)
  >40%:  Excessive (red flag for LP due diligence)

Our fund: 28.5% -- within standard range but on the higher end.
The 1.5% management fee on committed (not invested) capital during the
investment period is the main driver. Negotiating to 1.25% would save
$1.125M over the investment period.
```

---

## 4. Alpha Attribution

### Alpha Definition

```
Alpha = Net fund return - Benchmark return

For CRE, common benchmarks:
  NCREIF Property Index (NPI): Unlevered, core, all property types
  NCREIF ODCE Index: Open-end diversified core equity (levered, net of fees)
  Custom benchmark: Blend of NPI by property type weighted to fund allocation
```

### Alpha Decomposition

```
Total alpha = Selection alpha + Timing alpha + Leverage alpha + Sector alpha

Selection alpha:  Returns from asset-specific outperformance (better operations,
                  renovation execution, tenant quality) vs. same-type benchmark.

Timing alpha:     Returns from market timing (buying at cycle trough, selling at
                  peak). Measured by comparing entry/exit cap rates to market averages.

Leverage alpha:   Returns attributable to leverage strategy vs. benchmark leverage.
                  ODCE leverage is ~25%. If fund uses 60%, excess leverage contributes
                  (or detracts) from returns.

Sector alpha:     Returns from sector allocation different from benchmark.
                  Overweight MF vs. office in 2021-2025 generated positive sector alpha.
```

### Worked Example: Alpha Attribution

```
Fund net IRR: 11.3%
NCREIF NPI (unlevered, same period): 6.2%
NCREIF ODCE (levered, net, same period): 7.8%

Gross alpha vs NPI: 11.3% - 6.2% = 5.1%
Net alpha vs ODCE: 11.3% - 7.8% = 3.5%

Decomposition (vs ODCE):

1. Leverage alpha:
   Fund leverage: 60% LTV. ODCE leverage: 25%.
   Excess leverage = 35%.
   ODCE unlevered return ≈ 6.2% (NPI). Cost of ODCE debt ≈ 4.5%.
   Leverage alpha = (6.2% - 4.5%) * (0.35 / 0.75) = 0.79%

   Our fund's leverage alpha:
   (Unlev_return - our_debt_cost) * (our_D/E) - (ODCE_unlev - ODCE_debt) * (ODCE_D/E)
   = (10.8% - 4.5%) * 1.50 - (6.2% - 4.5%) * 0.33
   = 9.45% - 0.56% = 8.89% (gross)
   vs ODCE leverage contribution: 7.8% - 6.2% = 1.6%
   Fund excess leverage alpha: 8.89% - 1.6% ≈ 1.5% (net of fees, approximate)

2. Selection alpha (asset-level outperformance):
   Fund unlevered return: 10.8%
   NPI (same period, same property types): 6.2%
   Sector-adjusted NPI: 6.8% (MF outperformed the index)
   Selection alpha = 10.8% - 6.8% = 4.0%

   This is the value-add premium: renovation, operational improvement, and
   active management generated 4.0% above the passive index.

3. Sector alpha:
   Fund allocation: 72% MF, 18% Industrial, 10% Retail
   NPI returns by type (period):
     MF: 7.5%, Industrial: 8.2%, Retail: 3.8%, Office: 1.5%
   NPI overall: 6.2%
   Fund sector-weighted NPI: 0.72*7.5% + 0.18*8.2% + 0.10*3.8% = 7.25%
   Sector alpha = 7.25% - 6.2% = 1.05%

   Overweighting MF and Industrial (and avoiding office) added 1.05%.

4. Timing alpha (residual):
   Total alpha (3.5%) - Leverage (1.5%) - Selection (4.0% * fee adj ~2.8%) - Sector (1.05%)
   Timing ≈ -1.85% (negative)

   The fund entered in 2021 (peak pricing) and exited in 2025-2026
   (post-rate-hike, cap expansion). Timing detracted from returns.
   Despite poor timing, selection and leverage alpha more than compensated.

ALPHA SUMMARY vs ODCE:
  Selection:  +2.8% (net of fees)
  Sector:     +1.05%
  Leverage:   +1.50%
  Timing:     -1.85%
  -------------------
  Total net alpha: +3.5%
```

---

## 5. NCREIF / ODCE Benchmarking

### NCREIF Property Index (NPI)

```
Definition: Quarterly total return index measuring unlevered, institutional-grade
CRE held by tax-exempt entities (pension funds, endowments).

Characteristics:
  - Unlevered (no debt effects)
  - Appraisal-based (smoothed, lagging)
  - Core properties only (stabilized, institutional quality)
  - No fees deducted
  - Quarterly rebalancing

Usage: Benchmark for unlevered property-level returns.
       Compare gross unlevered deal returns to NPI by property type.

Typical annualized returns (20-year average):
  All property: 7.5-9.0%
  Apartment: 8.0-10.0%
  Industrial: 9.0-12.0%
  Office: 6.0-8.0%
  Retail: 7.0-9.0%
```

### NCREIF ODCE Index

```
Definition: Open-end diversified core equity. Measures returns of open-end
commingled funds investing in core CRE.

Characteristics:
  - Levered (typically 20-30% LTV)
  - Net of fees (management fee deducted, but not promote)
  - Diversified (minimum allocation requirements across types/geographies)
  - Quarterly NAV reporting
  - Appraisal-based (same smoothing as NPI)

Usage: Benchmark for levered, net-of-fee core fund returns.
       The standard institutional CRE benchmark.

Typical annualized returns (20-year average):
  Gross: 8.0-10.0%
  Net: 7.0-9.0%
```

### Benchmark Construction for Non-Core Strategies

```
ODCE is inappropriate as a direct benchmark for value-add or opportunistic funds.
Build a custom benchmark:

Custom benchmark = NPI by type * Fund allocation weights + Leverage adjustment

Example for our value-add fund:
  MF NPI return: 7.5%
  Industrial NPI return: 8.2%
  Retail NPI return: 3.8%

  Sector-weighted NPI: 0.72*7.5 + 0.18*8.2 + 0.10*3.8 = 7.25%

  Add target leverage effect: (7.25% - 4.5%) * 1.50 = 4.13%
  Add value-add premium (market consensus): 2.0-3.0%

  Custom benchmark: 7.25% + 4.13% + 2.5% = 13.88% (gross)
  Net of fees (3.0%): 10.88%

  Fund net IRR: 11.3% vs custom benchmark 10.9%
  Alpha: +0.4% (modest outperformance after adjusting for leverage and strategy)
```

### Appraisal Lag Adjustment

```
NPI and ODCE returns are appraisal-based and lag transaction-based returns by
1-3 quarters. During periods of rapid value change (2022-2023 rate hikes),
appraisal-based indices understated losses by 5-15%.

To adjust for smoothing:
  Unsmoothed_return_t = (Reported_return_t - (1-alpha)*Unsmoothed_return_{t-1}) / alpha

  Where alpha = smoothing parameter, typically 0.3-0.5 for quarterly data.

This unsmoothing reveals true volatility: NPI reported vol is ~4% annually,
but unsmoothed vol is ~8-12%. Transaction-based indices (Real Capital Analytics)
show similar higher volatility.

Implication: Alpha measured against NPI/ODCE may be overstated because the
benchmark understates its own volatility. Risk-adjusted alpha (Sharpe ratio
comparison) provides a more honest assessment.
```

---

## 6. Reporting Framework

### Quarterly Attribution Report Structure

```
Section 1: Fund Performance Summary
  - Net IRR (since inception, trailing 1yr, trailing 3yr)
  - Net equity multiple (DPI, TVPI, RVPI)
  - Net alpha vs ODCE

Section 2: Return Decomposition
  - Income, NOI growth, cap rate, leverage, amortization
  - By asset and aggregate

Section 3: Alpha Attribution
  - Selection, timing, leverage, sector
  - Vs NPI and ODCE

Section 4: Portfolio Metrics
  - Concentration (HHI by value, geography, type)
  - Leverage (portfolio LTV, DSCR)
  - Vintage distribution

Section 5: Benchmark Comparison
  - Gross and net returns vs NPI, ODCE, custom benchmark
  - Risk metrics (vol, Sharpe, max drawdown)
```

### DPI / TVPI / RVPI Definitions

```
DPI (Distributions to Paid-In): Realized return
  DPI = Cumulative distributions / Cumulative contributions
  DPI > 1.0 means LP has received back more than invested (in cash)

TVPI (Total Value to Paid-In): Realized + unrealized return
  TVPI = (Cumulative distributions + Remaining NAV) / Cumulative contributions
  TVPI is the equity multiple

RVPI (Residual Value to Paid-In): Unrealized return remaining
  RVPI = Remaining NAV / Cumulative contributions
  RVPI > 0 means there is still value in the fund to be harvested

TVPI = DPI + RVPI

For our fund at Year 4:
  Contributions: $142,500,000
  Distributions to date: $105,000,000 (from 3 asset sales)
  Remaining NAV: $63,000,000 (2 assets unsold)

  DPI = $105,000,000 / $142,500,000 = 0.74x (not yet returned all capital)
  RVPI = $63,000,000 / $142,500,000 = 0.44x
  TVPI = 0.74 + 0.44 = 1.18x (on track for 1.49x at fund termination)
```
