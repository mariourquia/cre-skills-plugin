# Rent Roll Validation Rules

## Purpose

Ensure data quality and catch errors before the rent roll is used for underwriting, reporting, or investor communications. Every rent roll has errors. The question is whether you catch them before they become underwriting assumptions.

## Validation Categories

### 1. Completeness Checks

These verify that all required fields are populated.

| Rule ID | Check | Severity | Action if Failed |
|---|---|---|---|
| V-C01 | Every unit has a unit_id | Error | Cannot process row without identifier |
| V-C02 | Every unit has tenant_name or 'VACANT' | Error | Flag for manual review |
| V-C03 | Every occupied unit has lease_start and lease_end | Error | Cannot calculate term metrics |
| V-C04 | Every unit has rentable_sf > 0 | Error | SF required for per-SF calculations |
| V-C05 | Every occupied unit has monthly_base_rent >= 0 | Error | Revenue calculation impossible |
| V-C06 | Every unit has lease_status populated | Error | Cannot determine occupancy |
| V-C07 | Market rent populated for all units (including vacant) | Warning | Loss-to-lease cannot be calculated |
| V-C08 | Security deposit populated for all occupied units | Warning | Deposit reconciliation impossible |

### 2. Consistency Checks

These verify that fields are internally consistent.

| Rule ID | Check | Formula | Severity |
|---|---|---|---|
| V-K01 | Annual rent = monthly x 12 | `ABS(annual_base_rent - monthly_base_rent * 12) < 12` | Error |
| V-K02 | Rent/SF = annual / SF | `ABS(rent_per_sf - annual_base_rent / rentable_sf) < 0.10` | Warning |
| V-K03 | Lease end >= lease start | `lease_end >= lease_start` | Error |
| V-K04 | Lease term matches dates | `ABS(lease_term_months - DATEDIFF(lease_start, lease_end, 'months')) <= 1` | Warning |
| V-K05 | Vacant units have $0 rent | `IF lease_status = 'vacant' THEN monthly_base_rent = 0` | Error |
| V-K06 | Occupied units have $0+ rent | `IF lease_status = 'occupied' THEN monthly_base_rent > 0` | Warning |
| V-K07 | Effective rent <= face rent | `effective_rent <= monthly_base_rent` | Warning |
| V-K08 | Total SF = sum of all units | `ABS(SUM(rentable_sf) - property_total_sf) < property_total_sf * 0.02` | Warning |
| V-K09 | Occupied unit count matches | `COUNT(occupied) = reported_occupied_count` | Error |
| V-K10 | NNN charges present for NNN leases | `IF lease_type = 'nnn' THEN cam_charge + tax_charge + insurance_charge > 0` | Warning |

### 3. Reasonableness Checks

These flag values outside expected ranges. They do not necessarily indicate errors but require review.

| Rule ID | Check | Threshold | Severity |
|---|---|---|---|
| V-R01 | Rent/unit within market range | `monthly_base_rent BETWEEN market_rent * 0.70 AND market_rent * 1.30` | Warning |
| V-R02 | Rent/SF within property type range | See ranges below | Warning |
| V-R03 | Lease term within typical range | MF: 1-24 months; Office: 12-180 months; Industrial: 12-240 months | Warning |
| V-R04 | Security deposit within typical range | MF: 0.5-2x monthly rent; Commercial: 1-6x monthly rent | Warning |
| V-R05 | Unit SF within typical range | Studio: 300-600; 1BR: 500-1000; 2BR: 700-1400; 3BR: 900-2000 | Warning |
| V-R06 | Lease start date is reasonable | `lease_start >= property_vintage_date AND lease_start <= TODAY()` | Warning |
| V-R07 | Lease end date is reasonable | `lease_end >= TODAY() - 365 AND lease_end <= TODAY() + 3650` | Warning |
| V-R08 | Balance due is not excessive | `balance_due < monthly_base_rent * 3` (more than 3 months = flag) | Warning |
| V-R09 | Concession value is reasonable | `concession_monthly < monthly_base_rent * 0.25` | Warning |
| V-R10 | CAM charge is within market range | Office: $5-25/SF; Retail: $8-30/SF; Industrial: $2-8/SF | Warning |

**Rent/SF Reasonableness Ranges (annual):**

| Property Type | Low | Typical | High | Extreme |
|---|---|---|---|---|
| Multifamily (per unit/mo) | $500 | $800-2,000 | $3,500 | $5,000+ |
| Office (NNN/SF) | $10 | $18-40 | $60 | $100+ |
| Industrial (NNN/SF) | $3 | $6-12 | $18 | $25+ |
| Retail (NNN/SF) | $8 | $15-35 | $60 | $100+ |
| Medical Office (NNN/SF) | $15 | $22-45 | $65 | $80+ |

Note: Ranges are national guidelines. Markets vary significantly. Adjust for local conditions.

### 4. Duplicate and Uniqueness Checks

| Rule ID | Check | Severity |
|---|---|---|
| V-U01 | No duplicate unit_id values | Error |
| V-U02 | No duplicate tenant_name + unit_id combinations | Error |
| V-U03 | Flag identical rent amounts for 5+ consecutive units (possible paste error) | Warning |
| V-U04 | Flag identical lease_start dates for 10+ units (possible default date) | Warning |

### 5. Temporal Checks

