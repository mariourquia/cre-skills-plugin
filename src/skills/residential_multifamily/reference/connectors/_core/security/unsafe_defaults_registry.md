# Unsafe Defaults Registry - Configurations Forbidden as Defaults

A default is the value a system produces when no one configures it. In a CRE integration layer, a careless default can cost residents their housing, expose the operator to fair-housing liability, or leak PII to people who should never see it. This registry enumerates configurations that are forbidden as defaults regardless of apparent convenience.

For each entry: the forbidden default, why it is unsafe, the detection rule, and the remediation.

## one - default credentials in a config template

- **Forbidden default.** Manifests and config templates ship with real credential values under any field (api_key, client_secret, password, bearer_token, oauth_client_id, sftp_key, mtls_cert, service_token).
- **Why unsafe.** Real credentials in a repo leak to anyone with read access, every past clone, every mirror, and every future fork. Rotation does not undo the leak of prior values.
- **Detection.** Secret-scan test in `security_testing_guidance.md`; manifest-schema validation that `auth_kind` is a placeholder value; reviewer check for any non-placeholder under auth-related keys.
- **Remediation.** Reject the merge. Rotate the exposed credential. Shred the file per the raw-leak protocol in `reference/connectors/_core/layer_design.md` if the file was committed. File an ApprovalRequest per `secrets_handling.md` leakage protocol.

## two - silent bypass of a data-quality blocker

- **Forbidden default.** A reconciliation check declared as `blocker` promotes to derived without human approval when the check fails.
- **Why unsafe.** Downstream metrics consume broken data. The downstream audience trusts the metric because the UI shows "reconciled." The operator has silently turned the gate off.
- **Detection.** `tests/test_connector_contracts.py` verifies that a `blocker` check always halts promotion until an ApprovalRequest is approved; the approval_action carries a coded reason.
- **Remediation.** Block the promotion. File an ApprovalRequest with `subject_object_type: policy_exception`. Route to compliance_risk plus the owning domain lead.

## three - auto-approve of any approval_floor action

- **Forbidden default.** An integration-layer action listed in `_core/approval_matrix.md` as a gated action is executed by the adapter without materializing an ApprovalRequest.
- **Why unsafe.** The canonical approval floor is the operator's guarantee to ownership, lenders, and residents that certain decisions require human judgment. Automation below the floor violates that guarantee.
- **Detection.** `approval_gates_for_integration_actions.md` enumerates integration-layer gated actions; `tests/test_connector_contracts.py` verifies that any codepath that would execute one of those actions first checks for a valid approved ApprovalRequest.
- **Remediation.** Halt the action. File an incident. Audit record the attempted bypass. Engage compliance_risk.

## four - fair-housing-sensitive exception silently resolved

- **Forbidden default.** An exception tagged `fair_housing_sensitive` in the exception taxonomy is marked resolved by an automated rule.
- **Why unsafe.** Fair-housing exceptions require compliance review and legal context. Silent resolution removes the opportunity for that review and produces no audit trail to reconstruct later.
- **Detection.** Monitoring-layer rule that `fair_housing_sensitive` exceptions never close without an `approval_action` audit record; `tests/test_regulatory_isolation.py` covers fair-housing posture more broadly.
- **Remediation.** Reopen the exception. Route to compliance_risk. File an ApprovalRequest for resolution.

## five - reference data refresh without approval

- **Forbidden default.** A reference-data refresh (market rents, concessions, staffing ratios, material costs, labor rates, turn cost library, capex library, schedule duration assumptions, utility benchmarks, vendor rate cards, approval thresholds, screening policies) is applied to the derived layer without an ApprovalRequest.
- **Why unsafe.** Reference-data changes move every downstream number. A silent refresh means the next report is computed against values nobody reviewed. Lender and investor submissions go out against unreviewed assumptions.
- **Detection.** `approval_gates_for_integration_actions.md` declares reference refresh as gated; `tests/test_connector_contracts.py` checks that derived recomputes reference a valid approved ApprovalRequest.
- **Remediation.** Rollback the refresh. File an ApprovalRequest for the refresh. Re-apply after approval.

## six - PII in sample data

- **Forbidden default.** A sample payload committed to the repo carries real names, real emails, real phones, real addresses, real SSNs, real DOBs, real tenant ids, or real vendor names.
- **Why unsafe.** Real PII in a repo is a data breach the moment the repo is cloned or mirrored. Operators, reviewers, and external auditors may all see the repo; none of them are authorized to see real resident data.
- **Detection.** Sample-scan test in `security_testing_guidance.md`; reviewer check against the checklist in `pii_sample_policy.md`.
- **Remediation.** Replace with synthetic values using the conventions in `pii_sample_policy.md`. If the real PII was already committed, follow the leakage protocol (rotate is not applicable to PII; the remediation is notice, redaction-stub of the raw file per `reference/connectors/_core/layer_design.md` exception one, and potentially legal review).

## seven - real credentials in repo

