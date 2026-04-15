# Audit Trail - Immutable Record of Every Connector Operation

Every connector operation emits an audit record. Audit records are append-only. Deletion of an audit record is forbidden. The audit log is retained under the `indefinite` retention class defined in `legal_hold_and_retention.md`.

## What qualifies as a connector operation

The following events, at minimum, produce an audit record. Operators may add event types in overlay, never remove canonical ones.

- `file_landed` - a raw file lands under `reference/raw/<connector>/<YYYY>/<MM>/`.
- `landing_rejected` - a raw file is rejected at landing and quarantined under `_rejected/`.
- `normalized` - a raw file has been mapped to normalized, or a row has been promoted from raw into a normalized table.
- `reconciled` - a reconciliation check has run and a reconciliation_report.json has been attached.
- `reconciliation_blocker_raised` - a blocker check failed and promotion to derived is halted.
- `workflow_activated` - a downstream workflow has been triggered by a normalized record.
- `manual_override_applied` - an operator override has modified a normalized record or mapping.
- `approval_action` - an ApprovalRequest has transitioned state (created, approved, rejected, withdrawn).
- `deletion_requested` - deletion of a record has been proposed.
- `deletion_executed` - deletion of a record has been executed.
- `legal_hold_applied` - `legal_hold: true` stamped on a matching record set.
- `legal_hold_released` - `legal_hold: false` restored after release.
- `legal_hold_read` - a read against a legal-hold record.
- `classification_changed` - a field classification has changed in the entity contract.
- `schema_change_acknowledged` - a schema change has been reviewed and signed off.
- `mapping_override_applied` - a mapping.yaml override has been applied.
- `reference_data_refreshed` - a reference-data refresh has been approved and applied.
- `reference_rollback` - a reference-data rollback has been approved and applied.
- `connector_activated` - a connector has entered production status.
- `connector_deprecated` - a connector has exited production status.

## Audit record schema

Every audit record carries the following fields. The fields below are the repo-declared contract; operators may extend but not remove.

| field | type | description |
|---|---|---|
| `audit_id` | string | stable unique id for this audit record. Operator-generated (UUID or equivalent). Never mutated. |
| `operation` | string (enum) | one of the operation types above. |
| `subject_connector_id` | string | the connector_id under `reference/connectors/<domain>/` that owns this event. |
| `subject_entity` | string | the canonical entity slug (e.g., `lease`, `invoice`, `work_order`) or `manifest` / `mapping` / `schema` for structural events. |
| `subject_identifier` | string | row count, file name, primary key, or resource identifier affected. Masked if the identifier itself is classified `high` or `restricted`. |
| `actor` | string | who executed the event. One of: `system_process`, a human approver slug, or `external_source`. |
| `actor_role` | string | mapped role from the audience catalog (`executive`, `regional_ops`, `asset_mgmt`, `finance_reporting`, `development`, `construction`, `compliance_risk`, `site_ops`) or `system`. |
| `timestamp` | string (ISO-8601, UTC) | event time. |
| `before_state_reference` | string | pointer (storage-backend-specific) to the state before the event. For file_landed, null. For normalized, points to the raw record. For overrides, points to the prior normalized state. |
| `after_state_reference` | string | pointer to the state after the event. |
| `reason` | string | coded reason when applicable. Free-text narrative is forbidden here; use a coded reason token (e.g., `reason_code: late_arriving_record`, `reason_code: operator_override_manual_fix`). |
| `approval_request_id` | string | present for every gated operation. Must cite a valid approval_request conforming to `_core/schemas/approval_request.yaml` in `approved` status. |
| `classification_context` | string | the most-sensitive field class touched by this operation (e.g., `moderate`, `high`, `restricted`). Used to route the audit record to the correct retention tier. |
| `legal_hold_context` | boolean | true if the operation touched one or more records under legal hold. |
| `connector_version` | string | version of the connector definition at the time of the event (`connector_id` + semver). |
| `adapter_version` | string | version of the operator's adapter code at the time of the event. |
| `correlation_id` | string | stable id shared across related events in a single workflow (file_landed → normalized → reconciled → workflow_activated form one correlated thread). |

## Immutability

The audit log is append-only. Specific rules:

- No audit record is edited after write.
- No audit record is deleted.
- A superseding event produces a new audit record with its own `audit_id` and a pointer in `before_state_reference` to the prior record's `after_state_reference`.
- A bug fix that corrects a misattributed event writes a new record with `operation: manual_override_applied` and `reason_code: audit_correction`, not an edit of the original.

Immutability is enforced by the operator's audit storage layer. The repo declares the contract and reviews compliance during incident review.

## Retention

- Audit log retention is `indefinite` (see `legal_hold_and_retention.md`).
- Audit retention is not shortened by the release of a legal hold on the underlying record.
- Audit retention is not shortened by the expiration of the operator's ordinary records-management horizon.
- The audit log lives in its own storage tier so that expiration of underlying record retention does not affect it.

## Signing

Each audit record carries a content hash. Operators sign the hash with a signing key bound in the secret backend. Signatures are retained with the record.

- The signing key rotates per the operator's rotation cadence (see `secrets_handling.md`).
- A rotation event itself produces an audit record (`operation: reference_data_refreshed` with `subject_entity: signing_key`) so that signature verification can always locate the correct key epoch.
- Verification is available to any authorized reader; any verification failure routes to compliance_risk with severity one.

## Access

Audit log access is role-based per `least_privilege_guidance.md`:

- `compliance_risk` can read all audit records.
- `asset_mgmt` and `finance_reporting` can read records tied to their scope.
- `site_ops` can read records tied to their specific property and their own actor slug.
- `executive` can read summary views; raw audit records require a read justification.
- Writing an audit record is limited to the operator's audit-service identity; no human actor writes directly.

## Retrieval contract

Audit queries support at least these filters without special handling:

- by `audit_id`
- by `correlation_id`
- by `subject_connector_id` and date range
- by `actor` and date range
- by `operation` type
- by `classification_context` (for retention-tier review)
- by `legal_hold_context: true`
- by `approval_request_id`

## Relationship to ApprovalRequest

Every gated operation references an `approval_request_id`. The approval_request is itself recorded in the audit log via `operation: approval_action` events for create, approve, reject, and withdraw. The canonical approval schema is `_core/schemas/approval_request.yaml`.

## Secret scrubbing

Audit records never contain secret material:

- No bound credentials.
- No tokens.
- No raw PII in the `subject_identifier` field; masking per `masking_and_redaction.md`.
- No free-text narrative in `reason`; coded reasons only.

## Incident review

Audit records are the primary evidence in incident review:

- Credential leakage - audit trail reconstructs what the leaked credential touched.
- Classification downgrade dispute - audit trail shows who approved and why.
- Legal hold breach - audit trail identifies every read against a held record.
- Mapping regression - audit trail shows when and by whom a mapping was overridden.

## Related

- `_core/schemas/approval_request.yaml` - approval schema.
- `_core/change_log_conventions.md` - change-log conventions for canonical changes.
- `legal_hold_and_retention.md` - retention and hold posture.
- `unsafe_defaults_registry.md` - the "silent resolution" entries that audit must catch.
- `security_testing_guidance.md` - tests that verify audit immutability and presence.
