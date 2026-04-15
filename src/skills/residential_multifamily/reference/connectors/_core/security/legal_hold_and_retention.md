# Legal Hold and Retention - How the Integration Layer Respects Holds and Retention Policy

Every record in the integration layer carries a classification (`pii_classification.md`) and a retention posture. The retention posture is qualitative in this subsystem; numeric retention horizons are operator-set in the operator's records management policy and not stated in prose here.

A legal hold overrides the default retention posture. A record under legal hold is read-only, non-overwriteable, non-deletable, and retained for the duration of the hold plus any statutory extension.

## Retention classes - qualitative

Five retention-posture classes. Each record inherits a posture from its field set.

- **ephemeral** - lands in raw and normalizes immediately; raw retained only for the audit trail. Operational data that is superseded by each refresh, where prior versions have no audit value (for example, a current-price snapshot that is recomputed daily).
- **operational** - retained for the operator's ordinary operational horizon. Covers routine PMS, GL, AP, CRM records.
- **extended** - retained for the operator's extended records-management horizon. Covers high-class fields and financial records.
- **legal** - retained for the longest applicable horizon declared in the operator's records policy. Covers restricted-class fields and legal-sensitive narratives.
- **indefinite** - never deleted. Covers audit logs (see `audit_trail.md`) and records under active or historical legal hold.

No numeric year value appears in prose here. Operators declare numeric horizons in their records-management policy outside the repo.

## Default retention by field class

From the taxonomy in `pii_classification.md`:

- `none`, `low` → `operational`
- `moderate` → `operational`
- `high` → `extended`
- `restricted` → `legal`
- audit log record → `indefinite`
- record under legal hold → `indefinite` for the duration of the hold

## Legal hold - flag and workflow

Every normalized record carries a boolean `legal_hold` flag. The flag is set by a legal-hold event through the following workflow:

1. A legal-hold event enters the system. Events may originate from compliance_risk (internal notice), from legal counsel (external notice such as preservation demand), or from a regulator (subpoena, litigation hold).
2. The event materializes an ApprovalRequest with `subject_object_type: policy_exception` (until a dedicated legal-hold subject type is added to `_core/schemas/approval_request.yaml`) citing the scope of the hold.
3. The hold's scope is encoded as a scope expression - a set of predicates over record attributes (for example, all records tied to a given property, a given resident, a given date range, a given vendor).
4. The compliance_risk audience and a named legal-counsel approver must both sign the ApprovalRequest.
5. Upon approval, the adapter stamps `legal_hold: true` on every matching record in normalized. Raw is already immutable; the hold does not change raw's posture but binds its retention to `indefinite`.
6. Records matching the scope expression that land after the hold receive the flag at ingestion time. The adapter checks the live hold scope set against every incoming record.

## Hold-state behavior

A record with `legal_hold: true`:

- **Read-only.** No normalized field may be overwritten. Late-arriving superseding records from raw are appended as versioned rows rather than overwrites.
- **Masking unchanged-or-more-restrictive.** The masking posture in `masking_and_redaction.md` applies; legal hold may tighten masking (for example, to prevent disclosure during active litigation) but never loosens it.
- **Audit-visible.** Every read against a legal-hold record writes an audit entry with `operation: legal_hold_read`. The audit entry captures the actor and the reason token.
- **Extended retention.** The record inherits `indefinite` retention. Normal deletion workflows skip it.
- **No bulk export.** Automated bulk export workflows exclude legal-hold records by default. Export of a legal-hold record requires an ApprovalRequest routed to compliance_risk plus legal counsel.

## Hold release

A legal hold is released only by an ApprovalRequest that:

- References the original hold ApprovalRequest.
- Cites the statutory or litigation event that terminates the hold (case closed, statute of limitations expired, preservation demand withdrawn).
- Is approved by compliance_risk plus a named legal-counsel approver.

Release sets `legal_hold: false` on the matched records. Release does not trigger deletion automatically; records revert to their field-class retention posture and are subject to ordinary retention enforcement from the release date forward.

Release is a gated action itself - see `approval_gates_for_integration_actions.md` entry on legal hold release.

## Deletion protocol

Ordinary deletion follows this ordering:

1. Retention policy identifies a record eligible for deletion.
2. The adapter checks `legal_hold`. If true, deletion is blocked.
3. The adapter checks the audit log. If the record is cited by any audit entry under active retention, deletion is blocked.
4. The adapter creates a deletion proposal. Deletion of individual records under operational or extended retention requires a compliance_risk signoff gate. Bulk deletion of a retention cohort requires an ApprovalRequest.
5. Upon approval, the record is deleted from normalized and from derived. Raw retains the record; raw redaction requires the exception protocol in `reference/connectors/_core/layer_design.md` (Layer one - raw, exception 1).
6. The audit log retains an entry for the deletion itself; audit entries are never deleted.

The audit log follows `indefinite` retention. A deletion of an audit entry would itself be an audit-worthy event and is forbidden by the `audit_trail.md` append-only contract.

## Fair-housing and legal hold

Fair-housing complaint narratives (`fair_housing_complaint_detail`) are `restricted`, `legal` retention by default, and `legal_hold capable` - meaning any such record may be flagged for hold at the operator's discretion even in the absence of an active litigation event, because fair-housing matters frequently yield preservation obligations later. The conservative posture is to treat fair-housing complaint narratives as on legal hold by default and require an ApprovalRequest to release.

## Interaction with raw immutability

Raw is immutable after landing (`reference/connectors/_core/layer_design.md`, Layer one - raw). Legal hold does not modify raw; it binds raw to `indefinite` retention and blocks the two exceptions to raw immutability from applying without additional approval:

- Exception 1 (legal retention policy removal of PII) is overridden by an active legal hold on the same record. Removal waits for the hold to release.
- Exception 2 (secret leakage) remains permitted under legal hold because the harm of an unredacted secret outweighs the hold's read-only posture; the redaction is still logged and still requires approval.

## Operator-owned elements

The repo declares the posture. The operator owns:

- Numeric retention horizons.
- Records-management policy governance.
- The physical deletion mechanism.
- The physical backup and restore cycle (including how holds interact with backups).
- The hold registry storage (outside the repo).
- Integration with the operator's e-discovery tooling.

## Related

- `_core/schemas/approval_request.yaml` - approval schema.
- `_core/approval_matrix.md` - canonical gated-action floor.
- `audit_trail.md` - audit record schema and retention.
- `pii_classification.md` - field classes and `legal_hold_capable` flag.
- `fair_housing_controls.md` - fair-housing-complaint posture.
- `approval_gates_for_integration_actions.md` - legal hold release as a gated action.
- `reference/connectors/_core/layer_design.md` - raw-layer immutability and its exceptions.
