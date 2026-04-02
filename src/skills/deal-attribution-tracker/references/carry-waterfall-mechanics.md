# Carry Waterfall Mechanics
# Reference for deal-attribution-tracker skill
# Defines American and European waterfall structures with worked examples
# covering 5+ deals showing interaction effects, netting, and clawback

---

## Overview

A carry waterfall is the contractual sequence of cash flow allocations between LPs and the GP. It determines when and how much carried interest the GP earns. The two primary structures -- American (deal-by-deal) and European (whole-fund) -- produce dramatically different GP economics in funds with mixed deal outcomes.

---

## American Waterfall (Deal-by-Deal)

### Mechanics

Under an American waterfall, the carry calculation is performed independently for each deal. The GP earns carried interest on profitable deals without waiting for the entire fund to clear its hurdle.

```
FOR EACH DEAL (independently):
  Tier 1: Return of LP Capital
    LP receives 100% of distributions until full invested capital is returned
    GP co-invest receives same treatment on GP's pro-rata capital

  Tier 2: Preferred Return
    LP receives distributions until cumulative IRR from investment date = hurdle rate
    Pref accrues on unreturned capital only (compound IRR method)
    Formula: Pref = Invested Capital * ((1 + hurdle_rate)^hold_years - 1)

  Tier 3: GP Catch-Up
    100% catch-up: GP receives 100% of distributions until GP total carry =
      carry_rate * (LP pref + LP capital + deal profit)
    50/50 catch-up: LP and GP split 50/50 until GP carry % of total profit
      reaches carry_rate
    No catch-up: proceeds directly to Tier 4

  Tier 4: Residual Split
    Remaining distributions split: (1 - carry_rate) to LP, carry_rate to GP
```

**Key property of American waterfall:** GP accumulates carry across deals independently. If Deal A generates $10M carry and Deal B generates a $3M loss (no carry), the GP keeps the $10M from Deal A unless a clawback is triggered.

---

### Worked Example: 5-Deal American Waterfall Fund

**Fund parameters:**
- Fund size: $250M LP committed
- GP commitment: 2% ($5.1M, or approximately $5M rounded)
- Preferred return: 8% IRR (compound)
- Carry rate: 20%
- Catch-up: 100% GP
- Waterfall type: American (deal-by-deal)
- All deals fully realized for simplicity

**Deal data:**

| Deal | Invested ($M) | Total Distributions ($M) | Hold Period (years) | Gross MOIC |
|------|--------------|--------------------------|---------------------|------------|
| Deal 1 (Warehouse) | 40 | 88 | 4.5 | 2.20x |
| Deal 2 (Apartment) | 55 | 110 | 5.0 | 2.00x |
| Deal 3 (Office)    | 45 | 50 | 4.0 | 1.11x |
| Deal 4 (Retail)    | 35 | 28 | 3.5 | 0.80x |
| Deal 5 (Industrial)| 50 | 107 | 5.5 | 2.14x |

**Step-by-step waterfall for each deal:**

#### Deal 1: Warehouse ($40M invested, $88M distributions, 4.5-year hold)

```
Tier 1 -- LP Return of Capital:
  LP receives $40M (first $40M of distributions)

Tier 2 -- LP Preferred Return:
  Pref = $40M * ((1.08)^4.5 - 1) = $40M * 0.4233 = $16.93M
  LP receives $16.93M (cumulative distributions now $56.93M)

Tier 3 -- GP Catch-Up (100%):
  Total profit above pref = $88M - $40M - $16.93M = $31.07M
  GP catch-up target = carry_rate / (1 - carry_rate) * total LP receipts so far
    = 0.20 / 0.80 * ($40M + $16.93M) = $14.23M
  GP receives $14.23M (100% of next $14.23M)
  Remaining profit after catch-up: $31.07M - $14.23M = $16.84M

Tier 4 -- Residual Split:
  LP receives: $16.84M * 80% = $13.47M
  GP receives: $16.84M * 20% = $3.37M

DEAL 1 SUMMARY:
  LP: $40M + $16.93M + $13.47M = $70.40M
  GP carry: $14.23M + $3.37M = $17.60M
  Total: $88.00M (checks out)
  GP carry as % of deal profit: $17.60M / $48.00M = 36.7%
    (high because catch-up at 100% on strong return)
```

