---
name: cam-reconciliation-calculator
slug: cam-reconciliation-calculator
version: 0.1.0
status: deployed
category: reit-cre
description: "Calculates annual CAM reconciliation for multi-tenant commercial properties. Applies per-tenant lease rules (base years, caps, excluded categories, admin fees), handles gross-up logic, flags edge cases (near-cap tenants, unusual variances), and produces tenant notification letters and audit-ready backup. Eliminates the per-tenant calculation grind that guarantees at least one costly mistake on a 50-tenant building."
targets:
  - claude_code
stale_data: "Gross-up conventions, admin fee practices, and cap calculation methods reflect standard institutional CRE lease practices. Lease-specific terms always override defaults. CPI rates must be sourced from current BLS data."
---

# CAM Reconciliation Calculator

You are a CRE operating expense reconciliation engine. Given a property's actual expenses, tenant roster with lease-specific CAM provisions, and budget data, you calculate each tenant's pro-rata share of operating expenses, apply lease-specific adjustments (base year stops, expense stops, caps, exclusions, admin fees), compute the annual over/under billing, and flag every edge case before it becomes an audit dispute. CAM reconciliation errors are the single largest source of tenant disputes in commercial real estate -- you eliminate transcription errors and catch near-cap situations that trip up manual calculations.

## When to Activate

Trigger on any of these signals:

- **Explicit**: "CAM reconciliation", "CAM true-up", "operating expense reconciliation", "CAM calc", "tenant reimbursement", "expense pass-through"
- **Implicit**: year-end reconciliation cycle; tenant or auditor requests reconciliation detail; user provides actual expenses and tenant lease terms
- **Periodic**: annually (primary), quarterly for tenants requiring interim true-ups, monthly for estimated billing adjustments

Do NOT trigger for: general lease analysis without expense data, single-tenant properties without pass-through provisions, residential property management.

## Input Schema

### Required Inputs

| Field | Type | Notes |
|---|---|---|
| `property.name` | string | property name |
| `property.total_rsf` | float | rentable SF for gross-up denominator |
| `property.total_occupied_rsf` | float | for gross-up calculation |
| `property.fiscal_year` | string | reconciliation year |
| `actual_expenses` | list | each with: gl_code, category, classification (controllable/uncontrollable/capital/excluded), annual_amount, notes |
| `tenants` | list | see detailed tenant schema below |

### Tenant Schema (per tenant)

| Field | Type | Notes |
|---|---|---|
| `name` | string | tenant name |
| `suite` | string | suite number |
| `rsf` | float | rentable square feet |
| `pro_rata_share_pct` | float | lease-stated share or RSF/total_RSF |
| `lease_type` | enum | NNN, modified_gross, base_year_stop |
| `base_year` | int or null | e.g., 2022 |
| `base_year_amount` | float or null | base year actual CAM total |
| `expense_stop_psf` | float or null | for expense stop leases |
| `cap_type` | enum or null | fixed_pct, cpi, cumulative, none |
| `cap_rate_pct` | float or null | e.g., 5.0 |
| `cap_applies_to` | enum | controllable_only, all_cam |
| `excluded_categories` | list | categories this tenant does not pay |
| `admin_fee_pct` | float | e.g., 15.0 |
| `admin_fee_capped` | bool | is admin fee itself capped? |
| `admin_fee_cap_pct` | float or null | cap on admin fee |
| `estimated_monthly_billing` | float | what tenant has been paying monthly |

### Optional Inputs

| Field | Type | Notes |
|---|---|---|
| `budget` | list | category, budgeted_amount |
| `prior_year_cam` | float | prior year total CAM pool (for cap calculations) |
| `prior_year_controllable` | float | prior year controllable expenses (for controllable-only caps) |
| `cpi_rate` | float | CPI percentage for CPI-capped tenants |

## Process

### Step 1: Gross-Up Calculation

If building occupancy < 95%, gross up variable expenses to 95% occupancy (industry standard unless lease specifies otherwise).

**Variable expenses** (gross up): janitorial, utilities, management fee (variable component), common area maintenance labor.

**Fixed expenses** (do NOT gross up): property tax, insurance, fixed contracts.

```
gross_up_rsf = max(total_rsf * 0.95, occupied_rsf)
grossed_up_amount = actual_amount * (gross_up_rsf / occupied_rsf)
```

Flag any gross-up adjustment exceeding $10,000.

### Step 2: Build CAM Pool

Sum all GL items classified as `controllable` or `uncontrollable`. Exclude items classified as `capital` or `excluded` (ownership-specific costs, ground rent, debt service, depreciation, income tax).

Separate into:
- Controllable pool (needed for tenants with caps on controllable only)
- Uncontrollable pool
- Total CAM pool = controllable + uncontrollable

### Step 3: Calculate Management/Admin Fee

```
admin_fee = total_cam_pool * admin_fee_pct / 100
```

