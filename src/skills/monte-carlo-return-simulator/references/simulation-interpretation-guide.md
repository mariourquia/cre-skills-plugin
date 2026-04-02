# Simulation Interpretation Guide

## Purpose

This guide explains how to read and present Monte Carlo simulation results for CRE investments. It covers common pitfalls in interpretation, when Monte Carlo adds value versus when it is overkill, and how to communicate probabilistic results to different audiences (IC committees, investors, lenders).

## Reading the Output

### Percentile Table

The percentile table is the most important output. Each row answers a specific question:

| Percentile | Question It Answers |
|---|---|
| P5 | "What happens in a near-worst-case scenario?" (95% of outcomes are better) |
| P10 | "What is the downside I should plan for?" (90% of outcomes are better) |
| P25 | "What if things go somewhat poorly?" (conservative estimate) |
| P50 | "What is the most likely outcome?" (median, not mean) |
| P75 | "What if things go somewhat well?" |
| P90 | "What is a realistic upside?" (only 10% of outcomes are better) |
| P95 | "What happens if nearly everything goes right?" |

**Key distinction: P50 (median) vs. mean.** For skewed return distributions (common in CRE, especially value-add and opportunistic), the mean is pulled by outlier outcomes. The median is a better "expected" return. Report both, but anchor discussion on the median.

### Probability Metrics

**Probability of loss (P(IRR < 0%))**: The single most important risk metric. Institutional investors typically require:
- Core: < 2% probability of loss
- Core-plus: < 5%
- Value-add: < 10%
- Opportunistic: < 15%

These thresholds are not industry standards but reasonable benchmarks. The user should define their own risk tolerance.

**Probability of achieving target IRR**: This directly answers "how likely am I to hit my return target?" A 60% probability of hitting a 15% target IRR is very different from a 90% probability. Both might have the same base-case IRR.

**Value-at-Risk (VaR)**: The IRR (or dollar loss) at a given confidence level. "95% VaR of 2.1% IRR" means there is a 5% chance the IRR falls below 2.1%.

**Conditional VaR (CVaR / Expected Shortfall)**: The average outcome in the tail beyond VaR. More informative than VaR because it tells you how bad things get in the tail, not just the threshold. "95% CVaR of -1.5% IRR" means that in the worst 5% of outcomes, the average IRR is -1.5%.

### Sensitivity Ranking

**Spearman rank correlation**: Measures the monotonic relationship between each input variable and the output IRR across all trials. Higher absolute value = more influence on returns.

Interpretation:
- |rho| > 0.50: dominant driver -- must be right on this variable
- 0.30 < |rho| < 0.50: significant driver -- warrants attention
- 0.10 < |rho| < 0.30: moderate driver -- monitor but not critical
- |rho| < 0.10: negligible -- can hold at base case without materially affecting results

**Contribution to variance**: Calculated as rho^2 / sum(rho^2) for all variables. Expressed as a percentage. A variable contributing 40% of IRR variance means that 40% of the spread in outcomes is attributable to uncertainty in that variable.

**Why simulation-based sensitivity beats deterministic tornado charts**: Deterministic analysis tests one variable at a time, holding all others constant. This misses interaction effects. In reality, when vacancy rises, rents also fall (correlated). The simulation captures this because it draws correlated samples. A variable that looks like the #2 driver in a deterministic tornado chart might be the #1 driver in simulation because its correlation with other variables amplifies its impact.

## When Monte Carlo Adds Value

Monte Carlo simulation adds the most value when:

1. **Multiple uncertain variables with meaningful interaction**: If only one variable is uncertain (e.g., exit cap rate on a stabilized NNN asset), a simple sensitivity table suffices. When 3+ variables interact (rent growth, vacancy, cap rates, rates), the joint distribution matters.

2. **Asymmetric or non-linear payoffs**: Levered returns are non-linear. A 100bps increase in vacancy has a different IRR impact at 90% occupancy vs. 80% occupancy. Monte Carlo naturally captures this non-linearity.

3. **Tail risk quantification**: Deterministic scenarios answer "what if X happens?" Monte Carlo answers "what is the probability of losing money?" and "how bad is the average bad outcome?" These are fundamentally different and more useful questions.

4. **Communicating risk to investors**: "P10 IRR is 4.2% and probability of loss is 3.1%" is more informative than "downside scenario IRR is 6.8%." The former quantifies likelihood; the latter does not.

5. **Comparing deals with different risk profiles**: Two deals might have the same base-case IRR but very different return distributions. Monte Carlo reveals which deal has tighter dispersion (lower risk) and which has more tail risk.

## When Monte Carlo Is Overkill

1. **Stabilized core asset with fixed-rate financing and long-term leases**: When most cash flows are contractual and the only real uncertainty is exit cap rate, a three-scenario analysis (base, upside, downside) captures the risk adequately. Monte Carlo adds complexity without proportional insight.

