---
name: Draw Package Review
slug: draw_package_review
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Lender requisition format, required attachments, lien-waiver types (conditional / final /
  unconditional), insurance endorsement types, and compliance attestation templates are
  loan-document-specific. Each loan has its own overlay. No loan-doc constants live in
  skill prose.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [development, construction, renovation]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [construction_manager, asset_manager, estimator_preconstruction_lead, reporting_finance_ops_lead, development_manager]
  output_types: [memo, checklist, kpi_review]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/normalized/capex_line_items__{scope}.csv
    - reference/normalized/labor_rates__{market}.csv
    - reference/normalized/material_costs__{region}_residential.csv
    - reference/normalized/lender_draw_requirements__{loan}.yaml
    - reference/derived/contingency_assumptions__{org}.csv
    - reference/normalized/approval_threshold_defaults.csv
  writes: []
metrics_used:
  - cost_to_complete
  - contingency_remaining
  - contingency_burn_rate
  - change_orders_pct_of_contract
  - schedule_variance_days
  - milestone_slippage_rate
  - draw_cycle_time
  - capex_spend_vs_plan
escalation_paths:
  - kind: draw_submission
    to: construction_manager + asset_manager -> approval_request(row 12 then row 14 for final lender submission)
  - kind: cost_to_complete_variance
    to: construction_manager -> asset_manager -> executive if above threshold
  - kind: insurance_or_lien_waiver_gap
    to: construction_manager -> legal (refuse submission until resolved)
approvals_required:
  - draw_submission
  - lender_final_submission
description: |
  Reviews a draw package end to end before lender submission. Validates construction cost
  to date, reconciles to the lender requisition, confirms lien waivers by vendor and
  period, verifies insurance endorsements, checks compliance attestations, and evaluates
  cost-to-complete. Splits construction manager and asset manager responsibilities.
  Opens approval gates for construction manager (row 12) and, finally, for the lender
  submission (row 14). Final submission never goes out without approved records.
---

# Draw Package Review

## Workflow purpose

Every construction draw is load-bearing for the project's financial trajectory and for the lender's view of risk. This workflow takes the assembled draw package, runs it through the construction manager's review and the asset manager's review in sequence, verifies every attachment (lien waivers, insurance endorsements, compliance attestations), recomputes cost-to-complete, and opens the two gated approvals: the internal approval that the draw is ready to submit (row 12), and the final lender submission (row 14).

This pack is flagship-depth. It is where construction discipline and ownership discipline meet. It is also where the most common silent-failure modes live: stale lien waivers, missing insurance endorsements, change orders not yet reflected in the requisition, and cost-to-complete drift. Each of those is a hard check in this workflow.

## Trigger conditions

- **Explicit:** "review draw package", "draw X ready for review", "lender requisition review", "submit draw", "monthly draw".
- **Implicit:** GC submits pencil draw; owner's rep produces requisition draft; lender calendar deadline approaches.
- **Recurring:** monthly per active project.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Draw package | bundle | required | requisition, G702/G703 or lender format, attachments |
| Budget and contract register | record | required | original + all COs |
| Cost-to-date report | report | required | GC pencil + owner's rep recut |
| Change orders | table | required | approved + pending + rejected |
| Lien waivers | docs | required | conditional current period, final prior period |
| Insurance certificates and endorsements | docs | required | builders risk, GL, umbrella, auto, workers comp |
| Compliance attestations | docs | required | per loan |
| Schedule update | record | required | current forecast |
| Lender draw requirements overlay | yaml | required | per loan |
| Prior draw record | record | required | for continuity |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Construction manager review checklist | `checklist` | per attachment, per line item |
| Asset manager review memo | `memo` | financial, schedule, risk |
| Cost-to-complete refresh | `kpi_review` | per trade, per project |
| Attachment gap list | `checklist` | missing lien waivers, insurance, attestations |
| Internal approval request | request | row 12 (submission readiness) |
| Final lender submission request | request | row 14 |
| Draw cycle tracking | record | `draw_cycle_time` update |

