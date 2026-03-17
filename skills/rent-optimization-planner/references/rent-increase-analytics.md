# Rent Increase Analytics Reference

## Overview

Frameworks for loss-to-lease analysis, renewal probability modeling, effective
rent NPV comparison, and rent optimization impact on property valuation.

---

## 1. Loss-to-Lease Waterfall

Loss-to-lease is the difference between in-place rent and current market rent,
aggregated across all tenants. It represents embedded upside (or downside) in
the rent roll.

### Calculation Framework

```
For each tenant i:

  loss_to_lease_i = max(0, market_rent_i - in_place_rent_i) * SF_i * remaining_months_i / 12

  gain_to_lease_i = max(0, in_place_rent_i - market_rent_i) * SF_i * remaining_months_i / 12

Property aggregate:
  gross_loss_to_lease = sum(loss_to_lease_i)
  gross_gain_to_lease = sum(gain_to_lease_i)
  net_loss_to_lease   = gross_loss_to_lease - gross_gain_to_lease
```

### Waterfall Decomposition

Break down the portfolio into buckets to identify where the opportunity sits:

```
STEP 1: Gross Potential Rent at Market
  = sum(market_rent_i * SF_i) for all occupied spaces
  = Total revenue if every tenant were at market today

STEP 2: Less -- Above-Market Leases (Gain-to-Lease)
  = sum((in_place_rent_i - market_rent_i) * SF_i) where in_place > market
  These tenants are already above market; risk of non-renewal

STEP 3: Less -- Below-Market Leases (Loss-to-Lease)
  = sum((market_rent_i - in_place_rent_i) * SF_i) where market > in_place
  These represent the capture opportunity

STEP 4: Less -- Contractual Escalation Lag
  = Revenue lost between now and next escalation date
  For CPI leases: estimated CPI increase not yet applied
  For fixed bump leases: delta between current step and next step

STEP 5: Less -- Vacancy & Credit Loss
  = Stabilized vacancy assumption * GPR
  + Expected credit loss (bad debt)

STEP 6: = Effective Gross Income (Proforma)

STEP 7: Mark-to-Market Capture Timeline
  For each below-market lease:
    capture_date = min(lease_expiration, next_renewal_option)
    probability_of_capture = P(renewal at market) + P(new tenant at market)
    annual_capture = (market - in_place) * SF * probability_of_capture
```

### Worked Example: 10-Tenant Office Building

```
Tenant | SF    | In-Place | Market | Delta  | Expiry  | Annual L2L
       |       | $/SF/yr  | $/SF/yr| $/SF   |         |
-------|-------|----------|--------|--------|---------|----------
  A    | 8,000 |   42.00  |  48.00 | -6.00  | 2027-03 | ($48,000)
  B    | 5,500 |   50.00  |  48.00 | +2.00  | 2028-06 |  $11,000
  C    | 3,200 |   38.00  |  48.00 |-10.00  | 2026-09 | ($32,000)
  D    | 6,800 |   45.00  |  48.00 | -3.00  | 2029-12 | ($20,400)
  E    | 4,100 |   47.00  |  48.00 | -1.00  | 2026-06 |  ($4,100)
  F    | 7,500 |   44.00  |  48.00 | -4.00  | 2027-09 | ($30,000)
  G    | 2,800 |   52.00  |  48.00 | +4.00  | 2030-03 |  $11,200
  H    | 5,000 |   46.00  |  48.00 | -2.00  | 2028-01 | ($10,000)
  I    | 3,500 |   40.00  |  48.00 | -8.00  | 2026-12 | ($28,000)
  J    | 4,600 |   43.00  |  48.00 | -5.00  | 2027-06 | ($23,000)

Gross Loss-to-Lease:  ($195,500)/year
Gross Gain-to-Lease:    $22,200/year
Net Loss-to-Lease:    ($173,300)/year
Net L2L as % of GPR:   7.1%
```

### Mark-to-Market Capture Schedule

