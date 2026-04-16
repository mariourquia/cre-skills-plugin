# PMS Reconciliation Rules

Narrative describing how reconciliation in the PMS domain works: which totals must agree with which sources, what tolerances exist, and what triggers escalation.

## Reconciliation scope

The PMS is the operational system of record for properties, units, leases, residents, ledgers, prospects, maintenance, and turns. It reconciles with:

- The property master (for unit counts and property-level metadata).
- The general ledger (for AR balances, cash receipts, and revenue timing).
- The accounts-payable system (indirectly, through shared vendor records on work orders).
- The CRM (for lead, tour, and application linkage).
- The construction connector (for unit-turn postings and capex draws that touch rentable units).

## Totals that must agree

### Unit counts (PMS versus property master)

For each property_id, the count of `pms.unit` records must equal `pms.property.unit_count_total`, with rentable units (excluding model, employee, down status) equal to `pms.property.unit_count_rentable`. Tolerance is zero. Enforced by `pms_unit_count_reconciles`. Missing units trigger a review because occupancy denominators are sensitive to the base.

### Lease status rollup (PMS internal)

For each property_id, the sum of units by status (occupied + vacant_rented + vacant_unrented + notice_occupied + notice_unrented) must equal `unit_count_rentable`. Model, employee, and admin units are excluded from both sides. Tolerance is zero. Enforced by `pms_lease_status_reconciles`.

### Charge and payment totals (PMS versus GL)

For each (property_id, period), the sum of `pms.charge.amount_cents` for charge_type in (rent, base_rent) must reconcile to the GL rental-income revenue postings per the canonical_account_slug mapping. Cash receipts via `pms.payment` must reconcile to the GL cash-receipts postings within the same period. Tolerance is the penny-level rounding allowance declared in `gl/manifest.yaml`. Enforced cross-domain by `gl_budget_actual_alignment` via the cross_source_reconciliation template.

### Delinquency balance (PMS internal)

For each (property_id, as_of_date), the sum of `pms.delinquency_case.current_balance_cents` for open cases reconciles to the aged AR balance computed from `pms.charge - pms.payment`. Tolerance is zero. A variance indicates either a missing charge, a payment posted to the wrong lease, or a write-off not propagated.

### Lease-up funnel consistency (PMS internal + CRM)

For each property_id and window, the count of pms.lead reaching each pipeline stage must equal the count of downstream artifacts (tour for tour_scheduled, application for applied, approval for approved, lease for leased). Tolerance is zero for the full window. Enforced indirectly via CRM checks that trace lead to lease.

## Tolerances

| Reconciliation | Absolute tolerance | Relative tolerance |
|---|---|---|
| Unit counts | 0 | 0 |
| Lease status rollup | 0 | 0 |
| Charge and payment vs GL | 0 | referenced from gl/manifest.yaml penny-rounding window |
| Delinquency balance | 0 | 0 |
| Lead funnel | 0 | 0 |

All tolerance values that are non-zero live in the connector manifest or the referenced overlay. No numeric thresholds appear in this document.

## Escalation triggers

- A blocker reconciliation failure holds the landing from promotion to normalized and emits a reconciliation_report.json entry. The operator is notified via the channel declared in `overlays/org/<org_id>/overlay.yaml#escalation_routes`.
- A warning reconciliation failure promotes the landing but flags the variance in the report; the monthly property operating review workflow surfaces outstanding warnings.
- Repeat warnings (same check failing in consecutive landings) escalate to the asset_mgmt or compliance_risk audience per the escalation matrix declared in `_core/approval_matrix.md`.

## Cross-domain reconciliation dependencies

The PMS reconciliation_report.json is an input to the GL and AP reconciliation reports. A blocker in PMS prevents promotion of matched GL and AP periods until PMS is re-landed successfully. The chain is enforced by `tests/test_connector_contracts.py` at the subsystem root.
