# Red Team Methodology for CRE Investment Recommendations

This file defines the analytical discipline behind the IC Red Team Challenger. It is a methodology reference, not a data table. All specific numbers below are labeled illustrative and exist only to show the shape of the output; they are not benchmarks to be quoted into a live deal.

## Purpose and Stance

The red team exists to make a recommendation survivable, not to kill it. The failure mode of a deal team is not stupidity; it is motivated reasoning under a deadline. A team that has spent three weeks and real diligence dollars on a deal is anchored to the thesis that justified the work. The red team's value is structural: it forces the separation of what is known from what is assumed, drags disconfirming evidence into the open, and converts soft worries into hard, falsifiable decision lines.

A good red team review does three things a sponsor cannot reliably do for its own deal:

1. **Steelmans before it attacks.** Attacking a strawman version of the thesis wastes the committee's time and lets the real weakness hide. State the strongest honest version of the bull case first.
2. **Quantifies every objection.** "Rates could rise" is not a risk; it is an anxiety. "A 75 bps move in the takeout rate cuts levered IRR by ~310 bps and pushes refi proceeds ~8% below the assumed payoff" is a risk. The discipline is to attach a probability band and a dollar/bps impact to everything.
3. **Pairs every challenge with a prepared answer.** The output is not a list of fears; it is a rehearsal. Each sharp question the committee will ask comes with the grounded, sourced answer the team should walk in ready to give. A question with no prepared answer is itself the finding.

## The Four Categories of Risk

The core taxonomy borrows from the known/unknown matrix and adapts it to CRE underwriting.

### 1. Known Knowns -> Known Risks (quantified)

Risks the team can already see and has likely already named. The red team's job here is not discovery; it is rigor. Reject any known risk stated without a number. Force each into: probability band, IRR impact, equity-dollar impact, early-warning indicator, in-plan mitigant, residual rating. Rank by impact on equity, never by ease of mitigation, because the easy-to-mitigate risks are not the ones that lose money.

### 2. Known Unknowns -> Diligence Gaps

Things the team knows it does not yet know: open diligence, unverified model inputs, data assumed but not confirmed. The discipline is to price the gap. For each: what is unknown, why it changes the verdict, the cost and time to resolve, and the fallback if it cannot resolve before the decision date. The most dangerous known unknowns in CRE are the inputs the model treats as facts: in-place rents (confirm via estoppels), structural reserves (confirm via PCA), tax basis at the new purchase price (confirm via the assessor's methodology, not the seller's historical bill), and real market rents (confirm via signed leases, not asking rents).

### 3. Unknown Unknowns -> Regime and Tail Risk

The risks that do not appear in the model because the model assumes the current regime persists. These cannot be enumerated by inspecting the spreadsheet; they require structured prompting against the model's silent assumptions. The three highest-value prompts:

- **What regime is silently assumed?** Most underwriting assumes today's rate path, today's cap-rate level, and today's credit availability at the refinance date. Name each assumption and ask what happens if it breaks.
- **What second-order effect is ignored?** A single tenant's industry concentration, a supply wave not yet permitted, an insurance market that reprices the entire asset class, a submarket that loses its demand driver.
- **What correlation is assumed to be zero that is not?** In a recession, vacancy rises and exit cap widens together; they are not independent. The refi rate and the exit value move together. Underwriting that stresses one variable at a time understates joint tail risk. This is why the "what breaks first" cascade from a stress test matters: it is the closest the model gets to correlated stress.

### 4. Unknown Knowns -> Anchors and Blind Spots

The things the team knows but has discounted because they cut against the thesis: the comp that does not fit, the prior deal in this submarket that underperformed, the broker pro forma that the team knows is aggressive but used anyway as the starting point. Naming the anchor is half the mitigation. The most common anchors in CRE: the broker's pro forma, a single recent trophy comp, the seller's un-normalized T-12, and the sponsor's last win in a different cycle.

## Disconfirming-Evidence Discipline

