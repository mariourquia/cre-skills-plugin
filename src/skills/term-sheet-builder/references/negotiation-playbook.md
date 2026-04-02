# Negotiation Playbook: CRE Debt Term Sheets

Lender-type-specific negotiation tactics, order of negotiation priority, which terms move and which don't, and worked examples for each major negotiation point. Use in conjunction with Workflow 4 of the term-sheet-builder skill.

---

## Negotiation Principles

**Principle 1: Sequence matters.** Win the most important term first. Lenders have a limited appetite for concessions in a given deal -- spend political capital on the terms that most affect your business plan, not on optics.

**Principle 2: Lead with data.** Every counterproposal should reference a market comparable. "We closed a deal last quarter at SOFR + 325 on a 70% LTV multifamily" is more effective than "your spread is too wide." Use benchmarks from `market-rate-benchmarks.yaml`.

**Principle 3: Bundle low-cost concessions.** Ask for multiple minor concessions simultaneously. Lenders feel better saying yes to a package than yes to multiple individual asks.

**Principle 4: Know your alternatives.** Your leverage disappears if the lender knows you have no competing quote. Always run at least 3 lenders before exclusivity.

**Principle 5: Separate economic from structural terms.** Rate is an economic term -- lenders are constrained by their cost of capital. Structural terms (carve-outs, cash management, reserves) are more negotiable because they don't directly affect the lender's yield.

---

## Lender Type Negotiation Profiles

### Agency (Freddie Mac / Fannie Mae)

**What is negotiable:**
- IO period (significant room, tied to LTV and DSCR)
- Rate lock type (early lock, float-down on select programs)
- Prepayment structure (step-down vs. yield maintenance on select programs)
- Replacement reserve rate (with evidence of recent capital investment)
- Processing timeline (sometimes; priority lane available on select programs)

**What is NOT negotiable:**
- Standard bad-boy carve-out language (agency uses prescribed forms)
- DSCR minimums (hard underwriting floors; lender is at risk for loss)
- LTV maximums (program limits are regulatory constraints)
- Escrow requirements (tax/insurance escrow is non-negotiable on agency)

**Negotiation approach:**
Agency lenders (Optigo/DUS correspondents) compete primarily on rate and IO period. If your DSCR has headroom, argue for a longer IO period explicitly: present DSCR at amortizing payment vs. IO to show the lender that coverage is comfortable either way. Freddie SBL is more flexible on IO terms for smaller loans. For replacement reserves, a capital improvement schedule from the past 5 years (with costs) is the strongest argument.

**Worked example (IO period negotiation):**
```
Lender quote: 0 months IO on 70% LTV deal
Stabilized NOI: $1,500,000
Loan: $12,000,000
Rate: 5.75% (30-year amortization)
  Amortizing debt service: $838,700
  DSCR amortizing: 1.79x

Borrower counterproposal: 3 years IO
  IO debt service: $690,000
  DSCR IO: 2.17x
  Argument: "Our DSCR at amortizing payment is 1.79x -- well above your 1.25x floor.
  At IO we are 2.17x. We are requesting 3 years IO to optimize cash-on-cash return
  while maintaining substantial coverage cushion. This is consistent with agency
  programs at 65-70% LTV with strong DSCR."
  Expected outcome: 2-3 years IO achievable.
```

---

### CMBS

**What is negotiable:**
- IO period (meaningful room at lower LTV)
- Defeasance vs. yield maintenance (on some conduit deals)
- Cash sweep trigger (usually 1.10-1.15x standard; some room to push to 1.05x)
- Distribution test (DSCR threshold for cash distribution; push down to match sweep trigger)
- TI/LC reserve amount (negotiate based on actual lease expiration schedule)
- Rate lock window (60-90 days; negotiate longer for complex deals)
- SPE covenant details (certain provisions in operating agreement)

**What is NOT negotiable:**
- SPE structure (bankruptcy-remote entity is a securitization requirement, not lender preference)
- Lender-ordered appraisal, Phase I, title, and survey (securitization compliance)
- Hard lockout period (securitization requires minimum 2-year lockout)
- SNDA and estoppel requirements from major tenants

**Negotiation approach:**
CMBS is the least flexible loan type post-securitization, but has the most room before securitization (during origination). The key is to negotiate everything in the term sheet -- do not defer issues to loan documents. Once a CMBS loan is originated and securitized, you negotiate with a special servicer, not your original lender.

TI/LC reserve is a common CMBS battleground. Lenders apply a formula; you should counter with an actual analysis of near-term lease rollover and the cost to re-tenant vacant space. If 80% of your leases don't expire for 7 years, you don't need 5 years of TI/LC reserves upfront.

