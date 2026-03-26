# Distribution Fitting Guide for CRE Monte Carlo Simulation

## Purpose

This guide provides the methodology for converting a practitioner's three-point estimate (best case, base case, worst case) into a parameterized probability distribution suitable for Monte Carlo simulation of CRE investment returns.

## Three-Point Estimate Convention

The user provides three values for each uncertain variable:

| Estimate | Percentile | Meaning |
|---|---|---|
| Best case | P10 | 10% chance of doing better; 90% chance of doing worse or equal |
| Base case | P50 | Most likely outcome; median expectation |
| Worst case | P90 | 90% chance of doing better; 10% chance of doing worse or equal |

Note the asymmetry convention: "best" and "worst" are defined from the investor's perspective, not from the variable's numerical direction. For rent growth, best case is the highest value. For exit cap rate, best case is the lowest value (tighter cap = higher exit price).

## Distribution Selection Decision Tree

```
Is the variable bounded on both sides?
  YES --> Are bounds at 0% and 100%? --> YES --> Use Beta distribution
                                     --> NO  --> Is the distribution symmetric?
                                                   YES --> Use Triangular (simple) or Truncated Normal
                                                   NO  --> Use Triangular
  NO  --> Can the variable go negative?
            YES --> Use Normal distribution
            NO  --> Use Lognormal distribution

Override: If user explicitly says "anywhere in this range is equally likely" --> Use Uniform
```

## Distribution Details

### 1. Triangular Distribution

**When to use**: Default for most CRE variables. Simple, intuitive, bounded, supports asymmetry.

**Parameters**:
- a (minimum) = worst_case (for return-enhancing variables like rent growth) or best_case (for cost variables)
- c (mode) = base_case
- b (maximum) = best_case (for return-enhancing variables) or worst_case (for cost variables)

Normalization: the three-point estimates represent P10/P50/P90, not min/mode/max. To convert:
- The triangular min and max extend beyond the P10/P90 estimates
- Scale factor: multiply the (base_case - worst_case) and (best_case - base_case) spreads by 1.22 to approximate P10/P90 alignment
- a = base_case - 1.22 * (base_case - worst_case_direction)
- b = base_case + 1.22 * (best_case_direction - base_case)

**Properties**:
- Mean = (a + b + c) / 3
- No probability mass outside [a, b]
- Supports asymmetric beliefs (skewness)

**CRE variables**: rent growth, expense growth, capex overrun factor, absorption pace

### 2. Normal Distribution

**When to use**: Symmetric uncertainty, unbounded outcomes plausible, historical data supports normality.

**Parameters**:
- mu (mean) = base_case
- sigma (std dev) = (best_case - worst_case) / 3.29

The 3.29 divisor ensures that 90% of draws fall within [worst_case, best_case] (P5 to P95 spans 3.29 sigma for a normal distribution; since our worst/best are P10/P90, use (best - worst) / 2.563 for exact P10/P90 calibration).

Corrected formula: sigma = (best_case - worst_case) / 2.563

**Properties**:
- Symmetric (skewness = 0)
- Unbounded: ~0.3% of draws exceed 3-sigma, producing outcomes beyond stated range
- Familiar to practitioners with statistics background

**CRE variables**: rent growth (when symmetric beliefs), interest rate changes

**Caution**: not appropriate for variables bounded at zero (vacancy, cap rates). Use lognormal or beta instead.

### 3. Lognormal Distribution

**When to use**: Variable must be positive, right-skewed distribution expected.

**Parameters** (derived from three-point estimate):
- mu_ln = ln(base_case)
- sigma_ln = (ln(best_case) - ln(worst_case)) / 2.563

This calibrates the underlying normal distribution so that the exponentiated result has P10 and P90 at the user's worst and best case.

**Properties**:
- Always positive
- Right-skewed (long tail on the upside)
- Multiplicative uncertainty (percentage changes are normally distributed)

