# AP Identity Resolution

How vendors, contracts, invoices, and commitments in the AP connector crosswalk to canonical identifiers.

## Crosswalk pointers

- `reference/connectors/master_data/vendor_crosswalk.yaml`: vendor identity, including merges and DBAs.
- `reference/connectors/master_data/property_crosswalk.yaml`: property identity (shared).
- `reference/connectors/master_data/contract_registry.yaml`: multi-property contract allocations.
- `reference/connectors/master_data/vendor_ap_construction_bridge.yaml`: vendors that appear in both AP and construction connectors.

## Match methods

| Method | Use | Confidence |
|---|---|---|
| `exact` | AP-native vendor_id, contract_id, invoice_id where AP is authoritative. | Highest. |
| `composite` | (normalized_vendor_name_hash, tax_id_hash) for duplicate-vendor detection; (vendor_id, vendor_invoice_number) for duplicate-invoice detection; (vendor_name_normalized, bank_account_hash) as secondary. | High. Surfaces merge candidates. |
| `fuzzy` | Normalized-name match only when tax_id is unavailable; low confidence, always queued. | Low. |
| `manual` | Operator-adjudicated vendor merge recorded in vendor_crosswalk with survivor vendor_id, reviewer, and timestamp. | Authoritative once recorded. |

## Confidence scoring

Every vendor_crosswalk row carries `confidence_tier`. Merges below `high` confidence are held pending operator review; until adjudicated, both vendor_ids remain distinct and the AP landing does not promote merged identity.

## Hard cases

### Duplicate vendors

Vendors are often created twice in the AP system: once at procurement setup, again when accounts payable receives an invoice with a slightly different name. The vendor_crosswalk surfaces candidates via composite tax_id + normalized name match. Failure mode: two vendor_ids for one entity split 1099 reporting, COI tracking, and spend-per-vendor analytics. Mitigation: `ap_vendor_duplicate_detection`.

### Merged vendors

Once the operator confirms a merge, one vendor_id becomes the survivor and the other carries `merged_into = survivor_vendor_id` plus `inactive = true`. No new invoice or commitment may reference the non-survivor. Failure mode: open AP obligations still referencing the non-survivor misroute cash disbursements. Mitigation: `ap_merged_vendor_survivorship`.

### Invoice credit memos

Vendors issue credit memos as negative-amount invoices. The canonical handling requires a `related_invoice_id` pointing to the offset invoice. Failure mode: an unlinked credit memo silently reduces open payable balance without a traceable source. Mitigation: `ap_invoice_credit_memo_handled`.

### Shared vendor contracts across multiple properties

An org-wide pest-control contract, a regional elevator service contract, and a portfolio-wide IT vendor all generate invoices that must allocate across properties. The contract_registry declares the contract_id as multi-property with an `allocation_basis` (square_footage, unit_count, revenue, direct-coded property_id). Failure mode: without a basis, shared costs bucket to one property and distort per-property CAM and controllable opex. Mitigation: `ap_shared_contract_multi_property_allowed` + `ap_invoice_property_assignment_required`.

### Vendor appearing in both AP and construction systems

A subcontractor on a capex project may be paid through the construction draw system while also submitting non-project invoices through AP. The vendor_ap_construction_bridge keeps the vendor_id stable across both connectors. Failure mode: two vendor_ids (one in AP, one in construction) fragment vendor-level spend and insurance tracking. Mitigation: the bridge crosswalk ensures a single canonical vendor_id; construction.commitment and ap.invoice both reference it.

## Failure modes summary

| Failure | Symptom | Check |
|---|---|---|
| Duplicate vendor not surfaced | Split 1099s, COI gaps, fragmented spend | `ap_vendor_duplicate_detection` |
| Merged vendor with open obligation | Misrouted disbursements | `ap_merged_vendor_survivorship` |
| Credit memo without link | Unexplained payable reduction | `ap_invoice_credit_memo_handled` |
| Shared contract without allocation basis | Per-property CAM distorted | `ap_shared_contract_multi_property_allowed` |
| Invoice without property assignment | Opex allocation distorted | `ap_invoice_property_assignment_required` |
| Duplicate invoice (same vendor + invoice #) | Double-pay risk | `ap_duplicate_invoice_by_vendor_and_invoice_number` |
| Vendor in AP and construction with different ids | Spend fragmented across two connectors | vendor_ap_construction_bridge missing entry |
