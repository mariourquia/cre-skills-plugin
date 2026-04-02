# Opportunity Zone Benefit Calculations Reference

Complete OZ benefit mechanics, compliance tests, and after-tax IRR differentials. Worked example: $2M capital gains invested into a Qualified Opportunity Zone tract in Jersey City, NJ.

---

## 1. Three OZ Benefits

### Benefit 1: Tax Deferral on Original Gain

Capital gains invested in a Qualified Opportunity Fund (QOF) within 180 days of realization are deferred until the earlier of:
- Sale or exchange of the QOF investment
- December 31, 2026 (statutory recognition date)

```
Deferral formula:
  Tax deferred = recognized_gain * capital_gains_rate
  Time value of deferral = deferred_tax * [(1 + r)^t - 1]

  where r = investor's opportunity cost of capital, t = years of deferral

Example:
  $2,000,000 gain recognized June 2025
  Federal LTCG rate: 20% + 3.8% NIIT = 23.8%
  Tax deferred: $2,000,000 * 23.8% = $476,000

  Deferral period: June 2025 to December 2026 = 1.5 years
  At 8% opportunity cost: $476,000 * [(1.08)^1.5 - 1] = $476,000 * 0.1225 = $58,310

  Time value of deferral benefit: $58,310
```

**Key constraint**: The December 31, 2026 forced recognition date means the deferral benefit is minimal for new investments in 2025-2026. The deferral was far more valuable for investments made in 2018-2021 with 5-8 years of deferral.

### Benefit 2: Step-Up in Basis (EXPIRED)

Originally, the TCJA provided:
- 10% step-up after 5 years of holding the QOF investment
- 15% step-up after 7 years

```
5-year step-up: deferred_gain * 10% reduction = tax savings of gain * 10% * tax_rate
7-year step-up: deferred_gain * 15% reduction = tax savings of gain * 15% * tax_rate
```

**Status as of 2025**: Both step-up deadlines have effectively passed. To achieve the 7-year step-up by December 31, 2026, the investment must have been made by December 31, 2019. The 5-year step-up required investment by December 31, 2021. New investments in 2025 receive NO basis step-up.

For legacy investments made before the deadlines:
```
Example: $2M gain invested December 2019 (7-year step-up eligible)
  Basis step-up: $2,000,000 * 15% = $300,000
  Gain recognized at Dec 31, 2026: $2,000,000 - $300,000 = $1,700,000
  Tax savings: $300,000 * 23.8% = $71,400
```

### Benefit 3: 10-Year Exclusion of QOF Appreciation

If the QOF investment is held for 10+ years, all appreciation in the QOF investment (not the original deferred gain) is excluded from federal income tax upon sale.

```
Exclusion formula:
  Taxable gain on QOF = $0 (if held 10+ years)
  Tax savings = QOF_appreciation * capital_gains_rate

Example:
  $2,000,000 invested in QOF in 2025
  QOF value after 10 years (2035): $5,500,000
  QOF appreciation: $5,500,000 - $2,000,000 = $3,500,000

  Tax excluded: $3,500,000 * 23.8% = $833,000

  This is the primary remaining benefit for new OZ investments.
```

**Important**: The 10-year exclusion applies only to appreciation in the QOF investment itself. The original deferred gain is still recognized (at December 31, 2026 or earlier sale). The exclusion is available for investments through December 31, 2047 (current statutory sunset).

---

## 2. QOZB Compliance Tests

### Qualified Opportunity Zone Business (QOZB) Requirements

A QOF must hold at least 90% of its assets in Qualified OZ Property (QOZP). If the QOF invests through a subsidiary, that subsidiary must be a QOZB meeting:

| Test | Requirement | Measurement |
|---|---|---|
| 70% tangible property test | >= 70% of tangible property owned/leased is QOZP | Semi-annual (June 30, Dec 31) |
| 50% gross income test | >= 50% of gross income derived from active business in the OZ | Annual |
| Nonqualified financial property | < 5% of average aggregate assets | Semi-annual |
| Sin business exclusion | No golf courses, country clubs, massage parlors, hot tub facilities, suntan facilities, racetracks, gambling, or liquor stores | Ongoing |
| Substantial business functions | Substantial portion of intangible property used in OZ | Ongoing |

### 90% Asset Test for QOF

```
QOF 90% test:
  (QOZP + QOZB_stock/partnership_interests) / total_QOF_assets >= 90%

  Tested semi-annually (June 30 and December 31)
  Penalty for failure: (shortfall * federal short-term rate * 1.5) / 12 per month of non-compliance
  Penalty is self-assessed on Form 8996
```

### Working Capital Safe Harbor

A QOZB may hold working capital (cash, cash equivalents) in excess of the 5% nonqualified financial property limit if:

```
1. Written schedule designating use of working capital for acquisition, construction, or substantial improvement of tangible property in the OZ
2. Working capital must be spent within 31 months per the schedule
3. The business must comply with the schedule
4. COVID extension: 24-month safe harbor extensions were available (now expired for new investments)
```

---

## 3. Substantial Improvement Test

### Rule

