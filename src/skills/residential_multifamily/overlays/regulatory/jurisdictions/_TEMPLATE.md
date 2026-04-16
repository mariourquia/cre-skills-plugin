# Jurisdiction Overlay Template

Placeholder. Each file or subdirectory under `jurisdictions/` represents a
state or local housing-finance-agency overlay that layers on top of a
program overlay to capture jurisdiction-specific rules (QAP variants, state
HFA compliance cadence, local UA publisher, state-specific rent-limit
schedule variants, local audit protocols).

An overlay under this directory should declare:

- `overlay_id: regulatory.affordable.jurisdiction.<slug>`
- `overlay_kind: regulatory` (or `regulatory.program` when scoped tighter)
- `parent_overlay: regulatory.affordable.<program>`
- `scope.jurisdiction: <slug>`
- `scope.regulatory_program: <program slug>`

Reference tables for jurisdiction overlays live at
`reference/normalized/*__{jurisdiction}.csv`.

Phase 1 ships no populated jurisdiction overlays; this template is the
landing pad for the first one.
