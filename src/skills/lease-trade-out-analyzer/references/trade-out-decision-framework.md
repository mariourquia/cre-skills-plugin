# Trade-Out Decision Framework

---

## Purpose

This reference provides a structured decision tree for the renewal-vs.-trade-out decision. Use it as a first-pass filter before running the full NPV model. The decision tree will identify clear-cut cases (where the NPV outcome is highly predictable) and the gray zone (where full NPV analysis plus risk adjustment is required).

---

## Part 1: Pre-Screening Decision Tree

Work through the branches in order. Stop when you reach a terminal node.

```
STEP 1: CO-TENANCY RISK CHECK (Retail only)
  Is this an anchor tenant (>15,000 SF in a retail center)?
    YES: Does trading out trigger co-tenancy clauses for other tenants?
           YES: STOP. Recommend RENEW unless identified replacement anchor is
                in-hand or under signed LOI. Co-tenancy cascade risk is
                existential. Proceed to NPV only after co-tenancy exposure
                is quantified and capped.
           NO: Continue to Step 2.
    NO: Continue to Step 2.

STEP 2: DEBT COVENANT CHECK
  Does this property have a DSCR covenant?
    YES: Would losing this tenant cause a DSCR breach?
           YES: STOP. Recommend RENEW at any terms above your walk-away floor.
                Covenant breach triggers cash trap, lender intervention, and
                potential acceleration. The cost of a breach far exceeds the
                rent gap NPV. Engage lender before making any trade-out decision.
           NO: Continue to Step 3.
    NO: Continue to Step 3.

STEP 3: DISPOSITION / REFI TIMELINE CHECK
  Is there a sale or refinancing planned within 18 months?
    YES: Bias strongly toward RENEW, especially if the tenant is credit-rated.
         Buyers and lenders price WALT and credit quality. A vacancy at disposition
         is doubly damaging: lost rent + cap rate widening + reduced buyer pool.
         Only trade-out if the rent gap is extreme (>35% below market) AND
         identified replacement is already in LOI.
    NO: Continue to Step 4.

STEP 4: SINGLE-TENANT BUILDING CHECK
  Is this a single-tenant building?
    YES: Trade-out = 100% vacancy. Apply 150bps additional discount rate to
         trade-out scenario. Require breakeven vacancy < 3 months to proceed.
         In most markets with balanced or soft conditions: RENEW.
    NO: Continue to Step 5.

STEP 5: RENT GAP CHECK
  What is the rent gap (current rent / market rent)?
    > 95% of market (in-place is AT or near market):
      RENEW. Trade-out provides no meaningful rent premium. The cost of
      vacancy and re-leasing will always exceed a sub-5% rent premium
      over any reasonable hold period.
    85-95% of market (slightly below market):
      Strong bias toward RENEW. Trade-out NPV almost never wins at this gap.
      Only proceed to full analysis if space is highly marketable (small SF,
      second-gen condition, tight submarket).
    70-85% of market (moderately below market):
      GRAY ZONE. Run full NPV. Neither path has a structural advantage.
      Market conditions, TI cost, and vacancy duration will determine outcome.
    50-70% of market (significantly below market):
      Bias toward TRADE-OUT. At 30-50% below market, the rent premium is
      large enough to offset significant vacancy and TI costs in most markets.
      Run full NPV to confirm but expect trade-out to win.
    < 50% of market (severely below market):
      TRADE-OUT in most cases. The rent gap is extreme enough that only
      extraordinary vacancy or TI costs would reverse the NPV advantage.
      Flag for immediate action -- this is a management failure to have
      reached this level. Begin trade-out preparation now regardless of
      NPV timing.

STEP 6: MARKET CONDITIONS CHECK
  What is the submarket vacancy rate?
    < 7% (tight market):
      Bias toward TRADE-OUT if rent gap >15%. Short downtime and multiple
      prospects mean trade-out risk is manageable. Run NPV to confirm.
    7-12% (balanced market):
      Neutral. NPV analysis is the primary decision tool. No structural bias.
    > 12% (soft market):
      Bias toward RENEW. Long expected downtime and TI competition from
      competing buildings make trade-out expensive. Only trade-out if
      rent gap is >30% below market AND tenant is non-credit.

STEP 7: TENANT CREDIT CHECK
  What is the tenant's credit quality?
    Investment-grade rated (e.g., publicly traded, Fortune 500, government):
      Add credit premium to renewal NPV: 10-25bps cap rate tightening for
      retaining a credit tenant. Quantify as dollar value (cap rate improvement
      x NOI). Add to renewal NPV before comparing.
    Non-credit / small business:
      Neutral credit impact. No adjustment needed.
    Troubled / delinquent:
      Bias toward TRADE-OUT. Replacing a troubled tenant with a qualified one
      is a credit quality improvement. Apply 10-20bps cap rate tightening
      to trade-out scenario as a benefit.
```

