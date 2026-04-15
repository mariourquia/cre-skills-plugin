# Security Model - Integration Layer

Seven-layer defense. Every inbound record from any connector must pass each layer before it becomes readable by a skill, an overlay, or a tailoring output. A record that fails any layer is quarantined and does not advance to the next.

All cross-references use paths rooted at `src/skills/residential_multifamily/`. When canonical paths move, this doc moves with them via a change-log entry per `_core/change_log_conventions.md`.

## Layer one - data_classification

Every field on every entity in every connector carries one of five classifications. Classifications are declared in the entity contract (`reference/connectors/_schema/entity_contract.schema.yaml`) and resolved against the canonical taxonomy in `pii_classification.md`.

| Class | Meaning | Default handling |
|---|---|---|
| `none` | No sensitivity. Public reference data. | No masking, no gating. |
| `low` | Non-personal operational data. | No masking; audited access. |
| `moderate` | Personal but not special-category. | Masked in aggregate outputs; unmasked only for operational routing. |
| `high` | Personal and high-harm-if-leaked. | Masked by default; unmasking requires an ApprovalRequest. |
| `restricted` | Forbidden in repo, sample, prose, or derived outputs. Allowed in raw only under encryption at rest and access control. | Never rendered in any tailoring output. |

A field with no declared class is rejected at schema-conformance time (`tests/test_connector_contracts.py`).

## Layer two - access_control

Access is least-privilege and role-based. Roles map to the tailoring audiences declared in `tailoring/AUDIENCE_MAP.md`:

- `executive`
- `regional_ops`
- `asset_mgmt`
- `finance_reporting`
- `development`
- `construction`
- `compliance_risk`
- `site_ops`

Full rules in `least_privilege_guidance.md`. Enforcement lives in the operator's infrastructure, not in this repo. What this repo owns:

- The role catalog (this list).
- The per-layer read and write policy (`least_privilege_guidance.md`).
- The forbidden combinations (e.g., `site_ops` cannot read restricted-class fields anywhere in any connector).

## Layer three - transit

Every connector manifest declares an `auth_kind` from a closed placeholder set:

- `api_key_placeholder`
- `oauth_placeholder`
- `sftp_key_placeholder`
- `mtls_placeholder`
- `basic_auth_placeholder`
- `email_inbox_placeholder`
- `shared_drive_placeholder`
- `tls_required_placeholder` (for generic HTTPS endpoints with service tokens bound at deploy time)
- `none` (used only by synthetic or file-drop sources that carry no credentials)

A manifest that does not declare `auth_kind` is rejected at schema-conformance time. The repo carries no real credential, no real URL, no real hostname. Full rules in `secrets_handling.md`.

## Layer four - at_rest

Encryption at rest is required for all three data layers (`raw`, `normalized`, `derived`). Operator-owned infrastructure provides the encryption backend (cloud KMS, managed storage encryption, vault-managed keys). The repo declares the requirement; it does not implement it.

- Raw retains its original provenance. Encryption does not rewrite provenance fields (`source_name`, `source_type`, `source_date`, `extracted_at`, `extractor_version`, `source_row_id`).
- Normalized and derived are rebuilt on demand from raw; their encryption wraps the rebuilt file.
- Key rotation cadence is operator-defined. Rotation must not invalidate prior raw lineage.

## Layer five - audit

Every connector operation emits an immutable audit record. Operations include:

- `file_landed`
- `normalized`
- `reconciled`
- `workflow_activated`
- `manual_override_applied`
- `approval_action`
- `deletion_requested`

Full schema and retention rules in `audit_trail.md`. Audit records are append-only. Deletion of an audit record is itself an audited event and requires an ApprovalRequest gated by the compliance_risk audience.

## Layer six - approval

Any integration-layer action that touches the canonical approval floor materializes an ApprovalRequest conforming to `_core/schemas/approval_request.yaml`. The full list of integration-layer gated actions lives in `approval_gates_for_integration_actions.md`. Examples:

- Reference data refresh (market rents, concessions, staffing ratios, material costs, labor rates, turn cost library, capex library, schedule duration assumptions, utility benchmarks, vendor rate cards, approval thresholds, screening policies).
- Master data crosswalk override.
- Schema change acknowledgment.
- Mapping override.
- PII classification downgrade.
- Legal hold release.
- Reference rollback.
- Connector deprecation.
- Production adapter activation.
- Fair-housing-sensitive manual override.

The approval floor is set in `_core/approval_matrix.md`. Overlays may tighten; overlays may not loosen.

## Layer seven - fair_housing

Resident-facing outputs and any model input that could influence a housing decision are scanned for protected-class proxies. No protected-class attribute is ever permitted as a match key or a model input, regardless of apparent predictive value. Full rules in `fair_housing_controls.md`. Violations are exceptions of the highest severity and route directly to the compliance_risk audience.

## legal_hold posture

Records under legal hold are treated as read-only regardless of their normal classification. Retention is extended per `legal_hold_and_retention.md`. No overwrite, no deletion, no masking change without an ApprovalRequest approved by both compliance_risk and a named legal-counsel approver.

## Composition rule

Classifications compose upward, not downward. A field that is `moderate` in one connector becomes `high` when joined with another field that elevates re-identifiability (for example, `unit_number` + `date_of_birth`). The entity contract must declare composed fields; automated joins that escalate classification require an ApprovalRequest.

## Enforcement surface

| Layer | Declared in | Enforced by |
|---|---|---|
| data_classification | entity contract | `tests/test_connector_contracts.py` |
| access_control | `least_privilege_guidance.md` | operator infrastructure + review |
| transit | connector manifest | `tests/test_connector_contracts.py` + grep in `security_testing_guidance.md` |
| at_rest | operator infrastructure | operator audit |
| audit | `audit_trail.md` | operator infrastructure + review |
| approval | `_core/schemas/approval_request.yaml` | tests referenced in `security_testing_guidance.md` |
| fair_housing | `fair_housing_controls.md` | `tests/test_regulatory_isolation.py` + review |