## Required context

Asset_class, segment, form_factor, market, project, loan (for requirements overlay).

## Process

### Step 1. Stages of the draw.

A draw package, in this workflow, has five layered stages that are verified in order. The workflow refuses to advance a stage with an open gap.

**Stage 1. Construction cost to date.**

- Recompute cost to date against the contract register (original + approved COs).
- Confirm that COs not yet approved are flagged, not included in the requisition.
- Compare to GC's pencil; reconcile variances line by line.
- Confirm retainage held per loan terms; verify any retainage release requests comply with the overlay.

**Stage 2. Lender requisition.**

- Assemble the requisition in the lender's required format (AIA G702/G703, custom lender form, or draw statement per overlay).
- Cross-check the requisition line items against the budget and cost-to-date.
- Ensure budget reallocations (if any) are accompanied by a budget reallocation memo and overlay-permitted.
- Verify that soft-cost categories in the requisition conform to loan-doc definitions.

**Stage 3. Lien waivers.**

- For each vendor paid in the prior period: final (or unconditional) lien waiver for that period's payment present and valid.
- For each vendor being paid in the current period: conditional waiver for the amount being paid present and valid.
- State-specific waiver language validated (some states have mandatory form language; overlay governs).
- Missing or mismatched waivers open gaps; submission holds.

**Stage 4. Insurance and bonding.**

- Builders risk policy in force through period; endorsement current.
- GC GL, umbrella, auto, workers comp certificates current; named insured clauses match loan requirements per overlay.
- Any subcontractor above overlay threshold: COI on file; endorsement if required.
- Bonds (performance, payment) current if required by loan.

**Stage 5. Compliance attestations.**

- Required attestations per loan overlay: may include contractor certifications, compliance with labor standards, prevailing wage, environmental, permitting status, building code inspections completed for the pay period's work.
- Missing attestation opens a gap; submission holds.

### Step 2. Construction manager's review responsibilities.

The construction manager's review covers the physical and contractual integrity of the draw:

- Are the quantities and percentages complete correct against field observation?
- Are lien waivers present and correct for every vendor and period?
- Is the insurance in force and correctly endorsed?
- Are compliance attestations current?
- Do change orders reflected in the requisition match approved COs? (Any pending CO not yet approved cannot appear as a cost in this draw.)
- Does the schedule view match the work claimed? If the draw claims progress on a milestone that the schedule has not yet started or completed upstream of, the discrepancy is flagged.
- Is retainage tracked correctly?
- Are any material or labor costs drifting vs. the estimator baseline?

The construction manager marks the draw "CM-reviewed" when Stages 1-5 pass. Any unresolved gap routes to the GC or the owner's rep for fix before advancement.

### Step 3. Asset manager's review responsibilities.

The asset manager's review covers the financial and risk posture of the draw:

- Recompute `cost_to_complete`. Is it trending vs. plan? What is the trajectory over the trailing 3 and 6 draws?
- Compute `contingency_remaining` and `contingency_burn_rate`. Is burn proportional to percent complete cost? If burn rate > 1.0, flag overburn.
- Compute `change_orders_pct_of_contract`. Above overlay threshold at current percent complete flags review.
- Compute `schedule_variance_days` and `milestone_slippage_rate`.
- Assess `draw_cycle_time` trend (submission -> funding days).
- Assess whether the loan's covenants or tests are impacted by this draw's claims (in-balance tests, required equity, remargining triggers). If any, the loan-doc overlay governs.
- Review the attached CM checklist for unresolved items.
- Ask: is there any scope quality, schedule, or risk signal that warrants a conversation with the GC or lender before submission?

The asset manager marks the draw "AM-reviewed" when the financial and risk posture is acceptable. The asset manager opens `approval_request` row 12 for submission readiness.

### Step 4. Internal approval (row 12).

