# AP Connector (stub, vendor-neutral)

Accounts-payable feed. Vendor master, invoices, contracts, commitments, purchase orders, and payment status. Distinct from the GL connector even though some operators run AP inside the general ledger — this connector captures the operational vendor-invoice side, the GL connector captures posted actuals.

## Status

`status: stub` — schema, mapping template, sample, and reconciliation checks only. No NetSuite / Sage / QuickBooks / Bill.com / AvidXchange / Nexus adapter code lives here.

## Entities

| Entity | One-liner |
|---|---|
| `vendor` | One row per vendor in the master. |
| `invoice` | One row per vendor invoice received. |
| `contract` | One row per active vendor contract. |
| `commitment` | One row per open AP commitment (distinct from GL commitment — tracks invoice-match status). |
| `purchase_order` | One row per PO issued to a vendor. |
| `payment_status` | One row per invoice payment state. |

## Scope

Vendor-agnostic. Provides the invoice-to-contract matching surface for the vendor-invoice-validator skill and the commitment-to-draw reconciliation for construction.

## Integration

- `ap.vendor` + `ap.invoice` feed vendor-invoice-validator.
- `ap.contract` + `ap.commitment` feed CAM reconciliation and construction commitment tracking.
- `ap.payment_status` feeds cash-flow and aging dashboards.

See `INGESTION.md`.
