---
name: Move-In Administration
slug: move_in_administration
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Move-in document packets, welcome materials, utility setup checklists, and
  reasonable-accommodation acknowledgment language are overlay-driven and will drift.
  Security-deposit and prepaid-rent handling is jurisdiction-specific. Fair-housing
  language in welcome communications is scanned at draft.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [lease_up, stabilized, renovation]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [property_manager, assistant_property_manager, leasing_manager]
  output_types: [checklist, email_draft, memo]
  decision_severity_max: recommendation
references:
  reads:
    - reference/normalized/approval_threshold_defaults.csv
    - reference/normalized/move_in_documents__{jurisdiction}.yaml
    - reference/normalized/utility_setup_guides__{market}.yaml
  writes: []
metrics_used:
  - move_in_conversion
  - leased_occupancy
  - preleased_occupancy
  - physical_occupancy
escalation_paths:
  - kind: move_in_ready_blocker
    to: maintenance_supervisor -> property_manager
  - kind: reasonable_accommodation_request
    to: regional_manager -> legal_counsel (human-only, routed)
  - kind: fair_housing_flag
    to: approval_request(row 3)
approvals_required: []
description: |
  Coordinates every step from lease execution to resident in the unit. Confirms move-in
  readiness, generates document packets per jurisdiction overlay, schedules utility
  transfers, produces welcome communications, and closes the loop by marking the move-in
  event and updating occupancy metrics. Routes any reasonable-accommodation signal out of
  the workflow to a human path.
---

# Move-In Administration

## Workflow purpose

Drive a reliable, fair, and documented move-in for every new resident. Convert an executed lease into a prepared unit, a complete document packet, a scheduled utility transfer, a welcome touch, and a clean event record that updates the property's leased and physical occupancy metrics.

## Trigger conditions

- **Explicit:** "prep move-in for unit X", "move-in packet for resident Y", "welcome communication", "move-in readiness check".
- **Implicit:** a lease transitions from `executed` to within `preleased_window` of `start_date`; a unit ready-date approaches; a renter confirms move-in time.
- **Recurring:** daily scan of upcoming move-ins inside the overlay's notice window.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Executed lease | record | required | lease_id, unit_id, start_date, resident_ids |
| Unit ready status | record | required | from `workflows/unit_turn_make_ready` |
| Jurisdiction move-in docs overlay | yaml | required | security-deposit and prepaid-rent handling |
| Utility setup overlay | yaml | required | transfer cutover guide by market |
| Welcome template library | md | optional | overlay-scoped templates |
| Accommodation-request flag | field | optional | if present, route out |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Move-in readiness checklist | `checklist` | blockers, owners, due dates |
| Document packet | assembled | lease copy, addenda, rules, disclosures per overlay |
| Utility transfer instructions | `email_draft` | resident-facing, market-specific |
| Welcome communication | `email_draft` | portal + email, marked `draft_for_review` |
| Move-in event record | update | triggers `leased_occupancy`, `physical_occupancy` refresh |

## Required context

Asset_class, segment, form_factor, lifecycle_stage, management_mode, market, jurisdiction. Jurisdiction gates document-packet composition.

## Process

1. **Scan upcoming move-ins.** Surface every lease with `start_date` inside the overlay's notice window.
2. **Readiness check (decision point).**
   - If unit status is `ready` (from turn workflow) and all required inspections are complete, proceed.
   - If unit is not ready, open a readiness-blocker checklist; escalate any blocker not resolvable by the overlay's SLA to maintenance_supervisor and property_manager.
3. **Document packet assembly.** Compose per jurisdiction overlay: lease + addenda + rules + disclosures + security-deposit receipt per statute + any state-required notices. Every template carries `legal_review_required` if jurisdiction treats it as statutory.
4. **Utility setup.** Produce the market-specific utility transfer instructions; include resident-held vs. RUBS-recovered items per overlay. Flag if utility is the owner's responsibility and transfer not needed.
5. **Welcome communication.** Draft portal message + email in overlay-approved tone; scan copy against the fair-housing term list.
6. **Accommodation-request handling (branch).** If the applicant or new resident has indicated a reasonable-accommodation / reasonable-modification need, route out of this workflow to the human-only accommodation path; do not process autonomously.
7. **Move-in day confirmation.** PM or leasing confirms move-in. Workflow records the event, updates metrics, and closes the readiness checklist.
8. **Post-move-in touch.** Schedule a 7-day follow-up draft for PM review.
9. **Confidence banner.** Reference `as_of_date` and `status` tags.

## Metrics used

`move_in_conversion`, `leased_occupancy`, `preleased_occupancy`, `physical_occupancy`.

## Reference files used

- `reference/normalized/approval_threshold_defaults.csv`
- `reference/normalized/move_in_documents__{jurisdiction}.yaml`
- `reference/normalized/utility_setup_guides__{market}.yaml`

## Escalation points

- Move-in readiness blocker: maintenance_supervisor and property_manager.
- Reasonable-accommodation signal: out of workflow, human path.
- Fair-housing term hit in any communication: `approval_request` row 3 before send.

## Required approvals

None by default. Legal-notice-style documents in the packet rely on jurisdiction overlay; the packet is not sent until PM confirms.

## Failure modes

1. Move-in without readiness confirmation. Fix: readiness state from the turn workflow is a gate.
2. Missing a jurisdiction-specific disclosure. Fix: overlay governs the packet composition; missing overlay refuses.
3. Sending welcome copy that signals protected-class preference. Fix: copy scan is mandatory.
4. Processing an accommodation request in-line. Fix: auto-handoff to human path.
5. Failing to update occupancy metrics. Fix: event record is the write that triggers metric recompute.

## Edge cases

- **Short-lead move-in (within 48 hours of signing):** shorten checklist and flag PM; overlay may require extra confirmation.
- **Joint lease with phased move-in (one resident in, one later):** event records partial; `leased_occupancy` updates on first; `physical_occupancy` reflects actual.
- **Subsidized or assistance-program resident:** additional overlay documents; workflow surfaces the overlay path.
- **Transfer within property:** use this workflow for the destination unit; `workflows/move_out_administration` handles the origin unit.

## Example invocations

1. "Prep move-in for unit 214 at Ashford Park on 2026-05-01."
2. "What's blocking the move-in for 305 next week?"
3. "Build the document packet for resident X at Willow Creek, jurisdiction=Charlotte."

## Example outputs

### Output — Move-in readiness brief (abridged, unit 214, Ashford Park, start 2026-05-01)

**Status.** Unit `ready` per turn workflow, inspection completed 2026-04-28. No blockers.

**Document packet.** Lease + addenda + rules + disclosures + security-deposit receipt per Charlotte overlay assembled; `legal_review_required` banners present on statutorily-required disclosures; PM confirmation pending before send.

**Utility setup.** Charlotte overlay: resident-held electric + gas; owner-held water (RUBS). Resident instruction draft produced.

**Welcome.** Portal message + email drafted `draft_for_review`. Copy scan clean.

**Accommodation flag.** None.

**Post-move-in follow-up.** 7-day touch scheduled 2026-05-08.

**Confidence banner.** `move_in_documents__charlotte@2026-03-31, status=sample`. `utility_setup_guides__charlotte@2026-03-31, status=starter`.
