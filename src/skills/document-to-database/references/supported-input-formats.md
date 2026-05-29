# Supported Input Formats

The document-to-database family ingests tokenized/extracted content, not raw binary files. It sits one step downstream of extraction: an upstream reader (the data-room extractor, an OCR pass, a PDF-table parser, an LLM extraction, or a Prose Frontier narrative artifact) turns a source document into structured tokens, and this family turns those tokens into validated, typed, provenance-stamped records. Every accepted shape arrives as a JSON payload through `--json` (or stdin), with selectors (`doc_type`, `run_id`, `as_of`, `tenant_id`, `profile`) inside the payload.

## The accepted shapes

### Prose Frontier narrative artifacts
Narrative deal artifacts (memos, governed narrative blocks) whose quantitative content has been extracted into structured tokens. The family ingests the structured tokens, not the prose. Each figure carries its `data-room/<doc>#<anchor>` source so the narrative claim and the database value share one citation.

### LLM-extracted JSON
The output of an LLM extraction step: rows of unit/charge objects or lines of account/period objects. The family classifies the shape (`doc_type: auto` if not declared), types every value deterministically, and — critically — flags rather than trusts any field the LLM produced at low confidence, because the upstream model's confidence is not the family's confidence floor.

### OCR output
Text recovered from scanned documents. OCR introduces character-level noise (misread digits, split cells), so OCR-sourced payloads lean on the validator's impossible-vs-implausible split: an OCR-mangled negative SF or out-of-range occupancy fails closed as impossible, while a borderline value is flagged for review rather than silently accepted.

### PDF-table extraction
Tables lifted from a PDF rent roll or operating statement. The family expects the table to arrive as rows/lines with column keys; when the column shape is unknown, a schema-inference pass recovers per-column type, nullability, a detected unit (currency, period, date), and a grain guess before normalization.

### Markdown tables
A rent roll or operating statement rendered as a markdown table and parsed into rows/lines. Treated identically to any other tabular token stream once parsed.

### CSV-like token streams
Delimited rows parsed into objects. Currency strings (`$1,234`, `(1,234)` for negatives) are coerced during typing; periods (`YYYY-MM`) and dates (`YYYY-MM-DD`) are distinguished by shape.

### Excel-like exports as JSON or CSV
A spreadsheet export reduced to JSON rows or CSV. The `source.table_id` and per-row numbers are preserved so a value can be traced back to a sheet and cell.

### Mixed qualitative + quantitative chunks
A document that interleaves narrative and numbers. The qualitative chunks are not forced into the schema; the quantitative chunks are extracted, typed, and mapped, and anything the family cannot classify cleanly is routed to human review rather than coerced.

## How provenance is preserved from each format

Regardless of the source shape, every emitted record carries the same provenance bundle (the superset of the 8-column warehouse contract) so the downstream warehouse and the data-room chain join cleanly:

- The **`source_ref`** is always `data-room/<doc>#<anchor>`, minted from the source document id and an in-document anchor.
- The **granular locator** (`source_page`, `source_section`, `source_table_id`, `source_row_number`, `source_column_name`, `source_cell_address`) is carried whenever the upstream extractor supplied it — a PDF table contributes a table id and row number; an Excel export contributes a cell address; an OCR pass contributes a page and section.
- The **`extraction_method`** records how the value arrived (e.g. extracted), and the **`confidence`** band reflects the mapping confidence, not a blanket trust of the source.
- For a PII-classified field the **locator is kept but the value is dropped** (`redaction_status: redacted`), no matter which format it came from — the locator-not-value rule is format-independent. See `security-governance.md`.

## The auto-classification path

When `doc_type` is `auto` (or omitted), classification is by shape, deterministically: a payload carrying unit rows with charge lines routes to the rent-roll reader; a payload carrying account lines with period amounts routes to the operating-statement reader. An unknown tabular stream can be passed to schema inference first to recover its columns and grain, then re-submitted with a known `doc_type`. The same tokens always classify the same way. See the SKILL.md Process and `canonical-schema.md` for what each path produces.
