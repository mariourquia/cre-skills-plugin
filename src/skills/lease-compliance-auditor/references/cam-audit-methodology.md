# CAM Audit Methodology Reference

## Overview

Systematic methodology for auditing Common Area Maintenance (CAM) charges,
gross-up verification, expense cap testing, percentage rent audit, and
recovery quantification. Applicable to retail, office, and industrial leases
with pass-through expense structures.

---

## 1. CAM Audit Framework

### Pre-Audit Setup

```yaml
required_documents:
  from_landlord:
    - "Year-end CAM reconciliation statement (current + prior 2 years)"
    - "General ledger detail for all pass-through expense categories"
    - "Supporting invoices for expenses > $5,000"
    - "Vendor contracts (janitorial, landscaping, security, HVAC maintenance)"
    - "Management agreement (fee structure, affiliate arrangements)"
    - "Property tax bills and assessment notices"
    - "Insurance policy declarations and premium invoices"
    - "Capital expenditure detail and amortization schedules"
    - "Budget vs actual variance report"

  from_tenant:
    - "Lease agreement (with all amendments and side letters)"
    - "CAM payment history (monthly estimates and reconciliation payments)"
    - "Prior audit reports (if any)"
    - "Tenant's pro-rata share calculation"

audit_rights:
  typical_clause: |
    Tenant has the right to audit landlord's books and records relating
    to operating expenses within 180 days of receiving the annual
    reconciliation statement.
  important_terms:
    - "Audit window: 90-365 days from statement receipt"
    - "Look-back period: current year + 2-3 prior years"
    - "Landlord must make records available within 30 days of request"
    - "Audit at landlord's office or copies provided"
    - "If errors > 3-5%: landlord pays audit costs"
```

### Audit Procedure Steps

```
STEP 1: Lease Abstraction
  Extract all expense-related provisions:
  - Pro-rata share calculation (rentable SF / total rentable SF)
  - Expense categories included/excluded
  - Base year or base amount
  - Cap provisions (cumulative vs non-cumulative, compounding)
  - Gross-up provisions
  - Capital expenditure treatment
  - Management fee cap
  - Excluded expenses list
  - Audit rights and remedies

STEP 2: Mathematical Verification
  - Verify pro-rata share calculation
  - Verify base year amount
  - Recalculate each expense category pass-through
  - Verify cap application
  - Verify gross-up calculation
  - Check arithmetic on reconciliation statement

STEP 3: Expense Inclusion Audit
  For each GL line item:
  - Is this expense category included per the lease?
  - Is this a capital expenditure improperly expensed?
  - Is this an excluded expense (landlord-specific, above-building)?
  - Is this a one-time cost not part of normal operations?
  - Is the vendor affiliated with the landlord (related party)?

STEP 4: Reasonableness Testing
  - Compare each category to prior year (>15% variance = flag)
  - Compare to industry benchmarks (BOMA, IREM)
  - Identify unusual or non-recurring items
  - Test management fee against lease cap

STEP 5: Recovery Quantification
  - Calculate total overcharges by category
  - Apply tenant's pro-rata share
  - Compute interest on overpayment (if lease provides)
  - Prepare audit findings report
```

---

## 2. Gross-Up Verification

### Purpose

Gross-up adjusts variable expenses to reflect what they would be at a
specified occupancy level (usually 95% or 100%). Prevents tenants from
bearing disproportionate costs when building is partially vacant.

### Standard Gross-Up Formula

```
Grossed-Up Expense = Actual Variable Expense * (Gross-Up Occupancy / Actual Occupancy)

Where:
  Gross-Up Occupancy = per lease (typically 95% or 100%)
  Actual Occupancy = actual physical or economic occupancy during period

Example:
  Variable janitorial: $120,000 actual
  Actual occupancy: 78%
  Gross-up level: 95%
  Grossed-up janitorial: $120,000 * (95% / 78%) = $146,154

  Tenant's pro-rata share (10%): $14,615
  Without gross-up: $12,000
  Gross-up effect: $2,615 additional charge to tenant
```

