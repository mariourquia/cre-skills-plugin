# Skill Conventions

Every role pack, workflow pack, and overlay in this subsystem follows the same file set and frontmatter shape so routing, tests, and the tailoring skill can reason about them uniformly.

## File set per pack

```
<pack_root>/
  SKILL.md                # the pack's prompt / operating doc (frontmatter + body)
  routing.yaml            # axes the pack applies to; triggers; priority
  reference_manifest.yaml # references this pack reads or writes
  metrics.md              # canonical metrics this pack uses (cites _core/metrics.md)
  workflows.md            # step-by-step workflow logic (if not a pure workflow pack)
  templates/              # starter templates referenced from SKILL.md
  examples/               # example invocations and outputs
  tests/                  # pack-level validation (optional; most tests live in top-level tests/)
  overlays/               # pack-scoped overlay hooks (rare; most overlays live under ../overlays/)
  change_log.md           # human-readable change log for this pack
```

`SKILL.md`, `routing.yaml`, and `reference_manifest.yaml` are **required** for every pack. Others are required when relevant (e.g., a pack without templates may omit `templates/`; a role pack without its own metrics may omit `metrics.md`).

## SKILL.md frontmatter

Every pack's `SKILL.md` starts with YAML frontmatter compatible with the existing `cre-skills-plugin` skill loader:

```yaml
---
name: <human-readable name>
slug: <kebab-case-slug, unique across the subsystem>
version: 0.1.0
status: draft | deployed | deprecated
category: residential_multifamily
subsystem: residential_multifamily
pack_type: role | workflow | overlay | tailoring
targets:
  - claude_code
stale_data: |
  A human-readable statement of what in the pack may drift.
applies_to:
  segment: [middle_market]          # list of segments the pack is explicitly tuned for
  form_factor: []                   # empty = all supported form factors
  lifecycle: [stabilized]           # lifecycle stages covered
  management_mode: [self_managed, third_party_managed]
  role: [property_manager]          # for role packs
  output_types: [operating_review, kpi_review, email_draft]
  decision_severity_max: recommendation
references:
  reads:
    - reference/normalized/market_rents.csv
    - reference/normalized/concession_benchmarks.csv
  writes: []
metrics_used:
  - physical_occupancy
  - economic_occupancy
  - delinquency_rate_30plus
escalation_paths:
  - kind: legal_notice
    to: role:property_manager -> role:regional_manager -> approval_request
  - kind: fair_housing_flag
    to: approval_request (required)
approvals_required:
  - concession_above_policy_threshold
  - eviction_filing
description: |
  One paragraph explaining what the pack does and when it triggers.
---
```

All frontmatter fields are validated by `tests/residential_multifamily/test_skill_manifests.py`.

## Body structure for role packs

1. **Role mission** — one paragraph stating the role's charter.
2. **Core responsibilities** — bulleted, covering daily / weekly / monthly / quarterly cadences.
3. **Primary KPIs** — canonical metric slugs with target bands pulled from `reference/derived/role_kpi_targets.csv`.
4. **Decision rights** — what the role can decide autonomously, what routes up, what requires approval.
5. **Inputs consumed** — document types, systems, references.
6. **Outputs produced** — templates, memos, reviews, emails.
7. **Cross-functional handoffs** — who the role hands off to, in what artifacts.
8. **Escalation paths** — explicit next-step-up for each escalation kind.
9. **Approval thresholds** — when the role must route an `approval_request`.
10. **Typical failure modes** — the 5–10 ways this role commonly gets wrong.
11. **Skill dependencies** — which workflow packs this role invokes.
12. **Templates used** — paths to templates in `templates/`.
13. **Reference files used** — paths to references in `reference/`.
14. **Example invocations** — 2–3 short prompts that should trigger this pack.
15. **Example outputs** — 1–2 short worked examples with inputs → outputs.

## Body structure for workflow packs

1. **Workflow purpose** — one paragraph.
2. **Trigger conditions** — explicit, implicit, recurring.
3. **Inputs (required / optional)** — with shapes.
4. **Outputs** — with shapes.
5. **Required context** — what the router must supply.
6. **Process** — numbered steps with decision points.
7. **Metrics used** — canonical slugs.
8. **Reference files used** — paths.
9. **Escalation points** — when the workflow hands off mid-process.
10. **Required approvals** — threshold-triggered and policy-triggered.
11. **Failure modes** — known ways the workflow gets wrong.
12. **Edge cases** — unusual inputs and how the workflow handles them.
13. **Example invocations** — 2–3 prompts.
14. **Example outputs** — 1–2 worked examples.

## Naming conventions

- Pack slugs: `<role_or_workflow>` or `<role_or_workflow>__<segment>` when a segment-specific pack is warranted (rare; usually overlays handle segmentation).
- Metric slugs: `snake_case`, singular unless the metric is inherently plural.
- Reference files: `<category>__<scope>.csv` (e.g., `market_rents__charlotte_mf.csv`) in `reference/normalized/`.
- Template files: `<artifact_slug>__<variant>.md` (e.g., `monthly_property_scorecard__middle_market.md`).

## Placeholder tags

Every example reference row and every sample template output carries `status: sample | starter | illustrative | placeholder`. Skills citing sample data must surface the tag in their output.

## No duplication rule

A pack may reference any canonical metric by slug. A pack may not redefine a metric. If a pack's business logic needs a derivative metric, the metric must be added to `_core/metrics.md` with full contract fields and an entry in `alias_registry.yaml`.

## Routing.yaml contract

See `schemas/skill_manifest.yaml`. A pack's `routing.yaml` declares:

- Which axes values activate the pack.
- Priority (used to break ties when multiple packs match).
- Required inputs the router must collect before invoking the pack.
- Fallback behavior when required inputs are missing.

## reference_manifest.yaml contract

See `schemas/reference_manifest.yaml`. Declares every reference file the pack reads or writes, plus the expected schema version for each. Tests fail if a pack reads a reference not declared in its manifest.

## Change log

Every pack has a `change_log.md`. Material edits (schema changes, metric slug additions, threshold changes) are logged with date, author, and reason. Reformatting, typo fixes, and prose clarifications do not require log entries.
