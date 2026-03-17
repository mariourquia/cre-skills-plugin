# CAM Reconciliation Calculation Rules Reference

Gross-up methodology, cap application, base year stops, admin fees, pro-rata share calculations, and a full 10-tenant worked reconciliation. Based on standard BOMA and lease conventions.

---

## 1. Pro-Rata Share Calculation

### Definition

A tenant's pro-rata share (PRS) determines what fraction of building operating expenses the tenant pays. It is defined in the lease and is typically based on rentable square footage.

### Formula

```
Pro-rata share = Tenant RSF / Building RSF (or floor RSF, depending on lease)

Where RSF = Rentable Square Feet (includes the tenant's proportionate share of
common areas per BOMA measurement standards)
```

### BOMA Measurement Hierarchy

```
Usable SF (USF): Tenant's exclusive space (within demising walls)
Rentable SF (RSF): USF + proportionate share of floor common area + building common area
Load factor = RSF / USF  (typically 1.10-1.20 for office)

Example:
  Tenant USF: 5,000 SF
  Floor load factor: 1.12
  Building load factor: 1.05
  Tenant RSF: 5,000 * 1.12 * 1.05 = 5,880 SF

  Building total RSF: 150,000 SF
  Pro-rata share: 5,880 / 150,000 = 3.92%
```

### Multi-Tenant Floor vs. Full-Floor Tenant

```
Multi-tenant floor:
  Pro-rata share includes floor common area (corridors, restrooms on multi-tenant floors)

Full-floor tenant:
  Tenant pays for entire floor common area directly (restrooms become part of USF)
  Load factor is lower (building common area only)
  Pro-rata share is slightly different
```

---

## 2. Gross-Up Convention (BOMA 95% Standard)

### Rule

Operating expenses that vary with occupancy must be "grossed up" to reflect what they would be if the building were at the assumed standard occupancy (typically 95%). This prevents tenants from subsidizing vacant space -- the landlord bears vacancy risk.

### Formula

```
Grossed-up expense = Actual variable expense / Actual occupancy rate

Or equivalently:
Grossed-up expense = Actual variable expense * (Standard occupancy / Actual occupancy)

Standard occupancy = 95% (BOMA convention, but check each lease)
```

### Which Expenses Are Variable (Grossed Up)?

```
Variable (gross up):
  - Janitorial / cleaning
  - Utilities (electric, gas, water)
  - Management fee (if % of revenue)
  - Repairs & maintenance (partially)
  - Trash removal
  - Security (partially)

Fixed (do NOT gross up):
  - Real estate taxes
  - Insurance
  - Capital reserve
  - Base building maintenance contracts (elevator, fire alarm)
  - Management fee (if flat dollar amount)
```

### Worked Example

```
Building: 150,000 RSF, currently 82% occupied (123,000 SF leased)

Actual janitorial expense: $246,000
This expense varies with occupancy (more tenants = more cleaning).

Grossed-up janitorial = $246,000 / 0.82 = $300,000

Alternative: $246,000 * (0.95 / 0.82) = $284,756 (gross up to 95%, not 100%)

The 95% convention means:
  Grossed-up = $246,000 * (0.95 / 0.82) = $284,756

This is what janitorial would cost if the building were 95% occupied.
Tenants pay their share of $284,756, not $246,000.
Landlord absorbs the difference between 95% and 100% occupancy.
```

### Lease Language Variations

```
"Landlord shall gross up variable operating expenses to reflect 95% occupancy"
  -> Standard BOMA. Gross up to 95%.

"Expenses shall be computed as if the building were fully occupied"
  -> Gross up to 100%. More tenant-friendly (lower per-tenant cost).

"No gross-up provision"
  -> Tenant pays share of actual expenses. Landlord-friendly at high occupancy,
     tenant-unfriendly at low occupancy. Rare in institutional leases.
```

---

## 3. CAM Cap Application

### Definition

A CAM cap limits the maximum annual increase in CAM charges a tenant can be assessed. It protects tenants from large year-over-year expense spikes.

### Types of Caps

```
Cumulative cap: Increase is measured from the base year, compounding each year.
  Year N max = Base_year_CAM * (1 + cap_rate)^N

Non-cumulative cap: Increase is measured year-over-year only.
  Year N max = Year_(N-1)_billed * (1 + cap_rate)

Cumulative caps are more tenant-friendly because they prevent "catching up" after
a low-expense year.
```

### Worked Example: Cumulative vs. Non-Cumulative

