# Sage Intacct GL Adapter

Adapter id: `sage_intacct_gl`
Vendor family: `sage_intacct_family`
Connector domain: `gl`
Status: `stub`
Rollout wave: `wave_4`

## Intacct's role in the stack

Sage Intacct is the financial system of record. For residential multifamily
deployments it carries:

- Posted actuals at journal-line granularity (one of the two primary
  inputs for variance analysis, alongside the PMS charge feed for cash-
  basis revenue).
- Approved budget versions, sourced from the Budget Module.
- Published forecast versions, sourced from the Forecast Module.
- Chart of accounts (the `Accounts` object).
- Dimension structure: Entities, Locations, Departments, Projects, Classes.
- Vendor master (the `Vendors` object).
- Capex project ties via the Project dimension.

Intacct is declared primary for: `budget_line`, `forecast_line`,
`actual_line`, and `variance_explanation`. It is a secondary consumer
for `vendor` (AppFolio and Procore also carry vendor records; three-way
reconciliation runs through the `vendor_master_crosswalk`).

## Dimension structure assumed

A typical CRE Intacct deployment uses Entities and Locations to model
the property portfolio. The assumed mapping is documented in the
onboarding runbook under `runbooks/sage_intacct_onboarding.md`:

- **Entity (`ENTITYID`)**: usually the owning legal entity. For a
  single-property SPE the Entity-to-Property mapping is 1:1. For a
  roll-up entity holding two or more properties the Entity resolves
  to several Property ids and a Location dimension disambiguates.
- **Location (`LOCATIONID`)**: usually the operating property site. In
  the single-entity roll-up pattern, Location is the primary carrier
  of property attribution.
- **Department (`DEPARTMENTID`)**: usually an operating function slice
  (leasing, maintenance, administration, marketing). Not typically used
  for property attribution on the CRE side.
- **Project (`PROJECTID`)**: used for capex projects; ties to the
  canonical `CapexProject` object via the `capex_project_crosswalk`.
- **Class (`CLASSID`)**: used for fund or portfolio slicing; LPs and
  owner groups often map to Class.

The `property_master_crosswalk` resolves Entity + Location dimension
tuples to the canonical `property_id`. The `capex_project_crosswalk`
resolves Project dimension ids to the canonical `capex_project_id`.

## Property-to-Entity-to-Dimension mapping

Two deployment patterns are supported:

1. **Entity-per-property (SPE pattern).** Each property has its own
   legal entity and Intacct entity. `ENTITYID` alone resolves to
   `property_id` via `property_master_crosswalk`. `LOCATIONID` may
   be set but is redundant.
2. **Roll-up-entity pattern.** Multiple properties share one legal
   entity and one Intacct entity. `ENTITYID` resolves to multiple
   properties; `LOCATIONID` is the primary disambiguator. Shared costs
   posted at the Entity level without Location must be allocated via
   the allocation basis declared in the property crosswalk.

Both patterns are common in CRE Intacct deployments. The onboarding
runbook captures the pattern selection as the first decision in the
adapter rollout.

## Reporting structure tie-ins

- Intacct reporting periods (`PERIOD`) carry a fiscal-year and fiscal-
  month shape. The `intacct_period_to_iso_month` transform normalizes
  to `YYYY-MM` for the canonical `operating_month` field.
- Intacct's Reporting Period is distinct from a posting's `BATCH_DATE`.
  Late postings re-open a closed period and post with a `BATCH_DATE`
  later than the `PERIOD`. The `posting_date` (canonical) carries
  `BATCH_DATE`; `operating_month` carries `PERIOD`. Variance analysis
  uses `operating_month`; late-posting detection reads both.
- Service period (`SERVICE_FROM`/`SERVICE_TO`) is captured on accrual
  lines and allocates cost across the service window; canonical
  `service_period_range` carries both dates.

## Capex vs opex classification

Capex vs opex in Intacct is driven by a combination of:

- Account category (the `ACCOUNT_TYPE` on the Account object).
- Project dimension tagging (`PROJECTID` set on the posting line).
- Capitalization threshold policy (declared in the org overlay).

The canonical classification uses the `account_crosswalk` to resolve
the Intacct account to a canonical account slug, then checks whether
the slug is in the capex family. If the posting carries a `PROJECTID`
but the account resolves to an opex slug, the `gl_capex_coded_as_opex_exception`
check fires. The reverse (capex account with no `PROJECTID`) fires
`gl_opex_coded_as_capex_exception`.

## Versioning conventions

- **Budget versions** carry a `BUDGETID` and a human-readable
  `BUDGETNAME` in Intacct. The onboarding runbook enforces a naming
  convention (`<scenario>_<fiscal_year>[_<revision>]`) so that
  version-drift checks can parse the label.
- **Forecast versions** carry a `FORECASTID` and `FORECASTNAME`. The
  canonical `forecast_version` label must match the allowed list
  declared in the GL manifest (for example: `reforecast_q1`,
  `reforecast_q2`, `reforecast_q3`, `year_end_estimate`).
- **Multiple forecast vintages** for the same `(property_id, account_id,
  period)` are permitted if they carry distinct `as_of_date` values;
  `gl_forecast_version_conflict_flagged` enforces.

## Provenance envelope

Every raw Intacct record in `sample_raw/` carries the canonical
provenance envelope: `source_name`, `source_type`, `source_date`,
`extracted_at`, `extractor_version`, `source_row_id`. `RECORDNO` is
the Intacct stable id and is captured as `source_row_id`.

## What this adapter does not cover

- Accounts Payable invoice lifecycle (bill entry, approval, payment
  batch). That remains with the `ap` connector and the AppFolio AP
  adapter (wave 4 parallel track).
- Inventory, order entry, or other Intacct modules outside the GL /
  Budget / Forecast / Project / Vendor scope.
- Sub-resident charges (PMS territory).

## Related files

- `manifest.yaml` — adapter manifest conforming to the adapter schema.
- `source_contract.yaml` — per-entity raw Intacct payload shape.
- `normalized_contract.yaml` — canonical-shape normalized output.
- `field_mapping.yaml` — source-to-canonical field-by-field mapping.
- `sample_raw/` — synthetic Intacct payload samples (tagged `status: sample`).
- `sample_normalized/` — canonical-shape mirrors of the same records.
- `dq_rules.yaml` — Intacct-specific DQ rule set.
- `reconciliation_rules.md` + `reconciliation_checks.yaml` — cross-system
  reconciliation logic.
- `edge_cases.md` — enumerated edge cases.
- `source_registry_entry.yaml` — source-registry fragment for
  `sage_intacct_prod`.
- `crosswalk_additions.yaml` — sample crosswalk rows for accounts,
  property-via-entity-and-location, vendors, and capex projects.
- `workflow_activation_additions.yaml` — workflow activation role
  declarations.
- `tests/test_adapter.py` — conformance tests.
- `runbooks/sage_intacct_onboarding.md` — onboarding procedure.
- `runbooks/sage_intacct_common_issues.md` — common issue handling.
