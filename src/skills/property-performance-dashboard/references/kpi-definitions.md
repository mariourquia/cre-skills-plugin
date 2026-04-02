# Property Performance KPI Definitions & Formulas

Precise definitions, formulas, and escalation triggers for every KPI used in institutional CRE asset management reporting. Each metric includes the exact calculation, interpretation, and threshold triggers.

---

## 1. Occupancy Metrics

### Physical Occupancy

```
Physical occupancy = occupied_units / total_units

Occupied = unit has a signed lease with a move-in date that has passed and no move-out recorded.
Model units, employee units, and down units (renovation) are excluded from total_units for some
operators. Confirm the denominator convention with the PM.
```

**Threshold triggers:**
- Green: >= 95%
- Yellow: 92-95% (investigate: seasonal or structural?)
- Red: < 92% (escalate: market shift, property condition, or management failure)

### Economic Occupancy

```
Economic occupancy = collected_revenue / gross_potential_rent (GPR)

GPR = total_units * market_rent_per_unit * 12

Economic occupancy < physical occupancy when:
  - Concessions are granted (free rent months)
  - Units are occupied but not paying (delinquency)
  - Loss-to-lease exists (in-place rents below market)
```

**Worked Example:**

```
200 units, market rent $1,525/month
GPR = 200 * $1,525 * 12 = $3,660,000

Collected revenue (annual):
  Gross rent collected: $3,247,200
  (reflects 188 occupied units avg, in-place rents avg $1,475, minus bad debt)

Physical occupancy: 188/200 = 94.0%
Economic occupancy: $3,247,200 / $3,660,000 = 88.7%
Gap: 5.3 percentage points

Gap decomposition:
  Physical vacancy (6.0%): 12 units * $1,525 * 12 / GPR = 5.0%
  Loss-to-lease: ($1,525 - $1,475) * 188 * 12 / GPR = 3.1%
  Bad debt: $51,600 / GPR = 1.4%
  Concessions: $24,000 / GPR = 0.7%
  Total gap drivers: 5.0% + 3.1% + 1.4% + 0.7% = 10.2%
  But net other income offsets some: 88.7% + other_income/GPR reconciles
```

**Threshold triggers (economic occupancy):**
- Green: >= 90%
- Yellow: 85-90%
- Red: < 85%

### Gap Analysis: Physical vs Economic

The physical-to-economic gap is one of the most important diagnostic metrics. A wide gap (>4%) indicates pricing or collection problems, not vacancy problems.

```
If physical occupancy is 94% but economic is 86%:
  - Loss-to-lease is likely 3-5% (rents significantly below market)
  - Bad debt may be elevated (>2% of GPR)
  - Concessions may be excessive

Action: investigate loss-to-lease (run rent comp analysis) and collections waterfall
```

---

## 2. Collections & Delinquency

### Collections Rate

```
Collections rate = cash_collected / total_billed

Monthly basis preferred (not trailing, which smooths problems).
Include late fees collected in numerator. Exclude prepayments.
```

**Threshold triggers:**
- Green: >= 98%
- Yellow: 95-98% (implement formal collections process)
- Red: < 95% (management escalation, consider collections attorney)

### Delinquency Aging

```
Delinquency aging buckets:
  Current (0-30 days): normal payment cycle
  31-60 days: first notice, demand letter
  61-90 days: formal legal notice, payment plan or eviction filing
  90+ days: eviction in process, likely write-off

Delinquency rate = total_delinquent_balance / monthly_billed_revenue

Per-bucket rates:
  Rate_31_60 = balance_31_60 / monthly_billed
  Rate_61_90 = balance_61_90 / monthly_billed
  Rate_90plus = balance_90plus / monthly_billed
```

**Worked Example:**

```
Monthly billed revenue: $278,500

Delinquency report:
  Current (0-30): $262,000 (93.5% -- this is not 'delinquent', it's normal cycle)
  31-60 days: $8,200 (2.9%)
  61-90 days: $4,800 (1.7%)
  90+ days: $3,500 (1.3%)

Total delinquent (31+ days): $16,500
Delinquency rate: $16,500 / $278,500 = 5.9%

Interpretation:
  31-60 is manageable (payment reminders).
  61-90 at 1.7% is elevated -- should have filed demand letters.
  90+ at 1.3% is likely bad debt -- begin eviction process.
  Expected write-off: 60-80% of 90+ bucket = $2,100-2,800/month
```

**Threshold triggers (total delinquency rate, 31+ days):**
- Green: < 3%
- Yellow: 3-6%
- Red: > 6% (systemic collections problem)

