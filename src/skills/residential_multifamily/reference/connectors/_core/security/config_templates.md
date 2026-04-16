# Config Templates - Manifests Ship Clean, Operators Populate Outside the Repo

Every connector ships its `manifest.yaml` as a template. The template declares the contract; it carries no real credentials, no real hostnames, no real property scope, no real cadence. The operator forks the template at deploy time and populates an environment-specific config outside the repo.

## Template shape

Every manifest at `reference/connectors/<domain>/manifest.yaml` conforms to `reference/connectors/_schema/connector_manifest.schema.yaml` and carries placeholder values for operator-bound fields.

Placeholder conventions:

- `source_name: SOURCE_NAME_PLACEHOLDER`
- `auth_kind: api_key_placeholder` (or another value from the closed set in `secrets_handling.md`)
- `cadence: CADENCE_PLACEHOLDER` (operator selects a cadence token such as `daily`, `weekly`, `monthly`, or `event_driven`)
- `property_scope: PROPERTY_SCOPE_PLACEHOLDER` (operator binds the list of property_id values at deploy time)
- `credential_reference: ENV_VAR_NAME_PLACEHOLDER` (operator replaces with the env-var name their secret backend exposes)
- `environment: ENVIRONMENT_PLACEHOLDER` (operator selects `development`, `staging`, or `production`)

A manifest containing any of those placeholder strings at the time of a deploy-time config check is rejected. A manifest with real values at merge time is rejected. The template is the canonical form in the repo; the populated form never enters the repo.

## Lifecycle

Three phases; each phase has distinct allowed contents.

### phase_one - template in repo

- Lives under `reference/connectors/<domain>/manifest.yaml`.
- Carries only placeholders for operator-bound fields.
- Conforms to the manifest schema (`reference/connectors/_schema/connector_manifest.schema.yaml`).
- Declares `vendor_neutral: true` and `status: stub` until a vendor adapter exists.
- Never carries real credentials, hostnames, tokens, URLs, property ids, or cadences.
- Merged through normal review; secret-scan and manifest-schema tests gate the merge.

### phase_two - environment-specific config, outside repo

- Lives in the operator's deployment artifacts, not in this repo.
- Typical path pattern: `<operator_deployment>/envs/<env_name>/<connector_id>.yaml`.
- Populates every placeholder with a real operator value.
- Binds `credential_reference` to the operator's secret backend (Azure Key Vault, AWS Secrets Manager, HashiCorp Vault, 1Password, etc. - see `secrets_handling.md`).
- Governed by the operator's configuration management, change control, and audit logging.
- Never committed back to this repo, even as example data.

### phase_three - deployed adapter reads env-bound config

- The adapter boots with the populated config as input.
- Env vars resolve from the secret backend at runtime, not at config-file write time.
- The adapter validates the config against the manifest template before first ingest. Any drift between the two fails the boot.
- Runtime diagnostics (logs, traces) must not echo the secrets or the credential_reference values. See `unsafe_defaults_registry.md`.

## Operator fork and populate - the handshake

Every manifest declares a `handshake` block. The handshake documents the operator's responsibility during fork:

- **Populate `source_name`** with a stable operator-chosen identifier. The label must not be a real vendor tenant id.
- **Populate `property_scope`** with the property_id list the adapter is authorized to ingest.
- **Populate `cadence`** with a scheduling token understood by the operator's runner.
- **Populate `environment`** with the deployment environment.
- **Populate `credential_reference`** with the env var name bound in the secret backend; do not populate the credential itself.
- **Run the manifest-schema test** after fork; if the populated config does not conform, the adapter is not started.
- **Run the secret-scan test** over the populated config; if a secret is detected in the populated file, the operator rotates the secret, removes it from the file, moves it to the secret backend, and retries.

## Config overlay interaction

Org overlays may parameterize the same manifest fields listed above but never alter the contract. Full rules in `config_overlay_interaction.md`. Summary:

- Allowed: overlays set source_instance identity (name, cadence, environment, credential reference, property scope).
- Forbidden: overlays modify schema, mapping transforms, reconciliation rules, or the normalized output shape.
- Forbidden: overlays remove canonical reference paths.
- Allowed: overlays add org-specific reference paths on top of canonical ones.

## Synthetic configs for tests

Test fixtures that simulate a populated config may live under `tests/fixtures/<connector>/` provided they:

- Use only synthetic identifiers (no real tenant, property, vendor, or person).
- Use placeholder env-var names that do not collide with the operator's real names.
- Carry no real secret material.
- Declare themselves as fixtures in the file header comment.

Fixtures that fail the secret-scan test are rejected regardless of intent.

## Example - clean template versus populated config

Illustrative shape only; no real values in either.

Clean template (lives in repo):

```yaml
connector_id: pms_east_region
connector_kind: pms
version: 0.1.0
status: stub
owner: integration_owner_placeholder
vendor_neutral: true
source_name: SOURCE_NAME_PLACEHOLDER
auth_kind: api_key_placeholder
credential_reference: ENV_VAR_NAME_PLACEHOLDER
cadence: CADENCE_PLACEHOLDER
property_scope: PROPERTY_SCOPE_PLACEHOLDER
environment: ENVIRONMENT_PLACEHOLDER
```

Populated config (lives outside repo, in operator deployment):

```yaml
connector_id: pms_east_region
connector_kind: pms
version: 0.1.0
status: stable
owner: ops_team_alpha
vendor_neutral: true
source_name: east_region_source_alpha
auth_kind: api_key_placeholder
credential_reference: PMS_EAST_REGION_API_KEY
cadence: daily
property_scope:
  - property_alpha_one
  - property_alpha_two
environment: production
```

The populated config never enters the repo. The operator's secret backend holds the value bound to `PMS_EAST_REGION_API_KEY`.

## Failure modes and remediation

| Failure | Detection | Remediation |
|---|---|---|
| Populated config merged to repo | secret-scan or manifest-schema test | revert; rotate any exposed credential; file ApprovalRequest per `secrets_handling.md` leakage protocol. |
| Template missing a placeholder | manifest-schema test | update template; re-run tests. |
| Placeholder value left in deployed config | adapter boot-time validation | halt boot; operator populates value; restart. |
| Overlay modifies schema via config | overlay-validation test (see `config_overlay_interaction.md`) | reject overlay; file change-log entry for canonical schema change if actually required. |
