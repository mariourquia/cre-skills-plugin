# Security Testing Guidance - Mechanical Checks That Enforce the Model

This doc lists the mechanical tests that enforce the rules across this security subsystem. Some tests are already implemented in `tests/` under the residential_multifamily skill; others are planned and listed here so the next agent building the test harness knows what to add.

Every test here produces a deterministic pass or fail with a clear remediation path. Tests that require subjective judgment belong in review, not here.

## test - no secrets in repo (secret-scan)

- **Purpose.** Verify no file in the repo carries real credential material.
- **Scope.** Every text file under `src/skills/residential_multifamily/**`, with particular attention to manifests, mappings, overlays, samples, and fixtures.
- **Detection patterns.**
  - Token-shape regex set covering common API key prefixes, JWT signatures, OAuth tokens, AWS access keys, Azure service principal secrets, GitHub personal access tokens, Stripe keys, Slack tokens.
  - Entropy check on strings longer than 20 characters inside YAML and JSON values.
  - High-entropy detection inside `.env.example` files or comments.
  - Regex for real-looking URLs with path secrets (webhook patterns).
- **Allowlist.** The subsystem-level `.gitleaks.toml` allowlist for skill example/tailoring transcripts (see prior commit `debab2f`) covers synthetic sample content. Any new allowlist entry requires review.
- **Pass condition.** Zero findings after allowlist.
- **Remediation on fail.** Reject the commit. Rotate any matched credential. Shred the file per the raw-leak protocol in `reference/connectors/_core/layer_design.md` if the file was already committed. File ApprovalRequest per `secrets_handling.md`.

## test - no real PII in sample data (sample-scan)

- **Purpose.** Verify no sample payload in the repo carries content that could be real PII.
- **Scope.** Every `sample_input.json`, `sample_normalized.json`, `example_raw_payload.jsonl`, and test fixture under `src/skills/residential_multifamily/reference/connectors/**`; illustrative snippets inside any `.md` file under the same tree.
- **Detection patterns.**
  - SSN-shape regex `\d{3}-?\d{2}-?\d{4}`.
  - Routing-shape regex `\b\d{9}\b` (with bank-routing checksum validator if available).
  - Account-shape regex `\b\d{12,17}\b`.
  - EIN-shape regex `\d{2}-?\d{7}`.
  - Credit card shape (any length 12 to 19 passing Luhn).
  - Email addresses on non-reserved TLDs (`gmail.com`, `yahoo.com`, `outlook.com`, any real TLD that is not `.test`, `.example`, or `.invalid`).
  - Phone numbers outside the `+1-555-555-01xx` reserved range.
  - Addresses whose city and state match real US locations - this is a review-level check, not a strict regex, but samples using `Sample City / Example State / 00000` are safe.
  - Date-of-birth shapes - any field named `date_of_birth` or any birthdate-plausible date under a field present in a sample.
- **Pass condition.** Zero findings except for strings explicitly allowlisted as synthetic (see `pii_sample_policy.md` conventions).
- **Remediation on fail.** Replace with synthetic per `pii_sample_policy.md`. File ApprovalRequest if the leak was committed.

## test - manifest auth_kind is placeholder

- **Purpose.** Verify every connector manifest declares a placeholder `auth_kind`.
- **Scope.** Every `reference/connectors/<domain>/manifest.yaml`.
- **Detection.** Parse each manifest. Confirm `auth_kind` is present and belongs to the closed set declared in `secrets_handling.md` (`api_key_placeholder`, `oauth_placeholder`, `sftp_key_placeholder`, `mtls_placeholder`, `basic_auth_placeholder`, `email_inbox_placeholder`, `shared_drive_placeholder`, `tls_required_placeholder`, `none`).
- **Pass condition.** Every manifest has `auth_kind` set to a placeholder value.
- **Remediation on fail.** Update the manifest to use a placeholder. If the prior value was a real credential, follow the secret-leak protocol.

