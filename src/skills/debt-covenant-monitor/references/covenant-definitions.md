# CRE Loan Covenant Definitions and Monitoring Framework

## Overview

Loan covenants are financial performance tests embedded in commercial real estate loan documents. Breach of a covenant can trigger default provisions, cash sweeps, or acceleration of the loan. This reference defines standard covenants, distinguishes between lender calculation methods, and provides an early warning methodology.

---

## Covenant 1: Debt Service Coverage Ratio (DSCR)

### Definition
```
DSCR = Net Operating Income / Annual Debt Service
```

### Lender vs. Standard Calculation

| Component | Standard Calculation | Typical Lender Calculation | Impact |
|-----------|---------------------|---------------------------|--------|
| NOI | Trailing 12-month actual NOI | Often uses "adjusted NOI" or "underwritten NOI" | Lender version may be lower |
| Revenue | Actual collected rent | May exclude percentage rent, parking, other income | Lower NOI |
| Vacancy | Actual vacancy | May impose minimum vacancy deduction (5-10%) even if fully occupied | Lower NOI |
| Expenses | Actual operating expenses | May impute management fee (3-5%) even if self-managed | Lower NOI |
| Reserves | May or may not include | Often deducts replacement reserves ($250-500/unit MF, $0.25-0.50/SF commercial) | Lower NOI |
| Ground rent | Deducted if applicable | Always deducted | Same |
| Debt service | Actual P&I payments | May use "stressed" debt service (e.g., 25-yr amortization even if I/O period) | Higher DS |
| Interest rate | Actual rate | May use DSCR floor rate or swap rate if floating | Higher DS |

**Common lender adjustments that reduce DSCR:**
1. Deducting replacement reserves from NOI (even if not actually spent)
2. Imposing minimum vacancy factor
3. Using imputed management fee
4. Excluding non-recurring revenue items
5. Amortizing debt service even during interest-only period
6. Using a higher "stress" interest rate for floating-rate loans

### DSCR Covenant Thresholds

| Loan Type | Typical Minimum DSCR | Lockbox/Cash Sweep Trigger | Hard Default Trigger |
|-----------|---------------------|---------------------------|---------------------|
| Agency (Fannie/Freddie) | 1.25x | 1.20x | 1.10x |
| CMBS (conduit) | 1.25x-1.30x | 1.20x | 1.10x |
| Balance sheet (bank) | 1.20x-1.35x | 1.15x-1.25x | 1.05x-1.15x |
| Bridge/transitional | 1.00x-1.15x | Varies | Below 1.00x |
| Construction | N/A during construction | Tested at stabilization | Completion guaranty |
| Mezzanine | 1.10x-1.20x (combined) | 1.05x-1.10x | 1.00x |

### DSCR Testing Frequency

| Loan Type | Testing Frequency | Reporting Deadline |
|-----------|-------------------|-------------------|
| Agency | Quarterly | 45 days after quarter-end |
| CMBS | Quarterly | 30-45 days after quarter-end |
| Bank | Quarterly or semi-annually | 30-60 days after period-end |
| Bridge | Monthly (during transition) | 30 days after month-end |

---

## Covenant 2: Loan-to-Value Ratio (LTV)

### Definition
```
LTV = Outstanding Loan Balance / Property Value
```

### Appraised vs. Mark-to-Market Value