### Common Gross-Up Audit Issues

```yaml
audit_issues:
  variable_vs_fixed:
    description: "Only variable expenses should be grossed up"
    variable_expenses:
      - "Janitorial / cleaning"
      - "Utilities (common area)"
      - "Trash removal"
      - "Elevator maintenance (usage-based portion)"
      - "Common area supplies"
    fixed_expenses_no_grossup:
      - "Property tax"
      - "Insurance"
      - "Management fee (typically on actual income, not grossed up)"
      - "Landscaping (fixed contract)"
      - "Security (fixed contract)"
      - "Snow removal (fixed contract)"
    finding: "Landlord grossing up fixed expenses = overcharge"

  wrong_occupancy:
    description: "Landlord using wrong occupancy denominator"
    common_error: "Using physical occupancy when lease says economic"
    common_error_2: "Using year-end occupancy instead of weighted average"
    correct_method: "Weighted average occupancy over the expense period"
    formula: "sum(occupied_sf_month * 1) / (total_sf * 12)"

  grossup_above_cap:
    description: "Grossed-up amount exceeds expense cap"
    rule: "Gross-up is calculated BEFORE cap is applied"
    common_error: "Landlord applies cap to actual, then grosses up"
    correct: "Gross up first, then test against cap"

  no_grossup_clause:
    description: "Lease does not contain gross-up provision"
    rule: "Without explicit gross-up language, landlord cannot gross up"
    finding: "If grossing up without lease authority = overcharge"
```

---

## 3. Expense Cap Testing

### Cap Types

```yaml
cap_types:
  cumulative_non_compounding:
    description: "Expenses cannot exceed base year + X% per year (simple)"
    formula: "Cap = Base * (1 + rate * years_elapsed)"
    example:
      base_year_cam: 500000
      cap_rate: 0.05  # 5% per year
      year_3_cap: 575000  # 500K * (1 + 0.05*3) = 500K + 75K
      year_5_cap: 625000

  cumulative_compounding:
    description: "Expenses cannot exceed base year compounded at X% per year"
    formula: "Cap = Base * (1 + rate)^years_elapsed"
    example:
      base_year_cam: 500000
      cap_rate: 0.05
      year_3_cap: 578813  # 500K * 1.05^3
      year_5_cap: 638141  # 500K * 1.05^5

  non_cumulative:
    description: "Each year's increase cannot exceed X% over prior year"
    formula: "Cap_year_n = Actual_year_(n-1) * (1 + rate)"
    note: "This is the WORST cap for tenants -- ratchets up if actual rises"
    example:
      year_1_actual: 500000  # Base
      year_2_actual: 520000  # Actual 4% increase
      year_3_cap: 546000    # 520K * 1.05 (caps off prior actual, not base)

  controllable_only:
    description: "Cap applies only to controllable expenses"
    controllable:
      - "Janitorial, landscaping, security"
      - "Repairs and maintenance"
      - "Management fee"
      - "Common area utilities"
    uncontrollable_excluded:
      - "Property tax"
      - "Insurance"
      - "Utilities (sometimes)"
      - "Snow removal (sometimes)"
    tenant_risk: "Uncontrollable expenses can increase without limit"
```

### Cap Testing Methodology

```
STEP 1: Identify cap type from lease
STEP 2: Determine base year amount
  - Was base year a full 12-month period?
  - Were there unusual expenses in base year?
  - Was gross-up applied to base year?
STEP 3: Calculate cap for current year
STEP 4: Compare actual expenses (or grossed-up) to cap
STEP 5: If actual > cap: tenant only pays up to cap
         Excess is landlord's cost
STEP 6: Verify landlord applied cap correctly in reconciliation
```

### Worked Example: Cap Audit

