# System Coverage Matrix

Rows are canonical objects from `_core/ontology.md`. Columns are source systems from `source_registry.yaml`. Cells carry one of:

- `primary`: the primary source of record for this object on assets the source covers
- `secondary`: provides partial or shadow data for the object, used for reconciliation
- `manual_fallback`: provides the object only through manual or spreadsheet-based entry
- `not_supported`: the source does not carry this object

A property is said to have `primary` coverage for an object only when one of the `wave_0` / `wave_1` sources is stubbed or active. Manual fallback stands in for coverage during the interim.

Abbreviations (source_id): `east_pms` = `east_region_pms`, `west_pms` = `west_region_pms`, `gl` = `corporate_gl`, `crm` = `marketing_crm`, `ap` = `accounts_payable_primary`, `mkt` = `market_rent_comps_primary`, `ctr` = `construction_tracker_primary`, `hr` = `hr_payroll_primary`, `sd_bud` = `budget_shared_drive_dropbox`, `op_sftp` = `operator_owner_portal_sftp`, `util` = `utility_expense_intake`, `coi` = `insurance_coi_intake`, `reg` = `regulatory_program_intake`.

## Properties, physical assets, units

| canonical object | east_pms | west_pms | gl | crm | ap | mkt | ctr | hr | sd_bud | op_sftp | util | coi | reg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| property | primary | primary | secondary | not_supported | not_supported | not_supported | secondary | not_supported | not_supported | secondary | not_supported | not_supported | secondary |
| building | primary | manual_fallback | not_supported | not_supported | not_supported | not_supported | secondary | not_supported | not_supported | manual_fallback | not_supported | not_supported | not_supported |
| unit | primary | primary | not_supported | not_supported | not_supported | not_supported | secondary | not_supported | not_supported | secondary | not_supported | not_supported | not_supported |
| unit_type | primary | manual_fallback | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | manual_fallback | not_supported | not_supported | not_supported |

## Leases, events, resident records, ledger

| canonical object | east_pms | west_pms | gl | crm | ap | mkt | ctr | hr | sd_bud | op_sftp | util | coi | reg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lease | primary | primary | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | secondary | not_supported | not_supported | secondary |
| lease_event | primary | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported |
| resident_account | primary | secondary | not_supported | secondary | not_supported | not_supported | not_supported | not_supported | not_supported | secondary | not_supported | not_supported | secondary |
| charge | primary | primary | secondary | not_supported | secondary | not_supported | not_supported | not_supported | not_supported | secondary | manual_fallback | not_supported | not_supported |
| payment | primary | primary | secondary | not_supported | secondary | not_supported | not_supported | not_supported | not_supported | secondary | not_supported | not_supported | not_supported |
| delinquency_case | primary | manual_fallback | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | manual_fallback | not_supported | not_supported | not_supported |

## Leasing funnel

| canonical object | east_pms | west_pms | gl | crm | ap | mkt | ctr | hr | sd_bud | op_sftp | util | coi | reg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lead | secondary | not_supported | not_supported | primary | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported |
| tour | secondary | not_supported | not_supported | primary | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported |
| application | secondary | not_supported | not_supported | primary | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported |
| approval_outcome | primary | manual_fallback | not_supported | secondary | not_supported | not_supported | not_supported | not_supported | not_supported | manual_fallback | not_supported | not_supported | not_supported |
| renewal_offer | primary | manual_fallback | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | manual_fallback | not_supported | not_supported | not_supported |

## Maintenance and turns

| canonical object | east_pms | west_pms | gl | crm | ap | mkt | ctr | hr | sd_bud | op_sftp | util | coi | reg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| work_order | primary | primary | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | secondary | not_supported | not_supported | not_supported |
| preventive_maintenance_task | manual_fallback | manual_fallback | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported |
| turn_project | primary | primary | not_supported | not_supported | secondary | not_supported | not_supported | not_supported | not_supported | secondary | not_supported | not_supported | not_supported |

## Vendors and agreements

| canonical object | east_pms | west_pms | gl | crm | ap | mkt | ctr | hr | sd_bud | op_sftp | util | coi | reg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| vendor | not_supported | not_supported | secondary | not_supported | primary | not_supported | primary | not_supported | not_supported | not_supported | not_supported | secondary | not_supported |
| vendor_agreement | not_supported | not_supported | not_supported | not_supported | primary | not_supported | primary | not_supported | not_supported | not_supported | not_supported | secondary | not_supported |

`accounts_payable_primary` and `construction_tracker_primary` both carry `vendor` and `vendor_agreement` as `primary`. Dedup is resolved by `master_data/vendor_master_crosswalk.yaml`; survivorship is defined in `master_data/survivorship_rules.md`.

## Staffing, payroll

| canonical object | east_pms | west_pms | gl | crm | ap | mkt | ctr | hr | sd_bud | op_sftp | util | coi | reg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| staffing_plan | not_supported | not_supported | secondary | not_supported | not_supported | not_supported | not_supported | primary | not_supported | not_supported | not_supported | not_supported | not_supported |

## Budget, forecast, variance, capex

| canonical object | east_pms | west_pms | gl | crm | ap | mkt | ctr | hr | sd_bud | op_sftp | util | coi | reg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| budget_line | not_supported | not_supported | primary | not_supported | not_supported | not_supported | not_supported | not_supported | manual_fallback | secondary | not_supported | not_supported | not_supported |
| forecast_line | not_supported | not_supported | primary | not_supported | not_supported | not_supported | not_supported | not_supported | manual_fallback | not_supported | not_supported | not_supported | not_supported |
| variance_explanation | not_supported | not_supported | primary | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | secondary | not_supported | not_supported | not_supported |
| capex_project | not_supported | not_supported | primary | not_supported | not_supported | not_supported | primary | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported |
| estimate_line_item | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | primary | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported |
| bid_package | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | primary | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported |
| change_order | not_supported | not_supported | primary | not_supported | not_supported | not_supported | primary | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported |
| draw_request | not_supported | not_supported | primary | not_supported | not_supported | not_supported | primary | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported |
| schedule_milestone | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | primary | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported |

`corporate_gl` and `construction_tracker_primary` both carry `capex_project`, `change_order`, and `draw_request` as primary. Identity resolution is resolved by `master_data/capex_project_crosswalk.yaml`, `master_data/change_order_crosswalk.yaml`, and `master_data/draw_request_crosswalk.yaml`. Survivorship is defined in `master_data/survivorship_rules.md`.

## Market data

| canonical object | east_pms | west_pms | gl | crm | ap | mkt | ctr | hr | sd_bud | op_sftp | util | coi | reg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| market_comp | not_supported | not_supported | not_supported | not_supported | not_supported | primary | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported |

## Approvals and escalations

| canonical object | east_pms | west_pms | gl | crm | ap | mkt | ctr | hr | sd_bud | op_sftp | util | coi | reg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| approval_request | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported |
| escalation_event | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported | not_supported |

Approval and escalation records are internal to the subsystem. They are generated by skills and overlays, not ingested from external sources; every row in the coverage matrix for these objects is `not_supported` by design.

## Interpretation

- No canonical object is covered by a single source in the entire matrix. Every primary source has at least one peer (secondary or manual fallback) from which cross-checks can be drawn. That is required for the reconciliation checks in `../qa/` to function.
- Regulatory program intake (`regulatory_program_intake`) is deliberately siloed: it carries `restricted` sensitivity on all three axes and is limited to `secondary` coverage of `property`, `lease`, and `resident_account`. It is only enabled under the regulatory overlay.
