# ADR 0001: Catalog as Single Source of Truth

**Status:** Accepted
**Date:** 2026-04-02
**Decision makers:** Mario Urquia

## Context

Prior to v4.1.0, the plugin maintained counts and metadata in multiple independent locations:
- `plugin.json` description (hardcoded counts)
- `README.md` Key Stats table (hardcoded counts)
- `hooks.json` SessionStart prompt (hardcoded counts)
- `registry.yaml` (manual skill metadata with stale status fields)
- `routing/CRE-ROUTING.md` (markdown routing table parsed at runtime)
- `agents/_index.md` (manual agent roster)

These surfaces drifted from each other. README claimed 54 agents when 54 existed; hooks claimed 102 skills when 105 existed; registry showed `status: planned` for skills that had been deployed for weeks.

## Decision

Introduce a canonical machine-readable catalog (`catalog/catalog.yaml`) as the single source of truth for all plugin metadata: skills, agents, commands, calculators, orchestrators, and workflows.

All public-facing surfaces (README counts, plugin.json description, hooks prompt, routing table, registry.yaml) are generated from this catalog via `scripts/catalog-generate.py`. No hardcoded counts exist in any public surface.

The router (`routing/skill-dispatcher.mjs`) reads `dist/catalog.json` (the generated JSON representation) instead of parsing markdown tables.

## Schema

`catalog/catalog.schema.json` defines the schema. Each item has:
- `id`, `display_name`, `type`, `status`, `source_path`
- `domain`, `lifecycle_phase`, `persona`
- `intent_triggers`, `input_artifacts`, `outputs`
- `downstream_items`, `upstream_items`
- `hidden_from_default_catalog`
- `owner`, `last_reviewed_at`

## Consequences

### Positive
- Counts can never drift between surfaces
- CI can verify consistency (`catalog-generate.py --check`)
- Router operates on structured data, enabling artifact-aware matching and confidence scoring
- Stub/experimental items are programmatically hidden from default navigation
- Adding a new skill requires editing one file (SKILL.md frontmatter) and running `catalog-build.py`

### Negative
- Two-step process to update metadata: edit source -> run generator
- catalog.yaml is large (~200 items) and requires tooling to edit efficiently
- `registry.yaml` is now a generated compatibility artifact, not an editable source

### Risks
- If generator is not run after adding skills, surfaces drift until next build
- Mitigated by CI check (`catalog-generate.py --check`)

## Alternatives Considered

1. **Scan-only (no catalog.yaml):** Generate all surfaces directly from repo structure. Rejected because override metadata (aliases, intent_triggers, notes) would have nowhere to live.
2. **Merge frontmatter + registry only:** Keep registry.yaml as source. Rejected because the registry lacks agent, command, calculator, and workflow metadata.
3. **Database (SQLite):** Too heavy for a plugin that runs in plain Claude Code sessions.
