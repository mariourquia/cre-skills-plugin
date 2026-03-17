# Broker Assumption Critique Framework

## Purpose

Every offering memorandum (OM) is a sales document. The broker's job is to maximize the seller's proceeds, which means the pro forma will present the most optimistic defensible case. This framework provides a systematic method to identify where the OM's assumptions diverge from reality and quantify the impact on value.

## The 5-Point Broker Assumption Checklist

### 1. Rent Growth Assumptions

**What brokers do:** Project rent growth at 3-4% annually, often citing "market momentum" or "comparable new lease rates" without accounting for mean reversion, concession burn-off, or supply pipeline impact.

**Reality check:**

| Metric | Typical Broker Assumption | Market Reality (Long-Run) | Red Flag Threshold |
|--------|--------------------------|--------------------------|-------------------|
| Annual rent growth | 3.0-4.5% | 2.0-3.0% (nominal, varies by market) | > 2x trailing 10yr MSA avg |
| Rent growth Year 1 | 3.5-5.0% | Loss-to-lease capture, then market | > loss-to-lease + 200bps |
| Mark-to-market on rollovers | 10-20% bump | Depends on lease vintage and market | > 15% without comp support |
| Concession trajectory | Declining to zero by Year 2 | Persistent in oversupplied markets | Zero concessions assumed with supply pipeline > 5% of stock |

**How to stress test:**

1. Pull CoStar submarket effective rent growth for trailing 3, 5, and 10 years.
2. Identify the supply pipeline (units under construction / existing inventory). If > 4%, haircut Year 1-3 growth by 100-200bps.
3. Check loss-to-lease on the rent roll. If the OM's Year 1 growth exceeds loss-to-lease capture, the remainder must be organic growth -- compare to trailing actuals.
4. Verify mark-to-market assumptions by pulling 5+ lease comps at the property's quality tier and location. Use effective rents (face minus concessions), not asking rents.

**Typical value impact:** Each 100bps of annual rent growth over a 5-year hold on a $50M deal shifts exit value by approximately $2-3M (assuming 5% exit cap).

---

### 2. Expense Growth Assumptions

**What brokers do:** Project expense growth at 2.0-2.5%, often below CPI, implying real expense deflation. Insurance and property taxes -- two of the three largest expense lines -- frequently grow faster than CPI.

**Reality check:**

| Expense Category | Typical Broker Assumption | Market Reality | Red Flag Threshold |
|-----------------|--------------------------|---------------|-------------------|
| Total opex growth | 2.0-2.5% | 3.0-4.0% (blended) | < trailing 3yr CPI |
| Property taxes | "Held flat" or 2% | Reassessment risk at acquisition; 3-5% annual in high-growth markets | Flat tax projection after acquisition in reassessment state |
| Insurance | 2-3% | 8-15% in coastal/CAT markets; 4-7% nationally | < 5% in any coastal or CAT-exposed market |
| Payroll/contract labor | 2-3% | 4-6% (wage inflation + tightening labor) | < 3.5% in tight labor markets |
| R&M / turnover | "Declining as units are renovated" | Stable or rising with age and inflation | Declining R&M without capital plan to support |
| Utilities | 2% | Volatile; 3-6% trend | < 3% without solar or efficiency capex |

**How to stress test:**

1. Request T-3 actual operating statements (audited or tax returns preferred over broker-prepared trailing).
2. Calculate actual expense CAGR over T-3. If broker pro forma projects growth below this rate, demand justification.
3. Check the county assessor for current assessed value vs acquisition price. In reassessment states (CA Prop 13 exception, TX, FL, GA), taxes will reset to near-acquisition price. This alone can add $500-2,000/unit in annual expense.
4. Get actual insurance quotes or at minimum the trailing 3 years of premiums. Broker pro formas routinely understate insurance by 15-30% in CAT-exposed markets.
5. Validate management fee assumption: 3-4% for institutional, 5-7% for third-party managed sub-200 units.

**Typical value impact:** Each 100bps of additional annual expense growth on a $50M deal reduces exit value by approximately $1.5-2.5M over a 5-year hold.

---

### 3. Exit Cap Rate Assumptions

**What brokers do:** Assume exit cap rate equal to or below going-in cap rate, implying cap rate compression during the hold period. This is the single most aggressive lever in most OM pro formas.

**Reality check:**

| Scenario | Typical Broker Assumption | Institutional Standard | Red Flag Threshold |
|----------|--------------------------|----------------------|-------------------|
| Exit cap vs going-in | Flat or -25bps | +10-25bps (reversion to mean) | Exit cap < going-in cap |
| Exit cap vs long-run avg | At or below current | At or above long-run avg | Exit cap > 50bps below 20yr avg for asset class |
| Rate environment adjustment | None or "rates will decline" | Sensitivity table required | Single-point exit cap with no sensitivity |

**How to stress test:**

1. Never model exit cap below going-in cap unless you have a specific thesis (e.g., repositioning from C to B class, lease-up from 80% to 95%).
2. Standard institutional practice: going-in cap + 10-25bps for exit. This accounts for aging of the asset, potential market cycle risk, and the fact that you cannot predict cap rates 5 years out.
3. Run a sensitivity table: +/- 50bps on exit cap in 25bps increments. If the deal does not work at going-in + 50bps, the return is overly dependent on favorable cap rates.
4. Check the 20-year average cap rate for the asset class and market. If the broker's exit cap is more than 50bps below this average, the model is pricing in permanent structural compression that may not materialize.

