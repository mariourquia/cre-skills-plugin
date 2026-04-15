# Config and Overlay Interaction

Rule of the road for how the integration layer interacts with the org-
tailoring overlay subsystem. The short version: canonical connector
contracts are immutable; org customization parameterizes them, never
mutates them.

## Immutable canon

Nothing in the org overlay may change:

- Canonical object shapes (`_core/ontology.md`).
- Canonical metric contracts (`_core/metrics.md`).
- Canonical enum sets (status values, severity values, exception
  categories).
- The field mapping template (`field_mapping_template.md`) and the
  normalization patterns (`normalization_patterns.md`).
- The raw-to-normalized pipeline design (`raw_to_normalized_design.md`).
- The lineage model (`lineage.md`) and the lineage manifest schema
  (`lineage_manifest.schema.yaml`).
- The layer design (`layer_design.md`).
- The exception taxonomy (`exception_taxonomy.md`) default severities,
  default routing, and auto-escalation rules for `critical` categories.
- The approval floor in `_core/approval_matrix.md`.
- The workflow activation map (`workflow_activation_map.yaml`) required
  inputs, blocking issues, and `human_approvals_required` lists.

A pull request that proposes to change any of the above under an org
overlay fails `tests/test_tailoring_canonical_immutability.py`.

## What the org overlay may parameterize

Everything listed below is org-scoped and lives under
`overlays/org/<org_id>/`.

### Source-instance configuration

An org runs specific instances of the connectors. Per-instance settings are
org-scoped and carry no canon implications.

Examples:

- `overlays/org/<org_id>/connectors/pms/instances.yaml` - named PMS
  instances, operator-facing labels (`source_name`), auth kind and access
  pattern (without credentials).
- `overlays/org/<org_id>/connectors/gl/instances.yaml` - GL instance(s).
- Similar per-connector files for `crm`, `ap`, `market_data`,
  `construction`, `hr_payroll`, `manual_uploads`.

### Property and account crosswalk overrides

The canonical crosswalk lives at `reference/connectors/master_data/`. An
org may carry org-specific crosswalk rows that bind their property codes,
vendor IDs, GL account codes, and unit IDs to canonical identifiers.

Crosswalk overrides:

- `overlays/org/<org_id>/master_data/property_crosswalk.csv`
- `overlays/org/<org_id>/master_data/vendor_crosswalk.csv`
- `overlays/org/<org_id>/master_data/gl_account_crosswalk.csv`
- `overlays/org/<org_id>/master_data/unit_crosswalk.csv`

These merge with canonical master data at run time. In the event of a
conflict, the org-scoped entry wins for that org; the canonical row is
unchanged for other orgs.

### Approval thresholds

Threshold values are org-scoped. Canonical `_core/approval_matrix.md`
defines the approval floor (minimum approver for each kind); the org
overlay sets the actual numeric thresholds.

Path: `overlays/org/<org_id>/approval_matrix.yaml`.

Rules:

- An org may tighten thresholds (require approval at lower values). It
  may not loosen them below the canonical floor.
- An org may name specific approvers per kind. Approvers resolve to
  `overlays/org/<org_id>/approvers.yaml`.

### Reporting preferences

Reporting cadence, distribution list, formatting preferences, and role
audiences live per org.

Path: `overlays/org/<org_id>/reporting/preferences.yaml`.

Rules:

- An org may set cadences tighter than canonical default. It may not
  skip required cadences (e.g., monthly property operating review is
  required; org may not disable it).
- An org may add roles to a distribution list. It may not remove required
  roles (e.g., compliance-risk receives TPM oversight output by default).

### Market coverage

An org's jurisdiction and market footprint.

Path: `overlays/org/<org_id>/markets/coverage.yaml`.

Rules:

- Identifies which states, metros, and submarkets the org operates in.
- Determines which `overlays/market/` overlays are candidates.
- Does not alter the shape of market data or the rent comp intake process.

### File-drop templates

For managers and operators whose data arrives as files, templates are
frequently customized per submitter.

