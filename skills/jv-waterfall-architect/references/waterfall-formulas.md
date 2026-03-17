# JV Waterfall Formula Reference

Complete derivations, worked examples, and distribution mechanics for joint venture equity waterfalls. All examples use a baseline $10,000,000 JV equity investment with 90/10 LP/GP split and GP co-invest.

---

## 1. Preferred Return Calculations

### Notation

| Symbol | Definition |
|---|---|
| E | Invested equity (LP or GP share) |
| r_pref | Annual preferred return rate |
| t | Period (years) |
| D_t | Distributions received in period t |
| U_t | Unpaid (accrued) preferred at end of period t |

### Simple Preferred Return

Pref accrues on original invested capital only. Distributions reduce outstanding pref but do not reduce the base.

```
Annual pref accrual = E * r_pref
Cumulative pref owed at year t = E * r_pref * t - sum(D_pref_1..t)
```

### Compounded Preferred Return

Unpaid pref is added to the base, and future pref accrues on the growing balance. This is the most LP-friendly formulation.

```
Accrual_t = (E + U_{t-1}) * r_pref
U_t = U_{t-1} + Accrual_t - D_pref_t
```

If no distributions are made for 3 years on $9,000,000 LP equity at 8% compounded pref:

```
Year 1: Accrual = 9,000,000 * 0.08 = 720,000.  U_1 = 720,000
Year 2: Accrual = (9,000,000 + 720,000) * 0.08 = 777,600.  U_2 = 1,497,600
Year 3: Accrual = (9,000,000 + 1,497,600) * 0.08 = 839,808.  U_3 = 2,337,408
```

Compare simple pref over the same period:

```
Simple: 9,000,000 * 0.08 * 3 = 2,160,000
Compounded: 2,337,408
Difference: $177,408 (8.2% more owed to LP under compounding)
```

### Cumulative vs. Non-Cumulative

- **Cumulative**: Unpaid pref from prior periods carries forward. If year 1 cash flow is insufficient, the shortfall accrues and must be paid before any promote distributions.
- **Non-cumulative**: Only the current period pref must be satisfied. Shortfalls from prior periods do not carry forward.

Non-cumulative pref is rare in institutional JVs. It is GP-friendly and typically only seen in development deals where the GP negotiated favorable terms.

---

## 2. Promote Tiers and Distribution Mechanics

### Standard Multi-Tier Structure

A typical institutional waterfall distributes in this order:

```
Tier 1: Return of capital (ROC) -- pro-rata to LP and GP based on equity share
Tier 2: Preferred return -- pro-rata until cumulative pref is satisfied
Tier 3: GP catch-up -- 100% (or a high share) to GP until GP has received its promote share of Tiers 2+3
Tier 4: Residual split -- LP/GP split (e.g., 70/30 or 60/40) on remaining distributions
```

Multi-tier waterfalls add intermediate tiers between the pref and the final split:

```
Tier 1: ROC (pro-rata)
Tier 2: 8% pref (pro-rata)
Tier 3: GP catch-up to 20% of Tiers 2+3
Tier 4: 80/20 LP/GP split up to 12% IRR
Tier 5: 70/30 LP/GP split up to 18% IRR
Tier 6: 60/40 LP/GP split above 18% IRR
```

### Catch-Up Mechanics

The catch-up ensures the GP receives its promote share of all distributions above ROC, not just distributions above the catch-up threshold.

For an 8% pref with 20% GP promote and full (100%) catch-up:

```
Total distributable above ROC: $X
LP receives 8% pref: E_LP * 0.08 * t = $P
GP catch-up: GP receives 100% of next distributions until GP has received P * (20/80) = 0.25 * P

After catch-up, GP has received 20% of total (P + catch-up) distributions:
  GP_catchup = P * 0.25
  Verify: GP share = GP_catchup / (P + GP_catchup) = 0.25P / 1.25P = 20%. Correct.

Remaining: 80/20 split (or next tier split)
```

### Partial Catch-Up (50% Catch-Up)

Some structures use a partial catch-up where GP receives only 50% of distributions during the catch-up phase (rather than 100%):

```
LP receives pref: $P
During catch-up: LP gets 50%, GP gets 50% of each dollar
Catch-up continues until GP has 20% of all above-ROC distributions

Amount distributed during catch-up phase = P * (20/80) / (50% - 20%) = P * 0.25 / 0.30 = 0.833P
GP receives during catch-up: 0.833P * 0.50 = 0.417P
LP receives during catch-up: 0.833P * 0.50 = 0.417P

Verify: GP total = 0.417P. LP total = P + 0.417P = 1.417P.
GP share = 0.417P / (1.417P + 0.417P) = 0.417 / 1.833 = 22.7%...
```

Partial catch-ups do not perfectly achieve the target promote share. They are a compromise -- GP receives more than pro-rata during catch-up but less than 100%. Partial catch-ups are LP-friendly relative to full catch-ups.

---

## 3. Full $10M JV Worked Example

### Deal Terms

