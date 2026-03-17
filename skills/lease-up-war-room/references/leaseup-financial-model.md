# Lease-Up Financial Model: 150-Unit Multifamily

## Overview

Monthly cash flow buildout for a 150-unit Class A multifamily during lease-up.
Covers revenue ramp, concession burn-down, operating expense phase-in, reserve
adequacy testing, and breakeven analysis.

---

## 1. Property Assumptions

```yaml
property:
  units: 150
  avg_unit_sf: 875
  total_rsf: 131250
  unit_mix:
    studio:  {count: 30, sf: 550, asking_rent: 1850}
    one_bed: {count: 75, sf: 825, asking_rent: 2400}
    two_bed: {count: 35, sf: 1150, asking_rent: 3200}
    three_bed: {count: 10, sf: 1400, asking_rent: 3800}
  weighted_avg_rent: 2513  # Blended across unit mix
  gross_potential_rent_monthly: 376950  # 150 x $2,513
  gross_potential_rent_annual: 4523400

other_income:
  parking_per_space: 150
  parking_spaces: 120
  storage_per_unit: 75
  storage_units: 40
  laundry_monthly: 2500
  pet_fees_monthly: 3000  # $50/mo x ~60 pets
  application_fees_monthly: 1500
  total_other_monthly: 25000
  total_other_annual: 300000

financing:
  loan_amount: 45000000
  interest_rate: 0.0575
  io_period_months: 36  # Interest-only during lease-up
  monthly_io_payment: 215625  # $45M x 5.75% / 12
  debt_service_annual: 2587500

development_cost:
  total: 58000000
  equity: 13000000
  equity_investor_pref: 0.08  # 8% preferred return
  monthly_pref_accrual: 86667  # $13M x 8% / 12
```

---

## 2. Absorption Schedule

Based on Class A multifamily in a normal market: 5% monthly absorption rate.

```
Month  | New Leases | Cumulative | Occupancy % | Notes
-------|------------|------------|-------------|------
  1    |     8      |      8     |    5.3%     | Pre-leasing conversions
  2    |     8      |     16     |   10.7%     |
  3    |     8      |     24     |   16.0%     |
  4    |     8      |     32     |   21.3%     |
  5    |     8      |     40     |   26.7%     |
  6    |     8      |     48     |   32.0%     |
  7    |     8      |     56     |   37.3%     |
  8    |     8      |     64     |   42.7%     |
  9    |     7      |     71     |   47.3%     | Slight deceleration
 10    |     7      |     78     |   52.0%     |
 11    |     7      |     85     |   56.7%     |
 12    |     7      |     92     |   61.3%     |
 13    |     7      |     99     |   66.0%     |
 14    |     7      |    106     |   70.7%     |
 15    |     6      |    112     |   74.7%     |
 16    |     6      |    118     |   78.7%     |
 17    |     6      |    124     |   82.7%     |
 18    |     5      |    129     |   86.0%     |
 19    |     5      |    134     |   89.3%     |
 20    |     4      |    138     |   92.0%     |
 21    |     3      |    141     |   94.0%     |
 22    |     2      |    143     |   95.3%     | Stabilized (>95%)
 23    |     0      |    143     |   95.3%     | Natural vacancy
 24    |     0      |    143     |   95.3%     |
```

Stabilization at month 22. Total lease-up period: ~22 months.

---

## 3. Concession Burn-Down Schedule

Concessions start at 2 months free on a 14-month lease (normal market + lease-up
premium) and burn down as occupancy increases.

```
Occupancy Band  | Free Rent | Effective   | Concession | Monthly
                | (months)  | Concession% | Cost/Unit  | Burn Rate
----------------|-----------|-------------|------------|----------
  0% - 20%      |   2.0     |  14.3%      |  $5,026    | Months 1-4
 20% - 40%      |   1.5     |  10.7%      |  $3,770    | Months 5-8
 40% - 60%      |   1.0     |   7.1%      |  $2,513    | Months 9-12
 60% - 75%      |   0.5     |   3.6%      |  $1,257    | Months 13-15
 75% - 85%      |   0.0     |   0.0%      |     $0     | Months 16-18
 85% - 95%      |   0.0     |   0.0%      |     $0     | Months 19-22
```