```yaml
lease_terms:
  base_year: 2023
  cap_type: "Cumulative compounding"
  cap_rate: 0.04  # 4% per year
  applies_to: "Controllable operating expenses only"

base_year_data:
  controllable: 380000
  uncontrollable: 245000  # Tax + insurance
  total: 625000

year_2025_audit:
  controllable_actual: 428000
  uncontrollable_actual: 275000
  landlord_charged_total: 703000

  cap_calculation:
    controllable_cap: 411085  # 380,000 * 1.04^2
    uncontrollable: 275000   # No cap, pass through actual
    capped_total: 686085     # 411,085 + 275,000

  overcharge:
    landlord_billed: 703000
    correct_amount: 686085
    overcharge: 16915
    tenant_pro_rata: 0.085  # 8.5%
    tenant_overcharge: 1438
```

---

## 4. Percentage Rent Audit

### Mechanics

Percentage rent is additional rent based on tenant's gross sales above a
breakpoint. Common in retail leases.

```
Percentage Rent = max(0, (Gross Sales - Breakpoint) * Percentage Rate)

Natural Breakpoint = Base Rent / Percentage Rate
Artificial Breakpoint = Specific dollar amount stated in lease
```

### Audit Focus Areas

```yaml
percentage_rent_audit:
  gross_sales_definition:
    description: "Lease defines what's included/excluded from gross sales"
    typically_included:
      - "In-store cash and credit sales"
      - "Gift card sales (when redeemed, not when purchased)"
      - "Layaway payments"
      - "Sales from temporary displays or kiosks"
    typically_excluded:
      - "Sales tax collected"
      - "Employee discounts"
      - "Returns and allowances"
      - "Sales of trade fixtures"
      - "Internet/online sales (depends on lease language)"
      - "Catalog sales shipped from distribution center"
      - "Insurance proceeds"
    audit_test: "Compare tenant's reported exclusions to lease definitions"

  reporting_verification:
    - "Monthly sales reports match annual certified statement"
    - "Annual statement certified by CPA (if lease requires)"
    - "POS system data reconciles to reported sales"
    - "Compare to industry benchmarks (sales per SF by category)"

  breakpoint_verification:
    - "Natural breakpoint correctly calculated from current base rent"
    - "If rent changed mid-year: pro-rata breakpoint adjustment"
    - "Artificial breakpoint per lease (not adjusted for rent changes)"
    - "If lease has both: verify which applies"

  common_errors:
    tenant_side:
      - "Excluding online sales that should be included per lease"
      - "Double-counting returns (excluding from gross AND net)"
      - "Not reporting gift card redemptions"
      - "Using fiscal year vs calendar year sales"
    landlord_side:
      - "Applying wrong percentage rate"
      - "Not adjusting breakpoint for mid-year rent changes"
      - "Billing percentage rent on total sales (ignoring breakpoint)"
      - "Not crediting percentage rent already paid monthly"
```

---

## 5. Recovery Quantification

### Recovery Categories

```yaml
common_findings:
  category_1_excluded_expenses:
    description: "Expenses included in CAM that lease excludes"
    examples:
      - "Capital expenditures expensed instead of amortized"
      - "Landlord's income tax or entity-level expenses"
      - "Leasing commissions or tenant improvement costs"
      - "Executive compensation above property level"
      - "Litigation costs (landlord vs other tenants)"
      - "Charitable contributions"
      - "Art or decorations for landlord's office"
    typical_recovery: "5-15% of total CAM charges"

  category_2_misallocation:
    description: "Expenses allocated to wrong property or entity"
    examples:
      - "Shared management office costs not properly allocated"
      - "Centralized accounting charges exceeding lease limit"
      - "Repair costs for other properties in portfolio"
    typical_recovery: "2-8% of total CAM charges"

  category_3_cap_violations:
    description: "Charges exceeding lease-specified caps"
    examples:
      - "Management fee above cap percentage"
      - "Controllable expense increase above annual cap"
      - "Administrative fee above stated limit"
    typical_recovery: "3-10% of capped categories"

  category_4_gross_up_errors:
    description: "Incorrect gross-up calculations"
    examples:
      - "Fixed expenses grossed up"
      - "Wrong occupancy rate used"
      - "Gross-up applied when not in lease"
    typical_recovery: "2-5% of grossed-up categories"

  category_5_prorate_errors:
    description: "Incorrect pro-rata share calculation"
    examples:
      - "Using wrong SF for tenant or building"
      - "Not adjusting for tenant's actual lease commencement"
      - "Using gross instead of rentable SF (or vice versa)"
    typical_recovery: "1-3% of total charges"
```

