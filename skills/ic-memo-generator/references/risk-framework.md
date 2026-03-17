# Risk Framework: "What Has to Go Right / What Could Go Wrong"

---

## FRAMEWORK INSTRUCTIONS (strip before use)

This framework produces the risk analysis section of an IC memo. It forces specificity by requiring probability estimates, dollar impacts, and explicit IRR sensitivities for every identified risk. The goal is to eliminate generic risk language ("market conditions could deteriorate") and replace it with quantified, deal-specific risk statements.

**Structure**: Two lenses applied to every deal:
1. **What has to go right** -- the assumptions embedded in the base case that must hold for returns to materialize
2. **What could go wrong** -- specific adverse scenarios with probability and dollar impact

**Rule**: Every risk must have a number attached to it. If you cannot quantify the risk, you do not understand it well enough to present it to IC.

---

## Part 1: What Has to Go Right

These are the embedded assumptions in the base case proforma. Each assumption is a risk if it fails.

### 1.1 Template: Base Case Assumption Audit

For each material assumption in the proforma, complete this row:

| # | Assumption | Base Case Value | Evidence Supporting | What If Wrong | IRR Impact | Probability of Holding |
|---|------------|----------------|--------------------|--------------|-----------|-----------------------|
| 1 | [Assumption name] | [Value used] | [Data source, comp, or analysis] | [Specific failure mode] | [bps change] | [High/Medium/Low] |

**Required assumptions to audit (minimum)**:

1. **Acquisition price / basis** -- Is the price fair? What comp sales support this basis?
2. **Going-in cap rate / NOI** -- Is trailing NOI sustainable? Any one-time items inflating it?
3. **Rent growth rate** -- What historical data supports this? Is the submarket decelerating?
4. **Vacancy / occupancy** -- Is the assumed stabilized vacancy realistic given supply pipeline?
5. **Expense growth rate** -- Insurance, property taxes, and utilities have outpaced CPI in many markets since 2022.
6. **Exit cap rate** -- Is cap compression assumed? What is the basis for the exit cap?
7. **Renovation cost and timeline** (if value-add) -- Are costs from a signed GC contract or an estimate?
8. **Rent premium on renovated units** (if value-add) -- How many comps support the premium?
9. **Financing terms** -- Is the rate locked or floating? What happens at maturity?
10. **Hold period** -- Is the exit timeline realistic given market conditions?

### 1.2 Worked Example: 50-Unit Multifamily

| # | Assumption | Base Case | Evidence | What If Wrong | IRR Impact | Prob. of Holding |
|---|-----------|-----------|----------|---------------|-----------|-----------------|
| 1 | Purchase price | $240K/unit | Off-market estate sale; broker guidance that market would clear at $250-260K | Overpaying by $10-20K/unit = $500K-1M excess basis | -50 to -100bps | High (estate sale, no competing bids) |
| 2 | Going-in cap | 3.94% on $473K NOI | T-12 financials reviewed; 3 vacant units confirmed | If 2 more units vacate pre-close, NOI drops to $430K, cap = 3.58% | -30bps (lower starting yield) | High (94% occupancy verified) |
| 3 | Rent growth | 3.0%/yr | Axiometrics 5-yr avg = 4.2%; adjusted down | Growth stalls at 1.0% due to affordability ceiling | -150bps | Medium (2024 showed deceleration to 2-3%) |
| 4 | Stabilized vacancy | 5.0% | CoStar Q4 2024 = 3.1%; buffered | Supply surprise pushes vacancy to 7-8% | -60 to -90bps | High (no near-term pipeline within 0.5 mi) |
| 5 | Expense growth | 2.5%/yr | 2022-24 actuals; CPI + 50bps | Insurance spike (40%+ increases seen in NJ) pushes to 4.0%/yr | -80bps | Medium (insurance market volatile) |
| 6 | Exit cap | 5.50% | Stabilized cap = 5.54%; 0bp compression | Rates stay higher-for-longer; exit cap = 6.00-6.50% | -200 to -400bps | Medium (rate environment uncertain) |
| 7 | Renovation cost | $18K/unit ($360K total) | GC estimate; 3 bids pending; 10% contingency | Cost overrun to $24K/unit (+33%) = $480K | -70bps from excess capex | Medium (Newark labor market tight) |
| 8 | Rent premium | $450/mo on renovated units | 2 comps: 450 Hamilton ($1,900), 280 Ferry ($1,875) | Premium is $300/mo instead of $450 (33% haircut) | -180bps | Medium-High (2 solid comps, but sample small) |
| 9 | Financing | 7.00% bridge, 2yr IO + 3yr amort | Term sheet in hand | Rate floats up 100bps on SOFR reset | -90bps | Medium (SOFR trajectory uncertain) |
| 10 | Hold period | 5 years | Fund mandate = 3-7yr target | Forced to hold 7 years if market frozen | -50 to -80bps (time value drag) | High (5yr is mid-range of mandate) |

