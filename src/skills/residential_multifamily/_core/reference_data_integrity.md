# Reference Data Integrity

This document defines what "finance-clean" means for reference data
read by final-marked workflows, and how the placeholder scanner
enforces it.

## Problem

Final-marked workflows (executive committee, LP, lender, board, IC)
produce decision-grade deliverables. If a reference file that feeds one
of these workflows contains a row with `TBD` or `PLACEHOLDER` in a
numeric field — and nothing in the row labels it as a placeholder —
the workflow will either refuse (the fallback_behavior: refuse path)
or silently emit a nonsense number dressed as operating fact.

The scanner closes this hole by requiring every placeholder row to be
**explicit**.

## Rule

For any reference file **read by a final-marked workflow**, if a row
contains any of the tokens below in any column:

```
TBD, TODO, FIXME, XXX, PLACEHOLDER, TKTK, TKTKTK
```

…then the same row MUST also have at least one of:

- `status` column set to `placeholder`, `tbd`, `todo`, or `deferred`
- `confidence` column set to `placeholder` or `low_placeholder`
- `source_type` column set to `placeholder`
- `placeholder` column set to `true`
- A column named `placeholder_row` set to `true`

In other words: placeholder data is allowed only when explicitly
labeled as such. Operators reading the artifact at runtime can then
refuse to consume placeholder rows.

## Enforcement

- `tests/test_finance_placeholder_scanner.py` runs the scanner on
  every reference path declared in the reference_manifest.yaml of
  every final-marked workflow.
- Scanner is deterministic, no network, no external deps beyond
  stdlib `csv` + `yaml`.

## Adding new reference data

1. Populate real values, OR
2. If the row is intentionally a placeholder, set one of the opt-out
   markers above, AND
3. Leave a row-level note explaining what must be populated and by
   when.

## Intentional exemptions

Files that are entirely placeholder bodies (e.g. a file with one row
that says `status: placeholder`) are fine — the scanner accepts them
because the row is labeled.

Files that do NOT participate in any final-marked workflow's manifest
are not scanned. That is not a loophole: non-final-marked workflows
are operating/tactical and their output is not presented as audited
fact.