---

## Part 2: Clear-Cut Cases

### When Renewal Is Always the Right Answer

These conditions produce overwhelming NPV advantage for renewal. Skip full NPV modeling -- proceed directly to deal structuring.

| Condition | Why Renewal Wins |
|---|---|
| Investment-grade credit tenant at 90-100% of market rent | Zero rent gap + credit premium makes trade-out economically irrational |
| Single-tenant building in soft market (vacancy >12%) | 100% vacancy + long downtime = catastrophic carrying cost |
| Anchor retail tenant with co-tenancy exposure | Co-tenancy cascade risk can destroy portfolio economics |
| Lease expiration within 12 months of planned disposition | Vacancy at disposition: double damage (lost rent + cap rate) |
| DSCR covenant within 10% of trigger, tenant is >20% of NOI | Covenant breach risk overrides all economic analysis |
| Submarket vacancy >15% and space >20,000 SF | Double risk: soft market + large block = 18-36 month expected downtime |

### When Trade-Out Is Always the Right Answer

These conditions produce overwhelming NPV advantage for trade-out. Skip full NPV modeling -- proceed directly to marketing preparation.

| Condition | Why Trade-Out Wins |
|---|---|
| Tenant is delinquent (>60 days past due) and showing no recovery | Credit risk exceeds any renewal benefit; replace immediately |
| In-place rent <50% of market in a tight submarket (<7% vacancy) | Extreme rent gap + fast lease-up = trade-out clearly wins |
| Tenant occupying space vastly larger or smaller than actual need (expanding or contracting dramatically) | Tenant will not renew on acceptable terms; market proactively |
| Identified replacement tenant under LOI at market rent + equivalent or better credit | Trade-out risk is eliminated by in-hand deal |
| Tenant defaulted and vacated early | Trade-out is forced; optimize the backfill strategy |

---

## Part 3: The Gray Zone

The gray zone is where the decision is genuinely uncertain and the full NPV analysis plus risk adjustment is required. Entry criteria: none of the clear-cut conditions apply, and the rent gap is 15-35% below market in a balanced (7-12% vacancy) market.

### Gray Zone Variables (rank by impact)

1. **Expected vacancy duration**: this is the single highest-impact variable. A 2-month swing in expected downtime can flip the NPV decision. Get current submarket absorption data before concluding.

2. **New tenant TI**: the second highest-impact variable. A $10/SF difference in TI (e.g., $20 vs. $30/SF) often equals 12-18 months of rent premium for a 10,000 SF space. Negotiate TI before committing to the trade-out path.

3. **Renewal rent achievable**: how much of the rent gap can be recaptured through renewal negotiation? If the tenant will accept $32/SF in a $35/SF market, the renewal effective rent gap narrows. If they insist on $28/SF, trade-out becomes more attractive.

4. **Credit quality differential**: if the new tenant is investment-grade and the current tenant is non-credit, the cap rate benefit of the trade-out may be worth $0.5-1.5M on a meaningful asset. Quantify this explicitly.

5. **Hold period**: a 10-year DCF minimizes the impact of a short vacancy. A 3-year hold period amplifies it dramatically. Always match the analysis period to the expected hold.

### Gray Zone Resolution Protocol

When in the gray zone, resolve in this order:

1. Run the NPV comparison (Workflow 4).
2. Run the breakeven analysis (Workflow 5).
3. Check the sensitivity table: is the NPV delta direction consistent across most cells of the table?
4. Apply the risk adjustment (Workflow 6): does the probability-weighted trade-out NPV still beat renewal?
5. Apply the credit adjustment if applicable.
6. If the decision is still unclear (delta <5% of renewal NPV after all adjustments): default to CONDITIONAL recommendation. Set a specific trigger (e.g., "Trade-out if we have a signed LOI within 6 months; renew if not") and a hard deadline.