## test - config template has no populated credentials

- **Purpose.** Verify that manifests do not carry real values in any auth-related field.
- **Scope.** Same manifest set.
- **Detection.** Parse each manifest. For every field with an auth-related name (`api_key`, `client_secret`, `token`, `password`, `bearer_token`, `oauth_client_id`, `sftp_key`, `mtls_cert`, `service_token`), confirm the value is either absent or a placeholder-shaped string (e.g., `ENV_VAR_NAME_PLACEHOLDER`).
- **Pass condition.** No auth-related field carries a real value.
- **Remediation on fail.** Same as secret-scan fail.

## test - PII classification present for new fields

- **Purpose.** Verify that every field in every entity contract carries a declared classification.
- **Scope.** Every `reference/connectors/<domain>/schema.yaml` plus the `_schema/entity_contract.schema.yaml`.
- **Detection.** Parse each entity contract. For every field, confirm `classification` is present and belongs to the set `none`, `low`, `moderate`, `high`, `restricted`, or `forbidden_in_processed_output`.
- **Pass condition.** Every field has a classification.
- **Remediation on fail.** Add the classification per `pii_classification.md`. Update masking in `masking_and_redaction.md` if the class default does not apply.

## test - approval gate cannot be bypassed

- **Purpose.** Verify that integration-layer gated actions enforce an ApprovalRequest check.
- **Scope.** Every codepath in the operator's adapter reference patterns; every reference to a gated action in this repo.
- **Detection.** Static check against the action inventory in `approval_gates_for_integration_actions.md`. For each listed gated action, verify that there exists a lint rule or code contract that prevents execution without an approved ApprovalRequest.
- **Pass condition.** Every gated action has a corresponding check pattern.
- **Remediation on fail.** Add the check; re-route the action through the approval workflow; audit record any execution that occurred without the check.

## test - audit log immutability

- **Purpose.** Verify that the operator's audit implementation is append-only.
- **Scope.** Operator infrastructure; reviewed in incident review using the contract declared in `audit_trail.md`.
- **Detection.** Out-of-band audit: compare audit record hashes over time; any disappearance or mutation is a severity-one finding. Additionally, verify that the audit service identity is the only writer and that no human role has edit or delete permission on the audit log.
- **Pass condition.** No audit record has ever been edited or deleted.
- **Remediation on fail.** Engage compliance_risk and legal counsel. Forensic analysis of the mutation. Full review of the operator's audit stack.

## test - legal_hold flag respected

- **Purpose.** Verify that records flagged `legal_hold: true` are never overwritten, deleted, or exported without approval.
- **Scope.** Every code path that writes normalized, deletes records, or exports data.
- **Detection.** Unit test that simulates each operation against a fixture record with `legal_hold: true`; verify that the operation raises an error or routes to an ApprovalRequest. Integration test at the adapter level verifying the same end-to-end.
- **Pass condition.** Every write, delete, and export path checks `legal_hold`.
- **Remediation on fail.** Halt the offending code path; engage legal counsel; restore any affected records from backup; file incident.

## test - fair-housing posture (regulatory isolation)

- **Purpose.** Verify that no protected-class attribute or catalogued proxy is used as a match key, a routing key, or a feature in any codified workflow.
- **Scope.** Every entity contract, every mapping, every derived-feature declaration, every workflow routing rule.
- **Detection.** Static scan for field names matching the protected-class attribute list or the proxy list in `fair_housing_controls.md`. Any use as a key, join condition, or feature input is flagged.
- **Pass condition.** Zero flagged uses.
- **Remediation on fail.** Remove the offending use; update the workflow; file ApprovalRequest if the use reached production.

## test - overlay bounds (boundary tests)

