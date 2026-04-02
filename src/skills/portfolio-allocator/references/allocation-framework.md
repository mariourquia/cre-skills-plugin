# Portfolio Allocation Framework Reference

HHI concentration metrics, correlation assessment, optimal allocation, rebalancing triggers, and vintage diversification. Full worked example with an 8-asset CRE portfolio.

---

## 1. Herfindahl-Hirschman Index (HHI) for Concentration

### Definition

HHI measures portfolio concentration. It is the sum of squared allocation weights.

```
HHI = sum(w_i^2)  for i = 1..n

Where w_i = asset i's weight (as decimal, not percent)

HHI ranges:
  1/n (perfectly equal) to 1.0 (100% in one asset)

For n=8 equally weighted assets: HHI = 8 * (0.125)^2 = 0.125
```

### Interpretation

```
HHI < 0.10:  Highly diversified
0.10 - 0.18: Moderately concentrated
0.18 - 0.25: Concentrated
HHI > 0.25:  Highly concentrated
```

### Effective Number of Positions

```
ENP = 1 / HHI

A portfolio with HHI = 0.20 has an effective number of positions = 5.
This means the portfolio is as concentrated as if it held 5 equal positions.
Even if it nominally holds 8 assets, concentration in a few dominates.
```

### Worked Example: 8-Asset Portfolio

```
Asset                 | Value ($M) | Weight  | w_i^2
----------------------|------------|---------|--------
Denver MF (250 units) |   $42.0    | 0.2333  | 0.05444
Austin MF (180 units) |   $32.5    | 0.1806  | 0.03261
Phoenix Industrial    |   $28.0    | 0.1556  | 0.02420
Nashville MF (120 u)  |   $22.0    | 0.1222  | 0.01494
Raleigh BTR (80 homes)|   $21.5    | 0.1194  | 0.01426
Tampa Retail          |   $16.0    | 0.0889  | 0.00790
Charlotte Office      |   $10.5    | 0.0583  | 0.00340
Salt Lake Flex Ind.   |    $7.5    | 0.0417  | 0.00174
----------------------|------------|---------|--------
Total                 |  $180.0    | 1.0000  | 0.15349

HHI = 0.1535
ENP = 1 / 0.1535 = 6.51

Interpretation: Moderately concentrated. The Denver asset alone holds 23.3%
of the portfolio. ENP of 6.5 means the portfolio acts as if it has ~6.5
equal positions despite nominally holding 8 assets.
```

---

## 2. Concentration Dimensions

### Multi-Dimensional HHI

CRE portfolios should assess concentration across multiple dimensions, not just asset value.

```
Dimension           | HHI Calculation                          | Threshold
--------------------|------------------------------------------|----------
Asset value         | sum(value_weight_i^2)                    | < 0.15
Geographic (MSA)    | sum(msa_weight_i^2)                      | < 0.20
Property type       | sum(type_weight_i^2)                     | < 0.30
Tenant (commercial) | sum(tenant_revenue_weight_i^2)           | < 0.10
Vintage year        | sum(vintage_weight_i^2)                  | < 0.25
Lender              | sum(lender_exposure_weight_i^2)          | < 0.25
```

### Worked Example: Geographic HHI

```
MSA           | Portfolio Value ($M) | Weight  | w_i^2
--------------|----------------------|---------|--------
Denver        |   $42.0              | 0.2333  | 0.05444
Austin        |   $32.5              | 0.1806  | 0.03261
Phoenix       |   $28.0              | 0.1556  | 0.02420
Nashville     |   $22.0              | 0.1222  | 0.01494
Raleigh       |   $21.5              | 0.1194  | 0.01426
Tampa         |   $16.0              | 0.0889  | 0.00790
Charlotte     |   $10.5              | 0.0583  | 0.00340
Salt Lake City|    $7.5              | 0.0417  | 0.00174
              |                      |         |--------
Geographic HHI = 0.1535

All assets are in different MSAs, so geographic HHI equals value HHI.
If Denver and Austin were the same MSA, geographic weight would be 41.4%
and HHI would spike to 0.232 (concentrated).
```