For each load-bearing assumption, the analyst must write the question whose answer would *disprove* the thesis and name the source that could answer it. This inverts the default search. Confirmation-seeking finds the comp that supports the rent; disconfirmation-seeking asks for the renovated comps that leased *below* the assumed premium, net of concessions, in the last six months. The rule: if you cannot state the evidence that would make you walk away, you have not underwritten the assumption; you have asserted it.

## Break-Trigger Discipline

A sensitivity shows how IRR moves as a variable moves. A break trigger names the specific value at which the deal stops clearing its hurdle, breaches a covenant, or cannot refinance. The conversion from sensitivity to trigger is what makes the output actionable: it gives the committee decision lines, not gradients.

For each key variable, compute the value at which one of the following fails:
- The return falls below the equity hurdle (e.g., levered IRR below the fund target).
- A debt covenant trips (DSCR or debt yield below the covenant floor).
- The refinance cannot clear (takeout proceeds below the maturing loan balance plus costs).
- Breakeven occupancy exceeds a level with no operational cushion.

Then express **headroom** as the percentage move from base case to the break trigger. Headroom is the single most useful number the red team produces, because it translates abstract risk into "how much can go wrong before this is a problem."

Illustrative example (numbers are illustrative, not benchmarks): a deal underwrites a 5.50% exit cap and breaks its equity hurdle at a 6.10% exit cap. Headroom is ~60 bps, roughly an 11% move. If the same deal also breaks its DSCR covenant at a 9% NOI haircut, the covenant is the tighter constraint and becomes the headline trigger.

## Headroom Guidance (Illustrative Reference Points)

The thresholds below are starting reference points for institutional core-plus and value-add. They are illustrative, not hard limits; always state the reference point you are applying and adjust for strategy and capital structure.

| Constraint | Illustrative "thin headroom" reference | Why it matters |
|---|---|---|
| Exit cap to hurdle | breaks within ~25 bps of base | Normal cap-rate drift over a hold can exceed 25 bps |
| DSCR / debt-yield covenant | clears base by less than ~10% | One soft quarter trips a technical default |
| Refi takeout rate | needs a rate ~100 bps+ below today | A refi cliff is a financing risk dressed as a return |
| Lease-up / renovation pace | breaks if pace slips ~3 months | Construction and leasing routinely slip a quarter |
| Breakeven occupancy | base-case breakeven above ~90% | No cushion for tenant rollover or move-out |

## Single-Assumption Concentration Test

If more than roughly 60% of the return swing in the tornado traces to a single variable, the deal is a bet on one number rather than a diversified thesis with a margin of safety. This is not automatically disqualifying (a credit-tenant NNN deal is legitimately a bet on the tenant's credit), but it must be named explicitly and the committee must be making that single bet knowingly. The illustrative 60% figure is a prompt to investigate concentration, not a pass/fail line.

## Verdict Discipline

The red team judges defensibility, not value. It does not re-underwrite. The three verdicts:

- **DEFENSIBLE**: the case survives the attack; proceed to the memo.
- **DEFENSIBLE WITH CONDITIONS**: name the 2-4 specific diligence items or structure changes that must close before the verdict holds.
- **NOT YET DEFENSIBLE**: the load-bearing assumption is unsupported by evidence, or a break trigger has too little headroom; return to underwriting.

Every verdict ties to specific findings from the risk register, the disconfirming prompts, and the break triggers, never to a general feeling. The red team that cannot point to the finding behind its verdict has not done the work.

## Anti-Patterns the Red Team Must Avoid

- **Generic worry**: "market conditions could deteriorate" with no variable, no number, no trigger. Banned.
- **Killing for sport**: raising risks with no path to mitigation and no headroom analysis. The goal is a survivable case, not a body count.
- **Asymmetric scrutiny**: attacking the downside while leaving the upside assumptions unexamined. Steelman first; then attack both directions.
- **Re-underwriting**: rebuilding the model instead of judging whether the existing one is defensible. Stay in your lane; cite the upstream skills.
- **Unsourced answers**: pairing a challenge question with an answer the team cannot actually support from diligence. An unsourced prepared answer is worse than none.
