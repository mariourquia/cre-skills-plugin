# Fee Load Calculator Methodology
# Reference for fund-terms-comparator skill
# Defines the computation framework for total fee load projection

---

## Overview

The fee load calculator projects the total cost to an LP over the full life of a fund at multiple return scenarios. It disaggregates the cost into management fee, carried interest, and other fees/expenses, then expresses each as a percentage of gross profits and as basis points of committed capital per year.

---

## Inputs Required

```
FUND PARAMETERS:
  fund_size:              Total committed capital
  lp_commitment:          LP's specific commitment
  investment_period:      Years (typically 3-5)
  fund_life:              Years (typically 7-10, including extensions)
  fund_strategy:          core / core_plus / value_add / opportunistic
  fund_type:              closed_end / open_end / co_invest / separate_account

FEE TERMS:
  mgmt_fee_ip_rate:       Management fee rate during investment period
  mgmt_fee_ip_basis:      Basis during IP (committed / invested / nav)
  mgmt_fee_post_rate:     Management fee rate post-investment period
  mgmt_fee_post_basis:    Basis post-IP (invested / nav / cost)
  carry_rate:             Carried interest percentage
  hurdle_rate:            Preferred return (IRR)
  catch_up:               Catch-up provision (100_gp / 50_50 / none)
  waterfall_type:         European / American
  gp_commitment_pct:      GP commitment as % of fund size
  gp_commitment_form:     cash / fee_waiver / mixed
  fee_offset_pct:         Percentage of transaction fees that offset mgmt fee
  org_expense_cap:        Organizational expense cap as % of committed

RETURN SCENARIOS:
  scenario_1 (downside):  TVPI = 1.2x (below target)
  scenario_2 (base):      TVPI = strategy-dependent target
  scenario_3 (upside):    TVPI = strategy-dependent upside
```

---

## Computation Steps

### Step 1: Management Fee Calculation

```
INVESTMENT PERIOD FEE:
  IF basis = committed_capital:
    IP_fee = mgmt_fee_ip_rate * lp_commitment * investment_period
  ELIF basis = invested_capital:
    IP_fee = mgmt_fee_ip_rate * average_invested_during_IP * investment_period
    (average_invested_during_IP = ramp from 0 to fully invested over IP)
  ELIF basis = nav:
    IP_fee = mgmt_fee_ip_rate * average_nav_during_IP * investment_period

POST-INVESTMENT PERIOD FEE:
  harvest_years = fund_life - investment_period
  IF basis = invested_capital:
    POST_fee = mgmt_fee_post_rate * average_invested_during_harvest * harvest_years
    (average_invested declines as assets are sold during harvest)
  ELIF basis = nav:
    POST_fee = mgmt_fee_post_rate * average_nav_during_harvest * harvest_years
  ELIF basis = cost:
    POST_fee = mgmt_fee_post_rate * total_cost_basis * harvest_years
    (cost basis does not decline with appreciation -- GP-favorable)

TOTAL MANAGEMENT FEE = IP_fee + POST_fee

DEPLOYMENT RAMP ASSUMPTION:
  Year 1: 25% deployed
  Year 2: 55% deployed
  Year 3: 80% deployed
  Year 4: 95% deployed (typical for 4-year IP)
  Year 5+: 100% deployed (or declining as exits occur)

EXIT RAMP ASSUMPTION (harvest period):
  Year IP+1: 95% invested
  Year IP+2: 80% invested
  Year IP+3: 60% invested
  Year IP+4: 40% invested
  Year IP+5: 20% invested
  Year IP+6: 5% invested (tail)
```

### Step 2: Carried Interest Calculation

