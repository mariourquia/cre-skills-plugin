# Least-Privilege Guidance - Role-Based Access Policy for the Integration Layer

Policy only. This repo does not enforce access at runtime; the operator's infrastructure does. This doc defines the canonical read, write, and approve rules for each audience across the three data layers (`raw`, `normalized`, `derived`) plus structural artifacts (manifests, mappings, classifications, reference tables, audit logs).

Roles map to the tailoring audiences declared in `tailoring/AUDIENCE_MAP.md`:

- `executive`
- `regional_ops`
- `asset_mgmt`
- `finance_reporting`
- `development`
- `construction`
- `compliance_risk`
- `site_ops`

Plus two system-level identities that are not tailoring audiences:

- `system_process` - the operator's connector adapter, audit service, retention job, and related automated agents.
- `external_source` - an upstream system producing inbound records. Never a reader of normalized or derived.

## Read policy - by layer

Read means "may view the record contents, subject to masking rules in `masking_and_redaction.md`."

### raw layer

| role | read policy |
|---|---|
| `system_process` | yes - the normalization pass and audit tooling read raw. |
| `compliance_risk` | yes - for incident review, legal hold review, fair-housing audit. |
| `executive` | only through summary views; raw record access requires a read justification and an audit entry. |
| every other audience | no direct read. Raw is operator-only territory. Readers of downstream data rely on normalized and derived. |

Incident-review read access by a human non-compliance audience materializes an ApprovalRequest and writes an audit entry with `operation: legal_hold_read` or a dedicated read-justification code.

### normalized layer

| role | read policy |
|---|---|
| `system_process` | yes. |
| `compliance_risk` | yes, full scope across all connectors. |
| `asset_mgmt` | yes, scoped to the portfolio assigned to the user. |
| `finance_reporting` | yes for financial entities (GL, AP, invoice detail, budget, forecast); scoped to the assigned portfolio. |
| `regional_ops` | yes for resident-linked and operational entities in the region; scoped to the region. |
| `site_ops` | yes for the single property assigned; restricted to operational routing fields; no access to compensation detail, no access to screening outcomes, no access to fair-housing complaint narratives. |
| `development` | yes for construction-domain entities on active projects. |
| `construction` | yes for construction-domain entities on active projects. |
| `executive` | yes through aggregated views; individual-record reads require justification and audit entry. |

Masking applies per `masking_and_redaction.md` regardless of layer-level read permission.

### derived layer

| role | read policy |
|---|---|
| `system_process` | yes. |
| `compliance_risk` | yes, full scope. |
| `asset_mgmt`, `finance_reporting`, `regional_ops`, `development`, `construction`, `executive` | yes, scoped to their portfolio or region or project. |
| `site_ops` | yes for property-level operational derived metrics. |

## Write policy - by layer

Write means "may create, modify, or promote records at this layer."

### raw layer

