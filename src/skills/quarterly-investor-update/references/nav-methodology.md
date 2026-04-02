# NAV Methodology Reference

---

## Purpose

This reference standardizes Net Asset Value (NAV) calculation for CRE fund quarterly reporting. NAV is the single most scrutinized number in an LP update because it drives the equity multiple, the promote calculation, and the LP's perception of whether the GP is a credible fiduciary. Getting NAV wrong -- in either direction -- erodes trust.

---

## Part 1: NAV Approaches

### 1.1 Three Standard Approaches

| Approach | Method | When to Use | Strengths | Weaknesses |
|----------|--------|------------|-----------|-----------|
| **Income Capitalization** | NOI / Cap Rate = Value | Most common for stabilized CRE. Quarterly internal valuations. | Simple, transparent, directly tied to operating performance | Highly sensitive to cap rate assumption; does not capture lease-by-lease detail |
| **Discounted Cash Flow (DCF)** | PV of projected cash flows + PV of reversion | Best for value-add, lease-up, assets with irregular cash flows | Captures timing of cash flows, renovation ramps, lease expirations | Requires many assumptions (rent growth, exit cap, discount rate); model complexity invites manipulation |
| **Sales Comparison** | Price per unit/SF from recent comparable sales | Useful as a cross-check; primary method for land and non-income assets | Market-based, easily verified | Comps may not be truly comparable; market thinness in some submarkets |

**Best practice**: Use income capitalization as the primary method for quarterly NAV. Use DCF for value-add assets in active renovation/lease-up. Use sales comparison as a cross-check on both. Disclose which method is used for each asset.

### 1.2 Income Capitalization -- Detailed

```
Property Value = Stabilized NOI / Cap Rate
```

**Which NOI?**

| NOI Definition | Use When | Caution |
|---------------|----------|---------|
| Trailing 12-month (T-12) actual | Stabilized assets with consistent NOI | May lag if rents recently increased |
| Forward 12-month (NTM) projected | Assets with signed leases at higher rents not yet in T-12 | Projection risk; must disclose assumptions |
| Annualized current quarter | Mid-renovation or lease-up | Volatile; can overstate or understate |
| Underwritten stabilized NOI | Value-add assets pre-stabilization | Most aggressive; use only with DCF cross-check |

**Rule**: For quarterly NAV, use T-12 actual NOI for stabilized assets and NTM projected for value-add with explicit disclosure of assumptions.

**Which Cap Rate?**

| Source | Description | Reliability |
|--------|------------|-------------|
| Recent comparable sales | Cap rates from sales of similar assets in the submarket within 6 months | Best if comps exist; thin in some markets |
| Broker opinion of value (BOV) | Informal valuation from 2-3 brokers | Free; useful as a range; not independently verifiable |
| Third-party appraisal | USPAP-compliant appraisal | Gold standard but expensive ($5-15K per asset); typically annual |
| Market data services | CoStar, CBRE, JLL cap rate surveys by market/type | Lagging; reflect broad market, not asset-specific |
| Internal estimate | GP's judgment based on experience and data | Most common for quarterly; must disclose methodology |

### 1.3 DCF Method -- Key Parameters

| Parameter | Typical Range | Sensitivity | Notes |
|-----------|-------------|-------------|-------|
| Discount rate | 7-12% | High | Should reflect asset risk; equity return expectation |
| Projection period | 5-10 years | Medium | Match to expected hold |
| Terminal cap rate | Going-in + 25-100bps | Very High | Small changes in terminal cap produce large value swings |
| Rent growth | 2-4%/yr | High | Must be supportable by submarket data |
| Expense growth | 2-3.5%/yr | Medium | Insurance and tax growth have exceeded CPI recently |
| Vacancy | 3-7% | Medium | Market-dependent |
| Capex reserves | $250-500/unit/yr (MF) | Low-Medium | Often underestimated |

---

## Part 2: Cap Rate Sensitivity

### 2.1 Why Cap Rate Sensitivity Matters

A 50bps change in cap rate on a $10M asset valued at a 5.50% cap rate:

```
Value at 5.50%: $10,000,000
Value at 5.00%: $11,000,000 (+$1.0M, +10.0%)
Value at 6.00%: $9,167,000  (-$833K, -8.3%)
```

The relationship is non-linear. Cap rate compression creates disproportionately more value than the same magnitude of expansion destroys. This asymmetry should be disclosed.