| Rule ID | Check | Severity |
|---|---|---|
| V-T01 | Expired leases flagged (lease_end < TODAY and status = occupied) | Warning |
| V-T02 | Leases expiring within 30 days flagged | Info |
| V-T03 | Leases expiring within 90 days with no renewal indication | Warning |
| V-T04 | Lease start in future but status = occupied | Warning |
| V-T05 | Move-in date after lease start by >30 days | Warning |

### 6. Cross-Validation Against External Data

| Rule ID | Check | External Source | Severity |
|---|---|---|---|
| V-X01 | Total revenue matches T12 last month | T12 P&L | Error if >2% variance |
| V-X02 | Total deposits match balance sheet | Balance sheet | Error if >1% variance |
| V-X03 | Unit count matches PCA or survey | PCA report | Warning |
| V-X04 | Total SF matches appraisal or survey | ALTA survey | Warning if >2% variance |
| V-X05 | Vacancy matches broker/seller representation | OM or listing | Warning if >3 pts variance |

## Derived Field Calculations

### Loss-to-Lease
```
Per Unit:    loss_to_lease = market_rent - monthly_base_rent
             (positive = below market, negative = above market)

Property:    total_loss_to_lease = SUM(loss_to_lease WHERE loss_to_lease > 0)
             loss_to_lease_pct = total_loss_to_lease / SUM(market_rent) * 100
```

### Occupancy Rates
```
Physical:    occupied_units / total_units * 100
             (counts: occupied, month_to_month)
             (excludes: vacant, down, model)

Economic:    actual_gross_rent / potential_gross_rent * 100
             actual_gross_rent = SUM(monthly_base_rent for occupied)
             potential_gross_rent = SUM(market_rent for all units)
```

### WALE (Weighted Average Lease Expiration)
```
WALE = SUM(remaining_months_i * annual_rent_i) / SUM(annual_rent_i) / 12

Where:
  remaining_months_i = MAX(0, DATEDIFF(TODAY, lease_end_i, 'months'))
  annual_rent_i = monthly_base_rent_i * 12

Result in years. Higher WALE = more income stability.
Typical targets:
  - Multifamily: 0.5-1.0 years (short leases are normal)
  - Office: 3-7 years
  - Industrial: 3-10 years
  - Retail (anchored): 5-15 years
```

### Lease Expiration Schedule
```
For each future quarter:
  expiring_units = COUNT(units WHERE lease_end IN quarter)
  expiring_sf = SUM(rentable_sf WHERE lease_end IN quarter)
  expiring_rent = SUM(annual_base_rent WHERE lease_end IN quarter)
  expiring_pct_revenue = expiring_rent / total_annual_revenue * 100
```

Concentration threshold: flag any quarter with >20% of revenue expiring.

### Tenant Concentration
```
For each tenant (or related entity group):
  tenant_sf = SUM(rentable_sf)
  tenant_pct_nra = tenant_sf / total_rentable_sf * 100
  tenant_rent = SUM(annual_base_rent)
  tenant_pct_revenue = tenant_rent / total_annual_revenue * 100
```

Concentration threshold: flag any tenant with >25% of revenue or >30% of NRA.

### Delinquency Analysis
```
Current:     balance_due <= 0 OR balance_due <= monthly_base_rent * 0.5
30-Day:      balance_due > monthly_base_rent * 0.5 AND <= monthly_base_rent * 1.5
60-Day:      balance_due > monthly_base_rent * 1.5 AND <= monthly_base_rent * 2.5
90-Day+:     balance_due > monthly_base_rent * 2.5

Delinquency rate = COUNT(units with balance_due > monthly_base_rent * 0.5) / occupied_units
Dollar delinquency = SUM(balance_due WHERE balance_due > 0)
```

### Revenue Projection
```
Gross Potential Rent (GPR):
  occupied_units: monthly_base_rent * 12
  vacant_units: market_rent * 12

Less: Vacancy & Credit Loss:
  physical_vacancy = (1 - physical_occupancy) * GPR_at_market
  concession_loss = SUM(concession_monthly) * 12
  bad_debt = GPR * bad_debt_pct (historical or assumed)

Effective Gross Income (EGI):
  EGI = GPR - vacancy_loss - concession_loss - bad_debt + other_income

This projection bridges the rent roll to the income statement.
```

## Common Errors and How to Catch Them

| Error | How It Appears | Detection Rule | Impact |
|---|---|---|---|
| Wrong unit count | Total units don't match seller's rep | V-X03 | Inflated/deflated occupancy |
| Stale rent roll | Dates are 3+ months old | Check rent_roll_date vs today | Underwriting on outdated data |
| Missing concessions | Face rent shown, concessions omitted | Compare face to market + interview leasing | Overstated revenue |
| Duplicate units | Same unit appears twice | V-U01 | Double-counted revenue |
| Default dates | All leases show same start date | V-U04 | Invalid term calculations |
| Above-market ghost tenants | High rent on soon-to-expire lease | V-R01 + V-T03 | Overstated sustainable income |
| Excluded units | Model, office, or down units omitted | Compare total to building SF | Understated vacancy |
| Wrong lease type | NNN shown as gross (or vice versa) | V-K10, compare to lease | Misstated expense responsibility |
| Rounded rents | All rents round to $50 increments | Statistical check | May mask actual terms |
| Pre-leased but not occupied | Lease signed, not yet moved in | V-T04, check with PM | May not generate revenue yet |
