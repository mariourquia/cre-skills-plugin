# Regulatory Overlay Family

Overlays under this directory handle the compliance regimes that attach to a
property when it is operated under a regulatory agreement, subsidy contract, or
program-specific rent and income restriction.

This family is SEPARATE from `overlays/segments/`. Segments describe
market-positioning (middle_market, luxury). A property's market positioning and
its regulatory status are independent axes: a middle-market garden property can
sit inside a LIHTC regulatory agreement; a mixed-income mid-rise can mix
regulated and market-rate units.

## When this overlay loads

The regulatory overlay family is only resolved when the `regulatory_program`
axis is set to a non-`none` value during overlay composition. Properties with
`regulatory_program = none` load zero overlays from this tree.

Resolution is keyed on `scope.regulatory_program`:

- `lihtc`, `hud_section_8`, `hud_202_811`, `usda_rd`, `state_program`,
  `mixed_income`.

A mixed-income property loads the `mixed_income` program overlay plus any
unit-level program overlays that apply to its regulated set-aside.

## Composition order

Merge order (later overrides earlier on the same `target_ref`):

1. Segment (middle_market / luxury).
2. Regulatory (this family, when `regulatory_program != none`).
3. Form factor.
4. Lifecycle.
5. Management mode.
6. Market.
7. Org.

See `overlays/README.md` for the full merge contract.

## Relationship to segments

- `overlays/segments/` defines market-positioning posture (rent-growth
  expectations, screening posture, concession policy, finish standard).
- `overlays/regulatory/` defines compliance-driven constraints that ride on top:
  what rent the property is ALLOWED to charge, what income the resident must
  qualify at, when recertification is due, when the agency inspects, and what
  the consequences of a finding are.

The two overlays do not duplicate. A regulatory overlay does not redefine
middle_market rent-growth posture; it caps the achievable rent at a program
limit and adds certification and reporting surfaces the segment does not carry.

## Phase 1 scope

Phase 1 is architecture only:

- Family README and canonical definition (this file and `OVERLAY_FAMILY.md`).
- Starter `_shared/*` stubs that define the target-key shape of each
  regulated-housing concept the overlay will eventually own.
- Program-level overlay stubs (LIHTC, HUD Section 8, HUD 202 / 811, USDA RD,
  state program, mixed income) that declare `parent_overlay: regulatory.affordable`
  and point at the `_shared/*` stubs.
- Jurisdiction template.

Phase 1 does NOT ship concrete rent limits, income limits, utility allowance
schedules, program forms, or approval threshold dollar amounts. Those land in
Phase 2 alongside the reference tables that hold the numeric state.

## Boundaries

See `_core/BOUNDARIES.md` (to be created in a follow-on pass) for the formal
rule about what cannot cross between segment and regulatory overlays and which
axis owns which target keys.
