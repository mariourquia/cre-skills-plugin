# Fund Accounting Methodology Reference

Complete methodologies for management fee calculation, capital account waterfall mechanics, carried interest computation, and fund expense allocation. All examples use a baseline $250M closed-end real estate PE fund (Fund IV, Vintage 2024, 4-year investment period, 8-year term, 8% preferred return, 20% carry with 100% catch-up, European waterfall).

---

## 1. Management Fee Calculation

### Fee Basis: Committed vs Invested Capital

**During investment period (Years 1-4)**:

```
Fee basis: total committed capital (including GP commitment)
Annual fee: $250,000,000 * 1.50% = $3,750,000
Quarterly fee: $3,750,000 / 4 = $937,500
```

**After investment period (Years 5-8+)**:

```
Fee basis: net invested capital
Net invested capital = cumulative capital called for investments
                     - cumulative return of capital distributions
                     - realized write-downs

Example at Year 5:
  Cumulative called for investments: $187,500,000 (75% of commitments)
  Return of capital distributed:      $45,000,000
  Realized write-downs:                $3,500,000
  Net invested capital:              $139,000,000

Annual fee (step-down rate 1.25%): $139,000,000 * 1.25% = $1,737,500
Quarterly fee: $1,737,500 / 4 = $434,375
```

### Per-LP Fee Allocation

```
LP fee allocation = LP_commitment / total_committed * fund_quarterly_fee

Example (investment period):
  Fund total committed: $250,000,000
  LP A commitment: $50,000,000 (20.0%)
  LP B commitment: $40,000,000 (16.0%)
  LP C commitment: $30,000,000 (12.0%)
  ...remaining 32 LPs: $130,000,000 (52.0%)

  LP A quarterly fee = $937,500 * 20.0% = $187,500
  LP B quarterly fee = $937,500 * 16.0% = $150,000
  LP C quarterly fee = $937,500 * 12.0% = $112,500
```

### Side Letter Fee Discount Application

```
Standard rate: 1.50% (investment period)
LP A side letter: 30bp discount = 1.20%
LP B MFN election: 30bp discount = 1.20%
LP C side letter: 15bp discount = 1.35%
All other LPs: 1.50% (standard)

Fee calculation with discounts:
  LP A: $50,000,000 * 1.20% / 4  = $150,000  (saves $37,500/quarter)
  LP B: $40,000,000 * 1.20% / 4  = $120,000  (saves $30,000/quarter)
  LP C: $30,000,000 * 1.35% / 4  = $101,250  (saves $11,250/quarter)
  Other LPs: $130,000,000 * 1.50% / 4 = $487,500
  Total quarterly fee: $858,750

  vs. no-discount quarterly fee: $937,500
  Quarterly revenue impact of side letters: -$78,750 (-8.4%)
  Annual revenue impact: -$315,000
```

### Late Close Equalization

When an LP joins at a subsequent closing, they must pay equalization interest on what they would have contributed had they been admitted at the first close.

```
Worked example:
  First close: January 1, 2024 -- $175M committed
  Second close: July 1, 2024 -- $75M additional (including LP D at $25M)

  Between first and second close:
    Capital calls made: $30,000,000 (17.1% of first close commitments)
    Management fees paid: $937,500 * 2 quarters = $1,875,000

  LP D's equalization:
    LP D's pro rata share of calls: $25M / $250M * $30M = $3,000,000
    LP D's pro rata share of fees: $25M / $250M * $1,875,000 = $187,500
    Equalization interest: ($3,000,000 + $187,500) * prime_rate * (6/12) = varies
      At 8.5% prime: $3,187,500 * 8.5% * 0.5 = $135,469

    LP D pays at second close:
      Capital call equalization: $3,000,000
      Fee equalization: $187,500
      Equalization interest: $135,469
      Total: $3,322,969
```

---

## 2. Capital Account Waterfall Mechanics

### European (Whole-Fund) Waterfall

The European waterfall requires that all LPs receive return of capital plus preferred return on the entire fund before the GP receives any carried interest. This is the most LP-favorable structure.

```
Tier 1: Return of Capital
  All distributions first return contributed capital to LPs (pro rata)
  LP receives 100% until: cumulative distributions = cumulative contributions

Tier 2: Preferred Return
  After full return of capital, LPs receive 100% of distributions
  until they have earned the preferred return on their contributed capital
  Preferred return = 8% IRR on a compounded, time-weighted basis

Tier 3: GP Catch-Up
  After LPs have received full preferred return, GP receives 100%
  of distributions until GP has received 20% of total profits
  (profits = all distributions in excess of return of capital)
  Catch-up = 100% to GP until: GP_carry = 20% * total_profits

Tier 4: 80/20 Split
  All remaining distributions split 80% to LPs, 20% to GP
```