### Property Type HHI

```
Property Type | Portfolio Value ($M) | Weight  | w_i^2
--------------|----------------------|---------|--------
Multifamily   |   $96.5              | 0.5361  | 0.28740
Industrial    |   $35.5              | 0.1972  | 0.03889
BTR           |   $21.5              | 0.1194  | 0.01426
Retail        |   $16.0              | 0.0889  | 0.00790
Office        |   $10.5              | 0.0583  | 0.00340
              |                      |         |--------
Property Type HHI = 0.3519

HHI = 0.35 exceeds the 0.30 threshold. The portfolio is over-concentrated
in multifamily (53.6%). Next acquisition should be non-MF to diversify.
```

---

## 3. Correlation Assessment

### CRE Return Correlations (NCREIF NPI, 2000-2024)

```
               | MF    | Office | Retail | Industrial | Hotel
---------------|-------|--------|--------|------------|------
Multifamily    | 1.00  | 0.65   | 0.58   | 0.72       | 0.45
Office         | 0.65  | 1.00   | 0.75   | 0.60       | 0.55
Retail         | 0.58  | 0.75   | 1.00   | 0.52       | 0.50
Industrial     | 0.72  | 0.60   | 0.52   | 1.00       | 0.40
Hotel          | 0.45  | 0.55   | 0.50   | 0.40       | 1.00

Key observations:
  - Office-Retail correlation is highest (0.75): both tied to employment/consumer cycle
  - Hotel has lowest correlations: different demand drivers (travel, conventions)
  - MF-Industrial correlation is high (0.72): both benefit from population growth
  - For diversification, add hotel or niche sectors (self-storage, data centers)
```

### Geographic Correlation Factors

```
Correlation between MSAs depends on:
  1. Economic base similarity (tech hubs correlate with each other)
  2. Distance (nearby MSAs share labor markets)
  3. Industry concentration (energy MSAs correlate with oil price)

Low correlation pairs (good for diversification):
  Austin (tech) <-> Nashville (healthcare/music) ≈ 0.45
  Phoenix (retirement/logistics) <-> Raleigh (education/pharma) ≈ 0.40
  Denver (energy/tech) <-> Tampa (tourism/medical) ≈ 0.50

High correlation pairs (less diversification benefit):
  Austin <-> Denver (both tech-heavy) ≈ 0.75
  Phoenix <-> Tampa (both Sunbelt retirement) ≈ 0.70
```

### Portfolio Variance

```
Portfolio variance = sum_i sum_j (w_i * w_j * sigma_i * sigma_j * rho_ij)

For two assets:
  sigma_p^2 = w_1^2*sigma_1^2 + w_2^2*sigma_2^2 + 2*w_1*w_2*sigma_1*sigma_2*rho_12

Lower correlation -> lower portfolio variance -> better risk-adjusted returns.
```

### Worked Example: 2-Asset Diversification Benefit

```
Asset A (MF): weight 60%, annual return vol = 8%
Asset B (Industrial): weight 40%, annual return vol = 10%
Correlation = 0.72

Portfolio vol = sqrt(0.60^2 * 0.08^2 + 0.40^2 * 0.10^2 + 2*0.60*0.40*0.08*0.10*0.72)
             = sqrt(0.002304 + 0.001600 + 0.002765)
             = sqrt(0.006669)
             = 8.17%

Weighted average vol (no diversification): 0.60*8% + 0.40*10% = 8.80%
Diversification benefit: 8.80% - 8.17% = 0.63% (63bps of risk reduction)

If correlation were 0.40:
  Portfolio vol = sqrt(0.002304 + 0.001600 + 0.001536) = sqrt(0.005440) = 7.38%
  Diversification benefit: 8.80% - 7.38% = 1.42%

Lower correlation doubles the diversification benefit.
```

