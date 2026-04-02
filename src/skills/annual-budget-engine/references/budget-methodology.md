# CRE Annual Budget Methodology Reference

Component-specific escalation frameworks, zero-based vs trend approaches, and NOI/SF benchmarking for institutional asset management. Worked example uses a 200-unit Class B multifamily in a secondary metro.

---

## 1. Escalation Framework by Line Item

### Why Component-Specific Escalators Matter

Applying a blanket 3% growth assumption to all opex lines is the single most common budgeting error in institutional CRE. Insurance, property taxes, and utilities follow entirely different cost drivers. A blanket escalator will understate volatile lines and overstate stable ones, producing a budget that is "right on average" but wrong everywhere.

### Component Escalator Sources

| Line Item | Escalation Driver | Source | 2024-2026 Trend |
|---|---|---|---|
| Insurance | CAT loss experience, reinsurance market | CIAB Commercial P&C Market Index | +8-15% coastal, +3-6% inland |
| Property tax | Reassessment cycle, millage rate changes | County assessor + state equalization | +2-5% typical, +15-30% post-acquisition |
| R&M labor | BLS Employment Cost Index (ECI), CPI-W | BLS series CIS2020000000000I | +4.0-5.5% annually |
| R&M materials | PPI for building materials | BLS series WPU13 | +2-4% (normalizing from 2021-22 spike) |
| Utilities - electric | Utility rate case filings, EIA | EIA Short-Term Energy Outlook | +3-6% (grid investment pass-through) |
| Utilities - gas | Henry Hub forward curve, delivery charges | EIA STEO, utility tariff filings | +0-3% (demand decline in warm regions) |
| Utilities - water/sewer | Municipal infrastructure cost recovery | Local utility rate orders | +5-8% (infrastructure deficit catch-up) |
| Payroll | BLS ECI + benefits inflation | BLS CIS series, Kaiser Family Foundation | +4-6% total comp |
| Management fee | % of EGI (contractual) | Management agreement | Scales with revenue, not cost inflation |
| Marketing/turnover | Submarket vacancy, turnover rate | Lease trade-outs, RealPage/CoStar | Countercyclical: rises when vacancy rises |
| Contract services | CPI-U services component + local labor | BLS CPI-U, vendor bids | +3-5% |
| Admin/G&A | CPI-U, technology costs | BLS CPI-U | +2-4% |

### Insurance Deep Dive

Insurance is the most volatile opex line. The CIAB (Council of Insurance Agents & Brokers) quarterly survey is the institutional benchmark.

```
Premium escalation methodology:
1. Start with prior-year actual premium
2. Apply CIAB market trend for property type and region
3. Adjust for property-specific loss history (3-year claims ratio)
4. Adjust for TIV (total insurable value) change if improvements made
5. Add any new coverage requirements (e.g., flood zone reclassification)

Example:
  Prior year premium: $180,000
  CIAB coastal MF trend: +12%
  Property loss ratio (3yr avg): 45% (favorable vs 60% class average)
  Loss history credit: -3%
  Net escalation: +12% - 3% = +9%
  Budget: $180,000 * 1.09 = $196,200
```

### Property Tax Escalation

Property taxes follow a fundamentally different pattern than other opex -- they are event-driven (reassessment upon sale) rather than inflation-driven.

```
Tax escalation methodology:
1. Determine reassessment trigger
   - Post-acquisition: assessed value resets to purchase price (most jurisdictions)
   - Periodic reassessment: county cycle (1-4 years depending on state)
2. Apply millage rate (stable year-to-year, changes require political action)
3. Check for exemptions (LIHTC, abatement, PILOT)

Post-acquisition example:
  Purchase price: $32,000,000
  Prior assessed value: $24,000,000 (seller held 8 years, capped increases)
  Millage rate: 28.5 mills
  Prior tax: $24,000,000 * 0.0285 = $684,000
  Post-reassessment tax: $32,000,000 * 0.0285 = $912,000
  Year 1 increase: +33.3%
  Subsequent years: +2-3% (assessment growth caps in many states)
```

### R&M Escalation (BLS Wage Index Method)

```
R&M budget = labor_component + materials_component

Labor (typically 55-65% of R&M):
  Prior year labor: $142,000
  BLS ECI for maintenance workers: +4.8%
  Budget: $142,000 * 1.048 = $148,816

Materials (35-45% of R&M):
  Prior year materials: $98,000
  PPI building materials: +3.2%
  Budget: $98,000 * 1.032 = $101,136

Total R&M: $148,816 + $101,136 = $249,952
vs. blanket 3% escalation: ($142,000 + $98,000) * 1.03 = $247,200
Difference: $2,752 -- small here, but compounds and is larger in high-labor markets
```

