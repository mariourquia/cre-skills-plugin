---
name: Move-Out Administration
slug: move_out_administration
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Jurisdiction-specific security-deposit accounting rules (return window, itemization
  format, statutory interest) and final-ledger reconciliation rules drift; all live in
  overlays. Damage charge schedules and fair wear-and-tear benchmarks come from reference
  libraries, not from skill prose.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [stabilized, renovation, lease_up, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [property_manager, assistant_property_manager]
  output_types: [checklist, memo, email_draft]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/normalized/approval_threshold_defaults.csv
    - reference/normalized/move_out_documents__{jurisdiction}.yaml
    - reference/normalized/damage_charge_schedule__{org}.csv
    - reference/normalized/unit_turn_cost_library__{market}.csv
  writes: []
metrics_used:
  - turnover_rate
  - average_days_vacant
  - make_ready_days
  - notice_exposure
  - bad_debt_rate
escalation_paths:
  - kind: disputed_damage_charges
    to: property_manager -> regional_manager -> approval_request(row 13 if waived)
  - kind: security_deposit_statutory_deadline
    to: property_manager (hard date) -> regional_manager escalation if missed
  - kind: fair_housing_flag
    to: approval_request(row 3)
approvals_required:
  - damage_charge_waiver_above_threshold
  - non_standard_final_ledger
description: |
  Coordinates every step from notice-to-vacate through unit transfer to the turn workflow.
  Produces the move-out inspection checklist, assembles the final ledger and
  statutorily-compliant security-deposit statement, handles damage charge disputes, and
  hands off to the turn workflow. Enforces jurisdiction-specific return deadlines.
---

# Move-Out Administration

## Workflow purpose

Turn a notice-to-vacate into a reliable, fair, fully documented move-out that clears the lease, reconciles the final ledger, meets statutory deposit-handling deadlines, and hands off to `workflows/unit_turn_make_ready` without information loss.

## Trigger conditions

- **Explicit:** "process move-out for unit X", "final ledger for resident Y", "security deposit return", "move-out inspection".
- **Implicit:** NoticeEvent filed; lease approaching end_date without renewal; judgment-ordered move-out from `workflows/delinquency_collections`.
- **Recurring:** daily scan of upcoming move-outs inside the notice window.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Lease record + NoticeEvent | record | required | end_date, vacate_date, reason |
| Resident ledger (current) | table | required | balance, open charges, prepaid |
| Jurisdiction move-out rules overlay | yaml | required | deposit return window, itemization |
| Damage charge schedule | csv | required | per-item charges bounded by overlay |
| Turn cost library | csv | optional | supports classic vs. renovation-tier estimate |
| Move-out inspection record | record | required post-inspection | photos, notes, damage list |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Move-out checklist | `checklist` | owner, due date, deadline |
| Inspection brief | `memo` | damages list with citations to schedule |
| Final ledger | statement | per jurisdiction format, `draft_for_review` |
| Security-deposit statement | statement | statutory format, `legal_review_required` |
| Turn handoff record | record | triggers `workflows/unit_turn_make_ready` |

## Required context

Asset_class, segment, form_factor, lifecycle_stage, management_mode, market, jurisdiction.

## Process

1. **Log the notice.** Confirm NoticeEvent fields; compute vacate_date; update `notice_exposure`.
2. **Communication to resident.** Draft acknowledgment with move-out instructions per overlay; `draft_for_review`; `legal_review_required` if jurisdiction treats as statutory.
3. **Pre-move-out inspection (optional per jurisdiction).** Schedule if allowed; produce pre-inspection packet.
4. **Move-out day.** PM records move-out event; photos, damage notes, final meter reads collected.
5. **Damage assessment (decision point).**
   - Apply the overlay's damage charge schedule. Any item not in the schedule is flagged for PM review; workflow does not invent a charge.
   - Classify wear-and-tear per the overlay's fair wear definition; do not charge fair wear.
   - If the resident pre-disputes charges, pause finalization and open a dispute ticket.
6. **Final ledger assembly.** Apply charges, prepaid rent, any off-cycle proration per overlay; produce the statement.
7. **Security-deposit statement (branch).**
   - If deposit applied fully against balance: produce the statutory statement showing itemization.
   - If refund due: produce the refund statement and schedule disbursement per jurisdiction overlay; refund handling is not a disbursement action inside this subsystem (finance/treasury handles).
   - Statutory deadline is tracked; missed deadline automatically escalates to regional_manager.
8. **Dispute handling.** If resident disputes charges, PM reviews; if a waiver is above the overlay's threshold, opens `approval_request` row 13.
9. **Fair-housing scan.** Compare proposed charges against baseline distribution; disparity signal routes to regional before finalization. Never adjusts charges on a protected-class basis.
10. **Turn handoff.** Write the turn handoff record with scope (classic vs. renovation) and planned cost band; triggers `workflows/unit_turn_make_ready`.
11. **Confidence banner.** Surface overlay `as_of_date` and `status`.

## Metrics used

`turnover_rate`, `average_days_vacant`, `make_ready_days`, `notice_exposure`, `bad_debt_rate`.

## Reference files used

- `reference/normalized/approval_threshold_defaults.csv`
- `reference/normalized/move_out_documents__{jurisdiction}.yaml`
- `reference/normalized/damage_charge_schedule__{org}.csv`
- `reference/normalized/unit_turn_cost_library__{market}.csv`

## Escalation points

- Statutory deposit-return deadline missed or at risk: regional_manager escalation.
- Disputed damage charges: PM -> regional; any waiver above threshold -> `approval_request` row 13.
- Fair-housing disparity signal: `approval_request` row 3.

## Required approvals

- Damage charge waiver above overlay threshold (row 13).
- Non-standard final ledger adjustment (row 13).

## Failure modes

1. Missing statutory deadline. Fix: hard-date tracker escalates automatically.
2. Charging for fair wear. Fix: overlay's wear definition is authoritative; items not in the charge schedule do not auto-populate.
3. Leaving the turn handoff without scope detail. Fix: handoff record requires classic/renovation tag and cost band.
4. Applying differential damage charges by resident attribute. Fix: fair-housing scan mandatory; disparity routes to regional.
5. Sample references treated as operating fact. Fix: confidence banner surfaces `status`.

## Edge cases

- **Early termination with fee:** apply fee per overlay; document the overlay basis.
- **Judgment-ordered move-out:** this workflow continues from `workflows/delinquency_collections`; inspections may be conducted by officer per jurisdiction.
- **Skip (resident left without notice):** statutory handling varies; overlay governs; inspection and charge schedule still apply.
- **Unit condition flagged hazardous:** route to maintenance_supervisor; do not conduct routine inspection.
- **Disputed balance at the door:** pause finalization; ledger snapshot is captured; PM and resident review.

## Example invocations

1. "Process move-out for unit 101 at Ashford Park, vacate 2026-04-30."
2. "Build the final ledger and security-deposit statement for unit 216 per Charlotte rules."
3. "Resident is disputing damage charges on unit 305. What's the path?"

## Example outputs

### Output — Move-out brief (abridged, unit 101, Ashford Park, vacate 2026-04-30)

**Notice logged.** Vacate_date 2026-04-30. `notice_exposure` updated.

**Inspection.** Photos and notes attached. Damages list cross-referenced against overlay schedule; one item flagged for PM review (not in schedule).

**Final ledger.** Applied charges, prorated rent through vacate_date, prepaid credits. `draft_for_review`.

**Security-deposit statement.** Charlotte overlay format; `legal_review_required`. Refund amount computed; disbursement routed to finance/treasury. Statutory deadline tracked.

**Fair-housing scan.** No disparity signal.

**Turn handoff.** Classic turn scope; cost band from reference library; `workflows/unit_turn_make_ready` triggered.

**Confidence banner.** `move_out_documents__charlotte@2026-03-31, status=sample`. `damage_charge_schedule@2026-03-31, status=starter`.
