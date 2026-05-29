# IC Question Taxonomy and Source-Grounding Methodology

This reference defines the standard investment committee (IC) question set, the
mapping from each question to the upstream artifact that should answer it, and
the fail-closed rules the skill enforces. The taxonomy reflects how
institutional real estate IC sessions actually run: members interrogate the
deal team across a predictable set of categories, and a prepared team answers
every question with a number traceable to the underwriting or diligence file.

All numeric values below are **illustrative** and exist only to show the shape
of an answer and how it cites a source. They are not market data and must never
be presented as benchmarks. Real answers must cite real upstream outputs.

---

## 1. Why source grounding, not recall

In committee, the failure mode is not "the team did not know the answer." It is
"the team gave a confident number that did not match the model." Once one
answer is shown to be off, every other answer is doubted. The discipline that
prevents this is simple and absolute:

- An answer may state a fact only if that fact exists in the assembled source
  index with a citable `sourceRef`.
- The answer quotes the upstream value; it does not re-derive it.
- If the fact is not in the index, the question is a context gap, not an
  invitation to estimate.

This is the same posture used in the AMOS prototype's coherence check, where
every dollar, percentage, and basis-point claim in a generated artifact must
reconcile to a row or computed total in the underlying data within tolerance, or
the artifact fails closed and surfaces the missing source.

---

## 2. The seven canonical IC categories

Committees cluster their questions into seven recurring categories. The skill
organizes the Q&A pack under these headings and orders them by the
`committee_profile` priority when known (credit-led committees open on Debt;
return-led committees open on Returns).

### A. Returns and Sensitivity
What the deal makes and how fragile that is.

### B. Basis and Valuation
What is being paid and whether the basis is defensible.

### C. Debt and Covenants
How the capital stack behaves and where it breaks.

### D. Physical and Capital
What the building needs and whether reserves cover it.

### E. Market and Demand
Whether the demand thesis holds.

### F. Sponsor and Execution
Whether this team can deliver the plan.

### G. Downside and Exit
What happens when the plan does not hold, and how capital gets out.

---

## 3. Question-to-source mapping

Each canonical question is paired with the upstream artifact whose `sourceRef`
should answer it. If that artifact is absent from the inputs, the question
becomes a context gap and the gap report names the skill that would close it.

| # | Category | Canonical question | Primary source artifact | Upstream skill |
|---|---|---|---|---|
| 1 | Returns | What is the levered and unlevered IRR? | `underwriting/levered_irr`, `underwriting/unlevered_irr` | acquisition-underwriting-engine |
| 2 | Returns | What drives the return: NOI growth or cap compression? | `underwriting/return_attribution` | acquisition-underwriting-engine |
| 3 | Returns | How does IRR move if exit cap widens 50 bps? | `underwriting/downside_irr`, `underwriting/sensitivity_grid` | acquisition-underwriting-engine / sensitivity-stress-test |
| 4 | Returns | What is the equity multiple and average cash-on-cash? | `underwriting/equity_multiple`, `underwriting/avg_coc` | acquisition-underwriting-engine |
| 5 | Basis | What is price per unit / per SF and how does it compare to replacement cost? | `underwriting/price_per_unit`, `underwriting/replacement_cost_ratio` | acquisition-underwriting-engine |
| 6 | Basis | What is the going-in vs. stabilized cap rate, and what is the spread? | `underwriting/going_in_cap`, `underwriting/stabilized_cap` | acquisition-underwriting-engine |
| 7 | Basis | Is the normalized NOI defensible? | `underwriting/normalized_noi`, `underwriting/normalization_adjustments` | t12-normalizer |
| 8 | Debt | What is the loan amount, LTV, rate, term, and IO period? | `debt_quote/loan_amount`, `debt_quote/ltv`, `debt_quote/rate` | loan-sizing-engine / agency-loan-quote-analyzer |
| 9 | Debt | What is the debt yield and is it above the lender's floor? | `debt_quote/debt_yield` | agency-loan-quote-analyzer |
| 10 | Debt | What are the covenants and where is the first breach point? | `debt_quote/covenants`, `underwriting/dscr_schedule` | agency-loan-quote-analyzer / debt-covenant-monitor |
| 11 | Debt | Is there negative leverage at going-in? | `underwriting/going_in_cap`, `debt_quote/rate` | acquisition-underwriting-engine |
| 12 | Physical | What are the immediate repairs and the reserve per unit/SF? | `pca/immediate_repairs`, `pca/reserve_per_unit` | pca-reserve-analyzer |
| 13 | Physical | Does the proforma reserve cover the 12-year capital schedule? | `pca/capital_schedule`, `underwriting/reserve_assumption` | pca-reserve-analyzer |
| 14 | Market | What is submarket vacancy, absorption, and the supply pipeline? | `diligence/market/vacancy`, `diligence/market/pipeline` | dd-command-center / submarket-truth-serum |
| 15 | Market | What is the rent mark-to-market vs. in-place? | `underwriting/mark_to_market` | rent-roll-analyzer |
| 16 | Sponsor | How many comparable deals has the sponsor closed? | `diligence/sponsor/track_record` | dd-command-center / document-to-data-room-extractor |
| 17 | Downside | What is the break-even occupancy and DSCR? | `underwriting/breakeven_occupancy`, `underwriting/min_dscr` | acquisition-underwriting-engine |
| 18 | Downside | What does the red team consider the single biggest risk? | `red_team/top_challenge` | ic-red-team-challenger |
| 19 | Exit | What is the exit assumption and the buyer pool at exit? | `underwriting/exit_cap`, `diligence/exit/buyer_pool` | acquisition-underwriting-engine |

