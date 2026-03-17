# Proforma Construction Reference

Year-by-year proforma methodology for CRE acquisition underwriting. All examples use a 50-unit multifamily garden property acquired for $12,000,000 with a normalized Year 1 NOI of $720,000 (6.0% going-in cap).

---

## 1. Proforma Architecture

A proforma projects annual cash flows from the normalized T-12 through the hold period plus one forward year (for exit cap valuation). The standard structure:

```
Gross Potential Rent (GPR)
  - Vacancy & Credit Loss
  - Concessions
  + Other Income
= Effective Gross Income (EGI)
  - Operating Expenses
= Net Operating Income (NOI)
  - Debt Service
= Before-Tax Cash Flow (BTCF)
  - Capital Expenditures (funded from reserves or equity)
= Distributable Cash Flow
```

The reversion (sale proceeds) in the terminal year completes the cash flow stream for IRR calculation.

---

## 2. Revenue Assumptions

### Rent Growth

Apply growth to GPR, not to collected rent. Vacancy is applied after growth.

```
GPR_year_n = GPR_year_1 * (1 + g)^(n-1)

where g = annual rent growth rate
```

Typical rent growth assumptions:

| Scenario | Annual Growth | Rationale |
|---|---|---|
| Conservative | 2.0% | Below inflation, stagnant market |
| Base case | 3.0% | Matches long-run CPI + real rent growth |
| Moderate upside | 4.0% | Supply-constrained submarket |
| Aggressive | 5.0%+ | Value-add premium capture, lease-up |

For value-add deals, separate renovated and unrenovated unit growth rates:

```
Unrenovated units: 3.0% annual growth on current rents
Renovated units: Step-up to market rent in renovation year, then 3.0% growth
```

### Vacancy and Credit Loss

```
Vacancy_year_n = GPR_year_n * vacancy_rate

Stabilized vacancy: 5.0% (base case)
Credit loss:        1.0-2.0% additional (non-paying tenants)
Total economic loss: 6.0-7.0% of GPR
```

For lease-up or value-add, model a vacancy glide path:

```
Year 1: 8.0% (renovation disruption)
Year 2: 6.0% (lease-up)
Year 3+: 5.0% (stabilized)
```

### Other Income Growth

Grow ancillary income at a lower rate than rent (typically 2.0%), since parking, laundry, and fee income are less elastic.

---

## 3. Expense Assumptions

### Expense Growth Rates

Not all expenses grow equally. Model by category:

| Expense Category | Growth Rate | Notes |
|---|---|---|
| Real estate taxes | 2.5-3.5% | Jurisdictional; may step up on reassessment |
| Insurance | 5.0-8.0% | Hardening market; higher in coastal |
| Utilities | 3.0-4.0% | Rate schedule increases |
| Payroll | 3.0-4.0% | Wage inflation |
| R&M | 2.5-3.0% | Materials and labor |
| Management fee | Tracks EGI | Percentage of EGI, grows with revenue |
| G&A | 2.0-3.0% | Relatively stable |
| Contracts | 2.0-3.0% | Multi-year contracts may be fixed |

### Management Fee Calculation

```
Mgmt_fee_year_n = EGI_year_n * mgmt_fee_pct

For a 50-unit property: 4.5% of EGI
```

The management fee is a variable expense that grows with revenue, which means expense growth outpaces revenue growth slightly when other fixed expenses also increase. This "expense drag" is a feature, not a bug -- it reflects reality.

---

## 4. Capital Expenditures

### Capex Categories

| Category | Timing | Typical Budget |
|---|---|---|
| Unit renovations | Years 1-3 (value-add) | $8,000-$25,000/unit |
| Common area improvements | Year 1-2 | $1,000-$3,000/unit |
| Roof replacement | Year 3-5 (if needed) | $4-$7/SF |
| HVAC replacement | Staggered | $5,000-$8,000/unit |
| Parking/paving | Year 3-5 | $2-$4/SF |
| Ongoing replacement reserves | Annual | $250-$500/unit/year |

### Replacement Reserves

Lenders require reserves even for stabilized properties:

```
Annual replacement reserve = units * per_unit_reserve
  = 50 * $350 = $17,500/year

This is a below-the-line deduction from NOI to arrive at NCF (net cash flow).
NCF = NOI - replacement_reserves
```

### Value-Add Capex Schedule

For a 20-unit interior renovation at $15,000/unit:

```
Total capex: 20 * $15,000 = $300,000
Year 1: 10 units = $150,000
Year 2: 10 units = $150,000
Year 3+: $0 renovation capex (ongoing reserves only)
```

---

## 5. Debt Service