- **Purpose.** Verify overlays satisfy the rules in `config_overlay_interaction.md`.
- **Scope.** Every overlay file composed with the canonical connector definitions.
- **Detection.** Run the nine boundary checks enumerated in `config_overlay_interaction.md` (schema_additive_only, mapping_not_modified, reconciliation_additive_only, reference_path_preserved, approval_not_loosened, classification_not_downgraded, no_secrets_in_overlay, no_real_pii_in_overlay_samples, fair_housing_forbidden_list_preserved).
- **Pass condition.** All nine checks pass.
- **Remediation on fail.** Reject the overlay. Guide the operator to the safe overlay patterns in `config_overlay_interaction.md`.

## test - masking matrix coverage

- **Purpose.** Verify that every canonical field has a defined masking transform for every canonical audience.
- **Scope.** `masking_and_redaction.md` matrix plus per-field overrides in `pii_classification.md`.
- **Detection.** Parse both docs; for every `(field, audience)` pair, confirm a transform is resolvable from the matrix plus overrides.
- **Pass condition.** No unresolved cells.
- **Remediation on fail.** Add the missing rule.

## test - debug-log PII scrubbing

- **Purpose.** Verify that log statements do not carry unmasked moderate-or-higher class PII.
- **Scope.** Code paths in the operator's adapter; reviewable patterns in this repo's example snippets.
- **Detection.** Lint or grep scan for log statement bodies that reference PII-shaped strings or PII-classified field names. Runtime log scrubbing is operator-owned and audited.
- **Pass condition.** No log statement emits unmasked PII.
- **Remediation on fail.** Replace with masked form or remove the log line; scrub any prior logs that captured the leak.

## test - no default autonomy on manual_override_applied

- **Purpose.** Verify that `manual_override_applied` audit events always carry a named human actor.
- **Scope.** Audit service contract; adapter codepaths that write override events.
- **Detection.** Audit-schema validation; lint rule on adapter code.
- **Pass condition.** Every `manual_override_applied` record has `actor != system_process`.
- **Remediation on fail.** Reverse the override; file incident.

## test - retention job honors legal hold

- **Purpose.** Verify that the retention-deletion job skips records with `legal_hold: true`.
- **Scope.** Operator's retention job.
- **Detection.** Fixture test: a retention job run against a dataset containing legal-hold records must not modify or delete them.
- **Pass condition.** Legal-hold records untouched.
- **Remediation on fail.** Halt the retention job; restore from backup; file incident; legal counsel notification.

## Test inventory - planned vs implemented

| test | implementation status | location |
|---|---|---|
| no secrets in repo | implemented (gitleaks) | repo CI |
| no real PII in sample data | planned | `tests/test_connector_contracts.py` extension |
| manifest auth_kind is placeholder | planned | `tests/test_connector_contracts.py` extension |
| config template has no populated credentials | planned | `tests/test_connector_contracts.py` extension |
| PII classification present for new fields | planned | `tests/test_connector_contracts.py` extension |
| approval gate cannot be bypassed | planned | `tests/test_connector_contracts.py` extension |
| audit log immutability | operator-owned review | out-of-band audit |
| legal_hold flag respected | planned | adapter-level fixture tests |
| fair-housing posture (regulatory isolation) | existing | `tests/test_regulatory_isolation.py` |
| overlay bounds | existing | `tests/test_boundary_rules.py` |
| masking matrix coverage | planned | doc-parse test |
| debug-log PII scrubbing | operator-owned | runtime middleware |
| no default autonomy on manual_override_applied | planned | adapter-level test |
| retention job honors legal hold | operator-owned | retention-job test |

Tests marked `planned` are the backlog for the test-harness agent. The contract they enforce is already binding; the mechanical check simply has not been wired yet.

## Related

- `secrets_handling.md`
- `pii_classification.md`
- `pii_sample_policy.md`
- `masking_and_redaction.md`
- `approval_gates_for_integration_actions.md`
- `config_overlay_interaction.md`
- `unsafe_defaults_registry.md`
- `audit_trail.md`
- `legal_hold_and_retention.md`
- `fair_housing_controls.md`
