# Config Overlay Interaction - Parameterize Without Mutating the Canonical Contract

Organizations layer their own configuration on top of the canonical connector contracts. Overlays may bind source identity, cadence, environment, credential reference, and property scope. Overlays may not alter the schema, the mapping transform, the reconciliation rules, or the normalized output shape.

This doc lays out the rule set with enough specificity that an overlay can be validated mechanically. The tests that enforce these rules live in `tests/test_boundary_rules.py`.

## What an org overlay is

An org overlay is a configuration file set maintained by an organization deploying the subsystem. Overlays live under `overlays/org/<org_id>/` in the operator's deployment artifacts (outside this repo) or, for org overlays that the subsystem ships as reference templates, under `src/skills/residential_multifamily/overlays/org/<org_id>/`.

An overlay never redefines a canonical concept. It either parameterizes a canonical concept (binding a concrete value to an abstract field) or extends canon with an org-specific addition that coexists with canon.

## Safe overlay patterns

### pattern one - bind source_instance identity

An org overlay may set:

- `source_name` - the operator-chosen stable identifier for an instance of a connector.
- `cadence` - the operator's ingest cadence token (daily, weekly, monthly, event_driven, etc.).
- `environment` - the deployment environment slug.
- `credential_reference` - the env-var name bound in the operator's secret backend (never the credential itself).
- `property_scope` - the list of property_id values the connector is authorized to ingest.
- `owner` - the named operator role or contact for the connector instance.

These fields are declared as placeholders in the canonical manifest (`reference/connectors/<domain>/manifest.yaml`) and populated by the overlay during deploy-time composition. See `config_templates.md` for the placeholder convention.

### pattern two - bind operator-specific scheduling, runner, and observability

An org overlay may declare:

- a connector runner identifier (operator-specific scheduler, e.g., `runner_alpha`).
- an observability sink identifier.
- a monitoring profile slug that maps to the operator's alert routing.
- a retention tier slug that maps to the operator's records-management policy.

These bindings do not change the connector contract; they provide the operator-specific hooks the adapter uses at runtime.

### pattern three - add org-specific reference paths on top of canon

An org overlay may add:

- a property master extension file with org-specific property attributes not present in canon.
- an additional reference category local to the org (for example, an org-specific amenity library).
- an org-specific overlay of an existing reference category with additional rows (never replacing canonical rows).

The overlay must cite the canonical reference path it is extending and must not remove or modify any canonical row.

### pattern four - tighten approval or classification thresholds

An org overlay may:

- add approvers to the required set on any gated action (`approval_gates_for_integration_actions.md`).
- raise a field's classification (e.g., treat `email` as `high` even though canon treats it as `moderate`).
- shorten ApprovalRequest validity windows.
- add additional fair-housing proxy attributes to the forbidden list.

All four are tightenings, not loosenings. Boundary tests verify overlay constraints are additive or more restrictive.

### pattern five - add org-specific exception taxonomy entries

An org overlay may add exception types to the taxonomy (owned by a separate agent under `reference/connectors/_core/`). The addition is additive; canonical exception types remain.

## Unsafe overlay patterns

The following are rejected by boundary tests and by reviewers.

### pattern A - overlay modifies canonical schema

An overlay may not change a canonical entity's field set, field types, required-field list, or primary key declaration. Schema changes live in `reference/connectors/<domain>/schema.yaml` and follow `approval_gates_for_integration_actions.md` entry three (schema change acknowledgment).

Example of what is forbidden:

- An overlay declares that `resident_name` is optional in the PMS `lease` entity. Forbidden: canon declares `resident_name` as required.
- An overlay declares a new required field on a canonical entity. Forbidden: new required fields must go through canonical schema change.

### pattern B - overlay modifies canonical mapping transforms

An overlay may not change the mapping logic declared in `reference/connectors/<domain>/mapping.yaml`. Mappings are canonical. Overrides follow `approval_gates_for_integration_actions.md` entry four (mapping override) and are gated per-instance, not redeclared in overlay.

### pattern C - overlay modifies canonical reconciliation rules

An overlay may not weaken, bypass, or replace a canonical reconciliation check. Canonical checks defined in `reference/connectors/<domain>/reconciliation_checks.yaml` or under `reference/connectors/qa/` apply to every org. An overlay may add additional checks; it may not remove or weaken canonical ones.

