# GP Scoring Rubric
# Reference for gp-performance-evaluator skill
# Defines the quantitative scoring framework for GP evaluation

---

## Overview

The GP Scorecard is a five-dimension scoring system that produces a weighted score between 1.0 and 5.0. Each dimension is scored independently on a 1-5 scale, then combined using the dimension weights to produce the overall score.

---

## Dimension 1: Returns (40% weight)

This is the most heavily weighted dimension because returns are the LP's primary objective.

### Scoring Criteria

| Score | Net IRR Percentile | DPI Percentile | TVPI Percentile | Pattern |
|-------|-------------------|----------------|-----------------|---------|
| 5 | Top decile (90th+) in at least 2 of 3 | Top quartile in all 3 | Top quartile in all 3 | Exceptional across metrics |
| 4 | Top quartile (75th+) in at least 2 of 3 | Top quartile in at least 2 | Top quartile in at least 2 | Strong, consistently above average |
| 3 | Second quartile (50-74th) in at least 2 | Above median in at least 2 | Above median in at least 2 | Average performer |
| 2 | Third quartile (25-49th) in at least 2 | Below median in at least 2 | Below median in at least 2 | Below average |
| 1 | Bottom quartile (<25th) in any metric | Bottom quartile in any | Bottom quartile in any | Material underperformance |

### Adjustment Factors

```
SUB-LINE ADJUSTMENT:
  If sub-line inflates IRR by > 200 bps:
    Use investment-date IRR for scoring, not as-reported IRR.
    If investment-date IRR drops the fund by one quartile: reduce score by 1.

VINTAGE CONTEXT:
  2019-2020 vintages: COVID disruption may temporarily depress metrics.
    Weight DPI more heavily than TVPI for these vintages (realized > paper).
  2021-2022 vintages: Rate shock may depress current marks.
    Weight deployment quality and deal pipeline over current TVPI.
  2023+ vintages: Too early for meaningful return scoring.
    Score as "N/A" and weight other dimensions more heavily.

DPI vs TVPI EMPHASIS:
  For funds in harvest phase (year 5+):
    DPI weight = 60%, TVPI weight = 40% of returns score.
    Rationale: Mature funds should be returning cash. High TVPI with low DPI
    suggests the GP is holding assets to inflate marks.
  For funds in deployment/early value creation (year 1-4):
    DPI weight = 20%, TVPI weight = 80%.
    Rationale: Early-stage funds cannot be judged on cash distributions.
```

---

## Dimension 2: Fee Economics (20% weight)

Fee economics measure the LP's cost of access. Even top-quartile GPs can be poor investments if fees consume too much of gross returns.

### Scoring Criteria

| Score | Gross-to-Net Spread | Total Fee Load | Fee Percentile | Pattern |
|-------|---------------------|----------------|----------------|---------|
| 5 | Below 25th percentile for strategy | Below 25th percentile | Most LP-favorable quartile | Exceptionally low fees |
| 4 | 25th-50th percentile | 25th-50th percentile | Second quartile | Below-market fees |
| 3 | 50th-75th percentile | 50th-75th percentile | Third quartile | Market fees |
| 2 | 75th-90th percentile | 75th-90th percentile | Fourth quartile | Above-market fees |
| 1 | Above 90th percentile | Above 90th percentile | Top decile | Excessive fees |

### Fee-Adjusted Performance Check

```
CRITICAL TEST:
  Compute GP's gross return percentile and net return percentile.
  If net percentile is lower than gross percentile by more than one quartile:
    The GP is capturing disproportionate value through fees.
    Reduce fee score by 1 point.

  Example:
    Gross IRR = 18.5% -> 70th percentile (top of second quartile)
    Net IRR = 13.8% -> 52nd percentile (bottom of second quartile)
    Difference = 18 percentile points -> within one quartile. Acceptable.

    Gross IRR = 22.0% -> 85th percentile (top quartile)
    Net IRR = 14.5% -> 55th percentile (second quartile)
    Difference = 30 percentile points -> more than one quartile. Fee score reduced.
```