| role | write policy |
|---|---|
| `system_process` (operator's ingestion adapter) | yes - the only writer. |
| every other role | no. The human writes paths are the manual_uploads connector (routed through normalization) and the manual_correction_log (audit-recorded, approval-gated). |

Raw is immutable after landing. Exceptions are listed in `reference/connectors/_core/layer_design.md` and carry their own approval gates.

### normalized layer

| role | write policy |
|---|---|
| `system_process` (normalization pass) | yes. |
| `compliance_risk` | manual override permitted under ApprovalRequest for PII redaction, classification change, legal hold flag. |
| `asset_mgmt` | manual override permitted under ApprovalRequest for master-data crosswalk correction, property-scope correction. |
| `finance_reporting` | manual override permitted under ApprovalRequest for financial mapping correction. |
| every other role | no direct write. Corrections route through the connector owner plus an ApprovalRequest. |

Every write produces a `manual_override_applied` audit entry with before-state and after-state references.

### derived layer

| role | write policy |
|---|---|
| `system_process` (derived recompute job) | yes, only after reconciliation passes and any required reference-refresh ApprovalRequest is approved. |
| every other role | no direct write. Derived is always recomputed from normalized; overrides are never applied to derived directly. |

## Structural artifact policy

Structural artifacts include manifests, mappings, entity contracts, reference tables, and classification declarations.

### manifests (`reference/connectors/<domain>/manifest.yaml`)

| role | policy |
|---|---|
| connector `owner` | may propose changes via PR. |
| `compliance_risk` | required reviewer for changes affecting auth_kind, classification, or PII touching fields. |
| `asset_mgmt` | required reviewer for changes to connectors touching portfolio scope. |
| `finance_reporting` | required reviewer for financial-domain connectors. |

Manifest changes always require schema conformance test pass plus secret-scan test pass plus human review per the relevant audiences.

### mappings (`reference/connectors/<domain>/mapping.yaml`)

Same policy as manifests.

### entity contracts and classifications

| role | policy |
|---|---|
| connector `owner` | proposes. |
| `compliance_risk` | required reviewer on any change to classification. |
| `compliance_risk` plus legal counsel | required reviewer on a classification downgrade. |

### reference tables (`reference/raw/`, `reference/normalized/`, `reference/derived/`)

Reference table contents are data, not structural artifacts. Read and write follow the layer policies above. Refresh of reference data at the derived layer requires ApprovalRequest per `approval_gates_for_integration_actions.md` entry one.

## Audit log policy

| role | policy |
|---|---|
| `system_process` (audit service) | exclusive writer. |
| `compliance_risk` | may read all records; may not edit or delete. |
| every audience | may read their own actor-scoped records; may not edit or delete. |
| `executive` | may read summary views; raw record reads require justification. |

Deletion of audit records is forbidden. See `audit_trail.md`.

## Approval policy - who may sign what

From `_core/approval_matrix.md` and `approval_gates_for_integration_actions.md`. Summary only; the source-of-truth lists live in those docs.

| gated action | required approvers (at minimum) |
|---|---|
| reference data refresh | compliance_risk + category-owning audience |
| master data crosswalk override | asset_mgmt + finance_reporting (financial) or regional_ops + compliance_risk (resident-linked) or asset_mgmt + construction (project) |
| schema change acknowledgment | connector owner + compliance_risk (if high or restricted class affected) |
| mapping override | connector owner + domain audience |
| PII classification downgrade | compliance_risk + legal counsel |
| legal hold release | compliance_risk + legal counsel |
| reference rollback | same as forward refresh |
| connector deprecation | connector owner + asset_mgmt + compliance_risk |
| production adapter activation | connector owner + compliance_risk + downstream-consuming audience |
| fair-housing-sensitive manual override | compliance_risk + legal counsel + regional_ops |

Single-audience approval is never sufficient for the actions above.

## Scope qualifiers

Read and write permissions apply within the actor's assigned scope:

- `portfolio_scope` - asset_mgmt, finance_reporting, compliance_risk (portfolio-level).
- `region_scope` - regional_ops.
- `property_scope` - site_ops, property-level compliance_risk.
- `project_scope` - development, construction.
- `global_scope` - executive, compliance_risk (when assigned).

Scope assignment is operator-owned and bound in the operator's identity provider.

## Enforcement

- The repo declares the policy.
- The operator's infrastructure enforces it (identity provider, storage permissions, API gateway, runtime authorization).
- Reviewers validate the operator's enforcement at audit time.
- `tests/test_boundary_rules.py` covers the policy boundaries that are mechanically checkable from repo content.

## Overlay behavior

Overlays may tighten the matrix above (more restrictive scope, more required approvers, additional reviewers for specific fields or connectors). Overlays may not loosen it. Boundary tests enforce this.

## Related

- `tailoring/AUDIENCE_MAP.md` - audience catalog.
- `security_model.md` - access_control layer overview.
- `masking_and_redaction.md` - render-time masking by class and audience.
- `audit_trail.md` - audit record access policy.
- `approval_gates_for_integration_actions.md` - full gated-action list.
- `unsafe_defaults_registry.md` - unsafe defaults adjacent to this policy.
