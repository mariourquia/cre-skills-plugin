# Residential Multifamily Subsystem — Changelog

## 0.1.0 — 2026-04-15 — Phase 1 foundation

Initial subsystem scaffold.

### Added

- Canonical `_core/` layer: taxonomy, ontology, metric contracts, routing framework, approval matrix, guardrails, naming conventions, change-log conventions, alias registry, schemas.
- Role packs under `roles/` (16 roles covering site through executive).
- Workflow packs under `workflows/` (24 workflows across operations, finance, development, construction, TPM oversight, executive).
- Overlays: middle-market segment (full depth), affordable + luxury stubs, form factor overlays, lifecycle overlays, management mode overlays.
- Reference schemas + starter CSVs across 16 reference categories; all starter data tagged `status: sample | starter | illustrative | placeholder`.
- Templates covering operating, reporting, construction, TPM oversight, resident communications.
- Tailoring skill with interactive terminal UI pattern, question bank, org overlay builder, missing-docs queue.
- Test suite validating reference manifests, metric completeness, no-hardcoded-figures, routing, naming, rendering.

### Not yet included

- Live market data.
- Deep affordable / LIHTC / HUD compliance logic (stubbed only).
- Deep luxury / high-rise logic (stubbed only).
- Student, senior, BTR, mixed-use residential overlays.
- International markets.