### Worked Example: $250M Fund Waterfall

```
Fund IV -- distribution at Year 6 exit of a portfolio investment

Fund-level capital activity:
  Total committed: $250,000,000
  Total called: $187,500,000 (75%)
  Prior distributions: $62,500,000 (all return of capital)
  Current distribution: $180,000,000 (from exit of 3 investments)

Capital account before distribution:
  Contributed capital: $187,500,000
  Prior ROC distributions: -$62,500,000
  Unreturned capital: $125,000,000

Waterfall calculation:

  Tier 1: Return of remaining capital
    Amount: $125,000,000
    Remaining to distribute: $180,000,000 - $125,000,000 = $55,000,000
    LP cumulative distributions after Tier 1: $62,500,000 + $125,000,000 = $187,500,000
    (equals contributed capital -- return of capital complete)

  Tier 2: Preferred return
    Calculate accrued preferred return:
      LP contributed capital weighted by time:
        Call 1: $50,000,000 on 01/01/2024 (6 years to distribution)
        Call 2: $37,500,000 on 07/01/2024 (5.5 years)
        Call 3: $50,000,000 on 01/01/2025 (5 years)
        Call 4: $50,000,000 on 07/01/2025 (4.5 years)

      8% compounded preferred return by call:
        Call 1: $50M * (1.08^6 - 1) = $29,385,000
        Call 2: $37.5M * (1.08^5.5 - 1) = $19,705,000
        Call 3: $50M * (1.08^5 - 1) = $23,466,000
        Call 4: $50M * (1.08^4.5 - 1) = $20,792,000
      Total accrued preferred: $93,348,000

      Less: any prior preferred return distributions: $0
      Preferred return owed: $93,348,000

    But only $55,000,000 remaining to distribute.
    $55,000,000 < $93,348,000 -- preferred return not fully met.
    Entire $55,000,000 goes to LPs as preferred return.
    Preferred return shortfall: $93,348,000 - $55,000,000 = $38,348,000

  Tier 3: GP Catch-Up
    Not reached (preferred return not fully satisfied)
    GP carry this distribution: $0

  Tier 4: 80/20 Split
    Not reached

  Distribution summary:
    To LPs: $180,000,000 (100%)
      Return of capital: $125,000,000
      Preferred return: $55,000,000
    To GP (carry): $0
    Preferred return still owed: $38,348,000

Note: GP receives management fees regardless of carry. The $0 carry is a
function of fund performance not yet reaching the 8% IRR hurdle on a
whole-fund basis.
```

### American (Deal-by-Deal) Waterfall

```
The American waterfall calculates carry on each deal independently.
This is more GP-favorable because the GP can earn carry on profitable
deals even if the overall fund has not returned all capital.

Key differences from European:
  1. Return of capital is computed per-deal, not whole-fund
  2. Preferred return is computed on deal-level capital, not total fund
  3. GP can earn carry on Deal A while Deal B is at a loss
  4. Clawback provision is critical to protect LPs if later deals lose money

Clawback mechanics:
  At fund wind-down, if GP has received more carry than it would have
  under a European waterfall, GP must return the excess.

  Example:
    Deal A: invested $25M, returned $50M, GP earned $4M carry
    Deal B: invested $25M, total loss, returned $0
    Fund-level: invested $50M, returned $50M, zero profit
    European waterfall carry: $0 (no profit above return of capital)
    American waterfall carry received: $4M
    Clawback owed by GP: $4M
```

---

## 3. Carried Interest Calculation

### Detailed Carry Computation (European Waterfall)