**Total concession cost:**
- Units 1-30 (0-20% band): 30 x $5,026 = $150,780
- Units 31-60 (20-40%): 30 x $3,770 = $113,100
- Units 61-90 (40-60%): 30 x $2,513 = $75,390
- Units 91-112 (60-75%): 22 x $1,257 = $27,654
- Units 113-143 (75%+): 31 x $0 = $0
- **Total concessions: $366,924** (2.2% of Year 1+2 GPR)

---

## 4. Monthly Cash Flow Model

### Revenue Build

```
Month | Occupied | Gross Rent | Concessions | Effective  | Other   | Total
      | Units    | (Monthly)  | (Monthly)   | Rent Rev   | Income  | Revenue
------|----------|------------|-------------|------------|---------|--------
  1   |    8     |  20,104    |   (2,872)   |   17,232   |  1,333  |  18,565
  2   |   16     |  40,208    |   (5,744)   |   34,464   |  2,667  |  37,131
  3   |   24     |  60,312    |   (8,616)   |   51,696   |  4,000  |  55,696
  4   |   32     |  80,416    |  (11,488)   |   68,928   |  5,333  |  74,261
  5   |   40     | 100,520    |  (10,756)   |   89,764   |  6,667  |  96,431
  6   |   48     | 120,624    |  (12,907)   |  107,717   |  8,000  | 115,717
  7   |   56     | 140,728    |  (15,058)   |  125,670   |  9,333  | 135,003
  8   |   64     | 160,832    |  (17,209)   |  143,623   | 10,667  | 154,290
  9   |   71     | 178,423    |  (12,659)   |  165,764   | 11,833  | 177,597
 10   |   78     | 196,014    |  (13,905)   |  182,109   | 13,000  | 195,109
 11   |   85     | 213,605    |  (15,151)   |  198,454   | 14,167  | 212,621
 12   |   92     | 231,196    |  (16,397)   |  214,799   | 15,333  | 230,132

Year 1 Total Revenue: $1,502,554

 13   |   99     | 248,787    |   (8,946)   |  239,841   | 16,500  | 256,341
 14   |  106     | 266,378    |   (9,580)   |  256,798   | 17,667  | 274,465
 15   |  112     | 281,456    |   (5,062)   |  276,394   | 18,667  | 295,061
 16   |  118     | 296,534    |       0     |  296,534   | 19,667  | 316,201
 17   |  124     | 311,612    |       0     |  311,612   | 20,667  | 332,279
 18   |  129     | 324,177    |       0     |  324,177   | 21,500  | 345,677
 19   |  134     | 336,742    |       0     |  336,742   | 22,333  | 359,075
 20   |  138     | 346,794    |       0     |  346,794   | 23,000  | 369,794
 21   |  141     | 354,333    |       0     |  354,333   | 23,500  | 377,833
 22   |  143     | 359,359    |       0     |  359,359   | 23,833  | 383,192
 23   |  143     | 359,359    |       0     |  359,359   | 23,833  | 383,192
 24   |  143     | 359,359    |       0     |  359,359   | 23,833  | 383,192

Year 2 Total Revenue: $3,876,302
```

### Operating Expense Phase-In

Expenses scale with occupancy but have a fixed floor (property tax, insurance,
management minimum).

```yaml
expense_categories:
  fixed_monthly:  # Independent of occupancy
    real_estate_tax: 42000
    insurance: 8500
    management_fee_minimum: 12000  # Or % of revenue, whichever is greater
    common_area_maintenance: 15000
    marketing_lease_up: 18000  # 2x stabilized ($9K/mo)
    total_fixed: 95500

  variable_per_occupied_unit:  # Scale with occupancy
    utilities: 85
    repairs_maintenance: 45
    turnover_reserve: 20
    total_per_unit: 150

  management_fee:
    rate: 0.04  # 4% of effective gross income
    minimum: 12000  # Floor during low-occupancy months
```

