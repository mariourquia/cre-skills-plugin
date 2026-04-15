# Yardi Multi-Role Adapter

Adapter id: `yardi_multi_role`
Vendor family: `yardi_family`
Primary connector domain: `pms` (multi-domain; see classification)
Status: `stub` (wave_2)

## When to use this adapter

Use this adapter when Yardi sits anywhere in the operator's stack —
primary PMS (Voyager residential), primary GL (Voyager financial),
primary leasing CRM (RentCafe + Voyager leasing), reporting feed (Data
Connect warehouse), legacy / historical archive during migration, or
any combination across portfolio segments. Yardi is the most flexible
source family in the stack; the adapter supports this by making every
downstream posture CLASSIFICATION-GATED.

## Classification dependency

Unlike `appfolio_pms` (single-role, domain-fixed), this adapter does
NOT commit to primary-source behavior for any canonical object until
`classification_worksheet.md` closes. Until then:

- Every object is ingested in `historical_only` posture.
- No workflow may treat Yardi as primary for any canonical object.
- RentCafe-sourced leasing objects are held in quarantine until
  Dimension 2c (access path) and Dimension 4 (PII posture) close.

See `runbooks/yardi_classification_path.md` for the operator decision
tree.

## Multi-role posture

Classifications this adapter supports (Dimension 1 of the worksheet):

- `primary_pms` — Voyager residential is the primary PMS
- `primary_gl` — Voyager financial is the primary GL
- `primary_leasing_crm` — RentCafe + Voyager leasing is primary
- `primary_everything` — Yardi is primary for PMS + GL + leasing
- `secondary_reporting_feed` — Data Connect is a BI source; other
  systems are operationally primary
- `legacy_historical_only` — Yardi is read-only archive
- `dual_run_during_cutover` — Yardi + successor system both live
- `mixed_by_portfolio_segment` — split by portfolio segment

Workflows consume Yardi output with role assigned per posture. See
`workflow_activation_additions.yaml`.

## Source-of-truth claims

Yardi's per-object precedence depends on the operator's classification
outcome. Default posture (until classification closes) is
`historical_only` for every canonical object. Role-specific posture is
documented in `normalized_contract.yaml::precedence_if_role_*` fields
and cross-referenced in
`../../_core/stack_wave4/source_of_truth_matrix.md`.

| Canonical object | Default | If primary_pms | If primary_gl | If primary_leasing_crm | If legacy_historical_only |
|---|---|---|---|---|---|
| Property | historical_only | primary | secondary | n/a | historical_only |
| Unit | historical_only | primary | n/a | n/a | historical_only |
| UnitType (floor_plan) | historical_only | primary | n/a | n/a | historical_only |
| Lease | historical_only | primary | n/a | n/a | historical_only |
| LeaseEvent | historical_only | primary | n/a | n/a | historical_only |
| ResidentAccount | historical_only | primary | n/a | n/a | historical_only |
| Charge | historical_only | primary | secondary | n/a | historical_only |
| Payment | historical_only | primary | n/a | n/a | historical_only |
| DelinquencyCase | historical_only | primary | n/a | n/a | historical_only |
| Vendor | historical_only | secondary | secondary | n/a | historical_only |
| WorkOrder | historical_only | primary | n/a | n/a | historical_only |
| Lead | blocked | n/a | n/a | primary | historical_only |
| Tour | blocked | n/a | n/a | primary | historical_only |
| Application | blocked | n/a | n/a | primary | historical_only |
| Account (GL chart) | historical_only | n/a | primary | n/a | historical_only |
| BudgetLine | historical_only | n/a | primary | n/a | historical_only |
| ActualLine | historical_only | n/a | primary | n/a | historical_only |
| ForecastLine | historical_only | n/a | primary | n/a | historical_only |

"blocked" = held in quarantine until Dimension 2c access path and
Dimension 4 PII posture close.

## Sub-systems covered

- `voyager_pms` — residential operational (unit, lease, ledger, WO)
- `voyager_gl` — financial accounting (chart, actuals, budgets,
  forecasts)
- `voyager_construction_support` — job cost (limited; Procore usually
  primary)
- `rentcafe_leasing` — leasing funnel + prospect portal
- `rentcafe_resident_portal` — post-move-in resident self-service
  (retained in raw only; no canonical mapping)
- `data_connect_warehouse` — replicated reporting warehouse
- `report_export_files` — Excel / CSV exports from Voyager UI

## File map

