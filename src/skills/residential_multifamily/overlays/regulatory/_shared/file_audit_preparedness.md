# File Audit Preparedness

Status: stub. Placeholder for the tenant-file discipline required by
regulated housing compliance audits.

## Concept

Agency compliance audits (state HFA, HUD, USDA) inspect tenant files to
verify that each household was correctly certified and recertified.
Common audit dimensions: initial eligibility documentation, income and
asset verification, annual recert packet completeness, signed
attestations, student-status documentation (LIHTC), VAWA notices,
reasonable-accommodation requests, and HAP-contract correspondence.
Files must be produced on request within a program-specified window.

## Target keys the overlay will populate

- `reporting_emphasis` -> adds file-audit-preparedness score.
- Adds:
  - `tenant_file_checklist`
  - `tenant_file_completeness_rate`
  - `audit_response_window_remaining`

## Tenant file checklist (concept level, not exhaustive)

- Initial eligibility packet.
- Annual and interim recert packets.
- Signed program-specific attestations (student, household composition,
  VAWA, reasonable accommodation where applicable).
- UA schedule in effect at each certification event.
- Rent-limit reference at each certification event.
- Subsidy correspondence (HAP contract amendments, voucher portability
  documents, PHA billing adjustments where applicable).
- Program-specific required forms (e.g., tenant income certifications,
  move-in / move-out checklists).

## Audit response protocol

When an agency issues an audit request:

- Intake: log the request, the requesting agency, the scope, and the
  response-window deadline.
- Retrieval: pull files from the retention system.
- Review: route to compliance lead for completeness check.
- Submit: deliver via the agency's designated channel.
- Remediate: if the audit returns findings, open remediation events and
  integrate them into the compliance calendar.

## Retention rules

Retention minimums are program-specific and typically measured in years
beyond the resident's move-out or the property's extended-use period,
whichever is longer. Program-specific retention windows are declared in
each program overlay and enforced via the org-level records policy.

## Phase 1 does not implement

- Concrete retention windows.
- Audit-response workflow pack.
- File-completeness scoring logic.
- Integration with document management systems.
