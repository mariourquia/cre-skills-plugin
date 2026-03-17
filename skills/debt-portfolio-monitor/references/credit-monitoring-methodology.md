# Credit Monitoring Methodology Reference

Systematic framework for monitoring a CRE debt portfolio: trend analysis, watchlist criteria, covenant testing, maturity wall analysis, and traffic-light classification. Designed for portfolio-level oversight of 20-200+ loans.

---

## 1. Core Metric Trend Analysis

### 1A. Debt Service Coverage Ratio (DSCR) Trend

#### Formula

```
DSCR_t = NOI_t / ADS_t

Trailing DSCR:  uses T-12 actual NOI
Forward DSCR:   uses underwritten/projected NOI
Stressed DSCR:  uses stressed NOI (vacancy +5-10%, rent growth 0%) or stressed rate (+200bp)
```

#### Trend Classification

| DSCR Trend (3 consecutive quarters) | Classification | Action |
|---|---|---|
| Rising, above 1.30x | Performing | Standard monitoring |
| Stable, 1.15-1.30x | Performing/Watch | Quarterly review |
| Declining, still above 1.15x | Early Warning | Increased monitoring frequency |
| Declining, 1.00-1.15x | Watchlist | Active asset management, quarterly site visit |
| Below 1.00x | Distressed | Workout initiation, reserve analysis |

#### Worked Example: 8-Quarter DSCR Trend

```
Loan: $15M, 6.25% fixed, 30yr amort. ADS = $1,109,160

Quarter    NOI (annualized)    DSCR    Trend
Q1 2025    $1,442,000          1.30x   --
Q2 2025    $1,410,000          1.27x   Declining
Q3 2025    $1,365,000          1.23x   Declining
Q4 2025    $1,320,000          1.19x   Declining
Q1 2026    $1,298,000          1.17x   Declining
Q2 2026    $1,275,000          1.15x   Watchlist trigger (3 consecutive declines + below 1.20x)
Q3 2026    $1,290,000          1.16x   Stabilizing
Q4 2026    $1,310,000          1.18x   Recovering
```

Migration: Performing -> Watch (Q3 2025) -> Watchlist (Q2 2026) -> Watch (Q4 2026 if recovery continues)

### 1B. Loan-to-Value (LTV) Trend

#### Formula

```
LTV_t = loan_balance_t / property_value_t

Mark-to-market LTV: uses current appraised or broker opinion of value
Underwritten LTV: uses original underwritten value
Stressed LTV: uses stressed cap rate (+50-100bp to current market cap)
```

#### Revaluation Triggers

Property values are not marked quarterly in most debt portfolios. Revaluation triggers:

```
1. DSCR decline below watch threshold (1.20x)
2. Major tenant departure (>20% of NRA or >15% of GPI)
3. Material capital event (fire, flood, environmental)
4. Market dislocation in property's submarket
5. Annual review for all loans >$10M
6. Loan maturity within 18 months
```

#### Stressed LTV Calculation

```
Current NOI: $1,275,000
Current market cap rate: 6.50%
Current value: $1,275,000 / 0.065 = $19,615,385
Current LTV: $15,000,000 / $19,615,385 = 76.5%

Stressed cap rate (+75bp): 7.25%
Stressed value: $1,275,000 / 0.0725 = $17,586,207
Stressed LTV: $15,000,000 / $17,586,207 = 85.3%
```

### 1C. Debt Yield Trend

#### Formula

```
DY_t = NOI_t / loan_balance_t
```

Debt yield is rate-independent and reflects the lender's return if they owned the property at their loan basis.

```
Minimum DY thresholds (2025-2026):
  Multifamily:  7.5%
  Industrial:   8.0%
  Retail:       9.0%
  Office:       10.0%
```

---

## 2. Watchlist Migration Criteria

### Entry Criteria (any one triggers watchlist placement)

