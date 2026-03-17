# Reverse DCF Methodology for CRE Offering Memoranda

## Purpose

A reverse DCF starts with the broker's stated price and solves backward for the implied assumptions. Instead of asking "what is this asset worth?", you ask "what must I believe for this price to be justified?" Then compare those implied beliefs to market reality.

This is the single most powerful tool for cutting through OM marketing. If the implied assumptions are aggressive relative to observable data, the price is too high.

## Step-by-Step Methodology

### Step 1: Extract the Broker's Inputs

From the OM, extract these stated or implied figures:

| Input | Source in OM | Notes |
|-------|-------------|-------|
| Asking price | Cover page or pricing guidance | If a range, use midpoint |
| In-place NOI (T-12) | Financial summary or rent roll | Verify by reconstructing from rent roll + T-12 opex |
| Pro forma Year 1 NOI | Financial projections | Usually the "stabilized" NOI |
| Stated going-in cap rate | Executive summary | = Pro forma NOI / asking price |
| Projected rent growth | Assumptions page | Annual % or per-unit growth |
| Projected expense growth | Assumptions page | Annual % |
| Projected exit cap rate | Disposition assumptions | Usually Year 5 or Year 7 |
| Projected exit year | Return analysis | Typically Year 5, 7, or 10 |
| Financing assumptions | If included | LTV, rate, IO period, amort |
| Capex / renovation budget | If value-add | Total and per-unit |

### Step 2: Reconstruct the Broker's Cash Flows

Build a year-by-year cash flow using the broker's stated assumptions. Verify that your reconstruction matches the broker's IRR and equity multiple. If it does not match within 25bps on IRR and 0.05x on equity multiple, you are missing something -- usually a timing difference on capex or a financing nuance.

```
Year    Revenue     OpEx        NOI         Capex       NCF
 0      ---         ---         ---         (Equity)    (Equity)
 1      GPR - Vac   Stated      Rev - OpEx  Reserves    NOI - Capex
 2      Yr1 * (1+g) Yr1 * (1+e) ...         ...         ...
 ...
 N      ...         ...         ...         ...         NCF + Reversion
```

Reversion = Year N+1 NOI / Exit Cap Rate, less disposition costs (1-2%).

### Step 3: Solve for Implied Assumptions

Now the critical step. Hold price constant and solve for what each assumption must be for the deal to meet market return thresholds.

**Target return benchmarks (unlevered):**

| Asset Profile | Target Unlevered IRR | Target Cash-on-Cash (Stabilized) |
|--------------|---------------------|--------------------------------|
| Core | 6.0-7.5% | 4.5-5.5% |
| Core-plus | 7.5-9.5% | 5.0-6.5% |
| Value-add | 9.5-13.0% | 6.0-8.0% (post-stabilization) |
| Opportunistic | 13.0%+ | 8.0%+ (post-stabilization) |

**Target return benchmarks (levered, 60-65% LTV):**

| Asset Profile | Target Levered IRR | Target Equity Multiple (5yr) |
|--------------|-------------------|----------------------------|
| Core | 8.0-10.0% | 1.4-1.6x |
| Core-plus | 10.0-13.0% | 1.5-1.8x |
| Value-add | 13.0-18.0% | 1.7-2.2x |
| Opportunistic | 18.0%+ | 2.0x+ |

**Implied assumption isolation method:**

For each assumption, hold all others at market-reality levels and solve for the single variable that makes the deal pencil at target returns.

a) **Implied rent growth:** Hold expenses at CPI + 50bps, exit cap at going-in + 25bps, vacancy at submarket average. Solve for annual rent growth required to hit target IRR.

b) **Implied exit cap:** Hold rent growth at 10yr trailing average, expenses at CPI + 50bps, vacancy at submarket average. Solve for exit cap rate required to hit target IRR.

c) **Implied vacancy:** Hold rent growth and exit cap at market-reality levels. Solve for stabilized vacancy required to hit target IRR.

d) **Implied expense ratio:** Hold revenue assumptions at market-reality levels. Solve for expense ratio required to hit target IRR.

### Step 4: Compare Implied vs Reality

Build a comparison table:

| Assumption | Broker's Stated | Market Reality | Implied (to Hit Target IRR) | Delta (Implied - Reality) |
|-----------|----------------|---------------|---------------------------|--------------------------|
| Rent growth (annual) | ___% | ___% | ___% | ___bps |
| Expense growth (annual) | ___% | ___% | ___% | ___bps |
| Exit cap rate | ___% | ___% | ___% | ___bps |
| Stabilized vacancy | ___% | ___% | ___% | ___bps |
| Stabilized expense ratio | ___% | ___% | ___% | ___bps |

**Interpretation matrix:**

| Delta | Assessment |
|-------|-----------|
| Implied within +/- 50bps of reality | Reasonably priced for the return profile |
| Implied 50-150bps more aggressive than reality | Modest optimism baked in. Negotiate 5-10% price reduction. |
| Implied 150-300bps more aggressive than reality | Materially overpriced. Requires significant concession or walk. |
| Implied 300bps+ more aggressive than reality | Broker fantasy. Walk unless distressed basis or unique thesis. |

### Step 5: Sensitivity and Scenario Analysis

Run a 2-variable sensitivity table (rent growth x exit cap) with your base case and +/- 1 standard deviation:

