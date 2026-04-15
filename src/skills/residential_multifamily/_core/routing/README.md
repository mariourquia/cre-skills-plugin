# Routing

The progressive-disclosure router. Given a request, it resolves the ten taxonomy axes and loads exactly the packs, overlays, and references needed — nothing more.

## Files

- `axes.yaml` — the axis catalog, mirroring `taxonomy.md` in machine-readable form.
- `rules.yaml` — the ordered rule set the router applies.
- `priority.yaml` — tie-breakers when multiple packs match.
- `defaults.yaml` — the default axis values applied when a user does not specify.
- `examples/` — end-to-end routing walk-throughs.

## Routing algorithm (pseudo-code)

```
def route(request):
    axes = resolve_axes(request)                    # from request text, session context, overlays
    missing = required_axes_missing(axes)
    if missing:
        return ask_user(missing) or fail_gracefully(missing)

    overlays = load_overlays(axes)                  # segment, form, lifecycle, mode, market, org
    packs = select_packs(axes, overlays)            # role / workflow / tailoring / router packs
    packs = apply_priority(packs)                   # priority.yaml
    references = load_reference_manifests(packs, overlays)

    if any reference required and missing:
        return surface_missing(reference) -- per Rule 10

    return Plan(packs, overlays, references, axes)
```

## Required axes

By default, the following axes must resolve before the router loads any role or workflow pack:

- `asset_class` (always `residential_multifamily` in this subsystem).
- `segment`.
- `form_factor`.
- `lifecycle_stage`.
- `management_mode`.
- `role` *or* `workflow`.
- `output_type` or decision severity indicator.

Other axes (`market`, `submarket`, `geography`, `org_id`) are required only when a loaded pack's `reference_manifest.yaml` requires a scoped reference.

## Failure modes

- **Missing axis, no default available.** Router asks the user with a short, focused question. Does not guess.
- **Missing axis, default available.** Router uses default and surfaces the substitution in the output.
- **Ambiguous match.** Router uses `priority.yaml` to pick. Ties are resolved by explicit priority number, then by pack recency (newer wins).
- **No match.** Router surfaces the gap and suggests the closest packs; does not fabricate.
- **Loaded pack requires reference not present.** Router refuses and opens a `missing_docs` entry for the tailoring skill's queue.

## Progressive disclosure in practice

- A short informational request ("what was occupancy last month at Ashford Park?") loads only `roles/property_manager/` (or `roles/asset_manager/` if the asker is an AM) plus the property's overlays and the minimal reference set to compute `physical_occupancy`.
- A weekly operating review loads `workflows/weekly_property_operating_review/` plus the role pack of the requester, plus segment / form / lifecycle overlays and their reference sets.
- A cross-portfolio question loads `roles/portfolio_manager/` plus the property master reference plus market overlays; property-specific overlays are loaded on demand as the portfolio pack drills down.

## Interaction with the existing cre-skills-plugin router

This subsystem is additive. A request that resolves to `residential_multifamily` enters the subsystem's router; other requests fall through to the existing flat-skill routing. The `SKILL.md` at the subsystem root acts as the entry point and declares its trigger phrases so the plugin's outer router can surface this subsystem appropriately.