### 2.2 Cap Rate Sensitivity Table -- Template

For each asset in the portfolio, provide this table in the quarterly update (or at minimum in the annual report):

**Asset: [Name] | T-12 NOI: $[X]**

| Cap Rate | Implied Value | vs. Carrying Value | LTV at Value |
|----------|-------------|-------------------|-------------|
| [Base - 100bps] | $[X] | +[X]% | [X]% |
| [Base - 50bps] | $[X] | +[X]% | [X]% |
| **[Base (carrying)]** | **$[X]** | **--** | **[X]%** |
| [Base + 50bps] | $[X] | -[X]% | [X]% |
| [Base + 100bps] | $[X] | -[X]% | [X]% |

### 2.3 Worked Example

**142 Ferry Street | T-12 NOI: $1,085,000 | Carrying cap: 5.50%**

| Cap Rate | Implied Value | vs. Carrying | LTV |
|----------|-------------|-------------|-----|
| 4.50% | $24,111K | +22.4% | 31.5% |
| 5.00% | $21,700K | +10.1% | 35.0% |
| **5.50%** | **$19,727K** | **--** | **38.5%** |
| 6.00% | $18,083K | -8.3% | 42.0% |
| 6.50% | $16,692K | -15.4% | 45.5% |

**Portfolio-level sensitivity** (aggregate T-12 NOI: $4,988K):

| Cap Rate | Portfolio Value | NAV | NAV/Unit | vs. Current |
|----------|---------------|-----|----------|-------------|
| 5.00% | $99,760K | $67,450K | $337.25 | +$225.25 |
| 5.25% | $95,010K | $62,700K | $313.50 | +$201.50 |
| **5.42% (carrying)** | **$92,029K** | **$59,719K** | **$298.60** | **--** |
| 5.75% | $86,748K | $54,438K | $272.19 | -$26.41 |
| 6.00% | $83,133K | $50,823K | $254.12 | -$44.48 |

---

## Part 3: Disclosure Standards

### 3.1 Minimum Quarterly Disclosures

Every quarterly update should include:

| Disclosure | Required | Recommended | Notes |
|-----------|----------|-------------|-------|
| NAV total and per unit | Yes | | |
| Methodology used per asset | Yes | | Income cap, DCF, or appraisal |
| Cap rate used per asset | Yes | | With source |
| NOI used per asset (T-12 or NTM) | Yes | | Specify which |
| NAV bridge (QoQ change) | Yes | | See template |
| Cap rate sensitivity table | | Yes | At least at portfolio level |
| Date of last third-party appraisal | Yes | | Per asset |
| Unrealized vs. realized gains | Yes | | LPs need to know what is paper vs. cash |
| GP promote accrual | Yes | | If above preferred return threshold |
| Debt balances and LTV | Yes | | Per asset |

### 3.2 Annual Disclosures (Beyond Quarterly)

| Disclosure | Notes |
|-----------|-------|
| Third-party appraisals for all assets | Annual or biannual depending on LPA |
| Audited financial statements | Required by most LPAs |
| Promote calculation detail | Waterfall showing LP/GP split |
| Fee summary | Management fee, acquisition fee, disposition fee, etc. |
| Related-party transactions | Any GP affiliates providing services to the fund |

### 3.3 Valuation Policy Language

Include this (or similar) in the fund's LPA and reference it in each quarterly:

```
Valuation Policy: Properties are valued quarterly using the income capitalization
approach, with cap rates derived from recent comparable sales, broker opinions of
value, and third-party market data. Third-party USPAP-compliant appraisals are
obtained annually for each property (or at acquisition and disposition). The General
Partner reserves the right to adjust valuations based on material events between
appraisals. All valuation assumptions are disclosed in the quarterly investor update.
```

---

## Part 4: Common NAV Pitfalls

### 4.1 Aggressive NAV Practices (Red Flags for LPs)

| Practice | Why It Is Problematic | Better Approach |
|----------|---------------------|----------------|
| Using NTM NOI with compressed cap rate | Double-counting growth: higher NOI AND lower cap | Use NTM NOI with current cap rate, or T-12 NOI with compressed cap -- not both |
| No third-party appraisals | GP marking own assets without external check | Annual appraisals minimum; quarterly broker BOV as interim |
| Cap rate cherry-picking | Using lowest comp cap rate; ignoring higher-cap sales | Report the range and explain where the subject falls within it |
| Ignoring capex in NOI | Deferred maintenance artificially inflates NOI | Deduct normalized capex reserves ($250-500/unit/yr for MF) |
| Promoting off unrealized NAV | GP takes promote on paper gains before realization | LPA should specify promote paid only on realized events |
| Smoothing NOI across quarters | Averaging to hide a bad quarter | Report actual quarterly NOI with variance explanation |