### Interest-Only vs. Amortizing

```
IO annual debt service = loan_amount * annual_rate
Amortizing annual DS = monthly_payment * 12

where monthly_payment = L * [r(1+r)^n] / [(1+r)^n - 1]
```

### Worked Example

Loan: $7,800,000 (65% LTV) at 6.50%, 30-year amortization, 2-year IO period

```
IO period (Years 1-2):
  Annual DS = $7,800,000 * 0.065 = $507,000

Amortizing period (Years 3-7):
  r = 0.065 / 12 = 0.005417
  n = 360
  (1 + r)^n = (1.005417)^360 = 6.9913
  Monthly = $7,800,000 * [0.005417 * 6.9913] / [6.9913 - 1]
  Monthly = $7,800,000 * 0.037866 / 5.9913
  Monthly = $7,800,000 * 0.006320
  Monthly = $49,296
  Annual DS = $49,296 * 12 = $591,552
```

### Loan Balance at Exit

For a 7-year hold with 2-year IO followed by 5 years of amortization:

```
Remaining amortization periods at exit: 360 - 60 = 300 months
Balance = 49,296 * [1 - (1.005417)^-300] / 0.005417
Balance = 49,296 * [1 - 0.1988] / 0.005417
Balance = 49,296 * 147.91
Balance = $7,291,000

Principal paydown over 5 amortizing years: $7,800,000 - $7,291,000 = $509,000
```

---

## 6. Reversion Calculation

### Exit Cap Rate Selection

The exit cap rate is the single most impactful assumption in the model.

```
Reversion value = NOI_year_(n+1) / exit_cap_rate
Net reversion = reversion_value - selling_costs - loan_balance

Selling costs: 2.0-2.5% of gross reversion (broker, legal, transfer tax)
```

Convention: apply the exit cap to a forward year NOI (Year 8 NOI for a 7-year hold). This is the buyer's going-in yield.

### Exit Cap Spread

```
Exit cap = going_in_cap + expansion_premium

Typical expansion premium: 0 to +50bps (conservative underwriting)
```

Rationale: your exit buyer faces an older property with less remaining useful life. A 10-25bps expansion per hold year is prudent for properties older than 20 years. For newer properties or value-add (where you improved the asset), exit cap may equal or compress below going-in.

---

## 7. Full 7-Year Worked Proforma

### Assumptions Summary

```
Property:         50-unit garden MF, 1995 vintage
Purchase price:   $12,000,000
Going-in cap:     6.0%
Year 1 GPR:       $1,800,000 (50 units * $3,000/mo avg)
Vacancy:          5.0% stabilized
Other income:     $60,000 Year 1 (2.0% growth)
Rent growth:      3.0%/year
Expense ratio:    40% of EGI Year 1 ($720,000 NOI)
Expense growth:   Blended 3.0%/year
Mgmt fee:         4.5% of EGI
Capex:            $300,000 renovation (Y1-Y2), $17,500/year reserves
Loan:             $7,800,000, 6.50%, 30yr amort, 2yr IO
Exit cap:         6.25% (25bps expansion)
Selling costs:    2.0%
Hold period:      7 years
```

### Year-by-Year Projection

```
                        Year 1      Year 2      Year 3      Year 4      Year 5      Year 6      Year 7
REVENUE
Gross Potential Rent  1,800,000   1,854,000   1,909,620   1,966,909   2,025,916   2,086,693   2,149,294
Less: Vacancy (5%)      -90,000     -92,700     -95,481     -98,345    -101,296    -104,335    -107,465
Less: Concessions       -27,000     -18,540     -14,322     -14,752     -15,194     -15,650     -16,120
Other Income             60,000      61,200      62,424      63,672      64,946      66,245      67,570
EGI                   1,743,000   1,803,960   1,862,241   1,917,484   1,974,372   2,032,953   2,093,279

EXPENSES
Management (4.5% EGI)   78,435      81,178      83,801      86,287      88,847      91,483      94,198
Real Estate Taxes       219,300     225,879     232,655     239,635     246,824     254,229     261,856
Insurance                62,500      67,500      72,900      78,732      85,031      91,833      99,180
Utilities                58,320      60,570      62,912      65,349      67,887      70,530      73,284
Payroll                  96,000      99,840     103,834     107,987     112,307     116,799     121,471
R&M                     100,000     103,000     106,090     109,273     112,551     115,927     119,405
G&A                      28,000      28,840      29,705      30,597      31,514      32,460      33,434
Contracts/Other          37,445      38,569      39,726      40,918      42,145      43,410      44,712
Total Expenses          680,000     705,376     731,623     758,778     787,106     816,671     847,540

NOI                   1,063,000   1,098,584   1,130,618   1,158,706   1,187,266   1,216,282   1,245,739

DEBT SERVICE
IO Payment (Y1-2)       507,000     507,000          --          --          --          --          --
Amort Payment (Y3-7)         --          --     591,552     591,552     591,552     591,552     591,552

BTCF                    556,000     591,584     539,066     567,154     595,714     624,730     654,187

CAPEX
Renovations             150,000     150,000          --          --          --          --          --
Replacement Reserves     17,500      17,500      17,500      17,500      17,500      17,500      17,500
Total Capex             167,500     167,500      17,500      17,500      17,500      17,500      17,500

DISTRIBUTABLE CF        388,500     424,084     521,566     549,654     578,214     607,230     636,687
```

