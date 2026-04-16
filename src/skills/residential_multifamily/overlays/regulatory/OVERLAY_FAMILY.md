# Regulatory Overlay Family: Canonical Definition

Status: Phase 1 architecture. Starter stubs populated; program-specific
rent / income / UA / form tables are deferred to Phase 2.

## Purpose

Own the compliance surface that attaches to a multifamily property operating
under a regulatory agreement, subsidy contract, or program-specific rent and
income restriction. Surfaces include eligibility screening, income and rent
limit testing, utility allowance reconciliation, recertification cadence,
agency reporting, file audit preparedness, inspection readiness, and
compliance-escalation sensitivity.

## Scope boundary

This family covers, and only covers, regulated affordable housing and
subsidized programs. Specifically in-scope:

- LIHTC (nine-percent credit, four-percent credit, tax-exempt bond-financed, state credits).
- HUD-subsidized: project-based Section 8 HAP, tenant-based vouchers,
  project-based vouchers, HUD 202 (elderly), HUD 811 (persons with
  disabilities).
- USDA Rural Development (515, 521).
- State and local HFA programs (workforce, state-credit, density bonus,
  inclusionary, CDBG / HOME-funded).
- Mixed-income properties that combine regulated set-aside units with
  market-rate units under the same ownership.

Out of scope for this family:

- Conventional market-positioning posture (middle_market, luxury). That lives
  in `overlays/segments/`.
- Form factor, lifecycle, management mode, market, org. Those live in their
  respective overlay families.
- Carbon / energy regulatory programs (e.g., NYC LL97). Those belong in a
  separate `overlays/regulatory_energy/` family, not here.

## Non-duplication rule

The regulatory overlay does NOT redefine segment-level concepts. It does NOT
override middle_market or luxury rent-growth posture, service standards,
staffing ratios, or finish standards except where a program rule demands it.
When in doubt, the segment owns the posture and the regulatory overlay adds
a constraint or a compliance surface on top.

## Loading rule

A property's `regulatory_program` axis is resolved first. If it is `none`,
the entire `overlays/regulatory/` tree is skipped. If it is non-`none`, the
shared `regulatory.affordable` overlay loads first, followed by the
program-specific overlay (e.g., `regulatory.affordable.lihtc`). Jurisdiction
overlays (under `jurisdictions/`) load after program overlays when a
state / local HFA overlay is registered for the property's market.

## Composition

Merge order, later wins on same `target_ref`:

1. Segment
2. Regulatory family (this file)
3. Form factor
4. Lifecycle
5. Management mode
6. Market
7. Org

## Phase 1 content

Phase 1 delivers:

- `affordable/overlay.yaml` as the parent overlay for the family. Status:
  stub. It points overrides and adds at the `_shared/*` stubs.
- Program overlays under `affordable/programs/<program>/overlay.yaml`, each
  declaring `parent_overlay: regulatory.affordable` and their own scope on
  `regulatory_program`. Status: stub.
- Nine `_shared/*` concept files defining the target-key shape each overlay
  will eventually own.
- A jurisdictions template.

Phase 1 does NOT deliver populated rent, income, or UA schedules; those
reference tables are the Phase 2 deliverable.

## Approvers

Phase 2 deepening of this family requires sign-off from:

- director_of_operations
- compliance_lead
- legal_counsel (when the change touches REAC / NSPIRE, noncompliance, or
  recapture)