---

## Part 2: What Could Go Wrong

### 2.1 Risk Categorization Matrix

Every risk falls into one of six categories. Probability and severity are assessed independently.

**Categories**:

| Category | Definition | Examples |
|----------|-----------|---------|
| **Market** | Macro or submarket conditions that affect rents, vacancy, or cap rates | Rent growth stalls; cap rates expand; demand declines |
| **Execution** | Operational risks under the sponsor's control | Renovation delay; cost overrun; lease-up slower than plan |
| **Financing** | Risks related to debt structure, covenants, or refinancing | Rate reset; maturity default; covenant breach |
| **Exit** | Risks related to disposition timing and pricing | No buyers at target cap; forced hold; market illiquidity |
| **Regulatory** | Government action affecting operations or value | Rent control; zoning change; tax reassessment; environmental |
| **Credit** | Tenant or counterparty default (especially NNN, office) | Tenant BK; subtenant default; guarantor insolvency |

### 2.2 Probability-Impact Grid

Plot each identified risk on this grid. Risks in the upper-right quadrant require explicit mitigation plans.

```
                    IMPACT ON LEVERED IRR
                    Low (<100bps)  Med (100-250bps)  High (>250bps)
                   +---------------+------------------+---------------+
  PROBABILITY      |               |                  |               |
  High (>50%)      | Monitor       | MITIGATE         | DEAL-BREAKER  |
                   |               |                  |  unless       |
                   |               |                  |  mitigated    |
                   +---------------+------------------+---------------+
  Medium (20-50%)  | Accept        | MITIGATE         | MITIGATE      |
                   |               |                  |               |
                   +---------------+------------------+---------------+
  Low (<20%)       | Accept        | Monitor          | Stress-test   |
                   |               |                  |               |
                   +---------------+------------------+---------------+
```

**Decision rules**:
- **Accept**: Risk is within normal operating parameters. Note in memo, no specific mitigation required.
- **Monitor**: Track the risk indicator; define a trigger for escalation.
- **Mitigate**: Require specific action plan (contractual protection, reserve, insurance, etc.).
- **Deal-breaker**: Risk must be eliminated or reduced to Medium before proceeding. If it cannot be, recommend NO-GO.
- **Stress-test**: Low probability but catastrophic impact. Model the scenario in sensitivity tables.

### 2.3 Template: Risk Factor Write-Up

For each risk rated "Mitigate" or higher:

```
### Risk [N]: [Name] -- [Category]

**Mechanism**: [How does this risk materialize? Be specific. Not "costs could increase" but
"Newark multifamily renovation costs have increased 8-12% annually in 2022-2024. A 6-month
delay in the 20-unit renovation program would extend work into the post-IO amortizing period,
adding $X in debt service to the project cost."]

**Probability**: [Low / Medium / High] -- [1-2 sentence justification with data]

**Impact if materialized**:
- Dollar impact: $[X] increase in cost or $[X] reduction in value
- IRR impact: [X]bps reduction in levered IRR
- Equity multiple impact: [X.XX]x reduction
- DSCR impact: [X.XX]x reduction (if applicable)

**Mitigation**:
- [Specific action 1 with responsible party]
- [Specific action 2 with deadline]
- [Structural protection: reserve, insurance, contractual provision]

**Residual risk after mitigation**: [Low / Medium] -- [1 sentence]

**Trigger for escalation**: [What observable event would indicate this risk is materializing?
e.g., "If renovation is not 50% complete by Month 9, convene IC update call."]
```

### 2.4 Worked Example: 50-Unit Multifamily

