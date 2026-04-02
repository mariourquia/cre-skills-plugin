# Refinancing Analysis Formula Reference

Complete formulas, worked examples, and decision frameworks for CRE refinancing analysis. Baseline scenario: refinancing a $20M loan from 5.00% to 6.50%, 5-year term, 30-year amortization, on a property with $1,500,000 NOI.

---

## 1. Prepayment Penalty Comparison

### 1A. Yield Maintenance

#### Definition

Yield maintenance compensates the lender for the interest differential between the contract rate and the reinvestment rate (Treasury) over the remaining loan term. It ensures the lender receives the same yield they would have earned had the loan remained outstanding.

#### Formula

```
YM = PV of rate differential over remaining term

YM = sum_{t=1}^{n} [Balance_t * (contract_rate - treasury_rate)] / (1 + treasury_rate)^t

Simplified (constant balance approximation for IO loans):
YM ≈ outstanding_balance * (contract_rate - treasury_rate) * PV_annuity_factor(treasury_rate, n)

PV_annuity_factor = [1 - (1 + r)^(-n)] / r
```

For amortizing loans, use the projected declining balance schedule in place of constant balance.

#### Worked Example

Existing loan: $19,200,000 outstanding (after 2 years of amortization on $20M, 30yr, 5.00%)
Contract rate: 5.00%
Remaining term: 36 months (3 years left on 5-year term)
Treasury rate (3-year): 4.25%

```
Rate differential = 5.00% - 4.25% = 0.75%
PV annuity factor (monthly, 4.25%/12, 36 months):
  r_m = 0.0425/12 = 0.003542
  PV_annuity = [1 - (1.003542)^(-36)] / 0.003542 = 33.53

Monthly differential = $19,200,000 * 0.0075 / 12 = $12,000
YM = $12,000 * 33.53 = $402,360

Alternative (annual approximation):
YM ≈ $19,200,000 * 0.0075 * [1 - (1.0425)^(-3)] / 0.0425
   ≈ $144,000 * 2.776
   ≈ $399,744
```

Yield maintenance penalty: approximately $400,000 (2.08% of outstanding balance).

#### Key Variables

- If Treasury rates RISE above contract rate, YM can be zero or negative (lender benefits from reinvestment at higher rates). Most loan docs floor YM at 1% of outstanding balance or zero.
- If Treasury rates FALL, YM increases dramatically. A 200bp drop with 3 years remaining could yield a penalty of 5-6% of outstanding balance.

### 1B. Defeasance

#### Definition

Defeasance substitutes the loan collateral: the borrower purchases a portfolio of U.S. Treasury securities that exactly replicate the remaining debt service payments, releasing the property from the mortgage lien.

#### Cost Estimation Formula

```
Defeasance cost = cost_of_treasury_portfolio + transaction_costs

Treasury portfolio cost = sum_{t=1}^{n} DS_t / (1 + treasury_yield_t)^t

where DS_t = scheduled debt service payment in period t (P&I)
      treasury_yield_t = yield on Treasury STRIP maturing at time t

Transaction costs:
  Successor borrower fee:     $10,000 - $25,000
  Legal counsel:              $25,000 - $50,000
  Accountant/servicer:        $10,000 - $15,000
  Rating agency (CMBS):       $10,000 - $25,000
  Total transaction costs:    $55,000 - $115,000
```

#### Worked Example

Existing CMBS loan: $19,200,000 outstanding
Rate: 5.00%, 30yr amort, 36 months remaining on 5-year term
Monthly P&I: $103,093 (on original $20M; balance declines over 36 months)
Balloon at maturity: $18,582,000 (approximate, after 60 months of amortization)

```
Cost of Treasuries to replicate 36 monthly payments + balloon:
  Assume flat Treasury curve at 4.25%:
  PV of 36 monthly payments: $103,093 * 33.53 = $3,456,728
  PV of balloon: $18,582,000 / (1.0425)^3 = $16,415,889
  Total Treasury cost: $19,872,617

  Premium over outstanding balance: $19,872,617 - $19,200,000 = $672,617

  Plus transaction costs: ~$75,000
  Total defeasance cost: ~$747,617  (3.89% of outstanding balance)
```

#### Yield Maintenance vs. Defeasance Comparison

| Factor | Yield Maintenance | Defeasance |
|---|---|---|
| Typical cost | Lower when rates rise | Higher due to transaction costs + Treasury premium |
| Execution timeline | 30-60 days | 45-90 days (Treasury purchase, successor borrower setup) |
| Rate sensitivity | Inversely correlated with rates | Inversely correlated with rates, plus fixed costs |
| Loan type | Bank/balance sheet loans | CMBS loans (required if in docs) |
| Floor | Often 1% of balance or $0 | Treasury portfolio cost cannot go below zero, but fixed costs always apply |

### 1C. Step-Down (Declining Prepayment Penalty)

#### Formula

```
Penalty = outstanding_balance * step_down_rate

Typical 5-year schedule:
  Year 1: 5% (locked out or 5%)
  Year 2: 4%
  Year 3: 3%
  Year 4: 2%
  Year 5: 1%
  After year 5: Open (0%)
```

