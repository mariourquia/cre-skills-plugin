# Track Record Methodology: GIPS-Compliant Presentation

---

## Purpose

This reference standardizes how a CRE GP presents its investment track record to prospective LPs. The goal is a presentation that is transparent, verifiable, and consistent with Global Investment Performance Standards (GIPS) principles adapted for private real estate. Institutional LPs will benchmark your disclosures against GIPS expectations; deviations will be flagged in their diligence.

---

## Part 1: Gross vs. Net Returns

### 1.1 Definitions

| Metric | Definition | What It Includes | What It Excludes |
|--------|-----------|-----------------|-----------------|
| **Gross IRR** | IRR before GP fees and expenses | All property-level cash flows, capex, debt service, disposition proceeds | Management fees, acquisition fees (if fund-level), carried interest, fund expenses |
| **Net IRR** | IRR after all fees and expenses to the LP | Same as gross MINUS management fees, fund expenses, carried interest, organizational costs | Nothing -- this is the LP's actual return |
| **Gross Equity Multiple** | Total distributions / total invested (before fees) | Property-level returns | Fees |
| **Net Equity Multiple** | Total distributions / total invested (after all fees) | LP's actual money-in vs. money-out | Nothing |

### 1.2 Calculation Standards

**IRR**: Must be time-weighted using actual cash flow dates. Not approximated from annual returns. Include the reinvestment assumption (GIPS assumes reinvestment at the portfolio rate, not risk-free).

```
IRR is the discount rate r that satisfies:
SUM[ CF_t / (1+r)^t ] = 0
where CF_0 = negative (equity invested), CF_1...CF_n = cash distributions,
and CF_final includes reversion proceeds.
```

**Equity Multiple**:
```
EM = (Total Distributions + Unrealized Value of Remaining Investments) / Total Invested Capital
```

### 1.3 Gross-to-Net Bridge

Always show how gross returns translate to net. LPs will compute this themselves; better that you present it transparently.

| Component | Impact on Returns | Typical Range |
|-----------|------------------|---------------|
| Gross IRR | Starting point | -- |
| Less: Management fee drag | -100 to -200bps | 1.0-2.0% annual on committed or invested |
| Less: Acquisition fee (if not offset) | -25 to -75bps | 0.5-1.5% of purchase price |
| Less: Fund expenses (audit, legal, admin) | -10 to -30bps | $100-300K/year for a $50-100M fund |
| Less: Organizational expenses | -5 to -15bps | Amortized over fund life |
| Less: Carried interest | -100 to -400bps | 20% above preferred return |
| **Net IRR** | End result | Typically gross minus 200-500bps |

### 1.4 Worked Example

```
Gross IRR:                     18.5%
Management fee drag:           -1.8%  (1.5% on committed x 4yr avg invested life)
Acquisition fee:               -0.5%  (1.0% on purchase price, not offset)
Fund expenses:                 -0.2%  ($200K/yr on $50M fund)
Org expenses:                  -0.1%  ($150K amortized over 7yr term)
Carried interest:              -2.4%  (20% carry above 8% pref)
----------------------------------------------
Net IRR:                       13.5%
Gross-to-net spread:           5.0%
```

---

## Part 2: Realized vs. Unrealized

### 2.1 Why Separation Matters

Realized returns are based on actual cash received. Unrealized returns depend on current valuations, which are GP estimates. LPs assign much higher confidence to realized returns.

### 2.2 Disclosure Requirements

| Category | What to Show | How to Label |
|----------|-------------|-------------|
| **Fully realized investments** | Actual entry and exit cash flows, dates, IRR, EM | "Realized" |
| **Partially realized (distributions but still held)** | Cash distributed to date + current estimated value | "Partially realized" -- show distributed EM and total EM separately |
| **Unrealized (no distributions, still held)** | Current estimated value vs. invested basis | "Unrealized" -- clearly state valuation methodology and date |

### 2.3 Blended Presentation

| Metric | Realized Only | Realized + Unrealized | Notes |
|--------|-------------|----------------------|-------|
| Gross IRR | [X]% | [X]% | Realized is the credibility number |
| Net IRR | [X]% | [X]% | |
| Gross EM | [X.X]x | [X.X]x | |
| Net EM | [X.X]x | [X.X]x | |
| Number of investments | [X] | [X] | |
| Total equity invested | $[X]M | $[X]M | |

**Rule**: Always show both columns. If unrealized returns are significantly higher than realized, LPs will assume the GP is marking aggressively. If unrealized is similar to or lower than realized, it builds confidence.

### 2.4 Vintage Year Bucketing