---

### Risk 1: Renovation Cost Overrun and Timeline Slippage -- Execution

**Mechanism**: The $360K renovation budget ($18K/unit for 20 units) is based on a single GC estimate. Newark construction costs have inflated 8-12% annually since 2022. If material costs spike or the GC encounters unforeseen conditions (asbestos, plumbing, electrical), costs could increase 20-40%. A 6-month delay pushes 8-10 units into the post-IO amortizing period, adding approximately $40K in incremental debt service.

**Probability**: Medium -- Single GC estimate without competitive bids yet. 1970s-vintage building increases likelihood of hidden conditions. However, scope is cosmetic (kitchens, baths, flooring), not structural.

**Impact if materialized**:
- Dollar impact: $72K-144K cost overrun (20-40% of $360K budget)
- IRR impact: -70 to -130bps (cost overrun alone); -115 to -130bps per 6-month delay
- Equity multiple impact: -0.05x to -0.10x
- Combined worst case (40% overrun + 12-month delay): -280bps, levered IRR = 9.3%

**Mitigation**:
- 10% contingency ($36K) included in capex budget
- Require 3 competitive GC bids before contract execution (Acquisition Team, 30 days)
- Phased renovation: start with units requiring least structural work
- Monthly draw schedule tied to unit completion milestones, not elapsed time
- Pre-renovation environmental/structural inspection to identify hidden costs before closing

**Residual risk after mitigation**: Low-Medium -- Competitive bidding and phased approach reduce but do not eliminate execution risk.

**Trigger for escalation**: If fewer than 5 of 20 units are completed by Month 6, convene IC update to assess revised timeline and budget.

---

### Risk 2: Rent Growth Stalls Below Assumption -- Market

**Mechanism**: The 3.0%/yr rent growth assumption relies on continued NYC housing demand overflow into Newark Ironbound. This pattern supported 4-5% growth in 2021-2023 but decelerated to 2-3% in 2024 as affordability approached ceilings. If NYC rents stabilize or decline (reducing the arbitrage incentive to move to Newark), or if new supply materializes (currently minimal), rent growth could fall to 0-1%.

**Probability**: Low-Medium -- Ironbound remains supply-constrained with 3.1% vacancy. No pipeline within 0.5 miles. But macro rental deceleration is a real trend nationally.

**Impact if materialized**:
- Dollar impact: At 1% growth, Year 5 NOI is $40K lower than base case ($575K vs. $615K)
- IRR impact: -150bps at 1.0% rent growth; -270bps at 0.0%
- At 0% growth + base exit cap: levered IRR = 9.4% (below 10% hurdle)
- At 1% growth + base exit cap: levered IRR = 10.7% (above hurdle by 70bps)

**Mitigation**:
- Renovation rent premium ($450/mo) is a quality differential, not a market rent growth bet. Even at 0% market growth, renovated units should achieve the premium relative to unrenovated peers.
- 1.0% rent growth scenario still meets hurdle (10.7%). Deal fails hurdle only at 0% growth.
- Monitor: Track quarterly Axiometrics/CoStar submarket rent data against plan.

**Residual risk after mitigation**: Low -- The value-creation strategy is not purely dependent on market rent growth.

**Trigger for escalation**: If submarket rent growth turns negative for two consecutive quarters post-acquisition, reassess disposition timeline.

---

### Risk 3: Exit Cap Rate Expansion -- Exit

**Mechanism**: The 5.50% exit cap assumes 0bps of compression from the stabilized cap of 5.54%. If the interest rate environment remains elevated (Fed funds above 4.5%) through 2030, multifamily cap rates in secondary markets like Newark could expand to 6.00-6.50%. This reduces the gross reversion by $1.0-2.3M.

**Probability**: Medium -- Rate trajectory over 5 years is inherently uncertain. Forward curve currently implies gradual normalization, but higher-for-longer is a plausible scenario.

**Impact if materialized**:
- Dollar impact: At 6.00% exit cap, gross reversion = $11.75M (vs. $12.85M base), -$1.1M
- Dollar impact: At 6.50% exit cap, gross reversion = $10.85M, -$2.0M
- IRR impact: -200bps at 6.00% exit cap; -400bps at 6.50%
- At 6.00% exit cap + base rent growth: levered IRR = 10.8% (above hurdle)
- At 6.50% + 3.0% growth: levered IRR = 8.7% (below hurdle)