2. **Early-stage screening**: When evaluating 50 deals to find 5 worth underwriting, a quick screen or back-of-envelope analysis is appropriate. Monte Carlo is a deep-dive tool for the final 2-3 candidates.

3. **When the user cannot quantify their uncertainty**: If the user cannot provide three-point estimates for any variable, they cannot calibrate a simulation. Garbage in, garbage out. Start with deterministic sensitivity to build intuition before going stochastic.

4. **When the audience does not understand probability**: Some investors, lenders, or partners are not comfortable with probabilistic analysis. Presenting "P10 IRR" to an audience that thinks in "base case / downside" terms can confuse rather than inform. Know your audience.

## Common Pitfalls

### 1. False Precision
Reporting "Monte Carlo expected IRR = 13.27%" implies precision that does not exist. The standard deviation might be 400bps. Report as "expected IRR of approximately 13.3%, with a standard deviation of 4.0 percentage points" or "expected IRR in the 9-17% range (P25 to P75)."

### 2. Anchoring on the Mean
The mean return is not the most likely return when the distribution is skewed. In a right-skewed distribution (common for value-add), the mean is above the median. In a left-skewed distribution (common for levered core with capped upside and unlimited downside from default), the mean is below the median. Always report the median alongside the mean.

### 3. Ignoring Model Risk
The simulation is only as good as its assumptions: distribution shapes, correlation structure, and the DCF model itself. A simulation with wrong assumptions is precisely wrong. Always present the assumption log and invite the user to challenge distributions and correlations.

### 4. Treating All Trials Equally
In practice, extreme tail outcomes often involve structural breaks (market crash, tenant bankruptcy, regulatory change) that are not well-captured by smooth distributions. The P1 outcome from a simulation may understate true tail risk because the simulation does not model regime changes. Supplement with deterministic stress scenarios for known tail events.

### 5. Correlation Stability
Correlations between CRE variables are not constant. During stress periods, correlations increase (everything gets worse together). The default correlation matrices represent average conditions. For stress testing, consider increasing the magnitude of negative correlations by 20-30%.

### 6. Conflating Annual and Terminal Uncertainty
Rent growth uncertainty compounds over the hold period (each year is uncertain, and errors accumulate). Exit cap rate uncertainty is a single draw applied at the terminal year. A 100bps standard deviation on rent growth has a much larger impact over a 10-year hold than a 100bps standard deviation on exit cap, even if the deterministic sensitivity shows them as similar. The simulation handles this correctly, but the user should understand why the sensitivity ranking may differ from their deterministic intuition.

## Communicating Results to Different Audiences

### Investment Committee (IC)
Focus on:
- Probability of loss and probability of hitting target return
- P10/P50/P90 returns (three numbers that tell the story)
- Top 2 risk drivers and what can be done about them
- Comparison to the IC's stated risk tolerance for the strategy

Skip: distribution fitting details, correlation matrices, technical statistics. Include in an appendix.

### Investors / LPs
Focus on:
- "In X% of scenarios, the investment achieves at least your target return"
- "The worst realistic outcome (P10) is X% IRR, representing Y% probability of capital loss"
- Scenario overlays (rate spike, recession) because investors think in scenarios
- Comparison to previous fund performance distributions if available

Skip: VaR/CVaR terminology (use plain language), sensitivity ranking (replace with narrative), technical methodology.

### Lenders
Focus on:
- Probability of DSCR falling below covenant levels (1.25x, 1.10x, 1.0x)
- Distribution of debt yield across scenarios
- Maximum rate at which DSCR remains above 1.0x (for floating rate)
- Cash flow coverage percentiles, not IRR percentiles

Skip: equity return metrics (lenders care about debt coverage, not equity returns), promote/waterfall structures.

## Trial Count Guidance

| Trial Count | Use Case | Percentile Stability |
|---|---|---|
| 1,000 | Quick estimate, directional only | P10/P90 stable within +/-100bps |
| 5,000 | Standard analysis (recommended default) | P10/P90 stable within +/-30bps |
| 10,000 | Publication-quality, formal IC presentation | P5/P95 stable within +/-20bps |

"Stable" means that re-running with a different seed produces percentile estimates within the stated tolerance. Below 1,000 trials, the P5 and P95 estimates are unreliable and should not be reported.

## Glossary

| Term | Definition |
|---|---|
| CDF | Cumulative distribution function. P(X <= x). |
| Cholesky decomposition | Matrix factorization used to generate correlated random samples from a correlation matrix. |
| CVaR | Conditional Value-at-Risk (Expected Shortfall). Average loss in the worst X% of outcomes. |
| IRR | Internal rate of return. Discount rate at which NPV of cash flows = 0. |
| Monte Carlo | Computational technique using repeated random sampling to model uncertainty. Named after the casino. |
| P10 / P50 / P90 | 10th, 50th, 90th percentile of the simulated distribution. |
| Spearman rho | Rank correlation coefficient. Measures monotonic (not necessarily linear) relationship. |
| VaR | Value-at-Risk. The threshold loss exceeded with probability X%. |