**Worked example (cash sweep trigger negotiation):**
```
Lender position: springing cash sweep at DSCR < 1.20x (quarterly testing)
Property: Class B office, 85% occupied, DSCR 1.35x stabilized
Business plan: lease-up one vacant floor over 12 months

Problem: during lease-up, occupancy drops temporarily as a tenant suite
turns over. DSCR could dip to 1.15x for 1-2 quarters -- triggering sweep.

Counterproposal:
  1. Move trigger to 1.10x (more room)
  2. Change testing frequency to trailing 12-month average (not quarterly spot)
  3. Add a cure mechanism: borrower can deposit 6-month interest reserve to
     cure trigger without invoking cash management

Argument: "Our stabilized DSCR is 1.35x with 95% occupancy as the long-term
target. We anticipate a temporary dip during lease-up. The current trigger
would impose cash management during a routine value-creation phase. Industry
standard for Class B office is 1.15x trailing. We propose 1.10x trailing
12-month with a deposit cure mechanism."
Expected outcome: 1.15x or 1.10x trigger; trailing 12-month testing achievable.
```

---

### Bank Balance Sheet

**What is negotiable:**
Bank balance sheet lenders are the most flexible -- this is a relationship product with no securitization constraints.

- Rate and spread (most leverage here; banks want to win the relationship)
- IO period (significant flexibility, especially if you have a deposit relationship)
- Prepayment (step-down to open is common; push for open after 12-18 months)
- Recourse structure (partial recourse on value-add; negotiate burn-off conditions)
- Reporting requirements (frequency, format)
- Personal financial statement frequency
- Reserve waivers (for recently renovated or strong-DSCR properties)
- Extension options and extension conditions
- Cross-default provisions (push to limit to this property, not all bank relationships)

**What is NOT negotiable:**
- Regulatory reporting (the bank has regulatory obligations you cannot override)
- Flood insurance (if property is in a flood zone)
- Lender-required appraisal independence (must be ordered by lender, not borrower)

**Negotiation approach:**
Banks negotiate as relationship partners. Your strongest leverage is relationship consolidation ("we would move our operating accounts and deposits to your bank"), portfolio size ("we have a 10-property portfolio and are evaluating our banking relationships"), and competitive quotes ("we have three quotes and yours is 25 bps wide -- can you get there?").

For recourse, present your sponsor net worth, liquidity, and track record. Lenders reduce or eliminate recourse for proven sponsors with adequate liquidity. Show net worth > 1.5x loan amount and liquidity > 10% of loan amount.

**Worked example (recourse burn-off negotiation):**
```
Lender position: full recourse during construction and lease-up;
  non-recourse conversion requires 90% occupancy for 6 months
Business plan: mixed-use value-add; target 90% occupancy within 12 months

Counterproposal: burn-off at 85% occupancy for 3 consecutive months
Argument: "Our underwriting shows stabilization at 88% occupancy generates
1.30x DSCR -- comfortably above your 1.25x floor. We propose 85% occupancy
for 90 days as the burn-off threshold, consistent with the market standard
for our property type in this submarket. Our sponsor has a track record of
9 similar value-add dispositions, all achieving 90%+ occupancy within 14 months."
Expected outcome: 85-87% occupancy threshold; 90-day lookback achievable.
```

---

### Bridge (Debt Funds / Mortgage REITs)

**What is negotiable:**
- Rate / spread (meaningful room, especially with competing quotes)
- IO period (usually full-term IO; rare bridge loan is not full IO)
- Extension conditions (most critical bridge negotiation point)
- Exit fee (sometimes waived or reduced for well-performing loans)
- Future funding structure (draw schedule, inspection requirements)
- Completion guaranty scope (full vs. budget-completion; burn-off conditions)
- Prepayment structure (negotiate open from day 1, or at minimum after 6 months)
- Rate cap strike and term

