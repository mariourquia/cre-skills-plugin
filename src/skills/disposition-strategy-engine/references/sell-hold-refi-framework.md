# Sell vs Hold vs Refinance Decision Framework

## Core Principle

The decision to sell, hold, or refinance is a capital allocation question. The right answer maximizes risk-adjusted returns on the equity currently trapped in the asset. Sunk costs are irrelevant. The only question: "Is this the best use of my equity today?"

## Marginal Return on Equity (MROE)

The single most important metric for disposition decisions.

### Formula
```
MROE = Incremental Cash Flow / Equity Invested in the Asset

Where:
  Incremental Cash Flow = Next-year projected NOI after debt service
  Equity Invested = Current market value - Outstanding debt (i.e., liquidation equity)
```

### Interpretation
- MROE > Target IRR: Hold. The asset is still earning above your hurdle rate on trapped equity.
- MROE < Target IRR: Sell or refinance. The equity is earning below your opportunity cost.
- MROE declining year-over-year: Even if above target, the trend signals diminishing returns. Plan exit timeline.

### Why MROE, Not IRR or ROE?

IRR looks backward -- it measures what the deal has already done. MROE looks forward -- it measures what the deal will do next year per dollar of equity currently at risk. A deal with a great historical IRR but 4% MROE is a sell if your target is 12%.

## Tax Friction

Selling triggers tax. Holding or refinancing does not. Tax friction is the single biggest reason investors hold too long.

### Tax Components on Disposition

| Component | Rate (2025-2026) | Calculation |
|---|---|---|
| Depreciation recapture | 25% (Section 1250) | Accumulated depreciation x 25% |
| Capital gains (federal) | 20% (top bracket) | (Sale price - adjusted basis) x 20% |
| Net investment income tax | 3.8% | Applies to capital gains for high earners |
| State income tax | 0-13.3% (varies) | State-specific, some states exempt CRE gains |

### After-Tax Equity Calculation
```
Gross Sale Proceeds          $10,000,000
- Selling costs (3-5%)       -$400,000
- Mortgage payoff             -$6,000,000
= Pre-tax equity              $3,600,000
- Depreciation recapture      -$375,000    ($1,500,000 accum depr x 25%)
- Capital gains tax            -$476,000   ($2,000,000 gain x 23.8%)
- State tax (est 5%)          -$100,000
= After-tax equity             $2,649,000

Tax friction: ($3,600,000 - $2,649,000) / $3,600,000 = 26.4%
```

### Tax Mitigation Strategies

| Strategy | Mechanism | Complexity | Savings |
|---|---|---|---|
| 1031 Exchange | Defer all taxes by reinvesting in like-kind | Medium | 100% deferral |
| Installment sale | Spread gains over payment period | Low | Time value + bracket mgmt |
| Opportunity Zone | Invest gains in QOZ fund | High | Partial deferral + exclusion |
| Charitable remainder trust | Donate to CRT, receive annuity | High | Avoid capital gains |
| DST (Delaware Statutory Trust) | 1031 into passive fractional | Medium | 100% deferral |
| Cost segregation (pre-sale) | Accelerate depreciation to offset gains | Medium | Partial offset |

## Reinvestment Assumption

The sell decision only makes sense if the reinvested proceeds earn more than the held asset. Model explicitly.

```
Sell Scenario:
  After-tax equity: $2,649,000
  Reinvestment IRR target: 15%
  5-year reinvestment value: $2,649,000 x (1.15)^5 = $5,327,000

Hold Scenario:
  Current equity in asset: $3,600,000 (pre-tax)
  MROE: 8%
  5-year hold value: $3,600,000 x (1.08)^5 = $5,290,000
  Less: tax on eventual sale = ~$950,000
  After-tax hold value: $4,340,000

Sell and reinvest wins: $5,327,000 > $4,340,000
But only if you actually achieve 15% IRR on reinvestment.
```

**The reinvestment assumption is the most commonly abused variable.** Investors assume they will find a better deal. Often they end up in cash for 12 months, deploy into a comparable deal, and lose the tax deferral benefit.

## Refinance as Third Option

Refinancing extracts equity without triggering tax. It is the optimal choice when:
1. MROE is moderate (8-12%) -- not bad enough to sell, not great enough to hold without leverage reset
2. Significant equity has built up (LTV has dropped below 50%)
3. Rate environment allows cash-out at reasonable terms
4. Reinvestment pipeline is active (you have identified deployment targets)

### Refinance Decision Checklist
- [ ] Current LTV has dropped below 55% (equity buildup justifies extraction)
- [ ] Cash-out refinance LTV achievable at 70-75%
- [ ] New debt service does not push DSCR below 1.25x
- [ ] Rate on new loan does not eliminate cash-on-cash yield
- [ ] Identified reinvestment target for extracted equity
- [ ] Prepayment penalty on existing loan is acceptable (defeasance, yield maintenance, or open period)
- [ ] Remaining hold period justifies new loan term and structure