| Method | Definition | When Used | Implications |
|--------|-----------|----------|-------------|
| Appraised value (origination) | Third-party appraisal at loan closing | Baseline; may be used for full term | Stale in declining markets -- overstates value |
| Updated appraisal | New third-party appraisal during loan term | Lender-triggered (at lender's discretion and cost) | Can trigger LTV breach if value has declined |
| Mark-to-market (broker opinion) | BPO or internal lender valuation | Quarterly surveillance (CMBS) | Less formal, but can trigger watchlist |
| Assessed value | Tax assessor's value | Rarely used for loan covenants | Often lags market by 1-3 years |
| Income-implied value | NOI / market cap rate | Quarterly (if income-tested) | Most responsive to NOI changes |

### LTV Covenant Thresholds

| Loan Type | Maximum LTV at Origination | Cash Sweep Trigger | Hard Default Trigger |
|-----------|---------------------------|--------------------|--------------------|
| Agency | 75-80% | 80-85% | >90% |
| CMBS (conduit) | 65-75% | 75-80% | >85% |
| Balance sheet (bank) | 65-75% | 75-80% | >80-85% |
| Bridge | 70-80% (as-is), 80-85% (as-stabilized) | Varies | Varies |
| Mezzanine (combined) | 75-85% | 85-90% | >90% |

### LTV Triggers for Lender Action

| LTV Level | Lender Action |
|-----------|--------------|
| At origination LTV | Normal servicing |
| +5% above origination | Watchlist, increased monitoring |
| +10% above origination | Cash sweep may activate |
| +15% above origination | Lender may require paydown or additional collateral |
| >90% | Potential acceleration, workout discussions |
| >100% | Loan is underwater; lender will pursue remedies |

---

## Covenant 3: Occupancy

### Physical vs. Economic Occupancy

| Metric | Definition | Calculation |
|--------|-----------|-------------|
| Physical occupancy | % of rentable SF that is leased (signed lease) | Leased SF / Total Rentable SF |
| Economic occupancy | % of potential revenue being collected | Collected Rent / Potential Gross Rent at Market |

**Why the distinction matters:**

Physical occupancy can be misleading:
- Tenant signed lease but paying below-market rent
- Tenant in free rent period (physically occupied, no revenue)
- Tenant in default (occupied but not paying)
- Lease signed but tenant not yet in occupancy (gap period)

```
Example:
  100,000 SF building, market rent $30/SF
  Potential Gross Revenue: $3,000,000

  Tenant A: 50,000 SF at $30/SF = $1,500,000 (paying)
  Tenant B: 25,000 SF at $22/SF = $550,000 (below market, paying)
  Tenant C: 15,000 SF at $30/SF = $0 (6-month free rent)
  Vacant: 10,000 SF

  Physical occupancy: 90,000 / 100,000 = 90%
  Economic occupancy: ($1,500,000 + $550,000) / $3,000,000 = 68.3%
```

Most lender covenants test physical occupancy, but economic occupancy is what drives DSCR. Monitor both.

### Occupancy Covenant Thresholds

| Loan Type | Minimum Occupancy (Physical) | Cash Sweep Trigger |
|-----------|-----------------------------|--------------------|
| Agency (stabilized) | 85-90% | 80-85% |
| CMBS | 80-85% | 75-80% |
| Bank | 75-85% | 70-80% |
| Bridge (lease-up) | Tested at stabilization milestone | Below projected absorption |

### Key Lease Events Affecting Occupancy Covenants

| Event | Impact | Lead Time |
|-------|--------|-----------|
| Lease expiration (no renewal) | Physical and economic occupancy drop | 6-18 months notice (track roll schedule) |
| Tenant default/bankruptcy | Economic occupancy drops immediately | Variable |
| Free rent period commencement | Economic occupancy drops | Per lease schedule |
| Tenant contraction (partial termination) | Occupancy drops by vacated SF | Per lease termination clause |
| Major new lease signing | Occupancy increases (may lag for buildout) | 3-6 months from signing to rent commencement |

---

## Covenant 4: Debt Yield

### Definition
```
Debt Yield = NOI / Outstanding Loan Balance
```

### Interpretation
Debt yield is a measure of loan risk independent of cap rates and interest rates. It answers: "If I had to foreclose today, what return would the property generate on my loan balance?"

| Debt Yield | Risk Level | Typical Loan Type |
|-----------|-----------|-------------------|
| > 12% | Conservative | Agency, conservative bank |
| 10-12% | Moderate | Standard CMBS, bank |
| 8-10% | Moderate-Aggressive | Higher-leverage CMBS, bridge |
| 6-8% | Aggressive | Bridge, mezzanine |
| < 6% | High risk | Distressed or over-leveraged |

### Debt Yield vs. DSCR vs. LTV

| Metric | What It Measures | Influenced By Interest Rate? | Influenced By Cap Rate? |
|--------|-----------------|------------------------------|------------------------|
| DSCR | Income vs. debt service | Yes (directly) | No |
| LTV | Leverage vs. value | No | Yes (directly) |
| Debt Yield | Income vs. loan amount | No | No |

Debt yield is the most "clean" metric because it is independent of both interest rates and cap rates. It is gaining prevalence, especially in CMBS underwriting.

---

## Covenant 5: Net Worth and Liquidity

### Definition
```
Net Worth = Guarantor's Total Assets - Total Liabilities
Liquidity = Guarantor's Cash + Cash Equivalents + Marketable Securities
```

### Typical Requirements

| Loan Type | Net Worth Requirement | Liquidity Requirement |
|-----------|----------------------|----------------------|
| Agency | Borrower net worth >= loan balance | Liquid assets >= 10% of loan balance |
| CMBS | Minimal (non-recourse structure) | Minimal (carveout guarantor requirements) |
| Bank | Guarantor net worth >= loan balance | Liquid assets >= 10-15% of loan balance |
| Bridge | Borrower net worth >= loan balance | Liquid assets >= 10% of loan balance |
| Construction | Guarantor net worth >= 1.0x loan | Liquid assets >= 15-20% of total project cost |

### Testing and Reporting
- Frequency: Annually (with annual financial statement delivery)
- Documentation: Certified personal financial statement or audited entity financials
- Deadline: 90-120 days after fiscal year-end
- Failure to deliver: Often an independent covenant default

---

## Covenant 6: Additional Loan-Specific Covenants

### Lease Approval Covenant
- Lender approval required for leases above [SF] threshold or below [term] or [rent] floor
- CMBS: often requires servicer approval for leases > 10,000 SF or > 10 years
- Bank: varies, but commonly for major leases (> 20% of NRA)

### Capital Expenditure / Reserve Covenant
- Monthly escrow for replacement reserves ($250-500/unit MF, $0.25-0.50/SF commercial)
- Restriction on withdrawals without lender approval
- Annual budget approval for capex above threshold

### Insurance Covenant
- Maintain specified coverage types and limits
- Lender named as mortgagee/loss payee
- Evidence of insurance due 30 days before expiration
- Failure to maintain: lender may force-place at borrower's expense

### Transfer / Change of Control
- Prohibition or restriction on equity transfers above [threshold] %
- Key principal / guarantor cannot be removed without lender consent
- CMBS: strict transfer restrictions (defeasance or yield maintenance required)

---

## Hard Default vs. Cash Trap/Sweep Triggers

### Distinction

| Feature | Cash Trap/Sweep | Hard Default |
|---------|----------------|-------------|
| Severity | Warning level | Critical |
| Cash flow impact | Excess cash flow swept to lender-controlled reserve | Entire cash flow may be redirected |
| Cure available? | Yes, by meeting threshold for consecutive quarters | Yes, but more difficult and costly |
| Acceleration? | No | Yes (at lender's option) |
| Reporting impact | Watchlisted, enhanced monitoring | Default notice, potential workout |
| Typical DSCR trigger | 1.15x-1.25x | 1.00x-1.15x |
| Typical LTV trigger | 75-85% | 85-95% |
| Duration | Until cure (consecutive test periods) | Until resolved |

### Cash Sweep Mechanics
```
Monthly Cash Flow Waterfall (during cash sweep):
1. Operating expenses (property level)
2. Debt service (P&I)
3. Required reserves and escrows
4. Tax and insurance escrows
5. ALL remaining cash -> Lender-controlled sweep account

Sweep account use:
  - Held as additional collateral
  - May be applied to outstanding loan balance
  - Released when cure conditions met (typically 2 consecutive quarters above threshold)
```

---

## Early Warning Methodology

### Leading Indicators (6-12 months before covenant breach)

| Indicator | Warning Signal | Data Source | Action |
|-----------|---------------|-------------|--------|
| Lease rollover schedule | > 20% of NRA expiring within 12 months | Rent roll | Accelerate renewal discussions |
| Tenant credit deterioration | Credit rating downgrade, late payments | D&B, credit agencies, AR aging | Engage tenant, assess replacement |
| Market vacancy increase | Submarket vacancy rising > 100 bps | CoStar, brokerage reports | Adjust leasing strategy |
| Rental rate compression | Market rents declining > 5% YoY | CoStar, lease comps | Model impact on renewals |
| Operating expense spike | Expense ratio increasing > 200 bps | Monthly financials | Identify drivers, implement controls |
| Interest rate increase | Floating rate loan, rate cap approaching ceiling | Bloomberg, loan docs | Model DSCR at higher rates, evaluate rate cap |
| Cap rate expansion | Market cap rates expanding > 50 bps | RCA, CoStar, broker surveys | Model LTV impact, prepare for revaluation |
| Insurance cost increase | Premium renewal > 20% increase | Broker market update | Budget impact, appeal renewal |
| Tax assessment increase | Reassessment notice > 10% increase | Assessor notice | File appeal immediately |
| Deferred maintenance | Capex backlog growing, emergency repairs increasing | Engineering reports, WO data | Evaluate impact on operating costs |

### Monitoring Dashboard (Monthly)

| Metric | Current | Prior Month | Prior Quarter | Covenant Threshold | Cushion | Status |
|--------|---------|-------------|--------------|-------------------|---------|--------|
| DSCR (lender-calc) | X.XXx | X.XXx | X.XXx | X.XXx | XX% | Green/Yellow/Red |
| LTV (income-implied) | XX.X% | XX.X% | XX.X% | XX.X% | XX% | Green/Yellow/Red |
| Physical occupancy | XX.X% | XX.X% | XX.X% | XX.X% | XX% | Green/Yellow/Red |
| Economic occupancy | XX.X% | XX.X% | XX.X% | N/A | N/A | Info |
| Debt yield | XX.X% | XX.X% | XX.X% | XX.X% | XX% | Green/Yellow/Red |
| NOI (T12) | $X,XXX | $X,XXX | $X,XXX | N/A | N/A | Trend |
| Cash reserves | $X,XXX | $X,XXX | $X,XXX | $X,XXX | XX% | Green/Yellow/Red |

### Status Thresholds

| Status | Definition | Action Required |
|--------|-----------|----------------|
| Green | > 15% cushion above covenant threshold | Normal monitoring |
| Yellow | 5-15% cushion above covenant threshold | Enhanced monitoring, prepare remediation plan |
| Red | < 5% cushion or breach imminent | Activate remediation, notify senior management |
| Default | Below covenant threshold | Execute remediation, engage lender (if required) |

### Stress Testing (Quarterly)

Run scenarios on each property and portfolio-wide:

| Scenario | Assumption | Test |
|----------|-----------|------|
| Vacancy shock | Largest tenant vacates | DSCR, occupancy, debt yield |
| Rent decline | 10% market rent decrease | DSCR, LTV (income-implied) |
| Rate shock (floating) | +200 bps interest rate increase | DSCR |
| Cap rate expansion | +100 bps cap rate increase | LTV |
| Combined stress | Vacancy + rate + cap rate | All covenants simultaneously |
| Expense shock | 15% operating expense increase | DSCR, debt yield |

### Reporting Cadence

| Report | Frequency | Audience | Content |
|--------|-----------|---------|---------|
| Covenant compliance certificate | Quarterly (per loan docs) | Lender/servicer | Certified calculations, financial statements |
| Internal covenant dashboard | Monthly | Asset management, finance | All metrics, trend, cushion, status |
| Stress test results | Quarterly | Investment committee | Scenario analysis, at-risk assets |
| Lease rollover impact | Quarterly | Asset management | Forward-looking covenant projections |
| Annual operating budget | Annually | Lender (if required), internal | Forward NOI projections, covenant compliance |
