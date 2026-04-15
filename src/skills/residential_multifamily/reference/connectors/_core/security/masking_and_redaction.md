# Masking and Redaction - Default Rules by Audience and Class

This doc specifies the default transform applied to a field before it is rendered into any tailoring output. Masking is keyed to two inputs: the field's classification (from `pii_classification.md`) and the destination audience (from `tailoring/AUDIENCE_MAP.md`).

The default rule applies unless the workflow declares a higher or lower sensitivity posture and materializes an ApprovalRequest justifying the deviation.

## Audience catalog

The eight canonical audiences:

- `executive`
- `regional_ops`
- `asset_mgmt`
- `finance_reporting`
- `development`
- `construction`
- `compliance_risk`
- `site_ops`

Two derived destinations that also receive rendered output:

- `board_pack` - materials for ownership, lender, or investor review. Always treated as the highest-sensitivity destination.
- `operational_routing` - internal task routing where unmasked identifiers are necessary for the field team to act. Always treated as the lowest-masking destination for routing-critical identifiers.

## Masking transforms - catalog

Named transforms used by the matrix below:

- `full` - render the value verbatim. Used only where the audience has operational need and the field's class permits it.
- `first_initial_last_name` - `John Doe` becomes `J. Doe`. Applies to resident_name, employee_name.
- `first_initial_only` - `John Doe` becomes `J.`. Used for the most sensitive memo contexts.
- `partial_mask_last_four` - reveal only the last four characters. Applies to phone, account_number, bank_routing, vendor_tax_id.
- `partial_mask_local_only` - email local part hashed; domain preserved. Applies to email for aggregate analytics.
- `email_hash` - cryptographic hash, no recoverable content. Applies to email in aggregate reporting.
- `suite_level_mask` - street and city preserved; unit or suite number and resident name suppressed. Applies to physical_address in board-pack contexts.
- `bucketed` - render a bucket label, not the raw value. Applies to credit_score (bucket ranges only), compensation_detail (aggregate bands only).
- `coded_reason` - render a coded reason, not the free-text narrative. Applies to termination_reason, eviction_detail.
- `status_code_only` - render a status enum only, no narrative. Applies to eviction_detail in memo contexts.
- `aggregated_only` - render only when aggregated across a minimum sample size. Applies to compensation_detail, invoice_detail.
- `never_rendered` - the field never appears in any rendered output. Applies to ssn, government_id, protected_class_attributes, fair_housing_complaint_detail.
- `forbidden_in_repo` - the field never appears in any file checked into the repo. Enforced by secret-scan and sample-scan tests.

## Rule matrix - by class and audience

A cell reads: the transform applied by default when a field of the given class is rendered to the given audience.

| class \ audience | executive | regional_ops | asset_mgmt | finance_reporting | development | construction | compliance_risk | site_ops | board_pack | operational_routing |
|---|---|---|---|---|---|---|---|---|---|---|
| `none` | full | full | full | full | full | full | full | full | full | full |
| `low` | full | full | full | full | full | full | full | full | full | full |
| `moderate` | first_initial_last_name | full | full | aggregated_only | first_initial_last_name | first_initial_last_name | full | full | first_initial_only | full |
| `high` | bucketed | coded_reason | bucketed | aggregated_only | coded_reason | coded_reason | full | coded_reason | never_rendered | coded_reason |
| `restricted` | never_rendered | never_rendered | never_rendered | never_rendered | never_rendered | never_rendered | never_rendered | never_rendered | never_rendered | never_rendered |

Notes on the matrix:

- `operational_routing` is the only destination permitted `full` for moderate-class identifiers; it is where the site needs the real name to dispatch a work order, the real phone to reach the resident, the real suite to show up at the right door.
- `compliance_risk` receives the widest unmasked access to high-class fields because that is the audience responsible for the downstream review; the access is still gated by the access_control layer.
- `board_pack` is always the most restrictive destination for resident-linked fields; it rarely needs an individual identifier and never needs an individual sensitive one.

## Field-level overrides

Where a specific field's default differs from its class default, the per-field rule in `pii_classification.md` wins. Examples:

- `resident_name` - class `moderate`. In memo contexts (executive, board_pack) the default is `first_initial_and_last` (`J. Doe`). In operational_routing the default is `full`.
- `email` - class `moderate`. In aggregate reporting the default is `email_hash`; in resident communication workflows the default is `full`.
- `physical_address` - class `moderate`. In board_pack the default is `suite_level_mask`; in dispatch the default is `full`.
- `credit_score` - class `high`. Never rendered individually; always `bucketed` even for compliance_risk unless inside the gated screening workflow that requires the raw value.
- `account_number`, `bank_routing` - class `high`. Default is `partial_mask_last_four` across every audience; full value appears only inside the payment workflow and is gated by ApprovalRequest.
- `vendor_legal_name` - class `low`. Always `full`.

## Financial detail - aggregate vs individual

The matrix treats financial detail as two distinct canonical fields:

- `invoice_detail_aggregated` - class `moderate`. Default `full` for finance_reporting and asset_mgmt; `aggregated_only` for external destinations.
- `invoice_detail_individual` - class `high`. Default `redacted_line_items_above_sensitivity_threshold`; unredacted rendering gated by ApprovalRequest.

## Derived rule - from class and audience

Rendering code must resolve the transform via this order:

1. If the field is `restricted`, render `never_rendered`.
2. If the field has a per-field override in `pii_classification.md`, apply it.
3. If the field is under legal hold, apply the legal-hold posture in `legal_hold_and_retention.md`.
4. Apply the matrix cell for the field's class and the destination audience.

## Fair-housing interaction

A rendering request that would expose a protected-class attribute is rejected regardless of audience. Protected-class attributes are declared in `fair_housing_controls.md` and classified `forbidden_in_processed_output` in `pii_classification.md`; they never appear in any rendered output under any gate.

## Legal-hold interaction

A field under legal hold is rendered read-only and masked to the most restrictive cell that any current legal-hold order requires. Legal-hold posture overrides audience defaults toward more restriction, never less. See `legal_hold_and_retention.md`.

## Deviation protocol

A workflow that wishes to render at a different masking level than the matrix default must:

1. Materialize an ApprovalRequest with `subject_object_type: policy_exception` citing this doc.
2. Route to the compliance_risk audience.
3. Log the deviation in the audit record.

## Test surface

- `tests/test_connector_contracts.py` - checks that every canonical field has a classification.
- A planned sample-scan test in `security_testing_guidance.md` enforces that rendered samples never carry unmasked high-class or restricted-class values.
- A planned render-time test verifies the matrix above against a fixture audience set.
