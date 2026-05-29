# Institutional Committee Deck Conventions

This reference GUIDES Claude on the universal conventions every institutional
committee deck must follow, regardless of family, plus the R/Y/G status rubric and
the source-map construction. It is documentation, not a rendering engine. Every
convention below is a composition rule Claude applies to the slide spec; a human
renders the actual deck.

## The non-negotiable conventions

1. **Executive-summary-first.** The first content slide (slide 2, after the cover)
   summarizes the whole deck: the headline metrics and the decision ask. A
   committee member who reads only slide 2 should know what they are voting on and
   why.
2. **Explicit decision ask.** Every committee deck states, on the front slide, the
   exact ask in vote language (GO/NO-GO/CONDITIONAL; APPROVE/REVISE the mark;
   NOTE/APPROVE adjustments; APPROVE the budget). Never implicit.
3. **Returns / metric snapshot near the front.** Headline numbers (returns,
   proposed mark, plan-vs-actual, strategy target) sit on slide 1-2, never buried.
4. **R/Y/G status carried honestly.** Status reflects the data; off-track
   dimensions show yellow or red, with the threshold stated.
5. **Sources & assumptions visible.** A sources-&-assumptions slide sits near the
   decision content (not only in the appendix); every headline figure carries a
   source cue on its face.
6. **Appendix + source-map.** A source-map lists every front-of-deck figure with
   its `source_ref` and `classification`, generated mechanically from the
   exhibits' provenance maps.
7. **Density discipline.** One primary exhibit per slide; no more than ~6 bullets;
   split or move detail to the appendix.
8. **Modeled content labeled.** Any `modeled-assumption` figure carries a visible
   "modeled" tag on the slide and in the source-map. Never dressed as a fact.

## R/Y/G status rubric

Status is a function of data vs. a stated threshold, not of desired outcome. For
each tracked dimension, assign the color and **state the threshold that set it**.
Default thresholds (override with firm policy via brand-guidelines if provided):

| Dimension | GREEN | YELLOW | RED |
|---|---|---|---|
| Returns vs. underwrite | projected return >= target | within 200 bps below target | > 200 bps below target |
| Leasing / occupancy vs. plan | actual >= plan | within 300 bps below plan | > 300 bps below plan |
| Budget variance (opex) | actual <= plan +2% | plan +2% to +8% | > plan +8% |
| Covenant headroom (DSCR) | >= 1.15x of covenant | 1.00x-1.15x of covenant | < covenant |
| Business-plan milestones | on/ahead of schedule | < 1 quarter behind | > 1 quarter behind |
| Valuation confidence | corroborated, recent comps | thin/older comps | stale or conflicting inputs |

Rules:

- A dimension whose underlying exhibit rows are `needs-review` cannot be GREEN —
  cap it at YELLOW until the data is accepted.
- A dimension that depends on a `flagged` figure cannot be shown on a committed
  slide at all — surface the gap.
- Never invent a status for a dimension you have no data for; omit it and note the
  omission.

## Source-map construction

The source-map is the deck's trust instrument. Build it mechanically from the
per-exhibit provenance maps supplied by `warehouse-to-exhibit-mapper`:

```
| Front-of-deck figure | Value | source_ref | classification |
|---|---|---|---|
| <figure label>        | <val> | data-room/<doc>#<anchor> (or model:<path>) | source-fact | calculated | modeled-assumption |
```

- A `source-fact` figure lists the document span it was read from.
- A `calculated` figure lists the contributing source spans (it is derived from
  facts; show the inputs).
- A `modeled-assumption` figure lists `model:<path>` (e.g.,
  `model:underwriting/levered_irr`) and is labeled modeled — never given a
  document `source_ref` it does not have.
- Every figure that appears on a committed slide must have a row here. A figure
  with no resolvable provenance does not go on a committed slide.

## Decision-ask phrasing patterns

| Family | Ask pattern |
|---|---|
| Investment Committee | "Approve acquisition of {asset} at ${price} ({$/unit or $/SF}), {going-in}% going-in, {LTV}% LTV; equity ${equity}." -> GO / NO-GO / CONDITIONAL (+ conditions) |
| Valuation Committee | "Approve {period} mark of ${value}, {±%} vs. prior ${prior}." -> APPROVE / REVISE |
| Quarterly Business Plan | "Note Q{n} performance; approve {adjustment}." -> NOTE / APPROVE |
| Annual Business Plan | "Approve FY{yr} budget of ${opex}/NOI ${noi} and {hold/sell/refi} strategy." -> APPROVE |

## Coherence checklist (run before emitting)

- [ ] Decision ask present, explicit, on the front slide, in vote language.
- [ ] Returns/metric snapshot on slide 1-2.
- [ ] Every front-of-deck figure appears in the source-map with a resolving
      `source_ref` (or `model:<path>` for modeled) and a classification.
- [ ] No `flagged` figure on any committed slide.
- [ ] Every `modeled-assumption` figure labeled "modeled" on slide and in
      source-map.
- [ ] R/Y/G status states the threshold that set each color; no green-washing.
- [ ] One primary exhibit per slide; detail in appendix.
- [ ] Any unfilled blueprint slide named, with the upstream input that would fill
      it.

## What this skill does NOT do

- It does not render slides (no .pptx/.key/.pdf output) — it specifies them.
- It does not write the memo prose (that is `ic-memo-generator`); it places
  narrative blocks.
- It does not build LP fundraising decks (that is `lp-pitch-deck-builder`).
- It does not assemble or validate data (that is `document-to-warehouse-pipeline`)
  or choose chart types from raw datasets (that is `warehouse-to-exhibit-mapper`).
- It does not invent figures. Every number traces to an exhibit's provenance.