#### Deal 2: Apartment ($55M invested, $110M distributions, 5.0-year hold)

```
Tier 1 -- LP Return of Capital: $55M

Tier 2 -- LP Preferred Return:
  Pref = $55M * ((1.08)^5.0 - 1) = $55M * 0.4693 = $25.81M

Tier 3 -- GP Catch-Up:
  Profit above pref = $110M - $55M - $25.81M = $29.19M
  Catch-up target = 0.20/0.80 * ($55M + $25.81M) = $20.20M
  GP receives $20.20M
  Remaining: $29.19M - $20.20M = $8.99M

Tier 4 -- Residual Split:
  LP: $8.99M * 80% = $7.19M
  GP: $8.99M * 20% = $1.80M

DEAL 2 SUMMARY:
  LP: $55M + $25.81M + $7.19M = $88.00M
  GP carry: $20.20M + $1.80M = $22.00M
  Total: $110.00M (checks)
  GP carry as % of deal profit: $22.00M / $55.00M = 40.0%
```

#### Deal 3: Office ($45M invested, $50M distributions, 4.0-year hold)

```
Tier 1 -- LP Return of Capital: $45M (first $45M)

Tier 2 -- LP Preferred Return:
  Pref = $45M * ((1.08)^4.0 - 1) = $45M * 0.3605 = $16.22M
  But total distributions = $50M; after capital return only $5M remains.
  LP pref accrued = $16.22M but only $5M available
  LP receives $5M (partial pref recovery)
  PREF NOT FULLY RECOVERED -- no carry on this deal

DEAL 3 SUMMARY:
  LP: $45M + $5M = $50M (entire proceeds to LP)
  GP carry: $0
  LP shortfall vs full pref: $11.22M (LP did not receive full preferred return)
  Note: Under American waterfall, this shortfall does NOT offset carry on Deals 1-2
```

#### Deal 4: Retail ($35M invested, $28M distributions, 3.5-year hold)

```
Tier 1 -- LP Return of Capital:
  Only $28M available; LP recovers $28M (partial)
  LP capital shortfall: $35M - $28M = $7M not returned

DEAL 4 SUMMARY:
  LP: $28M (all proceeds; capital not fully returned)
  GP carry: $0
  LP principal loss: $7M
  Note: Under American waterfall, this loss does NOT claw back Deals 1-2 carry
    unless a clawback clause is triggered
```

#### Deal 5: Industrial ($50M invested, $107M distributions, 5.5-year hold)

```
Tier 1 -- LP Return of Capital: $50M

Tier 2 -- LP Preferred Return:
  Pref = $50M * ((1.08)^5.5 - 1) = $50M * 0.5869 = $29.34M

Tier 3 -- GP Catch-Up:
  Profit above pref = $107M - $50M - $29.34M = $27.66M
  Catch-up target = 0.20/0.80 * ($50M + $29.34M) = $19.84M
  GP receives $19.84M
  Remaining: $27.66M - $19.84M = $7.82M

Tier 4 -- Residual Split:
  LP: $7.82M * 80% = $6.26M
  GP: $7.82M * 20% = $1.56M

DEAL 5 SUMMARY:
  LP: $50M + $29.34M + $6.26M = $85.60M
  GP carry: $19.84M + $1.56M = $21.40M
  Total: $107.00M (checks)
```

**Fund-level American waterfall summary:**