```
Year | SF Rolling | Capture   | Cumulative | Remaining
     | to Market  | Revenue   | Captured   | L2L
-----|------------|-----------|------------|----------
2026 |   10,800   |  $64,100  |   $64,100  | $109,200
2027 |   20,100   |  $101,000 |  $165,100  |   $8,200
2028 |   10,500   |  $22,000  |  $187,100  |  ($13,800)
2029 |    6,800   |  $20,400  |  $207,500  |  ($34,200)
```

---

## 2. Renewal Probability Modeling

### Base Renewal Rates by Property Type

```yaml
base_renewal_rates:
  multifamily:
    market_average: 0.55
    class_a: 0.50  # More mobile tenant base
    class_b: 0.58
    class_c: 0.62  # Fewer alternatives
  office:
    market_average: 0.65
    cbd_class_a: 0.60
    suburban: 0.70
    single_tenant: 0.75
  retail:
    market_average: 0.70
    anchor: 0.80
    inline_national: 0.72
    inline_local: 0.60
    restaurant: 0.55
  industrial:
    market_average: 0.75
    distribution: 0.78
    manufacturing: 0.80  # High switching costs
    flex: 0.65
```

### Adjustment Factors

The base rate is modified by lease-specific and market factors:

```
P(renewal) = base_rate * product(adjustment_factors)

Adjustment factors:
```

| Factor                          | Multiplier Range | Direction |
|---------------------------------|------------------|-----------|
| Rent vs market (each 5% above) | 0.90 per 5%     | Negative  |
| Rent vs market (each 5% below) | 1.05 per 5%     | Positive  |
| Remaining TI amortization       | 1.0 - 1.15      | Positive  |
| Tenant invested own capital     | 1.10 - 1.25     | Positive  |
| Recent tenant expansion         | 1.15             | Positive  |
| Tenant headcount declining      | 0.75 - 0.90     | Negative  |
| Tenant credit downgrade         | 0.80             | Negative  |
| Submarket vacancy > 15%         | 0.85             | Negative  |
| Submarket vacancy < 5%          | 1.10             | Positive  |
| Lease includes renewal option   | 1.10             | Positive  |
| Competitor new construction     | 0.85 - 0.95     | Negative  |
| Building amenity upgrade        | 1.05 - 1.10     | Positive  |
| Tenant satisfaction survey 4+   | 1.10             | Positive  |

### Renewal Probability Model (Logistic Regression Form)

For more quantitative applications:

```
logit(P(renewal)) = B0 + B1*(rent_spread) + B2*(years_in_place)
                    + B3*(ti_remaining) + B4*(submarket_vacancy)
                    + B5*(tenant_growth) + B6*(satisfaction_score)

Typical coefficients (office):
  B0 = 0.65
  B1 = -0.08 per 1% rent spread above market
  B2 = 0.04 per year in occupancy
  B3 = 0.03 per $10K unamortized TI
  B4 = -0.05 per 1% submarket vacancy above 10%
  B5 = 0.10 if tenant grew headcount last 12 months
  B6 = 0.08 per satisfaction point above 3.0
```

---

## 3. Effective Rent NPV Comparison

When evaluating a rent increase at renewal, compare the NPV of three outcomes:
renewal at proposed rent, renewal at lower negotiated rent, and vacancy/re-lease.

### Framework

```
Scenario 1: Renewal at Asking Rent (R_ask)

  P(accept) = f(rent spread, factors above)
  NPV_1 = P(accept) * sum(t=1..T) [R_ask / (1+r)^t]
         + (1-P(accept)) * NPV_vacancy_re_lease

Scenario 2: Renewal at Negotiated Rent (R_neg)

  P(accept) = higher than Scenario 1 (lower spread)
  NPV_2 = P(accept) * sum(t=1..T) [R_neg / (1+r)^t]
         + (1-P(accept)) * NPV_vacancy_re_lease

Scenario 3: Vacancy + Re-Lease at Market

  NPV_3 = -downtime_cost - TI - LC - make_ready
         + sum(t=vacancy+1..T) [R_market / (1+r)^t]
```

### Rent Increase Decision Matrix

