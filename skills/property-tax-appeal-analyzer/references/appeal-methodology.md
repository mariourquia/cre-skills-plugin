# Property Tax Appeal Methodology for Commercial Real Estate

## Three Bases of Appeal

Property tax assessments can be challenged on three independent bases. The strongest basis depends on property type, market conditions, and data availability. Often, the strongest approach combines two bases in a single appeal.

---

## Basis 1: Equity (Comparable Assessments)

### When This Is Strongest
- Subject property is assessed at a higher rate (assessed value per SF or per unit) than comparable properties in the same jurisdiction
- Recent reassessment created disparities
- Comparable sales data is limited (making income approach harder to support)
- Simple property types where per-SF or per-unit comparison is intuitive (industrial, retail)

### Methodology

**Step 1: Identify Comparable Properties**
Criteria for comparable selection:
- Same jurisdiction and tax district
- Same property type/class
- Similar size (within 50% of subject)
- Similar age/condition
- Similar location quality (submarket)
- Minimum 3 comparables, ideally 5-8

**Step 2: Calculate Assessment Ratios**
```
Assessment Ratio = Assessed Value / Market Value (or per-unit metric)

Assessment per SF = Assessed Value / Gross Building Area
Assessment per Unit = Assessed Value / Number of Units
```

**Step 3: Build Comparison Table**

| Property | Address | Type | Size (SF) | Assessed Value | $/SF Assessed | Year Built |
|----------|---------|------|-----------|----------------|---------------|-----------|
| Subject | [Address] | Office | 100,000 | $15,000,000 | $150.00 | 1995 |
| Comp 1 | [Address] | Office | 85,000 | $10,200,000 | $120.00 | 1998 |
| Comp 2 | [Address] | Office | 120,000 | $13,200,000 | $110.00 | 1992 |
| Comp 3 | [Address] | Office | 95,000 | $11,400,000 | $120.00 | 1996 |
| Comp 4 | [Address] | Office | 110,000 | $12,100,000 | $110.00 | 1990 |
| Comp 5 | [Address] | Office | 90,000 | $10,800,000 | $120.00 | 1997 |

**Step 4: Calculate Indicated Value**
```
Average comparable $/SF = ($120 + $110 + $120 + $110 + $120) / 5 = $116.00
Indicated assessed value = 100,000 SF * $116.00 = $11,600,000
Current assessment = $15,000,000
Overassessment = $3,400,000 (22.7% above equity level)
```

**Step 5: Quantify Tax Savings**
```
Tax savings = Overassessment * Tax Rate
Tax savings = $3,400,000 * 2.50% = $85,000/year
```

### Data Sources for Equity Analysis
| Source | Coverage | Access |
|--------|----------|--------|
| County assessor's office | Local | Public records, online GIS |
| CoStar / REIS | National | Subscription |
| County tax rolls | Local | Online portal or FOIA request |
| State equalization data | Statewide | Published reports |

---

## Basis 2: Income Approach (Cap Rate Applied to NOI)

### When This Is Strongest
- Income-producing property with demonstrable below-market NOI
- High vacancy or recent tenant loss
- Market cap rates have expanded (rising interest rate environment)
- Property has functional obsolescence reducing income potential
- Assessor used stale or incorrect income assumptions

### Methodology

**Step 1: Establish Market Rent (Potential Gross Income)**
```
Potential Gross Income (PGI) = Gross Leasable Area * Market Rent/SF

Use ACTUAL rent if below market (stronger argument for lower value)
Use MARKET rent if actual rent is above market (assessor may argue otherwise)
```

| Consideration | Use Actual Rent | Use Market Rent |
|---------------|-----------------|-----------------|
| Below-market leases | Yes -- supports lower value | No |
| Above-market leases | No | Yes -- more conservative |
| Vacant space | N/A (no rent) | Yes -- at market rate |
| Renewal risk | Discuss in narrative | Use probability-weighted rent |