```
FUND SUMMARY (American Waterfall):
Deal       | Invested | Distributions | GP Carry | LP Net   | Deal MOIC
-----------|----------|---------------|----------|----------|----------
Deal 1     | $40M     | $88M          | $17.60M  | $70.40M  | 2.20x
Deal 2     | $55M     | $110M         | $22.00M  | $88.00M  | 2.00x
Deal 3     | $45M     | $50M          | $0       | $50.00M  | 1.11x
Deal 4     | $35M     | $28M          | $0       | $28.00M  | 0.80x
Deal 5     | $50M     | $107M         | $21.40M  | $85.60M  | 2.14x

FUND TOTAL:
  Total Invested:       $225M
  Total Distributions:  $383M
  GP Carry Distributed: $61.00M
  LP Net Proceeds:      $322.00M

  Fund DPI (LP):        $322M / $225M = 1.43x (net of carry)
  Fund DPI (gross):     $383M / $225M = 1.70x (before carry)
  LP Net Return:        ~11.2% IRR (approximate, depends on timing)
```

**Clawback analysis:**

```
Under American waterfall, GP has earned $61M carry on Deals 1, 2, and 5.
Deals 3 and 4 had shortfalls: Deal 3 missed pref by $11.22M; Deal 4 had $7M capital loss.

QUESTION: Should the GP have earned $61M carry on a whole-fund basis?

Whole-fund carry calculation (European method for comparison):
  Total proceeds: $383M
  Total invested: $225M
  Total pref accrual (average 4.9-year hold on $225M at 8%): approximately $93M
  Profit above pref: $383M - $225M - $93M = $65M
  Whole-fund carry: 20% * $65M = $13M

CLAWBACK EXPOSURE: $61M distributed - $13M earned (whole-fund) = $48M
  The GP distributed $48M more carry under American waterfall
  than it would have earned under European waterfall.

KEY INSIGHT: This is the LP cost of an American waterfall in a mixed-result fund.
  The GP earned outsized carry on Deal 1, 2, and 5 before losses on 3 and 4 were known.
  LPs must negotiate strong clawback provisions and escrow requirements.
```

---

## European Waterfall (Whole-Fund)

### Mechanics

Under a European waterfall, carry is calculated on the entire fund, not deal-by-deal. The LP must receive return of ALL invested capital across the entire fund, PLUS preferred return on all capital, before the GP earns a single dollar of carry.

```
STEP 1: Return of All LP Capital
  LP receives all contributed capital across all deals before GP earns carry

STEP 2: Preferred Return on All Capital
  LP pref accrues on each capital call from the call date
  Total pref = sum over all calls of (call_amount * ((1+pref)^years - 1))
  LP receives this total pref before GP catch-up begins

STEP 3: GP Catch-Up
  Same mechanics as American, but applied to fund-level aggregate profits

STEP 4: Residual Split
  Remaining profits split (1 - carry_rate) LP, carry_rate GP
```

### Worked Example: Same 5 Deals Under European Waterfall

**Same deal data as above.**

```
EUROPEAN WATERFALL CALCULATION:

Total LP invested: $225M
Total distributions: $383M
Total preferred return accrual (varies by deal timing -- simplified to 4.9-year average):
  $225M * ((1.08)^4.9 - 1) = $225M * 0.459 = $103.3M

LP Total Required Before Carry:
  Return of capital: $225.0M
  Preferred return:  $103.3M
  Total LP requirement: $328.3M

Total available for distribution: $383M
LP receives first $328.3M: LP is made whole with pref

Remaining for carry calculation: $383M - $328.3M = $54.7M

GP Catch-Up (100%):
  Catch-up target = 0.20/0.80 * $328.3M = $82.1M
  But only $54.7M available above pref -- entire $54.7M goes to GP catch-up first
  Remaining after catch-up: $0 (GP has not yet fully caught up)
  Catch-up target not fully reached; deal with shortfall in Tier 4

  Wait -- re-examine: catch-up formula is:
    GP catch-up = min(available_profit, carry_rate * total_pref_inclusive_profits / (1 - carry_rate))
    = min($54.7M, 0.20 * ($328.3M + $54.7M) / 0.80)
    = min($54.7M, 0.25 * $383M)
    = min($54.7M, $95.75M)
    = $54.7M (catch-up not completed; all remaining profit goes to GP)
  Remaining for residual split: $0 (catch-up absorbs all)

  GP Carry (European): $54.7M
  Residual split (LP/GP): $0 (nothing left after catch-up)

LP net: $328.3M
GP carry: $54.7M
Total: $383M (checks)

NOTE: Under European waterfall, GP earns $54.7M carry (vs $61.0M American).
  Difference: $6.3M less for GP under European.
  This example is relatively close because most deals performed well.
  In a fund with more losers, the difference would be much larger.
```