---

## Dimension 3: Deal Quality (20% weight)

Deal quality measures whether fund performance is driven by broad portfolio strength (skill) or concentrated outliers (luck/concentration risk).

### Scoring Criteria

| Score | Gini Coefficient | Top Deal Contribution | Loss Ratio | Pattern |
|-------|------------------|----------------------|------------|---------|
| 5 | < 0.15 | Top deal < 15% of value | Loss ratio < 5% | Exceptional diversification and deal selection |
| 4 | 0.15-0.25 | Top deal < 20% | Loss ratio < 10% | Strong portfolio construction |
| 3 | 0.25-0.35 | Top deal < 25% | Loss ratio < 15% | Acceptable dispersion |
| 2 | 0.35-0.50 | Top deal 25-35% | Loss ratio 15-25% | Concentrated returns or elevated losses |
| 1 | > 0.50 | Top deal > 35% | Loss ratio > 25% | Fund performance depends on one or two deals |

### Special Cases

```
SINGLE-DEAL FUND PERFORMANCE:
  If removing the top deal drops fund TVPI below 1.5x (from above 1.5x):
    Maximum deal quality score = 2.
    Rationale: Fund performance is not repeatable without that specific deal.

HIGH LOSS RATIO WITH HIGH OVERALL RETURNS:
  If loss ratio > 20% but TVPI > 2.0x:
    Score = 2 (despite strong overall returns).
    Rationale: "Swing for the fences" strategy. Some will hit, many will miss.
    This is acceptable for opportunistic but concerning for value-add.

EARLY-STAGE FUND (< 5 deals realized):
  Insufficient data for reliable dispersion analysis.
  Score = 3 (neutral) unless clear pattern emerges.
  Note: "Insufficient realized deals for definitive dispersion analysis."
```

---

## Dimension 4: Alpha Generation (15% weight)

Alpha measures the GP's value-add beyond market returns and leverage effects. This is the most rigorous test of GP skill.

### Scoring Criteria

| Score | Annualized Alpha | Interpretation |
|-------|------------------|----------------|
| 5 | > 200 bps | Exceptional value creation. GP generates significant returns beyond market and leverage. |
| 4 | 100-200 bps | Strong alpha. GP consistently adds value through operations, asset selection, or timing. |
| 3 | 0-100 bps | Marginal alpha. GP adds some value but much of return comes from market and leverage. |
| 2 | -100 to 0 bps | Zero to negative alpha. GP is not adding value beyond market exposure and leverage. |
| 1 | < -100 bps | Value destruction. GP is underperforming what a passive market + leverage strategy would deliver. |

### Alpha Computation Methodology

```
PROPERTY-LEVEL ALPHA:
  Step 1: Compute actual property-level return (income + appreciation)
  Step 2: Compute expected property-level return from benchmark (NCREIF NPI by type/region)
  Step 3: Property alpha = actual - expected

LEVERAGE-ADJUSTED ALPHA:
  Step 4: Compute expected equity return at the GP's actual leverage level
    Expected Equity Return = Benchmark Property Return + (Benchmark Property Return - Cost of Debt) * (LTV / (1 - LTV))
  Step 5: Leverage-adjusted alpha = Actual Net Equity Return - Expected Equity Return

INTERPRETATION:
  Positive leverage-adjusted alpha: GP creates value beyond what leverage and market provide.
    Sources: better asset selection, better operations, better timing, better exit execution.
  Zero leverage-adjusted alpha: GP is a market participant, not a value creator.
    LP is paying fees for market exposure they could get cheaper.
  Negative leverage-adjusted alpha: GP destroys value.
    LP would be better off in a passive index or lower-cost vehicle.
```

---

## Dimension 5: Consistency (5% weight)

Consistency measures whether GP performance is repeatable across vintages. A single strong fund may be luck; consistent performance across multiple vintages indicates skill.

### Scoring Criteria

