# Committee Deck-Family Blueprints

This reference GUIDES Claude in composing each of the four institutional committee
deck families. It is documentation, not a rendering engine — nothing here produces
a slide file. Each blueprint defines the deck's audience, the decision ask form,
the required slides and storyline, and the exhibits each slide expects (the exhibit
forms come from `warehouse-to-exhibit-mapper`'s
`references/exhibit-type-selection.md`).

A composed deck for any family must satisfy the universal conventions in
`committee-deck-conventions.md`: executive-summary-first, explicit decision ask,
returns/metric snapshot near the front, R/Y/G status carried honestly, sources &
assumptions visible, appendix + source-map.

---

## 1. Investment Committee (transaction approval)

- **Audience**: the firm's investment committee voting on whether to acquire.
- **Decision ask**: **GO / NO-GO / CONDITIONAL** on a specific acquisition at
  specific terms (price, going-in cap, leverage, equity). If CONDITIONAL, name
  the 1-3 conditions.
- **Complements**: `ic-memo-generator` writes the memo prose; this deck presents
  the same decision visually. Do not duplicate the memo's full body on slides —
  place its thesis, key risks, and recommendation.

| # | Slide | Expects |
|---|---|---|
| 1 | Cover | brand cover, asset name, confidentiality |
| 2 | Executive Summary & Decision Ask | Returns snapshot (KPI strip), 1-2 sentence thesis, explicit GO/NO-GO/CONDITIONAL ask, R/Y/G strip |
| 3 | Opportunity / Thesis | thesis detail; why this, why now |
| 4 | Deal Overview & Sources/Uses | Sources & Uses table; terms summary |
| 5 | Market | submarket fundamentals; supply/demand |
| 6 | Financial Snapshot | NOI walk (waterfall); cash flow by year (column) |
| 7 | Risk & Sensitivities | sensitivity heat-map; key-risk list (from memo) |
| 8 | Recommendation | verdict + conditions (from memo) |
| 9 | Sources & Assumptions | key assumptions; modeled items labeled |
| A1+ | Appendix + Source Map | detail tables; full assumption schedule; per-figure source_ref map |

---

## 2. Valuation Committee (mark / valuation walk)

- **Audience**: the valuation committee approving a periodic mark.
- **Decision ask**: **APPROVE / REVISE** the proposed mark (state the proposed
  value and the change vs. prior, e.g., "Approve Q2 mark of $52.4M, +3.1% vs.
  prior").
- **Note**: marks are sensitive; unrealized values must rest on conservative,
  sourced inputs. Label every modeled input (assumed cap rate, projected NOI) as
  modeled. Never present a desired mark as if the data produced it.

| # | Slide | Expects |
|---|---|---|
| 1 | Cover | brand cover, asset/position, confidentiality |
| 2 | Mark Summary & Ask | proposed mark vs. prior (KPI strip), explicit APPROVE/REVISE ask, R/Y/G on valuation confidence |
| 3 | Value Walk | waterfall: prior mark -> NOI change -> cap-rate change -> capex -> new mark |
| 4 | Cap Rate / Yield Bridge | how the cap-rate assumption moved and why |
| 5 | Comp Support | comp set table supporting the mark |
| 6 | Mark History | line: mark trend over prior periods |
| 7 | Assumptions & Limitations | every modeled input labeled; limitations stated |
| A1+ | Appendix + Source Map | comp detail; valuation inputs with source_ref map |

---

## 3. Quarterly Business Plan / Asset Review (performance vs. plan)

- **Audience**: asset-management / portfolio committee reviewing quarterly
  performance against the business plan.
- **Decision ask**: usually **NOTE / APPROVE plan adjustments** (note performance;
  approve any proposed changes to the plan, budget reforecast, or hold thesis).
- **Status is central**: this family always carries the R/Y/G strip up front;
  status reflects actual vs. plan, not aspiration.

| # | Slide | Expects |
|---|---|---|
| 1 | Cover | brand cover, asset, period, confidentiality |
| 2 | Plan vs. Actual Snapshot & Status | plan-vs-actual KPI strip, R/Y/G strip, any asks |
| 3 | NOI Variance | waterfall: plan NOI -> revenue variance -> expense variance -> actual NOI |
| 4 | Leasing / Occupancy Trend | line vs. plan reference line |
| 5 | Budget vs. Actual by Line | table of line items off plan |
| 6 | Business-Plan Execution | column/table: milestone progress |
| 7 | Asks / Adjustments | proposed plan/budget changes to approve |
| A1+ | Appendix + Source Map | full budget-vs-actual; source_ref map for actuals |

---

## 4. Annual Business Plan (budget + strategy)

- **Audience**: the committee approving next year's operating budget and asset
  strategy.
- **Decision ask**: **APPROVE** the proposed budget + strategy (including any
  hold / sell / refinance recommendation).
- **Complements**: pulls hold/sell/refi inputs that other skills
  (`disposition-strategy-engine`, `refi-decision-analyzer`) may have produced;
  this deck presents the recommendation, it does not re-derive it.

| # | Slide | Expects |
|---|---|---|
| 1 | Cover | brand cover, asset, plan year, confidentiality |
| 2 | Strategy Summary & Ask | strategy target (KPI strip), explicit APPROVE ask, R/Y/G on plan confidence |
| 3 | Proposed Budget | next-year operating budget table |
| 4 | NOI Trajectory | line/column: multi-year NOI under the plan |
| 5 | Capex Plan | table: planned projects and timing |
| 6 | Hold / Sell / Refi Inputs | the inputs behind the strategy recommendation |
| 7 | Risks | plan risks; mitigations |
| A1+ | Appendix + Source Map | budget detail; assumption schedule with source_ref map |

---

## Cross-family rules

- **Short variant** (`length_target: short`) for any family: Cover -> Decision
  Ask + snapshot -> one primary exhibit -> risks/status -> Source Map. Use when
  the committee wants a tight read.
- **One primary exhibit per slide** (density limit). Split or move detail to the
  appendix.
- **Unfillable slide**: if a blueprint slide's exhibit is missing or was excluded
  (flagged), leave it unfilled in the slide map and name the upstream input that
  would fill it. Never fabricate an exhibit to complete the deck.
- **Decision ask is mandatory and explicit** for all four families, on the front
  slide, in the language the committee votes on.