---

## Comparison: American vs European in a Distressed Portfolio

To illustrate the maximum impact of waterfall type, consider a fund where half the deals fail:

```
DISTRESSED FUND (hypothetical):
  Deal A (Winner): $50M invested, $130M distributions (2.60x, 5-year hold)
  Deal B (Loser):  $50M invested, $30M distributions (0.60x, 4-year hold)
  Deal C (Winner): $50M invested, $120M distributions (2.40x, 5-year hold)
  Deal D (Loser):  $50M invested, $35M distributions (0.70x, 4-year hold)
  Deal E (Flat):   $50M invested, $65M distributions (1.30x, 5-year hold)

Total: $250M invested, $380M distributions

AMERICAN WATERFALL CARRY (deal-by-deal):
  Deal A carry: ~$28M
  Deal B carry: $0 (below pref)
  Deal C carry: ~$24M
  Deal D carry: $0 (below pref)
  Deal E carry: $3M (just above pref)
  Total GP carry: ~$55M

EUROPEAN WATERFALL CARRY (whole-fund):
  Total pref on $250M over ~4.8 years: ~$98M
  Total proceeds: $380M
  Available for carry: $380M - $250M - $98M = $32M
  GP carry: ~$8M (after catch-up dynamics)

DIFFERENCE: American generates ~$47M MORE carry for the GP in this scenario.
  This is the alignment gap between the two waterfall structures.
  LPs strongly prefer European waterfalls in strategies with high return dispersion.
```

---

## Clawback Provisions

### Standard Clawback Language

A clawback right gives LPs the right to recover carry already distributed to the GP if the fund's overall returns, at termination, do not justify the carry paid.

```
TRIGGER CONDITIONS:
  1. Fund termination (mandatory in most LPAs)
  2. Interim test dates (some LPAs require annual or biennial recalculation)
  3. GP key person event or removal (may accelerate clawback calculation)

CLAWBACK FORMULA:
  Clawback Amount = max(0,
    Total Carry Distributed to GP
    - Total Carry GP Should Have Earned on Whole-Fund Basis)

ESCROW REQUIREMENT:
  Market standard: 20-30% of carry distributions held in escrow
  Release: typically after clawback period expires (often 2 years post-fund)
  Investment: escrow usually invested in government bonds; income to GP

LIMITATIONS:
  1. GP escrow may not cover full clawback if fund has massive underperformance
  2. GP principal wealth may be illiquid (invested in other deals)
  3. Individual GP principals' personal liability varies by LPA structure
  4. Tax gross-up: GP must return pre-tax carry but may have paid taxes;
     some LPAs require GP to return only net-of-tax carry
     (LP unfavorable -- reduces effective clawback coverage)
```

### Clawback Security Options

| Security Type | Coverage | LP-Favorability | Notes |
|---------------|----------|-----------------|-------|
| Cash escrow (20% of carry) | Limited | Moderate | Standard; insufficient for large clawbacks |
| Cash escrow (30-50% of carry) | Better | Good | Negotiated by institutional LPs |
| Letter of credit | Strong | Good | GP cost is meaningful; rare |
| GP personal guarantee | Depends | Variable | Only valuable if GP is creditworthy |
| GP fund co-invest withheld | Limited | Moderate | Withholds co-invest until clawback liability cured |

