# Implementation Inventory

Status report per `source_domain`. Lists sources currently modeled, sample canonical objects they touch, the normalized outputs they produce, downstream workflows that depend on them, known gaps, blockers, and the documentation or credentials required before a stubbed source can move to `active`.

Cross-reference: `source_registry.yaml`, `source_inventory.md`, `system_coverage_matrix.md`, and the per-domain connectors under `../pms/`, `../gl/`, `../crm/`, `../ap/`, `../market_data/`, `../construction/`.

## pms

**Sources modeled (stubbed).** `east_region_pms`, `west_region_pms`.

**Sample canonical objects covered.** property, building, unit, unit_type, lease, lease_event, charge, payment, delinquency_case, lead (secondary), tour (secondary), application (secondary), renewal_offer, work_order, turn_project.

**Normalized outputs produced.** `reference/normalized/property__*`, `reference/normalized/unit__*`, `reference/normalized/lease__*`, `reference/normalized/lease_event__*`, `reference/normalized/charge__*`, `reference/normalized/payment__*`, `reference/normalized/delinquency_case__*`, `reference/normalized/work_order__*`, `reference/normalized/turn_project__*`. Scope suffix is per-property or per-region depending on source cadence.

**Dependent workflows.** Rent-roll analysis, delinquency playbook, renewal retention, work-order triage, turn scheduling, budget-vs-actual templates that use PMS-side revenue, lease-up war room, monthly property performance dashboard.

**Open gaps.** 
- Unit renumbering after renovation is not auto-handled; requires entries in `master_data/unit_crosswalk.yaml`.
- Lease events that do not cleanly map to the canonical enum (for example, legal notice served captured as free text) are dropped from structured output.
- Resident-account dedup against the CRM source depends on phone / email match and is handled by the resident account crosswalk.

**Blockers before move to active.** Live credentials for each PMS instance, a validated full-cycle reconciliation window (record count, duplicate PK, lease-status reconciliation, unit-count reconciliation) per source, an assigned on-call responder.

**Required future credentials or docs.** Operator-specific API keys or SFTP keys, schema documentation from each vendor instance, a data-processing agreement covering high PII classification.

## gl

**Sources modeled (stubbed).** `corporate_gl`.

**Sample canonical objects covered.** budget_line, forecast_line, variance_explanation, capex_project, change_order, draw_request. Secondary coverage of charge / payment (for GL-side revenue and expense postings) and vendor (for AP-side GL lines).

**Normalized outputs produced.** `reference/normalized/gl_actual__*`, `reference/normalized/gl_budget__*`, `reference/normalized/gl_forecast__*`, `reference/normalized/gl_capex_actual__*`, `reference/normalized/gl_commitment__*`, `reference/normalized/variance_explanation__*`.

**Dependent workflows.** Budget-vs-actual templates, variance narratives, capex prioritizer, draw request workflow, quarterly investor update, fund-level allocations.

**Open gaps.**
- Chart of accounts mapping is required before any GL record becomes useful; `master_data/account_crosswalk.yaml` is mandatory.
- Capex posted at parent-project level requires splitting against `master_data/capex_project_crosswalk.yaml`.
- FP&A-authored budgets may not land here; the shared-drive fallback (`budget_shared_drive_dropbox`) resolves until an FP&A connector ships.

**Blockers before move to active.** Validated account_crosswalk entries for the full chart, a passing budget-vs-actual alignment check (see `../qa/budget_actual_alignment.yaml`), a signed-off capex split.

**Required future credentials or docs.** ERP-specific API credentials, chart of accounts export, budget template spec, delegation of authority matrix for approvals reflected in posting workflow.

## crm

**Sources modeled (stubbed).** `marketing_crm`.

**Sample canonical objects covered.** lead, tour, application.

**Normalized outputs produced.** `reference/normalized/lead__*`, `reference/normalized/tour__*`, `reference/normalized/application__*`.

**Dependent workflows.** Leasing funnel metrics, lead conversion analysis, marketing attribution, lease-up war room, tour-to-lease and application-to-lease funnels.

**Open gaps.**
- Resident account dedup across CRM and PMS is required; `master_data/resident_account_crosswalk.yaml` carries the rules.
- Free-form note fields must be scrubbed for protected-class language per the fair-housing guardrails in the ontology.

**Blockers before move to active.** Live OAuth credentials for the CRM, passing fair-housing content scrub in a validation window, validated lead-to-PMS handoff.

**Required future credentials or docs.** OAuth client registration, fair-housing compliance sign-off, marketing attribution rules.

## ap

**Sources modeled (stubbed).** `accounts_payable_primary`.

**Sample canonical objects covered.** vendor, vendor_agreement, charge, payment.

**Normalized outputs produced.** `reference/normalized/vendor__*`, `reference/normalized/vendor_agreement__*`, `reference/normalized/ap_invoice__*`, `reference/normalized/ap_payment__*`.

**Dependent workflows.** Vendor invoice validator, COI compliance, commitment tracking, AP aging, variance narratives driven by expense detail.

**Open gaps.**
- Vendor master dedup against the construction tracker is required; `master_data/vendor_master_crosswalk.yaml` resolves.
- Concession reversal postings occasionally lag the PMS by one day, creating transient ledger mismatches during reconciliation.
- Insurance expiry tracking depends on the COI intake source when the AP platform does not track it.