### 4.2 Conservative NAV Practices (GP Credibility Builders)

| Practice | Why It Builds Trust |
|----------|-------------------|
| Use T-12 actual NOI (not projected) | LPs can verify against bank statements |
| Apply 25-50bps cushion to exit cap vs. current market | Shows GP is not assuming cap compression |
| Disclose cap rate range, not a single point | Transparency about valuation uncertainty |
| Note properties where internal val > last appraisal | Flags where GP's view may be optimistic |
| Separate realized vs. unrealized gains in NAV bridge | LPs know what is cash vs. paper |

---

## Part 5: NAV Reconciliation Workflow

### 5.1 Quarterly NAV Checklist

| Step | Action | Responsible | Timing |
|------|--------|------------|--------|
| 1 | Compile T-12 actual NOI per asset from accounting | Fund Accountant | Day 1-5 |
| 2 | Collect cap rate data: recent sales, broker BOVs, market surveys | Acquisitions / Asset Mgmt | Day 1-10 |
| 3 | Calculate property values using income cap (or DCF if value-add) | Asset Manager | Day 5-10 |
| 4 | Cross-check with sales comparison approach | Asset Manager | Day 10-12 |
| 5 | Compile debt balances, accrued liabilities, cash balances | Fund Accountant | Day 10-12 |
| 6 | Calculate NAV, NAV per unit, NAV bridge | Fund Accountant | Day 12-15 |
| 7 | GP review and sign-off | GP Principal | Day 15-18 |
| 8 | Fund administrator review (if applicable) | Administrator | Day 18-22 |
| 9 | Distribute quarterly update to LPs | Investor Relations | Day 25-30 |

### 5.2 NAV Audit Trail

Maintain a quarterly NAV workbook with:

```
Tab 1: Summary (NAV per unit, QoQ change, YoY change)
Tab 2: Property Values (per asset: NOI used, cap rate, value, source, prior quarter)
Tab 3: Cap Rate Support (comp sales, BOVs, market data with dates and sources)
Tab 4: Debt Summary (per loan: balance, rate, maturity, LTV)
Tab 5: NAV Bridge (QoQ waterfall with line-by-line explanation)
Tab 6: Sensitivity (cap rate sensitivity at asset and portfolio level)
Tab 7: Appraisal Log (date, firm, value per asset; flag if >12 months stale)
```

---

## Part 6: Regulatory and Institutional Considerations

### 6.1 ILPA Principles

The Institutional Limited Partners Association (ILPA) recommends:
- Quarterly NAV reporting within 45 days of quarter-end (60 days acceptable)
- Annual audited financials within 120 days of year-end
- Standardized fee and expense reporting
- Clear valuation policy in the LPA with GP discretion boundaries
- Advisory committee review of valuations where GP has a conflict

### 6.2 GAAP vs. Tax vs. NAV

| Basis | Purpose | Differences from NAV |
|-------|---------|---------------------|
| GAAP (ASC 820) | Financial reporting | Fair value hierarchy (Level 1/2/3); may use DCF with market participant assumptions |
| Tax (Schedule K-1) | Tax reporting | Cost basis with depreciation; does not reflect market value |
| NAV (fund reporting) | LP reporting, promote calc | Market value of assets less liabilities; GP's best estimate |

These three numbers will differ. Disclose which basis is used in each context. LPs primarily care about NAV but need K-1 for taxes and GAAP for their own portfolio reporting.

### 6.3 Conflicts of Interest in NAV

The GP has inherent conflicts in NAV calculation:
- Higher NAV = higher management fee (if AUM-based) and closer to promote threshold
- Lower NAV at acquisition = higher apparent return at exit

**Mitigations**:
- Annual third-party appraisals
- LP advisory committee with valuation oversight
- Fund administrator as independent NAV calculator
- Clear LPA language on valuation methodology and GP discretion limits
- Cap rate sensitivity disclosure so LPs can form their own view