**CRE variables**: exit cap rate, going-in cap rate, vacancy rate (when expressed as a rate, not a count)

### 4. Beta Distribution (bounded [0, 1])

**When to use**: Variable is a rate or percentage bounded between 0% and 100%.

**Parameters** (method of moments from three-point estimate):
- Estimate mean: mu = base_case
- Estimate variance: var = ((best_case - worst_case) / 2.563)^2
- alpha = mu * (mu * (1 - mu) / var - 1)
- beta_param = (1 - mu) * (mu * (1 - mu) / var - 1)

Verify alpha > 0 and beta_param > 0. If not, the variance is too large relative to the mean -- widen the bounds or use triangular.

**Properties**:
- Bounded [0, 1] -- no impossible outcomes
- Flexible shape: symmetric, left-skewed, or right-skewed depending on parameters
- Natural fit for occupancy rates, vacancy rates, expense ratios

**CRE variables**: vacancy rate, occupancy rate, loss severity

### 5. Uniform Distribution

**When to use**: Maximum uncertainty within a range. User has no view on which value is more likely.

**Parameters**:
- a = worst_case
- b = best_case

**Properties**:
- Flat probability across entire range
- Mean = (a + b) / 2
- Highest entropy (maximum uncertainty) for a bounded distribution

**CRE variables**: rarely appropriate. Consider only for binary-like outcomes (e.g., "the capex will cost between $2M and $3M and I have no idea where in that range").

## Variable-Specific Default Distributions

| Variable | Default Distribution | Rationale |
|---|---|---|
| Rent growth | Triangular | Bounded beliefs, often asymmetric (more downside than upside) |
| Exit cap rate | Lognormal | Must be positive, right-skewed risk (caps can blow out further than compress) |
| Vacancy rate | Beta | Bounded 0-100%, natural fit for rates |
| Expense growth | Triangular | Bounded beliefs, moderate asymmetry |
| Capex overrun | Lognormal | Must be positive (overrun factor >= 1.0), right-skewed (overruns more common than under-runs) |
| Refi rate | Normal | Can theoretically go negative (though unlikely), roughly symmetric |
| Absorption pace | Triangular | Bounded (cannot be negative months), right-skewed (delays more common than acceleration) |

## Practical Calibration Tips

### When the user gives only two points (base and downside)
- Assume upside magnitude = 0.6 * downside magnitude (asymmetric risk)
- best_case = base_case + 0.6 * abs(base_case - worst_case)

### When the user gives a base case and "I could see it being 200bps wider"
- worst_case = base_case + 200bps
- best_case = base_case - 120bps (60% of downside)

### When the user says "market consensus"
- Use base_case = consensus estimate
- Standard deviation = 1/3 of the historical standard deviation for that variable in that property type
- This assumes the user's uncertainty is about the consensus being wrong, not about future volatility per se

### When the user provides historical data
- Fit the distribution directly to the data using maximum likelihood
- Override the three-point method
- Report goodness-of-fit statistics

## Common Mistakes

1. **Using the three-point estimate as min/mode/max directly**: The user's "worst case" is their P90, not the absolute worst. The distribution should allow outcomes beyond the stated worst case (for unbounded distributions) or should scale the bounds appropriately (for bounded distributions).

2. **Symmetric distributions for inherently asymmetric variables**: Cap rates can blow out 300bps in a crisis but rarely compress 300bps in a recovery. Rent growth can go negative but rarely exceeds +8% annually. Use asymmetric distributions.

3. **Ignoring the difference between annual and terminal variables**: Rent growth is sampled once and applied each year (autocorrelated). Exit cap rate is sampled once for the terminal year. Do not treat a terminal variable as if it compounds.

4. **Over-specifying distributions**: A triangular distribution with three parameters is usually sufficient. Do not fit a four-parameter distribution (e.g., Johnson SU) unless you have strong empirical justification.