**Step 2: Deductions from PGI**
```
Effective Gross Income (EGI) = PGI - Vacancy & Collection Loss - Concessions

Vacancy allowance:
  Actual vacancy (if higher than market) or
  Market vacancy (if property is stabilized) or
  Structural vacancy (frictional: typically 5-10% for commercial)
```

**Step 3: Calculate Net Operating Income**
```
NOI = EGI - Operating Expenses

Operating Expenses include:
  - Property management (3-6% of EGI)
  - Insurance
  - Utilities (landlord-paid)
  - Repairs and maintenance
  - Common area maintenance
  - General and administrative
  - Replacement reserves (2-4% of EGI)

DO NOT INCLUDE:
  - Debt service (mortgage payments)
  - Income taxes
  - Depreciation
  - Capital expenditures (above replacement reserves)
  - Property taxes (appealing this very item -- circular reference)
```

**Note on property taxes in NOI**: Most tax appeal jurisdictions require NOI to be calculated BEFORE property taxes (i.e., property taxes are excluded from operating expenses). This avoids circularity. The assessor then applies the tax rate to the resulting value.

**Step 4: Select Capitalization Rate**
```
Value = NOI / Cap Rate
```

**Cap rate sources and hierarchy of credibility:**

| Source | Weight | Notes |
|--------|--------|-------|
| Recent comparable sales (same submarket, type) | Highest | Direct extraction: NOI / sale price |
| Investor surveys (PwC, CBRE, Newmark, RCA) | High | Published quarterly, property-type-specific |
| Band of investment | Moderate | Mortgage constant * LTV + equity dividend * (1-LTV) |
| Assessor's published cap rates | Reference | Compare to argue assessor's rate is too low |
| Broker opinions | Supporting | Useful but subjective |

**Cap rate adjustment factors:**
| Factor | Adjustment Direction |
|--------|---------------------|
| Inferior location vs. comps | + (higher cap rate = lower value) |
| Older building / deferred maintenance | + |
| Below-average occupancy | + |
| Near-term lease rollover risk | + |
| Superior location vs. comps | - (lower cap rate = higher value) |
| Long-term credit tenants | - |
| Recent renovations | - |

**Step 5: Worked Example**

```
Property: 100,000 SF suburban office building
Current Assessment: $15,000,000

INCOME APPROACH:
  Gross Leasable Area: 85,000 SF (85% efficiency)
  Market Rent: $22.00/SF NNN
  PGI: 85,000 * $22.00 = $1,870,000

  Less: Vacancy & Collection (12%): ($224,400)
  Effective Gross Income: $1,645,600

  Less: Operating Expenses
    Management (4%): ($65,824)
    Insurance: ($42,000)
    Utilities: ($85,000)
    R&M: ($95,000)
    CAM: ($55,000)
    G&A: ($25,000)
    Reserves (3%): ($49,368)
  Total Expenses: ($417,192)

  Net Operating Income: $1,228,408

  Cap Rate (supported by 5 comparables): 8.25%

  Indicated Value: $1,228,408 / 0.0825 = $14,890,400

  Say: $14,900,000

  Overassessment: $15,000,000 - $14,900,000 = $100,000
  Tax savings at 2.50%: $2,500/year
```

In this example, the income approach shows a modest overassessment. If market conditions worsen (higher vacancy, lower rents, higher cap rates), the income approach becomes much more powerful.

**Aggressive but defensible scenario (post-pandemic office):**
```
  Vacancy: 25% (actual)
  Market rent: $20.00/SF (declining market)
  Cap rate: 9.50% (cap rate expansion)

  PGI: 85,000 * $20.00 = $1,700,000
  Less vacancy (25%): ($425,000)
  EGI: $1,275,000
  Less expenses: ($382,500) -- roughly 30% of EGI
  NOI: $892,500
  Value: $892,500 / 0.095 = $9,394,737

  Overassessment: $15,000,000 - $9,400,000 = $5,600,000
  Tax savings at 2.50%: $140,000/year
```

