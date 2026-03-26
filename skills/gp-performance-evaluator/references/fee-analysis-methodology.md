# Fee Analysis Methodology
# Reference for gp-performance-evaluator skill
# Defines the framework for computing and benchmarking GP fee drag

---

## Overview

Fee drag is the total cost to an LP of participating in a GP's fund. It includes management fees, carried interest, and all other costs charged to the fund or LP. The gross-to-net spread (difference between gross and net IRR) is the most intuitive measure, but a complete analysis must disaggregate the components and benchmark each against market norms.

---

## Component 1: Management Fee

### Calculation

Management fee is the GP's base compensation, charged regardless of performance.

```
Investment Period (IP):
  Fee = Fee Rate * Fee Basis * Number of IP Years
  Fee Basis during IP: typically committed capital (sometimes invested capital)

  Example:
    $100M commitment * 1.50% * 4 years IP = $6.0M total

Harvest Period (Post-IP):
  Fee typically steps down to a lower basis:
    - Invested capital (most common)
    - NAV (less common)
    - Cost basis (least favorable to LP -- does not decline as assets are sold)

  Example:
    $80M average invested capital * 1.25% * 6 years = $6.0M total

Total Management Fee = IP fee + Harvest fee = $12.0M over fund life
Annual equivalent = $12.0M / 10 years = $1.2M/year
As bps of commitment = $1.2M / $100M = 120 bps/year
```

### Step-Down Mechanics

Common step-down structures and their LP impact:

| Structure | IP Basis | Post-IP Basis | LP Favorability |
|-----------|----------|---------------|-----------------|
| Committed to Invested | 1.50% on committed | 1.25% on invested | Market standard |
| Committed to NAV | 1.50% on committed | 1.00% on NAV | LP-favorable (NAV declines as exits occur) |
| Committed to Cost | 1.50% on committed | 1.25% on cost | GP-favorable (cost does not decline with appreciation) |
| No step-down | 1.50% on committed throughout | same | Very GP-favorable (LP pays on returned capital) |
| Declining rate on committed | 1.50% IP, 1.00% post-IP on committed | same basis, lower rate | Moderate LP-favorable |

### Fee Holiday Analysis

Some GPs offer a fee holiday during the first 6-12 months (no management fee while deploying initial capital). This is LP-favorable and saves approximately 50-75 bps in Year 1.

---

## Component 2: Carried Interest (Promote)

### Calculation Framework

Carry is the GP's performance-based compensation. The amount depends on the waterfall structure.

```
EUROPEAN WATERFALL (whole-fund):
  Step 1: LP receives return of all contributed capital
  Step 2: LP receives preferred return (typically 8% IRR) on all capital
  Step 3: GP catch-up (varies: 50/50 or 100% GP until 20/80 split is achieved)
  Step 4: Remaining profits split 80/20 (LP/GP)

  LP advantage: LP gets pref across ENTIRE fund before GP earns any carry.
  GP earns carry only if the whole fund exceeds the hurdle.

AMERICAN WATERFALL (deal-by-deal):
  For each deal separately:
  Step 1: LP receives return of contributed capital for that deal
  Step 2: LP receives preferred return on that deal's capital
  Step 3: GP catch-up on that deal
  Step 4: Remaining profits on that deal split 80/20

  GP advantage: GP earns carry on profitable deals even if other deals lose money.
  LP risk: GP may earn carry on early deals, then owe clawback on later losses.

DIFFERENCE IMPACT:
  In a fund with mixed results (some winners, some losers):
  - American waterfall: GP earns carry on winners, clawback on losers (if enforceable)
  - European waterfall: losses offset wins before carry is calculated
  - Typical difference: 50-200 bps of net IRR in a mixed-performance fund
```

### Catch-Up Mechanics

The catch-up provision determines how quickly the GP reaches the target carry split.

```
100% GP Catch-Up:
  After LP receives preferred return, 100% of next profits go to GP until
  the GP has received 20% of all profits (cumulative).
  Effect: GP catches up very quickly. LP receives no distributions during catch-up.
  This is GP-favorable.

50/50 Catch-Up:
  After LP receives preferred return, profits are split 50/50 (LP/GP) until
  the GP has received 20% of all profits (cumulative).
  Effect: GP catches up more slowly. LP still receives distributions during catch-up.
  This is LP-favorable compared to 100%.

No Catch-Up:
  After LP receives preferred return, all remaining profits split 80/20.
  GP never reaches a full 20% of total profits unless returns are very high.
  This is most LP-favorable but very rare.

DOLLAR IMPACT EXAMPLE ($100M fund returning 1.75x):
  Gross profit: $75M
  Preferred return (8% over 5 years): ~$47M cumulative
  Profit above pref: $28M

  100% GP catch-up: GP receives ~$15M carry (20% of $75M total)
  50/50 catch-up: GP receives ~$12.5M carry
  No catch-up: GP receives ~$5.6M carry (20% of $28M above pref)
```

### Carry at Multiple Return Scenarios

Model carry at three scenarios to understand the LP's cost across outcomes:

| Scenario | Fund TVPI | Gross Profit | GP Carry (20%, European) | Carry as % of Profit |
|----------|-----------|--------------|--------------------------|---------------------|
| Downside | 1.2x | $20M | $0 (below pref) | 0% |
| Base | 1.75x | $75M | $12-15M | 16-20% |
| Upside | 2.5x | $150M | $28-30M | 19-20% |

