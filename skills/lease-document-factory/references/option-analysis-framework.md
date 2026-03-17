# Option Analysis Framework

## Purpose

Quantitative framework for analyzing expansion, contraction, renewal, ROFR, and ROFO options in commercial leases. Provides valuation methodology, exercise probability estimation, and landlord decision support.

## Expansion Option Analysis

### Economic Components

An expansion option gives the tenant the right (but not obligation) to lease additional contiguous space at a predetermined price during a specified window.

**Option value to tenant** = (Market Rent - Strike Price) x Expansion SF x Remaining Term x Probability of Exercise, discounted to present

**Option cost to landlord** = Lost flexibility value + Below-market rent risk + Opportunity cost of holding space

### Valuation Methodology

**Step 1: Determine in-the-money status**

| Status | Condition | Tenant Behavior |
|--------|-----------|----------------|
| Deep in-the-money | Strike > 15% below market | Very likely to exercise |
| In-the-money | Strike 5-15% below market | Likely to exercise if growth supports |
| At-the-money | Strike within 5% of market | Exercise depends on operational need |
| Out-of-the-money | Strike above market | Unlikely to exercise |

**Step 2: Calculate option value**

```
Annual Savings = (Market Rent - Strike Price) x Expansion SF
NPV of Savings = Sum of Annual Savings / (1 + discount rate)^n for each year
Option Value = NPV of Savings x Exercise Probability
```

**Step 3: Calculate landlord flexibility cost**

- Holding cost: If space sits vacant while reserved, landlord loses rental income
- Opportunity cost: If a prospect wants the expansion space, landlord cannot lease it (or must negotiate a kick-out clause)
- Marketing constraint: Expansion space may not appear on marketing materials, reducing broker interest

### Worked Example: 50K SF Tenant with Expansion Option

**Given**:
- Tenant: Tech Corp, 50,000 SF, office
- Current rent: $28/SF (signed 3 years ago)
- Expansion option: 15,000 SF contiguous on same floor
- Strike price: $28/SF (fixed at original lease execution)
- Current market rent: $32/SF
- Exercise window: Months 48-54 of lease (9 months away)
- Notice period: 12 months prior to exercise window
- Remaining lease term after exercise window: 4 years

**Analysis**:

In-the-money status: $28 strike vs $32 market = $4/SF below market = 12.5% discount = In-the-money

Annual savings to tenant:
```
$4/SF x 15,000 SF = $60,000/year
Over 4 remaining years, NPV at 7%: $203,000
```

Exercise probability assessment:
- In-the-money: +30% base probability
- Tenant headcount growing 8% annually: +25%
- No comparable contiguous space in submarket: +15%
- Tenant has remote work policy (partially offsetting): -10%
- **Estimated probability: 60%**

Risk-adjusted option value: $203,000 x 60% = $122,000

Landlord impact:
- If tenant exercises: 15,000 SF at $28/SF vs $32/SF = $60K/year below market for 4 years
- If tenant does NOT exercise: Space is available but was not marketed, 3-6 months of lost marketing time
- If prospect wants the space NOW: Must include kick-out clause in prospect's lease (tenant has expansion right)

**Recommendation**: The option is contractual; landlord cannot refuse. However:
1. Monitor tenant's growth closely. If tenant is shrinking, option may lapse.
2. If a strong prospect emerges for the expansion space, approach tenant to negotiate early exercise or option buyout.
3. Option buyout value: $122K risk-adjusted value. Offer tenant $75-100K cash to relinquish option. This frees the space for a market-rate deal.

## Contraction Option Analysis

### Pricing Methodology

A contraction option allows the tenant to return (give back) a portion of its premises, usually upon payment of a fee.

**Contraction fee must cover**:

| Component | Formula | Typical Range |
|-----------|---------|---------------|
| Unamortized TI | TI/SF x Give-Back SF x (Remaining Months / Original Term Months) | $5-30/SF |
| Unamortized Commission | Commission $ x (Remaining Months / Original Term Months) | $1-5/SF |
| Estimated Vacancy Loss | Monthly Rent x Give-Back SF / Total SF x Expected Vacancy Months | 6-12 months |
| Re-leasing Commission | Market Commission Rate x New Lease Term x Market Rent x Give-Back SF | $3-8/SF |
| New TI for Give-Back | Market TI Allowance/SF x Give-Back SF | $10-50/SF |
| **Total Fee** | **Sum** | **$25-95/SF or 6-18 months rent** |

### Worked Example

**Given**:
- Tenant: Law Firm, 80,000 SF, CBD office
- Lease expiration: 6 years remaining
- Current rent: $55/SF
- Contraction option: Right to give back 20,000 SF at month 36 of remaining term
- TI amortization remaining: $15/SF on the 20,000 SF
- Commission amortization remaining: $3/SF

**Contraction fee calculation**:

| Component | Amount |
|-----------|--------|
| Unamortized TI: $15/SF x 20,000 SF x (36/72) | $150,000 |
| Unamortized Commission: $3/SF x 20,000 SF x (36/72) | $30,000 |
| Vacancy: $55/SF x 20,000 SF / 12 x 9 months | $825,000 |
| Re-leasing Commission: 5% yr1, 2.5% yrs 2-3 x $55/SF x 20,000 SF | $165,000 |
| New TI: $40/SF x 20,000 SF | $800,000 |
| **Total** | **$1,970,000** |
| **Per SF of give-back** | **$98.50/SF** |
| **Months of rent equivalent** | **~11 months** |

**Landlord NPV comparison**:

Scenario A (tenant retains full space): NPV of 6 years of rent on 80,000 SF at $55/SF = $22.4M

Scenario B (tenant contracts after 3 years):
- 3 years of rent on 80,000 SF + contraction fee + 3 years of rent on 60,000 SF + re-leasing 20,000 SF
- NPV = $20.8M

**Shortfall**: $1.6M. If contraction fee is $1.97M, landlord is made whole plus $370K surplus. Acceptable.

## Renewal Option Analysis

### Fair Market Rent Determination Methods

Renewal options typically specify the renewal rent as "fair market rent" (FMR). Three standard determination methods:

#### Method 1: Three Appraisers

```
Process:
1. Landlord and Tenant each appoint one MAI appraiser within 15 days
2. Two appointed appraisers select a third appraiser within 15 days
3. All three appraisers determine FMR independently within 30 days
4. FMR = average of the two closest appraisals (discard outlier)
   OR FMR = average of all three
5. Each party pays its own appraiser; third appraiser cost shared
```

**Pros**: Objective, established process
**Cons**: Expensive ($15-30K total), time-consuming (60-90 days), still subject to gaming

#### Method 2: Baseball Arbitration

```
Process:
1. Landlord and Tenant each submit sealed FMR determination
2. Single arbitrator selects one or the other (no splitting)
3. Parties are incentivized to be reasonable (extreme positions lose)
```

**Pros**: Fast (30 days), forces reasonableness
**Cons**: Binary outcome, can feel arbitrary

#### Method 3: CPI-Based

```
Process:
1. Base rent is adjusted by CPI increase from lease commencement
2. Formula: Renewal Rent = Base Rent x (CPI at renewal / CPI at commencement)
3. Floor and ceiling may apply (e.g., 2% floor, 4% ceiling per annum)
```

**Pros**: Formulaic, no dispute possible
**Cons**: May diverge significantly from actual market rent over long periods

### Landlord Strategy by Method

| Method | Landlord Advantage | Tenant Advantage | When to Propose |
|--------|-------------------|------------------|-----------------|
| 3 Appraisers | Most objective | Most objective | Standard; high-value leases |
| Baseball | Discourages tenant lowballing | Discourages landlord highballing | When quick resolution needed |
| CPI-Based | Protects if market appreciating slower than CPI | Protects if market appreciating faster than CPI | Stable, low-growth markets |

### What Is Included in FMR

The definition of FMR must specify whether it includes or excludes:

| Component | Include? | Impact |
|-----------|----------|--------|
| TI allowance | Usually excluded for renewals (minimal TI) | Lower FMR if included |
| Free rent / concessions | Usually excluded | Lower FMR if included |
| Brokerage commission | Excluded (renewal commissions lower) | Minor impact |
| Lease term | Specify the term to be valued | Longer term = lower FMR |
| Comparable buildings | Define comp set (class, age, location) | Narrow vs. broad comp set |

## ROFR vs ROFO Analysis

### Right of First Refusal (ROFR)

Tenant has the right to match any bona fide third-party offer on designated space.

**Mechanics**:
1. Landlord receives offer from third-party prospect
2. Landlord presents offer to ROFR holder with all material terms
3. ROFR holder has [10-15] business days to match
4. If matched: ROFR holder leases the space on matched terms
5. If declined: Landlord proceeds with third party

**Landlord risk**: Chills third-party interest. Prospects may not invest time negotiating if they know tenant can swoop in. Creates negotiation disadvantage for landlord (prospect knows about ROFR).

**Economic model**:
```
ROFR Cost to Landlord = Third-Party Lease NPV x Probability of ROFR Exercise
  + Marketing Inefficiency (fewer prospects) x Estimated Revenue Loss
  - Avoided Vacancy (if ROFR holder takes space quickly)
```

### Right of First Offer (ROFO)

Landlord must offer designated space to ROFO holder before marketing to third parties.

**Mechanics**:
1. When space becomes available, Landlord offers it to ROFO holder at Landlord's asking price
2. ROFO holder has [10-15] business days to accept
3. If accepted: ROFO holder leases the space at offered terms
4. If declined: Landlord markets the space freely to third parties (no further obligation to ROFO holder for this instance)

**Landlord preference**: ROFO is strongly preferred over ROFR because:
1. Landlord sets the initial terms (not matching a third party)
2. Does not chill third-party interest (they do not know about ROFO)
3. Landlord can market freely after ROFO is declined
4. Faster resolution (no waiting for third-party offers)

### Comparison

| Feature | ROFR | ROFO |
|---------|------|------|
| Who sets terms | Third party (tenant matches) | Landlord (offers first) |
| Chilling effect | High (prospects deterred) | Low (prospects unaware) |
| Landlord control | Low | High |
| Tenant certainty | High (can match any deal) | Moderate (Landlord's offer may be aggressive) |
| Market standard | Disfavored by landlords | Preferred by landlords |
| Negotiation leverage | Tenant has information advantage | Landlord has pricing advantage |

### Decision Framework

Grant expansion rights in this priority order:
1. **Fixed-price expansion option**: Most expensive for landlord but most certain for both parties
2. **ROFO**: Moderate cost; landlord controls pricing
3. **ROFR**: Highest cost to landlord; offer only to anchor tenants or credit tenants with significant leverage
4. **None**: Best for landlord flexibility; acceptable when tenant has no leverage

## Option Expiration Calendar Management

### Critical Date Tracking

For every option in the portfolio, maintain:

| Field | Description |
|-------|-------------|
| Tenant | Option holder name |
| Option type | Expansion, contraction, renewal, ROFR, ROFO, termination |
| Exercise window open | First date tenant can exercise |
| Exercise window close | Last date (after which option lapses) |
| Notice deadline | Date by which written notice must be received |
| Landlord response deadline | Date by which landlord must respond (ROFR/ROFO) |
| Financial impact | Estimated NPV impact if exercised |
| Probability | Estimated exercise probability |
| Action required | Landlord's preparation needed before window opens |

### Advance Notice Workflow

| Timeline | Action |
|----------|--------|
| 18 months before | Review option economics, update market rent assumptions |
| 12 months before | Internal strategy meeting: want exercise or lapse? |
| 9 months before | If want exercise: approach tenant proactively |
| 9 months before | If want lapse: prepare marketing plan for space |
| 6 months before | If tenant hasn't signaled: reach out to gauge intent |
| Notice deadline | Monitor for receipt of notice; if none, confirm lapse |
| After lapse | Begin marketing space immediately |