---

## Part 4: Renewal Negotiation Floors

Even when renewal is the recommendation, the landlord needs walk-away terms. Use these floors as the minimum acceptable renewal:

| Metric | Minimum Threshold | If Below Threshold |
|---|---|---|
| Renewal rent | 85% of current market rent | Quantify the NPV cost of the discount. If NPV(Trade-Out) > NPV(Renewal at this floor), recommend trade-out. |
| Renewal effective rent | 80% of market effective rent (after TI and LC) | Below this, trade-out is almost certainly better on NPV. |
| Renewal term | 3 years minimum (5 years preferred) | A renewal shorter than 3 years provides minimal WALT benefit and often results in the same trade-out decision in 3 years, at higher cost. |
| Renewal TI | Market TI minus 70% (renewal discount) | If the tenant demands TI approaching new-lease levels, the renewal economic benefit disappears. |

---

## Part 5: Trade-Out Viability Checklist

Before recommending a trade-out, confirm each item:

```
TRADE-OUT VIABILITY CHECKLIST

Pre-Condition Checks:
  [ ] No DSCR covenant breach triggered by vacancy
  [ ] No co-tenancy clause cascade triggered by vacancy
  [ ] No disposition/refi within 12 months (or replacement tenant in LOI)
  [ ] Space is marketable in current condition (or make-ready budget is allocated)

Economics Checks:
  [ ] Trade-out NPV > Renewal NPV (base case)
  [ ] Trade-out NPV > Renewal NPV (risk-adjusted)
  [ ] TI payback period < 24 months (ideally < 18 months)
  [ ] Expected vacancy duration is below breakeven vacancy threshold
  [ ] New rent achievable > breakeven rent threshold

Market Checks:
  [ ] Submarket vacancy < 12% (tight or balanced market)
  [ ] Active prospects or comparable leasing velocity in the submarket
  [ ] No competing building offering dramatically better TI or concession packages
  [ ] Competitive set has no recent large block of similar space added

Operational Checks:
  [ ] Make-ready budget is approved and vendor is identified
  [ ] Marketing materials (floor plan, space sheet) are or can be prepared
  [ ] Leasing team capacity to actively work a new deal
  [ ] Landlord's broker (if retained) is briefed and engaged

If any box is unchecked: address the gap before proceeding with trade-out.
If 3+ boxes are unchecked: reconsider whether trade-out is the right path.
```

---

## Part 6: Post-Decision Action Plans

### If RENEW: Immediate Steps

1. Set negotiation authority: maximum TI, minimum rent, maximum free rent, minimum term.
2. Open dialogue with the tenant (or tenant's broker): express intention to renew, request a meeting within 30 days.
3. Pull market comps to anchor the market rent conversation -- do not let the tenant set the market narrative.
4. Issue a preliminary renewal proposal within 14 days of the decision.
5. Set a hard deadline for LOI execution: typically 6-9 months before expiration.
6. If the tenant does not respond within 30 days: escalate to Workflow 5 (consider transition to trade-out mode).

### If TRADE-OUT: Immediate Steps

1. Notify property management to begin make-ready planning and scoping.
2. Brief the leasing broker (if retained) or begin direct marketing.
3. Set asking rent, concession budget, and target tenant profile.
4. Begin marketing immediately -- do not wait for the existing tenant to vacate.
5. Alert the existing tenant per lease notice requirements (if renewal option has expired or was not exercised).
6. Activate lease-up-war-room protocol for tracking and reporting.
7. Monitor the existing tenant's behavior: a trade-out strategy is vulnerable if the tenant changes their mind and requests renewal. Have a defined policy on whether to re-engage.

### If CONDITIONAL: Immediate Steps

1. Document the specific trigger conditions and deadlines in writing.
2. Begin parallel tracks: engage tenant on renewal terms AND begin preliminary marketing.
3. Set a decision date: by [date], commit to one path and stand down the other.
4. Monitor the trigger conditions weekly.
5. If a qualified prospect appears before the deadline: reassess NPV with identified tenant and accelerate the trade-out decision.
6. If no prospect appears by 90 days before expiration: default to renewal.