Group investments by vintage year (year of initial equity deployment). This allows LPs to compare your performance to peer benchmarks (e.g., Cambridge Associates, Preqin, NCREIF ODCE).

| Vintage | Investments | Equity Deployed | Gross IRR | Net IRR | Net EM | Status |
|---------|------------|----------------|-----------|---------|--------|--------|
| 2020 | 3 | $15.2M | 22.1% | 16.8% | 2.15x | 3 realized |
| 2021 | 2 | $9.8M | 15.4% | 11.2% | 1.72x | 1 realized, 1 unrealized |
| 2022 | 3 | $14.5M | 11.8% | 8.5% | 1.38x | 3 unrealized |
| 2024 | 2 | $8.7M | NM | NM | 1.05x | 2 unrealized (early) |

**NM = Not Meaningful**: Use for investments held less than 12 months where IRR is mathematically meaningless due to short duration.

---

## Part 3: Fee Disclosure

### 3.1 Full Fee Transparency

LPs increasingly demand gross-to-net fee disclosure. Present all fees charged to the fund or to portfolio companies:

| Fee | Rate | Basis | Charged To | Offset? | Annual Estimate |
|-----|------|-------|-----------|---------|----------------|
| Management fee | [X]% | Committed capital (IP) / Invested (post-IP) | Fund | N/A | $[X] |
| Acquisition fee | [X]% | Purchase price | Fund or deal | [Y/N -- offset against mgmt fee?] | $[X] per deal |
| Disposition fee | [X]% | Sale price | Deal | [Y/N] | $[X] per deal |
| Construction mgmt fee | [X]% | Capex budget | Deal | [Y/N] | $[X] per deal |
| Refinancing fee | [X]% | Loan amount | Deal | [Y/N] | $[X] per deal |
| Property mgmt fee | [X]% | EGI | Deal (affiliate) | [Y/N] | $[X] per asset |

### 3.2 Fee Offset Mechanics

If acquisition fees or other deal-level fees offset the management fee, show the calculation:

```
Year 1 Management Fee:          $750,000  (1.5% x $50M committed)
Less: Acquisition fee offset:  -$180,000  (1.0% x $18M acquisition, 100% offset)
Net Management Fee Charged:     $570,000
```

### 3.3 Total Expense Ratio (TER)

Calculate and disclose the TER:

```
TER = (Management fees + Fund expenses + Org expenses) / Average NAV
```

Typical ranges:
- Small fund (<$100M): 2.5-4.0% TER
- Mid-size fund ($100-500M): 1.5-2.5% TER
- Large fund (>$500M): 1.0-1.5% TER

---

## Part 4: GIPS Compliance Considerations

### 4.1 GIPS for Private Real Estate (Key Provisions)

GIPS is a voluntary standard. Most emerging managers are not GIPS-verified, but institutional LPs expect GIPS-consistent presentations. Key principles:

| GIPS Requirement | Practical Implication |
|-----------------|---------------------|
| Include all portfolios in the composite | Cannot cherry-pick winning deals; must include losses |
| Use time-weighted returns for composites | Or money-weighted (IRR) with disclosure |
| Clearly label gross vs. net | Both required |
| Disclose valuation methodology | State frequency, approach, and who performs |
| Disclose fee schedule | All fees affecting net returns |
| Disclose leverage | Fund-level LTV and debt cost |
| Present at least 5 years (or since inception) | Shorter track records are OK if since inception |
| Do not link non-GIPS performance to GIPS-compliant periods | If you became GIPS-compliant in 2023, do not chain 2020-2022 non-GIPS data |

### 4.2 Common GIPS Pitfalls in CRE

| Pitfall | What Goes Wrong | How to Avoid |
|---------|----------------|-------------|
| Excluding losing deals from track record | LP discovers in diligence; kills the raise | Include all investments. Explain losses. |
| Showing "gross of promote" as "net" | Misleads LPs about their actual return | Net must be net of ALL fees and carry |
| Using projected returns for unrealized | Inflates track record | Use current valuation, not proforma |
| Comparing to wrong benchmark | CRE is not the S&P 500 | Use NCREIF ODCE, Preqin private RE, or Cambridge Associates |
| Combining co-invest returns with fund returns | Different fee structures distort the composite | Separate co-invest performance from fund performance |

### 4.3 Non-GIPS Disclosure Language

If you are not GIPS-verified (most emerging managers are not), include this disclosure:

```
Performance Disclosure: [GP Name] has not been independently verified as
complying with the Global Investment Performance Standards (GIPS). The
performance data presented herein has been prepared by [GP Name] and has
not been audited by an independent third party. Gross returns are
presented before management fees, carried interest, and fund-level
expenses. Net returns are presented after all such fees and expenses.
Past performance is not indicative of future results.
```