```
Total equity:     $10,000,000
LP equity (90%):  $9,000,000
GP equity (10%):  $1,000,000
Pref return:      8% simple, cumulative
Promote structure:
  Tier 1: Return of capital (pro-rata)
  Tier 2: 8% pref (pro-rata)
  Tier 3: 100% GP catch-up to 20% of Tiers 2+3
  Tier 4: 80/20 LP/GP split to 12% IRR
  Tier 5: 70/30 LP/GP split to 18% IRR
  Tier 6: 50/50 LP/GP split above 18% IRR
Hold period:      5 years
```

### Scenario A: 8% IRR ($14,693,281 total distributions)

At exactly 8% IRR, total distributions equal equity + cumulative pref.

```
Total distributions needed for 8% IRR (simple, 5 years):
  ROC:  $10,000,000
  Pref: $10,000,000 * 0.08 * 5 = $4,000,000
  Total: $14,000,000

Assume cash flows:
  Year 1-4: $400,000/year operating CF
  Year 5:   $400,000 CF + $12,400,000 reversion = $12,800,000
  Total:    $14,400,000

Distribution waterfall:
  Tier 1 (ROC): LP receives $9,000,000. GP receives $1,000,000.
  Tier 2 (Pref): LP pref = 9,000,000 * 0.08 * 5 = $3,600,000
                  GP pref = 1,000,000 * 0.08 * 5 = $400,000
  Remaining: $14,400,000 - $10,000,000 - $4,000,000 = $400,000
  Tier 3 (Catch-up): GP receives 100% until GP has 20% of above-ROC distributions.
    Above-ROC so far = $4,000,000 pref.
    GP has $400,000 of that (10% from pro-rata pref).
    GP needs 20% of total above-ROC = needs to reach a point where GP_above_ROC / total_above_ROC = 20%.
    Let C = catch-up amount (goes 100% to GP).
    GP_above_ROC = $400,000 + C
    Total_above_ROC = $4,000,000 + C
    Solve: (400,000 + C) / (4,000,000 + C) = 0.20
    400,000 + C = 800,000 + 0.20C
    0.80C = 400,000
    C = $500,000

  But only $400,000 remains. Catch-up is not fully satisfied.
  GP receives remaining $400,000 as catch-up.

Summary at 8% IRR:
  LP total: $9,000,000 + $3,600,000 = $12,600,000  (1.40x multiple)
  GP total: $1,000,000 + $400,000 + $400,000 = $1,800,000  (1.80x multiple)
  GP effective promote: ($400,000 catch-up) / $14,400,000 = 2.8% above pro-rata
```

### Scenario B: 12% IRR ($17,623,417 total distributions)

```
Assume cash flows yielding ~12% IRR:
  Year 1-4: $600,000/year
  Year 5:   $600,000 + $14,623,000 reversion = $15,223,000
  Total:    $17,623,000

Waterfall:
  Tier 1 (ROC):    LP: $9,000,000.  GP: $1,000,000.
  Tier 2 (Pref):   LP: $3,600,000.  GP: $400,000.
  Remaining after Tiers 1-2: $17,623,000 - $14,000,000 = $3,623,000

  Tier 3 (Catch-up):
    Need C = $500,000 (from Scenario A calculation). Sufficient funds.
    GP receives $500,000. Remaining: $3,123,000.
    Verify: GP above-ROC = $400,000 + $500,000 = $900,000.
    Total above-ROC through catch-up = $4,000,000 + $500,000 = $4,500,000.
    GP share: $900,000 / $4,500,000 = 20%. Correct.

  Tier 4 (80/20 up to 12% IRR):
    At 12% IRR, approximately all remaining $3,123,000 is in this tier.
    LP: $3,123,000 * 0.80 = $2,498,400
    GP: $3,123,000 * 0.20 = $624,600

Summary at 12% IRR:
  LP total: $9,000,000 + $3,600,000 + $2,498,400 = $15,098,400  (1.678x)
  GP total: $1,000,000 + $400,000 + $500,000 + $624,600 = $2,524,600  (2.525x)
  GP promoted share of above-ROC: ($500,000 + $624,600) / $7,623,000 = 14.8%
```

### Scenario C: 18% IRR ($22,877,578 total distributions)

```
Assume total distributions = $22,878,000

Waterfall:
  Tiers 1-3: Same as Scenario B.
    LP: $12,600,000 + $2,498,400 = $15,098,400 (through Tier 4 at 12% IRR breakpoint)
    GP: $1,000,000 + $400,000 + $500,000 + $624,600 = $2,524,600

  But we need the exact breakpoint for Tier 4 vs Tier 5.
  Total through 12% IRR breakpoint: $17,623,000 (from Scenario B).
  Remaining for Tier 5 (70/30): $22,878,000 - $17,623,000 = $5,255,000

  Tier 5 (70/30 up to 18% IRR):
    LP: $5,255,000 * 0.70 = $3,678,500
    GP: $5,255,000 * 0.30 = $1,576,500

Summary at 18% IRR:
  LP total: $15,098,400 + $3,678,500 = $18,776,900  (2.086x)
  GP total: $2,524,600 + $1,576,500 = $4,101,100  (4.101x)
  GP promoted share of above-ROC: ($500,000 + $624,600 + $1,576,500) / $12,878,000 = 21.0%
```