### Cash-Out Refinance Math
```
Current value:        $10,000,000
Existing loan:        $6,000,000 (60% LTV)
New loan at 70% LTV:  $7,000,000
Cash extracted:        $1,000,000

New debt service:     $7,000,000 x 6.5% / 12 = $37,917/mo (IO)
                      vs old: $6,000,000 x 5.5% / 12 = $27,500/mo (IO)
Incremental cost:     $10,417/mo = $125,000/yr

Extracted equity reinvested at 15%: $150,000/yr return
Net benefit: $150,000 - $125,000 = $25,000/yr positive arbitrage
Plus: no tax triggered on extraction
```

## Decision Matrix: Worked Example

**Asset Profile:**
- 200-unit multifamily, Phoenix, acquired 2021 for $28M ($140k/unit)
- Current value: $42M ($210k/unit) based on recent comps
- Existing loan: $21M, 5.25% fixed, matures 2028, no prepay after 2026
- Current NOI: $2,940,000 (7.0% yield on cost, 5.6% cap on current value)
- Accumulated depreciation: $3,200,000
- Renovation complete, stabilized at 95% occupancy
- Fund target IRR: 14%

### Scenario Analysis

```
SCENARIO A: SELL
  Gross proceeds:           $42,000,000
  Selling costs (4%):       -$1,680,000
  Loan payoff:              -$21,000,000
  Pre-tax equity:           $19,320,000
  Depreciation recapture:   -$800,000   ($3.2M x 25%)
  Capital gains tax:        -$2,523,000 (($42M-$1.68M-$28M+$3.2M) x 23.8%)
  State tax (AZ 2.5%):     -$387,000
  After-tax equity:         $15,610,000
  IRR since acquisition:    28.4% (5-year hold, inclusive of cash flow)

  Reinvestment required:    $15,610,000 at 14% target
  Pipeline availability:    2 identified deals totaling $38M

SCENARIO B: HOLD 3 MORE YEARS
  Current equity (market):  $21,000,000
  MROE Year 1:             ($2,940,000 - $1,102,500 DS) / $21,000,000 = 8.7%
  MROE Year 2 (2% growth):  ($2,999,000 - $1,102,500) / $22,500,000 = 8.4%
  MROE Year 3 (2% growth):  ($3,059,000 - $1,102,500) / $24,000,000 = 8.2%

  MROE is declining and below 14% target every year.
  Hold value in 3 years:    ~$45M at 5.5% exit cap
  After-tax equity (yr 8):  ~$18,200,000
  Incremental IRR (yr 5-8): 10.2%

SCENARIO C: REFINANCE AND HOLD 3 YEARS
  Cash-out refi at 70% LTV: $29,400,000
  Payoff existing:           -$21,000,000
  Cash extracted:            $8,400,000
  New rate: 6.25%, IO        DS: $1,837,500/yr

  Property MROE post-refi:   ($2,940,000 - $1,837,500) / $12,600,000 = 8.7%
  Extracted equity deployed:  $8,400,000 at 14% target
  Combined MROE:             Blended ~11.8%

  No tax triggered.
  Flexibility to sell in 2028 at loan maturity.
```

### Decision
```
                    Sell        Hold        Refi + Hold
After-tax equity    $15.6M      N/A         N/A (no tax event)
5-yr forward value  $22.1M*     $18.2M      $20.8M**
Required execution  Find 14%    Do nothing  Find 14% for $8.4M
                    for $15.6M              + manage refi
Risk                Reinvestment Declining   Partial reinvestment
                    risk        MROE        risk, higher leverage

* Assumes 14% reinvestment achieved on $15.6M
** Assumes 14% on $8.4M extracted + property appreciation + refi cash flow

RECOMMENDATION: Refinance and Hold
- Extracts $8.4M tax-free
- Maintains upside in appreciating Phoenix market
- Smaller reinvestment target ($8.4M vs $15.6M) is more executable
- Defers $3.7M in taxes
- Decision to sell deferred to 2028 loan maturity (natural trigger)
- If Phoenix market softens, sell decision becomes easier with lower equity at risk
```

## Decision Triggers

Automatic sell triggers (override MROE analysis):
1. **Fund life constraint**: Must liquidate within 24 months of fund termination
2. **MROE below risk-free rate**: If the asset earns less than treasuries on a levered basis, sell immediately
3. **Structural market decline**: Secular demand shift (suburban office, obsolete retail) -- do not hold hoping for recovery
4. **Deferred capex exceeds renovation ROI**: When the next dollar of capex earns below cost of capital
5. **Concentration risk**: Single asset exceeds 30% of portfolio NAV

Automatic hold triggers:
1. **Lease-up in progress**: Selling mid-lease-up destroys value. Stabilize first
2. **Capital improvement in progress**: Complete the renovation, capture the premium, then decide
3. **Market dislocation**: Forced selling during dislocated markets crystallizes losses unnecessarily
4. **Below-market debt**: If existing loan is 200+ bps below market, the debt is an asset -- hold or assume

Refinance triggers:
1. **LTV has dropped below 55%**: Equity is lazy
2. **Existing loan approaching maturity**: Refinance proactively, extract equity, reset term
3. **Rate environment favorable**: Rates have dropped significantly below existing loan
4. **Identified deployment pipeline**: Only extract if you have a place to put the money