---

## 4. Optimal Allocation (Mean-Variance Framework)

### Efficient Frontier for CRE

```
Inputs:
  Expected returns (by property type)
  Return volatility (by property type)
  Correlation matrix

The efficient frontier maximizes return for a given level of risk (or minimizes
risk for a given return). In CRE, this is adapted from Markowitz because:
  - Returns are smoothed (appraisal-based, not mark-to-market)
  - True volatility is understated by ~50%
  - Liquidity constraints prevent rapid rebalancing
  - Transaction costs (2-5% of value) make frequent trading uneconomic
```

### Practical Allocation Targets

```
Strategy   | MF    | Industrial | Retail | Office | Other | Expected Return | Vol
-----------|-------|------------|--------|--------|-------|-----------------|-----
Core       | 35-45%| 20-30%     | 10-15% | 10-20% | 5-10% | 6-8%           | 5-7%
Core-plus  | 30-40%| 20-30%     | 10-15% | 5-15%  | 10-20%| 8-10%          | 7-10%
Value-add  | 25-40%| 15-25%     | 5-15%  | 0-10%  | 15-25%| 10-14%         | 10-14%
Opportunist| 20-30%| 10-20%     | 0-10%  | 0-10%  | 30-50%| 14-20%         | 14-20%

"Other" includes: BTR, student housing, self-storage, data centers, life sciences,
seniors housing, manufactured housing
```

### Our 8-Asset Portfolio Assessment

```
Current allocation:
  MF: 53.6%  (target core-plus: 30-40%) -- OVERWEIGHT
  Industrial: 19.7%  (target: 20-30%) -- AT TARGET
  BTR: 11.9%  (within "Other" bucket)
  Retail: 8.9%  (target: 10-15%) -- SLIGHTLY BELOW
  Office: 5.8%  (target: 5-15%) -- AT TARGET

Recommendation: Next $20-30M of deployment should be non-MF.
  Option A: $20M industrial in a non-Sunbelt market (Midwest, Mid-Atlantic)
  Option B: $15M self-storage + $10M grocery-anchored retail
  Option C: $25M data center or life science (emerging sector diversification)
```

---

## 5. Rebalancing Triggers

### Trigger Framework

```
Trigger Type     | Threshold              | Action
-----------------|------------------------|-------
Single asset     | > 25% of portfolio     | Flag for disposition or no further investment
Property type    | HHI > 0.30             | Redirect deployment to underweight sectors
Geographic       | HHI > 0.20             | Redirect deployment to underweight MSAs
Vintage year     | > 40% in single vintage| Stagger acquisitions over time
Leverage         | Portfolio LTV > 65%    | Deleverage or equity injection
Correlation      | Incremental rho > 0.80 | Do not add asset (insufficient diversification)
Return drift     | Asset IRR < portfolio target - 300bps | Disposition candidate
```

### Implementation Rules

```
1. Review allocation quarterly against targets
2. Any acquisition must reduce (or not increase) portfolio HHI on at least
   one dimension (value, geography, or property type)
3. If portfolio HHI exceeds threshold, next deployment must reduce it
4. Dispositions should prioritize the highest-weight asset in the most
   concentrated dimension
5. Do not rebalance purely for allocation -- transaction costs must be
   justified by risk reduction benefit
```

### Rebalancing Cost-Benefit Analysis

```
Selling the Denver MF ($42M, 23.3% weight) would:
  Reduce value HHI from 0.1535 to approximately 0.1200
  Reduce property type HHI from 0.3519 to approximately 0.2800

Transaction costs:
  Selling costs (2%): $840,000
  Transfer taxes (varies): $200,000-$500,000
  Tax liability (if no 1031): $1,500,000-$3,000,000
  Lost future cash flow: $2,500,000 PV (if 5-year hold planned)
  Total cost: $5,000,000-$6,800,000

Risk reduction benefit (estimated):
  Portfolio vol reduction: approximately 50-80bps
  Over 5 years, VaR improvement: $1,800,000-$2,900,000

In this case, the transaction costs likely exceed the diversification benefit.
Better to (a) redeploy new capital into non-MF, or (b) 1031 exchange the Denver
asset into a non-MF, non-Sunbelt asset to achieve diversification without tax drag.
```