---

## 4. Worked answer examples (illustrative numbers only)

These show the required answer shape: a short claim, every number cited. The
figures are invented for format demonstration.

**Q (#9): What is the debt yield and is it above the lender's floor?**

> Debt yield is 8.1% on normalized NOI, above the agency floor of 7.5% cited in
> the quote, leaving roughly 60 bps of cushion before a paydown is triggered.
> Sources: `riverside-gardens/debt_quote/debt_yield`,
> `riverside-gardens/debt_quote/debt_yield_floor`

**Q (#11): Is there negative leverage at going-in?**

> Going-in cap rate is 5.4% versus an all-in loan rate of 6.1%, so the deal
> carries negative leverage at acquisition; accretion depends on the year-2 NOI
> lift bringing the stabilized cap above the loan rate.
> Sources: `riverside-gardens/underwriting/going_in_cap`,
> `riverside-gardens/debt_quote/rate`, `riverside-gardens/underwriting/stabilized_cap`

**Q (#12): What are the immediate repairs and the reserve per unit?**

> The PCA identifies 0.4M dollars of immediate repairs and recommends a reserve
> of 350 dollars per unit per year; the proforma underwrites 300 per unit, a
> gap the team should close or explain.
> Sources: `riverside-gardens/pca/immediate_repairs`,
> `riverside-gardens/pca/reserve_per_unit`, `riverside-gardens/underwriting/reserve_assumption`

Note how the third example does not hide the 50-dollar-per-unit shortfall: it
cites both the recommended and underwritten figures and lets the discrepancy
surface. That is the source-grounded posture in practice.

---

## 5. Fail-closed decision rules

The skill applies these rules in order to every drafted answer:

1. **No sourceRef -> refuse.** If a numeric claim has no citation, suppress the
   answer and emit the governed refusal string. Never ship a partially sourced
   answer.
2. **Reconcile within tolerance.** Compare each cited claim to its source value.
   Default tolerances: +/-10K dollars, +/-0.5 percentage points, +/-2 bps,
   +/-0.05x ratios. Outside tolerance is a reconciliation break, surfaced to the
   team, not silently resolved.
3. **Out-of-context -> refuse.** Any question outside this deal's source index
   (another deal, a market opinion with no cited input, a projection beyond the
   modeled hold, or anything resembling investment advice) returns the governed
   refusal string regardless of what general knowledge would suggest.
4. **Stale input -> flag.** If an input artifact predates the latest
   underwriting revision, mark every answer citing it as potentially stale.
5. **Missing spine -> stop.** If there is no underwriting pack, do not build the
   index; request it.

---

## 6. Governed refusal string (canonical)

Use verbatim for any unanswerable or out-of-context question:

> "This question is outside the assembled IC context pack. No source artifact
> supports an answer, so it is not answered here. To answer it, add the missing
> input: [name the upstream skill or document that would supply it]."

The refusal is not a failure of the pack; it is the pack working as designed. A
committee trusts a Q&A brief precisely because it declines to answer what it
cannot source.
