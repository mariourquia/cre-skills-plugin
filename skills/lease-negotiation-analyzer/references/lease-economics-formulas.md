# Lease Economics Formulas Reference

## Overview

Core formulas for TI amortization, effective rent calculation, concession NPV,
credit enhancement sizing, and landlord economics. Every formula includes the
mathematical definition, a worked example, and common pitfalls.

---

## 1. Tenant Improvement (TI) Amortization

### Basic TI Amortization

TI is a landlord capital outlay amortized over the lease term. The annual cost
of TI, expressed per SF, is added to the landlord's true occupancy cost.

```
Annual TI Cost = TI_per_SF * [r * (1+r)^n] / [(1+r)^n - 1]

Where:
  TI_per_SF = total TI allowance per square foot
  r = landlord's cost of capital (monthly or annual, match period)
  n = lease term in periods (months or years)
```

### Worked Example

```
TI allowance: $65/SF
Lease term: 10 years
Landlord cost of capital: 7.5% annual

Annual TI amortization per SF:
  = 65 * [0.075 * (1.075)^10] / [(1.075)^10 - 1]
  = 65 * [0.075 * 2.06103] / [2.06103 - 1]
  = 65 * 0.15458 / 1.06103
  = 65 * 0.14569
  = $9.47/SF/year

On 10,000 SF space:
  Annual TI amortization = $94,700
  Total TI cost = $650,000
  Total payments over 10 years = $947,000
  Interest cost = $297,000
```

### TI Amortization Table (Common Scenarios)

| TI/SF | Term (yrs) | Rate 6% | Rate 7% | Rate 8% | Rate 9% |
|-------|------------|---------|---------|---------|---------|
| $25   | 5          | $5.93   | $6.10   | $6.26   | $6.43   |
| $25   | 7          | $4.50   | $4.65   | $4.81   | $4.97   |
| $25   | 10         | $3.40   | $3.56   | $3.73   | $3.90   |
| $45   | 5          | $10.68  | $10.97  | $11.27  | $11.57  |
| $45   | 7          | $8.10   | $8.37   | $8.65   | $8.94   |
| $45   | 10         | $6.11   | $6.41   | $6.71   | $7.02   |
| $65   | 5          | $15.43  | $15.85  | $16.28  | $16.72  |
| $65   | 7          | $11.71  | $12.10  | $12.49  | $12.92  |
| $65   | 10         | $8.83   | $9.26   | $9.69   | $10.14  |
| $85   | 7          | $15.31  | $15.82  | $16.34  | $16.89  |
| $85   | 10         | $11.55  | $12.10  | $12.67  | $13.26  |
| $85   | 15         | $8.75   | $9.33   | $9.94   | $10.56  |

### Pitfalls

- Always amortize at the landlord's cost of capital, not the tenant's
- If TI is partially funded by a construction loan, use blended cost
- Unamortized TI at lease termination is a loss -- factor into early termination fees
- Tax treatment: TI owned by landlord is depreciated (39 years commercial); TI owned
  by tenant is tenant's asset (no landlord depreciation)

---

## 2. Effective Rent Calculation

### Simple Effective Rent

```
Simple Effective Rent = (Total Lease Payments - Total Concessions) / Lease Term

Example:
  Face rent: $50/SF/year
  Term: 5 years (60 months)
  Free rent: 3 months
  SF: 5,000

  Total payments: ($50 * 5,000 * 57/12) = $1,187,500
  Simple effective rent: $1,187,500 / 5 / 5,000 = $47.50/SF/year
```

### NPV-Adjusted Effective Rent (Net Effective Rent)

Accounts for time value -- free rent at the front is worth more than at the back.

```
NER = [sum(t=1..T) CF_t / (1+r)^t] / [sum(t=1..T) 1/(1+r)^t]

Where:
  CF_t = rent payment in period t (0 during free rent)
  r = discount rate per period
  T = total lease periods
```