- **Forbidden default.** Any real credential exists in any file in the repo, including in comments, in example `.env` files with real values, in test fixtures, in commit messages, in screenshot attachments, or in terminal recordings.
- **Why unsafe.** Same rationale as entry one; stated broader here because this forbids real credentials anywhere in the repo surface area, not just in manifests.
- **Detection.** Secret-scan test run at pre-commit, at PR, and over the full history on demand.
- **Remediation.** Rotate. Shred per the leakage protocol. File ApprovalRequest.

## eight - logging PII at debug level

- **Forbidden default.** Adapter or connector code emits log lines at debug level (or any level) that include moderate-or-higher class PII in readable form.
- **Why unsafe.** Debug logs land in monitoring systems, aggregation pipelines, and developer laptops. A debug-level PII log is a PII leak into every environment downstream of the logger.
- **Detection.** Reviewer check against the log-scrubbing rule; planned grep test that flags PII-shaped strings in log-statement bodies; runtime log-scrubbing middleware (operator-owned).
- **Remediation.** Remove the log line or replace with a masked form following `masking_and_redaction.md`. Scrub any logs that already captured the leak.

## nine - default masking off for resident-facing outputs

- **Forbidden default.** A renderer emits output to a resident-facing destination (communication, notice, letter) with masking turned off and full unmasked PII inline, because the workflow did not declare the destination.
- **Why unsafe.** Masking defaults depend on the destination. A renderer that lacks a destination should refuse to render, not default to unmasked. A resident may receive their neighbor's private data; legal and reputational harm is direct.
- **Detection.** Render-time contract: every render call requires a declared audience; missing audience raises an error rather than defaulting to full. Test in the renderer layer (operator-owned).
- **Remediation.** Halt the render path. Declare the audience. Default to the most restrictive matrix cell when the audience is ambiguous.

## ten - default autonomy on manual override workflows

- **Forbidden default.** A manual_override_applied event executes without a named human actor.
- **Why unsafe.** "Manual override" by an automated process is not a manual override - it is an unlogged change. Auditors cannot reconstruct intent.
- **Detection.** Audit-schema check that `manual_override_applied` events carry a non-system actor; reviewer check.
- **Remediation.** Reverse the override. Require a named human approver.

## eleven - default retention shorter than legal hold

- **Forbidden default.** Records under legal hold are deleted by the default retention job.
- **Why unsafe.** Legal hold is a preservation obligation. Violating the hold is sanctionable and exposes the operator to liability.
- **Detection.** Retention job contract: check `legal_hold` before deletion; test in the retention layer (operator-owned). The retention-layer check is enumerated in `legal_hold_and_retention.md`.
- **Remediation.** Suspend the retention job. File an ApprovalRequest. Restore from backup if any hold-flagged record was deleted. Engage legal counsel.

## twelve - default classification missing on a new field

- **Forbidden default.** A new field enters an entity contract without a classification declared.
- **Why unsafe.** Unclassified fields default to `none` in the absence of declaration, which is wrong for any new PII. The system treats the field as safely renderable when it may be highly sensitive.
- **Detection.** `tests/test_connector_contracts.py` rejects entity contracts missing classification on any field.
- **Remediation.** Add a classification per `pii_classification.md`. Update mapping and masking per `masking_and_redaction.md` if the class differs from its default.

## thirteen - default approval routing to a single approver

- **Forbidden default.** A gated action routes to a single approver for a decision that canon requires dual approval (`_core/approval_matrix.md` lists minimum approvers per action).
- **Why unsafe.** Single-approver routing loosens the canonical floor. Collusion risk rises; bus-factor risk rises.
- **Detection.** ApprovalRequest schema enforces `approvers_required` per action; `tests/test_connector_contracts.py` checks the routing logic against the matrix.
- **Remediation.** Add the missing approver role. Re-route the pending request.

## fourteen - default propagation of failed upstream reconciliation

- **Forbidden default.** A failed reconciliation check does not block downstream workflows that depend on the reconciled dataset.
- **Why unsafe.** A broken number propagates. Every decision taken against the broken dataset during the propagation window is a decision made against a value that failed its own quality gate.
- **Detection.** Workflow contract: workflows declare upstream reconciliation dependencies and refuse to trigger when a dependency is in `reconciliation_blocker_raised` state.
- **Remediation.** Halt the dependent workflow. Resolve the reconciliation blocker (with ApprovalRequest if required). Restart.

## fifteen - default silent schema drift acceptance

- **Forbidden default.** A schema change in an upstream source (new required field, removed field, changed field type) is accepted silently by the adapter and propagated into normalized.
- **Why unsafe.** The operator's assumption about the entity contract is violated without notice. Derived metrics computed against the new shape may be wrong.
- **Detection.** Schema-change detection at the adapter layer; change triggers `schema_change_acknowledged` event which requires an ApprovalRequest.
- **Remediation.** Quarantine incoming data against the new schema. File an ApprovalRequest. Update the entity contract in a change-log entry. Re-run reconciliation.

## Related

- `security_testing_guidance.md` - the mechanical checks that catch the detections listed here.
- `pii_classification.md` - classification rules.
- `masking_and_redaction.md` - masking rules the default-off entries reference.
- `approval_gates_for_integration_actions.md` - the gated-action list this registry refers to.
- `audit_trail.md` - the audit log the registry depends on for detection.
- `_core/approval_matrix.md` - the canonical approval floor.
