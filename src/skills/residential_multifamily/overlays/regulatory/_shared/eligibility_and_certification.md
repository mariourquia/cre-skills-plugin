# Eligibility and Certification

Status: stub. Placeholder for the eligibility-screening and certification
surface that regulated housing adds on top of conventional screening.

## Concept

Eligibility screening tests whether a prospective household qualifies under
the program rules attached to the unit. Certification captures the verified
state of that household at a defined event (move-in, annual recert, interim
recert, transfer, move-out). The regulatory overlay owns this surface;
conventional screening policy (credit, rental history, background) is still
governed by the segment overlay's `screening_policy`.

## Target keys the overlay will populate

When deepened, this file will back the following overrides:

- `screening_policy` -> adds program-specific eligibility gates
  (income band, student status, household composition, subsidy documentation)
  on top of the segment screening policy. Does NOT replace it.
- `reporting_emphasis` -> adds certification timeliness as a tracked
  reporting metric.
- Adds (new canonical concepts under this overlay):
  - `income_certification_timeliness`
  - `certification_event_ledger`
  - `eligibility_screening_outcome`

## Certification event types

- move_in
- annual
- interim (household composition change, income change above program
  threshold, voucher portability event)
- transfer (unit-to-unit within the same property)
- move_out

## Verification source references

Reference files (created in Phase 2) that hold the verified document
checklists and acceptable source types:

- `reference/normalized/verification_sources__{program}.csv`
- `reference/normalized/certification_forms__{program}.csv`

## Phase 1 does not implement

- Specific document checklists per program.
- Verification vendor preferences.
- Certification timeliness SLA bands.
- Program-specific student-rule decision trees.
