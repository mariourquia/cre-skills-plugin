# Executive Output Contract

This document defines the output-structure rubric that every
final-marked workflow must honor. It exists because decision-grade
deliverables — board packets, LP quarterly letters, lender reports, IC
memos — fail when the verdict is buried or when numeric cells have no
source classification.

Scope: final-marked workflows (see `_core/final_marked_workflows.yaml`):

- `executive_operating_summary_generation`
- `investment_committee_prep`
- `quarterly_portfolio_review`
- `executive_pipeline_summary`

## Rule 1. Verdict-first

The first section of every final-marked output MUST be a verdict block
that stands alone without any subsequent section.

A verdict block contains:

- **Recommendation / call:** one sentence. Proceed / hold / refuse /
  approve / escalate / re-underwrite. Unambiguous.
- **Three-bullet rationale:** the 3 specific drivers behind the call,
  each citing a metric or evidence item.
- **Confidence:** one of `high`, `medium`, `low`, `refused`. If
  `refused`, include the missing-input reason inline.
- **Materiality:** dollar or % figure that frames the decision scope.
- **Next action:** one concrete ask with owner + due date.

Everything that follows is evidence, not verdict. If a reader stops
after the verdict block, they have the actionable signal.

## Rule 2. Source-class labels on numeric cells

Every numeric cell in a table, every $ / % figure in narrative, and
every threshold reference MUST carry a source-class tag. The tags are:

| Tag              | Meaning                                                              |
|------------------|----------------------------------------------------------------------|
| `[operator]`     | Entered by a human operator in a report or system (PMS, GL, etc.)    |
| `[derived]`      | Computed from other cells; formula or workflow step produces it      |
| `[benchmark]`    | Sourced from a reference file in `reference/normalized/` or `derived/` |
| `[overlay]`      | Comes from an org/market/loan overlay at runtime                     |
| `[placeholder]`  | Illustrative; should be replaced before final submission             |

The tag appears in-line immediately after the figure: `$1.25M [operator]`,
`1.23 [derived]`, `72% [benchmark]`. In tables, the tag occupies its
own column labeled **Source** or is appended to the cell value.

If a figure has mixed provenance (e.g. a derived ratio whose inputs
are one operator value and one benchmark), use the most permissive
upstream class — `[derived]` — and document the upstream classes in a
footnote.

A cell labeled `[placeholder]` BLOCKS final submission. Workflows MUST
refuse to produce a final output if any non-optional cell is
`[placeholder]`. Draft outputs may carry `[placeholder]` tags as a
signal for what still needs real data.

## Rule 3. Refusal evidence trail

When a final-marked workflow refuses (per `fallback_behavior: refuse`
in the reference_manifest), the output is not silent. It is a refusal
artifact with the shape:

```
## Verdict: REFUSED

- Recommendation: refuse (missing required input)
- Rationale:
  1. {file or input path} is required but absent
  2. Workflow `{slug}` is declared `final_marked` — cannot proceed with fallback
  3. Audience `{audience}` requires {minimum_close_status or seal requirement}
- Confidence: refused
- Materiality: {n/a — no output produced}
- Next action: populate missing input ({file}) and re-run; owner {overlay owner}
```

The refusal artifact replaces the output, is logged, and is eligible
for audit. Period-seal violations (per `required_period_seal`) produce
a refusal artifact of this exact shape.

## Enforcement

- `tests/test_executive_output_contract.py` asserts every final-marked
  workflow's `SKILL.md` references this contract document and that at
  least one worked example demonstrates the verdict-first + source-class
  pattern.
- Reviewers should reject any new final-marked workflow that does not
  conform to this rubric in its example output.