#### Worked Example

Prepaying in year 3 of a 5-year term:

```
Outstanding balance: $19,200,000
Step-down rate in year 3: 3%
Penalty: $19,200,000 * 0.03 = $576,000
```

Step-down is simpler and more predictable than YM or defeasance. Common in balance sheet and bridge loans. Not sensitive to interest rate movements.

---

## 2. Rate Lock Strategy

### Lock Cost Components

```
Total lock cost = base_lock_fee + extension_risk + float_cost

Base lock fee (at application): 0.00-0.50% of loan amount
Rate lock period: 30-90 days standard
Extension fee: 0.125-0.250% per 15-day extension
Float-down option: +0.125% to base rate (allows borrower to capture rate declines)
```

### Lock Decision Framework

```
Expected rate movement over closing period:
  If rates expected to rise > lock cost: LOCK
  If rates expected to fall > lock cost: FLOAT
  If uncertain and deal cannot absorb rate increase: LOCK (insurance value)

Break-even analysis:
  Lock cost = $20,000,000 * 0.00375 = $75,000 (37.5bp lock fee)
  Rate increase that equals lock cost over loan life:
    PV of 37.5bp over 5-year term = $75,000 (approximately, given $20M loan)
    Rate increase of ~4bp makes the lock worthwhile (extremely small)

  Conclusion: locking is almost always rational unless rates are actively declining.
```

---

## 3. Debt Constant Analysis

### Formula

```
Debt constant (K) = annual_debt_service / loan_amount

For fully amortizing loan:
K = [r * (1 + r)^n / ((1 + r)^n - 1)] * 12

where r = monthly_rate, n = amortization_months

For IO loan:
K = annual_interest_rate
```

### Significance

The debt constant is the effective annual cost of the loan per dollar borrowed, including both interest and principal amortization. It is the direct comparator to the property's cap rate for determining positive vs. negative leverage.

```
If cap_rate > K: positive leverage (property earns more than debt costs)
If cap_rate < K: negative leverage (debt costs more than property earns)
If cap_rate = K: leverage-neutral
```

### Worked Example: Refi Comparison

| Metric | Existing Loan (5.00%) | New Loan (6.50%) |
|---|---|---|
| Loan amount | $19,200,000 | $20,000,000 |
| Rate | 5.00% | 6.50% |
| Amortization | 30 years | 30 years |
| Monthly payment | $103,093 | $126,408 |
| Annual debt service | $1,237,116 | $1,516,896 |
| Debt constant (K) | 6.44% | 7.58% |
| Property cap rate | 7.50% | 7.50% |
| Leverage impact | Positive (+106bp) | Slightly negative (-8bp) |

The refi from 5.00% to 6.50% flips the deal from positive to negative leverage. The debt constant at 6.50% (7.58%) exceeds the cap rate (7.50%), meaning each dollar of debt now destroys rather than creates value. This is a critical decision point: the refi only makes sense if (a) the existing loan is maturing and must be replaced, or (b) the cash-out proceeds fund a higher-returning use.

---

## 4. Cash-Out NPV Analysis

### When to Refi for Cash-Out

```
NPV of cash-out refi = PV of cash-out proceeds used at reinvestment rate
                     - PV of incremental debt service cost
                     - prepayment penalty
                     - transaction costs (origination, legal, title, appraisal)
```

### Worked Example

Existing loan: $19,200,000 at 5.00%, 3 years remaining
New loan: $22,000,000 at 6.50%, 5-year term, 30-year amort
Cash-out: $22,000,000 - $19,200,000 - penalty - costs

```
Step 1: Prepayment penalty (yield maintenance)
  YM = ~$400,000 (from Section 1A)

Step 2: Transaction costs
  Origination (1%): $220,000
  Legal, title, appraisal: $75,000
  Total closing costs: $295,000

Step 3: Net cash-out
  $22,000,000 - $19,200,000 - $400,000 - $295,000 = $2,105,000

Step 4: Incremental annual debt service
  New ADS: $22M at 6.50%, 30yr = $1,668,580
  Old ADS: $19.2M at 5.00%, 30yr = $1,237,116  (remaining 3 years)
  Incremental: $431,464/year

  But old loan matures in 3 years. After year 3, the comparison is:
    Years 1-3: incremental cost = $431,464/year
    Years 4-5: new ADS vs. whatever replacement loan would have been
    Assume replacement at year 3 would be at 6.50% for $19.2M:
      Replacement ADS = $19.2M at 6.50% = $1,457,088
    Years 4-5 incremental = $1,668,580 - $1,457,088 = $211,492/year

Step 5: NPV at 12% discount rate (sponsor's reinvestment return on cash-out)
  PV of cash-out at 12% return:
    Year 1 return: $2,105,000 * 0.12 = $252,600
    (Assume cash-out is deployed immediately and earns 12% IRR)
    PV of 5-year cash-out deployment at 12%: $2,105,000 (already present value)

  PV of incremental costs at 8% WACC:
    Years 1-3: $431,464 * PV annuity(8%, 3) = $431,464 * 2.577 = $1,111,884
    Years 4-5: $211,492 * PV annuity(8%, 2) discounted 3 years = $211,492 * 1.783 * 0.794 = $299,587
    Total PV of incremental cost: $1,411,471

Step 6: NPV
  NPV = $2,105,000 - $1,411,471 = $693,529

  Decision: Cash-out refi is NPV-positive IF the sponsor can deploy proceeds at 12%+ IRR.
```