---

## Catch-Up Mechanics Deep Dive

The catch-up provision determines the speed at which the GP reaches its target carry split after the LP preferred return is paid.

### 100% GP Catch-Up (Most Common in CRE)

```
After LP receives pref, 100% of all remaining distributions go to GP
until the GP has received exactly carry_rate / (1 - carry_rate) times
what the LP has received in pref.

Example ($100M fund, 8% pref, 20% carry, European, 5-year, 1.7x TVPI):
  LP capital: $100M, LP pref: $46.9M (8% x 5 years compound)
  Total profit: $170M - $100M = $70M
  Profit above pref: $70M - $46.9M = $23.1M

  GP catch-up = 0.25 * total LP receipts = 0.25 * ($100M + $46.9M) = $36.7M
  But only $23.1M available above pref; catch-up not complete
  GP receives all $23.1M

  Final split: LP = $146.9M ($100 + $46.9M + $0 residual), GP = $23.1M
  GP as % of total profit: $23.1M / $70M = 33%
    (GP earns more than 20% because catch-up captures 33% before residual is reached)
```

### 50/50 Catch-Up

```
After LP receives pref, profits split 50/50 between LP and GP until the GP's
cumulative share equals carry_rate * total profits.

Same example:
  After pref, $23.1M available
  50/50 split: LP $11.55M, GP $11.55M
  Check: GP total = $11.55M / $70M = 16.5% (below 20% target)
    Catch-up complete but GP is below target carry %
  Residual: $0 remaining (all profit consumed in catch-up)
  GP carry as % of profit: $11.55M / $70M = 16.5%
    (LP-favorable vs 100% catch-up)
```

### No Catch-Up

```
After LP receives pref, remaining profits split per target split (80/20) immediately.
GP never recovers the 20% of profits "earned" during the pref period.

Same example:
  After pref, $23.1M available
  80/20 split: LP $18.48M, GP $4.62M
  GP carry as % of profit: $4.62M / $70M = 6.6%
    (very LP-favorable; GP earns far less than 20% of profits)

NOTE: No catch-up is extremely rare in institutional CRE. It may appear in
debt funds or in manager-of-managers structures as an LP-favorable concession.
```

---

## Preferred Return Mechanics

### IRR-Based vs Multiple-Based Hurdle

**IRR-based hurdle (most common):**
```
Pref accrues as a compound IRR from each capital call date
Pref = Sum over all calls of: call_amount * ((1 + hurdle_rate)^years_outstanding - 1)

This method: time penalizes slow deployment and rewards fast returns
```

**Multiple-based hurdle (less common):**
```
LP must receive 1.0x return of capital before carry begins
No IRR accrual; simply capital recovery requirement
After capital recovery, all profits go through catch-up immediately

Useful in: shorter-duration debt funds, CLO equity strips
Less useful in: equity CRE where time value of capital matters
```

**Hybrid hurdle:**
```
Some LPAs use both: LP must receive return of capital (multiple hurdle) AND
an IRR on deployed capital (IRR hurdle). Both must be satisfied.
This is the most LP-favorable structure.
```

---

## Common Errors in Carry Calculations

1. **Simple interest vs compound interest on pref:** LPAs specify IRR-based (compound) pref. Using simple interest understates pref and overstates GP carry.

2. **Ignoring management fee netting:** Management fees paid from LP capital reduce the net invested capital base. Carry should be computed on the LP's net capital contribution, not gross capital.

3. **Recallable distributions:** If distributions are recallable (LP must return them if called again), they should not reduce the capital basis for preferred return calculation until non-recallable.

4. **Catch-up applied before capital recovery:** Catch-up only begins after capital AND pref are returned. Never apply catch-up to gross proceeds.

5. **GP co-invest pro-rata carry:** GP co-invest capital participates in deal returns but does not earn carry on itself (carry is only on LP capital). Some models incorrectly apply carry to total fund capital including GP commitment.