```
Assumptions:
  Fund size: $250,000,000
  GP commitment: $5,000,000 (2%)
  Preferred return: 8% compounded annually
  Carry: 20% with 100% catch-up
  Fund life: investments fully realized at Year 8

  Total called: $200,000,000 (80% of commitments)
  Total distributions: $400,000,000
  Total profit: $200,000,000

Step 1: Return of capital = $200,000,000
  Remaining: $400,000,000 - $200,000,000 = $200,000,000

Step 2: Preferred return
  8% compounded on $200M called over an average hold of 5 years:
  (simplification -- actual calculation is time-weighted per capital call)
  Approximate preferred return: $200M * (1.08^5 - 1) = $93,866,000
  Remaining after preferred: $200,000,000 - $93,866,000 = $106,134,000

Step 3: GP catch-up
  Total profits = $200,000,000
  GP target carry = 20% * $200,000,000 = $40,000,000
  GP has received: $0 in carry so far
  Catch-up amount: 100% to GP until GP has $40,000,000
  But also: check that remaining amount supports the catch-up

  Catch-up math:
    After preferred, $106,134,000 remains
    GP receives 100% catch-up: $40,000,000
    Remaining after catch-up: $106,134,000 - $40,000,000 = $66,134,000

Step 4: 80/20 split on remainder
  LP share: 80% * $66,134,000 = $52,907,000
  GP share: 20% * $66,134,000 = $13,227,000

Total distribution:
  LPs: $200,000,000 (ROC) + $93,866,000 (pref) + $52,907,000 (80/20)
     = $346,773,000 (86.7%)
  GP carry: $40,000,000 (catch-up) + $13,227,000 (80/20) = $53,227,000 (13.3%)

  Verification: $346,773,000 + $53,227,000 = $400,000,000 (matches)

  Effective carry rate: $53,227,000 / $200,000,000 profit = 26.6%
    (exceeds 20% because catch-up accelerates GP's share)

  Note: GP also participates as a 2% LP ($5M commitment), receiving
  pro rata LP distributions. GP's total economics:
    LP share: $346,773,000 * ($5M / $250M) = $6,935,000
    Carry: $53,227,000
    Total GP: $60,162,000 on $5,000,000 invested = 12.0x
```

---

## 4. Fund Expense Allocation

### Expense Categories

```
GP-borne expenses (not charged to fund):
  - GP entity operating costs (rent, salaries, benefits)
  - Internal travel for deal sourcing
  - GP-level insurance (D&O, E&O)
  - Marketing and fundraising costs (except placement agent fees)
  - Formation costs above LPA cap

Fund-borne expenses (charged to fund/LPs):
  - Management fees
  - Organizational expenses (up to LPA cap, typically $250K-$500K)
  - Annual audit fees
  - Tax preparation and filing (fund and subsidiary level)
  - Legal fees (ongoing fund operations, not formation)
  - Fund administrator fees
  - Insurance (fund-level, property-level)
  - Banking and custody fees
  - LPAC meeting expenses
  - Regulatory filing fees
  - Placement agent fees (if charged to fund per LPA)

Deal-level expenses (charged to specific investments):
  - Due diligence costs (appraisals, environmental, surveys)
  - Transaction legal fees
  - Transfer taxes and recording fees
  - Property management fees
  - Asset management fees (if separate from fund management fee)
  - Property-level insurance
  - Property-level taxes
```

### Worked Example: Quarterly Fund Expense Calculation

```
Fund IV -- Q3 2025 Expense Summary

| Category | Amount | Notes |
|---|---|---|
| Management fee | $858,750 | Per fee calc with side letter discounts |
| Fund administrator | $37,500 | $150K/year, quarterly |
| Audit fee accrual | $25,000 | $100K annual audit, quarterly accrual |
| Legal (fund ops) | $42,000 | Ongoing regulatory and LP matters |
| Tax preparation accrual | $18,750 | $75K annual, quarterly accrual |
| Insurance (fund level) | $12,500 | $50K annual D&O/E&O |
| Banking fees | $2,500 | Custody and wire fees |
| LPAC meeting | $4,200 | Q3 LPAC meeting costs |
| Regulatory filings | $1,500 | State notice filings |
| Total fund expenses | $1,002,700 | |

Fund NAV (estimated): $195,000,000
Annualized TER: ($1,002,700 * 4) / $195,000,000 = 2.06%
Benchmark: 2.0-3.0% for $100M-$500M funds
Status: WITHIN RANGE

Expense allocation to LPs (pro rata by commitment):
  LP A ($50M, 20.0%): $200,540
  LP B ($40M, 16.0%): $160,432
  LP C ($30M, 12.0%): $120,324
  ...
```

### Management Fee Offset

```
Some LPAs require that fee income earned by the GP from portfolio
companies (e.g., transaction fees, monitoring fees, director fees)
offset the management fee by 50-100%.

Offset calculation:
  Q3 management fee: $858,750
  GP fee income from portfolio companies:
    Transaction fee (Deal E closing): $500,000
    Monitoring fee (3 portfolio companies): $75,000
  Total GP fee income: $575,000
  Offset rate: 80% per LPA
  Offset amount: $575,000 * 80% = $460,000
  Net management fee: $858,750 - $460,000 = $398,750

This offset directly benefits LPs by reducing the total fee burden.
Track offsets quarterly and report in LP capital account statements.
```