---

## 6. Vintage Diversification

### Definition

Vintage risk is the risk that all assets were acquired at the same point in the cycle. A portfolio acquired entirely in 2021-2022 (peak pricing, low rates) faces uniform cap rate expansion risk.

### Vintage HHI

```
Vintage Year | Acquisition ($M) | Weight  | w_i^2
-------------|------------------|---------|--------
2020         |   $22.0          | 0.1222  | 0.01494
2021         |   $42.0          | 0.2333  | 0.05444
2022         |   $32.5          | 0.1806  | 0.03261
2023         |   $28.0          | 0.1556  | 0.02420
2024         |   $34.0          | 0.1889  | 0.03568
2025         |   $21.5          | 0.1194  | 0.01426
             |                  |         |--------
Vintage HHI = 0.1761

ENP = 5.68 vintages

This is within the 0.25 threshold. The portfolio is reasonably vintage-diversified,
though 2021-2022 represents 41.4% combined (peak cycle exposure).
```

### Stress Test: Cap Rate Expansion on Peak Vintages

```
2021-2022 vintage assets ($74.5M combined):
  Average entry cap: 4.8%
  If cap rates expand to 5.8% (100bps):
    Value decline: approximately 17.2% = $12.8M loss
  If cap rates expand to 6.3% (150bps):
    Value decline: approximately 23.8% = $17.7M loss

2024-2025 vintage assets ($55.5M combined):
  Average entry cap: 6.0%
  If cap rates expand 100bps to 7.0%:
    Value decline: approximately 14.3% = $7.9M loss

Total portfolio loss at +100bps: $20.7M (11.5% of $180M portfolio)
Peak vintage contributes 62% of the loss despite being 41% of value.
```

---

## 7. Worked 8-Asset Portfolio Optimization

### Current State and Target

```
Metric               | Current | Target (Core-Plus) | Gap
---------------------|---------|--------------------|---------
Portfolio value      | $180M   | --                 | --
Number of assets     | 8       | 10-15              | Need 2-7 more
Value HHI            | 0.1535  | < 0.15             | Slightly over
Geographic HHI       | 0.1535  | < 0.20             | Passes
Property type HHI    | 0.3519  | < 0.30             | Over (MF heavy)
Vintage HHI          | 0.1761  | < 0.25             | Passes
Portfolio LTV        | 62%     | < 65%              | Passes
Weighted avg cap rate| 5.6%    | --                 | --
Target net IRR       | 12%     | 10-14%             | On target
```

### Recommended Next 3 Acquisitions

```
Acquisition 1: $25M industrial (Columbus, OH) -- 2026 vintage
  Reduces property type HHI: 0.3519 -> 0.2714
  Adds new MSA (geographic diversification)
  Industrial complements MF demand drivers

Acquisition 2: $18M self-storage portfolio (3 facilities, Southeast)
  Further reduces property type HHI: 0.2714 -> 0.2211
  Self-storage has low correlation to MF and office (rho ~ 0.35)
  Adds emerging sector exposure

Acquisition 3: $15M grocery-anchored retail (Minneapolis, MN)
  Adds non-Sunbelt geographic exposure
  Reduces geographic concentration in Sun Belt markets
  Stable cash flow profile anchored by credit tenant

Post-deployment portfolio:
  Value: $238M, 11 assets
  Value HHI: 0.0985 (diversified)
  Property type HHI: 0.2211 (passes)
  Geographic HHI: 0.0970 (highly diversified)
  Vintage HHI: 0.1520 (passes)
```