---

## Part 5: Deal-Level Track Record Table

### 5.1 Standard Format

Present every investment in a single table. This is the LP's primary diligence artifact.

| # | Property | Type | Market | Acq Date | Disp Date | Equity In | Distrib. | Gross IRR | Gross EM | Net IRR | Net EM | Status |
|---|----------|------|--------|----------|-----------|-----------|----------|-----------|----------|---------|--------|--------|
| 1 | [Name] | MF | [City] | [Date] | [Date] | $[X]M | $[X]M | [X]% | [X.X]x | [X]% | [X.X]x | Realized |
| 2 | [Name] | MF | [City] | [Date] | -- | $[X]M | $[X]M* | [X]% | [X.X]x | [X]% | [X.X]x | Unrealized |

*Includes current estimated value for unrealized investments.

### 5.2 Loss Presentation

If you have a loss, present it with the same detail and add a "Lessons Learned" row:

| Field | Detail |
|-------|--------|
| Property | [Name] |
| Equity invested | $[X]M |
| Total distributions | $[X]M |
| Gross IRR | -[X]% |
| Gross EM | [0.X]x |
| Loss amount | $[X]M |
| Root cause | [Specific: e.g., "Tenant default on NNN lease; dark store provision inadequate. REO sale at 30% discount to acquisition."] |
| What changed in process | [Specific: e.g., "Added credit underwriting requirement for all NNN acquisitions. Minimum credit rating now BBB-."] |

---

## Part 6: Benchmark Comparison

### 6.1 Appropriate Benchmarks for CRE

| Benchmark | Best For | Source | Frequency |
|-----------|---------|--------|-----------|
| NCREIF ODCE | Core open-end fund comparison | NCREIF | Quarterly |
| NCREIF Property Index (NPI) | Unlevered property-level returns | NCREIF | Quarterly |
| Cambridge Associates US RE | Private RE fund returns by vintage | Cambridge | Quarterly |
| Preqin Private RE Benchmark | By strategy (core, value-add, opportunistic) | Preqin | Quarterly |
| MSCI/IPD | Global RE benchmarks | MSCI | Quarterly |

### 6.2 How to Present

```
Fund I Net IRR:    13.5%
Cambridge Associates Median (2020 vintage, value-add):  10.2%
Fund I Quartile Ranking:  Top Quartile

Note: Benchmark comparison is to the Cambridge Associates US Private Real
Estate Value-Add composite for the 2020 vintage year. Fund I is not a
member of the Cambridge Associates database. Comparison is for
illustrative purposes only.
```

### 6.3 What Not to Do

- Do not compare a value-add fund to core benchmarks (makes you look better but is misleading)
- Do not compare net returns to gross benchmarks
- Do not compare since-inception returns to trailing 1-year benchmarks
- Do not omit the benchmark when your returns are below median
- Do not create a custom benchmark that conveniently shows outperformance

---

## Part 7: Attribution Analysis

### 7.1 Return Decomposition

Break down gross return into sources:

| Component | Calculation | Example |
|-----------|------------|---------|
| Income return | Cumulative cash distributions / equity invested | 28% of total return |
| NOI growth | (Exit NOI - Entry NOI) x cap rate impact | 35% of total return |
| Cap rate change | Value change from cap rate movement alone | 22% of total return |
| Leverage amplification | Return premium from debt | 15% of total return |

### 7.2 Why Attribution Matters to LPs

LPs use attribution to assess repeatability:
- **NOI growth driven**: Repeatable, skill-based. Strongest signal.
- **Cap rate compression driven**: Market-dependent, not repeatable in all environments.
- **Leverage driven**: Mechanical, not skill. Any manager can lever up.
- **Income driven**: Stable but low growth. Appropriate for core, not value-add.

A GP whose returns are 60%+ NOI-growth-driven has a more compelling story than one whose returns are 60% cap-rate-compression-driven.

### 7.3 Worked Example

| Component | Fund I | Fund II | Combined |
|-----------|--------|---------|----------|
| Income return | 3.2% | 2.8% | 3.0% |
| NOI growth | 7.8% | 6.5% | 7.2% |
| Cap rate effect | 4.1% | 1.2% | 2.7% |
| Leverage effect | 3.4% | 3.0% | 3.2% |
| **Gross IRR** | **18.5%** | **13.5%** | **16.1%** |

Interpretation: Fund I benefited from 410bps of cap compression (2020-2023 was a favorable rate environment). Fund II, in a higher-rate environment, generated only 120bps from cap movement. NOI growth remained strong at 650bps, confirming the operational value-creation thesis is durable across rate cycles.