### Sensitivity to Reinvestment Rate

| Reinvestment Rate | NPV of Cash-Out | Decision |
|---|---|---|
| 8% | -$243,000 | Reject |
| 10% | $178,000 | Marginal accept |
| 12% | $693,000 | Accept |
| 15% | $1,452,000 | Strong accept |

The breakeven reinvestment rate is approximately 9.2%. Below that, the incremental debt cost exceeds the return on deployed capital.

---

## 5. DSCR Sensitivity at Rate Increments

### Formula

```
DSCR(rate) = NOI / ADS(rate)

ADS(rate) = loan * [r * (1 + r)^n / ((1 + r)^n - 1)] * 12
where r = rate / 12, n = amortization months
```

### Worked Example: $20M Loan, $1,500,000 NOI, 30-Year Amortization

| Rate | Monthly Payment | Annual DS | DSCR | Debt Constant | Leverage vs. 7.5% Cap |
|---|---|---|---|---|---|
| 5.00% | $107,364 | $1,288,368 | 1.16x | 6.44% | Positive (+106bp) |
| 5.50% | $113,569 | $1,362,828 | 1.10x | 6.81% | Positive (+69bp) |
| 6.00% | $119,910 | $1,438,920 | 1.04x | 7.19% | Positive (+31bp) |
| 6.50% | $126,408 | $1,516,896 | 0.99x | 7.58% | Negative (-8bp) |
| 7.00% | $133,060 | $1,596,720 | 0.94x | 7.98% | Negative (-48bp) |
| 7.50% | $139,883 | $1,678,596 | 0.89x | 8.39% | Negative (-89bp) |
| 8.00% | $146,753 | $1,761,036 | 0.85x | 8.81% | Negative (-131bp) |

### Key Observations

1. **DSCR drops below 1.0x at 6.50%**: The property cannot fully service debt from NOI alone. Sponsor must fund shortfall from reserves or equity.
2. **Each 50bp increase reduces DSCR by approximately 0.03-0.05x** at this leverage level.
3. **Lender minimum DSCR of 1.25x constrains maximum loan amount**: At 6.50%, max loan for 1.25x DSCR = $1,500,000 / (1.25 * 0.0758) = $15,831,000 (vs. $20M requested). The borrower must either bring more equity, reduce the ask, or negotiate a lower DSCR requirement.
4. **Breakeven rate** (DSCR = 1.00x): approximately 6.35% for this deal. Above that, the loan is cash-negative.

### DSCR Floor Calculation

```
For a target DSCR of 1.25x:
  Max ADS = NOI / 1.25 = $1,500,000 / 1.25 = $1,200,000
  Max loan amount = $1,200,000 / K(rate)

  At 5.00%: $1,200,000 / 0.0644 = $18,634,000
  At 6.00%: $1,200,000 / 0.0719 = $16,689,000
  At 6.50%: $1,200,000 / 0.0758 = $15,831,000
  At 7.00%: $1,200,000 / 0.0798 = $15,038,000
  At 7.50%: $1,200,000 / 0.0839 = $14,302,000
```

---

## 6. Refi Decision Matrix

### When to Refi (Even at Higher Rate)

| Scenario | Refi Rational? | Key Test |
|---|---|---|
| Loan maturing, no extension | Yes (forced) | Minimize new rate; compare term sheet competitively |
| Rate decrease available | Yes (voluntary) | Savings > penalty + costs (NPV positive) |
| Cash-out for higher-return deployment | Maybe | Reinvestment IRR > breakeven (see Section 4) |
| Rate increase but need to extend term | Maybe | Value of term extension > cost of higher rate |
| Rate increase, no cash-out, loan not maturing | Rarely | Almost never rational to voluntarily refi into a higher rate without other benefits |

---

## 7. Common Errors

| Error | Consequence |
|---|---|
| Ignoring prepayment penalty in refi NPV | Overstates savings by $200K-$1M+ on institutional loans |
| Using IO debt constant to compare amortizing loans | Understates true debt cost; amortizing loan at 6.5% has K=7.58%, not 6.5% |
| Assuming cash-out proceeds earn risk-free rate | Understates refi benefit; cash-out should be evaluated at the sponsor's actual reinvestment return |
| Comparing rates without comparing terms | A 6.5% rate with 3yr IO and 5yr term is cheaper than 6.0% with immediate amortization and 3yr term |
| Ignoring transaction costs | Legal, title, appraisal, and origination fees total 1.5-2.5% of new loan amount |
| Not stress-testing floating rate refi | If new loan is SOFR-based, must model rate scenarios; a 200bp SOFR increase changes the entire decision |
