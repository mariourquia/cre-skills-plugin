# Middle-Market Finish Standards

Middle-market finish packages prioritize durability, repeatability, and resident
perceived value per dollar. The posture is: the resident should walk in and see a
clean, modern, durable apartment that will look the same on month 36 as on day one.

## Classic package

The classic package is the make-ready baseline for a non-renovated unit. Scope
includes:

- Resilient flooring (LVP or equivalent) throughout wet and high-traffic areas.
- Painted or refaced cabinets where cabinet boxes are sound; full replacement only
  when structural integrity fails.
- Durable appliance package sourced from the preferred vendor list in
  `reference/normalized/vendor_preferences.csv#row_mm_turn_vendors`.
- Neutral wall color with the standard paint code recorded in the turn library.
- Modernized light fixtures and faucets where cost-effective vs. like-for-like.

Costs and life expectancies live in `reference/normalized/turn_library/`. The overlay
does not embed dollar figures.

## Value-add package

When a unit qualifies for a value-add turn (triggered via the `renovation` lifecycle
overlay), the scope expands to the value-add package:

- Quartz-look countertops in kitchen and baths (quartz or reliable quartz-lookalike
  per preferred vendor and market).
- Upgraded resilient flooring or LVT with pad.
- Cabinet replacement or refresh with upgraded hardware.
- Upgraded appliance package from the preferred list.
- Lighting, faucet, and fixture upgrades.

The value-add scope ties to the `renovation_yield_on_cost` metric. Overruns are
reviewed against the metric's target band in
`reference/derived/role_kpi_targets.csv#row_mm_renovation_yield_on_cost`.

## What the overlay does not do

This overlay does not name brands, does not set dollar targets, and does not
substitute for the turn and capex libraries in the reference layer. It states the
segment's posture so the library rows can be applied correctly.