Note: Carry as percentage of profit converges toward 20% at higher returns (the preferred return becomes less meaningful as total returns increase).

---

## Component 3: Other Fees and Expenses

### Transaction Fees

Fees charged to the fund for deal-related activities:

| Fee Type | Typical Range | Fee Offset Standard | Red Flag |
|----------|---------------|---------------------|----------|
| Acquisition fee | 0.50-1.00% of purchase price | 100% offset against mgmt fee | <80% offset |
| Disposition fee | 0.50-1.00% of sale price | 100% offset | <80% offset |
| Construction management fee | 3-5% of hard costs | 80-100% offset | No offset |
| Financing fee | 0.25-0.50% of loan amount | 100% offset | No offset |

### Organizational Expenses

One-time costs at fund formation charged to LPs:

| Expense | Typical Range | Cap Standard | Red Flag |
|---------|---------------|--------------|----------|
| Legal (fund formation) | $500K-$2M | Capped at 0.5-1.5% of committed | No cap |
| Placement agent | 1-2% of capital raised | Paid by GP (market standard) | Paid by fund |
| Regulatory filings | $50-200K | Included in cap | Excluded from cap |
| Travel/marketing | Varies | GP cost (not fund) | Charged to fund |

### Operating Expenses

Ongoing costs charged to the fund:

| Expense | Typical Range | Notes |
|---------|---------------|-------|
| Fund admin | $150-400K/year | Varies by fund size and complexity |
| Audit | $100-300K/year | Increases with number of entities |
| Legal (ongoing) | $200-500K/year | Transactional legal usually separate |
| Tax preparation | $100-300K/year | K-1 preparation for all LPs |
| D&O/E&O insurance | $50-150K/year | Fund-level coverage |
| Broken-deal costs | Varies widely | Some LPAs cap at $X per failed deal |

---

## Gross-to-Net Spread Analysis

### Computation

```
Gross-to-Net Spread = Gross IRR - Net IRR

Components:
  Management Fee Drag:  typically 80-150 bps of the spread
  Carry Drag:           typically 50-200 bps (depends on return level)
  Other Fee Drag:       typically 20-80 bps
  Total:                typically 150-400 bps

Example:
  Gross IRR: 18.0%
  Net IRR:   13.5%
  Spread:    450 bps

  Decomposition:
  Management fee:    140 bps (1.50% fee on $80M avg invested over 10 years)
  Carry:             250 bps (20% carry on $75M profit)
  Other fees/costs:   60 bps (organizational, transaction, operating)
  Total:             450 bps (matches)
```

### Benchmarking the Spread

| Strategy | 25th Pctile | Median | 75th Pctile | 90th Pctile | Red Flag |
|----------|-------------|--------|-------------|-------------|----------|
| Core | 80 bps | 130 bps | 180 bps | 230 bps | > 250 bps |
| Core-Plus | 120 bps | 175 bps | 240 bps | 300 bps | > 320 bps |
| Value-Add | 180 bps | 260 bps | 350 bps | 430 bps | > 450 bps |
| Opportunistic | 250 bps | 370 bps | 470 bps | 580 bps | > 600 bps |

### Interpretation Framework

```
Spread < Median:
  LP-favorable fee economics.
  Either low management fee, low carry (due to modest returns), or strong fee offsets.
  Positive signal for re-up.

Spread at Median:
  Market-standard fee economics. Neutral signal.

Spread > 75th Percentile:
  Elevated fee drag. Acceptable ONLY if gross returns are top-quartile.
  Compute: what is the net return percentile? If net return percentile is lower
  than gross return percentile, the GP is capturing disproportionate value.

Spread > 90th Percentile:
  Excessive fee drag. Red flag regardless of gross returns.
  LP is overpaying for access. Negotiate fee reduction or consider alternatives.
```

---

## Subscription Credit Facility Adjustment

### Detection Indicators

```
1. First capital call occurs months after first investment
2. Large initial capital calls followed by immediate partial return
3. GP-reported IRR significantly higher than IRR implied by TVPI and time
4. Fund documents reference subscription facility or capital call facility
5. Significant "net asset value" reported before meaningful capital calls
```

### Adjustment Methodology

```
STEP 1: Obtain investment-level cash flow data
  For each investment: date of actual deployment, amount deployed

STEP 2: Replace sub-line-enhanced cash flows with investment-date cash flows
  Original: Capital call on Day 180 funds investments made on Days 30, 60, 90, 120
  Adjusted: Four capital calls on Days 30, 60, 90, 120 (matching actual deployment)

STEP 3: Recompute IRR using adjusted cash flows (XIRR)

STEP 4: Report both metrics
  "As-reported IRR (including sub-line benefit): XX.X%"
  "Investment-date IRR (sub-line adjusted): XX.X%"
  "Sub-line IRR inflation: XXX bps"

TYPICAL INFLATION:
  Sub-line used < 6 months:   50-150 bps inflation
  Sub-line used 6-12 months:  150-300 bps inflation
  Sub-line used 12-18 months: 300-500 bps inflation
  Sub-line used > 18 months:  400-800 bps inflation

NOTE: Sub-line facilities serve legitimate operational purposes (bridging capital
calls, smoothing cash management). The issue is not usage but disclosure. GPs
must report sub-line impact on IRR or the metric is misleading.
```
