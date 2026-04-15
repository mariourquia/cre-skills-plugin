# Construction Platform Stub

Adapter id: `construction_platform_stub`
Vendor family: `generic_construction_stub`
Connector domain: `construction`
Status: `stub`

## Scope

Stub overlay on the canonical `construction` connector at
`../../construction/`. Documents the project, cost-code, commitment,
change-order, draw, and retention conventions commonly seen in
construction and capex platforms. Canonical `construction` schema
remains the contract.

Orientation examples (not endorsements, not in file paths): platforms
commonly encountered include Procore, Sage 300 CRE (Timberline),
Autodesk Construction Cloud (Autodesk Build), CMiC, and Viewpoint Vista
families. Operators fork this stub to an internal codename.

## Assumed source objects

- `capex_project` (project master, budget, and status)
- `estimate_line_item` (budgeted line items by cost code / CSI)
- `bid_package` (RFPs and awarded bids)
- `change_order` (CO master with status)
- `draw_request` (payment applications with retention)
- `schedule_milestone` (schedule dates)
- `vendor` and `vendor_agreement` (subcontractors)

## Raw payload naming

- `projects_<yyyymmdd>.csv`
- `commitments_<yyyymmdd>.csv`
- `change_orders_<yyyymmdd>.csv`
- `draw_requests_<yyyymmdd>.csv`

Synthetic example at `example_raw_payload.jsonl`, `status: sample`.

## Mapping template usage

Apply `mapping_template.yaml` over the canonical construction mapping at
`../../construction/mapping.yaml`. Canonical mapping wins on conflict.

## Known limitations

- Stubs carry synthetic data only.
- Budget-version handling is operator-specific; the stub flags it but
  does not impose a specific convention.

## Common gotchas

- Multiple budget versions in flight. Always carry `budget_version`;
  do not silently pick the latest.
- Owner vs contractor contingency commingled. Split via
  `map_contingency_type` before variance analysis.
- Pending vs approved change orders. Filter by
  `change_order_status` before running any variance-to-budget check.
- Draw timing lags actual physical work by weeks. Do not use
  `draw_amount` as a completed-work proxy.
- Rehab expense miscoded as construction capex and vice versa. Confirm
  against `cost_code` and CSI mapping before opex/capex classification.
- Retention holdbacks release at substantial completion. Reconcile
  `retention_amount` against `commitment_amount` at close-out.
- Commitment amounts change silently when change orders post. Always
  join commitments to COs to get the current committed figure.
- Owner-contractor id mismatch between construction and GL systems.
  Resolve through `capex_project_crosswalk`.