Row 12 is the internal approval that the draw package is ready to submit to the lender. Minimum approvers: construction_manager + asset_manager. The approval record carries the draw number, the period, the requisition total, the cost-to-complete at this period, contingency remaining, and a brief narrative.

### Step 5. Lender final submission (row 14).

A draw is a lender-facing submission marked `final`. Row 14 governs any lender-facing `final` submission; an approved row 14 record is required before the package leaves the organization. Minimum approvers: asset_manager + finance/reporting lead. The workflow holds the package (does not transmit) until approval returns `approved`.

### Step 6. Submission and tracking.

On approved row 14, the package is released. The workflow records submission timestamp; cycle-time clock starts; status moves to "submitted-to-lender".

### Step 7. Funding close-out.

On lender funding, the workflow updates `draw_cycle_time`, updates disbursement records, and flags any lender callbacks or questions for the construction manager.

### Step 8. Confidence banner.

Surface: lender requirements overlay `as_of_date` and `status`; estimator baseline `as_of_date`; insurance certificate expiration dates; lien waiver period coverage; contingency assumption `as_of_date`. Any sample-tagged reference is explicit.

### Decision points and branches

- If Stage 3 (lien waivers) has a missing final waiver for a prior-period vendor: do not advance. Open gap, route to GC for cure before CM review continues.
- If Stage 4 (insurance) finds a lapsed or misaddressed endorsement: do not advance.
- If Stage 5 (compliance) finds a missing attestation: do not advance.
- If cost-to-complete shows material variance above overlay threshold: CM + AM engage; `workflows/cost_to_complete_review` triggered in parallel.
- If contingency burn rate > overlay band at current % complete: AM flags; `workflows/cost_to_complete_review` triggered and executive review path considered.
- If schedule variance > overlay threshold: `workflows/schedule_risk_review` triggered in parallel.
- If the draw would cause a loan covenant or test to fail (e.g., in-balance test, required equity): escalation to CFO / executive; draw may be delayed pending remediation.
- If a pending CO is excluded from the requisition but the GC has started the work: flag; the workflow does not retroactively add unapproved COs to the draw.

## Metrics used

`cost_to_complete`, `contingency_remaining`, `contingency_burn_rate`, `change_orders_pct_of_contract`, `schedule_variance_days`, `milestone_slippage_rate`, `draw_cycle_time`, `capex_spend_vs_plan` (program-level feeder).

## Reference files used

