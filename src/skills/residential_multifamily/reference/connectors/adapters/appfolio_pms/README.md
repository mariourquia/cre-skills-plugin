# AppFolio PMS Adapter

Adapter id: `appfolio_pms`
Vendor family: `appfolio_family`
Connector domain: `pms`
Status: `stub` (wave_4)

## Role in the stack

AppFolio Property Manager is the operational system of record for unit
roster, leasing funnel, lease lifecycle, tenant ledger, work order
dispatch, and vendor directory at the site level. Accounting system of
record (entity-level GL, legal entity ids, vendor tax ids, and formal
posting) remains in Intacct. This adapter wires AppFolio into the
canonical `pms` connector under `../../pms/` while acknowledging the
dual-source reality with Intacct.

## Source-of-truth claims

| Canonical object | Primary | Secondary | Notes |
|---|---|---|---|
| Property | secondary | Intacct primary | AppFolio carries operating attributes; Intacct owns legal_entity_id and GL hierarchy. Reconcile via property_master_crosswalk. |
| Building | primary | — | AppFolio carries the in-property building split for garden / townhome layouts. |
| Unit | primary | — | AppFolio is authoritative for unit roster and occupancy status. |
| UnitType | primary | — | |
| Lease | primary | — | AppFolio owns lease lifecycle. |
| LeaseEvent | primary | — | Event stream reconstructed from AppFolio status transitions plus explicit event records. |
| ResidentAccount | primary | — | AppFolio TenantId maps 1:1 to canonical resident_account_id via resident_account_crosswalk. |
| Charge | primary | Intacct secondary | AppFolio posts tenant-side charges; Intacct posts the GL side. Tie-out runs at property-period grain. |
| Payment | primary | Intacct secondary | Same pattern as Charge. |
| DelinquencyCase | primary | — | Derived from AppFolio delinquency stage + payment plan state. |
| Lead | primary | — | AppFolio Guest Card objects map to canonical Lead. |
| Tour | primary | — | ShowingIds from AppFolio Leasing module. |
| Application | primary | — | AppFolio rental application records. |
| ApprovalOutcome | primary | — | Derived from AppFolio ApplicationStatus transitions + ScreeningResult. |
| WorkOrder | primary | — | AppFolio Service Requests map to canonical WorkOrder. |
| TurnProject | derived | — | Not a native AppFolio object. Inferred from (move_out LeaseEvent, make_ready WorkOrders, move_in LeaseEvent) sequence on a unit. |
| Vendor | secondary | Intacct primary | AppFolio vendor directory is operational; Intacct vendor master is authoritative for tax_id, W-9, and 1099 reporting. Dedup via vendor_master_crosswalk. |
| VendorAgreement | secondary | AP primary | AppFolio carries informal rate cards; formal agreements live in AP. |

## Covered entities (this adapter)

- Properties (AppFolio Properties API, GL Partner associations)
- Units and UnitTypes (unit roster + floor plan metadata)
- Unit turns inferred from status transitions (make_ready state)
- Leads (Guest Cards)
- Tours / Showings
- Rental applications and outcome
- Leases (active, future, historical)
- Tenants (resident accounts)
- Lease events (move_in, move_out, renewal, notice, transfer)
- Charges (Tenant Charges)
- Payments (Tenant Payments)
- Tenant ledgers (aging and balances)
- Work orders (Service Requests)
- Vendors (directory only; master-of-record is Intacct)

## Deferred / out of scope

- Budget upload (lives in GL adapter and manual_uploads).
- Cash posting to GL (lives in GL adapter).
- Formal vendor agreements and W-9 tracking (lives in AP adapter).
- Preventive maintenance calendar (AppFolio carries it, but canonical
  `PreventiveMaintenanceTask` is not in this adapter's pass).
- CapexProject coordination (lives in construction adapter).

## Operator notes

- Pilot property selection: choose one property per GL Partner, one
  stabilized and one lease-up, so property-code drift and future-lease
  handling both surface during onboarding. See
  `runbooks/appfolio_onboarding.md`.
- AppFolio's portfolio hierarchy (Portfolio > GL Partner > Property)
  rarely matches the operator's ownership-entity hierarchy. Resolve via
  `property_master_crosswalk` and add explicit `related_canonical_ids`
  for multi-property entities.
- Concession accounting is informal in AppFolio. Formal concession
  accruals continue to flow through the AP and GL adapters.
- Work orders that close within one extract window can lose
  `DateCompleted` in date-range API calls; use `status=Completed` as the
  primary signal and re-extract for back-fill.
- Evictions are not distinct from delinquency stage in native AppFolio.
  The adapter derives `EvictionFiled` and `EvictionJudgment` lease events
  from the DelinquencyStage enum sequence; see
  `runbooks/appfolio_common_issues.md`.

## Files in this directory

```
manifest.yaml                              <- adapter manifest (schema conformant)
README.md                                  <- this file
source_contract.yaml                       <- raw AppFolio payload shape per entity
normalized_contract.yaml                   <- canonical-object mapping declarations
field_mapping.yaml                         <- field-by-field mappings per entity
mapping_template.yaml                      <- test-required overlay on canonical pms/mapping.yaml
example_raw_payload.jsonl                  <- small synthetic mixed payload (test harness)
normalized_output_example.jsonl            <- small synthetic canonical payload (test harness)
sample_raw/                                <- per-entity synthetic raw JSONL files
sample_normalized/                         <- per-entity synthetic canonical JSONL files
dq_rules.yaml                              <- AppFolio-specific DQ rules
reconciliation_rules.md                    <- narrative reconciliation rules (AppFolio vs Intacct)
reconciliation_checks.yaml                 <- machine-readable checks
edge_cases.md                              <- edge cases and AppFolio quirks
source_registry_entry.yaml                 <- fragment for source_registry.yaml
crosswalk_additions.yaml                   <- fragment for master_data crosswalks
workflow_activation_additions.yaml         <- fragment for workflow_activation_map.yaml
runbooks/appfolio_onboarding.md
runbooks/appfolio_common_issues.md
tests/test_adapter.py                      <- pytest conformance tests
```

## Quality bar

- Status: `stub`. No live credentials. Example `api_key_placeholder`.
- Every sample record carries `status: sample`.
- No real PII; synthetic names, synthetic addresses, synthetic property ids.
- No hardcoded numeric thresholds in prose; references cite the overlay
  or master schema that owns the band.
- Canonical `pms` schema wins on every conflict.