Tangible property purchased from an unrelated party (existing buildings) must be substantially improved within 30 months of acquisition. Substantial improvement means the QOF/QOZB must invest an amount equal to or exceeding the adjusted basis of the PURCHASED PROPERTY (excluding land) in improvements.

```
Substantial improvement test:
  Improvements_within_30_months >= adjusted_basis_of_purchased_building

  Note: Land is EXCLUDED from the basis calculation. Only the building's adjusted basis
  must be doubled. This is a critical planning point.
```

### Worked Example: Jersey City OZ Acquisition

```
Purchase price: $4,000,000
  Land value: $1,200,000 (30%)
  Building value: $2,800,000 (70%)

Substantial improvement required: $2,800,000 within 30 months of acquisition

Improvement budget:
  Hard costs (renovation):       $2,200,000
  Soft costs (architecture, engineering, permits): $350,000
  FF&E (if capitalized):         $300,000
  Total qualifying improvements: $2,850,000

  $2,850,000 >= $2,800,000 -> TEST PASSED

Timeline:
  Acquisition: March 2025
  30-month deadline: September 2027
  Must have $2,800,000 in capitalized improvements placed in service by September 2027
```

### Land Basis Trick

If land represents a high percentage of purchase price (common in high-value urban OZs like Jersey City), the improvement threshold is lower:

```
Scenario A: 30% land ($1.2M land, $2.8M building) -> improve by $2.8M
Scenario B: 50% land ($2.0M land, $2.0M building) -> improve by $2.0M
Scenario C: 70% land ($2.8M land, $1.2M building) -> improve by $1.2M

Higher land ratio = lower improvement threshold = easier compliance
```

### Original Use Exception

If the QOF/QOZB is the first user of the property (new construction on vacant land, or substantially vacant building), the substantial improvement test does NOT apply.

```
Original use:
  - New construction: no improvement test (building placed in service for first time)
  - Vacant building (abandoned for 5+ years per safe harbor): treated as original use
  - Substantially vacant: building where >80% of usable square footage was unused for 1+ year
```

---

## 4. After-Tax IRR Differential: OZ vs. Non-OZ

### Setup: $2M Gain Invested in Jersey City OZ

**Assumptions:**
- Gain recognized: $2,000,000 (June 2025)
- 180-day investment deadline: December 2025
- Investment vehicle: QOF investing in multifamily development in JC OZ tract
- Total project cost: $4,000,000 ($2M QOF equity + $2M construction loan)
- Hold period: 10 years (required for exclusion benefit)
- Project-level IRR (unlevered, pre-tax): 12%
- Federal tax rate: 23.8% (LTCG + NIIT)
- State tax rate (NJ): 10.75%
- Combined effective rate: ~32% (with some offset for state deduction)

### Scenario A: Non-OZ Investment (Taxable)

```
Step 1: Pay tax on $2M gain immediately
  Federal: $2,000,000 * 23.8% = $476,000
  NJ state: $2,000,000 * 10.75% = $215,000
  Total tax year 0: $691,000

Step 2: Net investable capital
  $2,000,000 - $691,000 = $1,309,000

Step 3: Invest $1,309,000 at 12% pre-tax for 10 years
  Terminal value (pre-tax): $1,309,000 * (1.12)^10 = $4,065,262

Step 4: Tax on appreciation at exit
  Gain: $4,065,262 - $1,309,000 = $2,756,262
  Tax (32%): $881,924

Step 5: After-tax terminal value
  $4,065,262 - $881,924 = $3,183,338

Step 6: After-tax IRR (on original $2M)
  $2,000,000 -> $3,183,338 over 10 years
  IRR = (3,183,338 / 2,000,000)^(1/10) - 1 = 4.77%
```

### Scenario B: OZ Investment (QOF)

```
Step 1: Defer tax on $2M gain (invested in QOF by December 2025)
  No tax paid in 2025
  Full $2,000,000 invested

Step 2: Tax on deferred gain recognized December 31, 2026
  Federal: $2,000,000 * 23.8% = $476,000
  NJ state: $2,000,000 * 10.75% = $215,000
  Total deferred gain tax (paid April 2027): $691,000
  PV of deferred tax (at 8%, 1.75 years from investment): $691,000 / 1.08^1.75 = $601,174

Step 3: Invest full $2,000,000 at 12% pre-tax for 10 years
  Terminal value (pre-tax): $2,000,000 * (1.12)^10 = $6,211,696

Step 4: Tax on QOF appreciation at exit (10+ year hold = EXCLUDED)
  Federal tax on appreciation: $0 (10-year exclusion)
  NJ state tax on appreciation: varies by state conformity
    NJ partially conforms to OZ provisions. Assume state exclusion applies.
  Tax on appreciation: $0

Step 5: After-tax terminal value
  $6,211,696 - $0 (appreciation excluded) = $6,211,696
  Less: deferred gain tax already paid ($691,000 in 2027, already accounted for separately)

Step 6: After-tax IRR (on original $2M, accounting for deferred gain tax outflow)
  Year 0: -$2,000,000 (invested in QOF)
  Year 1.75: -$691,000 (deferred gain tax paid April 2027)
  Year 10: +$6,211,696

  Solving for XIRR:
  NPV(r) = -2,000,000 + (-691,000)/(1+r)^1.75 + 6,211,696/(1+r)^10 = 0

  Iterating:
  At r=10%: NPV = -2,000,000 - 591,645 + 2,394,519 = -197,126
  At r=9%:  NPV = -2,000,000 - 597,580 + 2,619,798 = +22,218
  Converges to XIRR = 9.10%
```

