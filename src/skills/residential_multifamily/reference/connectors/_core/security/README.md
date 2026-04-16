# Security and Privacy - Integration Layer

This subsystem defines the security and privacy model for every connector, every adapter, every manual upload that lands data under `reference/raw/`, `reference/normalized/`, or `reference/derived/`. The rules here are not aspirational. They are the enforceable floor.

## Scope

Applies to:

- All connector domains: `pms/`, `gl/`, `crm/`, `ap/`, `market_data/`, `construction/`, `hr_payroll/`, `manual_uploads/`.
- Every adapter an operator builds against the canonical connector contracts (`reference/connectors/_schema/`).
- Every manual upload routed through the `manual_uploads/` connector.
- Every reference-data refresh that draws on inbound third-party feeds.

Does not apply to: skill prose, overlays, or tailoring outputs. Those are governed by `_core/DESIGN_RULES.md` and `_core/BOUNDARIES.md`.

## Relationship to canon

- **Approval floor.** Any action the integration layer could automate but that touches an eviction, concession above policy, vendor award, draw release, investor submission, or fair-housing sensitive decision is gated by `_core/approval_matrix.md` and must materialize an ApprovalRequest that conforms to `_core/schemas/approval_request.yaml`.
- **Design rules.** `_core/DESIGN_RULES.md` forbids secrets in repo, silent defaults on critical fields, hardcoded credentials, and PII in samples. The docs in this subsystem operationalize those rules for the integration layer.
- **Layer design.** `reference/connectors/_core/layer_design.md` owns the raw-normalized-derived contract. Security classifications stack on top of that contract per layer.

## Layered defense

Seven layers, each with its own doc in this directory. A failure in any single layer does not grant access; an attacker or a careless operator must defeat all seven in sequence to cause harm.

1. **data_classification** - every field carries a classification (`none`, `low`, `moderate`, `high`, `restricted`). Rules in `pii_classification.md`.
2. **access_control** - role-based, least-privilege, mapped to the tailoring audiences declared in `tailoring/AUDIENCE_MAP.md`. Rules in `least_privilege_guidance.md`.
3. **transit** - every connector declares a placeholder auth kind in its manifest (`api_key_placeholder`, `oauth_placeholder`, `sftp_key_placeholder`, `mtls_placeholder`, `basic_auth_placeholder`, `email_inbox_placeholder`, `shared_drive_placeholder`, `none`). Operators bind real credentials outside the repo. Rules in `secrets_handling.md`.
4. **at_rest** - normalized and derived layers require encryption at rest. Raw is retained with its original provenance and the same at-rest requirement. Rules in `security_model.md`.
5. **audit** - every connector operation emits an immutable audit record. Rules in `audit_trail.md`.
6. **approval** - gated actions enforce `_core/schemas/approval_request.yaml`. Rules in `approval_gates_for_integration_actions.md`.
7. **fair_housing** - resident-facing outputs are scanned; protected-class attributes never become match keys or model inputs. Rules in `fair_housing_controls.md`.

A parallel doc, `legal_hold_and_retention.md`, defines how the layer respects legal holds and records retention policy; `unsafe_defaults_registry.md` enumerates the configurations that would be unsafe if defaulted; `config_templates.md` and `config_overlay_interaction.md` define how templates stay clean of secrets while still permitting org-specific parameterization; `masking_and_redaction.md` defines default masking rules keyed to audience and classification; `pii_sample_policy.md` defines the rules for synthetic sample payloads; `security_testing_guidance.md` lists the mechanical checks that enforce the above.

## File index

- `security_model.md` - the seven-layer model end to end.
- `pii_classification.md` - canonical field-level classifications.
- `secrets_handling.md` - credential lifecycle outside the repo.
- `masking_and_redaction.md` - default masking rules by audience and class.
- `config_templates.md` - how manifest and config templates ship without secrets.
- `pii_sample_policy.md` - synthetic-only sample data policy.
- `fair_housing_controls.md` - fair-housing-aware design controls.
- `legal_hold_and_retention.md` - legal hold workflow and retention defaults.
- `audit_trail.md` - immutable audit record schema and retention.
- `unsafe_defaults_registry.md` - configurations unsafe to default.
- `approval_gates_for_integration_actions.md` - integration actions that require ApprovalRequest.
- `least_privilege_guidance.md` - role-based least-privilege recommendations.
- `config_overlay_interaction.md` - how org overlays parameterize safely.
- `security_testing_guidance.md` - mechanical security tests.

## How to use this subsystem

1. Before defining a new connector: read `security_model.md`, then `pii_classification.md` for the field set, then `config_templates.md` for the manifest shape.
2. Before adding a new field to an existing connector: classify it per `pii_classification.md`; declare masking per `masking_and_redaction.md`.
3. Before building a sample payload: read `pii_sample_policy.md`.
4. Before automating an integration action: check `approval_gates_for_integration_actions.md` and `unsafe_defaults_registry.md`.
5. Before an operator deploys an adapter: walk `security_testing_guidance.md`.

Every doc in this directory cites canonical sources by path. When canon moves, docs here move with it.