**What is NOT negotiable:**
- Floating rate structure (bridge lenders do not offer fixed rate)
- Rate cap requirement (lenders require rate caps on floating loans)
- Future funding inspection process (third-party inspector is lender's protection)

**Negotiation approach:**
Bridge lenders compete aggressively for good deals. Your leverage is your business plan quality, sponsor track record, and competing quotes. Extension conditions are the most important negotiation because the bridge loan's value is in its flexibility -- if extension conditions are unachievable, the loan is a trap.

Focus on extension condition 3 (DSCR test): push for as-stabilized pro forma DSCR, not trailing 12-month. Present your leasing plan, executed LOIs, and signed leases. If you have 80% of target occupancy under lease, the trailing DSCR will lag the business plan by 12 months -- that's not a risk, that's normal lease-up.

**Worked example (extension condition negotiation):**
```
Lender position:
  Extension 1 conditions: (1) no default; (2) 85% occupancy;
  (3) DSCR > 1.15x trailing 12-month; (4) extension fee 0.50%

Problem: property is 70% occupied with 3 signed LOIs (85% at signing).
DSCR at 85% occupancy is 1.18x stabilized but trailing DSCR at closing
is 0.85x (renovation phase). Trailing 12-month test is unachievable.

Counterproposal:
  Extension 1 conditions: (1) no monetary default; (2) 80% executed leases
  (not LOIs, but signed leases); (3) no DSCR test (replace with occupancy);
  (4) extension fee 0.375%

Argument: "Our stabilized DSCR at 85% occupancy is 1.18x as-stabilized.
The trailing 12-month test does not reflect the business plan -- a value-add
property in lease-up will show below-1.0x trailing DSCR while generating
value. The industry standard for bridge extension conditions is a minimum
occupancy test (80-85% executed leases) without a DSCR test during
lease-up. We propose a 0.125% fee reduction given our strong sponsor
track record and property location."
Expected outcome: 80-82% occupancy test (no DSCR); reduced extension fee possible.
```

---

## Universal Negotiation Priority Order

When you cannot negotiate everything, prioritize in this order based on business plan impact:

| Priority | Term | Business Plan Impact | Typical Win Rate |
|---|---|---|---|
| 1 | IO period length | Direct cash-on-cash return impact | High (60-80% of asks succeed) |
| 2 | Extension conditions | Downside protection on value-add | Medium-High (50-70%) |
| 3 | Prepayment structure | Exit flexibility and cost | Medium (40-60%) |
| 4 | Carve-out scope | Guarantor exposure | Medium (40-60%) |
| 5 | Cash sweep trigger | Distribution access during stress | Medium (30-50%) |
| 6 | Reserve requirements | Upfront capital efficiency | Medium (40-60%) with evidence |
| 7 | Rate lock window | Rate risk management | High (70-85%) |
| 8 | Guaranty burn-off conditions | Long-term risk mitigation | Medium (30-50%) |
| 9 | Exit fee reduction | Cost at payoff | Low-Medium (20-40%) |
| 10 | Spread reduction | Cost of capital | Low (10-30%); market-dependent |

---

## Negotiation Scripts by Term

### IO Period

Opening: "Our acquisition model was underwritten to include an IO period. The cash-on-cash return differential between IO and amortizing is [X bps]. We would like to discuss extending the IO period to [X] years. Our DSCR at the amortizing payment is [X.XX]x -- [X] bps of cushion above your [X.XX]x floor -- which supports additional IO without meaningful credit risk to you."

Counter if lender refuses full IO: "We understand your constraint. Would you consider a partial IO structure -- [X] years IO transitioning to [X]-year amortization? This gives you amortization in the later years while allowing us to execute the business plan in the critical early period."

### Prepayment (Defeasance to Step-Down)

Opening: "Our target hold is [X] years, but we need flexibility for an opportunistic exit if market conditions improve. Defeasance on a [X]-year loan in the current rate environment costs approximately [X] points at our projected exit -- effectively a prepayment penalty equivalent. We would like to request a step-down prepayment structure: [X]% in year 3, [X]% in year 4, open thereafter. This provides you certainty on the loan's initial term while giving us a clear exit path."

Counter if lender insists on defeasance: "Would you accept yield maintenance as an alternative to defeasance? Yield maintenance is more transparent in cost and eliminates the operational complexity of defeasance while providing equivalent economic protection to you."

### Carve-Out Scope

Opening: "We've reviewed the carve-out guaranty draft and noted [specific expansion]. This provision would impose full recourse in the event of [specific trigger] -- which is an operational metric rather than a bad act. Standard market practice limits carve-outs to actual bad acts (fraud, waste, misappropriation, voluntary bankruptcy). We would like to remove [specific provision] or limit it to situations involving actual misconduct by the guarantor."

Counter if lender insists: "We can accept a modified version: rather than full loan amount recourse on [trigger], can we agree to actual damages only? This aligns the guaranty exposure with the harm caused while maintaining your protection against intentional misconduct."

### Extension Conditions (DSCR test)

Opening: "Extension condition [X] requires trailing 12-month DSCR > [X.XX]x. Our business plan projects stabilized DSCR of [X.XX]x, but trailing DSCR at the extension date will be below 1.0x because we will still be in active lease-up. This is by design -- the property is not impaired, it is being value-created. We propose replacing the DSCR test with a minimum occupancy of [X]% executed leases and a rent achievement test of [X]% of projected asking rent."

### Reserve Requirements

Opening: "The replacement reserve requirement of $[X]/unit exceeds our capital plan needs. This property completed a $[X]/unit renovation [X] years ago, including [roof, HVAC, plumbing, elevators, etc.]. Our 10-year capital plan projects $[X]/unit in annual reserves. We request a reduction to $[X]/unit with a provision that we may request a lender review at [year X] of the loan term."