### IRR Differential Summary

| Metric | Non-OZ (Taxable) | OZ (QOF, 10-Year Hold) | Differential |
|---|---|---|---|
| Capital invested | $2,000,000 | $2,000,000 | -- |
| Net capital deployed | $1,309,000 | $2,000,000 | +$691,000 (deferred tax deployed) |
| Terminal value (pre-tax) | $4,065,262 | $6,211,696 | +$2,146,434 |
| Tax on appreciation | $881,924 | $0 | -$881,924 |
| Deferred gain tax | $0 (paid upfront) | $691,000 (paid yr 1.75) | +$691,000 (timing shift) |
| After-tax terminal value | $3,183,338 | $5,520,696 | +$2,337,358 |
| After-tax IRR | 4.77% | 9.10% | +433bp |
| After-tax equity multiple | 1.59x | 2.76x | +1.17x |

The OZ investment delivers 433bp of incremental after-tax IRR, driven primarily by the 10-year exclusion of $4.2M in appreciation. The deferral benefit is relatively minor given the short deferral window (through Dec 2026).

---

## 5. Sensitivity Analysis

### IRR Differential by Pre-Tax Project Return

| Pre-Tax Project IRR | Non-OZ After-Tax IRR | OZ After-Tax IRR | Differential |
|---|---|---|---|
| 8% | 2.94% | 6.08% | +314bp |
| 10% | 3.85% | 7.58% | +373bp |
| 12% | 4.77% | 9.10% | +433bp |
| 15% | 6.17% | 11.43% | +526bp |
| 18% | 7.57% | 13.79% | +622bp |

The OZ benefit increases with higher project returns because the 10-year exclusion shelters a larger absolute gain. For low-return projects (<8%), the OZ benefit may not justify the 10-year hold requirement and compliance burden.

### IRR Differential by Hold Period

| Hold Period | Non-OZ After-Tax IRR | OZ After-Tax IRR | Differential | Notes |
|---|---|---|---|---|
| 5 years | 4.77% | 4.89% | +12bp | No 10-year exclusion; only deferral benefit |
| 7 years | 4.77% | 5.52% | +75bp | No 10-year exclusion; deferral benefit |
| 10 years | 4.77% | 9.10% | +433bp | Full 10-year exclusion activated |
| 12 years | 4.77% | 9.43% | +466bp | Exclusion + additional compounding |
| 15 years | 4.77% | 9.72% | +495bp | Exclusion + additional compounding |

The discontinuity at year 10 is dramatic. Selling in year 9 instead of year 10 forfeits virtually the entire OZ benefit.

---

## 6. State Tax Conformity (Selected States)

| State | OZ Deferral | OZ Basis Step-Up | OZ 10-Year Exclusion | Notes |
|---|---|---|---|---|
| New Jersey | Yes (partial) | N/A (expired) | Yes (legislation enacted) | NJ has state-designated OZs with additional benefits |
| New York | Yes | N/A | Yes | Full conformity to federal provisions |
| California | No | No | No | CA does not conform to any OZ provisions |
| Connecticut | Yes | N/A | Yes | Full conformity |
| Pennsylvania | Yes | N/A | Yes | Full conformity |
| Florida | N/A (no state income tax) | N/A | N/A | Federal benefits apply; no state layer |
| Texas | N/A (no state income tax) | N/A | N/A | Federal benefits apply; no state layer |

California non-conformity is a major consideration for CA-resident investors: the 10-year exclusion provides zero state benefit, and CA's 13.3% top rate on capital gains significantly reduces the net benefit.

---

## 7. Common Errors

| Error | Consequence |
|---|---|
| Assuming basis step-up is still available for new investments | Step-up deadlines passed (5-year by Dec 2021, 7-year by Dec 2019); new 2025 investments get zero step-up |
| Selling in year 9 instead of 10 | Forfeits the entire 10-year exclusion; all QOF appreciation becomes taxable |
| Ignoring the Dec 2026 forced gain recognition | Deferred gain is recognized regardless of whether the QOF investment is sold; investor must plan for tax liability in 2026 |
| Failing the 90% asset test | Penalty assessed monthly; repeated failure can disqualify the QOF entirely |
| Including land in the substantial improvement calculation | Only building basis must be doubled; including land inflates the required improvement amount unnecessarily |
| Assuming state conformity without verification | California, Mississippi, and others do not conform; state tax benefits may be zero |
| Treating OZ as a pure tax play | The 10-year hold requirement and compliance costs mean the underlying investment must generate competitive returns on its own merits; a bad deal in an OZ is still a bad deal |
| Investing non-qualifying gains | Only capital gains (not ordinary income) qualify for OZ deferral; Section 1231 gains qualify, but Section 1245 recapture (ordinary) does not |