### Recovery Calculation Template

```
Audit Finding Summary
Property: [name]
Tenant: [name]
Audit Period: [year]
Pro-Rata Share: [X.XX%]

Finding | Category     | Gross    | Tenant   | Notes
  #     |              | Amount   | Share    |
--------|--------------|----------|---------|------
  1     | Excluded     | $18,400  | $1,564  | Capital exp. not amortized
  2     | Excluded     | $12,200  | $1,037  | Litigation costs
  3     | Cap violation| $16,915  | $1,438  | Controllable cap exceeded
  4     | Gross-up     |  $8,300  |   $706  | Fixed exp. grossed up
  5     | Prorate      |  $4,100  |   $349  | Wrong SF in calculation
  6     | Mgmt fee     |  $7,500  |   $638  | Fee above 4% cap
--------|--------------|----------|---------|------
  TOTAL |              | $67,415  | $5,732  |

Interest (if lease provides):
  Overcharge period: 12 months average
  Interest rate: prime + 2% = 10.5%
  Interest: $5,732 * 10.5% * 0.5 = $301

Total Recovery Claim: $6,033

Audit Cost Reimbursement:
  Overcharge > 5% of total charges: YES (5,732 / 85,000 = 6.7%)
  Landlord reimburses audit cost per lease: $8,500
```

---

## 6. Industry Benchmarks

### Operating Expense Benchmarks ($/SF/Year)

Reference for reasonableness testing. Source framework: BOMA Experience
Exchange Report, IREM Income/Expense Analysis.

```
                    | Office    | Retail    | Industrial | MF (per unit)
--------------------|-----------|-----------|------------|-------------
Property Tax        | $6-15     | $3-10     | $1.50-5    | $1,200-4,000
Insurance           | $1-3      | $0.75-2   | $0.40-1.50 | $500-1,500
CAM / Maint.        | $4-10     | $2-6      | $0.75-3    | $1,000-3,000
Utilities           | $3-7      | $1.50-4   | $0.50-2    | $1,200-2,400
Management Fee      | 3-5% EGI  | 3-5% EGI  | 3-5% EGI  | 4-6% EGI
Janitorial          | $2-5      | $0.50-2   | $0.25-1    | Included in CAM
Security            | $1-4      | $0.50-3   | $0.25-1    | $300-1,200/unit
Elevator            | $0.50-2   | N/A       | N/A        | $200-800/unit
--------------------|-----------|-----------|------------|-------------
Total OpEx          | $18-45    | $8-25     | $3.50-12   | $4,000-12,000

Note: Wide ranges reflect geographic, class, and age variation.
Use local BOMA/IREM data for specific market benchmarks.
```

### Variance Thresholds

```yaml
variance_flags:
  year_over_year_increase:
    normal: "<5%"
    investigate: "5-10%"
    red_flag: ">10%"
  budget_vs_actual:
    normal: "+/- 5%"
    investigate: "+/- 5-15%"
    red_flag: ">15% over budget"
  benchmark_comparison:
    normal: "Within 20% of benchmark median"
    investigate: "20-50% above median"
    red_flag: ">50% above median"
```