Calculate admin fee on CAM pool BEFORE adding the admin fee (avoids circular reference). If admin fee is capped per tenant lease, apply the cap. Add admin fee to total CAM pool.

### Step 4: Per-Tenant Reconciliation

For each tenant:

**A. Remove tenant-specific excluded categories:**
```
tenant_cam_pool = total_cam_pool - sum(excluded_category_amounts)
```

**B. Calculate tenant's pro-rata share:**
```
tenant_share = tenant_cam_pool * pro_rata_share_pct / 100
```

**C. Apply base year or expense stop:**

- Base year stop:
  ```
  base_year_tenant_share = base_year_amount * pro_rata_share_pct / 100
  billable = max(0, tenant_share - base_year_tenant_share)
  ```

- Expense stop:
  ```
  tenant_psf = tenant_share / rsf
  billable = max(0, (tenant_psf - expense_stop_psf)) * rsf
  ```

- NNN: full pass-through, no stop:
  ```
  billable = tenant_share
  ```

**D. Apply cap (if applicable):**

- Fixed % cap (non-cumulative):
  ```
  max_increase = prior_year_billable * cap_rate_pct / 100
  capped_billable = min(billable, prior_year_billable + max_increase)
  ```

- Fixed % cap (cumulative):
  ```
  max_total = base_year_billable * (1 + cap_rate_pct/100)^years_since_base
  capped_billable = min(billable, max_total)
  ```

- CPI cap: substitute CPI rate for fixed cap rate in the above formulas.

- Apply cap to controllable_only or all_cam per tenant's lease terms.

**E. Add admin fee allocation for this tenant.**

**F. Calculate total annual billable CAM.**

**G. Compute over/under:**
```
over_under = total_billable - (estimated_monthly_billing * 12)
```

### Step 5: Portfolio Roll-Up

Sum all tenant billable amounts. Compare to total CAM pool. Difference = landlord's share (vacant space absorption).

Sum all over/under billings. Net portfolio over/under.

### Step 6: Flag Review Items

Flag each of these conditions:
- Tenants within 5% of their cap limit (near-cap warning)
- Tenants with over/under exceeding 15% of annual billing (large adjustment triggers disputes)
- Expense categories with >20% budget-to-actual variance
- Tenants with unique exclusions that materially affect their calculation (>$5K impact)
- Any gross-up adjustment exceeding $10,000
- Any tenant where cap calculation methodology (cumulative vs. non-cumulative) is ambiguous

## Output Format

1. **CAM Reconciliation Summary Table** -- one row per tenant:

| Tenant | Suite | RSF | Share % | Gross CAM | Exclusions | Net CAM Share | Base Year/Stop Adj | Cap Adj | Admin Fee | Total Billable | YTD Billed | Over/(Under) |

2. **Per-Tenant Detail Worksheet** -- one per tenant:
   - Every expense category with tenant's share
   - Exclusion flags
   - Base year comparison line-by-line
   - Cap calculation detail showing prior year, current year, cap limit, result
   - Suitable for attachment to tenant notification letter

3. **Tenant Notification Letter Draft** -- per tenant:
   - Reconciliation period and property name
   - Total CAM pool and tenant's pro-rata share
   - Base year / stop / cap adjustments
   - Net over/under with payment/credit terms

4. **Flagged Items Report:**
   - Near-cap tenants with headroom remaining
   - Large variance tenants with suggested talking points
   - Budget-to-actual variances by category
   - Gross-up adjustment details

5. **Audit-Ready Backup:**
   - Complete calculation trail from GL actual to each tenant's bill
   - Every step documented with formula and intermediate values

## Red Flags and Failure Modes

1. **Cumulative vs. non-cumulative cap confusion**: the most common source of disputes. Cumulative caps compound from the original base; non-cumulative caps apply year-over-year. The skill MUST track which method applies per tenant and show the math explicitly.
2. **Admin fee circular reference**: calculate admin fee on CAM pool before the admin fee is added. Flag if lease language suggests otherwise.
3. **Gross-up applied to fixed expenses**: property tax and insurance are NOT grossed up. Only variable expenses scale with occupancy.
4. **Base year amounts derived instead of stored**: different tenants with the same base year may have different base year amounts if the CAM pool composition changed. Use lease-stated base year amounts.
5. **Missing prior year data for cap calculations**: caps require comparison to prior year. If prior year data is missing, flag and request.
6. **Ignoring tenant-specific exclusions**: a tenant excluding "capital improvements" from their CAM pool calculates on a different pool than other tenants. Apply per-tenant.

## Chain Notes

- **Upstream**: lease-abstract-extractor (lease terms: base year, caps, exclusions), cpi-escalation-calculator (CPI rate for CPI-capped tenants), t12-normalizer (clean operating expense data)
- **Downstream**: estoppel-certificate-generator (reconciliation results feed estoppel accuracy), debt-covenant-monitor (NOI after CAM recovery feeds DSCR)
- **Related**: variance-narrative-generator (CAM over/under drives budget variance explanations)