```
                 | Market Rent > In-Place     | Market Rent <= In-Place
                 | (Loss-to-Lease exists)     | (Gain-to-Lease exists)
-----------------|----------------------------|---------------------------
Strong Market    | Push to market or 5% above | Hold at in-place, extend
(vacancy < 5%)  | High P(re-lease if vacate) | term to lock in above-
                 | Moderate risk, high reward  | market rent long-term
-----------------|----------------------------|---------------------------
Normal Market    | Push to market, offer 3-5  | Offer flat renewal or
(vacancy 5-10%)  | year term for stability    | slight reduction to
                 | Balance capture vs risk     | retain and avoid vacancy
-----------------|----------------------------|---------------------------
Weak Market      | Offer below-market renewal | Reduce to market, extend
(vacancy > 10%)  | Retention > rent capture   | term. Above-market tenant
                 | Concede on face rent, get  | is high flight risk.
                 | term extension             | Lock in any positive spread
```

### Worked Example: Renewal Analysis

```yaml
tenant:
  name: "Acme Professional Services"
  sf: 6000
  current_rent_psf: 44.00
  market_rent_psf: 50.00
  remaining_lease: 8 months
  in_place_since: 2019
  satisfaction: high
  credit: investment_grade

assumptions:
  discount_rate: 0.07
  renewal_term: 5 years (60 months)
  vacancy_if_departure: 6 months
  re_lease_ti: 45.00 psf ($270,000)
  re_lease_lc: 4% aggregate ($72,000)
  make_ready: 15.00 psf ($90,000)
  free_rent_new_tenant: 3 months

scenarios:
  push_to_market_50:
    asking_rent: 50.00
    annual_revenue: 300000
    p_accept: 0.55  # Significant jump from 44
    npv_if_accept: 1232760  # 5yr discounted
    npv_if_vacate: 683200  # Net of vacancy + costs + new lease
    expected_npv: 985182  # 0.55 * 1,232,760 + 0.45 * 683,200

  compromise_at_48:
    asking_rent: 48.00
    annual_revenue: 288000
    p_accept: 0.78
    npv_if_accept: 1183450
    npv_if_vacate: 683200
    expected_npv: 1073384  # 0.78 * 1,183,450 + 0.22 * 683,200

  moderate_at_46:
    asking_rent: 46.00
    annual_revenue: 276000
    p_accept: 0.92
    npv_if_accept: 1134140
    npv_if_vacate: 683200
    expected_npv: 1098065  # 0.92 * 1,134,140 + 0.08 * 683,200

  hold_at_44:
    asking_rent: 44.00
    annual_revenue: 264000
    p_accept: 0.98
    npv_if_accept: 1084830
    npv_if_vacate: 683200
    expected_npv: 1076797

optimal_strategy:
  recommended: "Compromise at $48/SF"
  reasoning: |
    $48/SF maximizes expected NPV at $1,073,384 while maintaining a
    78% renewal probability. Pushing to $50 drops expected NPV due to
    the 45% vacancy risk. Holding at $44 leaves $24K/year on the table
    unnecessarily -- the tenant has high satisfaction and investment-grade
    credit, supporting a moderate increase.
  negotiation_anchor: "$50/SF (market) with willingness to settle at $48"
```

---

## 4. Valuation Impact of Rent Optimization

Rent increases affect property value through NOI and cap rate compression.

### Direct Capitalization Impact

```
Value = NOI / Cap Rate

Each $1 of incremental rent creates:
  Value impact = $1 / cap_rate

At various cap rates:
  Cap Rate | Value per $1 of Rent
  ---------|---------------------
   4.0%    | $25.00
   4.5%    | $22.22
   5.0%    | $20.00
   5.5%    | $18.18
   6.0%    | $16.67
   6.5%    | $15.38
   7.0%    | $14.29
   8.0%    | $12.50
```

### Portfolio-Level Optimization Impact

For the 10-tenant office example above:

```
Current in-place NOI: $1,850,000
Net loss-to-lease: $173,300/year

If 100% captured over 3 years:
  Year 3 NOI: $2,023,300
  NOI increase: 9.4%

  At 6.0% cap:
    Current value: $30,833,333
    Optimized value: $33,721,667
    Value creation: $2,888,333 (9.4%)

  At 5.5% cap (compression from higher rents):
    Optimized value: $36,787,273
    Value creation: $5,953,939 (19.3%)
```