**Typical value impact:** Each 25bps of exit cap rate expansion on a $50M deal at a 5% going-in cap reduces exit value by approximately $2.3M.

**Cap rate sensitivity on $3M Year-5 NOI:**

| Exit Cap | Implied Value | Delta vs 5.00% |
|----------|-------------|----------------|
| 4.50% | $66,667,000 | +$6,667,000 |
| 4.75% | $63,158,000 | +$3,158,000 |
| 5.00% | $60,000,000 | Baseline |
| 5.25% | $57,143,000 | -$2,857,000 |
| 5.50% | $54,545,000 | -$5,455,000 |
| 5.75% | $52,174,000 | -$7,826,000 |

---

### 4. Vacancy and Credit Loss

**What brokers do:** Project stabilized vacancy at 3-5% regardless of submarket conditions, asset class, or supply pipeline. Credit loss often projected at 0.5-1.0% even for workforce housing with historically higher bad debt.

**Reality check:**

| Metric | Typical Broker Assumption | Market Reality | Red Flag Threshold |
|--------|--------------------------|---------------|-------------------|
| Physical vacancy | 3-5% | Submarket-dependent; 5-8% in many markets | > 200bps below trailing 3yr submarket avg |
| Economic vacancy | 5-7% | Physical vacancy + concessions + credit loss; often 8-12% | Economic vacancy < physical vacancy (impossible without negative concessions) |
| Credit loss | 0.5-1.0% | 1.5-3.0% for workforce housing; 0.5-1.5% for Class A | < 1.5% for B/C class without proof from T-12 actuals |
| Concession impact | "Burning off" | 0.5-2 months free in lease-up or oversupplied markets = 4-17% effective discount | Zero concessions when submarket shows 1+ month free |

**How to stress test:**

1. Pull CoStar submarket vacancy for trailing 3, 5, and 10 years. Use the 5-year average as your stabilized vacancy, not the broker's number.
2. Request the actual rent roll and calculate economic occupancy: (gross potential rent - vacancy loss - concessions - credit loss - model units) / gross potential rent. Compare to broker's stated occupancy.
3. For workforce housing (< 80% AMI area median income tenants), model credit loss at 2.0-3.0% unless T-12 actuals demonstrate otherwise. Post-COVID eviction moratorium hangovers persist in some jurisdictions.
4. If the submarket has a supply pipeline > 4% of existing stock, add 100-200bps to stabilized vacancy for the delivery years.

**Typical value impact:** Each 100bps of additional vacancy/credit loss on a $50M deal reduces NOI by $150-250K, reducing value by $3-5M at a 5% cap.

---

### 5. Capital Expenditure Reserves

**What brokers do:** Show $250-500/unit annual capex reserves in the pro forma, regardless of building age, condition, or deferred maintenance. Some OM pro formas show zero reserves, flowing all NOI to the cap rate line.

**Reality check:**

| Asset Profile | Typical Broker Reserve | Institutional Standard | Red Flag Threshold |
|--------------|----------------------|----------------------|-------------------|
| New construction (< 5yr) | $0-250/unit | $250-400/unit | $0 reserves on any asset |
| Value-add (10-25yr) | $250-500/unit | $500-1,000/unit (excluding renovation capex) | < $500/unit on 15+ year asset |
| Older / deferred (25yr+) | $300-500/unit | $1,000-2,000/unit | < $1,000/unit on 25+ year asset without PCA |
| Commercial (office/retail) | $0.50-1.00/SF | $1.50-3.00/SF | < $1.50/SF on 15+ year building |

**How to stress test:**

1. Obtain or commission a Property Condition Assessment (PCA). The PCA will provide a 12-year capital needs table. Annualize total needs and compare to broker's reserve.
2. Distinguish between recurring capex (roofs, HVAC, parking lots, appliances) and value-add capex (unit renovations, amenity upgrades). Only recurring capex should reduce ongoing NOI. Value-add capex is a separate investment decision with its own return threshold.
3. For vintage assets, use the vintage capex benchmarks from the screening rubric. If the PCA's 12-year total exceeds 15% of acquisition basis, the capex drag will materially reduce levered returns.
4. Verify the broker has not capitalized recurring maintenance items (painting, landscaping, pressure washing) that should be operating expenses. This inflates NOI.

**Typical value impact:** Each $500/unit of understated annual capex on a 200-unit deal = $100K/yr less cash flow = $2M less value at a 5% cap.

---

## Aggregated Impact Analysis

After scoring all 5 assumptions, aggregate the delta between broker's assumptions and your base case:

| Assumption | Broker Value | Your Value | Annual NOI Impact |
|-----------|-------------|-----------|-------------------|
| Rent growth (Year 1) | ___ | ___ | ___ |
| Expense growth | ___ | ___ | ___ |
| Stabilized vacancy | ___ | ___ | ___ |
| Credit loss | ___ | ___ | ___ |
| Capex reserves | ___ | ___ | ___ |
| **Net NOI adjustment** | | | **___** |

Apply the net NOI adjustment to the broker's stabilized NOI. Then apply your exit cap rate (not the broker's) to arrive at your adjusted value. The delta between the broker's price and your adjusted value is the "OM gap" -- the distance between the sales pitch and reality.

**Rule of thumb:** If the OM gap exceeds 15%, the deal is materially overpriced relative to market reality. A 5-10% gap is normal broker optimism. Under 5% indicates a relatively honest OM (rare).
