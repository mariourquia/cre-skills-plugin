# PMS Connector (stub, vendor-neutral)

Property-management-system feed. The PMS is the operational system of record for properties, units, leases, residents, ledgers, prospects, work orders, and turns. This connector is the widest surface area in the ingestion layer.

## Status

`status: stub` — schema, mapping template, sample, and reconciliation checks only. No Yardi / Entrata / MRI / RealPage / AppFolio / Rent Manager adapter code lives here. A future vendor adapter would fork this connector and supply vendor-specific `mapping.yaml` entries.

## Entities

| Entity | One-liner |
|---|---|
| `property` | One row per property (PMS view of the asset). |
| `unit` | One row per unit per property. |
| `lease` | One row per executed lease. |
| `lease_event` | One row per lease lifecycle event (signed, move-in, notice, move-out, etc.). |
| `charge` | One row per resident charge posting. |
| `payment` | One row per resident payment receipt. |
| `delinquency_case` | One row per active delinquency case. |
| `lead` | One row per prospect inquiry. |
| `tour` | One row per tour scheduled or conducted. |
| `application` | One row per rental application. |
| `renewal_offer` | One row per renewal offer issued. |
| `work_order` | One row per maintenance work order. |
| `turn` | One row per unit turn project. |

## Scope

Vendor-agnostic. Defines the entity shape every PMS feed must provide, the primary key and provenance contract, and the reconciliation checks that must pass. Does not enumerate fields vendors carry but the subsystem does not need.

## Integration

- `pms.property` and `pms.unit` reconcile against the property master (see `qa/unit_count_reconciliation.yaml`).
- `pms.lease` + `pms.lease_event` feed the delinquency playbook, renewal retention, and lease-expiry metrics.
- `pms.charge` + `pms.payment` feed collections and aging metrics; required before any variance-narrative workflow runs against a property.
- `pms.lead` / `tour` / `application` feed the lease-up war room, leasing roles, and CRM cross-checks.
- `pms.work_order` feeds property-operations admin and building-systems-maintenance workflows.
- `pms.turn` feeds the capex prioritizer's turn-cost inputs and the post-move-out playbook.

See `INGESTION.md` for the landing convention and `reconciliation_checks.yaml` for the domain-specific QA invariants.
