# Manual Uploads Connector (stub, vendor-neutral)

First-class intake for operators that do not have full API access to a PMS, GL, or AP system, and for artifacts that do not exist as system feeds at all (bid tabs, rent surveys, draw packages, approval matrices, monthly review packs). Every supported template has a schema, a mapping template, sample data, reconciliation checks, DQ rules, and a placeholder file in `file_templates/`.

## Status

`status: stub`. Schema, mapping, sample, reconciliation checks, DQ rules, placeholder templates, and tests only. No vendor adapter code lives here; manual uploads are operator-driven by design.

## Rollout wave

Wave 2. Ships together with `hr_payroll`. This connector is deliberately a first-class citizen, not an afterthought. Many operators will land several manual-upload templates before they land any system-integrated feed.

## Scope

Supported templates (fifteen):

| Template | Format | Purpose |
|---|---|---|
| `budget_file` | csv | Annual budget per property per account code. |
| `forecast_file` | csv | Period-level forecast per property per account code. |
| `owner_report` | markdown | Monthly or quarterly owner-facing narrative. |
| `vendor_bid_tab` | csv, xlsx | Bid tab for RFPs. |
| `rent_survey` | csv, xlsx | Rent comps captured manually. |
| `market_comp_sheet` | csv, xlsx | Comparable sales sheet. |
| `approval_matrix_upload` | yaml | Approval thresholds per role. |
| `property_list` | csv, xlsx | Portfolio property list. |
| `staffing_model_upload` | csv, xlsx | Staffing model rows per property. |
| `capex_request_upload` | yaml | Capex request submissions. |
| `draw_package_upload` | markdown, pdf | Construction draw requests. |
| `monthly_review_pack` | markdown | Monthly review pack sections. |
| `delinquency_report_upload` | csv, xlsx | Monthly delinquency report when no PMS feed exists. |
| `work_order_backlog_upload` | csv, xlsx | Monthly WO backlog when no PMS feed exists. |
| `pm_scorecard_upload` | csv | Quarterly PM scorecard. |

## Not in scope

- No vendor credentials or API tokens. This connector is file-drop only.
- No PII augmentation. Every template uses opaque identifiers for residents and employees.
- No auto-creation of master data records. The connector rejects unknown crosswalk values and routes the operator to add them to the appropriate master file first.

## Folder layout

Manual uploads land under:

```
reference/raw/manual_uploads/<template_slug>/<YYYY>/<MM>/<source>__<as_of>.<ext>
```

See `intake_folder_structure.md` for the full convention.

## Templates directory

Placeholder templates live under `file_templates/`. Each template carries a `status: template` tag and a pointer to the canonical schema. Operators use these as the starting point; they do not represent real data.

## Integration with other connectors

- `property_list` bootstraps the property master; every other connector depends on it.
- `budget_file` + `forecast_file` feed `gl.budget` and `gl.forecast` when no GL feed exists.
- `staffing_model_upload` bootstraps `hr_payroll.staffing_position`.
- `approval_matrix_upload` provides the approval routing table consumed by `ap`, `construction`, and `vendor_invoice_validator`.
- `vendor_bid_tab` feeds `construction_procurement_contracts_engine` and cross-references `ap.vendor`.
- `delinquency_report_upload` is the fallback for `pms.delinquency_case`; `work_order_backlog_upload` is the fallback for `pms.work_order`.
- `pm_scorecard_upload` cross-references `hr_payroll.employee`.

## Connector kind classification note

The `connector_kind` field in `manifest.yaml` is constrained by the subsystem schema enum `[pms, gl, crm, ap, market_data, construction]`. Manual uploads span all five domains. The dominant template family is financial (budget, forecast, owner report, monthly review pack, property list, staffing model), so this connector picks `gl` as the closest semantic match. Flag for human review: if a future schema revision adds a `manual_uploads` or `intake` kind, update `manifest.yaml` and the INGESTION source_type table.

See `INGESTION.md` for the landing convention, `connector_overview.md` for operator onboarding, `intake_folder_structure.md` for the drop-zone layout, `identity_resolution.md` for crosswalks, `reconciliation_checks.yaml` for the QA invariants, and `dq_rules.yaml` for the DQ rules.