**Mitigation**:
- Exit cap of 5.50% assumes zero compression -- already a conservative starting point
- NOI growth is the primary return driver; even at a higher exit cap, the NOI uplift from $473K to $706K provides substantial value creation independent of cap rate movement
- If cap rates expand meaningfully, consider extending hold and refinancing into agency debt at 8.1% debt yield (within Fannie/Freddie qualification range)

**Residual risk after mitigation**: Medium -- Cap rates are a macro variable outside sponsor control. The deal's NOI growth provides a partial buffer.

**Trigger for escalation**: If multifamily cap rates in Newark expand 50bps+ from acquisition within Years 1-2, model revised exit scenarios and present to IC.

---

### Risk 4: Regulatory -- Newark Rent Control Exposure

**Mechanism**: Newark's rent control ordinance applies to units occupied before the owner's substantial rehabilitation. The exemption pathway requires documentation and municipal approval, which can take 3-12 months. If the exemption is delayed or denied, re-tenanting renovated units at market rents could be restricted, capping rent increases at the CPI-based regulatory maximum (typically 2-4%).

**Probability**: Low-Medium -- Substantial rehabilitation exemption exists and is commonly used. However, Newark's rent board has become more restrictive since 2023.

**Impact if materialized**:
- Dollar impact: If 20 renovated units capped at CPI increase instead of $450 premium, Year 3 NOI shortfall = $108K ($450 x 20 units x 12 months)
- IRR impact: -200 to -250bps if exemption denied entirely
- If exemption delayed 12 months: -80 to -100bps (delayed lease-up at premium rents)

**Mitigation**:
- Engage Newark real estate counsel before closing to confirm exemption pathway
- Document renovation scope against the statutory threshold
- Budget 3-6 month buffer for regulatory approval timeline
- Condition to close: legal opinion confirming exemption eligibility

**Residual risk after mitigation**: Low -- Legal pre-clearance before closing eliminates the surprise factor. Delay risk remains.

**Trigger for escalation**: If counsel identifies any uncertainty in exemption eligibility, escalate to IC before contract execution.

---

## Part 3: Aggregated Risk Dashboard

### 3.1 Template: Risk Summary Table for IC Presentation

| # | Risk | Category | Prob. | Impact (bps) | Mitigated? | Residual |
|---|------|----------|-------|-------------|-----------|---------|
| 1 | [Name] | [Cat] | [L/M/H] | [X] | [Y/N/Partial] | [L/M] |
| 2 | [Name] | [Cat] | [L/M/H] | [X] | [Y/N/Partial] | [L/M] |
| 3 | [Name] | [Cat] | [L/M/H] | [X] | [Y/N/Partial] | [L/M] |

### 3.2 Worked Example

| # | Risk | Category | Prob. | Impact | Mitigated? | Residual |
|---|------|----------|-------|--------|-----------|---------|
| 1 | Reno cost/timeline | Execution | Med | -70 to -260bps | Partial | Low-Med |
| 2 | Rent growth stalls | Market | Low-Med | -150 to -270bps | Partial | Low |
| 3 | Exit cap expansion | Exit | Med | -200 to -400bps | Partial | Med |
| 4 | Rent control delay | Regulatory | Low-Med | -80 to -250bps | Yes | Low |

### 3.3 Combined Stress Scenario

**Question IC will ask**: "What happens if multiple risks hit simultaneously?"

Model the combined downside:

| Scenario | Assumptions | Levered IRR | EM | vs. Hurdle |
|----------|-----------|-----------|-----|-----------|
| Base case | All assumptions hold | 12.1% | 1.83x | +2.1% |
| Single risk (worst) | 0% rent growth, all else base | 9.4% | 1.65x | -0.6% |
| Double risk | 0% growth + 6.00% exit cap | 7.1% | 1.52x | -2.9% |
| Triple stress | 0% growth + 6.00% cap + 6mo reno delay | 5.8% | 1.42x | -4.2% |
| Catastrophic | 0% growth + 6.50% cap + 12mo delay + cost overrun | 3.2% | 1.25x | -6.8% |

