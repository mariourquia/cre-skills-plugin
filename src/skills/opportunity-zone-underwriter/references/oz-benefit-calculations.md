# Opportunity Zone Benefit Calculations Reference

Complete OZ benefit mechanics, compliance tests, and after-tax IRR differentials. Two regimes apply, keyed on the QOF investment date. Worked example: $2M capital gains invested into a Qualified Opportunity Zone tract in Jersey City, NJ.

> **Statute basis.** IRC Section 1400Z-2 as amended by the One Big Beautiful Bill Act (OBBBA, enacted 2025-07-04), which made Opportunity Zones permanent. Last verified 2026-06-03. This reference is advisory, not tax or legal advice; confirm with qualified tax counsel and check state conformity.

---

## 0. Two Regimes, Keyed on Investment Date

| | **OZ 1.0 (pre-2027 vintage)** | **OZ 2.0 (post-2026 vintage)** |
|---|---|---|
| Applies to | QOF investments on or before 12/31/2026 | QOF investments after 12/31/2026 |
| Deferred-gain inclusion | Fixed date 12/31/2026 (or earlier inclusion event) | Rolling: 5 years from the investment date (or earlier inclusion event) |
| Basis step-up | 10% at 5-year hold / 15% at 7-year hold -- but only if the hold completes before 12/31/2026, so unreachable for 2022-2026 vintages ($0) | 10% at 5-year hold restored; **30% for a Qualified Rural Opportunity Fund (QROF)**. The 15% step-up was not carried forward |
| Zone designations | Original 2018 map | New map effective 2027-01-01, 10-year term, **decennial** redesignation; prior map overlaps through 12/31/2028 |
| 10-year exclusion | Yes | Yes (unchanged) |

Always classify the vintage before quantifying benefits.

---

## 1. Three OZ Benefits

### Benefit 1: Tax Deferral on Original Gain

Capital gains invested in a Qualified Opportunity Fund (QOF) within 180 days of realization are deferred, with the inclusion date depending on the regime:

- **OZ 1.0**: until the earlier of (i) sale/exchange of the QOF investment, or (ii) **December 31, 2026** (the fixed statutory inclusion date).
- **OZ 2.0**: until the earlier of (i) sale/exchange, or (ii) the **5-year anniversary** of the investment (a rolling clock, no fixed calendar terminus).

```
Deferral formula:
  Tax deferred = recognized_gain * capital_gains_rate
  Time value of deferral = deferred_tax * [(1 + r)^t - 1]

  where r = investor's opportunity cost of capital, t = years of deferral
  OZ 1.0: t = (12/31/2026 - investment_date)
  OZ 2.0: t = 5 (rolling), unless sold earlier

Example (OZ 1.0, early vintage):
  $2,000,000 gain recognized June 2019, invested in a QOF within 180 days
  Federal LTCG rate: 20% + 3.8% NIIT = 23.8%
  Tax deferred: $2,000,000 * 23.8% = $476,000
  Deferral period: ~7.5 years (to 12/31/2026)
  Time value at 8%: $476,000 * [(1.08)^7.5 - 1] = ~$370,000

Example (OZ 2.0, post-2026 vintage):
  $2,000,000 gain invested January 2027
  Tax deferred: $476,000, included on the 5-year anniversary (Jan 2032)
  Time value at 8%: $476,000 * [(1.08)^5 - 1] = $476,000 * 0.4693 = $223,400
```

**Key constraint (OZ 1.0 only)**: a late OZ 1.0 vintage invested near year-end 2026 has only weeks of deferral to the fixed 12/31/2026 date, so the benefit is minimal. The deferral was far more valuable for 2018-2021 vintages with 5-8 years of runway. Under OZ 2.0 the rolling 5-year window restores a meaningful, vintage-independent deferral.

### Benefit 2: Step-Up in Basis of the Deferred Gain

The TCJA (OZ 1.0) provided a 10% step-up after a 5-year hold and a 15% step-up after a 7-year hold, each reducing the deferred gain recognized at inclusion. OBBBA (OZ 2.0) restored a 10% step-up (5-year hold) and added a 30% step-up for Qualified Rural Opportunity Funds; the 15% (7-year) tier was not carried forward.

```
step_up_savings = deferred_gain * step_up_pct * capital_gains_rate

OZ 1.0:
  10% step-up: requires the 5-year hold to complete before 12/31/2026
    -> reachable only for gains invested by 12/31/2021
  15% step-up: requires the 7-year hold to complete before 12/31/2026
    -> reachable only for gains invested by 12/31/2019
  For 2022-2026 vintages, neither is reachable: step_up_pct = 0

OZ 2.0 (investments after 12/31/2026):
  step_up_pct = 0.10 (standard QOF, 5-year hold)
  step_up_pct = 0.30 (Qualified Rural Opportunity Fund, 5-year hold)
  No 15% tier.
```

