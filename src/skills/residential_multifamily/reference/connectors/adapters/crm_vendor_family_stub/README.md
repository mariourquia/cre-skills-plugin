# CRM Vendor Family Stub

Adapter id: `crm_vendor_family_stub`
Vendor family: `generic_crm_stub`
Connector domain: `crm`
Status: `stub`

## Scope

Stub overlay on the canonical `crm` connector at `../../crm/`. Documents
the lead-source taxonomies, tour-outcome enums, and pipeline-stage
conventions most commonly seen in multifamily leasing CRMs. Canonical
`crm` schema remains the contract.

Orientation examples (not endorsements, not in file paths): platforms
commonly encountered include the Entrata, Knock, Funnel, Engrain,
RentCafe CRM, and Yieldstar CRM families. Operators fork this stub to
an internal codename.

## Assumed source objects

- `lead` (inquiry master record)
- `tour` (scheduled and completed site visits)
- `application` (application state and approval)

## Raw payload naming

- `leads_<yyyymmdd>.csv`
- `tours_<yyyymmdd>.csv`
- `applications_<yyyymmdd>.csv`

Synthetic example at `example_raw_payload.jsonl`, `status: sample`.

## Mapping template usage

Apply `mapping_template.yaml` over the canonical CRM mapping at
`../../crm/mapping.yaml`. Canonical mapping wins on conflict.
Lead-source and tour-outcome taxonomies go through their named
transforms (`map_lead_source`, `map_tour_outcome`).

## Known limitations

- Stubs carry synthetic data only.
- Fair-housing guardrails require that preference-note free-text is
  screened before storage; the adapter does not carry the screening
  logic, but it flags the field path.

## Common gotchas

- Duplicate leads appear when the same prospect inquires across
  channels. Dedup on a composite key including phone, email, and
  property, not on `lead_id` alone.
- Merged leads drop source attribution silently. Preserve all source
  channels on merge.
- Offline touches (walk-ins, phone calls logged manually) are often
  missing from pipeline-stage transitions. Reconcile against the PMS
  leasing funnel.
- Lead-source taxonomies vary widely. Use `map_lead_source` to
  normalize against the subsystem's canonical source taxonomy.
- Timezone ambiguity on tour scheduling. Preserve the original `tz`
  field; do not assume UTC.
- Preference notes occasionally contain fair-housing-sensitive
  free-text. Screen before storage; the subsystem's fair-housing
  guardrail lists disallowed categories.
- Resident-account dedup across CRM and PMS relies on phone and email
  match because each system issues its own internal id.
