# Adapter Lifecycle

Every vendor-family adapter under `reference/connectors/adapters/` moves
through four stages: `stub`, `starter`, `production`, and `deprecated`. Each
stage has explicit entry criteria. Status is declared in the adapter's
`manifest.yaml` and must match the current state of its files and tests.

## Stage one: stub

Entry state for every adapter shipped with the subsystem skeleton.

Required artifacts:

- `manifest.yaml` declares `status: stub`.
- `mapping_hints` contain illustrative entries only. Hints are sourced
  from general knowledge of the vendor family, not from a validated
  operator payload.
- `example_raw_payload.jsonl` is synthetic. Every row carries
  `status: sample` or `status: stub`. No real property names, no PII,
  no live identifiers.
- `mapping_template.yaml` is a scaffold that references the canonical
  `mapping.yaml` layout but leaves vendor-specific columns as placeholders.
- `normalized_output_example.jsonl` shows post-mapping shape using the
  canonical field names.
- `tests/test_adapter.py` asserts manifest conformance to
  `adapter_manifest.schema.yaml`.

Exit criteria to advance to `starter`:

- An operator has provided a real, sanitized sample payload.
- The mapping template has been run against that payload and the mapping
  errors resolved.
- Tests pass.
- A reviewer has signed off in `author_metadata.reviewed_by`.

## Stage two: starter

Real data, no live credentials.

Required artifacts:

- `manifest.yaml` declares `status: starter`.
- `example_raw_payload.jsonl` contains sanitized payload rows drawn from
  an actual vendor-system export. Sanitization rules: no real property
  names, no resident PII, no employee PII, no contract prices in prose,
  no account numbers. Synthetic replacements substitute for sensitive
  fields while preserving the original shape and column headers.
- `mapping_template.yaml` is filled against real column headers. No
  TODO placeholders in mapped entities.
- `normalized_output_example.jsonl` is produced by running the template
  over the sanitized payload.
- Tests include schema conformance plus a shape check that the sanitized
  payload normalizes into the canonical schema without dropping required
  fields.
- The matching source system is registered in
  `reference/connectors/source_registry/source_registry.yaml` with
  `status: stubbed` at minimum.
- `author_metadata.reviewed_by` is populated.

Exit criteria to advance to `production`:

- Live credential method has been declared in the source registry entry.
- The adapter has completed its rollout wave.
- Operator has validated a non-sample ingestion window end to end.
- Required audience sign-off is captured. Finance-carrying domains
  (`gl`, `ap`, `construction`, `hr_payroll`) require
  `finance_reporting` sign-off. PII-carrying or regulated domains
  (`pms`, `hr_payroll`, plus any adapter routed through the
  affordable or regulatory overlays) require `compliance_risk`
  sign-off. Leasing-funnel domains (`crm`) require `site_ops` sign-off.
- Reconciliation checks declared by the canonical connector pass for at
  least one full cadence cycle on the adapter's data.

## Stage three: production

Live, operator-validated.

Required artifacts:

- `manifest.yaml` declares `status: production`.
- `author_metadata.reviewed_by` is populated by a named role.
- The matching source system is registered with `status: active` in
  `source_registry.yaml`.
- Rollout wave has completed; `rollout_wave` tag is retained for
  planning history.
- The adapter references a credential method (via the source registry,
  never inside the adapter files themselves).

Operator responsibilities while an adapter is in production:

- Keep `last_updated` current when mapping_template.yaml changes.
- Log any mapping exceptions through the canonical connector's
  reconciliation checks, not by mutating adapter files silently.
- Flag drift (new columns appearing, columns disappearing, taxonomy
  changes) as a mapping-template revision with a version bump in the
  adapter manifest.

## Stage four: deprecated

Replacement path defined.

Required artifacts:

- `manifest.yaml` declares `status: deprecated` and includes
  `deprecation_metadata` with `replacement_adapter_id`,
  `dual_run_window_start`, `dual_run_window_end`, and `cutoff_date`.
- The replacement adapter exists in this directory and is at `starter`
  or `production` status.
- A dual-run window has been scheduled during which both adapters are
  allowed to produce records. Reconciliation checks must match between
  the two adapters for the window.
- After the cutoff date, the deprecated adapter retains its files for
  provenance lookup but is removed from
  `vendor_family_registry.yaml` active listings.

## Gate summary

| Stage       | Real data      | Live credentials  | Audience sign-off                                                                                                       | Source registry status |
|-------------|----------------|-------------------|-------------------------------------------------------------------------------------------------------------------------|------------------------|
| stub        | no             | no                | no                                                                                                                      | not required           |
| starter     | sanitized      | no                | reviewer only                                                                                                           | stubbed                |
| production  | live           | yes               | finance_reporting for financial; compliance_risk for PII or regulated; site_ops for leasing funnel                      | active                 |
| deprecated  | historical     | cutoff            | replacement path signed off by the same audiences that approved production                                              | deprecated             |

## Non-negotiables

- An adapter cannot advance to `production` without the matching
  audience sign-off.
- An adapter cannot advance to `production` while any reconciliation
  check declared by the canonical connector is failing on its data.
- A stub adapter does not ingest live data, even in dev. Stubs are for
  orientation only.
