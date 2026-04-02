# Benchmark Methodology: NCREIF NPI/ODCE Comparison & GIPS Compliance

## NCREIF Property Index (NPI) Overview

The NPI measures quarterly total returns of institutional-quality commercial real estate held in a fiduciary environment. It is an **unleveraged**, appraisal-based index.

### NPI Characteristics
- **Universe**: 9,000+ properties, $900B+ market value
- **Property types**: Office, Industrial, Retail, Apartment, Hotel
- **Geographic**: U.S. only, reported by NCREIF region (East, Midwest, South, West)
- **Return basis**: Unleveraged, before fees
- **Valuation**: Appraisal-based (quarterly or more frequent)
- **Weighting**: Value-weighted

### NPI Limitations for Fund Comparison
- Unleveraged: most funds use 50-70% LTV leverage
- Appraisal lag: values update quarterly, not marking to market
- Survivorship bias: properties removed upon sale (often distressed)
- No fees: does not reflect management fee or promote drag
- Property-level only: no fund-level expenses (admin, legal, audit)

---

## NCREIF ODCE (Open-End Diversified Core Equity) Index

The ODCE tracks returns of open-end commingled funds pursuing a core strategy. It is a **fund-level** benchmark that includes leverage effects.

### ODCE Characteristics
- **Universe**: ~30 open-end core funds
- **Return basis**: Net of fund-level fees (management fee included, promote varies)
- **Leverage**: Reflects actual fund leverage (typically 20-30% LTV)
- **Valuation**: Appraisal-based at fund level
- **Weighting**: Value-weighted (equal-weight also available)
- **Cash drag**: Includes impact of cash holdings and subscription/redemption queues

### When to Use NPI vs. ODCE

| Fund Type | Primary Benchmark | Secondary Benchmark |
|-----------|------------------|---------------------|
| Open-end core | ODCE (VW or EW) | NPI (property-level attribution) |
| Closed-end core | ODCE (gross) | NPI + leverage adjustment |
| Value-add | NPI + 200-400 bps | ODCE + 200 bps |
| Opportunistic | Absolute return target (15%+ net IRR) | NPI + 400-600 bps |
| Sector-specific | NPI sector sub-index | ODCE sector (if available) |

---

## Total Return Decomposition

### Component Calculation

```
Total Return = Income Return + Appreciation Return

Where:
  Income Return = Net Operating Income / Beginning Market Value
  Appreciation Return = (Ending MV - Beginning MV - Capital Expenditures) / Beginning MV
```

For leveraged funds, add the leverage component:

```
Leveraged Return = Unleveraged Return + (Unleveraged Return - Cost of Debt) x (Debt / Equity)

Example:
  Unleveraged Return = 7.0%
  Cost of Debt = 4.5%
  LTV = 60% (Debt/Equity = 1.5)
  Leveraged Return = 7.0% + (7.0% - 4.5%) x 1.5 = 7.0% + 3.75% = 10.75%
```

### Return Attribution Framework

| Attribution Level | Components |
|------------------|------------|
| **Market** | Beta exposure to property market (NPI return x fund beta) |
| **Sector allocation** | Over/underweight to property types vs. benchmark |
| **Geographic allocation** | Over/underweight to regions vs. benchmark |
| **Property selection** | Individual asset alpha within sector/geography |
| **Active management** | NOI growth above market, capex timing, lease execution |
| **Leverage** | Spread between property return and cost of debt x leverage ratio |
| **Fee drag** | Management fee + promote carry reduction from gross to net |

---

## Vintage Year Comparison

### J-Curve Analysis

Closed-end funds exhibit a J-curve pattern: negative returns in early years due to fees on committed (not invested) capital, transition costs, and value creation lag.

**Typical J-Curve by Strategy**:

| Year | Core | Value-Add | Opportunistic |
|------|------|-----------|---------------|
| 1 | -1% to +2% | -3% to 0% | -5% to -2% |
| 2 | +3% to +6% | 0% to +5% | -2% to +3% |
| 3 | +5% to +8% | +5% to +12% | +5% to +15% |
| 4 | +6% to +9% | +8% to +15% | +10% to +25% |
| 5 | +6% to +8% | +10% to +18% | +15% to +30% |

**Vintage year comparison rules**:
1. Compare only within same strategy (value-add to value-add)
2. Allow +/- 1 year vintage window for peer universe
3. Normalize for deployment pace: a fund 90% deployed in year 2 vs. 60% deployed will have different J-curves
4. Adjust for subscription line usage: report IRR both with and without facility

### Peer Universe Construction

```yaml
universe_criteria:
  strategy: same as subject fund
  vintage: fund_vintage +/- 1 year
  geography: same primary market focus (US, Europe, Asia)
  fund_size: 0.5x to 2.0x subject fund size
  minimum_peers: 10 funds for statistical validity
  data_source: Preqin, PitchBook, Cambridge Associates, Burgiss
```

**Quartile ranking**:
- Top quartile: >= 75th percentile
- Second quartile: 50th-74th percentile
- Third quartile: 25th-49th percentile
- Bottom quartile: < 25th percentile

---

## Alpha Calculation

### Time-Weighted Return Alpha

```
Alpha (TWR) = Fund Net TWR - Benchmark TWR

Leverage-adjusted Alpha = Fund Net TWR - [Benchmark TWR + (Benchmark TWR - Risk-Free Rate) x (Fund Leverage - Benchmark Leverage)]
```

### IRR-Based Alpha (Kaplan-Schoar PME)

The Public Market Equivalent adjusts for timing of cash flows:

