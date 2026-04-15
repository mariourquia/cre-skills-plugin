# Secrets Handling - Credential Lifecycle Outside the Repo

No credentials in repo. Not in code. Not in YAML. Not in comments. Not in commit messages. Not in test fixtures. Not in sample files. Not in docs. No real hostname that implies a specific vendor tenant. No real API base URL that a scraper could harvest. No real SFTP address.

This doc defines the declarative posture every connector manifest adopts and the operator-owned lifecycle that binds real credentials at deploy time.

## Manifest auth_kind - closed placeholder set

Every connector manifest at `reference/connectors/<domain>/manifest.yaml` declares `auth_kind` from the closed set below. Tests at `tests/test_connector_contracts.py` reject a manifest with any other value.

| auth_kind | When to use | What the manifest carries |
|---|---|---|
| `api_key_placeholder` | REST API with single secret. | name of env var the operator will bind. No key. No header template that reveals prefix conventions specific to a vendor tenant. |
| `oauth_placeholder` | OAuth client_credentials or authorization_code flow. | names of env vars for client_id, client_secret, token_url. No values. |
| `sftp_key_placeholder` | SFTP drop with key-pair auth. | path to key reference; host placeholder `SFTP_HOST_PLACEHOLDER`; user placeholder. |
| `mtls_placeholder` | Mutual-TLS endpoint. | paths to cert and key references; CA bundle reference placeholder. |
| `basic_auth_placeholder` | Legacy basic auth (discouraged; allowed for deprecated sources). | env var names only. |
| `email_inbox_placeholder` | Mailbox that receives signed vendor reports. | mailbox address placeholder; token reference placeholder. |
| `shared_drive_placeholder` | Cloud shared drive drop. | drive id placeholder; service principal reference placeholder. |
| `tls_required_placeholder` | Generic HTTPS endpoint with operator-provided service token. | env var name for token; base URL placeholder. |
| `none` | File-drop only, no credential needed (manual upload). | no auth fields. |

A manifest with `auth_kind: none` is permitted only for `manual_uploads/` and for synthetic file-drop fixtures in tests.

## What the repo never contains

Forbidden content, enforced by the secret-scan test and by reviewers:

- Real API keys, tokens, secrets, passwords.
- Real OAuth client_id, client_secret, or tenant identifier.
- Real SFTP host, port, username, key material.
- Real SSL certificates or private keys.
- Real webhook URLs that contain secret tokens in path or query string.
- Real vendor-specific base URLs that reveal a live tenant.
- Real email inbox addresses that receive production data.
- Real cloud shared-drive identifiers tied to a live tenant.

A file that matches the secret-scan test is quarantined and not merged. See `security_testing_guidance.md` for the check set.

## Operator-owned credential lifecycle

Operators bind real credentials in their deployment environment, never in this repo. The lifecycle looks like:

1. **Template checkout.** Operator forks the canonical manifest from `reference/connectors/<domain>/manifest.yaml`.
2. **Environment-specific config.** Operator creates an environment-specific config outside the repo (example path pattern: `<operator_deployment>/envs/<env_name>/<connector_id>.yaml`) that binds the env-var names declared in the manifest to the operator's secret backend.
3. **Secret backend.** Operator selects a secret backend. The contract is backend-agnostic. Acceptable backends include:
   - Azure Key Vault
   - AWS Secrets Manager
   - Google Secret Manager
   - HashiCorp Vault
   - 1Password (via op-cli or SDK)
   - any FIPS-aligned equivalent the operator adopts
4. **Deploy-time binding.** At adapter start the runtime resolves env vars from the secret backend. The adapter reads the resolved values; it never writes them back to disk.
5. **Runtime posture.** Secrets are not logged. Not at info, not at debug, not at trace. See `unsafe_defaults_registry.md` entry on "logging PII at debug level" - the same rule applies to secrets.

## Rotation

Rotation cadence is operator-defined. The repo does not dictate a numeric cadence. It does require the following posture:

- **Rotation runbook pointer.** Operators maintain a rotation runbook keyed by connector_id at `reference/connectors/_core/runbooks/` (authored by a separate agent, not in this subsystem's scope). The runbook cites the secret backend, the env-var names, the rollback path, and the smoke-test the adapter runs after rotation.
- **Expiration monitoring.** Operators instrument secret backends to alert on upcoming expiration. Alerts route to the operator's monitoring stack; see `reference/connectors/_core/monitoring/` (authored separately) for the alert contract.
- **Grace period.** Rotating credentials should not break ingestion. The adapter supports dual-credential overlap during rotation windows; the manifest declares `supports_credential_overlap: true` when this is feasible for the source. Sources that do not support overlap (e.g., some SFTP daemons) declare `supports_credential_overlap: false` and the operator schedules a maintenance window.
- **Post-rotation validation.** After rotation the adapter runs a smoke handshake; on failure it quarantines to `_rejected/` and alerts.

## Secret leakage - incident protocol

If a credential is suspected leaked:

1. Rotate the leaked credential in the secret backend.
2. Revoke the leaked credential at the source (kill tokens, disable user, revoke key).
3. If the leak touched a file committed to the repo, follow the raw-file shred protocol defined in `reference/connectors/_core/layer_design.md` (section "Layer one - raw", exception 2 - confirmed secret leakage).
4. File an ApprovalRequest with `subject_object_type: policy_exception` and the compliance_risk audience.
5. Append a change-log entry per `_core/change_log_conventions.md`.
6. Run the secret-scan test set from `security_testing_guidance.md` over the full history; any additional findings escalate.

## Anti-patterns - enumerated

The following patterns are forbidden and caught by the secret-scan or reviewer:

- Base64-encoded credentials in repo under the assumption they are "encoded, not secret."
- Credentials in `.env.example` with real values (example files carry only names and placeholder values such as `<bind_at_deploy>`).
- Credentials in test fixtures, even when the test is skipped.
- Credentials in commit messages or PR descriptions.
- Credentials in screenshot attachments or terminal recordings included in the repo.
- URLs with secret tokens in the path (webhook-style secrets).
- Hardcoded default credentials in code or config templates.
- Real credential committed to a branch with the intent to "squash on merge."

## Relationship to manifest schema

The manifest schema (`reference/connectors/_schema/connector_manifest.schema.yaml`) enforces `auth_kind` as a required field. The secret-scan test enforces that no manifest carries real values under `auth_kind`. Together these two mechanisms form the mechanical floor; reviewers enforce the rest.
