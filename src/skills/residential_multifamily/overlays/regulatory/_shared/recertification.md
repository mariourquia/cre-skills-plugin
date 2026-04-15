# Recertification

Status: stub. Placeholder for the periodic recertification cadence and
event types attached to regulated housing.

## Concept

Recertification is the periodic re-verification of household income,
composition, and eligibility. It produces a certification event (see
`eligibility_and_certification.md`) and may trigger a rent adjustment,
a subsidy recalculation, or a noncompliance finding if missed. Cadence
and required documentation vary by program.

## Target keys the overlay will populate

- `reporting_emphasis` -> adds a recertification backlog and timeliness
  metric.
- `delinquency_playbook_stage` -> interim recert on income loss may
  change the tenant portion and therefore the delinquency posture.
- Adds:
  - `recertification_schedule`
  - `recertification_timeliness`
  - `recertification_backlog`

## Event types

- move_in (initial certification at lease signing)
- annual (on anniversary of move-in or property-wide calendar)
- interim (triggered by reportable change: income, household composition,
  voucher portability)
- transfer (unit change within the same regulated property)
- move_out (exit certification)

## Program-specific cadences

Cadences are PROGRAM-OWNED. The parent overlay points at this file but
the specific cadence lives in each program overlay's `overrides` list.
Examples of variation: full annual recert always, annual self-cert with
triennial full, event-driven only. No numeric cadence is embedded here.

## Documentation requirements

Each recert event requires a program-specific documentation package
(income verification, asset verification, household-composition
attestation, student-status attestation where applicable, subsidy
recalculation worksheet where applicable). The document checklists live
in `reference/normalized/certification_forms__{program}.csv`.

## Phase 1 does not implement

- Program-specific cadence values.
- Document checklists.
- Workflow packs for issuing, tracking, and closing recert events.
- Agency-submission integration (TRACS, state HFA portals).