---

## 2. Zero-Based vs Trend Budgeting

### Trend Budgeting

```
Line_item_budget = prior_year_actual * (1 + escalation_rate)
```

Appropriate when: property is stabilized, no operational changes, no major contract renewals, no capital events.

Risk: embeds prior-year inefficiencies. If the prior year had a $15K plumbing emergency coded to R&M, trend budgeting escalates that one-time cost into the permanent baseline.

### Zero-Based Budgeting (ZBB)

Every line item is rebuilt from scratch each year using bottom-up unit costs.

```
Line_item_budget = unit_count * unit_cost * frequency

Example -- turnover costs:
  Expected turnovers: 200 units * 45% turnover rate = 90 units
  Cost per turn:
    Paint: $650
    Clean: $350
    Carpet/flooring allowance: $400
    Appliance touch-up: $150
    Make-ready labor: $250
  Cost per turn: $1,800
  Total turnover budget: 90 * $1,800 = $162,000
```

### Hybrid Approach (Institutional Standard)

Use ZBB for the 5-6 lines that represent 75-80% of controllable opex:
- Payroll (rebuild from staffing plan)
- R&M (rebuild from unit economics + deferred maintenance schedule)
- Turnover (rebuild from projected turnover rate)
- Contract services (rebuild from vendor contract terms)
- Marketing (rebuild from vacancy forecast and cost-per-lease)

Use trend for the remaining 10-15 small lines (admin, licenses, legal, miscellaneous).

---

## 3. NOI/SF Benchmarking

### Sources

| Source | Coverage | Metric Basis | Update Frequency |
|---|---|---|---|
| IREM Income/Expense Analysis | National, by MSA and property type | Per unit and per SF | Annual |
| BOMA Experience Exchange | Office-focused | Per SF (rentable) | Annual |
| NAA Survey of Operating Income & Expenses | Multifamily only | Per unit | Annual |
| RealPage/Yardi benchmarking | Client portfolios | Per unit | Quarterly |

### Benchmark Comparison Method

```
Step 1: Normalize property data to per-unit and per-SF basis
Step 2: Identify IREM comp set (same MSA, same vintage, same unit count range)
Step 3: Compare each line item to IREM median and quartile range
Step 4: Flag any line >15% above IREM median for investigation
Step 5: Document justification for outliers (e.g., "insurance 20% above median due to coastal exposure")
```

### Typical Opex Ranges (Class B Multifamily, Secondary Metro, 2025)

| Line Item | Per Unit/Year | % of EGI | IREM Median Reference |
|---|---|---|---|
| Payroll | $1,200-1,800 | 8-12% | $1,450 |
| R&M | $1,000-1,600 | 7-11% | $1,250 |
| Insurance | $600-1,200 | 4-8% | $850 |
| Property tax | $1,200-2,400 | 8-16% | varies by state |
| Utilities | $800-1,400 | 5-9% | $1,050 |
| Management fee | 3-5% of EGI | 3-5% | 4.0% |
| Marketing/turnover | $400-800 | 3-5% | $550 |
| Contract services | $500-900 | 3-6% | $650 |
| Admin/G&A | $300-600 | 2-4% | $400 |
| **Total controllable** | **$6,000-10,000** | **40-55%** | **$7,500** |

---

## 4. Worked Line-Item Budget: 200-Unit Class B Multifamily

### Property Profile

```
Units: 200 (mix: 80 1BR, 100 2BR, 20 3BR)
Average SF: 925
Location: Raleigh-Durham MSA (secondary metro, no coastal exposure)
Year built: 2008
Avg in-place rent: $1,475/unit/month
Market rent: $1,525/unit/month (3.4% loss-to-lease)
Physical occupancy: 94%
Turnover rate: 48%
Prior year actuals available
```

### Revenue Build

```
Gross potential rent (GPR):
  200 units * $1,525/mo * 12 = $3,660,000

Loss to lease:
  200 units * ($1,525 - $1,475) * 12 * 0.94 occupancy = -$112,800
  As % of GPR: -3.1%

Vacancy & credit loss:
  Physical vacancy: 6% * $3,660,000 = -$219,600
  Bad debt: 1.5% of collected revenue = -$51,606
  Total V&C: -$271,206 (7.4% of GPR)

Other income:
  Pet rent: 120 units * $35/mo * 12 = $50,400
  Parking: 40 premium spots * $75/mo * 12 = $36,000
  Late fees: $18,000
  Application fees: $12,000
  Utility reimbursement (RUBS): 188 occupied * $45/mo * 12 = $101,520
  Total other income: $217,920

Effective gross income (EGI):
  $3,660,000 - $112,800 - $271,206 + $217,920 = $3,493,914
```