| Score | Quartile Pattern (across all prior funds) | Interpretation |
|-------|------------------------------------------|----------------|
| 5 | All prior funds top quartile | Exceptional consistency. Rare. |
| 4 | All prior funds top half, at least one top quartile | Strong consistency. GP maintains quality. |
| 3 | Mixed results, no bottom quartile fund | Average consistency. Some variation but no disasters. |
| 2 | One or more bottom-quartile funds | Inconsistent. GP has demonstrated the ability to underperform. |
| 1 | Declining trajectory (each successive fund worse) or multiple bottom quartile | Deteriorating quality. Negative trend is the strongest signal against re-up. |

### Minimum Fund History

```
1 prior fund: Consistency score = 3 (neutral -- insufficient data)
2 prior funds: Consistency score based on 2-fund pattern
3+ prior funds: Full consistency scoring with trend analysis
```

### Trend Direction

```
IMPROVING TRAJECTORY:
  Fund I: Q3 -> Fund II: Q2 -> Fund III: Q1
  Add +0.5 to consistency score (improvement is a positive signal)

STABLE TRAJECTORY:
  Fund I: Q2 -> Fund II: Q2 -> Fund III: Q2
  No adjustment (stable is acceptable)

DECLINING TRAJECTORY:
  Fund I: Q1 -> Fund II: Q2 -> Fund III: Q3
  Subtract -1.0 from consistency score (declining is the strongest negative signal)
  Declining trajectory with bottom-quartile latest fund: automatic score = 1
```

---

## Overall Score Calculation

```
Weighted Score = (Returns * 0.40) + (Fee Economics * 0.20) + (Deal Quality * 0.20) + (Alpha * 0.15) + (Consistency * 0.05)

VERDICT MAPPING:
  4.0-5.0: STRONG GP -- RE_UP signal
    GP demonstrates skill, competitive fees, broad deal quality, and consistency.
    Recommend commitment at or above current level.

  3.0-3.9: AVERAGE GP -- CONDITIONAL, need compelling thesis
    GP is competent but not differentiated. Re-up justified only if:
    (a) strategy thesis is uniquely compelling, or
    (b) portfolio fit is strong (fills an allocation gap), or
    (c) terms can be negotiated to below-market levels.

  2.0-2.9: WEAK GP -- REDUCE signal
    GP has material weaknesses in one or more dimensions.
    Complete current fund obligation but reduce or decline next fund.
    Explore alternative GPs for the allocation slot.

  1.0-1.9: POOR GP -- EXIT signal
    GP has failed on multiple dimensions.
    Explore secondary sale of current position.
    Do not commit to successor fund under any circumstances.
```

---

## Confidence Adjustments

The GP score comes with a confidence rating that reflects data quality:

```
CONFIDENCE DEDUCTIONS:
  Per missing metric (DPI, TVPI, IRR):     -5 points from 100
  Per unverified GP-reported metric:       -3 points
  No deal-level data available:            -15 points
  No prior fund data (first-time GP):      -20 points
  Sub-line usage unknown:                  -5 points
  Gross returns only (no net provided):    -10 points
  No cash flow data for verification:      -10 points
  Vintage benchmark not available:         -5 points

CONFIDENCE CATEGORIES:
  90-100: HIGH -- strong data, reliable scoring
  70-89:  MEDIUM -- adequate data, some gaps
  50-69:  LOW -- significant gaps, scoring is directional not precise
  <50:    VERY LOW -- insufficient data for reliable GP scoring
          Flag: "Scoring reflects limited available data. Request additional
          data before making commitment decision."
```

---

## Automatic Disqualification Triggers

Regardless of overall score, the following conditions trigger automatic FAIL:

1. **Fraud or material misrepresentation** in GP-reported data
2. **Regulatory enforcement action** (SEC, state) in prior 5 years
3. **Active litigation by LPs** alleging fiduciary breach
4. **Key person departure** without succession plan and without prior LP notification
5. **Bottom-decile performance** (below 10th percentile) in most recent fund
6. **NAV manipulation** suspected (valuation methodology changes without disclosure, marks inconsistent with market evidence)
7. **Unreported related-party transactions** that benefit GP at fund expense
