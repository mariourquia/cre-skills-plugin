# Naming Conventions

## Slug rules

- Slugs are `snake_case`, ASCII lowercase letters, digits, and underscores. Pattern: `^[a-z][a-z0-9_]*$`.
- Slugs are singular unless the referent is inherently plural (e.g., `residents` is permitted in a field name; a metric or object slug is singular).
- Slugs are stable. Renames require deprecation (see `change_log_conventions.md`), not silent rewrites.

## Scope suffixes

Use scope suffixes when the same metric exists at multiple grains:

- `_by_market` — rolled up to market grain.
- `_by_submarket` — rolled up to submarket grain.
- `_by_property` — rolled up to property grain (default for most metrics; omit unless ambiguous).
- `_portfolio` — rolled up to portfolio grain.

## Window suffixes

When the window is not the canonical default:

- `_mtd` / `_qtd` / `_ytd` — to-date windows.
- `_t3` / `_t6` / `_t12` — trailing month windows.
- `_rolling` — generic rolling window; use only if specifying in metadata.

## Scenario suffixes

- `_budget`, `_forecast`, `_reforecast`, `_actual`, `_underwriting`, `_estimate`, `_bid`, `_benchmark`.

Generally, scenarios are declared in frontmatter of a metric contract, not baked into the slug. Suffix only when a scenario-specific slug is needed for disambiguation (e.g., `dev_cost_per_unit_estimate` vs. `dev_cost_per_unit_actual`).

## Pack slug rules

- Role packs live under `roles/<role_slug>/`. Slug matches `applies_to.role[0]`.
- Workflow packs live under `workflows/<workflow_slug>/`. Slug is the canonical workflow name (e.g., `renewal_retention`, `delinquency_collections`).
- Overlay packs live under `overlays/<overlay_kind>/<scope>/`. Slug is `overlay_kind__scope` (e.g., `segment__middle_market`).
- Tailoring skill slug is `tailoring`.

## Reference file naming

- `reference/normalized/<category>__<scope>.csv` where scope is the aggregation axis (e.g., `market_rents__charlotte_mf.csv`, `material_costs__southeast_residential.csv`).
- `reference/raw/<category>/<yyyy>/<mm>/<source>__<as_of>.csv` for raw inbound.
- `reference/derived/<category>__<scope>.csv` for computed benchmarks.

## Template file naming

- `templates/<artifact_slug>__<variant>.md` where variant captures segment / form / mode (e.g., `monthly_property_scorecard__middle_market.md`, `tour_email_response__draft_for_review.md`).

## Example file naming

- `examples/<scenario_slug>/` with `INPUT.md`, `ROUTING.md`, `OUTPUT.md`.

## Conflict detection

The test suite scans:

1. All metric slugs across `_core/metrics.md` and pack-level `metrics.md` files. Duplicate slugs fail the build.
2. All object aliases across `ontology.md` and `alias_registry.yaml`. Aliased name used canonically without registration fails the build.
3. All field names across pack `SKILL.md` frontmatter against `schemas/skill_manifest.yaml`. Extras fail.
4. All reference paths declared in `reference_manifest.yaml` against actual files. Missing paths fail.
5. All metric references in pack text against `_core/metrics.md` and the pack's `metrics_used` list. Missing fail.

## Forbidden patterns

- Colliding slugs across families (e.g., two metrics named `occupancy`).
- Alias-only usage of a canonical concept without a registry entry.
- Redefinition of a canonical metric's numerator, denominator, filters, or rollup in a pack (overrides only via overlay).
- Numeric thresholds embedded in prose. (Write: "exceeds the policy threshold for approval in `overlays/org/<org>/approval_matrix.yaml`". Do not write: "exceeds $25,000".)
- Hardcoded market identifiers in pack prose. (Write: "the property's market". Do not write: "Charlotte" unless the pack is explicitly market-scoped.)

## Warning patterns (soft fails; reviewed)

- Use of "occupancy" without qualifier outside explicit metric references. The test warns and suggests adding a qualifier.
- Use of "turnover", "rent growth", "delinquency", "concession", "make-ready" without qualifier.
- Use of "comp" without "rent" or "sales" qualifier.
- Use of "rate" without clear unit (percent, days, dollars).

## Directory-slug exception for subsystem roots

The wider `cre-skills-plugin` repository uses `kebab-case` for skill directory names
(`acquisition-underwriting-engine`, `dd-command-center`). The residential multifamily
subsystem uses `snake_case` for its internal slugs — roles, workflows, overlays, metrics,
taxonomy axes — and the subsystem root directory (`src/skills/residential_multifamily/`)
therefore also uses `snake_case` so that the skill-folder name and the internal slug
are identical.

This is an intentional exception, not a drift.

- `conftest.py` explicitly asserts `SUBSYS.name == "residential_multifamily"`.
- `src/catalog/catalog.yaml` registers the skill with `id: residential_multifamily`.
- A rename to `residential-multifamily` would require updating the assertion, the
  catalog, and every doc that names the path. It is tracked as a standalone ticket in
  `session_state/NEXT_SESSION_PROMPT.md` and is NOT executed during the 2026-04-15
  refinement pass.

All new skill directories created elsewhere in the repo continue to use `kebab-case`.

## Segment vs regulatory program

Two distinct axes cover what used to be conflated:

- `segment` covers **conventional market-positioning**: `middle_market`, `luxury`.
- `regulatory_program` covers **regulated affordable housing compliance regimes**:
  `none` (default), `lihtc`, `hud_section_8`, `hud_202_811`, `usda_rd`, `state_program`,
  `mixed_income`.

These axes compose. A property may be `segment: middle_market` AND
`regulatory_program: lihtc` — the two overlays merge under the composition order in
`_core/BOUNDARIES.md`. Conventional routes default `regulatory_program: none`; no
regulatory overlay ever loads unless the user sets the axis explicitly.

The legacy axis value `segment: affordable` is accepted for one refinement cycle as a
migration alias that prompts the user for `regulatory_program` and retries routing.

## Preferred vocabulary

To reduce drift, the subsystem prefers:

- "Resident" over "tenant" for multifamily context. Lease-level objects use "lease"; account-level uses "resident account". "Tenant" appears only as an alias.
- "Notice to vacate" for the resident-initiated notice; "non-renewal" for the owner-initiated equivalent.
- "Make-ready" for the unit-turn workflow; "turn" as shorthand allowed in prose.
- "Capex" for capital expenditure; "capital project" in formal headings.
- "TPM" for third-party manager; spell out at first mention in narrative documents.
- "PMA" for property management agreement.
- "GPR" for gross potential rent; "NOI" for net operating income; "NRSF" for net rentable square feet.
- "DSCR" and "debt yield" as uppercase acronyms.
