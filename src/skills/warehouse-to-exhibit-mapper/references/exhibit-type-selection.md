# Exhibit-Type Selection Guide

This reference GUIDES Claude in choosing the right exhibit form (table vs. chart,
and which chart) for a CRE committee deck, and lists the default exhibit set per
deck family. It is documentation, not a rendering engine — nothing here draws a
chart. Every choice is a model-generated specification a downstream composer
implements.

## First principle: match the form to the question

| The reader needs... | Use | Why |
|---|---|---|
| Exact figures, line-item detail, many fields per entity | **Table** | Precision and density; the eye looks up a value |
| A trend over time | **Line chart** | Slope and direction read instantly |
| A part-to-whole change (a "walk" / bridge) | **Waterfall** | Shows how a starting value becomes an ending value via signed steps |
| A comparison across a few categories | **Column / bar chart** | Length comparison is the most accurate visual judgment |
| A composition (mix) | **Stacked bar / 100% bar** | Part-to-whole at one or a few points in time |
| A two-variable sensitivity | **Heat-map grid** | Color encodes the outcome across a 2-D parameter space |
| A relationship between two continuous variables | **Scatter** | Correlation/outliers; rarely needed in CRE committee decks |

Tie-breakers:

- If the audience will read exact dollars off the exhibit (sources & uses, debt
  terms), prefer a **table** even when a chart is possible.
- If there are more than ~7 categories, a chart becomes cluttered — switch to a
  table or aggregate the long tail into "Other".
- Every **chart** must still specify a backing data table (the composer and the
  source-map appendix require it). A chart without backing rows cannot be
  provenance-mapped and must not be emitted.

## Density limits (deck craft)

- One primary chart **or** one focused table per slide. If an exhibit needs both
  a chart and a detail table, either bind the table to the appendix or split into
  two slides.
- A KPI strip (3-5 headline metrics) may share the header of a slide that also
  carries one primary exhibit.
- A table over ~12 rows usually belongs in the appendix with a summarized version
  on the main slide.

## Provenance rule for every exhibit

Each cell and each plotted point keeps a pointer to its `source_ref` and
`classification` (carried from the warehouse dataset). Aggregated points (a bar
that sums rows) carry the full set of contributing `source_ref`s and are
classified `calculated`. A `modeled-assumption` field carries a visible "modeled"
tag. This is non-negotiable: it is what lets the deck's source-map appendix be
generated mechanically.

## Default exhibit sets by deck family

The deck family selects a default storyline and exhibit set. The mapper may add
user-requested exhibits on top.

### investment-committee (transaction approval)

| Exhibit | Form | Question | Typical slide |
|---|---|---|---|
| Returns Snapshot | Table (KPI strip) | What are the headline returns? | Executive Summary (front) |
| Sources & Uses | Table | How is the deal capitalized? | Deal Overview |
| NOI Walk (in-place -> stabilized) | Waterfall | How does NOI bridge to stabilized? | Financial Snapshot |
| Cash Flow by Year | Column | What is the annual cash profile over the hold? | Financial Snapshot |
| Sensitivity (exit cap x rent growth) | Heat-map | How robust are returns to the two key drivers? | Risk |
| Rent Roll Summary | Table | Who pays the rent, and what rolls when? | Asset |
| Debt Terms | Table | What are the financing terms and covenants? | Capital Structure |
| Sources & Assumptions / Source Map | Table | Where does every number come from? | Appendix |

### valuation-committee (mark / valuation walk)

| Exhibit | Form | Question | Typical slide |
|---|---|---|---|
| Mark Summary | Table (KPI strip) | What is the proposed mark vs. prior? | Front |
| Value Walk (prior mark -> new mark) | Waterfall | What drove the change in value (NOI, cap rate, capex)? | Valuation |
| Cap Rate / Yield Bridge | Waterfall or table | How did the cap rate assumption move? | Valuation |
| Comp Set | Table | What do comparable marks/sales support? | Support |
| Mark History | Line | How has the mark trended over prior periods? | Support |
| Sources & Assumptions / Source Map | Table | Provenance of the mark inputs | Appendix |

### quarterly-business-plan (performance vs. plan / asset review)

| Exhibit | Form | Question | Typical slide |
|---|---|---|---|
| Plan vs. Actual KPI strip | Table (KPI strip) | Are we on plan this quarter? | Front |
| NOI Variance (plan vs. actual) | Waterfall | What explains the NOI variance to plan? | Performance |
| Occupancy / Leasing Trend | Line | How is occupancy/leasing trending vs. plan? | Leasing |
| Budget vs. Actual by Line | Table | Which line items are off plan? | Operations |
| Capex / Business-Plan Progress | Column or table | How far along is the business plan? | Execution |
| Sources & Assumptions / Source Map | Table | Provenance of actuals | Appendix |

### annual-business-plan (budget + strategy)

| Exhibit | Form | Question | Typical slide |
|---|---|---|---|
| Strategy Summary | Table (KPI strip) | What is the asset strategy and target? | Front |
| Proposed Budget by Line | Table | What is next year's operating budget? | Budget |
| NOI Trajectory (multi-year) | Line or column | How does NOI grow over the plan horizon? | Plan |
| Capex Plan | Table | What capital projects are planned and when? | Capital |
| Hold/Sell or Refi Decision Inputs | Table | What does the strategy recommendation rest on? | Strategy |
| Sources & Assumptions / Source Map | Table | Provenance of budget assumptions | Appendix |

## Worked examples

- A 5-step NOI bridge (In-Place -> +Loss-to-Lease -> +Reno Lift -> -Vacancy ->
  Stabilized) is a **waterfall**, not a table: it is a part-to-whole change.
  Specify start bar, ordered signed delta bars (each tied to its source rows),
  end bar.
- A sources & uses with 8-12 line items is a **table**: the reader wants exact
  dollars and percentages, not a pie.
- An exit-cap (rows) x rent-growth (columns) IRR matrix is a **heat-map grid**:
  color encodes IRR; cells carry the calculated classification and the contributing
  model refs.
- Quarterly occupancy vs. planned occupancy is a **line chart** with a reference
  line for plan; both series specify their backing rows.