---

## 3. Revenue Intensity Metrics

### Rent Per Square Foot

```
In-place rent/SF = (sum of monthly_rent for all occupied units * 12) / total_occupied_SF

Market rent/SF = (market_rent_per_unit * 12) / average_unit_SF

Loss-to-lease/SF = market_rent/SF - in_place_rent/SF
Loss-to-lease % = loss_to_lease/SF / market_rent/SF
```

### Revenue Per Available Unit (RevPAU)

Borrowed from hotel management. Captures both pricing power and occupancy in a single metric.

```
RevPAU = total_collected_revenue / total_units / 12  (monthly)

RevPAU = rent_PSF * occupancy  (equivalent formulation per SF)
```

**Worked Example:**

```
Collected revenue: $3,247,200/year
Total units: 200

RevPAU = $3,247,200 / 200 / 12 = $1,353/unit/month

Compare to:
  Average in-place rent: $1,475/month (occupied units only)
  RevPAU is $122 lower because it includes the vacancy drag

RevPAU is the truest measure of property revenue generation -- it cannot be gamed
by showing high rents on low occupancy or high occupancy at below-market rents.
```

---

## 4. Operating Efficiency

### Opex Ratio

```
Opex ratio = total_operating_expenses / EGI

Controllable opex ratio = controllable_opex / EGI
  Controllable: payroll, R&M, marketing, contracts, admin, mgmt fee
  Non-controllable: property tax, insurance, utilities (rate component)
```

**Benchmark Ranges (Class B MF, Secondary Metro):**

| Metric | Top Quartile | Median | Bottom Quartile |
|---|---|---|---|
| Total opex ratio | < 52% | 55-58% | > 62% |
| Controllable opex ratio | < 24% | 26-29% | > 32% |
| NOI margin | > 48% | 42-45% | < 38% |

### Opex Per Unit

```
Opex/unit = total_operating_expenses / total_units

Useful for cross-property comparison when unit sizes differ significantly.
Normalize to per-SF for office/industrial.
```

---

## 5. NOI Metrics

### Net Operating Income

```
NOI = EGI - operating_expenses

EGI = GPR - vacancy_loss - concessions - bad_debt + other_income

Do NOT deduct below the NOI line:
  - Debt service
  - Capital expenditures
  - Depreciation
  - Income taxes
  - Leasing commissions (office/retail -- debated, but institutional standard is below the line)
```

### Same-Store NOI Growth

```
Same-store NOI growth = (NOI_current_period - NOI_prior_period) / NOI_prior_period

Requirements for "same-store" designation:
  1. Property owned for full 12 months in both periods
  2. No major renovation (>10% of units offline) in either period
  3. No change in unit count (no conversion, demolition, or addition)
```

**Worked Example:**

```
2025 NOI: $1,358,000
2026 NOI (budget): $1,431,000
Same-store NOI growth: ($1,431,000 - $1,358,000) / $1,358,000 = +5.4%

Decomposition:
  Revenue contribution: +$140,000 / $1,358,000 = +10.3% contribution
  Opex increase: -$67,000 / $1,358,000 = -4.9% drag
  Net: +5.4%
```

**Threshold triggers (same-store NOI growth):**
- Green: > 3% (value creation)
- Yellow: 0-3% (flat, investigate)
- Red: < 0% (value destruction -- immediate escalation)

### T-12 Trending

```
T-12 (trailing twelve months) = sum of monthly actuals for the prior 12 months

T-12 NOI is the primary valuation input for income approach appraisals and broker opinions.
It smooths seasonality (utilities, snow removal) but can be dragged by one-time events.

T-12 trending: plot T-12 NOI monthly (each month, drop the oldest month, add the newest).
A rising T-12 trend indicates improving operations; a declining trend signals problems.

Annualized run-rate (alternative to T-12):
  = latest_month_NOI * 12  or  latest_quarter_NOI * 4
  Riskier: does not smooth seasonality. Use only for very recent trajectory analysis.
```

---

## 6. Budget Variance

### Calculation

```
Variance ($) = actual - budget
Variance (%) = (actual - budget) / budget * 100

For revenue lines: positive variance is favorable (collected more than budgeted)
For expense lines: positive variance is unfavorable (spent more than budgeted)

Convention: report unfavorable variances as negative for both revenue and expense
  Revenue unfavorable: actual < budget (report as negative)
  Expense unfavorable: actual > budget (report as negative)
  This ensures all negative numbers are bad, simplifying IC reporting.
```

