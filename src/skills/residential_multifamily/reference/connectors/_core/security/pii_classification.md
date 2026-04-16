# PII Classification - Canonical Taxonomy

The authoritative classification of every personally identifying or otherwise sensitive field that any connector may carry. A field that is not listed here is rejected at schema-conformance time unless the entity contract declares a matching `classification` alongside a brief rationale the reviewer signs off on via `_core/change_log_conventions.md`.

Classifications: `none`, `low`, `moderate`, `high`, `restricted`. Definitions in `security_model.md`.

## Columns

For each canonical field the taxonomy declares:

- **canonical_field** - snake_case name used in entity contracts and mappings.
- **classification** - one of the five classes.
- **allowed_in_sample** - `true` only if the field can appear in `sample_input.json`, `sample_normalized.json`, or `example_raw_payload.jsonl` using synthetic content.
- **masking_rule** - default transform applied at rendering time. Full matrix in `masking_and_redaction.md`.
- **redaction_pattern** - regex or shape used by the sample-scan and log-scrubbing tests.
- **retention_default** - qualitative retention horizon (operational, extended, indefinite). No numeric years in prose.
- **downstream_exposure_guidance** - a short rule for which audiences may ever see the unmasked field and under what gate.

## Resident identifiers

| canonical_field | classification | allowed_in_sample | masking_rule | redaction_pattern | retention_default | downstream_exposure_guidance |
|---|---|---|---|---|---|---|
| `resident_name` | moderate | true (synthetic only) | first_initial_last_name_memo_first_initial_and_last | `[A-Z][a-z]+ [A-Z][a-z]+` | operational | unmasked allowed for operational routing only; masked in board-pack and investor-facing. |
| `email` | moderate | true (synthetic domain) | hash_or_partial_for_aggregate_full_for_communications | email-shape | operational | never rendered in board-pack; hashed for aggregate analytics. |
| `phone` | moderate | true (synthetic) | partial_mask_last_four | phone-shape | operational | unmasked only for operational dispatch. |
| `physical_address` | moderate | true (synthetic) | suite_level_mask_for_board_full_for_dispatch | postal-shape | operational | suite-level masking default; unmasking requires operational purpose. |
| `unit_number` | low (property-scoped) | true | none | token-shape | operational | property-scoped; no masking when joined only with property_id. |
| `date_of_birth` | high | false | forbidden_in_sample; masked_in_all_outputs | date-shape | extended | never rendered in any audience output. Access gated by ApprovalRequest. |
| `ssn` | restricted | false | forbidden_in_repo | `\d{3}-?\d{2}-?\d{4}` | legal | never stored in normalized or derived; raw only under encryption; unmasking prohibited. |
| `government_id` | restricted | false | forbidden_in_repo | alphanumeric with country-specific shape | legal | same as ssn. |
| `credit_score` | high | false | bucketed_only_for_aggregate_never_individual | three-digit | extended | aggregate bucket only; individual score never rendered outside screening workflow. |
| `background_check_result` | high | false | outcome_code_only_no_detail | outcome-enum | extended | outcome-code only; detail never rendered outside compliance_risk gated workflow. |
| `income_source` | moderate | true (synthetic) | category_only_no_employer_name | free-text redaction | operational | employer name never rendered to site_ops; category only. |
| `payment_instrument_detail` | high | false | last_four_only | `\d{12,19}` or routing-shape | operational | last-four only in any rendered output. |

## Employee identifiers

| canonical_field | classification | allowed_in_sample | masking_rule | redaction_pattern | retention_default | downstream_exposure_guidance |
|---|---|---|---|---|---|---|
| `employee_id` | low | true | none | token-shape | operational | internal routing only. |
| `employee_name` | moderate | true (synthetic) | first_initial_last_name | `[A-Z][a-z]+ [A-Z][a-z]+` | operational | unmasked to regional_ops and site_ops only. |
| `employee_ssn` | restricted | false | forbidden_in_repo | `\d{3}-?\d{2}-?\d{4}` | legal | raw only under encryption; never in normalized. |
| `compensation_detail` | high | false | aggregated_only | currency-shape | extended | individual detail only to compliance_risk with ApprovalRequest; aggregate for finance_reporting. |
| `termination_reason` | high | false | coded_reason_only | free-text redaction | extended | coded reason only; free-text narrative never rendered. |
| `protected_class_attributes` | forbidden_in_processed_output | false | never_rendered; never_used_as_feature | all protected-class attribute shapes | legal | never a model input, never a match key, never a routing key. See `fair_housing_controls.md`. |

## Vendor identifiers

| canonical_field | classification | allowed_in_sample | masking_rule | redaction_pattern | retention_default | downstream_exposure_guidance |
|---|---|---|---|---|---|---|
| `vendor_legal_name` | low | true (synthetic) | none | business-name | operational | public; unmasked in all rendered outputs. |
| `vendor_tax_id` | high | false | last_four_only_for_memo_full_only_for_remit | `\d{2}-?\d{7}` | extended | last-four only outside remit workflow. |
| `vendor_remit_to_address` | moderate | true (synthetic) | suite_level_mask_for_memo_full_for_remit | postal-shape | operational | full address only on remit documents. |

## Financial identifiers

| canonical_field | classification | allowed_in_sample | masking_rule | redaction_pattern | retention_default | downstream_exposure_guidance |
|---|---|---|---|---|---|---|
| `account_number` | high | false | last_four_only | `\d{6,17}` | extended | last-four in any rendered output; full only inside payment workflow. |
| `bank_routing` | high | false | last_four_only | `\d{9}` | extended | last-four only. |
| `invoice_detail_aggregated` | moderate | true (synthetic) | none | n/a | operational | unmasked for finance_reporting aggregates. |
| `invoice_detail_individual` | high | false | redacted_line_items_above_sensitivity_threshold | n/a | extended | individual line items gated by ApprovalRequest when sensitivity-tagged. |

## Legal and compliance identifiers

| canonical_field | classification | allowed_in_sample | masking_rule | redaction_pattern | retention_default | downstream_exposure_guidance |
|---|---|---|---|---|---|---|
| `eviction_detail` | high | false | status_code_only_for_memo | free-text redaction | extended | free-text narrative never rendered outside compliance_risk. |
| `fair_housing_complaint_detail` | restricted | false | forbidden_in_repo; legal_hold_capable | free-text redaction | indefinite | legal_hold capable; read-only; never rendered in any tailoring output. See `legal_hold_and_retention.md`. |

## Rules

1. `allowed_in_sample: true` never authorizes real data. It authorizes synthetic placeholders only. See `pii_sample_policy.md`.
2. `allowed_in_sample: false` means the field must not appear in any sample file or example payload in the repo. Sample-scan tests enforce.
3. `classification: restricted` means the field is forbidden in any file checked into the repo except in entity contracts (where it is named only to declare its contract).
4. A new field with no classification is rejected. Adding a field requires declaring its classification in the entity contract and citing this doc.
5. Downgrading a field's classification requires an ApprovalRequest with `subject_object_type: policy_exception` and the compliance_risk audience as required approver. See `approval_gates_for_integration_actions.md`.
6. A field that composes with another field to yield higher re-identifiability escalates to the higher class when joined. The entity contract must declare the join and the composed class.

## Field additions

When a connector needs a new canonical field:

1. Propose it in the entity contract with a candidate classification.
2. Reference the candidate class here in a change-log entry (`_core/change_log_conventions.md`).
3. Add a row to the relevant table above.
4. Update `masking_and_redaction.md` with the default masking rule if it differs from the class default.
5. Update `security_testing_guidance.md` if a new redaction pattern must be enforced.