### pattern D - overlay modifies the normalized output shape

An overlay may not change the shape of normalized output files. The canonical entity contract in `_schema/entity_contract.schema.yaml` is authoritative across all orgs. Derived metrics computed against org-specific shapes could not be benchmarked across the subsystem and would silently break every cross-org comparison.

### pattern E - overlay removes canonical reference paths

An overlay may not remove or override canonical reference paths. Canonical references are the baseline; overlays coexist with canon.

### pattern F - overlay loosens approval or classification thresholds

An overlay may not:

- remove a required approver from a canonical gated action.
- drop a field's classification below its canonical level.
- lengthen ApprovalRequest validity windows.
- remove a canonical fair-housing proxy attribute from the forbidden list.
- waive any `unsafe_defaults_registry.md` entry.

All five loosenings are rejected.

### pattern G - overlay introduces secrets

An overlay that carries real credentials, real tokens, real URLs with tenant-specific paths, or any other `secrets_handling.md` forbidden content is rejected by the secret-scan test.

### pattern H - overlay introduces PII in sample data

An overlay that carries sample content with real PII is rejected by the sample-scan test (`pii_sample_policy.md`).

## Validation - mechanical tests

`tests/test_boundary_rules.py` runs the following checks against every overlay in scope:

1. **schema_additive_only** - verifies that every entity present in both canon and overlay has the same required-field set and primary key in overlay as in canon.
2. **mapping_not_modified** - verifies that overlays do not carry alternative mappings for canonical entities.
3. **reconciliation_additive_only** - verifies that canonical reconciliation checks are still present when an overlay is composed.
4. **reference_path_preserved** - verifies that canonical reference paths remain after overlay composition.
5. **approval_not_loosened** - verifies that overlay-declared approver sets for canonical gated actions are supersets of the canonical required approver set.
6. **classification_not_downgraded** - verifies that overlay-declared classifications are equal to or higher than canon.
7. **no_secrets_in_overlay** - secret-scan test against every overlay file.
8. **no_real_pii_in_overlay_samples** - sample-scan test against every overlay sample file.
9. **fair_housing_forbidden_list_preserved** - verifies that canonical forbidden-proxy list is preserved in overlay-composed config.

## Safe overlay - illustrative example

Synthetic only; no real values.

```yaml
# overlays/org/sample_alpha/pms_east_region.overlay.yaml
# binds source_instance identity only.
connector_id: pms_east_region
source_name: east_region_source_alpha
cadence: daily
environment: production
credential_reference: PMS_EAST_REGION_API_KEY_ALPHA
property_scope:
  - property_alpha_one
  - property_alpha_two
owner: ops_team_alpha
# adds an additional approver for this org's gated actions.
additional_approvers:
  reference_data_refresh:
    - executive
# tightens classification for this org.
classification_tightenings:
  email: high
```

Canon still controls schema, mapping, reconciliation, and normalized output; the overlay binds identity and scope only.

## Unsafe overlay - illustrative example of what would be rejected

```yaml
# overlays/org/sample_beta/pms_east_region.overlay.yaml
connector_id: pms_east_region
# REJECTED: schema override
schema_overrides:
  lease:
    required_fields:
      resident_name: false  # pattern A violation
# REJECTED: mapping override
mapping_overrides:
  lease:
    resident_name_from_source: name_field_alpha  # pattern B violation; should go through gated mapping override
# REJECTED: reconciliation bypass
reconciliation_overrides:
  duplicate_pk_check: skip  # pattern C violation
# REJECTED: approval loosening
approval_overrides:
  reference_data_refresh:
    required_approvers:
      - connector_owner  # pattern F violation; canon requires compliance_risk plus category owner
```

Each line above fails a boundary test.

## Related

- `config_templates.md` - manifest placeholders that overlays bind.
- `secrets_handling.md` - why overlays never carry credentials.
- `pii_sample_policy.md` - why overlays never carry real PII.
- `approval_gates_for_integration_actions.md` - gated actions overlays may tighten but not loosen.
- `pii_classification.md` - canonical classifications overlays may raise but not lower.
- `fair_housing_controls.md` - fair-housing posture overlays may extend but not weaken.
- `security_testing_guidance.md` - full test list including boundary tests.