| Criterion | Threshold | Source |
|---|---|---|
| DSCR (trailing) | < 1.15x for 2+ consecutive quarters | Operating statements |
| DSCR (forward, stressed) | < 1.00x under +200bp rate stress | Rate sensitivity model |
| LTV (mark-to-market) | > 80% (or > original UW LTV + 10%) | Appraisal / BOV |
| Debt yield | < minimum threshold by property type | Operating statements |
| Occupancy decline | > 10 percentage points from UW | Rent roll |
| Major tenant risk | Tenant >20% of GPI files bankruptcy, gives notice, or goes dark | Lease monitoring |
| Payment delinquency | 30+ days past due | Servicer report |
| Covenant breach | Any financial covenant breach | Compliance certificate |
| Maturity risk | < 18 months to maturity with refi risk (DSCR < 1.20x or LTV > 75%) | Maturity schedule |

### Exit Criteria (all must be met)

```
1. Triggering condition cured for 2 consecutive quarters
2. DSCR > 1.20x (trailing) for 2 consecutive quarters
3. No payment delinquency for 6+ months
4. No outstanding covenant breaches
5. Approved by credit committee or portfolio manager
```

### Watchlist Severity Tiers

| Tier | Name | Criteria | Monitoring Frequency | Escalation |
|---|---|---|---|---|
| 1 | Watch | Single metric breach, mild | Quarterly deep review | Portfolio manager |
| 2 | Concern | Multiple metrics or sustained decline | Monthly review | Credit committee |
| 3 | Workout | Payment default, severe breach, or foreclosure consideration | Weekly | Special servicing / workout team |

---

## 3. Covenant Compliance Testing

### Standard Financial Covenants

```
DSCR Covenant:
  Test: DSCR_trailing >= DSCR_minimum (typically 1.20-1.30x)
  Frequency: Quarterly
  Cure mechanism: Cash sweep, equity infusion, or reserve deposit
  Cure period: 30-60 days from notice

LTV Covenant (less common in fixed-rate loans):
  Test: LTV <= LTV_maximum (typically 75-80%)
  Trigger: Annual revaluation or refi event
  Cure mechanism: Principal curtailment or additional collateral

Debt Yield Covenant:
  Test: DY >= DY_minimum (typically 7.5-10.0%)
  Frequency: Quarterly
  Cure: Same as DSCR

Net Worth / Liquidity Covenant (sponsor-level):
  Test: Guarantor net worth >= $X,XXX,XXX and/or liquidity >= $X,XXX,XXX
  Frequency: Annual (with guarantor financial statement delivery)
```

### Cash Management Triggers

```
Lockbox structure:
  Hard lockbox: All property revenue flows directly to lender-controlled account
  Soft lockbox: Revenue flows to borrower, swept to lender only upon trigger

Trigger events:
  DSCR < cash_sweep_trigger (e.g., 1.15x): excess cash swept after DS and reserves
  DSCR < cash_trap_trigger (e.g., 1.05x): ALL excess cash trapped
  Payment default: immediate hard lockbox activation

Release conditions:
  DSCR > trigger level for 2 consecutive quarters
  No events of default
```

### Worked Example: Covenant Compliance Report

```
Loan: $15,000,000 | Borrower: ABC Property LLC | Property: 123 Main St Office

Covenant                   Required    Actual (Q2 2026)    Status
-----------------------------------------------------------------
Trailing DSCR              >= 1.25x    1.17x               BREACH
Forward DSCR (stressed)    >= 1.00x    0.98x               BREACH
LTV                        <= 75.0%    76.5%               BREACH
Debt Yield                 >= 9.0%     8.5%                BREACH
Sponsor Net Worth          >= $5M      $8.2M               PASS
Sponsor Liquidity          >= $1M      $1.4M               PASS
Occupancy                  >= 80%      82%                 PASS
Cash Sweep Trigger         DSCR<1.20x  ACTIVE              SWEEP ON

Actions Required:
  1. Cash sweep activated (excess CF to reserve)
  2. 30-day cure notice sent for DSCR/LTV/DY breach
  3. Borrower to submit remediation plan within 15 business days
  4. Site visit scheduled for next 30 days
  5. Escalated to Tier 2 (Concern)
```

---

## 4. Maturity Wall Analysis

### Definition

A maturity wall is a concentration of loan maturities within a narrow time window, creating refinancing risk (market capacity, rate environment) and potential forced dispositions.