**Worked step-ups:**
```
OZ 1.0 legacy: $2M gain invested December 2019 (7-year step-up reachable)
  Basis step-up: $2,000,000 * 15% = $300,000
  Gain included at 12/31/2026: $2,000,000 - $300,000 = $1,700,000
  Tax savings: $300,000 * 23.8% = $71,400

OZ 1.0 late vintage: $2M gain invested in 2026
  Neither 5- nor 7-year hold completes before 12/31/2026
  Step-up: $0; full $2,000,000 included at 12/31/2026

OZ 2.0 standard: $2M gain invested January 2027, held 5 years
  Basis step-up: $2,000,000 * 10% = $200,000
  Tax savings: $200,000 * 23.8% = $47,600

OZ 2.0 rural (QROF): $2M gain invested January 2027, held 5 years
  Basis step-up: $2,000,000 * 30% = $600,000
  Tax savings: $600,000 * 23.8% = $142,800
```

Do not state that step-ups "expired." That is accurate only for late OZ 1.0 vintages; OZ 2.0 restores the step-up (and enhances it for rural).

### Benefit 3: 10-Year Exclusion of QOF Appreciation

If the QOF investment is held for 10+ years, all appreciation in the QOF investment (not the original deferred gain) is excluded from federal income tax upon sale.

```
Exclusion formula:
  Taxable gain on QOF = $0 (if held 10+ years)
  Tax savings = QOF_appreciation * capital_gains_rate

Example:
  $2,000,000 invested in QOF
  QOF value after 10 years: $5,500,000
  QOF appreciation: $5,500,000 - $2,000,000 = $3,500,000

  Tax excluded: $3,500,000 * 23.8% = $833,000

  This is the dominant benefit in both OZ 1.0 and OZ 2.0.
```

**Important**: The 10-year exclusion applies only to appreciation in the QOF investment itself; the original deferred gain is still recognized at its inclusion date (OZ 1.0: 12/31/2026 or earlier sale; OZ 2.0: the rolling 5-year anniversary or earlier sale, net of the 10%/30% step-up). Under OBBBA the program is permanent, so the exclusion is no longer tied to a single statutory sunset; eligibility for any given investment depends on the zone designation in force (the post-2026 map runs 2027-01-01 for a 10-year term, redesignated decennially).

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

State conformity to the OBBBA OZ 2.0 amendments lags federal law and must be re-verified per state. Many states couple to the IRC on a rolling basis (and thus pick up OZ 2.0 automatically), others on a fixed/static date (and need legislation), and a few decouple entirely. The table below is the federal-conformity posture as a starting point only.

| State | OZ Deferral | OZ Basis Step-Up | OZ 10-Year Exclusion | Notes |
|---|---|---|---|---|
| New Jersey | Yes (partial) | Follows federal where conformed | Yes (legislation enacted) | NJ has state-designated OZs with additional benefits; confirm OZ 2.0 coupling |
| New York | Yes | Follows federal | Yes | Generally conforms to federal provisions; confirm OZ 2.0 date coupling |
| California | No | No | No | CA does not conform to any OZ provisions (1.0 or 2.0) |
| Connecticut | Yes | Follows federal | Yes | Generally conforms |
| Pennsylvania | Yes | Follows federal | Yes | Generally conforms |
| Florida | N/A (no state income tax) | N/A | N/A | Federal benefits apply; no state layer |
| Texas | N/A (no state income tax) | N/A | N/A | Federal benefits apply; no state layer |

California non-conformity is a major consideration for CA-resident investors: the OZ benefit provides zero state relief, and CA's 13.3% top rate on capital gains significantly reduces the net benefit. Always verify whether the investor's state has conformed to the OBBBA OZ 2.0 amendments for the relevant tax year.

---

## 7. Common Errors

| Error | Consequence |
|---|---|
| Applying the wrong regime's step-up rule | For late OZ 1.0 vintages (2022-2026) the step-up is $0 because the 5-/7-year holds cannot complete before 12/31/2026; for OZ 2.0 (post-2026) the 10% step-up is restored (30% rural QROF). Pin the rule to the investment date, do not blanket-assert step-ups "expired" |
| Selling in year 9 instead of 10 | Forfeits the entire 10-year exclusion; all QOF appreciation becomes taxable |
| Using the fixed 12/31/2026 inclusion date for a post-2026 investment | OZ 2.0 defers on a rolling 5-year clock from the investment date, not to a fixed calendar date; the deferred gain is recognized at the 5-year anniversary (net of the 10%/30% step-up) or earlier sale |
| Failing the 90% asset test | Penalty assessed monthly; repeated failure can disqualify the QOF entirely |
| Including land in the substantial improvement calculation | Only building basis must be doubled; including land inflates the required improvement amount unnecessarily |
| Assuming state conformity without verification | California, Mississippi, and others do not conform; state tax benefits may be zero |
| Treating OZ as a pure tax play | The 10-year hold requirement and compliance costs mean the underlying investment must generate competitive returns on its own merits; a bad deal in an OZ is still a bad deal |
| Investing non-qualifying gains | Only capital gains (not ordinary income) qualify for OZ deferral; Section 1231 gains qualify, but Section 1245 recapture (ordinary) does not |
