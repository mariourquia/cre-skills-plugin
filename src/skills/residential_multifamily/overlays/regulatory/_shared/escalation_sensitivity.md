# Escalation Sensitivity

Status: stub. Placeholder for the compliance events that escalate beyond
the normal approval-matrix path and trigger legal / agency coordination.

## Concept

Regulated housing adds a class of compliance events that exceed the
sensitivity of a routine operating approval. These events must route to
the compliance lead, to legal counsel, and in some cases to the owner
and the lender. The overlay declares which event kinds escalate; the
routing destinations themselves live in the org approval matrix.

## Target keys the overlay will populate

- `approval_threshold` -> inserts compliance-escalation gates that ride
  alongside the segment / org approval matrix rather than replacing them.
- Adds (escalation_kind):
  - `reac_nspire_finding`
  - `agency_noncompliance_notice`
  - `recapture_risk_trigger`
  - `vawa_event`
  - `fair_housing_complaint`
  - `file_audit_finding`

## Event kinds and escalation path (concept level)

- REAC / NSPIRE inspection findings: property-condition findings that
  threaten a pass score. Escalates to compliance lead and director of
  operations; legal counsel on any threatened contract action.
- Agency noncompliance notice: state HFA or HUD issues notice of
  noncompliance. Escalates to compliance lead, director of operations,
  legal counsel, owner.
- Recapture risk trigger: LIHTC event that could trigger credit
  recapture (extended-use breach, noncompliance beyond the correction
  period). Escalates to legal counsel and owner; tax counsel loops in.
- VAWA events: Violence Against Women Act requests (transfer, lease
  bifurcation, confidentiality). Escalates to compliance lead and legal
  counsel. Privacy-sensitive; resident communication handled carefully.
- Fair housing complaints: HUD or state complaint. Escalates to legal
  counsel and director of operations.
- File audit finding: tenant-file discrepancy surfaced by an agency
  audit. Escalates to compliance lead with remediation event opened on
  the compliance calendar.

## Relationship to org approval matrix

The overlay does not duplicate the org approval matrix. It points the
escalation kinds at the matrix rows that carry the actual routing
destinations (compliance_lead, legal_counsel, director_of_operations,
owner). The matrix rows themselves are filled during org tailoring.

## Phase 1 does not implement

- Escalation-SLA bands.
- Notification templates per escalation kind.
- Legal-counsel routing rules by jurisdiction.
- Integration with the org approval matrix rows (those are declared but
  not populated).