### Reversion Calculation (End of Year 7)

```
Year 8 forward NOI = Year 7 NOI * (1 + rent_growth)
                   = $1,245,739 * 1.03 = $1,283,111

Gross reversion = $1,283,111 / 0.0625 = $20,529,776
Less selling costs (2.0%): -$410,596
Less loan balance: -$7,291,000
Net equity reversion: $12,828,180
```

### Return Metrics

```
Equity invested: $12,000,000 - $7,800,000 + $300,000 capex = $4,500,000

Cash flows for IRR:
  Year 0:  -$4,500,000
  Year 1:   +$388,500
  Year 2:   +$424,084
  Year 3:   +$521,566
  Year 4:   +$549,654
  Year 5:   +$578,214
  Year 6:   +$607,230
  Year 7:   +$636,687 + $12,828,180 = $13,464,867

Total cash returned: $388,500 + $424,084 + $521,566 + $549,654 + $578,214
                   + $607,230 + $13,464,867 = $16,534,115
Equity multiple: $16,534,115 / $4,500,000 = 3.67x
Levered IRR: ~22.3%

Year 1 Cash-on-Cash: $388,500 / $4,500,000 = 8.6%
Average Cash-on-Cash: (sum of distributable CF years 1-7) / (7 * $4,500,000) = 11.5%
```

---

## 8. Sensitivity to Key Assumptions

Small changes in assumptions produce large changes in returns:

| Assumption Change | IRR Impact | Multiple Impact |
|---|---|---|
| Rent growth +/-1% | +/-250-350bps | +/-0.3-0.5x |
| Exit cap +/-25bps | +/-150-250bps | +/-0.2-0.4x |
| Vacancy +/-2% | +/-100-150bps | +/-0.1-0.2x |
| Interest rate +/-50bps | +/-75-125bps | +/-0.05-0.1x |

The exit cap rate and rent growth dominate returns. Always stress these first.

---

## 9. Common Errors

1. **Growing expenses at a flat rate**: Insurance, taxes, and payroll grow faster than R&M and G&A. A blended 3% masks the divergence. Model expense categories individually for accuracy.

2. **Applying rent growth to EGI instead of GPR**: Vacancy should be a percentage of the grown GPR, not a fixed dollar amount. Growing EGI directly understates vacancy loss as rents rise.

3. **Forgetting to grow the exit-year NOI**: The exit cap is applied to forward NOI (Year n+1), not the final hold-year NOI. Using hold-year NOI understates the reversion by one year of growth.

4. **Ignoring the IO-to-amortization transition**: Debt service jumps significantly when IO burns off. If this transition occurs mid-hold, BTCF drops and DSCR tightens. Model the exact transition month.

5. **Omitting selling costs from reversion**: Transfer taxes, broker commissions, and legal fees typically total 1.5-2.5% of gross proceeds. On a $20M reversion, this is $300K-$500K.

6. **Double-counting capex and reserves**: Renovation capex is a one-time project cost. Replacement reserves are ongoing. Do not add reserves on top of active renovation capex in the same year for the same components.

7. **Using nominal exit cap without justification**: An exit cap below the going-in cap implies the next buyer accepts a lower yield on an older building. This requires a strong narrative (NOI growth, market compression, repositioning). Default to flat or slight expansion.

---

## 10. Proforma Quality Checks

Before finalizing:

- [ ] Year 1 NOI matches normalized T-12 (within 2%)
- [ ] Expense ratio trends are realistic (should drift slightly higher as expenses outpace revenue)
- [ ] DSCR exceeds 1.25x in all years (or lender minimum)
- [ ] Capex schedule totals match renovation budget
- [ ] Exit cap is justified relative to going-in
- [ ] Reversion uses forward NOI, not trailing
- [ ] Equity multiple and IRR are consistent with each other
- [ ] Cash-on-cash is positive in all stabilized years