### Portfolio-Level Maturity Profile

```
For each year t in [current_year, current_year + 10]:
  Maturing_balance_t = sum of outstanding balances for all loans maturing in year t
  Maturing_count_t = count of loans maturing in year t
  At_risk_balance_t = sum of balances where refi is uncertain (DSCR < 1.20x or LTV > 75%)
  Concentration_t = Maturing_balance_t / total_portfolio_balance
```

### Risk Scoring per Maturity Cohort

```
For each loan maturing in period t:
  Refi risk score = f(DSCR, LTV, DY, property_type, market_conditions)

Scoring rubric (1-5 scale):
  DSCR component:
    > 1.40x: 1 (low risk)
    1.25-1.40x: 2
    1.10-1.25x: 3
    1.00-1.10x: 4
    < 1.00x: 5 (high risk)

  LTV component:
    < 60%: 1
    60-70%: 2
    70-75%: 3
    75-80%: 4
    > 80%: 5

  DY component:
    > 12%: 1
    10-12%: 2
    8-10%: 3
    7-8%: 4
    < 7%: 5

  Composite refi risk = (DSCR_score * 0.40) + (LTV_score * 0.35) + (DY_score * 0.25)
  Risk category: Low (1.0-2.0), Moderate (2.1-3.0), Elevated (3.1-4.0), High (4.1-5.0)
```

### Worked Example: 5-Year Maturity Wall

```
Portfolio: $500M total outstanding, 45 loans

Year    Maturing $   Count   At-Risk $   Concentration   Avg Refi Score
------------------------------------------------------------------------
2026    $62M         6       $18M        12.4%           2.3 (Moderate)
2027    $145M        14      $52M        29.0%           3.1 (Elevated)
2028    $88M         9       $22M        17.6%           2.5 (Moderate)
2029    $55M         5       $8M         11.0%           1.8 (Low)
2030    $42M         4       $5M         8.4%            1.6 (Low)
Extended $108M       7       --          21.6%           --

ALERT: 2027 maturity wall -- 29% of portfolio matures in single year.
  Action items:
  1. Begin refi discussions 18 months ahead (Q3 2025)
  2. Identify extension candidates (review loan docs for extension options)
  3. Stress test at-risk $52M cohort under +100bp rate scenario
  4. Prepare disposition strategy for loans with refi risk score > 4.0
```

---

## 5. Traffic-Light Classification System

### Three-Level System

| Color | Label | Criteria | Portfolio Allocation Target |
|---|---|---|---|
| Green | Performing | DSCR > 1.25x, LTV < 70%, DY > threshold, no covenant breach, current on payments | > 80% of portfolio |
| Yellow | Watch | DSCR 1.05-1.25x, LTV 70-80%, single covenant breach (curable), maturity within 18 months with moderate refi risk | < 15% of portfolio |
| Red | Distressed | DSCR < 1.05x, LTV > 80%, payment delinquency > 60 days, multiple covenant breaches, foreclosure or workout initiated | < 5% of portfolio |

### Migration Rules

```
Green -> Yellow: Any watchlist entry criterion triggered
Yellow -> Green: All watchlist exit criteria met (2 consecutive quarters)
Yellow -> Red: Payment default > 60 days, or 3+ covenant breaches, or DSCR < 1.05x for 2 quarters
Red -> Yellow: Loan restructured and performing under modified terms for 2+ quarters
Red -> Green: Not permitted directly; must pass through Yellow for minimum 2 quarters
```

### Dashboard Metrics

```
Portfolio Summary (as of MM/DD/YYYY):
  Total UPB: $XXX,XXX,XXX
  Loan count: XX

  Green:  XX loans, $XXX,XXX,XXX (XX.X%)
  Yellow: XX loans, $XX,XXX,XXX (XX.X%)
  Red:    XX loans, $X,XXX,XXX (X.X%)

  Weighted Average DSCR: X.XXx
  Weighted Average LTV: XX.X%
  Weighted Average DY: X.X%
  WA Remaining Term: X.X years
  Delinquency Rate (60+ days): X.X%
```

---

## 6. Portfolio-Level Aggregation Methodology

### Weighted Average Calculations