```
EUROPEAN WATERFALL:
  Step 1: LP receives return of contributed capital
    LP gets back: lp_commitment (all called capital)
  Step 2: LP receives preferred return (compound IRR)
    Preferred = lp_commitment * ((1 + hurdle_rate) ^ hold_period - 1)
  Step 3: Catch-up
    IF catch_up = 100_gp:
      GP receives 100% of next profits until GP has received carry_rate of total profits
      Catch_up_amount = (Total_profit * carry_rate) / (1 - carry_rate) -- simplified
    ELIF catch_up = 50_50:
      Profits split 50/50 until GP has received carry_rate of total profits
      Catch_up_amount = same target, slower pace
    ELIF catch_up = none:
      Skip directly to residual split
  Step 4: Residual split
    Remaining profits split (1-carry_rate) LP / carry_rate GP

AMERICAN WATERFALL:
  Apply Steps 1-4 PER DEAL, then aggregate
  Note: GP earns carry on each profitable deal individually
  Total carry may be HIGHER than European waterfall in mixed-performance portfolios

CARRY COMPUTATION AT EACH SCENARIO:
  For each scenario_tvpi:
    Gross_profit = lp_commitment * (scenario_tvpi - 1.0)
    Apply waterfall mechanics to compute GP carry
    LP_net_profit = Gross_profit - GP_carry - Management_fee - Other_fees
    Net_TVPI = 1.0 + LP_net_profit / lp_commitment
    Compute: net IRR from cash flow timing model
```

### Step 3: Other Fees and Expenses

```
ORGANIZATIONAL EXPENSES:
  Org_cost = MIN(org_expense_cap * lp_commitment, estimated_actual_org_cost)
  Estimated actual: $1-3M for funds <$1B, $2-5M for funds >$1B
  Amortized over investment period for annual impact

TRANSACTION FEES (NET OF OFFSET):
  Estimated_total_transaction_fees = fund_size * avg_transaction_fee_rate * 2
    (acquisition + disposition on average portfolio)
  LP_share = Estimated_total_transaction_fees * (lp_commitment / fund_size)
  Offset = LP_share * fee_offset_pct
  Net_transaction_cost = LP_share - Offset
  Note: if fee_offset = 100%, net cost to LP from transaction fees is $0
    (they reduce management fee dollar-for-dollar)

OPERATING EXPENSES:
  Annual_operating = estimated per fund size:
    < $500M: $400K-$700K / year
    $500M-$2B: $600K-$1.2M / year
    > $2B: $1M-$2M / year
  LP_share = Annual_operating * (lp_commitment / fund_size)
  Total_operating_over_life = LP_share * fund_life

BROKEN-DEAL COSTS:
  Estimated at 0.5-1.0% of capital deployed on failed transactions
  Typical: 10-20% of deals pursued result in broken-deal costs
  LP_share = broken_deal_estimate * (lp_commitment / fund_size)

TOTAL OTHER FEES = Org + Net_Transaction + Operating + Broken_Deal
```

### Step 4: Total Fee Load Summary

```
TOTAL FEE LOAD = Management Fee + Carry + Other Fees

EXPRESS AS:
  1. Absolute dollars: $X over fund life
  2. Percentage of gross profits: Total / Gross_Profit * 100
  3. Basis points per year: (Total / lp_commitment / fund_life) * 10,000
  4. Gross-to-net spread: Gross IRR - Net IRR (in bps)

COMPARISON TABLE (populate for all 3 scenarios):
| Component | Downside | Base | Upside |
|-----------|----------|------|--------|
| Gross Profit ($) | | | |
| Management Fee ($) | | | |
| Carry ($) | | | |
| Other Fees ($) | | | |
| Total Fees ($) | | | |
| Fees as % of Profit | | | |
| Net Profit ($) | | | |
| Net TVPI | | | |
| Net IRR (est) | | | |
| Gross-Net Spread (bps) | | | |
| Fee Load (bps/yr) | | | |
```

---

## Scenario Calibration by Strategy

Default TVPI scenarios for fee load modeling:

| Strategy | Downside TVPI | Base TVPI | Upside TVPI |
|----------|---------------|-----------|-------------|
| Core | 1.1x | 1.4x | 1.7x |
| Core-Plus | 1.15x | 1.5x | 1.9x |
| Value-Add | 1.2x | 1.75x | 2.3x |
| Opportunistic | 1.0x | 2.0x | 3.0x |

