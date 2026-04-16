# Example Adapter Authoring Guide

Step-by-step workflow for turning a stub into a real-vendor adapter.

## Prerequisites

- A canonical connector exists for the domain (one of `pms/`, `gl/`, `crm/`,
  `ap/`, `market_data/`, `construction/`, `hr_payroll/`,
  `manual_uploads/`).
- The target source system is registered, or can be registered, in
  `reference/connectors/source_registry/source_registry.yaml`.
- The operator has provided at least one real export sample. Sample must be
  sanitized before it enters this tree.

## Step one: fork the closest stub

Pick the stub that matches the canonical domain of the target source system.
Copy the entire stub directory under a new slug in the same directory.

```
cp -R adapters/pms_vendor_family_stub adapters/pms_my_vendor_adapter
```

Rules:

- Slug is snake_case. No spaces. No vendor trademarks in the slug; use an
  internal codename if needed.
- New directory sits under `adapters/` next to the other adapter folders.
- `__pycache__` directories, if present, are not copied.

## Step two: populate the raw payload

Replace `example_raw_payload.jsonl` with sanitized rows from the real
vendor export. Sanitization rules:

- No real property names. Substitute `sample_property_one`,
  `sample_property_two`, etc.
- No resident PII. Substitute synthetic names and hashed-looking
  identifiers.
- No employee PII. Substitute role codes.
- No real account numbers. Substitute placeholder patterns such as
  `acct_placeholder_001`.
- No contract prices written as dollar amounts in text. Numeric fields
  that represent amounts should retain shape; prose inside the row
  should reference magnitudes qualitatively.
- Preserve the original column headers, enum values, and null patterns.
  The shape is what makes the adapter useful; the values can be swapped.

Every row carries `status: sample` alongside provenance stubs
(`source_name`, `source_type`, `source_date`, `extracted_at`,
`extractor_version`, `source_row_id`). Use a fixed fake `extracted_at`
timestamp; never a live one.

## Step three: refine the mapping template

Open `mapping_template.yaml` and walk through each entity the canonical
`mapping.yaml` declares for this domain.

- For each source column that exists in the real export, add a
  `source_column -> normalized_column` entry with the appropriate
  transform (`trim_string`, `to_integer`, `to_iso_date`,
  `dollars_to_cents`, `to_boolean`, or a domain-specific transform).
- For columns that do not exist in the real export, leave a comment that
  the field will be derived, inferred, or dropped.
- For entities the vendor does not expose, mark them `status: TODO` with
  a `note` explaining why.

When a vendor emits a column that does not correspond to any canonical
field, do not invent a canonical field. Raise the gap to the canonical
connector's owners and let them decide whether to amend the canonical
schema. Adapters never shadow canonical schemas.

## Step four: run the tests

From the skills repo root:

```
pytest src/skills/residential_multifamily/reference/connectors/adapters/<adapter_slug>/tests
```

Required passing checks:

- `test_adapter.py` asserts manifest conformance to
  `adapter_manifest.schema.yaml`.
- If the adapter includes a shape check (recommended at `starter`
  status), it runs the mapping template over the sanitized payload and
  asserts the normalized output matches the canonical schema primary key
  shape.

Resolve errors by editing only files under the adapter's own directory.
Never edit canonical connector files to make an adapter test pass.

## Step five: advance the status

In `manifest.yaml`, update `status` from `stub` to `starter`:

- Populate `author_metadata.authored_by` and `author_metadata.authored_role`.
- Populate `author_metadata.reviewed_by`.
- Update `last_updated` to today.
- Keep `vendor_family` descriptive but vendor-neutral-ish. Use an
  internal codename rather than a trademark if sharing the file widely.

To advance from `starter` to `production`, follow the gates in
`adapter_lifecycle.md`. Production requires audience sign-off
(finance_reporting, compliance_risk, or site_ops depending on the
domain), plus a successful reconciliation cycle.

## Step six: register

Add the adapter to `adapters/vendor_family_registry.yaml` with
`adapter_id`, `adapter_name`, `connector_domain`, `status`, `rollout_wave`,
a `short_description`, and `owner`.

Add or update the matching source system in
`reference/connectors/source_registry/source_registry.yaml`. Set the
source registry `status` to `stubbed` for `starter`, or `active` for
`production`. Never declare a live `credential_method` inside the adapter
itself; credentials live in the deployment environment.

## Step seven: commit

- Commit only files under the new adapter directory plus the two
  registry files (`vendor_family_registry.yaml` and
  `source_registry.yaml`).
- Do not commit edits to canonical connector files in the same change.
  Canonical-schema evolution is a separate review path.
- Follow the subsystem's snake_case conventions. No em dashes, no
  emojis, no numeric dollar amounts in prose.

## Worked example outline

1. Operator provides an export drop from a mid-market PMS.
2. Author forks `pms_vendor_family_stub` to
   `pms_mid_market_vendor_adapter` (internal codename, not a trademark).
3. Author sanitizes three months of raw rent roll, charge, and payment
   exports into `example_raw_payload.jsonl` rows.
4. Author fills `mapping_template.yaml` against the vendor's column
   headers for property, unit, lease, charge, and payment. Marks
   `work_order`, `turn`, `lead`, `tour`, `application`, and
   `renewal_offer` as TODO.
5. Author reruns tests, resolves two mapping errors.
6. Author advances `manifest.yaml` to `status: starter`, registers
   the adapter in `vendor_family_registry.yaml`, registers the source
   in `source_registry.yaml`.
7. Operator validates one cadence cycle in stage. Finance_reporting
   and compliance_risk reviewers sign off.
8. Author advances to `status: production`, flips the source registry
   entry to `status: active`, keeps the adapter under active monitoring.
