# Human-Review Workflow

The family never resolves ambiguity silently. Anything it cannot defend with high confidence — or anything that fails to reconcile — accumulates into a human-review queue with a stated reason and a recommended action. This document specifies what gets queued, what a reviewer does with each item, and why the queue exists.

## Principle: flag, never guess; surface, never plug

Two rules govern the queue:

1. A value the calculators cannot map or type at high confidence is flagged for a human, not guessed into place.
2. A reconciliation gap is surfaced as an explicit residual, not absorbed into a balancing plug. A forced tie-out is `forced_tie_out` — a critical failure — and is impossible by construction, because nothing in the pipeline adjusts a number to make it tie.

## What gets routed to review

### Unmapped charges and accounts
A rent-roll charge whose code matches no known code or alias and whose description matches no keyword is `unmapped` (`charge_category` null, `needs_review` true). A T-12 / operating-statement line that matches neither a GL code nor a name keyword lands in the `unmapped` bucket. Both are flagged, never dropped — the dollars stay visible for a controller to classify. Reason: `account_unmapped` / `charge_code_unmapped`.

### Low- and medium-confidence inferences
A mapping made from a free-text description (charges) or a line label (accounts) is medium confidence and routed to review even though a category was found — a description match is a defeasible reading that a human should confirm. A record at or below the confidence floor (`low`) routes to review and, when it gates a decision, raises `confidence_below_floor`. Reason: `charge_code_inferred` / `account_inferred` / `confidence_below_floor`.

### Forced or low-confidence tie-outs
Every untied reconciliation dimension is queued with its classified difference type, its variance, its residual-unexplained, and a confidence band. A `missing` classification (the total does not tie — income present in one source and absent in the other) carries low confidence and is the highest-priority review item. A `timing` classification (e.g. a CAM estimate-vs-true-up drift with the total tied) carries medium confidence. Reason: the difference type (`mapping` / `timing` / `missing`).

### Sign-convention ambiguity
When an operating statement's expense sign convention cannot be read cleanly, the normalizer falls back to the positive-magnitude convention and the line is reviewable; a detected NOI inconsistency (`noi_includes_below_the_line`) is critical and blocks until a reviewer confirms the section classification. Reason: sign-convention / NOI classification.

### Structural validation warnings
Unknown unit/lease statuses, unknown line types, a partial-year T-12 (fewer than twelve periods), and duplicate/subtotal-suspect account lines are all surfaced for a reviewer to confirm before the payload is trusted.

## What a reviewer does with an item

Each queue item carries a `dimension` or `field_path`, a `reason`, the relevant values (variance and residual for tie-outs; the inferred category and method for mappings), a `confidence`, and a recommended `action` (e.g. "Route to analyst: confirm timing difference"). A reviewer takes exactly one of two terminal actions per item:

- **Accept** — confirm the inferred mapping, classification, or normalization. The record's `review_status` moves to `accepted` and it stops gating the grade.
- **Flag** — reject or escalate. The record's `review_status` becomes `flagged`; it remains a quality signal and continues to gate the merge/production gate until resolved.

A reviewer never edits a governed number to make it tie. If a tie-out is wrong, the upstream extraction or mapping is corrected and the ingestion is re-run deterministically — the same inputs reproduce the same result, so a fix is verifiable.

## How the queue gates the grade

The human-review queue is the operational face of the gates in `data-quality-rules.md`. The merge gate (>= 85, no C, no critical) and the production gate (>= 92, all-A, no critical) cannot be cleared while a critical item is unresolved. Medium-confidence inferences lower the relevant graded dimension but do not, by themselves, block merge; an unresolved critical (and always a PII breach) does. The point of the queue is to make the cost of accepting a low-confidence record explicit and to keep a human in the loop on exactly the items where the machine could be wrong.

See `self-iteration-loop.md` for the roles that staff this review and `data-quality-rules.md` for the gate arithmetic.
