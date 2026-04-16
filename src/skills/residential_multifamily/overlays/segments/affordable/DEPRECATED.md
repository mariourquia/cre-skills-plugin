# DEPRECATED: overlays/segments/affordable/

Status: deprecated as of 2026-04-15.

Affordable regulated housing has moved to `overlays/regulatory/affordable/`.

## Why

The `overlays/segments/` family is reserved for conventional market-positioning
overlays (middle_market, luxury). Affordable regulated housing is a compliance
axis, not a market-positioning segment: a middle_market property can sit
inside a LIHTC regulatory agreement and both overlays should compose.
Placing it under `segments/` conflated two orthogonal axes.

## New location

`overlays/regulatory/affordable/` carries the parent regulatory overlay.
Program-specific overlays live under
`overlays/regulatory/affordable/programs/<program>/overlay.yaml`.

## Action required

Any `reference_manifest` or pack that still resolves to this path should be
updated to point at `overlays/regulatory/affordable/`. The overlay loader
should log a deprecation warning when the old path is resolved.

## Lifecycle

This deprecation notice and the accompanying deprecated stubs
(`overlay.yaml`, `DIVERGENCE.md`) remain in place for one refinement cycle
to flag late-migrating callers. They are scheduled for removal in the
2026-Q3 refinement pass.
