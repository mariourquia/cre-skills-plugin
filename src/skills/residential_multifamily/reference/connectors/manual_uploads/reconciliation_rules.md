# Reconciliation Rules: manual_uploads

Narrative description of how manual_uploads land, validate, and reconcile against adjacent feeds. Codified checks live in `reconciliation_checks.yaml`; this document is the operator-facing companion.

## File acceptance

Every landing starts with a file-format check:

- File extension matches the `expected_file_format` for the template in `schema.yaml.templates.<template>`.
- Header row matches the `expected_header_pattern` for the template.
- File size is within the `dq_rules.yaml.mu_size_*` bounds.

Failure routes the file to `reference/raw/manual_uploads/_rejected/<YYYY>/<MM>/` with an operator-readable log entry naming the template, the expected pattern, and the observed deviation.

## Template version recognition

Every landed file must declare a template_slug that matches a known template in `schema.yaml.templates`. The slug is inferred from the drop-zone subdirectory, not from the filename. Operators who drop a file in the wrong folder see an immediate rejection with guidance pointing to the correct folder.

## Primary-key uniqueness

Each template has a primary key declared in `schema.yaml.entities.<template>.primary_key`. At landing, duplicates are resolved by `mapping.yaml.<template>.dedup_rule.tie_breaker` (usually `latest_extracted_at_wins`). Duplicates within a single file are rejected outright; duplicates across landings are resolved by the tie-breaker.

## Provenance preservation

Every normalized record must carry the full provenance tuple (`source_name`, `source_type`, `source_date`, `extracted_at`, `extractor_version`, `source_row_id`). Markdown and YAML templates that do not carry provenance per row must have provenance synthesized at landing time (the landing helper stamps the file's provenance onto every row derived from it).

## Approval status semantics

Templates with approval lifecycle (owner_report, monthly_review_pack, capex_request_upload, draw_package_upload) carry `approval_status` that gates downstream consumption:

- `draft` - not yet ready for review.
- `in_review`, `submitted`, `under_review` - circulating for review.
- `approved` - promotable to workflow consumption.
- `rejected`, `deferred` - archived; does not flow downstream.

Rows without approval_status land successfully but a warning is emitted; downstream workflows that require approval (investor update generation, draw disbursement) filter out unapproved rows.

## Crosswalk validation

- property_id crosswalks to property master (or is permitted when the landing file IS property_list).
- vendor_id (vendor_bid_tab) crosswalks to ap.vendor.
- employee_id (pm_scorecard_upload) crosswalks to hr_payroll.employee.
- resident_account_id (delinquency_report_upload) crosswalks to pms.lease.
- work_order_id (work_order_backlog_upload) crosswalks to pms.work_order.
- account_code (budget_file, forecast_file) crosswalks to gl.chart_of_accounts.
- project_id (draw_package_upload) crosswalks to the construction project master.

Dangling foreign keys block promotion.

## Sensitive content handling

Manual-upload templates are the highest-PII-risk surface in the connector family (resident data in delinquency_report, employee data in pm_scorecard). The rules:

- No resident or employee names in any template row. Use opaque identifiers (resident_account_id, employee_id).
- Narrative fields (notes, commentary, body_markdown) are scanned for common PII patterns at landing. Matches emit a warning and recommend a template refresh.
- delinquency_report_upload and pm_scorecard_upload are flagged as sensitive templates in `reconciliation_checks.yaml.mu_sensitive_fields_masked_if_flagged`; operators must confirm that sensitive content has been masked or dropped before promotion.

## Promotion gate

Landing promotes from `reference/raw/manual_uploads/` to `reference/normalized/` only when all blocker reconciliation checks pass. Warning-level failures log and allow promotion. Info-level failures report and do not gate.

## Rollout sequence

Manual uploads are wave 2 but are designed to be the fallback every other connector can lean on. In practice, early operators land `property_list`, `budget_file`, `staffing_model_upload`, and `approval_matrix_upload` before any system integration exists; the connector is the bootstrap mechanism for the property master, the COA, the StaffingPlan, and the approval gating logic.