Path: `overlays/org/<org_id>/connectors/manual_uploads/templates/<template_slug>/`.

Rules:

- Org templates inherit from canonical templates at
  `reference/connectors/manual_uploads/templates/<template_slug>/`.
- Org templates may add columns, rename display headers, relax optional
  fields, and set org-specific validation rules.
- Org templates may not remove required canonical columns, alter canonical
  types, or change identity-resolution behavior.
- Org template version bumps produce a new lineage manifest and a
  `mapping_override_log.yaml` entry if the override reaches a canonical
  mapping rule.

### Staleness ceilings and DQ tolerances

An org may tighten staleness ceilings and DQ tolerances beyond canonical
defaults.

Path: `overlays/org/<org_id>/dq/thresholds.yaml`.

Rules:

- Tighter (more strict) allowed. Looser (less strict) forbidden.
- If an org overlay sets a looser ceiling than canonical, the org overlay
  is rejected at load.

### Escalation chains

Per-exception escalation chains.

Path: `overlays/org/<org_id>/escalation_chains.yaml`.

Rules:

- An org may add roles before the final canonical step.
- An org may not remove canonical final steps (e.g., compliance-risk
  must remain in the chain for categories that canonically require it).
- Auto-escalate categories (`fair_housing_sensitive`, `legal_sensitive`,
  `policy_violation`) cannot have their auto-escalation behavior disabled.

### TPM-specific overlays

For third-party-managed portfolios, the org overlay carries TPM-specific
parameters:

Path: `overlays/org/<org_id>/pma/<tpm_id>.yaml`.

Contents:

- TPM identity, contract effective window, jurisdiction.
- Required report schedule (cadence, due offset, distribution).
- KPI set required on the scorecard.
- SLA definitions specific to the TPM.
- Escalation contacts at the TPM.
- File-drop template bindings for that TPM.

Rules:

- May tighten canonical requirements. May not loosen below canonical.
- May add TPM-specific metrics (as org extension) that reference but do
  not redefine canonical metrics.

## Interaction with the tailoring skill

The tailoring skill (`tailoring/SKILL.md`) writes the interview output
into the sign-off queue. Only an externally-approved commit tool writes
the actual overlay files. The tailoring skill never writes to:

- `_core/` (any path).
- `overlays/segments/`, `overlays/regulatory/`, `overlays/form_factor/`,
  `overlays/lifecycle/`, `overlays/management_mode/`, `overlays/market/`.
- `reference/` (any path).
- `reference/connectors/` (any path, including this `_core/`).

The org overlay is the only write target for tailoring, and only after
sign-off.

## Load order and merge semantics

At run time, configuration composes bottom-up:

1. Canonical base (`_core/` + `reference/connectors/_core/`).
2. Per-connector canon (`reference/connectors/<domain>/`).
3. Segment overlay.
4. Regulatory overlay (when `regulatory_program != none`).
5. Form-factor overlay.
6. Lifecycle overlay.
7. Management-mode overlay.
8. Market overlay.
9. Org overlay.

Each layer may override only what it is permitted to override per the
boundary rules. The merge rule on a given key is:

- Scalar: later overlay replaces earlier.
- Array: later overlay appends unless annotated with `replace: true`; when
  it replaces, the replaced values remain audit-visible.
- Object: merged key-by-key.
- Canonical immutables: rejected if the override would mutate them.

## Validation

The overlay validation suite runs on every PR that touches an overlay
path:

- `tests/test_tailoring_canonical_immutability.py` - canonical surfaces
  are unchanged.
- `tests/test_boundary_rules.py` - boundary contracts are respected.
- `tests/test_connector_contracts.py` - connector contracts still pass.
- `tests/test_regulatory_isolation.py` - regulatory content stays in the
  regulatory family.

An overlay that fails any of these cannot land.

## Summary rule

Org customization parameterizes canonical connector contracts. It does
not mutate them. Everything that looks like customization - thresholds,
approvers, cadence, coverage, templates, TPM schedules - attaches to the
org overlay and composes over canonical base at run time. The canonical
base stays unchanged across orgs.
