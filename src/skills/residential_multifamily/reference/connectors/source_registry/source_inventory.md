# Source Inventory

Readable view of the starter registry in `source_registry.yaml`. Entries are grouped by `source_domain`. Every entry below is tagged `status: sample` and carries a lifecycle status of `stubbed` or `planned`. No live production source is declared from this repo.

See `source_registry.schema.yaml` for field definitions and `README.md` for lifecycle rules.

## PMS

| source_id | vendor_family | mode | cadence | objects | status | wave |
|---|---|---|---|---|---|---|
| `east_region_pms` | yardi_family | api | hourly | property, building, unit, unit_type, lease, lease_event, charge, payment, delinquency_case, lead, tour, application, renewal_offer, work_order, turn_project | stubbed | wave_0 |
| `west_region_pms` | realpage_family | sftp | daily | property, unit, lease, charge, payment, work_order, turn_project | stubbed | wave_0 |

Modeled in `../pms/`. CRM-like entities (lead, tour, application) emitted by `east_region_pms` overlap with the `marketing_crm` source; the crosswalk resolves identity.

## GL

| source_id | vendor_family | mode | cadence | objects | status | wave |
|---|---|---|---|---|---|---|
| `corporate_gl` | generic_erp | scheduled_export | daily | budget_line, forecast_line, variance_explanation, capex_project, change_order, draw_request | stubbed | wave_0 |

Modeled in `../gl/`. Capex project records here overlap with `construction_tracker_primary`; resolved via `master_data/capex_project_crosswalk.yaml`.

## CRM

| source_id | vendor_family | mode | cadence | objects | status | wave |
|---|---|---|---|---|---|---|
| `marketing_crm` | entrata_family | api | hourly | lead, tour, application | stubbed | wave_0 |

Modeled in `../crm/`. Resident identity dedup against PMS sources uses `master_data/resident_account_crosswalk.yaml`.

## AP

| source_id | vendor_family | mode | cadence | objects | status | wave |
|---|---|---|---|---|---|---|
| `accounts_payable_primary` | appfolio_family | api | daily | vendor, vendor_agreement, charge, payment | stubbed | wave_0 |

Modeled in `../ap/`. Vendor dedup against `construction_tracker_primary` uses `master_data/vendor_master_crosswalk.yaml`.

## Market data

| source_id | vendor_family | mode | cadence | objects | status | wave |
|---|---|---|---|---|---|---|
| `market_rent_comps_primary` | costar_family | api | weekly | market_comp | stubbed | wave_1 |

Modeled in `../market_data/`.

## Construction

| source_id | vendor_family | mode | cadence | objects | status | wave |
|---|---|---|---|---|---|---|
| `construction_tracker_primary` | procore_family | api | daily | capex_project, estimate_line_item, bid_package, change_order, draw_request, schedule_milestone, vendor, vendor_agreement | stubbed | wave_1 |

Modeled in `../construction/`.

## HR and payroll

| source_id | vendor_family | mode | cadence | objects | status | wave |
|---|---|---|---|---|---|---|
| `hr_payroll_primary` | generic_hr_payroll | scheduled_export | weekly | staffing_plan | stubbed | wave_1 |

No dedicated connector directory yet. Payroll aggregates flow into the GL via `master_data/account_crosswalk.yaml`. A dedicated `hr_payroll` connector is a candidate for wave_2.

## Manual upload and planned

| source_id | vendor_family | mode | cadence | objects | status | wave |
|---|---|---|---|---|---|---|
| `budget_shared_drive_dropbox` | spreadsheet_workflow | shared_drive | quarterly | budget_line, forecast_line | stubbed | wave_1 |
| `operator_owner_portal_sftp` | operator_owner_portal | sftp | monthly | property, unit, lease, charge, payment, work_order, budget_line, variance_explanation | planned | wave_2 |
| `utility_expense_intake` | utility_billing_intake | email_drop | monthly | charge | planned | wave_2 |
| `insurance_coi_intake` | compliance_intake | email_drop | on_demand | vendor, vendor_agreement | planned | wave_2 |
| `regulatory_program_intake` | compliance_intake | shared_drive | quarterly | lease, resident_account | planned | wave_deferred |

Manual-upload and planned sources do not have a dedicated connector directory; they land through the generic ingestion path in `../INGESTION.md` and are crosswalked into the appropriate canonical objects via the master data layer.

## Rollout wave summary

| wave | domains covered | purpose |
|---|---|---|
| `wave_0` | pms, gl, crm, ap | Core operational stack. Required for delinquency, rent-roll, budget-vs-actual, and leasing funnel skills. |
| `wave_1` | market_data, construction, hr_payroll, shared-drive budget | Capex, market comparability, staffing. Required for variance narratives, budget defense, and construction workflows. |
| `wave_2` | operator portals, utilities, insurance COI | Extended coverage for third-party managed assets and compliance intake. |
| `wave_deferred` | regulatory program intake | Isolated behind the regulatory overlay; disabled by default in core. |

## Canonical objects currently covered or gapped

Cross-reference the ontology in `_core/ontology.md`. See `system_coverage_matrix.md` for the full grid.

Covered across at least one stubbed source: property, building, unit, unit_type, lease, lease_event, charge, payment, delinquency_case, lead, tour, application, renewal_offer, work_order, turn_project, budget_line, forecast_line, variance_explanation, capex_project, change_order, draw_request, schedule_milestone, vendor, vendor_agreement, market_comp, staffing_plan.

Gapped in the starter registry: resident_account (feeds implicitly through lease and charge sources; a dedicated stream is not modeled), approval_request, escalation_event (internal objects, not expected from external sources), estimate_line_item (only from `construction_tracker_primary`), bid_package (same), preventive_maintenance_task (not in any listed source yet).