### Worked Example: NER

```
Face rent: $50/SF/year ($4.167/SF/month)
Term: 60 months
Free rent: Months 1-3
Discount rate: 7% annual (0.5654% monthly)
SF: 5,000

Step 1: PV of rent stream
  Months 1-3: $0 (free rent)
  Months 4-60: $4.167/SF/month

  PV = sum(t=4..60) [4.167 / (1.005654)^t]
     = 4.167 * [sum(t=1..60) 1/(1.005654)^t - sum(t=1..3) 1/(1.005654)^t]
     = 4.167 * [50.502 - 2.966]
     = 4.167 * 47.536
     = $198.08/SF

Step 2: PV of annuity factor (denominator)
  sum(t=1..60) [1/(1.005654)^t] = 50.502

Step 3: NER (monthly)
  = $198.08 / 50.502
  = $3.923/SF/month

Step 4: NER (annual)
  = $3.923 * 12
  = $47.08/SF/year

Note: NER ($47.08) < Simple effective ($47.50) because free rent at
the front is worth more in PV terms.
```

### Landlord Net Effective Rent (includes TI and LC)

```
Landlord NER = [PV(rent stream) - TI - LC] / PV(annuity factor)

Example:
  PV(rent stream): $198.08/SF (from above)
  TI: $45/SF (paid at month 0)
  LC: $12/SF (paid at month 1)
  LC_PV: $12 / 1.005654 = $11.93/SF

  Landlord NER = ($198.08 - $45.00 - $11.93) / 50.502
               = $141.15 / 50.502
               = $2.795/SF/month
               = $33.54/SF/year

  Face rent: $50.00/SF
  Tenant effective: $47.08/SF
  Landlord effective: $33.54/SF
  Landlord-tenant spread: $13.54/SF (TI + LC drag)
```

---

## 3. Concession NPV Comparison

### Framework

When comparing two proposals with different concession structures, convert
everything to NPV for apples-to-apples comparison.

```
Landlord NPV = PV(rent) + PV(reimbursements) - PV(TI) - PV(LC) - PV(free rent)

The proposal with the highest Landlord NPV wins.
```

### Multi-Proposal Comparison Template

```
                    | Proposal A     | Proposal B     | Proposal C
--------------------|----------------|----------------|----------------
Tenant              | Acme Corp      | Beta LLC       | Gamma Inc
Credit              | Investment Grd | Mid-Market     | Startup
SF                  | 8,000          | 8,000          | 8,000
Term                | 7 years        | 10 years       | 5 years
Face Rent ($/SF)    | $52.00         | $48.00         | $56.00
Escalation          | 3% annual      | 2.5% annual    | Flat
Free Rent (months)  | 4              | 6              | 2
TI ($/SF)           | $55            | $40            | $75
LC ($/SF)           | $14            | $10            | $18
--------------------|----------------|----------------|----------------
PV of Rent          | $2,619,840     | $3,112,560     | $1,958,400
PV of Free Rent     | ($138,667)     | ($192,000)     | ($74,667)
PV of TI            | ($440,000)     | ($320,000)     | ($600,000)
PV of LC            | ($112,000)     | ($80,000)      | ($144,000)
--------------------|----------------|----------------|----------------
Landlord NPV        | $1,929,173     | $2,520,560     | $1,139,733
NPV per SF/Year     | $34.45         | $31.51         | $28.49
Annual NER (L'lord) | $34.45         | $31.51         | $28.49
--------------------|----------------|----------------|----------------
Ranking             | 1st            | 2nd            | 3rd
```

Note: Proposal A wins on annual NER despite lower total NPV because of shorter
term. Proposal B wins on absolute NPV (longer cash flow stream). Decision
depends on landlord's hold period and capital recycling strategy.

---

## 4. Credit Enhancement Sizing

### Letter of Credit (LOC)

