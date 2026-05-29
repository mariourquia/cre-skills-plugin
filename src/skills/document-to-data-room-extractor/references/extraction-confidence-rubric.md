# Extraction Confidence Rubric

How `document-to-data-room-extractor` assigns the `confidence` score in [0, 1]
to every fact (Step 5). Confidence is not a guess about whether the document is
right; it is a measure of how reliably the value was lifted from the source.
A precise figure from a labeled spreadsheet cell is high-confidence even if the
underlying business assumption is questionable. A figure inferred from prose, or
read off a skewed scan, is low-confidence even if it turns out to be correct.

All threshold and weight numbers below are ILLUSTRATIVE defaults, tuned for
demo behavior. They are not industry benchmarks. Override via `confidence_floor`
in the input schema.

## Four drivers

Confidence is the product of four sub-scores, each in [0, 1]:

```
confidence = method_score * legibility_score * specificity_score * corroboration_score
```

Multiplicative (not additive) so that any single weak dimension caps the score.
A perfectly legible, perfectly specific number that only one document asserts
(`corroboration_score = 0.80`) cannot exceed 0.80. That is intentional: lack of
corroboration on a deal-driving number is itself a risk.

### 1. method_score -- how the value was obtained

| extractionMethod | method_score | Rationale |
|---|---|---|
| spreadsheet_cell | 1.00 | A labeled cell in a structured workbook. The value is the value. |
| labeled_table | 0.95 | A clearly labeled row/column in a PDF table. |
| agency_quote | 0.95 | Quoted terms are explicit in the quote letter (still indicative, not committed). |
| computed_aggregate | 0.90 | Aggregated from clean detail (e.g., column sum). Loses a little for transcription/grouping risk. |
| broker_stated | 0.85 | Explicit in OM prose ("Year 1 NOI $4,210,000"). High legibility, but unverified by source documents. |
| prose_inferred | 0.55 | Derived from narrative that did not state the number outright (e.g., backing GPR out of "averaging $920/unit across 219 units"). |
| ocr_low | 0.40 | Read off a low-quality scan/photo where digits may be transposed. |

### 2. legibility_score -- quality of the source rendering

| Source quality | legibility_score |
|---|---|
| Native digital text / spreadsheet | 1.00 |
| Clean PDF, selectable text | 0.95 |
| Good-quality scan, OCR clean | 0.85 |
| Skewed / faxed / photographed, OCR uncertain | 0.55 |
| Handwritten margin notes | 0.40 |

### 3. specificity_score -- how directly the document states the fact

| Specificity | specificity_score |
|---|---|
| Exact value explicitly stated ("$4,210,000") | 1.00 |
| Value stated to rounded precision ("approx. $4.2M") | 0.85 |
| Value computed from an explicit, document-provided breakdown | 0.90 |
| Value computed from a total the document did NOT itself provide | 0.75 |
| Value is a range; midpoint taken | 0.65 |

### 4. corroboration_score -- cross-document agreement

| Corroboration | corroboration_score |
|---|---|
| Two or more documents agree within tolerance | 1.00 |
| Single source, but the canonical source for that fact (e.g., T-12 for expenses) | 0.90 |
| Single source, non-canonical (e.g., OM for NOI with no T-12 to check) | 0.80 |
| Two documents DISAGREE beyond tolerance | 0.40 + force `conflict: true`, `reviewState: needs_review` |

## Worked scoring examples (ILLUSTRATIVE)

All figures fictional; for demonstration of the rubric only.

**Example A -- T-12 GPR from a clean workbook cell**
- method: spreadsheet_cell (1.00) x legibility: native (1.00) x specificity: exact (1.00) x corroboration: canonical single source (0.90)
- confidence = 1.00 x 1.00 x 1.00 x 0.90 = **0.90** -> `auto_pass`

**Example B -- OM-stated NOI, no T-12 yet provided**
- method: broker_stated (0.85) x legibility: clean PDF (0.95) x specificity: exact (1.00) x corroboration: non-canonical single source (0.80)
- confidence = 0.85 x 0.95 x 1.00 x 0.80 = **0.646** -> below 0.70 floor, `needs_review`, note "single-source OM NOI, no T-12 corroboration"

**Example C -- OM NOI vs. T-12-derived NOI disagree by 6.3%**
- corroboration collapses to 0.40 and `conflict: true`
- method: broker_stated (0.85) x legibility (0.95) x specificity (1.00) x corroboration (0.40) = **0.323** -> `needs_review`, surfaced in Cross-Document Conflicts

**Example D -- expense line off a skewed scanned T-12**
- method: ocr_low (0.40) x legibility: photographed (0.55) x specificity: exact-as-read (1.00) x corroboration: canonical single (0.90)
- confidence = 0.40 x 0.55 x 1.00 x 0.90 = **0.198** -> `needs_review`, note "low-OCR; verify digits against source page"

## Review-state mapping (Step 7)

```
auto_pass     : confidence >= confidence_floor AND conflict == false AND stale == false
needs_review  : confidence < confidence_floor OR conflict == true OR stale == true
                (and ALL facts in review_mode == manual_all)
human_confirmed / human_rejected : set ONLY by downstream write-back, never by the extractor
```

## Notes on staleness

`stale = true` does not change the multiplicative confidence; it independently
forces `needs_review`. A six-month-old T-12 may be perfectly legible and score
0.90 on extraction quality, but it understates current expense inflation, so the
human must confirm it is still representative before it anchors a normalized NOI.