```
WA_DSCR = sum(balance_i * DSCR_i) / sum(balance_i)
WA_LTV = sum(balance_i * LTV_i) / sum(balance_i)
WA_DY = sum(balance_i * DY_i) / sum(balance_i)
WA_rate = sum(balance_i * rate_i) / sum(balance_i)
WA_remaining_term = sum(balance_i * remaining_months_i) / sum(balance_i) / 12
```

### Concentration Metrics

```
Geographic HHI = sum(share_i^2)  where share_i = balance in market i / total balance
Property type HHI = sum(share_j^2)  where share_j = balance in type j / total balance
Sponsor HHI = sum(share_k^2)  where share_k = balance to sponsor k / total balance

HHI interpretation:
  < 0.10: Well diversified
  0.10-0.18: Moderate concentration
  0.18-0.25: Concentrated
  > 0.25: Highly concentrated
```

### Worked Example: 6-Loan Portfolio Aggregation

```
Loan   Balance      Rate    DSCR    LTV     DY      Type       Market
A      $25,000,000  6.25%   1.35x   68%     8.8%    MF         NYC
B      $18,000,000  6.75%   1.18x   74%     7.9%    Office     NYC
C      $12,000,000  5.90%   1.42x   62%     9.5%    Industrial NJ
D      $15,000,000  7.00%   1.08x   78%     7.2%    Retail     CT
E      $22,000,000  6.50%   1.28x   71%     8.3%    MF         DC
F      $8,000,000   6.00%   1.55x   55%     11.2%   Industrial PA
Total  $100,000,000

WA DSCR: (25*1.35 + 18*1.18 + 12*1.42 + 15*1.08 + 22*1.28 + 8*1.55) / 100
        = (33.75 + 21.24 + 17.04 + 16.20 + 28.16 + 12.40) / 100
        = 128.79 / 100 = 1.29x

WA LTV: (25*68 + 18*74 + 12*62 + 15*78 + 22*71 + 8*55) / 100
       = (1700 + 1332 + 744 + 1170 + 1562 + 440) / 100 = 69.5%

WA DY: (25*8.8 + 18*7.9 + 12*9.5 + 15*7.2 + 22*8.3 + 8*11.2) / 100
      = (220 + 142.2 + 114 + 108 + 182.6 + 89.6) / 100 = 8.56%

Traffic light:
  Green: A, C, E, F (DSCR > 1.25x, LTV < 75%)  -- $67M (67%)
  Yellow: B (DSCR 1.18x, LTV 74%)                -- $18M (18%)
  Yellow: D (DSCR 1.08x, LTV 78%)                -- $15M (15%)
  Red: none

Geographic HHI: (43/100)^2 + (12/100)^2 + (15/100)^2 + (22/100)^2 + (8/100)^2
  NYC: $43M (43%), NJ: $12M, CT: $15M, DC: $22M, PA: $8M
  = 0.1849 + 0.0144 + 0.0225 + 0.0484 + 0.0064 = 0.2766 (Highly concentrated -- NYC dominates)

Property type HHI: MF=$47M(47%), Office=$18M(18%), Industrial=$20M(20%), Retail=$15M(15%)
  = 0.2209 + 0.0324 + 0.0400 + 0.0225 = 0.3158 (Highly concentrated -- MF dominates)
```

---

## 7. Common Errors

| Error | Consequence |
|---|---|
| Using underwritten NOI instead of trailing actual for DSCR monitoring | Masks deterioration; actual performance may lag projections significantly |
| Weighting DSCR by loan count instead of balance | A $50M loan with 0.95x DSCR is far more impactful than a $2M loan at 0.95x |
| Not stress-testing floating rate loans at maturity | A loan performing at 1.30x today may be at 0.90x if SOFR rises 200bp at refi |
| Ignoring cap rate expansion in LTV updates | Using original cap rates for ongoing LTV monitoring understates actual LTV in rising-rate environments |
| Single-metric watchlist triggers | DSCR alone is insufficient; a loan can have 1.30x DSCR but 85% LTV due to value decline |
| Treating covenant cure as resolution | A cash infusion cures the covenant breach but does not fix the underlying operational issue |