```
                    Exit Cap Rate
                4.75%   5.00%   5.25%   5.50%   5.75%
Rent      2.0%  ___     ___     ___     ___     ___
Growth    2.5%  ___     ___     ___     ___     ___
          3.0%  ___     ___     ___     ___     ___
          3.5%  ___     ___     ___     ___     ___
          4.0%  ___     ___     ___     ___     ___
```

Each cell contains the levered IRR. Shade cells green (above target), yellow (within 200bps of target), red (below target by 200bps+).

Count the green cells. If fewer than 40% of scenarios meet target returns, the deal has an unfavorable risk/reward skew at the asking price.

---

## Worked Example: Exposing an Aggressive OM

### The Setup

A broker sends an OM for a 180-unit Class B garden-style apartment complex in Raleigh, NC.

**Broker's stated assumptions:**

| Input | Broker's Number |
|-------|----------------|
| Asking price | $34,200,000 ($190,000/unit) |
| T-12 NOI | $1,710,000 (5.00% in-place cap) |
| Pro forma Year 1 NOI | $1,881,000 (5.50% "stabilized" cap) |
| Annual rent growth | 4.0% |
| Annual expense growth | 2.5% |
| Exit cap (Year 5) | 4.75% |
| Stabilized vacancy | 4.0% |
| Capex reserves | $300/unit/year |
| **Broker's levered IRR** | **16.2%** |
| **Broker's equity multiple** | **2.1x** |

Financing: 65% LTV, 6.0% rate, 2yr IO then 30yr amort.

### Step 1-2: Reconstruct Cash Flows

Reconstructing with broker's assumptions:

```
Year   Revenue      OpEx        NOI          NCF
 1     $3,360,000   $1,479,000  $1,881,000   $1,827,000
 2     $3,494,000   $1,516,000  $1,978,000   $1,924,000
 3     $3,634,000   $1,554,000  $2,080,000   $2,026,000
 4     $3,780,000   $1,593,000  $2,187,000   $2,133,000
 5     $3,931,000   $1,633,000  $2,298,000   $2,244,000

Year 5 Reversion: $2,398,000 / 4.75% = $50,484,000
Less 2% disposition costs = $49,474,000
```

Levered IRR: 16.3%. Close enough to broker's 16.2% -- reconstruction validated.

### Step 3: Solve for Implied Assumptions

Now replace broker's assumptions with market reality and see what breaks.

**Market reality for Raleigh Class B garden-style:**

| Input | Market Reality |
|-------|---------------|
| Trailing 10yr rent growth (Raleigh MF) | 3.0% |
| CPI + 50bps (expense growth) | 3.5% |
| Submarket vacancy (5yr avg) | 6.5% |
| Appropriate exit cap (going-in + 25bps) | 5.25% |
| Capex reserves (1998 vintage) | $800/unit/year |

**Cash flows under market-reality assumptions:**

First, adjust Year 1 NOI: the broker shows a $171K jump from T-12 to pro forma. Investigating the rent roll reveals $95K of loss-to-lease capture (legitimate) and $76K from reducing vacancy from 6.8% actual to 4.0% pro forma (aggressive). At 6.5% stabilized vacancy, the legitimate Year 1 adjustment is only $95K.

```
Year   Revenue      OpEx        NOI          NCF
 1     $3,278,000   $1,519,000  $1,759,000   $1,615,000
 2     $3,376,000   $1,572,000  $1,804,000   $1,660,000
 3     $3,477,000   $1,627,000  $1,850,000   $1,706,000
 4     $3,582,000   $1,684,000  $1,898,000   $1,754,000
 5     $3,689,000   $1,743,000  $1,946,000   $1,802,000

Year 5 Reversion: $2,004,000 / 5.25% = $38,171,000
Less 2% disposition costs = $37,408,000
```

**Reality-adjusted levered IRR: 8.7%**
**Reality-adjusted equity multiple: 1.45x**

The deal went from a 16.2% levered IRR to 8.7%. That is a core return, not value-add. At the asking price, you are paying for perfection and getting average.

### Step 4: The Comparison Table

| Assumption | Broker | Reality | Delta | NOI Impact (Yr 5) |
|-----------|--------|---------|-------|--------------------|
| Rent growth | 4.0% | 3.0% | -100bps | -$176,000 |
| Expense growth | 2.5% | 3.5% | +100bps | -$88,000 |
| Stabilized vacancy | 4.0% | 6.5% | +250bps | -$96,000 |
| Exit cap | 4.75% | 5.25% | +50bps | N/A (exit value impact: -$12.3M) |
| Capex reserves | $300/unit | $800/unit | +$500/unit | -$90,000 |
| **Total Year 5 NOI impact** | | | | **-$450,000** |
| **Total exit value impact** | | | | **-$12,066,000** |

### Step 5: What Price Makes This Work?

At market-reality assumptions, to achieve a 13% levered IRR (value-add target), the price needs to be approximately $27,500,000 ($153K/unit). That is a 20% discount to the asking price.

**The conversation with the broker:** "We see $27.5M of value. Here is our assumption set with supporting data. We are happy to discuss where our views diverge."

### Key Takeaway

The broker's assumptions collectively overstated value by $6.7M (20%). No single assumption was outrageous, but each small optimism compounded:

- Rent growth: +100bps above trailing 10yr average
- Expense growth: -100bps below CPI (implies real deflation)
- Vacancy: 250bps below submarket average
- Exit cap: 50bps of compression (no justification)
- Capex: $500/unit below institutional standard for vintage

This is the standard OM playbook. The reverse DCF exposes it quantitatively, arming you with a defensible counter-offer backed by market data rather than gut feel.
