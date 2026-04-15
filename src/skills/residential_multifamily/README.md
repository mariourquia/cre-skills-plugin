# Residential Multifamily Skill System

A modular, composable, role-aware operating layer for U.S. residential multifamily, built to support near-zero-human back-office operations across property management, asset management, portfolio management, development, construction, estimating, reporting, third-party manager oversight, and executive operating leadership.

**Phase 1 focus:** middle-market / workforce / attainable conventional rental housing. Lower-rent/affordable and luxury are present as stubs so the canonical core stays stable while overlays expand.

## What is in this subsystem

```
src/skills/residential_multifamily/
  _core/                  canonical ontology, metrics, schemas, routing, guardrails
  roles/                  role-oriented skill packs (site, regional, corporate, exec)
  workflows/              workflow-oriented skill packs (funnel, renewal, turn, capex, draw, etc.)
  overlays/
    segments/             middle_market (deep), affordable (stub), luxury (stub)
    form_factor/          garden, walk_up, wrap, mid_rise, high_rise (stub)
    lifecycle/            lease_up, stabilized, renovation, development, construction, recap
    management_mode/      self_managed, third_party_managed, owner_oversight
    org/                  organization-specific overlays produced by the tailoring skill
  reference/              externalized figures (rent comps, labor, materials, capex, etc.)
    raw/                  source-of-truth inbound records
    normalized/           cleaned, schema-conforming
    derived/              benchmarks computed from normalized
    archives/             superseded records (for audit)
    examples/             walk-throughs showing how an update flows end-to-end
  templates/              operating/reporting/construction/resident starter templates
  tailoring/              interactive terminal-UI skill that produces org overlays
  examples/               end-to-end routed scenarios
  tests/                  validation: manifests exist, metrics complete, no hardcoded figures
```

## The core operating thesis

1. **Skills are modular, composable, and role-aware.** A site PM, an asset manager, and a CFO ask different questions; the system routes to the right pack and loads only the depth required.
2. **No hard-coded numbers in skill prose.** Every mutable figure (rents, concessions, labor rates, material costs, staffing ratios, capex benchmarks) lives in `reference/` and is referenced by ID. Agents and humans can update references without editing skill text.
3. **Canonical core, overlays on top.** Metrics, ontology, and workflow verbs are defined once in `_core/`. Segment / form-factor / lifecycle / management-mode / market / org specifics are layered as overlays.
4. **Progressive disclosure.** The routing layer resolves (asset class → segment → form factor → stage → management mode → role → market → org) before surfacing templates, thresholds, and reference files.
5. **Controlled autonomy.** Drafting, analysis, summarization, monitoring, and routing are automated. Legal, fair-housing, safety, licensed-engineering, and threshold-bound financial actions require explicit human approval.
6. **Auditability by default.** Every reference change carries old/new values, source, as-of date, proposer, approver, confidence, and reason. Every decision surfaces the references and assumptions behind it.

## Where to start

- **New to the system?** Read `_core/README.md`, then `_core/taxonomy.md`, then `_core/metrics.md`.
- **Building a skill?** Read `_core/skill_conventions.md` and copy the `roles/_TEMPLATE/` scaffold.
- **Updating a figure?** Read `reference/README.md` and follow the update-flow that matches the figure type.
- **Onboarding an operator?** Run the `tailoring/` skill; it produces `overlays/org/<org_id>/` without mutating the canonical core.
- **Running the test suite?** `pytest tests/residential_multifamily/` from repo root (see `tests/README.md`).

## Out of scope for Phase 1

- Deep build-out of affordable / LIHTC / HUD compliance workflows (architecture only, no depth).
- Deep build-out of luxury / high-rise workflows (architecture only, no depth).
- Student, senior, BTR, and mixed-use residential variants (not stubbed yet; taxonomy reserves space).
- International markets.

## Design rules (non-negotiable)

See `_core/DESIGN_RULES.md`. Summary:

- No metric is defined twice. `_core/alias_registry.yaml` prevents silent redefinition.
- No figure lives in prose. Every number traces to `reference/`.
- Every skill declares its `reference_manifest.yaml` — what it reads, what it writes.
- Fair housing and legal-sensitive actions carry explicit approval gates, not optional ones.
- Example files are tagged `status: sample | starter | illustrative | placeholder`. Never pretend sample data is live.

## Relationship to the broader cre-skills-plugin

This subsystem is additive. It does not replace existing flat skills under `src/skills/*` (leasing-operations-engine, capex-prioritizer, annual-budget-engine, etc.). Over time, residential-multifamily–specific logic that currently lives in those flat skills may be referenced by or migrated into this subsystem via overlays; that migration is not part of Phase 1.
