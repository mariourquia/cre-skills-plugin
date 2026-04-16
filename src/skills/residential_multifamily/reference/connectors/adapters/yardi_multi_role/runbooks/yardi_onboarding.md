# Yardi Onboarding Runbook

Per-access-path onboarding with credential model, sandbox setup,
validation steps, and dual-run protocol. Scope: from kickoff meeting
through first validated production extract.

Prerequisite: `classification_worksheet.md` Dimensions 1-3 closed;
Dimension 4 closed before any live sample data flows. See
`yardi_classification_path.md` for the full decision tree.

---

## Access path 1: Voyager API (REST or SOAP)

### Credential model

- OAuth 2.0 client credentials OR API key, per tenant. Never share
  credentials across tenants.
- Scope: read-only for PMS + GL objects declared in role.
- Rotation: per subsystem security policy (typically 90 days).
- Storage: secrets manager only; never in this adapter directory.

### Sandbox setup

1. Request a Yardi sandbox tenant from operator's Yardi account rep.
2. Confirm sandbox carries representative data (at least one property,
   units, leases, charges, payments, work orders).
3. Acquire sandbox credentials via subsystem secrets workflow.
4. Record sandbox endpoints (REST base URL, SOAP WSDL if applicable)
   in `master_data/source_endpoints` (never here).

### Validation

1. Pull a single property record; verify mapping to
   `canonical Property` via field_mapping.yaml works cleanly.
2. Pull lease stream; run `yd_conformance_tcode_decoded` rule.
3. Pull charge stream; confirm property-scoped chargecode decode
   succeeds for every chargecode observed.
4. Pull payment stream; verify payment_status enum maps through
   map_yardi_payment_status.
5. Pull work_order stream; verify priority enum maps through
   map_yardi_priority.
6. Run DQ rule set end-to-end; no blocker failures before advancing
   from sandbox to production.

---

## Access path 2: Data Connect warehouse

### Credential model

- Direct warehouse connection: SQL auth or Azure AD passthrough.
- Read-only role scoped to replicated schemas (`dc.fact_*`,
  `dc.dim_*`).
- Credentials in subsystem secrets manager; never here.

### Sandbox setup

1. Confirm operator has Data Connect provisioned (not every Yardi
   tenant does).
2. Verify warehouse refresh schedule in operator runbook; encode
   `expected_latency_minutes`.
3. Register warehouse endpoint in `master_data/source_endpoints`.

### Validation

1. Query `dc.dim_property`; verify row count matches Voyager API
   property count.
2. Query `dc.fact_charge` for a recent property-period; reconcile
   against Voyager API charge stream via
   `yd_recon_data_connect_vs_voyager_charges`.
3. Query `dc.fact_gl_actual`; verify accrual book availability.
4. Query `dc.dim_unit_effective`; ensure effective-dated unit
   structure is present if operator has renovation history.

---

## Access path 3: SFTP scheduled export

### Credential model

- SFTP user per tenant. Key-based auth preferred; password rotation
  per policy if password-based.
- Read-only access to operator's export bucket.

### Sandbox setup

1. Confirm operator runs a nightly Voyager export job to SFTP.
2. Obtain list of export file naming conventions (often include
   propid or tenant abbreviation).
3. Record export schedule and retention window.

### Validation

1. Pull one night's export; validate file landing cadence matches
   declared `expected_latency_minutes`.
2. Parse and map through field_mapping.yaml for each entity present.
3. Run completeness DQ rules to catch missing entities.
4. Check that historical entities (e.g., closed leases) are flagged
   correctly and do not trigger current-period aggregations.

---

## Access path 4: Manual report exports

### Credential model

- No credentials; operator staff upload files.
- Uploaders authenticated via subsystem's upload portal.

### Sandbox setup

1. Register every report_template_id in
   `master_data/report_export_templates` with its column_map.
2. Confirm upload portal accepts CSV and Excel; reject other formats.
3. Record allowed submitters.

### Validation

1. Upload a sample file per template; verify column_map decodes
   cleanly.
2. Run `yd_conformance_report_columns` to catch template drift.
3. Confirm every record carries an internal `as_of_date` distinct
   from `file_received_at`.
4. Run stale-export rule `yd_freshness_stale_exports` with a
   deliberately old file to verify warn behavior.

---

## Access path 5: RentCafe API

### Credential model

- RentCafe REST API uses operator-scoped OAuth tokens.
- Scope: read-only for prospect / lead / tour / application objects.
- PII posture: Dimension 4 MUST close before any applicant data is
  retained.

### Sandbox setup

1. Confirm RentCafe API is provisioned for the operator's sites.
2. Note: RentCafe scope typically covers prospect / lead / tour /
   application but NOT full resident ledger. See
   `yardi_common_issues.md::rentcafe_voyager_drift`.

### Validation

1. Pull lead stream for one property; verify source_channel and
   pipeline_stage map cleanly.
2. Pull tour stream; verify tour_type and outcome map.
3. Pull application stream; verify screening_result and decided_date
   map.
4. Run `yd_recon_rentcafe_vs_voyager_lead_state` to verify RentCafe
   lead stage consistency with Voyager applicant records.

---

## Dual-run protocol

When Yardi is being migrated to AppFolio (or vice versa):

### Pre-cutover

1. Confirm `cutover_effective_date` per property in
   `yardi_migration_to_appfolio.md`.
2. Enable `yardi_voyager_stub` and `appfolio_prod` extracts in
   parallel.
3. Activate reconciliation check `yd_recon_yardi_vs_appfolio_overlap`.

### During cutover window

1. Daily reconciliation at property-period grain; warn within
   `cutover_overlap_band`, block outside.
2. Downstream workflows mark outputs `dual_run_active = true`.
3. Any discrepancy outside band requires regional_ops_director
   sign-off before blocking the affected workflow.

### Post-cutover

1. Set `effective_end: cutover_effective_date` on
   `property_master_crosswalk` row for the property with
   `yardi_voyager_stub` as source.
2. Enable `yd_consistency_historical_only_mode` for the property.
3. AppFolio becomes sole source; Yardi writes blocked.
4. Retain Yardi read access for comparative reports.

---

## Post-IC property setup (acquisition landing)

When a Dealpath-approved deal closes and the property lands in Yardi
(instead of AppFolio):

1. Trigger per `acquisition_handoff` workflow.
2. Seed `property_master_crosswalk` with Dealpath asset_id and Yardi
   propid.
3. Seed `unit_crosswalk` from Voyager unit roster.
4. Run `yd_recon_dealpath_to_yardi_handoff` to validate lag within
   `handoff_lag_band`.

---

## Charge code seed

Every (propid, chargecode) pair in operator's scope must be seeded in
`master_data/charge_code_crosswalk_by_property` before charges can be
decoded to canonical charge_type. See
`yardi_common_issues.md::chargecode_per_property`.

---

## First-pass validation sign-offs

Before advancing the adapter from `stub` to `starter`:

- [ ] Manifest schema valid
- [ ] At least one property through full PMS entity set
- [ ] DQ rule set runs clean (no blocker failures)
- [ ] Reconciliation checks pass within declared bands
- [ ] classification_worksheet.md Dimensions 1-4 closed
- [ ] Dimension 4 sign-off from compliance_risk
- [ ] data_platform_team sign-off on sandbox completion