```
Month | Fixed    | Variable   | Mgmt Fee | Total    | Notes
      | Expenses | (per unit) | (4%/min) | OpEx     |
------|----------|------------|----------|----------|------
  1   |  95,500  |   1,200    |  12,000  | 108,700  | Mgmt fee at minimum
  2   |  95,500  |   2,400    |  12,000  | 109,900  |
  3   |  95,500  |   3,600    |  12,000  | 111,100  |
  6   |  95,500  |   7,200    |  12,000  | 114,700  |
  9   |  95,500  |  10,650    |  12,000  | 118,150  |
 12   |  95,500  |  13,800    |  12,000  | 121,300  | Revenue crosses mgmt min
 15   |  95,500  |  16,800    |  11,802  | 124,102  | 4% of EGI > minimum
 18   |  86,500  |  19,350    |  13,827  | 119,677  | Marketing drops to stabilized
 22   |  86,500  |  21,450    |  15,328  | 123,278  | Stabilized
```

Marketing expense drops from $18K to $9K at month 18 (85% occupancy).

---

## 5. NOI and Debt Service Coverage

```
Month | Revenue  | OpEx     | NOI       | Debt Svc  | DSCR  | Cash Flow
------|----------|----------|-----------|-----------|-------|----------
  1   |  18,565  | 108,700  |  (90,135) | 215,625   | Neg   | (305,760)
  3   |  55,696  | 111,100  |  (55,404) | 215,625   | Neg   | (271,029)
  6   | 115,717  | 114,700  |    1,017  | 215,625   | 0.00x | (214,608)
  9   | 177,597  | 118,150  |   59,447  | 215,625   | 0.28x | (156,178)
 12   | 230,132  | 121,300  |  108,832  | 215,625   | 0.50x | (106,793)
 15   | 295,061  | 124,102  |  170,959  | 215,625   | 0.79x |  (44,666)
 18   | 345,677  | 119,677  |  226,000  | 215,625   | 1.05x |   10,375
 20   | 369,794  | 121,200  |  248,594  | 215,625   | 1.15x |   32,969
 22   | 383,192  | 123,278  |  259,914  | 215,625   | 1.21x |   44,289
```

**Key milestones:**
- NOI breakeven (NOI > 0): Month 6
- Debt service breakeven (DSCR > 1.0x): Month 18
- Stabilized DSCR: 1.21x (Month 22+)

---

## 6. Reserve Adequacy Test

### Required Reserves

```yaml
reserves:
  operating_reserve:
    purpose: "Fund operating deficits during lease-up"
    calculation: "Cumulative negative cash flow through breakeven"
    amount: 2850000  # Sum of monthly shortfalls months 1-17
    cushion_factor: 1.15  # 15% buffer
    required: 3277500

  interest_reserve:
    purpose: "Fund debt service shortfalls during lease-up"
    months_of_io: 18  # Through debt service breakeven
    total_io_payments: 3881250  # 18 x $215,625
    offset_by_noi: 1050000  # Partial NOI during months 6-17
    net_required: 2831250

  ti_and_lc_reserve:
    purpose: "Leasing costs, concessions, broker commissions"
    concession_budget: 366924
    broker_fees: 0  # In-house leasing team
    lease_up_marketing_premium: 108000  # 12 months x $9K premium
    total: 474924

  capital_reserve:
    purpose: "Initial period capital needs"
    per_unit_annual: 300
    year_1: 45000  # 150 x $300
    year_2: 45000

  total_required_reserves: 6673674
```

### Reserve Adequacy Ratio

```
Reserve Adequacy Ratio = Available Reserves / Required Reserves

Available reserves (from closing):
  Operating reserve escrow:    $3,500,000
  Interest reserve escrow:     $3,000,000
  TI/LC reserve:                 $500,000
  Capital reserve:               $100,000
  Total available:             $7,100,000

Adequacy ratio: $7,100,000 / $6,673,674 = 1.064x

TARGET: > 1.10x
STATUS: MARGINAL -- 6.4% cushion is below 10% target
```