```
Base year CAM per SF: $12.00
Cap rate: 5%/year

Year | Actual CAM | Cumulative Cap | Non-Cumulative Cap | Billed (Cumul) | Billed (Non-Cumul)
-----|------------|----------------|--------------------|-----------------|---------
  1  |   $12.00   |    $12.00      |     $12.00         |    $12.00       | $12.00
  2  |   $12.80   |    $12.60      |     $12.60         |    $12.60       | $12.60
  3  |   $12.50   |    $13.23      |     $13.23         |    $12.50       | $12.50
  4  |   $14.50   |    $13.89      |     $13.13         |    $13.89       | $13.13
  5  |   $15.20   |    $14.59      |     $13.79         |    $14.59       | $13.79

Year 4: Actual ($14.50) exceeds cumulative cap ($13.89) and non-cumul cap ($13.13).
  Cumulative: Tenant pays $13.89. Landlord absorbs $0.61/SF.
  Non-cumulative: Tenant pays $13.13. Landlord absorbs $1.37/SF.

Year 5: Non-cumulative cap is lower because it builds on Year 4's capped (lower) amount.
  Cumulative: $14.59 cap (5% compound from $12.00 base)
  Non-cumulative: $13.79 cap (5% from Year 4's $13.13 billed amount)

Over 5 years, the landlord absorbs $0.61/SF under cumulative and $1.41/SF under
non-cumulative. Non-cumulative caps create a growing gap over time.
```

### Controllable vs. Non-Controllable Split

Some leases apply the cap only to "controllable" expenses and pass through "non-controllable" expenses without a cap.

```
Controllable (subject to cap):
  - Janitorial, repairs, maintenance, landscaping, security, admin

Non-controllable (no cap, full pass-through):
  - Real estate taxes
  - Insurance
  - Utilities (sometimes)

This structure protects the landlord from tax and insurance spikes while
giving the tenant predictability on operating costs.
```

---

## 4. Base Year / Expense Stop

### Definition

A base year (or expense stop) establishes the landlord's share of operating expenses. The tenant pays their pro-rata share of expenses above the base year amount.

### Formula

```
Tenant's additional rent = max(0, (Current_year_expenses - Base_year_expenses)) * PRS

Where PRS = pro-rata share
```

### Base Year vs. Fixed Stop

```
Base year: The actual operating expenses in the year the lease commences.
  Dynamic -- set by actual costs. Landlord bears risk of high base year.

Fixed stop (dollar stop): A negotiated fixed dollar amount per SF.
  Example: $14.00/SF stop. Tenant pays share of expenses above $14.00/SF.
  Predictable for both parties. Landlord prefers lower stops; tenant prefers higher.
```

### Worked Example

```
Building: 150,000 RSF
Tenant: 7,500 RSF (5.0% PRS)
Lease commencement: January 2024 (base year = 2024)

2024 actual operating expenses: $2,100,000 ($14.00/SF)
2025 actual operating expenses: $2,250,000 ($15.00/SF)

Tenant's 2025 additional rent:
  Increase over base: $15.00 - $14.00 = $1.00/SF
  Tenant share: $1.00 * 7,500 SF = $7,500

If base year was set artificially low (e.g., building was 60% occupied in 2024):
  2024 grossed-up expenses: $2,100,000 / 0.60 * 0.95 = $3,325,000 ($22.17/SF)
  2025 at full occupancy: $2,250,000 ($15.00/SF)
  Tenant's additional rent: max(0, $15.00 - $22.17) * 7,500 = $0

  The high grossed-up base year protects the tenant for several years.
  This is why landlords prefer gross-up provisions in base year leases.
```

---

## 5. Administrative Fee

### Definition

Landlords typically add an administrative fee (or overhead charge) to CAM reimbursements to cover the cost of accounting, reconciliation, and property management overhead.

### Standard Rates

```
Administrative fee: 5-15% of total CAM charges (10% most common)

Applied to: Total operating expenses before tenant share calculation
```

### Worked Example

```
Total building operating expenses: $2,250,000
Admin fee: 10%
Adjusted expenses: $2,250,000 * 1.10 = $2,475,000

Tenant (5.0% PRS) share of adjusted expenses:
  $2,475,000 * 0.05 = $123,750

Without admin fee:
  $2,250,000 * 0.05 = $112,500

Admin fee impact: $11,250/year to this tenant
Building-wide admin fee revenue: $225,000/year
```

### Lease Negotiation Note

Tenants should negotiate whether the admin fee applies to all expenses or only controllable expenses. Applying a 10% admin fee to real estate taxes ($800,000) adds $80,000 of landlord revenue with no corresponding administrative effort.

