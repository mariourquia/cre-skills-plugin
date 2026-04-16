# AP Vendor Family Stub

Adapter id: `ap_vendor_family_stub`
Vendor family: `generic_ap_stub`
Connector domain: `ap`
Status: `stub`

## Scope

Stub overlay on the canonical `ap` connector at `../../ap/`. Documents
the invoice, vendor-master, and approval-status conventions most commonly
seen in multifamily AP systems. Canonical `ap` schema remains the contract.

Orientation examples (not endorsements, not in file paths): AP platforms
commonly encountered include AvidXchange, Nexus Payables, Bill.com,
AppFolio AP, Yardi Payables, and Stampli families. Operators fork this
stub to an internal codename.

## Assumed source objects

- `vendor` (vendor master with status and COI flags)
- `vendor_agreement` (master services agreements and contract metadata)
- `charge` (invoice lines landing against property / account)
- `payment` (cash disbursement records)

## Raw payload naming

- `ap_invoices_<yyyymmdd>.csv`
- `vendor_master_<yyyymmdd>.csv`
- `ap_payments_<yyyymmdd>.csv`

Synthetic example at `example_raw_payload.jsonl`, `status: sample`.

## Mapping template usage

Apply `mapping_template.yaml` over the canonical AP mapping at
`../../ap/mapping.yaml`. Canonical mapping wins on conflict.

## Known limitations

- Stubs carry synthetic data only.
- Partial-payment and credit-memo handling is vendor-specific and
  typically requires the `vendor_master_crosswalk`.

## Common gotchas

- Duplicate vendors across legacy and current systems. Consolidate
  through the `vendor_master_crosswalk`.
- Credit memos silently reverse posted invoices. Watch for sign flips
  when joining on `invoice_number`.
- Partial payments split across pay runs. Not always rolled up under a
  parent `invoice_id`; dedup on the composite key
  (`vendor_id`, `invoice_number`).
- Shared contracts touching multiple properties. Per-property
  allocation rules live in the `vendor_agreement` master.
- Missing property assignment. Flag and route to a manual allocation
  queue rather than imputing.
- Tax and freight lines collapse into the `amount` column in some
  exports. Decompose per vendor rules before normalization.
- COI expiry blocks payment dispatch per the vendor insurance
  guardrail. Respect the check in downstream workflows; the adapter
  does not gate on its own.