### Stress Test: Absorption Delay

What if absorption is 25% slower than projected?

```
Scenario               | Stabilization | Peak Deficit | Reserve Need | Adequacy
-----------------------|---------------|--------------|--------------|--------
Base case              | Month 22      | ($305,760)   | $6,673,674   | 1.064x
25% slower absorption  | Month 29      | ($305,760)   | $8,841,000   | 0.803x
50% slower absorption  | Month 38      | ($305,760)   | $11,200,000  | 0.634x
10% lower rents        | Month 24      | ($310,900)   | $7,450,000   | 0.953x
Combo: 25% slow + 5%  | Month 32      | ($312,000)   | $9,800,000   | 0.724x
  lower rents          |               |              |              |
```

**Conclusion:** Base case reserves are thin. A 25% absorption delay would
exhaust reserves by month 25, requiring a capital call or line draw. The
sponsor should secure a $2M standby facility or negotiate a reserve top-up
mechanism with the lender.

---

## 7. Breakeven Occupancy Analysis

```
Fixed costs (monthly):
  Operating expenses (fixed):   $95,500
  Debt service (IO):           $215,625
  Total fixed obligations:     $311,125

Variable margin per unit:
  Average rent:                  $2,513
  Less: variable OpEx:            ($150)
  Less: concessions (blended):    ($120)  # Averaged over lease-up
  Net margin per unit:           $2,243

Breakeven units = $311,125 / $2,243 = 139 units = 92.5% occupancy

Post-stabilization (marketing normalized):
  Fixed obligations:           $302,125  # Marketing drops $9K
  Breakeven units:                  135 = 89.8% occupancy
```

---

## 8. Lease-Up Monitoring Dashboard Metrics

Track weekly during lease-up:

```yaml
kpis:
  velocity:
    - tours_per_week
    - applications_per_week
    - leases_signed_per_week
    - tour_to_application_conversion  # Target: >30%
    - application_to_lease_conversion  # Target: >70%
    - cancellation_rate  # Target: <5%

  financial:
    - gross_potential_rent
    - effective_gross_income
    - concession_cost_mtd
    - concession_cost_cumulative
    - noi_trailing_30_day
    - cash_burn_rate  # Monthly cash outflow net of income
    - months_of_reserves_remaining

  occupancy:
    - physical_occupancy  # Units occupied / total
    - economic_occupancy  # Revenue collected / GPR
    - pre_leased_units  # Signed but not yet moved in
    - notice_to_vacate_count  # Early move-outs

  marketing:
    - cost_per_lead
    - cost_per_lease
    - lead_source_breakdown
    - website_traffic
    - social_engagement

  variance:
    - actual_vs_proforma_absorption  # +/- units per month
    - actual_vs_proforma_rent  # +/- per unit
    - actual_vs_proforma_concessions
    - reserve_burn_vs_budget
```

---

## 9. Decision Triggers

```yaml
triggers:
  increase_concessions:
    condition: "Absorption < 75% of proforma for 2 consecutive months"
    action: "Increase free rent by 0.5 months, add $500 move-in bonus"
    budget_impact: "~$50K additional concession cost"

  decrease_concessions:
    condition: "Absorption > 125% of proforma for 2 consecutive months"
    action: "Reduce free rent by 0.5 months, remove move-in bonus"

  raise_rents:
    condition: "Occupancy > 80% AND absorption still > proforma"
    action: "Increase asking rents 2-3% on unleased units"

  capital_call_warning:
    condition: "Reserve adequacy ratio < 1.05x"
    action: "Notify investors, prepare capital call documentation"

  capital_call_trigger:
    condition: "Reserve adequacy ratio < 0.90x"
    action: "Issue capital call for 6 months of projected shortfall"

  marketing_pivot:
    condition: "Cost per lease > $2,000 OR tour conversion < 15%"
    action: "Reallocate marketing spend, review pricing strategy"

  re_underwrite:
    condition: "Absorption < 50% of proforma for 3 consecutive months"
    action: "Full re-underwriting, notify lender, prepare modified business plan"
```
