# Yardi Classification Worksheet

Purpose: structured operator interview that closes the four dimensions
required before this adapter can trust Yardi output as primary for any
canonical object. Until every required dimension is closed, Yardi output
is treated as historical-only per
`bounded_assumptions.yaml::yardi_role.unknown`.

Answers feed `manifest.yaml`, `source_contract.yaml`,
`provisional_source_contract.yaml`, `crosswalk_additions.yaml`,
`workflow_activation_additions.yaml`, and the source-of-truth matrix
under `../../_core/stack_wave4/source_of_truth_matrix.md`.

See `runbooks/yardi_classification_path.md` for the full decision tree
and `runbooks/yardi_onboarding.md` for access-path selection after this
worksheet closes.

---

## Dimension 1: Role

Declares which canonical domain(s) Yardi acts as system of record for.
At least one role must be selected. Multiple roles are common.

Options (each can be selected independently):

- [ ] `primary_pms`                 — Voyager is the primary PMS (unit, lease, ledger, WO)
- [ ] `primary_gl`                  — Voyager financial is the primary GL
- [ ] `primary_leasing_crm`         — RentCafe + Voyager leasing is the primary leasing funnel
- [ ] `primary_reporting_feed`      — Data Connect warehouse is the primary BI source
- [ ] `secondary_pms`               — Yardi is PMS secondary (e.g., Yardi for some portfolio segments; AppFolio primary)
- [ ] `secondary_gl`                — Yardi is GL secondary (e.g., Intacct primary, Yardi used for a legacy entity)
- [ ] `secondary_leasing_crm`       — RentCafe consumed as supplemental lead-source data only
- [ ] `legacy_historical_only`      — Yardi is read-only archive for pre-cutover comparatives
- [ ] `dual_run_during_cutover`     — Yardi + successor system both live for a bounded migration window
- [ ] `mixed_by_portfolio_segment`  — Yardi is primary for some segments, secondary for others (declare the split below)

Selected: [ ]

Portfolio-segment split (only if `mixed_by_portfolio_segment` selected):
```
# segment_key -> yardi_role
#   market_rate_garden: primary_pms
#   affordable_midrise: secondary_pms
```

Evidence:
```
# paste operator response verbatim; attach links to any role-defining documents
```

Open questions:
```
# e.g., "is GL Yardi or Intacct for entity ENT_A?" / "is RentCafe leasing used at properties not in Voyager?"
```

---

## Dimension 2: Access Path

Declares the extraction mechanism per sub-system. Each sub-system below
must have at least one access path selected once the role dimension
includes that sub-system.

### 2a. Voyager PMS (resident / unit / lease / ledger / WO)

- [ ] `api_voyager_rest`            — Voyager REST API (per-tenant scopes)
- [ ] `api_voyager_soap`            — Voyager SOAP (legacy, still common)
- [ ] `data_connect_warehouse`      — Data Connect replicated warehouse (Snowflake/SQL)
- [ ] `sftp_scheduled_export`       — operator-scheduled nightly SFTP drops
- [ ] `manual_report_export`        — Excel / CSV exports from Voyager UI, delivered via email or shared drive
- [ ] `no_extraction`               — Voyager UI only; adapter surfaces no Voyager data

Selected: [ ]

### 2b. Voyager GL (chart / actuals / budgets / forecasts)

- [ ] `api_voyager_rest`
- [ ] `api_voyager_soap`
- [ ] `data_connect_warehouse`
- [ ] `sftp_scheduled_export`
- [ ] `manual_report_export`
- [ ] `no_extraction`

Selected: [ ]

### 2c. RentCafe (leasing / portal / lead / tour / application)

- [ ] `api_rentcafe_rest`
- [ ] `data_connect_warehouse`      — some RentCafe data replicates into Data Connect
- [ ] `manual_report_export`
- [ ] `no_extraction`

Selected: [ ]

### 2d. Data Connect warehouse (reporting)

- [ ] `direct_warehouse_connection` — Snowflake / SQL Server connection to operator's warehouse
- [ ] `warehouse_extract_to_landing` — nightly warehouse export to landing zone
- [ ] `no_extraction`

Selected: [ ]

### 2e. Report export files (manual uploads)

- [ ] `shared_drive_dump`
- [ ] `email_drop`
- [ ] `manual_upload_portal`
- [ ] `no_extraction`

Selected: [ ]

Evidence:
```
# credentials owner, sandbox availability, sample export dates
```

Open questions:
```
# rate limits? pagination behavior? data-refresh cadence?
```

---

## Dimension 3: Operating Pattern