---

## 6. Full 10-Tenant CAM Reconciliation

### Building Profile

```
Building: 150,000 RSF, Class A office, 10 tenants
Fiscal year: January-December 2025
Base building occupancy: 92% (138,000 SF occupied)
Gross-up standard: 95%
```

### Tenant Roster

```
Tenant         | RSF    | PRS    | Base Year | Stop Type   | Cap  | Admin Fee
---------------|--------|--------|-----------|-------------|------|----------
AlphaCo        | 30,000 | 20.00% | 2022      | Base year   | 5%   | 10%
BetaInc        | 22,500 | 15.00% | 2023      | Base year   | None | 10%
GammaTech      | 18,000 | 12.00% | 2024      | $14.50 stop | 5%   | 10%
DeltaFin       | 15,000 | 10.00% | 2023      | Base year   | 5%   | 15%
EpsilonMgmt    | 12,000 |  8.00% | 2024      | Base year   | None | 10%
ZetaLaw        | 10,500 |  7.00% | 2022      | $13.00 stop | None | 10%
EtaMedia       |  9,000 |  6.00% | 2025      | Base year   | 5%   | 10%
ThetaHealth    |  7,500 |  5.00% | 2024      | $14.00 stop | 3%   | 10%
IotaDesign     |  7,500 |  5.00% | 2025      | Base year   | None | 10%
KappaConsult   |  6,000 |  4.00% | 2023      | $13.50 stop | 5%   | 10%
Vacant         | 12,000 |  8.00% | --        | --          | --   | --
               |--------|--------|           |             |      |
Total          |150,000 |100.00% |           |             |      |
```

### 2025 Actual Operating Expenses

```
Category              | Actual     | Variable? | Grossed-Up (to 95%)
----------------------|------------|-----------|---------------------
Real estate taxes     | $780,000   | No        | $780,000
Insurance             | $120,000   | No        | $120,000
Janitorial            | $276,000   | Yes       | $285,000  [276K * 0.95/0.92]
Utilities             | $330,000   | Yes       | $340,761  [330K * 0.95/0.92]
Repairs & maintenance | $195,000   | Partial   | $201,250  [50% grossed up]
Management fee        | $225,000   | Yes       | $232,337  [225K * 0.95/0.92]
Security              | $108,000   | Partial   | $111,522  [50% grossed up]
Elevator maintenance  | $54,000    | No        | $54,000
Common area supplies  | $36,000    | Yes       | $37,174
Landscaping           | $42,000    | No        | $42,000
Trash removal         | $24,000    | Yes       | $24,783
Capital reserve       | $75,000    | No        | $75,000
----------------------|------------|-----------|---------------------
Total                 | $2,265,000 |           | $2,303,827
Per SF (actual):      | $15.10     |           | $15.36
```

### Historical Base Years (Grossed-Up)

```
2022 operating expenses (grossed-up): $1,950,000 ($13.00/SF)
2023 operating expenses (grossed-up): $2,055,000 ($13.70/SF)
2024 operating expenses (grossed-up): $2,175,000 ($14.50/SF)
2025 operating expenses (grossed-up): $2,303,827 ($15.36/SF)
```

### Tenant-by-Tenant Reconciliation

