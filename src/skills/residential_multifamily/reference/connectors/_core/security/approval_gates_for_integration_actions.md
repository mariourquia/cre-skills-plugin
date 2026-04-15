# Approval Gates for Integration Actions - Regardless of Automation

The canonical approval floor lives in `_core/approval_matrix.md` and covers subsystem-level actions (eviction, lease deviation, draw release, investor submission, and so on). This doc enumerates the integration-layer actions that materialize an ApprovalRequest conforming to `_core/schemas/approval_request.yaml` regardless of how automated the underlying connector or adapter is.

Every action below is gated. Automation may draft, propose, and queue; automation may not approve. Approval requires a named human actor in each listed approver audience.

## Gated integration-layer actions

### one - reference data refresh

- **Action.** Promote a new reference-data vintage into `reference/derived/`. Covers market rents, concessions, staffing ratios, material costs, labor rates, turn cost library, capex library, schedule duration assumptions, utility benchmarks, vendor rate cards, approval thresholds, screening policies.
- **Approver audience.** `compliance_risk` plus the audience that owns downstream metrics for the refreshed category (for example, `finance_reporting` for rate cards, `asset_mgmt` for capex library).
- **Escalation.** If the refresh would move a derived benchmark by more than the sensitivity threshold declared in the reference category's contract, escalate to add `executive`.
- **Documentation.** ApprovalRequest carries `subject_object_type: policy_exception` (until a dedicated `reference_refresh` subject type is added to `_core/schemas/approval_request.yaml`), the category slug, the source of the new vintage, the rationale, and the rollback pointer.

### two - master data crosswalk override

- **Action.** Override the master-data crosswalk that maps raw source keys to canonical identifiers (property, vendor, account, employee).
- **Approver audience.** `asset_mgmt` plus `finance_reporting` for financial crosswalks; `regional_ops` plus `compliance_risk` for resident-linked crosswalks; `asset_mgmt` plus `construction` for project crosswalks.
- **Escalation.** Overrides affecting more than one property require `asset_mgmt` plus regional audience.
- **Documentation.** ApprovalRequest cites prior crosswalk, new crosswalk, and the reason. Audit record captures before-state and after-state references.

### three - schema change acknowledgment

- **Action.** Acknowledge an upstream-source schema change (new required field, removed field, changed type, enum expansion) and update the entity contract under `reference/connectors/<domain>/schema.yaml`.
- **Approver audience.** The connector's `owner` plus `compliance_risk` if the change introduces a field of class `high` or `restricted`; `asset_mgmt` plus `finance_reporting` for financial domains.
- **Escalation.** Schema change that removes a required canonical field requires `executive` approval because derived metric definitions may break.
- **Documentation.** ApprovalRequest cites the before-contract and after-contract file paths. Change-log entry per `_core/change_log_conventions.md`.

### four - mapping override

- **Action.** Override the default `mapping.yaml` applied during raw-to-normalized transformation.
- **Approver audience.** Connector `owner` plus `compliance_risk` if the override affects a field of class `high` or `restricted`; `finance_reporting` plus `asset_mgmt` for financial mappings.
- **Escalation.** Overrides with backward-incompatible effect on derived metrics require `executive` approval.
- **Documentation.** ApprovalRequest captures the before-mapping, the after-mapping, and the expected impact on downstream metrics.

### five - PII classification downgrade

- **Action.** Downgrade a field's classification in `pii_classification.md` (for example, moving a field from `high` to `moderate`, or from `restricted` to `high`).
- **Approver audience.** `compliance_risk` plus a named legal-counsel approver. For downgrades involving resident-identifying or employee-identifying fields, add `asset_mgmt`.
- **Escalation.** Downgrades of `restricted`-class fields require executive approval in addition to compliance_risk and legal counsel.
- **Documentation.** ApprovalRequest cites the prior classification, the proposed classification, the justification referencing statute or case change, and the impact on the masking matrix. Change-log entry required.

### six - legal hold release

- **Action.** Remove `legal_hold: true` from records previously flagged.
- **Approver audience.** `compliance_risk` plus named legal-counsel approver.
- **Escalation.** Release affecting records tied to a regulatory investigation requires additional documentation referencing the investigation close.
- **Documentation.** ApprovalRequest cites the original hold ApprovalRequest, the termination event (case close, statute expiration, demand withdrawal), and the scope of records affected. Audit records are written for each record unflagged.

### seven - reference rollback

