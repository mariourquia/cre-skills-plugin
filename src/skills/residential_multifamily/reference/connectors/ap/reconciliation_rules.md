# AP Reconciliation Rules

Narrative describing how reconciliation in the AP domain works.

## Reconciliation scope

The AP connector is the system of record for vendor master, invoices, contracts, commitments, purchase orders, and payment status. It reconciles with:

- The general ledger (for open payable balance and cash disbursement timing).
- The construction connector (for capex commitments that span both systems).
- The PMS work-order system (for work-order-triggered invoices through the vendor dispatch chain).

## Totals that must agree

### Open AP vs GL payable account

For each property_id and period, the sum of `ap.invoice` open balances (`amount_cents - paid_to_date_cents` where `status != voided`) equals the `gl_actual` balance on the canonical_account_slug `ap_payable` at period close. Tolerance is penny-level rounding as declared in `gl/manifest.yaml`. Enforced by `ap_ap_to_gl_payable_alignment`.

### Commitment vs invoice-to-date vs change orders

For each commitment_id, `invoiced_to_date_cents` must not exceed `committed_amount_cents + sum(approved change orders)`. Tolerance is zero. Enforced by `ap_commitment_invoice_cap`.

### Contract burn-down vs invoice sum

For each fixed-total contract (`pricing_model IN (lump_sum, retainer)`), `sum(invoice.amount_cents where invoice.contract_id = contract.contract_id)` must not exceed `contract_total_cents`. Tolerance is zero. Enforced by `ap_contract_burn_down_consistency`.

### PO balance vs invoice-to-date

For each purchase_order in status `issued` or `partial`, `amount_cents - sum(invoice.amount_cents where invoice.po_id = po_id)` must be non-negative. Tolerance is zero. Enforced by `ap_purchase_order_balance_tracks`.

### AP to construction bridge

For each vendor that appears in both ap.vendor and construction.commitment, the vendor_id must be the same canonical id via `vendor_ap_construction_bridge`. No tolerance; mismatch is a crosswalk gap.

## Tolerances

| Reconciliation | Absolute tolerance | Relative tolerance |
|---|---|---|
| Open AP vs GL payable | 0 | referenced from gl/manifest.yaml penny-rounding |
| Commitment invoice cap | 0 | 0 |
| Contract burn-down | 0 | 0 |
| PO balance | 0 | 0 |
| AP-construction bridge | 0 | 0 |

All non-zero tolerance values live in referenced configuration.

## Escalation triggers

- A blocker failure on AP vs GL payable alignment holds month-close. Escalates to the compliance_risk and executive audiences because audit trail is at stake.
- Commitment overdraw (invoiced beyond committed + approved COs) holds the invoice and escalates to the approval matrix declared in `_core/approval_matrix.md`.
- COI expiry failure (`ap_coi_expiry_gate`) escalates immediately because dispatch continues only with valid insurance.
- Duplicate invoice detection (`ap_duplicate_invoice_by_vendor_and_invoice_number`) escalates to the site_ops audience because double-pay risk is material.

## Cross-domain reconciliation dependencies

AP reconciliation is a precondition for:

- Monthly close (via the AP-to-GL reconciliation).
- Vendor-invoice-validator skill (every invoice passes AP QA first).
- Construction cost-to-complete (pulls commitment burn-down from AP + construction).
- COI compliance checker (consumes vendor master insurance dates).

A blocker in AP holds monthly_property_operating_review for the affected property until reconciled.
