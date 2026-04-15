# PMS Vendor Family Stub

Adapter id: `pms_vendor_family_stub`
Vendor family: `generic_pms_stub`
Connector domain: `pms`
Status: `stub`

## Scope

Stub overlay on the canonical `pms` connector at `../../pms/`. Documents
the column-name patterns and taxonomies most commonly seen in
property-management-system exports so operators can accelerate mapping
when a real vendor payload arrives. Canonical `pms` schema remains the
contract.

Orientation examples (not endorsements, not in file paths): major
PMS vendors in this space include platforms in the Yardi, RealPage,
Entrata, AppFolio, Rent Manager, and ResMan families. Operators
typically fork this stub to a vendor-specific internal codename before
populating real sample payloads.

## Assumed source objects

A typical PMS export emits some subset of the following raw objects:

- `property` (master record per property/community)
- `unit` (unit roster with occupancy status)
- `lease` (active, future, and historical leases)
- `charge` (rent, recurring, and one-time charges)
- `payment` (tender-typed payments against resident accounts)
- `delinquency_case` (aged balances and legal stage tags)
- `lead`, `tour`, `application`, `renewal_offer` (leasing funnel)
- `work_order` and `turn` (maintenance and make-ready)

## Raw payload naming

Typical export filenames follow patterns such as:

- `rent_roll_<yyyymmdd>.csv`
- `delinquency_<yyyymmdd>.csv`
- `leasing_pipeline_<yyyymmdd>.csv`
- `charge_ledger_<yyyymmdd>.csv`
- `payment_register_<yyyymmdd>.csv`

The synthetic example in this directory lives at
`example_raw_payload.jsonl` and carries `status: sample`.

## Mapping template usage

The file `mapping_template.yaml` is applied on top of the canonical PMS
mapping at `../../pms/mapping.yaml`. Entries in this adapter template
are non-binding hints; the canonical mapping overrides on conflict.

Typical workflow:

1. Fork this directory to a vendor-specific slug.
2. Replace `example_raw_payload.jsonl` with a sanitized sample from the
   target vendor.
3. Walk each canonical entity (`property`, `unit`, `lease`, `charge`,
   `payment`, ...) and add per-column mapping entries against the
   vendor's real column headers.
4. Run the adapter's tests. Advance `manifest.yaml` `status` when the
   gates in `../adapter_lifecycle.md` pass.

## Known limitations

- Stubs carry synthetic data; no live values.
- Mapping hints cover high-traffic columns; long-tail columns require
  operator adjustment.
- Unit-status taxonomies and charge-type taxonomies are highly
  vendor-specific. The hints below are starting points only.
- No PII, no real property names, no live identifiers in this tree.

## Common gotchas

- Model and amenity units are often omitted from rent-roll exports.
  Reconcile `unit_count_total` against master data.
- Mixed unit-status taxonomies. A single vendor may expose
  `occupied`, `occupied_on_notice`, `vacant_unrented`, `vacant_notice`,
  `model`, and `down` under inconsistent labels. Normalize through
  `map_unit_status` and keep the raw taxonomy in the ingest log.
- Concessions are encoded inconsistently: sometimes as a negative rent
  line, sometimes as a separate credit row, sometimes embedded in a
  rolled-up effective-rent column. The canonical normalized model
  tracks `concessions_total_cents` regardless of source encoding.
- Unit-number suffix conventions vary. `101-A`, `101.01`, and `101a`
  may refer to the same physical unit. Resolution lives in the
  property master crosswalk, not in the adapter.
- Future-lease rows appear in some exports and not others. Filter by
  lease status before running reconciliation checks.
- Resident identifiers are rarely stable across moves or household
  reconfigurations. Dedup on the composite key
  (`lease_id`, `unit_id`, `property_id`) rather than on
  `resident_account_id` alone.