### Rent Optimization Value Creation Formula

```
V_created = (delta_NOI / exit_cap) - concession_cost - vacancy_cost - TI_LC_cost

Where:
  delta_NOI = incremental annual rent captured at stabilization
  exit_cap = capitalization rate at disposition
  concession_cost = PV of any concessions given to achieve rent increase
  vacancy_cost = PV of lost rent during any vacancy caused by non-renewals
  TI_LC_cost = PV of tenant improvements and leasing commissions for new tenants
```

---

## 5. Rent Optimization Strategy Sequencing

### Priority Matrix

```
                 | Large Loss-to-Lease      | Small Loss-to-Lease
                 | (> 10% below market)      | (< 10% below market)
-----------------|--------------------------|-------------------------
Near-Term Expiry | PRIORITY 1               | PRIORITY 2
(< 12 months)    | Push aggressively to     | Moderate increase to
                 | market. High impact,     | market. Lower risk.
                 | immediate capture.        |
-----------------|--------------------------|-------------------------
Mid-Term Expiry  | PRIORITY 3               | PRIORITY 4
(12-36 months)   | Begin early renewal      | Monitor. Address at
                 | discussions. Offer term  | natural renewal. No
                 | extension for rent bump. | early action needed.
-----------------|--------------------------|-------------------------
Long-Term Expiry | PRIORITY 5               | NO ACTION
(> 36 months)    | Early renewal only if    | Lease is performing
                 | tenant willing. Focus on | as designed. Wait.
                 | escalation clause review.|
```

### Annual Rent Optimization Calendar

```yaml
quarterly_cadence:
  Q1:
    - Pull expiration report for next 18 months
    - Calculate loss-to-lease by tenant
    - Update market rent comps (broker opinions of value)
    - Identify Priority 1 and 2 tenants
    - Send renewal proposals to all tenants expiring in Q3-Q4

  Q2:
    - Negotiate renewals for Q3-Q4 expirations
    - Begin early renewal outreach for Priority 3 tenants
    - Review Q1 lease execution metrics (achieved vs asking)
    - Adjust market rent assumptions if needed

  Q3:
    - Execute Q3-Q4 renewal leases
    - Send proposals for Q1-Q2 next year expirations
    - Mid-year loss-to-lease recalculation
    - Begin marketing any expected vacancies

  Q4:
    - Finalize next-year budget with updated rent assumptions
    - Close remaining open negotiations
    - Year-end loss-to-lease and capture reporting
    - Set next-year target rents by unit/suite
```

---

## 6. Effective Rent Calculation Methods

### Gross Effective Rent

```
Effective Rent = (Total Lease Revenue - Total Concessions) / Lease Term

Where total concessions include:
  - Free rent months (face value)
  - Reduced rent periods
  - TI above standard (if treated as rent concession)
  - Moving allowances
  - Parking credits
  - Any other inducements
```

### Net Effective Rent (NPV Method)

More accurate -- accounts for time value of concessions:

```
NER = r * sum(t=1..T) [Rent_t / (1+r)^t] / sum(t=1..T) [1 / (1+r)^t]

This is the level annuity payment equivalent to the actual rent stream.
```

### Concession-Adjusted Rent for Comparison

When comparing two tenant proposals:

```
Proposal A: $50/SF, 5-year, 3 months free, $40/SF TI
Proposal B: $48/SF, 7-year, 1 month free, $30/SF TI

NER_A:
  Total rent: ($50 * 57/12) + ($0 * 3/12) = $237.50/SF over 5 years
  Less TI: $40/SF
  Net to landlord: $197.50/SF
  Annual NER: $197.50 / 5 = $39.50/SF

NER_B:
  Total rent: ($48 * 83/12) + ($0 * 1/12) = $332.00/SF over 7 years
  Less TI: $30/SF
  Net to landlord: $302.00/SF
  Annual NER: $302.00 / 7 = $43.14/SF

Proposal B is superior despite lower face rent.
```