---

## Basis 3: Cost Approach (Replacement Cost Less Depreciation)

### When This Is Strongest
- Special-purpose properties (churches, schools, hospitals, public facilities)
- New construction (replacement cost is closest to market value)
- Properties with significant physical depreciation or functional obsolescence
- Limited comparable sales and income data
- Industrial properties where land + improvements is intuitive

### Methodology

**Step 1: Estimate Replacement Cost New (RCN)**
```
RCN = Cost/SF * Gross Building Area

Sources:
  - Marshall & Swift / CoreLogic cost manual
  - RSMeans Building Construction Cost Data
  - Actual construction cost (if recently built)
  - Contractor estimates
```

**Step 2: Deduct Depreciation**

Three types of depreciation:

| Type | Definition | Measurement | Curable? |
|------|-----------|-------------|---------|
| Physical deterioration | Wear and tear from age and use | Age-life method or component breakdown | Sometimes |
| Functional obsolescence | Design deficiencies reducing utility | Cost to cure or income loss capitalized | Sometimes |
| External (economic) obsolescence | Market/location factors reducing value | Income loss attributable to external factors | No |

**Age-Life Method (Physical Depreciation):**
```
Effective Age / Total Economic Life = Depreciation %

Example:
  Actual age: 30 years
  Effective age (after renovations): 20 years
  Total economic life: 50 years
  Physical depreciation: 20/50 = 40%
```