### Materiality Thresholds

| Line Item | Investigation Trigger | Escalation Trigger |
|---|---|---|
| Total revenue | +/- 2% | +/- 5% |
| Total opex | +/- 3% | +/- 7% |
| NOI | +/- 3% | +/- 5% |
| Any single line | +/- 10% | +/- 20% |
| Controllable opex (aggregate) | +/- 5% | +/- 10% |

### Variance Narrative Framework

Every material variance (exceeding investigation trigger) requires a narrative with three components:

```
1. Root cause: Why did the variance occur? (one sentence)
2. Duration: Is this permanent, temporary, or one-time? (one word + explanation)
3. Corrective action: What is being done? (one sentence with timeline)

Example:
  Line: R&M
  Variance: +$18,000 unfavorable (+12% vs budget)
  Root cause: Two HVAC compressor failures in units 204 and 218 ($6,200 each) plus
    an emergency sewer line repair ($5,400).
  Duration: One-time (equipment failure, not systemic).
  Corrective action: HVAC failures accelerate the compressor replacement program
    (budgeted in Year 2 capex). Sewer repair isolated to Building C; camera inspection
    of remaining lines scheduled for Q2 ($3,500, will add to Q2 forecast).
```

---

## 7. Capital Return Metrics (Property-Level)

### Cash-on-Cash Return (Levered)

```
CoC = annual_before_tax_cash_flow / total_equity_invested

Before-tax cash flow = NOI - debt_service (annual)
Equity = purchase_price + closing_costs + capex reserves - loan_proceeds
```

**Threshold triggers:**
- Green: > 7% (value-add) or > 5% (core)
- Yellow: 4-7% (value-add) or 3-5% (core)
- Red: < 4% (value-add) or < 3% (core)

### DSCR (Debt Service Coverage Ratio)

```
DSCR = NOI / annual_debt_service

Annual debt service = monthly_P&I_payment * 12 (or IO payment * 12 during IO period)
```

**Threshold triggers:**
- Green: > 1.30x
- Yellow: 1.15-1.30x (lender may require cash sweep)
- Red: < 1.15x (covenant breach territory -- immediate escalation)

### Yield on Cost

```
Yield on cost = stabilized_NOI / total_cost_basis

Total cost basis = purchase_price + closing_costs + renovation_capex + carry_costs

This is the "manufactured cap rate" -- the cap rate you created through execution.
Compare to market cap rate: if yield_on_cost > market_cap_rate, you created value.
```

**Worked Example:**

```
Purchase price: $32,000,000
Closing costs: $480,000
Renovation capex: $2,400,000
Carry costs during reno: $180,000
Total cost basis: $35,060,000

Stabilized NOI: $2,100,000

Yield on cost: $2,100,000 / $35,060,000 = 5.99%
Market cap rate: 5.25%
Value at market cap: $2,100,000 / 0.0525 = $40,000,000
Embedded value creation: $40,000,000 - $35,060,000 = $4,940,000
```

---

## 8. Common Errors

| Error | Impact | Correction |
|---|---|---|
| Reporting physical occupancy alone | Hides loss-to-lease, concessions, and bad debt. Property can be 96% occupied and still underperforming on revenue. | Always report both physical and economic occupancy side by side. |
| Using GPR as denominator for opex ratio | Overstates efficiency (GPR is higher than EGI). Institutional standard is EGI. | Opex ratio denominator = EGI, not GPR. |
| Comparing T-12 NOI across properties without normalizing | Properties with different hold periods, renovation timing, or seasonality are not comparable. | Use same-store NOI growth for portfolio comparison. Normalize per unit or per SF for cross-property. |
| Ignoring the physical-to-economic occupancy gap | A 2%+ gap signals pricing or collections issues that physical occupancy masks. | Track and report the gap monthly. Investigate when gap exceeds 4%. |
| Annualizing a strong quarter as "run-rate" | Seasonality in utilities, turnover, and rent concessions can make Q2-Q3 NOI unrepresentative of annual performance. | Use T-12 for valuation. Use annualized run-rate only for very recent trend analysis with a seasonality caveat. |
| Mixing up favorable/unfavorable sign conventions | Confusion about whether positive = good or bad. Different teams use different conventions. | Standardize: negative = unfavorable for ALL lines. Document the convention in the reporting package header. |
| Computing DSCR on budgeted NOI instead of actual | Masks covenant compliance issues. Lender covenants are tested on actual, not budget. | Report DSCR on actual T-12 NOI. Show budgeted DSCR separately as a forecast. |