```
LOC Sizing Formula:
  LOC_amount = max(
    months_coverage * monthly_rent,
    unamortized_TI + estimated_re_leasing_cost,
    landlord_downside_exposure
  )

Typical sizing by credit tier:
  Investment Grade:  0-1 months (or none)
  Mid-Market:        2-3 months
  Small Business:    3-6 months
  Startup/No Credit: 6-12 months
```

### Declining LOC / Burn-Down Structure

```
Year | LOC Amount | Trigger for Reduction
-----|-----------|---------------------
  1  | 6 months  | N/A (full security)
  2  | 5 months  | 12 consecutive on-time payments
  3  | 4 months  | Revenue covenant met ($X/year)
  4  | 3 months  | Revenue covenant + net worth test
  5  | 2 months  | All covenants met
```

### Personal Guarantee Sizing

```
Guarantee Coverage = min(
  remaining_lease_obligation,
  max(
    unamortized_TI + LC,
    12 months of rent + reimbursements,
    estimated_re_leasing_cost
  )
)

Good-guy guarantee (NY market):
  Coverage: rent + additional rent through surrender date
  Trigger: tenant gives 6-month notice, vacates in broom-clean condition
  Exposure: known and limited (unlike full guarantee)
  Standard in: NYC office, increasingly in other gateway markets
```

### Security Deposit Adequacy Test

```
adequacy_ratio = security_deposit / (monthly_rent * risk_months)

Where risk_months varies by use:
  Office: 3-6 months
  Retail: 3-6 months
  Industrial: 2-3 months
  Restaurant: 6-12 months (higher failure rate)

Target adequacy_ratio >= 1.0

If < 1.0: supplement with LOC, guarantee, or prepaid rent
```

---

## 5. Escalation Economics

### Fixed Escalation NPV

```
Rent with X% annual escalation:
  Year_t = Base_Rent * (1 + escalation_rate)^(t-1)

NPV of escalating rent stream:
  NPV = sum(t=1..T) [Base * (1+g)^(t-1) / (1+r)^t]
      = Base * [1 - ((1+g)/(1+r))^T] / (r - g)    (for r != g)

Where:
  g = escalation rate
  r = discount rate
  T = lease term
```

### CPI Escalation Expected Value

```
Expected CPI escalation = E[CPI] with typical range modeling:

  Scenario    | CPI   | Probability | Weighted
  ------------|-------|-------------|--------
  Deflation   | -1.0% |    5%       | -0.05%
  Low         |  1.5% |   20%       |  0.30%
  Normal      |  2.5% |   45%       |  1.13%
  Elevated    |  4.0% |   20%       |  0.80%
  High        |  6.0% |   10%       |  0.60%
  ------------|-------|-------------|--------
  Expected    |       |  100%       |  2.78%

NPV comparison: CPI vs Fixed escalation:
  If expected CPI > fixed rate: CPI lease favors landlord
  If expected CPI < fixed rate: fixed lease favors landlord
  CPI with floor (e.g., min 2%): best of both worlds for landlord
```

### Escalation Comparison Table

Annual NER impact of different escalation structures on a $50/SF base:

| Structure          | Year 5 Rent | Year 10 Rent | 10-Yr NER | Notes          |
|--------------------|-------------|--------------|-----------|----------------|
| Flat               | $50.00      | $50.00       | $50.00    | Worst for LL   |
| 2% fixed annual    | $54.12      | $59.75       | $54.56    |                |
| 3% fixed annual    | $56.28      | $65.24       | $57.00    | Most common    |
| CPI (est 2.5%)     | $55.18      | $62.37       | $55.73    | Variable       |
| CPI floor 2% cap 5%| $55.18     | $62.37       | $55.73    | Bounded CPI    |
| 10% bump every 5yr | $50.00      | $55.00       | $51.88    | Lumpy          |
| $2/SF annual       | $58.00      | $68.00       | $58.16    | Linear growth  |