Declares the operator's day-to-day usage pattern. Affects cadence,
reconciliation expectations, and which workflows can trust Yardi as
primary.

- [ ] `standalone_yardi`                 — Yardi is the only operating stack for this portfolio
- [ ] `yardi_plus_intacct`               — Yardi PMS + Intacct GL (common large-operator split)
- [ ] `yardi_plus_appfolio_split`        — different portfolios on Yardi and AppFolio (by segment or acquisition source)
- [ ] `yardi_cutover_in_progress`        — migrating out of Yardi into AppFolio or Entrata; dual-run window active
- [ ] `yardi_cutover_completed_archival` — cut over already; Yardi retained only for historical comparatives
- [ ] `yardi_plus_thirdparty_manager`    — TPM-managed properties land in Yardi; owner-managed land in another PMS
- [ ] `yardi_reporting_only`             — operating in AppFolio + Intacct; Yardi purely a reporting layer
- [ ] `yardi_for_commercial_only`        — Yardi runs commercial / mixed-use; residential is elsewhere (residential_multifamily scope may be empty)

Selected: [ ]

Cadence expectation:
- [ ] real_time
- [ ] hourly
- [ ] daily
- [ ] weekly
- [ ] monthly
- [ ] on_demand

Selected: [ ]

Evidence:
```
# who logs into Voyager daily? who touches RentCafe? who pulls Data Connect reports?
```

Open questions:
```
```

---

## Dimension 4: Data Sensitivity and Control

Declares PII / financial / legal sensitivity, retention posture, and
downstream distribution constraints.

### 4a. PII content

- [ ] `resident_pii_present`         — Voyager carries resident names, SSNs, contact info
- [ ] `employee_pii_present`         — Voyager or HR module carries staff PII
- [ ] `applicant_pii_present`        — RentCafe carries screening results, credit data, prior residences
- [ ] `vendor_pii_present`           — vendor tax ids (EIN/SSN) present
- [ ] `no_pii_in_scope`              — extract is restricted to de-identified aggregates only

Selected: [ ]

### 4b. Financial sensitivity

- [ ] `detailed_ledger_present`      — charge and payment detail at tenant grain
- [ ] `gl_actuals_present`           — posted entries at account / property / period grain
- [ ] `budget_forecast_present`      — internal budget / forecast versions visible
- [ ] `fee_schedule_present`         — recovery fees, management fees, margin data visible

Selected: [ ]

### 4c. Legal sensitivity

- [ ] `eviction_and_legal_notice_present`   — delinquency cases carrying legal filings
- [ ] `fair_housing_notes_present`          — screening / denial notes
- [ ] `lease_document_attachments_present`  — full lease PDFs
- [ ] `none_of_above`

Selected: [ ]

### 4d. Downstream control posture

- [ ] `no_restrictions`              — normalized output can be consumed by any downstream workflow
- [ ] `redact_resident_pii_downstream`
- [ ] `block_fee_schedule_distribution`
- [ ] `legal_review_required_for_eviction_data`
- [ ] `compliance_review_required_for_affordable_overlays`

Selected: [ ]

### 4e. Retention posture

- [ ] `retain_full_history_on_landing`
- [ ] `rolling_window_limited_to_Nyears` (declare N in Evidence)
- [ ] `purge_on_resident_close_plus_Nyears`
- [ ] `retention_matches_compliance_statute` (cite statute in Evidence)

Selected: [ ]

Evidence:
```
# cite internal data-governance policy or compliance team sign-off
```

Open questions:
```
# affordable overlay data? HUD / LIHTC compliance module?
```

---

## Scoring Summary

Until every REQUIRED dimension below is answered, this adapter stays at
`status: stub` and downstream workflows MUST NOT treat Yardi as primary
for any canonical object. Dimension 4 is required before any live-data
sample is accepted.

| Dimension | Required to advance | Gate |
|---|---|---|
| 1. Role | yes | adapter cannot advance without at least one role selected |
| 2. Access Path | yes | each declared role must have at least one access path |
| 3. Operating Pattern | yes | cadence must be declared |
| 4. Data Sensitivity and Control | yes | required before live data sample accepted |

Worksheet status:
- [ ] Dimension 1 closed
- [ ] Dimension 2 closed
- [ ] Dimension 3 closed
- [ ] Dimension 4 closed

Sign-off:
- data_platform_team: ________
- finance_reporting: ________
- compliance_risk: ________
- regional_ops_director: ________
- last_reviewed_at: ________

See `runbooks/yardi_classification_path.md` for the fork-and-advance
flow once this worksheet closes.
