# Runbook: Fair-Housing-Sensitive Flag

status_tag: reference

Any exception touching fair-housing-sensitive fields, screening data, demographic indicators, protected-class proxies, accessibility accommodations, occupancy-restriction signals, triggers immediate containment and legal review.

## 1. Trigger

- Exception of category `fair_housing_sensitive` in the queue.
- Any alert whose `trigger_condition` references a screening, demographic, or protected-class field.
- Any schema-drift or mapping-override request that would change the handling of such fields.
- Any workflow activation that encountered a fair-housing-sensitive field in a context where the field should not have been visible.

## 2. Symptoms

- Field-level warning from the connector's mapping engine that a sensitive field is being transformed or emitted.
- Screening workflow produces an output that appears correlated with a protected-class proxy.
- A pattern of concession decisions or unit assignments looks demographically skewed during review.
- Resident communication drafts reference a protected-class term inappropriately.

## 3. Likely causes (ranked)

1. Upstream system exposed a field that should not cross the connector boundary.
2. Mapping inadvertently routed a free-text field (preferences, notes) containing sensitive content into a structured destination.
3. Screening policy drift, an overlay or org override introduced a criterion that correlates with a protected class.
4. Data entry by a site operator that recorded protected-class information in a note field.
5. False positive, the flag fired but the field in context is not sensitive (still treat as if sensitive until confirmed).

## 4. Immediate actions (minute-by-minute, numbered)

1. Containment first. Halt any workflow currently executing against the affected records. Halt any draft communication referencing the fields. Hold raw and normalized records in place; do not delete.
2. Do not escalate through broadcast channels. Fair-housing-sensitive incidents use a narrow, named distribution: `compliance_risk`, `legal_counsel`, and the specific `data_owner` and `business_owner` for the source. No all-hands messages, no broad Slack-style channels. See `../monitoring/alert_channel_design.md` for the restricted-channel pattern.
3. Confirm the category. If the incident is confirmed fair-housing-sensitive, file the audit-log entry immediately with the restricted label. If the flag is a false positive, still file an audit-log entry noting the investigation and outcome.
4. Identify affected records. List the fields, the affected property or properties, the affected resident accounts (by internal id only, no PII in downstream notes), and the time window.
5. Legal review per `_core/approval_matrix.md` row 3 (tenant dispute with legal exposure) and row 4 (human-approval-required policy overlay). `legal_counsel` must sign off on remediation, communication, and any downstream action involving the records.
6. Halt dependent workflows for the scope in question:
   - `lead_to_lease_funnel_review` screening branches.
   - `renewal_retention` decisions that used the field.
   - `delinquency_collections` decisions that used the field.
   - `move_in_administration` scoring.
   - `third_party_manager_scorecard_review` segments affected by the data.
7. Apply the fix under legal direction: redact the field, update the mapping to exclude it, correct the upstream policy, or (if the field must remain) tighten access controls and add a compensating control.
8. Document the incident in the restricted audit log. Retain the entry per the retention policy set by `legal_counsel`; this record is never truncated by routine log rotation.

## 5. Escalation path

- Do not follow the standard escalation chain for this category.
- First responder: `on_call_ops` stops at containment and immediately pages `compliance_risk` and `legal_counsel`.
- `compliance_risk` and `legal_counsel` are the sole decision authorities for proceeding.
- `executive` is briefed on any incident that reaches the legal-review stage.
- No broader audience is informed without `legal_counsel` authorization.
- Fair-housing escalations automatically cross the `executive_review_always` tier in `_core/approval_matrix.md`.

## 6. Affected workflows

Any workflow that touches screening, demographic, accessibility, or protected-class data. Specifically:

- `lead_to_lease_funnel_review` (screening decisions).
- `renewal_retention` (renewal decisions).
- `delinquency_collections` (payment plan decisions).
- `move_in_administration` (reasonable-accommodation handling).
- `move_out_administration` (dispute resolution).
- `third_party_manager_scorecard_review` (manager-level fair-housing oversight).
- Any template or communication-drafting workflow that referenced the field.
- Any executive-facing report that aggregated across the field.

## 7. Recovery steps

- Apply legal-directed remediation.
- Reopen halted workflows only after `compliance_risk` and `legal_counsel` sign off.
- Update connector contracts: if the sensitive field should never cross the boundary, tighten `mapping.yaml` and `schema.yaml` to exclude it; add a test under `tests/test_connector_contracts.py` that fails if the field reappears.
- Retrain overlays: if an overlay caused the issue, correct the overlay and re-run the affected workflows.
- Notify residents only under `legal_counsel` direction; the system does not draft or send resident communications about the incident without counsel approval.

## 8. Verification steps

- Restricted audit log entry exists and is complete.
- Remediation is in place and tested.
- Connector boundary test for the sensitive field passes.
- `compliance_risk` and `legal_counsel` have signed off on recovery.
- No residual records in the affected window carry the exposed field in a downstream location.

## 9. Post-incident review hooks

- Restricted post-incident review attended by `compliance_risk`, `legal_counsel`, affected `data_owner`, and `executive`.
- Review is not recorded in routine operational logs; it is filed in the compliance-restricted archive.
- Pattern monitoring: if similar incidents recur, `compliance_risk` commissions a structural audit of all connectors and overlays that touch protected-class-adjacent fields.
- Annual fair-housing program review pulls every flag raised in the prior year, regardless of severity, and confirms every open corrective action is closed.
- No runbook in this directory lowers the escalation chain for this category; only the canonical approval matrix governs.
