# owner_report template

status: template

## Expected document shape

```
# Owner Report - <property_id> - <report_period>

## executive_summary
<body markdown>

## financial_summary
<body markdown>

## operations_summary
<body markdown>

## leasing_summary
<body markdown>

## capex_summary
<body markdown>

## risk_outlook
<body markdown>
```

## Rules

- Top-level heading carries `property_id` and `report_period` in the form `YYYY-MM`.
- Each section heading uses one of the canonical `section_key` values: `executive_summary`, `financial_summary`, `operations_summary`, `leasing_summary`, `capex_summary`, `risk_outlook`.
- Narrative bodies are free-form markdown. Avoid PII.
- Optional approval status is declared in a frontmatter block at the top of the document:

```
---
approval_status: approved
---
```

## Parsing

The landing helper parses the document into one record per section, using the section heading as `section_key` and the body between section headings as `body_markdown`. Provenance is stamped on each parsed section from the filename and file mtime.

## Schema pointer

See `reference/connectors/manual_uploads/schema.yaml` under `entities.owner_report` for the full entity contract.

## Illustrative sample

```
# Owner Report - sample_property_one - 2026-03

---
approval_status: approved
---

## executive_summary
Sample narrative for illustrative purposes. Template only; replace with real content before landing.

## financial_summary
Sample narrative.

## operations_summary
Sample narrative.

## leasing_summary
Sample narrative.

## capex_summary
Sample narrative.

## risk_outlook
Sample narrative.
```
