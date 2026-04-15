# Overlays

Overlays layer on top of the canonical core and role/workflow packs. They never redefine canonical concepts; they constrain, override, or extend.

## Overlay kinds

| Kind | Directory | Purpose |
|---|---|---|
| Segment | `segments/` | middle_market (deep), affordable (stub), luxury (stub). |
| Form factor | `form_factor/` | garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise, high_rise (stub). |
| Lifecycle | `lifecycle/` | lease_up, stabilized, renovation, development, construction, recap_support. |
| Management mode | `management_mode/` | self_managed, third_party_managed, owner_oversight. |
| Market | `<not-yet-built-out>` | per-market overlays (loaded from `reference/normalized/markets/`). |
| Org | `org/` | organization-specific overlays produced by the tailoring skill. |
| Policy | inside org/ | screening policy, concession policy, vendor policy, etc. |
| Property | inside org/ | per-property overrides (rare). |

## Overlay manifest

Every overlay has an `overlay.yaml` conforming to `_core/schemas/overlay_manifest.yaml`. Required fields:

- `overlay_id`, `overlay_kind`, `scope`.
- `overrides`: list of `{target_kind, target_ref, override_value, reason}`.
- `adds`: list of overlay-specific additions.
- `authoring_notes`.

## Merging rules

Overlays are applied in this order (later overlays override earlier on the same `target_ref`):

1. Segment (one of: middle_market / affordable / luxury).
2. Form factor.
3. Lifecycle.
4. Management mode.
5. Market (if loaded).
6. Org (always last; the operator's overrides win).

A pack asking for a threshold or target band reads the merged result. Each merge step is auditable.

## What overlays can override

Per `overlay_manifest.yaml`, allowed `target_kind` values:

- `metric_threshold`, `metric_target_band`, `metric_filters_default`.
- `approval_threshold`.
- `staffing_ratio`, `service_standard`, `finish_standard`.
- `concession_policy`, `renewal_strategy`, `delinquency_playbook_stage`.
- `resident_comm_tone`.
- `reporting_emphasis`.
- `screening_policy`.
- `vendor_preference`.

## What overlays cannot do

- Redefine a canonical metric's numerator / denominator / rollup (must go through `_core/metrics.md` change log).
- Add new canonical objects (ontology changes go through core).
- Remove a guardrail.
- Loosen an approval floor below the canonical minimum.
- Disable a fair-housing or safety rule.

## Stubs and divergence notes

The `affordable/` and `luxury/` segment overlays are stubs in Phase 1. They include:

- `overlay.yaml` with empty or placeholder overrides.
- `DIVERGENCE.md` — a narrative listing how they are expected to differ from `middle_market`.

This keeps the architecture visibly extensible without implying depth that does not exist.