**Functional Obsolescence Examples:**
- Inadequate ceiling height (warehouse < 28' clear)
- Insufficient parking ratio
- Floor plate too large or too small for market demand
- Single-loaded corridor (inefficient layout)
- No freight elevator in multi-story industrial
- Asbestos or environmental contamination requiring remediation

**External Obsolescence Examples:**
- Declining market / submarket
- Environmental contamination from adjacent property
- Change in traffic patterns reducing accessibility
- Overbuilt market with structural vacancy
- Unfavorable zoning changes

**Step 3: Add Land Value**
```
Depreciated Value = RCN * (1 - Total Depreciation %)
Total Value = Depreciated Value + Land Value

Land Value sources:
  - Comparable land sales
  - Residual land value (from income approach)
  - Assessor's land value allocation (often low, argue for higher land %)
```

**Step 4: Worked Example**

```
Property: 200,000 SF industrial warehouse, built 1990
Current Assessment: $12,000,000

COST APPROACH:
  Replacement Cost New:
    Building: 200,000 SF * $85/SF = $17,000,000
    Site improvements: $1,200,000
    Total RCN: $18,200,000

  Less Depreciation:
    Physical (age-life): Effective age 25 / Economic life 50 = 50%
    Functional obsolescence: 18' clear height (market wants 28'+) = 10%
    External obsolescence: Overbuilt submarket, 15% structural vacancy = 5%
    Total depreciation: 65%

  Depreciated improvement value: $18,200,000 * (1 - 0.65) = $6,370,000

  Land value (comparable sales): $3,000,000

  Total indicated value: $9,370,000

  Overassessment: $12,000,000 - $9,370,000 = $2,630,000
  Tax savings at 2.50%: $65,750/year
```

---

## Appeal Process Framework

### General Timeline

| Step | Typical Deadline | Action |
|------|-----------------|--------|
| Assessment notice received | Varies (Jan-May depending on jurisdiction) | Review immediately |
| Informal review request | 30-60 days after notice | Call assessor, present evidence informally |
| Formal appeal filing | 30-120 days after notice (JURISDICTION SPECIFIC) | File written appeal with review board |
| Hearing preparation | 2-6 months after filing | Prepare evidence package, hire appraiser if needed |
| Hearing | Scheduled by board | Present case (15-60 minutes typical) |
| Decision | 30-90 days after hearing | Written decision from board |
| Further appeal (court) | 30-60 days after board decision | File with tax court or superior court |

### Deadline Tracking by Selected States

| State | Assessment Date | Appeal Deadline | Appeal Body |
|-------|----------------|-----------------|-------------|
| New York | January 1 | March (tentative roll), May (final roll) -- varies by jurisdiction | Board of Assessment Review, then SCAR |
| New Jersey | October 1 | April 1 (county board), then Tax Court | County Board of Taxation |
| California | January 1 (or change of ownership) | September 15 or November 30 | Assessment Appeals Board |
| Texas | January 1 | May 15 or 30 days after notice | Appraisal Review Board (ARB) |
| Illinois | January 1 | 30 days after publication | Board of Review, then PTAB |
| Florida | January 1 | 25 days after TRIM notice (August) | Value Adjustment Board (VAB) |
| Pennsylvania | Varies by county | Varies (check county) | Board of Assessment Appeals |
| Massachusetts | January 1 | February 1 (after Q3 tax bill) | Board of Assessors, then ATB |

**CRITICAL: Missing the filing deadline waives your right to appeal for that tax year. Calendar all deadlines immediately upon acquisition.**

---

## Appeal Brief Template

### Section 1: Property Identification
- Parcel number / tax ID
- Property address
- Owner name / taxpayer
- Property type and description
- Year under appeal
- Current assessed value
- Claimed value (what you believe is correct)

### Section 2: Grounds for Appeal
State which basis (or bases) you are pursuing:
- [ ] Equity (comparable assessments)
- [ ] Income approach
- [ ] Cost approach
- [ ] Other (clerical error, incorrect property data)

### Section 3: Evidence Presentation
(Use the methodology sections above to structure the evidence)

### Section 4: Conclusion and Requested Relief
- State the indicated value from your analysis
- Request the assessment be reduced to indicated value
- State the resulting tax reduction

### Section 5: Exhibits
- Rent roll (if income approach)
- Operating statements (2-3 years)
- Comparable sales data
- Comparable assessment data
- Appraisal report (if commissioned)
- Market surveys (vacancy, rent, cap rates)
- Photos of property condition
- Building plans (if functional obsolescence)

---

## ROI Analysis: Appeal vs. Consultant Cost

### When to Self-Appeal vs. Hire a Consultant

| Assessment | Potential Tax Savings | Recommendation |
|------------|----------------------|---------------|
| < $1M overassessment | < $25,000/yr savings | Self-appeal or small firm |
| $1M-$5M overassessment | $25,000-$125,000/yr | Tax consultant (contingency fee) |
| > $5M overassessment | > $125,000/yr | Tax consultant + independent appraisal |

### Consultant Fee Structures

| Fee Type | Typical Range | Pros | Cons |
|----------|--------------|------|------|
| Contingency | 25-40% of first-year savings | No cost if no savings | Higher total cost on large wins |
| Flat fee | $2,500-15,000 per appeal | Predictable cost | Owner bears risk of no savings |
| Hourly | $200-500/hour | Pay for work performed | Unpredictable total, no alignment |
| Hybrid | $2,500-5,000 retainer + 15-25% contingency | Some alignment + cost control | More complex arrangement |

### ROI Calculation

```
Appeal ROI = (Multi-year tax savings - Consultant cost) / Consultant cost

Example:
  Annual tax savings achieved: $85,000
  Duration of reduced assessment: 3 years (until next reassessment)
  Total savings: $255,000
  Consultant fee (33% of year 1): $28,050

  ROI = ($255,000 - $28,050) / $28,050 = 809%
```

### Portfolio-Level Tax Appeal Strategy

For portfolios of 10+ properties:
1. Screen all assessments annually for overassessment indicators
2. File appeals on all properties exceeding threshold (e.g., >5% above indicated value)
3. Negotiate volume discount with consultant (20-25% contingency vs. 30-40%)
4. Track appeal outcomes and refine screening criteria
5. Budget 0.5-1.0% of property taxes for appeal costs
6. Expected recovery: 5-15% of total portfolio tax liability