Default hold periods:
| Strategy | Avg Hold | Deployment | Harvest |
|----------|----------|------------|---------|
| Core | 10 years | 3 years | 7 years |
| Core-Plus | 8 years | 3 years | 5 years |
| Value-Add | 8 years | 3 years | 5 years |
| Opportunistic | 8 years | 4 years | 4 years |

---

## Benchmarking Framework

### Fee Load Percentile Assessment

After computing total fee load, compare against market benchmarks:

```
TOTAL FEE LOAD (bps/year of committed capital):

  Core:
    LP-Favorable (<25th): < 75 bps/yr
    Market (25th-75th): 75-150 bps/yr
    GP-Favorable (>75th): > 150 bps/yr
    Red Flag (>90th): > 200 bps/yr

  Value-Add:
    LP-Favorable: < 150 bps/yr
    Market: 150-290 bps/yr
    GP-Favorable: > 290 bps/yr
    Red Flag: > 380 bps/yr

  Opportunistic:
    LP-Favorable: < 200 bps/yr
    Market: 200-400 bps/yr
    GP-Favorable: > 400 bps/yr
    Red Flag: > 500 bps/yr

FEES AS % OF GROSS PROFIT (at base case returns):

  Healthy: < 25%
  Acceptable: 25-35%
  Elevated: 35-45%
  Excessive: > 45%
  Note: In downside scenarios, fees as % of profit will be much higher.
  The downside fee percentage shows how much fee drag hurts in bad outcomes.
```

---

## Negotiation Impact Quantification

For each negotiable term, compute the dollar impact of improvement:

```
MANAGEMENT FEE REDUCTION:
  Each 25 bps reduction in management fee rate:
    Dollar savings = 0.0025 * fee_basis * applicable_years
    For $100M on committed over 4-year IP: $1.0M savings
    Total over fund life (with step-down): typically $1.5-2.5M per 25 bps

CATCH-UP CHANGE (100% GP -> 50/50):
  At base case returns:
    Savings = difference in catch-up allocation
    Typical savings: $0.5-1.5M for $100M commitment

WATERFALL CHANGE (American -> European):
  At base case returns with mixed deal outcomes:
    Savings = carry avoided on early profitable deals that offset later losses
    Typical savings: $0.5-2.0M for $100M commitment
    More significant in higher-volatility strategies (opportunistic)

FEE OFFSET IMPROVEMENT (50% -> 100%):
  Savings = additional offset amount
  Typical savings: $0.3-0.8M for $100M commitment

GP COMMITMENT INCREASE:
  No direct dollar savings, but improves alignment.
  Qualitative value: GP with 5% cash commitment manages differently than 1% fee waiver.

SIDE LETTER MFN PROVISION:
  Value: ensures LP receives best terms offered to any LP of similar or smaller size.
  Typical impact: may capture additional 25-50 bps fee reduction or improved co-invest rights.
```

---

## Output Template

The fee load calculator produces the following output structure:

```
FEE LOAD ANALYSIS: [Fund Name] - [LP Commitment]

1. TERM SUMMARY
   [Table of all material terms with market percentile]

2. FEE LOAD PROJECTION
   [Three-scenario table as specified in Step 4]

3. COMPONENT BREAKDOWN
   [Pie chart data: management fee % of total, carry % of total, other % of total]

4. TERM EVOLUTION (if prior fund data available)
   [Table comparing current vs prior fund terms]

5. MARKET POSITIONING
   [How this fund's total fee load compares to strategy/size benchmarks]

6. NEGOTIATION RECOMMENDATIONS
   [Prioritized list with dollar impact per recommendation]

7. BREAK-EVEN ANALYSIS
   [What gross return is needed to deliver target net return after all fees]
   Break_even_gross = target_net + fee_drag (solved iteratively)
```