- **Action.** Roll back a previously approved reference-data refresh.
- **Approver audience.** Same approver audience that approved the forward refresh; plus `compliance_risk` for any rollback that would revert a classification or policy change.
- **Escalation.** Rollbacks that would invalidate prior lender or investor submissions require `executive` approval and coordination with the relevant finance_reporting and asset_mgmt audiences.
- **Documentation.** ApprovalRequest cites the forward ApprovalRequest being rolled back, the post-forward events that motivate rollback, and the blast radius on downstream metrics.

### eight - connector deprecation

- **Action.** Change a connector's status from `stable` to `deprecated`.
- **Approver audience.** Connector `owner` plus `asset_mgmt` plus `compliance_risk`.
- **Escalation.** Deprecation of a connector that feeds a currently-active regulatory or investor report requires `executive` approval plus a transition plan for the dependent reports.
- **Documentation.** ApprovalRequest cites the replacement connector (if any) and the transition plan. Change-log entry required.

### nine - production adapter activation

- **Action.** Move a connector from `stub` or `draft` status to `stable` and activate a production adapter against it.
- **Approver audience.** Connector `owner` plus `compliance_risk` plus the audience that owns downstream consumption.
- **Escalation.** Activation of a connector that ingests `high`-class or `restricted`-class fields (such as a screening-vendor connector) requires `compliance_risk` and a named legal-counsel approver, plus a pre-activation run through `security_testing_guidance.md`.
- **Documentation.** ApprovalRequest captures the adapter version, the operator environment, the secret backend binding (reference only, no values), and the go-live checklist result.

### ten - fair-housing-sensitive manual override

- **Action.** Apply a manual override to a record tagged `fair_housing_sensitive` in the exception taxonomy.
- **Approver audience.** `compliance_risk` plus named legal-counsel approver; plus the property's `regional_ops` audience for context.
- **Escalation.** Overrides involving denial, non-renewal, or eviction outcomes require `executive` approval.
- **Documentation.** ApprovalRequest cites the exception id, the protected-class risk the exception raised, the proposed resolution, and the audit record planned for post-approval action. Audit record is written at resolution with `operation: manual_override_applied` and `reason_code: fair_housing_sensitive_resolution`.

## Generic rules for every gated action

### rule one - ApprovalRequest conformance

Every gate above materializes an ApprovalRequest conforming to `_core/schemas/approval_request.yaml` with the required fields populated:

- `approval_request_id`
- `created_at`, `created_by`
- `subject_object_type` (selected from the schema enum; if the match is `policy_exception`, the rationale field clarifies the specific integration-layer subject)
- `subject_object_id`
- `action_proposed`
- `rationale`
- `approvers_required` (listing every role from the action's approver audience)
- `status` (begins `proposed`; advances to `approved` only after all required approvers sign)

### rule two - two-person integrity where listed

Actions listing more than one approver audience require distinct human approvers. A single actor may not satisfy both roles even if they hold both audience memberships.

### rule three - no pre-approval

Actions are not pre-approved by category. Every action materializes its own ApprovalRequest at the time of the action.

### rule four - approval expiration

Approved ApprovalRequests expire if not acted upon within the operator-defined validity window (operator-set; no numeric horizon in prose here). Expired requests require re-approval before the action may execute.

### rule five - approval revocation

Any approver in the required set may revoke their signature before the action executes. Revocation returns the request to `proposed` and blocks execution.

### rule six - automation may draft

Automation may prepare the ApprovalRequest, populate every field except `approvers_required`'s signature block, and attach supporting artifacts. Automation may not sign.

### rule seven - audit record on every transition

Every ApprovalRequest state transition (created, approved, rejected, withdrawn, revoked, expired) writes an audit record with `operation: approval_action` per `audit_trail.md`.

## Overlay behavior

Overlays may tighten these gates - add approver audiences, shorten validity windows, require additional documentation. Overlays may not loosen the canonical list above. Tests in the boundary-rule set (`tests/test_boundary_rules.py`) enforce that overlay-declared gates never drop below canon.

## Related

- `_core/approval_matrix.md` - canonical subsystem-level gated actions.
- `_core/schemas/approval_request.yaml` - approval schema.
- `audit_trail.md` - audit records for approval transitions.
- `unsafe_defaults_registry.md` - default behaviors that would bypass these gates.
- `legal_hold_and_retention.md` - legal-hold interactions with the gates above.
- `fair_housing_controls.md` - fair-housing-specific approval posture.
- `security_testing_guidance.md` - tests that verify gates cannot be bypassed.