- `reference/normalized/capex_line_items__{scope}.csv`
- `reference/normalized/labor_rates__{market}.csv`
- `reference/normalized/material_costs__{region}_residential.csv`
- `reference/normalized/lender_draw_requirements__{loan}.yaml`
- `reference/derived/contingency_assumptions__{org}.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Escalation points

- Lien waiver gap: CM -> legal; submission held.
- Insurance endorsement gap: CM -> risk/legal; submission held.
- Compliance attestation gap: CM -> PM / development_manager; submission held.
- Cost-to-complete variance: CM -> AM -> executive (conditional).
- Schedule variance: `workflows/schedule_risk_review` triggered.
- Covenant / in-balance failure risk: CFO / executive.
- Internal submission readiness: row 12.
- Lender final submission: row 14.

## Required approvals

- Row 12 (internal submission readiness).
- Row 14 (lender final submission).
- Rows 10 / 11 on any CO embedded in the draw.

## Failure modes

1. Including unapproved COs in requisition. Fix: any pending CO is excluded; approved COs only.
2. Stale lien waiver (prior period final waiver missing). Fix: hard gate; submission held.
3. Insurance endorsement misaddressed to wrong insured. Fix: overlay-driven named-insured check.
4. Compliance attestation missing. Fix: hard gate; per loan overlay.
5. Cost-to-complete silent drift. Fix: recompute every draw; flag vs. trailing 3 and 6.
6. Contingency over-burn hidden by reallocation. Fix: contingency burn-rate metric explicit; reallocation memo required.
7. Submission without row 14 approval. Fix: transmission gated.
8. Retainage misapplied. Fix: overlay retainage policy is the reference.
9. Sample overlay treated as loan-doc. Fix: `lender_draw_requirements__{loan}.yaml` must be loan-specific; sample tag surfaced at runtime.

## Edge cases

- **First draw:** mobilization-heavy; overlay may have specific mobilization rules; verify closely.
- **Final draw:** retainage release, close-out documents (punch list, as-builts, warranties), final lien waivers from every subcontractor; compliance attestation for final completion.
- **Lender-ordered inspection mid-draw:** results incorporated before submission if available; else noted.
- **Change in lender (loan assumption / refi mid-construction):** overlay transitions; next draw per new lender's format.
- **In-balance test triggered by draw:** remargining required before submission; CFO / executive path.
- **Completed TCO but not certificate-of-occupancy:** soft-cost categories shift per loan overlay.
- **Disputed mechanic's lien against the project:** do not submit current draw until cleared or bonded over; overlay governs.
- **FX or cross-border component (rare for U.S. residential but conservative):** do not silently handle; flag for human.

## Example invocations

1. "Review the April draw for the Willow Creek construction project. It's due to the lender on the 25th."
2. "Run the CM and AM reviews on draw #7 for the Riverbend development."
3. "Cost-to-complete trending off for the South End renovation. Pull the most recent draw and pressure-test."

## Example outputs

### Output — Draw review (abridged, April draw, Willow Creek)

**Stage 1 — Cost to date.** Reconciled to contract register. Three COs approved and included; one pending CO excluded. GC pencil aligned with owner's rep recut within overlay tolerance.

**Stage 2 — Requisition.** Lender format matches loan overlay. Soft-cost categories conform to loan-doc definitions. No budget reallocation this period.

**Stage 3 — Lien waivers.** Prior-period final waivers present for every vendor paid. Current-period conditional waivers present and valid. State-specific language verified per jurisdiction overlay.

**Stage 4 — Insurance.** Builders risk in force through period; named-insured clause matches. GC GL, umbrella, auto, workers comp current. Two subcontractors above overlay threshold: COI on file, endorsement current.

**Stage 5 — Compliance attestations.** All required attestations present per loan overlay.

**CM review.** "CM-reviewed" status set.

**AM review.**

- `cost_to_complete` recomputed; within overlay band.
- `contingency_remaining` within band; `contingency_burn_rate` at or below 1.0 at current percent complete.
- `change_orders_pct_of_contract` within overlay band at current percent complete.
- `schedule_variance_days` within overlay band; `milestone_slippage_rate` within band.
- `draw_cycle_time` trailing within band.
- No covenant or in-balance impact.

**Approvals.** `approval_request` row 12 opened and `approved`. `approval_request` row 14 opened; pending lender final submission approval.

**Submission.** Held pending row 14 approval. On approval, package releases and cycle-time clock starts.

**Confidence banner.** `lender_draw_requirements__loan_willow_creek@2026-01-15, status=sample (loan-doc overlay pending confirmation)`. `capex_line_items__scope@2026-03-31, status=starter`. `labor_rates__charlotte@2026-03-31, status=sample`. `contingency_assumptions@2026-03-31, status=starter`.

### Output — Cost-to-complete pressure test (abridged, South End renovation)

**Trigger.** Cost-to-complete trending above plan beyond overlay threshold on recent draws.

**Findings.** Material-cost drift on two line items; labor hours above estimator baseline on a third. `workflows/cost_to_complete_review` invoked for deeper analysis.

**Draw impact this period.** Current draw does not yet require contingency drawdown; however, trajectory implies contingency pull within 2-3 draws.

**Recommendation.** AM to convene CM and estimator; owner-side remediation plan needed before next draw. Draw may still submit with notation.

**Confidence banner.** As above.