---

## 6. Lease Value Formulas

### Present Value of a Lease (Landlord Perspective)

```
PV_lease = sum(t=1..T) [(rent_t + reimbursements_t) / (1+r)^t]
         - TI / (1+r)^0
         - LC / (1+r)^0
         - sum(free_rent_months) [rent_t / (1+r)^t]
```

### Incremental Value of Lease Extension

```
Value of N additional years:

  Extension_value = sum(t=T+1..T+N) [rent_t / (1+r)^t]
                  - TI_refresh / (1+r)^T
                  - LC_renewal / (1+r)^T

  Cap rate value = Extension_annual_NOI / cap_rate
```

### Mark-to-Market Value

```
MTM_value = (market_rent - in_place_rent) * SF * remaining_years / (1+r)^avg_year

If MTM > 0: below-market lease (value upside on expiration)
If MTM < 0: above-market lease (value risk on expiration)
```

---

## 7. Operating Expense Pass-Through Economics

### NNN (Triple Net) Effective Rent

```
Landlord net = base_rent (all OpEx passed through)
Tenant total cost = base_rent + RE_tax + insurance + CAM

Landlord effective rent comparison:
  NNN $35/SF with $18/SF pass-throughs = Gross equivalent $53/SF
  Gross $50/SF = NNN equivalent $32/SF (if OpEx = $18/SF)
```

### Modified Gross with Base Year Stop

```
Tenant obligation:
  Year 1: base_rent (landlord absorbs all OpEx up to base year amount)
  Year 2+: base_rent + (actual_OpEx - base_year_OpEx)

If OpEx grows 3% annually from $18/SF base:
  Year 1: tenant pays $0 overage
  Year 2: tenant pays $0.54/SF ($18.54 - $18.00)
  Year 3: tenant pays $1.09/SF ($19.09 - $18.00)
  Year 5: tenant pays $2.24/SF ($20.24 - $18.00)
  Year 10: tenant pays $5.15/SF ($23.15 - $18.00)
```

### Expense Stop Valuation Impact

```
Comparison of two leases, both $50/SF face:

Lease A: Full-service gross, no stop
  Landlord absorbs all OpEx increases
  If OpEx grows 3%/yr from $18/SF:
    Year 10 landlord net: $50 - $23.15 = $26.85/SF

Lease B: Modified gross, $18/SF base year stop
  Tenant pays increases above $18/SF
  Year 10 landlord net: $50 - $18.00 = $32.00/SF

10-year NPV difference (per SF, 7% discount):
  Lease B advantage: $21.34/SF cumulative
  On 10,000 SF: $213,400 value difference

Takeaway: always negotiate expense stops, never full-service gross
on long-term leases in an inflationary environment.
```

---

## 8. Quick Reference: Key Ratios

```yaml
ratios:
  occupancy_cost_ratio:
    formula: "Total tenant occupancy cost / Tenant annual revenue"
    healthy_office: "5-10%"
    healthy_retail: "8-15%"
    healthy_restaurant: "6-10% (rent only, ex utilities)"
    warning: ">15% for any use"
    distress: ">20%"

  coverage_ratio:
    formula: "Tenant EBITDA / Annual rent obligation"
    healthy: ">3.0x"
    acceptable: "2.0-3.0x"
    watch_list: "1.5-2.0x"
    distress: "<1.5x"

  ti_yield:
    formula: "Annual incremental rent from TI / TI cost"
    target: ">12%"
    acceptable: "8-12%"
    poor: "<8%"

  concession_ratio:
    formula: "Total concession value / Total lease value"
    typical_office: "8-15%"
    typical_retail: "5-12%"
    typical_industrial: "3-8%"
    lease_up_premium: "+3-5%"

  retention_cost:
    formula: "Total renewal concessions / Estimated vacancy + re-lease cost"
    target: "<50% (renewal should cost less than half of re-tenanting)"
```
