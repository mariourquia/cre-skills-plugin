# Interest Rate Hedging Guide for CRE

Instrument mechanics, pricing, construction, and selection criteria for CRE floating-rate debt hedging. All examples use a $19,000,000 senior floating-rate loan at SOFR + 250bps.

---

## 1. Interest Rate Cap

### Mechanics

A rate cap is a purchased option. The borrower pays an upfront premium and receives payments when the reference rate exceeds the strike rate.

```
Cap payoff per period = max(0, Reference_rate - Strike_rate) * Notional * (days/360)

If SOFR = 5.50% and strike = 4.00%:
  Payoff = (0.0550 - 0.0400) * 19,000,000 * (30/360) = $23,750/month
```

The borrower's effective rate is capped at: Strike + Spread = 4.00% + 2.50% = 6.50%.

### Pricing Factors

Cap pricing depends on:
1. **Strike rate**: Lower strike = more protection = higher premium
2. **Term**: Longer cap = higher premium (more optionality)
3. **Volatility**: Higher implied vol = higher premium
4. **Forward curve**: If the market expects rates to rise, caps are more expensive

### Pricing Framework (Black-76 Model)

Each caplet (individual period's cap) is priced as a European call option on the forward rate:

```
Caplet_value = DF * delta * [F * N(d1) - K * N(d2)]

Where:
  DF = discount factor to payment date
  delta = day count fraction (actual/360)
  F = forward rate for the period
  K = strike rate
  d1 = [ln(F/K) + 0.5*sigma^2*T] / (sigma*sqrt(T))
  d2 = d1 - sigma*sqrt(T)
  sigma = implied volatility for that tenor
  N() = standard normal CDF

Cap price = sum of all caplet values over the cap term
```

### Worked Example: 3-Year Cap Pricing

```
Notional: $19,000,000
Strike: 4.00%
Term: 3 years (quarterly resets)
Current SOFR: 4.50%
Forward curve: 4.25% (Y1), 3.75% (Y2), 3.50% (Y3)
Implied vol: 45% (swaption vol surface)

Approximate caplet values (simplified):
  Y1 caplets (4 quarters): High value -- SOFR above strike
    Avg forward: 4.25%, intrinsic ≈ 0.25%, time value adds ~0.15%
    Y1 caplet value ≈ $19M * 0.0040 * 1.0 = $76,000

  Y2 caplets: Lower value -- forward near strike
    Avg forward: 3.75%, out-of-the-money
    Y2 caplet value ≈ $19M * 0.0020 * 1.0 = $38,000

  Y3 caplets: Low value -- forward below strike
    Avg forward: 3.50%, further OTM
    Y3 caplet value ≈ $19M * 0.0010 * 1.0 = $19,000

Total cap premium ≈ $133,000 (0.70% of notional)

Amortized cost: $133,000 / 3 years = $44,333/year
Effective rate increase: $44,333 / $19,000,000 = 0.23%/year
All-in max rate: SOFR cap at 4.00% + 2.50% spread + 0.23% amort = 6.73%
```

### Typical CRE Cap Costs (2025-2026 Environment)

| Cap Term | Strike (SOFR) | Approx Cost (% of Notional) |
|---|---|---|
| 2 years | 3.00% | 1.5-2.5% |
| 2 years | 4.00% | 0.5-1.2% |
| 3 years | 3.00% | 2.5-4.0% |
| 3 years | 4.00% | 0.7-1.5% |
| 3 years | 5.00% | 0.2-0.5% |
| 5 years | 4.00% | 1.5-3.0% |

Agency and CMBS lenders typically require borrowers to purchase a rate cap on floating-rate loans. The required strike is often set so that the all-in rate at the strike does not exceed a specific DSCR threshold (usually 1.0x to 1.25x).

---

## 2. Interest Rate Swap

### Mechanics

A swap exchanges floating-rate payments for fixed-rate payments. No upfront premium (at inception, the swap has zero NPV if priced at the par swap rate).

```
Borrower pays:  Fixed swap rate * Notional * (days/360)
Borrower receives: SOFR * Notional * (days/360)

Net: Borrower's floating loan payment is converted to a fixed rate.

All-in fixed rate = Swap rate + Loan spread
```

### Swap Rate Determination

The par swap rate is the fixed rate that makes the present value of fixed payments equal to the present value of expected floating payments (derived from the forward curve):

```
Swap_rate = [sum(DF_i * Forward_SOFR_i * delta_i)] / [sum(DF_i * delta_i)]

Where DF_i = discount factor, delta_i = accrual period
```

### Worked Example: 5-Year Swap

```
Notional: $19,000,000
Current SOFR: 4.50%
5-year swap rate: 3.80% (market mid, per SOFR swap curve)
Loan spread: 2.50%

All-in fixed rate: 3.80% + 2.50% = 6.30%

Annual fixed payment: $19,000,000 * 0.0630 = $1,197,000
Monthly: $99,750

Comparison to unhedged:
  Current floating: (4.50% + 2.50%) = 7.00% = $1,330,000/year
  Swap converts to: 6.30% = $1,197,000/year
  Year 1 savings: $133,000 (if rates stay at 4.50%)

If SOFR drops to 3.00%:
  Unhedged: (3.00% + 2.50%) = 5.50% = $1,045,000/year
  Swapped: still 6.30% = $1,197,000/year
  Swap cost: $152,000/year (locked in above market)
```

### Swap Risks

1. **Mark-to-market risk**: If rates drop significantly, the swap has negative value. Exiting early requires paying the termination value.
2. **Termination cost**: For a $19M 5-year swap, a 100bps rate drop creates approximately $19M * 0.01 * 4 (remaining years, rough duration) = $760,000 termination cost.
3. **Basis risk**: If the loan resets on a different index or frequency than the swap, residual floating exposure remains.
4. **Counterparty risk**: The swap provider must remain solvent. Use ISDA documentation with credit support annex (CSA).

### When to Use a Swap

```
Swap is appropriate when:
  - Hold period is well-defined (no early exit flexibility needed)
  - Borrower wants certainty of debt service for underwriting
  - Forward curve implies rates will stay elevated or rise
  - Loan is large enough to justify documentation costs ($10M+ typically)

Swap is NOT appropriate when:
  - Early sale or refinance is likely (termination costs)
  - Rate environment is expected to decline (opportunity cost)
  - Loan has significant prepayment penalties that conflict with swap unwind
```

---

## 3. Interest Rate Collar

### Mechanics

A collar combines a purchased cap (protection against rate increases) with a sold floor (giving up benefit from rate decreases). The floor premium offsets the cap premium, reducing or eliminating the net cost.

```
Collar = Long cap at K_cap + Short floor at K_floor

Borrower's effective rate is bounded:
  Minimum rate: K_floor + spread
  Maximum rate: K_cap + spread
```

### Construction

```
Step 1: Price the cap at the desired strike.
  Cap at 4.00%, 3 years: $133,000 (from Section 1)

Step 2: Find the floor strike that offsets the cap cost.
  Solve for K_floor such that floor premium ≈ cap premium.

  Floor pricing uses the same Black-76 framework but for put options on SOFR:
  Floorlet = DF * delta * [K * N(-d2) - F * N(-d1)]

  If cap costs $133,000, a floor struck at 3.25% for 3 years might generate
  approximately $125,000 in premium (since forward rates are near 3.50-4.25%).

Step 3: Net cost
  Net premium = $133,000 - $125,000 = $8,000 (near zero-cost collar)
```

### Worked Example: Zero-Cost Collar

```
Notional: $19,000,000
Cap strike: 4.00%
Floor strike: 3.25%
Term: 3 years
Net premium: ≈ $0 (strikes chosen to offset)
Loan spread: 2.50%

Rate scenarios:
  SOFR = 5.00%: Cap activates. Effective rate = 4.00% + 2.50% = 6.50%
  SOFR = 4.00%: No activation. Effective rate = 4.00% + 2.50% = 6.50%
  SOFR = 3.50%: No activation. Effective rate = 3.50% + 2.50% = 6.00%
  SOFR = 3.00%: Floor activates. Effective rate = 3.25% + 2.50% = 5.75%
  SOFR = 2.50%: Floor activates. Effective rate = 3.25% + 2.50% = 5.75%

Rate range: 5.75% to 6.50% (75bps band)
```

### Collar Trade-Offs

```
Advantages:
  - Low or zero upfront cost
  - Provides rate ceiling (like a cap)
  - Simpler than a swap (no mark-to-market exposure)

Disadvantages:
  - Gives up downside benefit (floor limits savings if rates drop)
  - If rates drop significantly, borrower pays above market
  - Less common in CRE; some lenders may not accept for DSCR compliance
```

---

## 4. Instrument Selection Framework

### Decision Tree

```
1. Is the loan floating-rate?
   No  -> No hedge needed (fixed-rate loan)
   Yes -> Continue

2. Does the lender require a rate cap?
   Yes -> Purchase required cap (comply with lender terms)
         Consider collar to offset cost if allowed
   No  -> Continue

3. Is the hold period certain?
   Yes -> Consider swap (full protection, zero upfront cost)
   No  -> Prefer cap or collar (no termination risk)

4. What is the borrower's rate view?
   Rates will rise:    Cap or swap (protect against increases)
   Rates will fall:    No hedge or cap only (preserve downside benefit)
   No strong view:     Collar (bounded range, low cost)

5. What is the deal's cash flow sensitivity?
   Thin margins:       Swap (certainty of debt service)
   Healthy margins:    Cap (protection with upside flexibility)
```

### Cost Comparison for $19M, 3-Year Hedge

```
Instrument       | Upfront Cost | Ongoing Cost  | Max All-In Rate | Min All-In Rate
-----------------|--------------|---------------|-----------------|----------------
No hedge         | $0           | $0            | Unlimited       | Spread only
Rate cap (4.00%) | $133,000     | $0            | 6.50%           | Spread + SOFR
Swap (3.80%)     | $0           | Fixed at 6.30%| 6.30%           | 6.30%
Collar (4.00/3.25)| ~$0         | $0            | 6.50%           | 5.75%
```

### Hedge Accounting Note

Under ASC 815, qualifying cash flow hedges allow the effective portion of the hedge gain/loss to be recorded in other comprehensive income (OCI) rather than P&L. This smooths earnings volatility for GAAP-reporting entities. Most CRE JVs are partnerships and do not require hedge accounting, but REIT-held assets may benefit.

---

## 5. Swaption: The Option to Enter a Swap

### When Used in CRE

Swaptions are relevant for:
- Forward-starting construction loans (lock in the permanent loan swap rate before conversion)
- Rate lock before acquisition closing
- Portfolio-level hedging where timing is uncertain

### Mechanics

```
A payer swaption gives the holder the right (not obligation) to enter into a swap
where they pay fixed and receive floating.

Premium = Black-76 option value on the forward swap rate

Example:
  6-month payer swaption into a 5-year swap at 3.80%
  If 5-year swap rate in 6 months > 3.80%: exercise (lock in 3.80%)
  If 5-year swap rate in 6 months < 3.80%: let expire (get better market rate)

  Typical premium: 0.3-0.8% of notional depending on vol and time to expiry
  $19M * 0.005 = $95,000 for moderate premium
```

### CRE Application: Construction-to-Perm

```
Developer secures a 24-month construction loan (floating).
At month 18, converts to permanent loan (fixed or swapped).

Risk: If rates rise during construction, the permanent loan is more expensive.

Hedge: Purchase a payer swaption at month 0 with 18-month expiry into a 7-year swap.
  Cost: ~$150,000
  Benefit: If rates rise 100bps during construction, saves approximately:
    $19M * 0.01 * 5.5 (duration of 7yr swap) = $1,045,000 in PV terms

  Risk/reward: $150K premium vs ~$1M savings in a rising rate scenario.
```

---

## 6. Hedging Cost Impact on Deal Returns

### Worked Example: $30M Deal with Hedging

```
Base case (no hedge, current rates):
  Floating rate: SOFR (4.50%) + 2.50% = 7.00%
  Annual DS: $19M * 0.07 = $1,330,000 (IO)
  Equity CF Y1: $1,800,000 - $1,330,000 = $470,000
  Equity IRR (5yr): 12.7%

With rate cap ($133K upfront, 4.00% strike):
  Amortized cap cost: $44,333/year
  Max rate: 6.50%
  Expected DS (rates stay at 4.50%): $1,330,000 + $44,333 cap amort = $1,374,333
  Equity CF Y1: $1,800,000 - $1,374,333 = $425,667
  Equity IRR: 12.2% (base case) to 11.0% (rates at cap) to 14.5% (rates drop to 3%)

With swap (3.80% fixed):
  All-in rate: 6.30%
  Annual DS: $19M * 0.063 = $1,197,000
  Equity CF Y1: $1,800,000 - $1,197,000 = $603,000
  Equity IRR: 14.1% (locked, regardless of rate moves)

With collar (4.00%/3.25%):
  Rate band: 5.75% to 6.50%
  Expected DS: $1,235,000 to $1,330,000
  Equity IRR: 12.2% to 13.5% (bounded)
```

The swap produces the highest IRR in this example because the swap rate (3.80%) is below the current SOFR (4.50%). The swap effectively "buys" an expected rate decline embedded in the forward curve.