### Operating Expense Build (Hybrid ZBB)

```
1. Payroll (ZBB -- staffing plan):
   Property manager (1): $68,000 + 28% benefits = $87,040
   Asst manager (1): $48,000 + 28% = $61,440
   Leasing agent (1): $42,000 + 25% = $52,500
   Maintenance tech (2): $52,000 * 2 + 30% = $135,200
   Porter (1): $36,000 + 22% = $43,920
   Total payroll: $380,100 ($1,901/unit)
   Escalation: +4.5% (BLS ECI) = $397,205

2. R&M (ZBB -- unit economics):
   Routine (per unit): $650/unit * 200 = $130,000
   Turnover make-ready: 96 turns * $1,800 = $172,800
   Common area: $45,000
   Snow/seasonal: $18,000
   Total R&M: $365,800 ($1,829/unit)

3. Insurance (CIAB trend):
   Prior year: $156,000
   CIAB inland MF trend: +6%
   Loss history: favorable (-1.5%)
   Budget: $156,000 * 1.045 = $163,020 ($815/unit)

4. Property tax (reassessment):
   Prior year: $412,000
   No acquisition trigger (held 3 years)
   County reassessment: +3.2%
   Budget: $412,000 * 1.032 = $425,184 ($2,126/unit)

5. Utilities:
   Electric (common area + HVAC): $142,000 * 1.05 = $149,100
   Gas: $38,000 * 1.02 = $38,760
   Water/sewer: $118,000 * 1.06 = $125,080
   Trash: $42,000 * 1.04 = $43,680
   Total utilities: $356,620 ($1,783/unit)

6. Management fee:
   4.0% of EGI = $3,493,914 * 0.04 = $139,757

7. Marketing:
   Cost per lease: $350 * 96 new leases = $33,600
   Digital/ILS: $2,200/month * 12 = $26,400
   Signage/collateral: $6,000
   Total marketing: $66,000 ($330/unit)

8. Contract services:
   Landscaping: $48,000
   Pest control: $18,000
   Elevator maintenance: $9,600
   Fire/life safety: $7,200
   Pool service: $14,400
   Total contracts: $97,200 ($486/unit)

9. Admin/G&A:
   Software (Yardi/RealPage): $24,000
   Legal: $12,000
   Accounting/audit: $8,000
   Office supplies: $4,800
   Licenses/permits: $3,200
   Total admin: $52,000 ($260/unit)
```

### NOI Summary

```
Effective gross income:           $3,493,914
Total operating expenses:        -$2,062,986
  Payroll:          $397,205    (11.4% of EGI)
  R&M:              $365,800    (10.5%)
  Insurance:        $163,020    ( 4.7%)
  Property tax:     $425,184    (12.2%)
  Utilities:        $356,620    (10.2%)
  Management fee:   $139,757    ( 4.0%)
  Marketing:        $66,000     ( 1.9%)
  Contracts:        $97,200     ( 2.8%)
  Admin:            $52,000     ( 1.5%)

Net operating income (NOI):       $1,430,928

NOI/unit:     $7,155
NOI/SF:       $7.74 (200 units * 925 SF = 185,000 SF)
Opex ratio:   59.0%

IREM benchmark NOI/unit (Raleigh Class B): $6,800-7,600
Status: within benchmark range
```

---

## 5. Common Errors

| Error | Impact | Correction |
|---|---|---|
| Blanket 3% escalation on all lines | Understates insurance and tax by 5-15%, overstates stable lines | Use component-specific escalators with named sources |
| Ignoring post-acquisition tax reassessment | Understates Year 1 taxes by 20-40% | Model reassessment to purchase price in acquisition year |
| Using physical occupancy for revenue | Overstates revenue (ignores concessions, free rent, model units) | Use economic occupancy = collected revenue / GPR |
| Budgeting management fee on GPR | Overstates fee (fee is on collected revenue, not gross potential) | Apply fee percentage to EGI per management agreement |
| Missing RUBS/utility reimbursement in other income | Understates revenue by $80-150K on a 200-unit property | Always model utility reimbursement as other income with corresponding utility expense |
| Trend-budgeting turnover costs | Embeds prior year turnover rate, which may not repeat | Zero-base: projected turnover rate * cost per turn |
| Omitting vacancy on other income | Overstates by 4-7% (vacant units do not generate pet rent, parking, etc.) | Apply vacancy factor to unit-linked other income lines |