**Interpretation**: The deal withstands any single risk event and still produces acceptable returns. A double-risk scenario (0% growth + cap expansion) pushes IRR below hurdle but preserves capital (EM > 1.0x). The catastrophic scenario -- requiring simultaneous failure across market, execution, and capital markets -- has a low joint probability but still returns capital with a modest gain.

---

## Part 4: Anti-Patterns -- Risk Language to Reject

### Phrases That Signal Insufficient Risk Analysis

| Bad Language | Why It Fails | Better Version |
|-------------|-------------|---------------|
| "Market conditions could deteriorate" | No specificity on mechanism, magnitude, or probability | "If SOFR remains above 5.25% through 2028, cap rates in Newark MF could expand 75-100bps, reducing reversion by $1.1-1.5M" |
| "We are comfortable with the risk" | Comfort is not analysis | "The risk is mitigated by X, Y, Z. Residual impact is -80bps, within the return cushion above hurdle" |
| "Subject to further diligence" | What diligence? By when? | "Condition to close: Phase I environmental report confirming no contamination (Environmental Consultant, 30 days)" |
| "Strong sponsor track record" | Track record does not eliminate deal-level risk | "Sponsor has completed 3 comparable renovations in Newark (list addresses). Average cost overrun was 8% vs. budget" |
| "The deal has attractive risk/reward" | This must be demonstrated, not stated | "Base case IRR exceeds hurdle by 210bps. The deal fails hurdle only in the double-stress scenario (cap expansion + zero rent growth), which requires simultaneous deterioration with an estimated joint probability below 15%" |
| "Downside protection from basis" | Basis is one input; quantify the protection | "At $240K/unit, the basis is $80K below replacement cost. Even at a 6.50% exit cap with 0% growth, the investment returns 1.25x equity -- capital is preserved" |
| "Favorable debt terms" | Compared to what? | "7.00% bridge rate with 2yr IO is 50bps below the current Arbor/Ready Capital quote for comparable transitional MF loans" |

---

## Part 5: Risk-Adjusted Return Overlay

### 5.1 Expected Return Calculation

For sophisticated IC presentations, compute the probability-weighted expected return:

```
Expected IRR = SUM(Scenario_IRR * Scenario_Probability)
```

| Scenario | Probability | IRR | Weighted Contribution |
|----------|------------|-----|----------------------|
| Bull case | 15% | 20.0% | 3.00% |
| Base case | 50% | 12.1% | 6.05% |
| Moderate stress | 25% | 8.3% | 2.08% |
| Downside | 10% | 5.1% | 0.51% |
| **Expected IRR** | **100%** | | **11.64%** |

**Interpretation**: The probability-weighted expected IRR of 11.64% exceeds the 10.0% hurdle by 164bps. This is more informative than the point-estimate base case of 12.1% because it incorporates downside weighting.

### 5.2 Margin of Safety Calculation

```
Margin of Safety = (Base Case IRR - Hurdle Rate) / Base Case IRR
```

For the worked example: (12.1% - 10.0%) / 12.1% = 17.4% margin of safety.

**Benchmarks**:
- <10% margin: Tight. Deal has little room for error. Recommend NO-GO unless thesis is highly differentiated.
- 10-20% margin: Adequate for core-plus or light value-add. Require solid mitigations.
- 20-30% margin: Comfortable for value-add. Standard approval range.
- >30% margin: Strong cushion. Opportunistic-level upside.

### 5.3 Breakeven Analysis

State the breakeven conditions -- what has to happen for the deal to exactly meet hurdle:

- **Breakeven exit cap**: [X.X]% (base rent growth) -- [X]bps above base case exit cap
- **Breakeven rent growth**: [X.X]% (base exit cap) -- [X]bps below base case rent growth
- **Breakeven renovation cost**: $[X]/unit -- [X]% above base case budget

For the worked example:
- Breakeven exit cap (at 3.0% growth): ~5.85% -- 35bps of cushion above base
- Breakeven rent growth (at 5.50% exit cap): ~0.8% -- 220bps of cushion below base
- Breakeven renovation cost: ~$28K/unit -- 56% above budget (ample cushion on this variable)

The deal's return is most sensitive to exit cap rate, least sensitive to renovation cost. This tells IC where to focus their scrutiny.