```
KS-PME = (PV of distributions at benchmark return) / (PV of contributions at benchmark return)

If KS-PME > 1.0: fund outperformed the benchmark on a cash-flow-adjusted basis
If KS-PME < 1.0: fund underperformed
```

### Direct Alpha (Gredil-Griffiths-Stucke)

```
Direct Alpha = IRR of PME-adjusted cash flows

Where each cash flow is future-valued to the end of the measurement period using the benchmark return, then the IRR of these adjusted flows is calculated.
```

---

## GIPS Compliance Requirements

### CFA Institute GIPS 2020 Standards -- Real Estate

**Composite Construction Rules**:
1. All actual, fee-paying, discretionary portfolios must be included in at least one composite
2. Composites must be defined by strategy before performance results are known
3. Terminated portfolios must remain in the composite for the full period they were managed
4. New portfolios must be added at the start of the next full measurement period after funding
5. Non-discretionary portfolios may be excluded with documentation of non-discretionary status

**Required Disclosures**:
- Firm definition and total firm assets
- Composite description including strategy, benchmark, creation date
- Benchmark description and any custom benchmark methodology
- Fee schedule: management fee, performance fee structure
- Composite returns: gross and net of fees
- Number of portfolios in composite (or state "5 or fewer" if disclosing count is misleading)
- Composite dispersion: internal dispersion measure (standard deviation if 6+ portfolios)
- 3-year annualized ex-post standard deviation of composite and benchmark
- Percentage of firm assets represented by the composite

**Return Calculation Standards**:
- Time-weighted returns required (modified Dietz or true daily acceptable)
- Returns must be calculated at least quarterly
- Composite returns must be asset-weighted (beginning-of-period values)
- External cash flows: use actual date of cash flow, not month-end approximation
- Real estate: income return and capital return components must be separately presented

### Worked Example: 5-Year Fund vs. ODCE

**Subject**: Metro Core Real Estate Fund
**Vintage**: 2021 | **Strategy**: Core | **Benchmark**: NCREIF ODCE (Value-Weighted)

| Period | Fund Net TWR | ODCE TWR | Alpha | Fund Income | ODCE Income | Fund Appreciation | ODCE Appreciation |
|--------|-------------|----------|-------|-------------|-------------|-------------------|-------------------|
| 2021 | 18.4% | 21.1% | -2.7% | 3.8% | 3.6% | 14.6% | 17.5% |
| 2022 | -4.2% | -5.8% | +1.6% | 4.1% | 3.9% | -8.3% | -9.7% |
| 2023 | 2.8% | 1.5% | +1.3% | 4.3% | 4.1% | -1.5% | -2.6% |
| 2024 | 7.1% | 6.2% | +0.9% | 4.4% | 4.2% | 2.7% | 2.0% |
| 2025 | 8.9% | 7.6% | +1.3% | 4.5% | 4.3% | 4.4% | 3.3% |
| **5-Yr Ann.** | **6.4%** | **5.6%** | **+0.8%** | **4.2%** | **4.0%** | **2.2%** | **1.6%** |

**Attribution Analysis**:

| Source | Contribution to Alpha |
|--------|--------------------|
| Income premium (higher occupancy, better lease execution) | +0.2% |
| Appreciation premium (value creation, better acquisitions) | +0.6% |
| Leverage effect (lower cost of debt, better timing) | +0.3% |
| Fee drag (fund fees higher than ODCE average) | -0.3% |
| **Net Alpha** | **+0.8%** |

**Peer Ranking** (Core funds, 2021 vintage, 15 funds in universe):

| Metric | Fund | Median | Rank | Quartile |
|--------|------|--------|------|----------|
| Net TWR (5-yr ann.) | 6.4% | 5.8% | 4/15 | Top |
| Sharpe Ratio | 0.82 | 0.64 | 3/15 | Top |
| Max Drawdown | -4.2% | -5.1% | 5/15 | Top |
| Income Return | 4.2% | 4.0% | 6/15 | Second |
| Volatility (std dev) | 7.1% | 8.3% | 4/15 | Top |

**GIPS Composite Presentation** (abridged):

```
Metro Core Real Estate Composite
Inception: January 1, 2021
Benchmark: NCREIF ODCE (Value-Weighted)
Fee Schedule: 1.00% management fee on committed capital (investment period),
              0.75% on invested capital (post-investment period)

                    Composite    Composite    Benchmark    Composite    Number of    Total Firm
Year    Gross (%)   Net (%)      (%)          Dispersion   Portfolios   Assets ($M)
2021    19.6        18.4         21.1         n/a          <=5          2,450
2022    -3.1        -4.2         -5.8         n/a          <=5          2,180
2023    4.0         2.8          1.5          n/a          <=5          2,310
2024    8.3         7.1          6.2          n/a          <=5          2,520
2025    10.1        8.9          7.6          n/a          <=5          2,780

3-Year Annualized Standard Deviation:
  Composite: 5.2%
  Benchmark: 5.8%

Composite contains 3 portfolios. Internal dispersion is not presented
as composite contains fewer than 6 portfolios.
```

**Notes for compliance**:
- Gross returns are presented before management fees and before performance allocation
- Net returns are presented after management fees and after performance allocation
- Benchmark does not incur management fees; ODCE returns are net of fund-level fees for constituent funds
- External valuations are performed quarterly by independent MAI-designated appraisers
- The firm claims compliance with the Global Investment Performance Standards (GIPS) and has prepared and presented this report in compliance with GIPS standards
- The firm has been independently verified for the periods 2019-2025