```
AlphaCo (20.00% PRS, 2022 base year, 5% cumulative cap, 10% admin):
  2025 grossed-up expenses: $2,303,827
  + 10% admin fee: $2,303,827 * 1.10 = $2,534,210
  Per SF: $16.89
  Base year (2022): $13.00/SF
  Increase: $16.89 - $13.00 = $3.89/SF
  Cap check (5% cumulative from 2022, 3 years): $13.00 * 1.05^3 = $15.05
  Capped increase: $15.05 - $13.00 = $2.05/SF
  Billed: min($3.89, $2.05) = $2.05/SF  [CAP BINDING]
  Tenant payment: $2.05 * 30,000 = $61,500
  Uncollected (landlord absorbs): ($3.89 - $2.05) * 30,000 = $55,200

BetaInc (15.00% PRS, 2023 base year, no cap, 10% admin):
  Increase: $16.89 - $13.70 = $3.19/SF (adjusted for 2023 base)
  No cap: full $3.19 passes through
  Tenant payment: $3.19 * 22,500 = $71,775

GammaTech (12.00% PRS, $14.50 stop, 5% cumulative cap, 10% admin):
  Increase: $16.89 - $14.50 = $2.39/SF
  Cap (from 2024 lease start, 1 year): $14.50 * 1.05 = $15.23
  Capped increase: $15.23 - $14.50 = $0.73/SF  [CAP BINDING]
  Tenant payment: $0.73 * 18,000 = $13,140
  Uncollected: ($2.39 - $0.73) * 18,000 = $29,880

DeltaFin (10.00% PRS, 2023 base year, 5% cumulative cap, 15% admin):
  Expenses + 15% admin: $2,303,827 * 1.15 = $2,649,401 / 150,000 = $17.66/SF
  Increase: $17.66 - $13.70 = $3.96/SF
  Cap (2 years from 2023): $13.70 * 1.05^2 = $15.10
  Capped increase: $15.10 - $13.70 = $1.40/SF  [CAP BINDING]
  Tenant payment: $1.40 * 15,000 = $21,000

EpsilonMgmt (8.00% PRS, 2024 base year, no cap, 10% admin):
  Increase: $16.89 - $14.50 = $2.39/SF
  No cap: full pass-through
  Tenant payment: $2.39 * 12,000 = $28,680

ZetaLaw (7.00% PRS, $13.00 stop, no cap, 10% admin):
  Increase: $16.89 - $13.00 = $3.89/SF
  No cap: full pass-through
  Tenant payment: $3.89 * 10,500 = $40,845

EtaMedia (6.00% PRS, 2025 base year, 5% cap, 10% admin):
  Base year = current year. No increase.
  Tenant payment: $0

ThetaHealth (5.00% PRS, $14.00 stop, 3% cumulative cap, 10% admin):
  Increase: $16.89 - $14.00 = $2.89/SF
  Cap (1 year from 2024): $14.00 * 1.03 = $14.42
  Capped increase: $14.42 - $14.00 = $0.42/SF  [CAP BINDING]
  Tenant payment: $0.42 * 7,500 = $3,150
  Uncollected: ($2.89 - $0.42) * 7,500 = $18,525

IotaDesign (5.00% PRS, 2025 base year, no cap, 10% admin):
  Base year = current year. No increase.
  Tenant payment: $0

KappaConsult (4.00% PRS, $13.50 stop, 5% cumulative cap, 10% admin):
  Increase: $16.89 - $13.50 = $3.39/SF
  Cap (2 years from 2023): $13.50 * 1.05^2 = $14.88
  Capped increase: $14.88 - $13.50 = $1.38/SF  [CAP BINDING]
  Tenant payment: $1.38 * 6,000 = $8,280
```

### Reconciliation Summary

```
Tenant         | Billed   | Cap Loss  | Uncapped Would-Be
---------------|----------|-----------|-------------------
AlphaCo        | $61,500  | $55,200   | $116,700
BetaInc        | $71,775  | $0        | $71,775
GammaTech      | $13,140  | $29,880   | $43,020
DeltaFin       | $21,000  | $38,400   | $59,400
EpsilonMgmt    | $28,680  | $0        | $28,680
ZetaLaw        | $40,845  | $0        | $40,845
EtaMedia       | $0       | $0        | $0
ThetaHealth    | $3,150   | $18,525   | $21,675
IotaDesign     | $0       | $0        | $0
KappaConsult   | $8,280   | $8,280    | $16,560
Vacant (LL)    | --       | --        | --
---------------|----------|-----------|-------------------
Total          | $248,370 | $150,285  | $398,655

Total CAM revenue collected: $248,370
Total CAM lost to caps: $150,285 (37.7% of potential recovery)
Landlord's unrecoverable expense: $150,285 + vacant space share

Effective recovery rate: $248,370 / $2,303,827 = 10.8%
  (Low because base year tenants and new leases have $0 escalation in year 1)

At stabilization (all tenants 3+ years into leases, no base year effect):
  Estimated recovery rate: 55-65% of grossed-up expenses above weighted-avg stop
```

---

## 7. Common Reconciliation Errors

```
1. Failing to gross up variable expenses (understates tenant charges)
2. Applying admin fee to base year AND current year (double-counting)
3. Using USF instead of RSF for pro-rata share (understates tenant share)
4. Not applying cap correctly (cumulative vs non-cumulative confusion)
5. Including capital expenditures in operating expenses (overstates charges)
6. Forgetting to exclude expenses specifically carved out in the lease
7. Using wrong base year for tenants with different commencement dates
8. Not pro-rating for partial-year tenants (move-in mid-year)
9. Applying gross-up when building is above 95% occupancy (should use actual)
10. Failing to segregate controllable vs non-controllable for cap application
```