**Blockers before move to active.** Live AP credentials, vendor master reconciliation window passed, COI tracking surfaced.

**Required future credentials or docs.** API credentials, vendor onboarding policy reference, COI retention schedule.

## market_data

**Sources modeled (stubbed).** `market_rent_comps_primary`.

**Sample canonical objects covered.** market_comp.

**Normalized outputs produced.** `reference/normalized/market_comp__*`, feeding `reference/derived/rent_benchmark__*`.

**Dependent workflows.** Comp snapshot, market memo generator, submarket truth serum, rent optimization planner.

**Open gaps.**
- Submarket taxonomy mismatch with internal submarket labels must be resolved in the market_data connector's mapping.
- Concession observations from market data are estimates; the subsystem should not treat them as audited lease data.

**Blockers before move to active.** Subscription credentials, submarket mapping validated, rent-benchmark freshness test passing.

**Required future credentials or docs.** Subscription API key, submarket mapping table, data license terms.

## construction

**Sources modeled (stubbed).** `construction_tracker_primary`.

**Sample canonical objects covered.** capex_project, estimate_line_item, bid_package, change_order, draw_request, schedule_milestone, vendor, vendor_agreement.

**Normalized outputs produced.** `reference/normalized/capex_project__*`, `reference/normalized/estimate_line_item__*`, `reference/normalized/bid_package__*`, `reference/normalized/change_order__*`, `reference/normalized/draw_request__*`, `reference/normalized/schedule_milestone__*`, `reference/normalized/construction_vendor__*`.

**Dependent workflows.** Construction project command center, capex prioritizer, draw request workflow, GC bid analysis, change order compliance.

**Open gaps.**
- Capex project identity overlap with the GL must be resolved; `master_data/capex_project_crosswalk.yaml` is mandatory.
- Change order and draw request identity share the same issue; see `master_data/change_order_crosswalk.yaml` and `master_data/draw_request_crosswalk.yaml`.
- Construction vendors overlap with AP vendors; the vendor master crosswalk resolves.

**Blockers before move to active.** Validated capex crosswalk, validated change-order and draw-request crosswalks, vendor master reconciliation.

**Required future credentials or docs.** API credentials, delegation of authority for change order approvals, draw package template.

## hr_payroll

**Sources modeled (stubbed).** `hr_payroll_primary`.

**Sample canonical objects covered.** staffing_plan.

**Normalized outputs produced.** `reference/normalized/staffing_plan__*`. Payroll aggregates flow into the GL via `master_data/account_crosswalk.yaml` until a dedicated connector exists.

**Dependent workflows.** Staffing ratio benchmarking, payroll variance narratives, contractor-vs-employee cost analysis, FTE allocation across properties.

**Open gaps.**
- No dedicated connector directory exists yet; `hr_payroll` lives only in the registry.
- Employee-to-property assignment is not single-valued; `master_data/employee_crosswalk.yaml` carries the list of property assignments and the split weights where used.
- Contractors are comingled with employees in exports; must be flagged in the crosswalk.

**Blockers before move to active.** Dedicated `hr_payroll` connector directory (wave_2 candidate), restricted-PII handling sign-off, payroll-to-GL reconciliation window.

**Required future credentials or docs.** HRIS credentials, contractor classification policy, restricted-PII handling policy, property assignment source of truth.

## manual_upload and planned

**Sources modeled (stubbed or planned).** `budget_shared_drive_dropbox`, `operator_owner_portal_sftp`, `utility_expense_intake`, `insurance_coi_intake`, `regulatory_program_intake`.

**Sample canonical objects covered.** budget_line, forecast_line, property (secondary), unit (secondary), lease (secondary), charge (secondary and manual fallback), payment (secondary), work_order (secondary), variance_explanation (secondary), vendor (secondary via COI), resident_account (secondary via regulatory intake).

**Normalized outputs produced.** Same file naming convention as the other domains. Scope suffix usually includes the source_id to avoid clashes with the primary source for the same object.

**Dependent workflows.** Budget defense, third-party operator reporting, utility expense reconciliation, COI compliance, regulatory program reporting.

**Open gaps.**
- File formats and internal schemas vary significantly per source.
- Property name mismatches across sources are very common; the property master crosswalk is the primary resolver.
- The regulatory intake is isolated behind the regulatory overlay and is not enabled in core.

**Blockers before move to active.** For the stubbed shared-drive budget source, a validated property-name mapping window. For the planned sources, a dedicated per-source adapter, a per-source reconciliation window, and a sign-off on restricted sensitivity where it applies.

**Required future credentials or docs.** Shared-drive access placeholders, operator SFTP keys, utility provider format specs, COI retention policy, regulatory program reporting templates per jurisdiction.

## Aggregate gaps surface

- The hr_payroll domain lacks a connector directory.
- The resident_account canonical object has no dedicated primary source; it is implied from lease, charge, and CRM feeds. Any deployment that needs a clean resident-account master must either designate one of the existing sources as primary in deployment configuration or stand up a dedicated source.
- Approval and escalation records are not sourced externally (by design). Skills that generate them must emit records that carry the subsystem's own `source_id` of `subsystem_internal` at landing.
- Protected-class content scrubbing is called out in multiple sources (crm, pms lead) but the scrub is not yet wired into the landing pipeline.
- Restricted-PII handling for hr_payroll and the regulatory intake requires a separate sign-off workflow not represented in the registry schema.
