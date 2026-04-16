# AP Derived Dependencies

Which canonical metrics, workflows, and templates depend on normalized AP data.

## Required normalized inputs

- `ap.vendor`: vendor master.
- `ap.invoice`: invoice ledger.
- `ap.payment_status`: payment state.

## Optional enrichment inputs

- `ap.contract`: recurring contract reference.
- `ap.commitment`: open commitment tracking.
- `ap.purchase_order`: PO three-way match.

## Confidence minimum

- No open blocker failures on `ap.invoice` and `ap.vendor` landing.
- COI expiry clean for any vendor in active dispatch.
- AP vs GL payable reconciled within tolerance.

## Blocking data issues

- Unresolved vendor_id on an invoice.
- Orphan commitment invoice cap.
- COI expiry in the past for a safety-critical vendor.
- Duplicate invoice by (vendor_id, vendor_invoice_number).
- Property mapping missing on an invoice without corporate_overhead flag.
- Non-USD invoices without registered FX rate.

## Fallback mode when partial

- Without ap.contract, contract burn-down metrics refuse; one-off invoices still process.
- Without ap.commitment, commitment-draw metrics refuse; three-way match degrades to PO + invoice.
- Without ap.purchase_order, three-way match refuses; two-way match (invoice + contract) still runs.
- Without ap.payment_status, aging analytics refuse.

## Canonical metrics that depend on AP

### Property Operations family

- `controllable_opex_per_unit`: benefits from AP-level vendor segmentation to attribute opex properly.
- `rm_per_unit`: cross-checked against AP invoice spend on R&M vendor categories.

### Asset Management family

- `noi` and `noi_margin`: depend on GL being AP-reconciled.
- `capex_spend_vs_plan`: draws on AP's commitment/invoice burn plus construction draws.

### Development and Construction family

- `cost_to_complete`: requires AP open commitments + construction commitments + COs + draws.
- `trade_buyout_variance`: depends on AP vendor/contract data.
- `change_orders_pct_of_contract`: depends on AP commitment total plus construction COs.

## Example output types

- Vendor invoice validation report (rate compliance, scope-vs-pay, duplicate detection).
- Monthly AP aging report with COI flags.
- Vendor spend-by-property report.
- Commitment burn-down dashboard per project.
- COI refresh queue.
- 1099 consolidation by canonical vendor.

## Dependent workflows

- `vendor_dispatch_sla_review`: uses vendor master and invoice history.
- `bid_leveling_procurement_review`: cross-checks AP vendor history.
- `change_order_review`: integrates AP commitment data.
- `draw_package_review`: integrates AP invoice data.
- Monthly close workflows (`monthly_property_operating_review`, `monthly_asset_management_review`).