---

## 4. Clawback Mechanics

### Definition

A clawback provision requires the GP to return excess promote distributions if, at final liquidation, the LP has not received its full contractual return (ROC + pref).

### When Clawback Triggers

Clawback risk arises when:
1. Interim promote distributions were made based on periodic returns that exceeded the pref hurdle.
2. Later-period performance (particularly the reversion) is worse than projected.
3. The cumulative LP return falls below the pref threshold when final distributions are included.

### Worked Example

```
$10M JV, 90/10 LP/GP, 8% pref, 80/20 above pref.

Year 1-3: Strong cash flows. GP receives $300,000 in promote distributions.
Year 4: Property value declines. Sale proceeds = $8,500,000.

LP entitlement check:
  LP equity invested:        $9,000,000
  LP pref (4 years):         $2,880,000
  LP total entitlement:      $11,880,000

LP actually received:
  Years 1-3 cash flow share: $2,700,000 (estimated)
  Year 4 reversion share:    $8,500,000 * 0.90 = $7,650,000
  Total:                     $10,350,000

Shortfall: $11,880,000 - $10,350,000 = $1,530,000

Clawback: GP must return the lesser of:
  (a) Promote distributions received = $300,000
  (b) LP shortfall = $1,530,000

GP returns $300,000. LP shortfall is reduced to $1,230,000 (still underwater).
```

### Clawback Escrow

Most institutional JVs require the GP to escrow a portion of promote distributions (typically 20-50%) until final liquidation. This protects the LP against GP inability to fund a clawback.

```
If 30% escrow on $300,000 promote: $90,000 held in escrow.
At liquidation, if clawback triggers: escrow released to LP first.
If no clawback: escrow released to GP.
```

---

## 5. GP Co-Invest Requirements

### Standard Structures

| JV Type | GP Co-Invest % | Rationale |
|---|---|---|
| Institutional JV | 5-15% | GP alignment; typical 10% |
| Programmatic JV | 10-20% | Higher GP alignment for multiple deals |
| Development JV | 5-10% | GP brings expertise, LP brings capital |
| High-net-worth | 1-5% | Often more about GP sweat equity |

### Impact on Promote Economics

GP co-invest affects the promote calculation because the GP earns returns on two streams:
1. Pro-rata return on co-invested capital (same as LP per dollar)
2. Promote on total above-hurdle distributions

```
$10M JV, GP co-invests 10% ($1M), 8% pref, 80/20 promote.
Total distributions = $16,000,000 (1.6x multiple, ~10% IRR over 5 years).

GP return decomposition:
  Pro-rata ROC:      $1,000,000
  Pro-rata pref:     $1,000,000 * 0.08 * 5 = $400,000
  Catch-up:          $500,000
  Promote (80/20):   ($16M - $14M - $0.5M catch-up) * 0.20 = $300,000

GP total: $1,000,000 + $400,000 + $500,000 + $300,000 = $2,200,000
GP multiple on co-invest: 2.20x
LP total: $13,800,000
LP multiple: 13,800,000 / 9,000,000 = 1.533x
```

The GP earns 2.20x vs LP 1.53x. The promote creates significant return asymmetry that rewards GP for outperformance.

### Fiduciary Duty Considerations

When a GP co-invests, they have fiduciary obligations as both a co-investor and a manager. Conflicts arise when:
- GP controls disposition timing (sell early to lock promote vs. hold for LP upside)
- GP controls refinancing (pull equity out to return capital, triggering pref reset)
- GP allocates deal opportunities across multiple JVs

Institutional LPAs address these through LPAC oversight, co-investment allocation policies, and key-person provisions.

---

## 6. European vs. American Waterfall

### American (Deal-by-Deal)

Promote is calculated and distributed on each deal independently. GP can earn promote on Deal A even if Deal B is underwater.

```
Advantage: GP gets paid as deals monetize (faster promote realization)
Risk to LP: GP earns promote on winners while LP absorbs losses on losers
Mitigation: Clawback provision at fund level
```

### European (Whole-Fund / Portfolio)

Promote is calculated on aggregate portfolio returns. GP does not earn promote until the entire portfolio has returned LP capital plus pref.

```
Advantage: LP fully protected; GP only earns promote on true portfolio outperformance
Risk to GP: One bad deal can eliminate promote on entire fund
GP preference: American (faster, higher expected promote)
LP preference: European (full protection)
```

### Hybrid Structures

Most institutional funds use a hybrid:
- Return of capital computed on a whole-fund basis
- Preferred return computed on a whole-fund basis
- Promote distributed deal-by-deal with a clawback true-up at fund termination

This gives the GP some interim liquidity while protecting the LP at the portfolio level.