```
manifest.yaml                              <- adapter manifest (schema conformant)
README.md                                  <- this file
classification_worksheet.md                <- operator interview
bounded_assumptions.yaml                   <- assumptions held until classification closes
provisional_source_contract.yaml           <- placeholder contract
source_contract.yaml                       <- full raw Yardi payload shape per sub-system
normalized_contract.yaml                   <- canonical-object mapping per role
field_mapping.yaml                         <- field-by-field mappings with transforms
dq_rules.yaml                              <- DQ rules (yd_ prefix)
reconciliation_rules.md                    <- narrative reconciliation rules
reconciliation_checks.yaml                 <- machine-readable recon checks
edge_cases.md                              <- documented edge cases
crosswalk_additions.yaml                   <- master_data crosswalk fragments
workflow_activation_additions.yaml         <- workflow activation fragment
sample_raw/                                <- synthetic raw JSONL files per entity
sample_normalized/                         <- synthetic canonical JSONL files per entity
runbooks/yardi_classification_path.md      <- operator decision tree
runbooks/yardi_onboarding.md               <- per-access-path onboarding
runbooks/yardi_common_issues.md            <- well-known Yardi gotchas
runbooks/yardi_migration_to_appfolio.md    <- cutover protocol
tests/test_yardi_adapter.py                <- pytest conformance tests
__init__.py                                <- Python package marker
```

## Links

- Runbooks: see `runbooks/` directory.
- Source-of-truth matrix:
  `../../_core/stack_wave4/source_of_truth_matrix.md`.
- Tolerance bands:
  `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.

## Master_data crosswalk dependencies

The following master_data crosswalks must be seeded before this
adapter can exit classification and advance to `starter`:

- `property_master_crosswalk` — Yardi propid ↔ AppFolio property_id ↔
  Intacct entity_dim
- `unit_crosswalk` — Yardi hunit ↔ AppFolio unit_id
- `lease_crosswalk` — Yardi hlease ↔ AppFolio lease_id
- `resident_account_crosswalk` — Yardi hten ↔ AppFolio tenant_id
- `vendor_master_crosswalk` — Yardi hvendor ↔ Intacct vendor ↔
  Procore vendor
- `account_crosswalk` — Yardi GL chart ↔ Intacct chart
- `unit_type_crosswalk` — Yardi fpcode ↔ canonical unit_type_id
- `building_crosswalk` — Yardi building_code ↔ canonical building_id
- `capex_project_crosswalk` — Yardi job ↔ Procore project
- `asset_crosswalk` — Yardi propid ↔ Dealpath asset
- `market_crosswalk` / `submarket_crosswalk` — Yardi labels ↔ canonical ids
- `charge_code_crosswalk_by_property` — PROPERTY-SCOPED chargecode decode
- `report_export_templates` — column_map per Yardi report template

## Security and PII notes

- Resident PII (names, emails, phones, SSNs) and applicant PII
  (screening data, credit scores) are present in Voyager and RentCafe.
  Dimension 4 of `classification_worksheet.md` MUST close before any
  live sample data flows.
- Vendor tax_ids (EIN/SSN) hashed at landing; plaintext never
  persisted.
- Downstream redaction follows the strictest declared posture.
- Legal / eviction data carries separate legal_sensitivity tier; access
  gated by legal review when operator declares
  `legal_review_required_for_eviction_data` in Dimension 4d.

## Quality bar

- Status: `stub`. No live credentials. All examples carry
  `api_key_placeholder` / `warehouse_connection_placeholder`.
- Every sample record carries `status: sample`.
- No real PII; synthetic names ("Maple Vista", "Harbor Crest",
  "Lantern Flats", "Briarfield") and synthetic property ids.
- No hardcoded numeric tolerance thresholds in prose; references cite
  `reference/normalized/schemas/reconciliation_tolerance_band.yaml`.
- Canonical `pms` / `gl` / `crm` schemas win on every conflict.
- Classification-gating is enforced at DQ rule level
  (`yd_classification_pending_block_primary_claims`).

## Open items tracked for advancement to starter

- `reconciliation_tolerance_band.yaml` must exist or be created in
  `reference/normalized/schemas/` (cited by every reconciliation check
  and several DQ rules).
- `asset_crosswalk.yaml`, `market_crosswalk.yaml`,
  `submarket_crosswalk.yaml`, and `charge_code_crosswalk_by_property`
  must be created in `master_data/`.
- `t_code_decode` adapter-local helper must be implemented and tested.
- `map_yardi_chargecode_property_scoped` implementation must be
  registered.
- `source_registry_entry` seeds (one per supported source system) must
  be written once classification closes.
- RentCafe API scope documentation must be captured during Dimension 2c.
