---
name: Delinquency and Collections
slug: delinquency_collections
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Jurisdiction-specific legal-notice requirements, grace-period definitions, court timing,
  and statutory cure periods drift and are governed by overlays. Dollar thresholds for
  write-off and legal escalation live in org overlays, not in this pack. Payment-plan
  terms (max length, minimum down, cap per unit) are overlay-driven. Nothing in this pack
  constitutes legal advice; every legal-notice action passes through a gate and a
  jurisdiction-specific overlay.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [stabilized, renovation, lease_up, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [property_manager, assistant_property_manager, regional_manager, asset_manager, reporting_finance_ops_lead]
  output_types: [kpi_review, memo, checklist, email_draft]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/normalized/collections_benchmarks__{region}_mf.csv
    - reference/normalized/delinquency_playbook_middle_market.csv
    - reference/normalized/approval_threshold_defaults.csv
    - reference/derived/role_kpi_targets.csv
    - reference/normalized/jurisdiction_legal_notice_rules__{jurisdiction}.yaml
    - reference/normalized/payment_plan_policy__{org}.yaml
  writes: []
metrics_used:
  - delinquency_rate_30plus
  - collections_rate
  - bad_debt_rate
  - economic_occupancy
  - notice_exposure
escalation_paths:
  - kind: legal_notice
    to: property_manager + regional_manager -> approval_request(row 1)
  - kind: eviction_filing
    to: property_manager + regional_manager + legal_counsel -> approval_request(row 2)
  - kind: fair_housing_flag
    to: regional_manager + legal_counsel -> approval_request(row 3)
  - kind: non_standard_payment_plan
    to: regional_manager -> approval_request(row 13)
  - kind: write_off
    to: regional_manager + asset_manager -> approval_request(row 6 or 7 per threshold)
approvals_required:
  - legal_notice
  - eviction_filing
  - non_standard_payment_plan
  - write_off_above_threshold
  - tenant_dispute_legal_exposure
description: |
  Canonical delinquency-to-resolution playbook. Classifies every case by aging stage,
  proposes the next-step action per the overlay's playbook, generates draft resident
  communications with legal-review banners where jurisdictions treat them as notices, opens
  approval_requests for every gated transition (legal notice, eviction filing, non-standard
  payment plan, write-off above threshold), and records fair-housing guardrails at each
  decision point. Runs weekly at the property and on-demand when a single case transitions
  aging buckets.
---

# Delinquency and Collections

## Workflow purpose

Move residents through a documented aging-and-resolution pipeline with zero guesswork about what the next permissible action is, under the governing jurisdiction's rules and the operator's policy overlay. Every transition that could become a legal action opens an `approval_request` at the correct row in the approval matrix. The workflow never sends notices, never files, never commits to a non-standard payment plan, and never writes off without a matching approved record. It does produce drafts, the structured cases, and the sensitivity math to make human decisions fast.

This pack is deliberately load-bearing. Collections discipline is one of the highest-leverage inputs to `economic_occupancy`, `bad_debt_rate`, `noi_margin`, and `dscr`. It is also the area most prone to fair-housing risk, so every stage carries an explicit guardrail.

## Trigger conditions

- **Explicit:** "weekly delinquency review", "delinquency by aging", "payment plan request for unit X", "what's the next step on case Y", "pre-legal case list", "bad-debt write-off candidates".
- **Implicit:** ledger balance transitions an aging bucket; `delinquency_rate_30plus` week-over-week spike above overlay materiality; resident requests a payment plan; a case approaches the jurisdiction's cure-period deadline; write-off date approaches.
- **Recurring:** weekly at property grain for the aging review; daily screen for cases crossing cure-period or court-deadline dates.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Resident ledger (current + T12) | table | required | unit_id, balance, as_of_date, aging bucket |
| DelinquencyCase records | table | required | case_id, stage, opened_date, last_action_date |
| Rent roll snapshot | table | required | unit status, lease state |
| Jurisdiction legal-notice rules | yaml | required | grace period, cure period, notice format rules |
| Delinquency playbook | csv | required | overlay-driven stage-by-stage action matrix |
| Payment-plan policy | yaml | required | max term, min down, cap per unit, off-policy flag criteria |
| Approval thresholds | csv | required | write-off and legal thresholds |
| Fair-housing baseline | derived | optional | trailing approval/collections disparity baseline |
| Prior approval records | table | required | link every gated action to an approved record |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Stage cohort table | `kpi_review` | counts + dollars by aging bucket |
| Per-case action list | `checklist` | case_id, current stage, proposed next step, approval gate, due date |
| Draft communication set | `email_draft` | resident-facing letters per stage with banners |
| Approval request bundle | list | one per gated transition, pre-filled |
| Weekly delinquency memo | `memo` | narrative with fair-housing scan result |
| Confidence banner | banner | reference freshness + status tags |

## Required context

Asset_class, segment, form_factor, lifecycle_stage, management_mode, market, jurisdiction, role. Jurisdiction is **required** — the workflow refuses to propose any notice or filing action without a jurisdiction overlay. If the jurisdiction reference is missing, workflow opens a `missing_docs` entry and routes the case list without proposing legal-stage actions.

## Process

### Step 1. Pull cohorts and tag each case with stage.

Canonical stages (this is the overlay's playbook axis; stages map to the overlay's `delinquency_playbook_middle_market.csv`):

- `current` — ledger balance zero or below the `delinquency_threshold_dollars`; case open only to track recent payment patterns.
- `1_7` — balance above threshold, 1–7 days past due. Most cases resolve themselves here; gentle reminder only.
- `8_30` — 8–30 days past due. Formal reminder, payment offer menu, payment-plan eligibility reviewed.
- `31_60` — 31–60 days past due. Pre-legal posture. Cure period warning if jurisdiction supports. Payment plan must be in place or pre-legal pathway is considered.
- `61_90` — 61–90 days past due. Legal-notice pathway becomes active under most jurisdictions.
- `91_plus` — 91+ days past due. Filing window for most jurisdictions.
- `legal_notice` — a legal notice has been served; case is in cure window.
- `eviction_filed` — filing complete; awaiting court date.
- `judgment` — judgment entered (favorable or adverse); next step is either payment enforcement, move-out, or post-judgment workout.
- `write_off` — case recognized as bad debt per overlay write-off rules; ledger entry scheduled.

### Step 2. Per-case proposed next step (playbook lookup).

For each case, read the playbook row for the case's `(stage, jurisdiction, lease_state, payment_plan_state)` tuple. The playbook returns:

- `proposed_action` (e.g., send_reminder, offer_payment_plan, issue_legal_notice_draft_for_review, file_eviction_draft_for_review, continue_legal_hold, propose_write_off_draft_for_review).
- `approval_gate_row` (if any).
- `communication_template_ref` (path to the draft template).
- `legal_review_required` flag.

No case advances autonomously past a gated row.

### Step 3. Gated transitions — open approvals.

The following transitions always open an `approval_request`, regardless of dollar:

- **Any transition that would issue a legal notice** (moving into `legal_notice` stage, or preparing one in `31_60` / `61_90` / `91_plus`): opens `approval_request` row 1. The request names the jurisdiction, the cure-period deadline, the overlay playbook row, and the template reference. The workflow does not send the notice.
- **Any transition that would file for eviction** (moving into `eviction_filed`): opens `approval_request` row 2. Requires legal counsel sign-off in addition to PM and regional.
- **Any proposed non-standard payment plan** (outside the payment_plan_policy overlay: longer term, lower down, more frequent rescheduling, etc.): opens `approval_request` row 13.
- **Any proposed write-off** at or above the org overlay's threshold: opens row 6 or row 7 depending on threshold band.
- **Any tenant dispute with legal exposure signal** (retaliation claim, fair-housing complaint, reasonable-accommodation / reasonable-modification dispute): opens `approval_request` row 3; resident-facing response draft is not produced without counsel sign-off.

Any action without a matching `approved` record refuses to execute. This is a hard guardrail.

### Step 4. Stage-by-stage playbook (canonical).

The workflow references the overlay's playbook; this section describes the canonical skeleton that overlays customize. Overlays may tighten (faster escalation, more conservative write-off) but may not loosen below the floor described here.

**`current`.** No action required. If a resident shows repeated late-in-cycle payments (late in-month but never over 1–7 days), the workflow notes a pattern flag for the PM, informational only.

**`1_7`.** Informational reminder draft. Template `draft_for_review`. No approval gate. No fair-housing scan beyond routine. The goal is self-cure.

**`8_30`.**
- Formal reminder draft (portal + email).
- Payment-offer menu: full pay, split pay (inside policy), ledger-hold for short window (inside policy).
- Payment-plan eligibility evaluation: if request is **inside** `payment_plan_policy`, no approval gate; the workflow draft-produces the plan for PM confirmation. If request is **outside** policy, opens `approval_request` row 13.
- Auto-payment prompt if failed auto-pay is the cause.
- Fair-housing guardrail: sort by category (unit type, building, resident tenure) and compare action distributions to baseline. Statistically meaningful disparity opens a human-review flag (not autonomous action).

**`31_60`.**
- Pre-legal posture. The draft communication now includes overlay-approved escalation language and the cure-period heads-up if jurisdiction requires. Template carries `legal_review_required` banner.
- If payment plan is in place and in compliance, keep on plan; no escalation.
- If no payment plan or plan in default, proposed action is to prepare a legal-notice draft; that proposal opens `approval_request` row 1.
- Fair-housing guardrail: same disparity scan. Any statistically meaningful disparity routes to regional_manager before any legal-stage draft is opened.

**`61_90`.**
- Legal-notice pathway active under most jurisdictions. The workflow prepares the legal notice draft per the overlay's template. Every legal notice has a `legal_review_required` banner. The notice is never sent; it opens `approval_request` row 1 with the cure-period deadline attached.
- If jurisdiction requires a specific form (e.g., pay-or-quit, cure-or-quit), the overlay's template library is consulted; if the overlay does not cover the jurisdiction, the workflow refuses the legal draft and opens a `missing_docs` ticket. It still produces the informational memo for the PM.
- Payment plan, if any, is reassessed: missed installments move the plan to default, which triggers the `31_60 -> 61_90` path above.

**`91_plus`.**
- Filing pathway active. The workflow prepares an eviction-filing draft per the jurisdiction overlay and opens `approval_request` row 2. Requires legal counsel sign-off.
- Alternative path: if a qualifying workout or payment plan is now in play (overlay allows this to suspend filing), filing preparation is held but row 2 approval is still opened in parallel with a hold note.
- Any resident who raises a legal defense (retaliation, habitability, fair housing, reasonable accommodation) triggers `approval_request` row 3; filing holds pending legal direction.

**`legal_notice`.**
- Case is in cure window. The workflow tracks the cure deadline from the jurisdiction overlay and prepares a cure-verification action for the deadline date.
- Payments received during cure window are applied per overlay rules (full cure vs. partial cure vs. payment-plan-initiated cure).

**`eviction_filed`.**
- Case is in court process. The workflow maintains the case record, tracks hearing dates, and prepares a post-judgment decision brief with scenarios (judgment + payment, judgment + move-out, vacated / dismissed).
- No resident-facing communication is produced without legal direction.

**`judgment`.**
- Post-judgment branch:
  - **Favorable, payment plan proposed:** the workflow prepares a proposed plan per the overlay's post-judgment policy; opens row 13 if the plan is outside overlay.
  - **Favorable, move-out ordered:** hands off to `workflows/move_out_administration` and updates the rent roll; opens the turn project via `workflows/unit_turn_make_ready`.
  - **Adverse / vacated / dismissed:** closes the legal stage; case may return to earlier stages for non-legal workout or may move to `write_off` per overlay.

**`write_off`.**
- Recognizes the balance as bad debt per overlay write-off rules. Opens `approval_request` row 6 or row 7 depending on threshold band. Produces the GL journal draft `draft_for_review`.

### Step 5. Fair-housing guardrails at every stage.

At every stage the workflow:

- Never records, infers, or uses a protected-class attribute in any recommendation. The Fair Housing Act superset is the governing set; the guardrail treats source-of-income, age, marital status, lawful occupation, military status, and the full jurisdiction-specific set as protected.
- Produces no communication with protected-class language; copy is scanned against the term list before any draft is finalized.
- Runs a disparity scan on proposed actions by (aging bucket, unit cluster, tenure). Statistically meaningful disparity is an **informational flag** — never an autonomous action. Flagged cases route to regional_manager.
- Refuses to propose differential enforcement (e.g., faster escalation for one set of cases than another) without an explicit, documented policy justification that is traceable to the overlay.
- Escalates any reasonable-accommodation or reasonable-modification request immediately to human handling; does not route it through this playbook.

### Step 6. Communication drafts and banners.

Every resident-facing draft is `draft_for_review`. Drafts that could constitute notice under the jurisdiction carry `legal_review_required`. Drafts never assert sample data as fact; if a ledger balance or amount owed is cited, the confidence banner surfaces the ledger's `as_of` timestamp and source.

### Step 7. Weekly roll-up and portfolio view.

At the weekly cadence, the workflow produces:

- Aging distribution (count + dollars) by bucket.
- Week-over-week transitions (cases into and out of each bucket).
- `delinquency_rate_30plus`, `collections_rate`, `bad_debt_rate` vs. bands and benchmarks.
- Pattern flags: clusters by building / unit type / lease vintage.
- Fair-housing disparity scan summary.
- Gated-action queue: pending approvals, open cases, deadlines by date.
- Anchors to `economic_occupancy`, `notice_exposure`, and `noi_margin` impact.

### Step 8. Confidence banner.

Surface: jurisdiction overlay `as_of_date`, playbook `as_of_date` and `status`, ledger snapshot timestamp, and fair-housing baseline `as_of_date`. If any required reference is sample-tagged, the output says so.

## Metrics used

`delinquency_rate_30plus`, `collections_rate`, `bad_debt_rate`, `economic_occupancy`, `notice_exposure`. Supporting but not primary: `turnover_rate` (post-judgment move-outs), `average_days_vacant` (collections-related turns).

## Reference files used

- `reference/normalized/collections_benchmarks__{region}_mf.csv`
- `reference/normalized/delinquency_playbook_middle_market.csv`
- `reference/normalized/approval_threshold_defaults.csv`
- `reference/derived/role_kpi_targets.csv`
- `reference/normalized/jurisdiction_legal_notice_rules__{jurisdiction}.yaml`
- `reference/normalized/payment_plan_policy__{org}.yaml`
- `reference/normalized/resident_comm_templates__{jurisdiction}/*.md` (via reference; every template scoped to jurisdiction)

## Escalation points

- Any proposed transition into `legal_notice` or `eviction_filed` -> `approval_request` row 1 or 2.
- Any proposed non-standard payment plan -> `approval_request` row 13.
- Any write-off above threshold -> `approval_request` row 6 or 7.
- Any dispute with legal exposure -> `approval_request` row 3.
- Any missing jurisdiction overlay -> `missing_docs` ticket; workflow refuses to draft legal-stage actions.

## Required approvals

- `legal_notice` (row 1).
- `eviction_filing` (row 2).
- Non-standard payment plan (row 13).
- Write-off at/above threshold (row 6 or 7).
- Tenant dispute with legal exposure (row 3).

## Failure modes

1. Drafting a legal notice for a jurisdiction without an overlay. Fix: overlay missing -> refuse the draft; open `missing_docs`.
2. Treating "delinquency" as a single rate. Fix: always report `delinquency_rate_30plus` plus aging distribution; bad debt separately.
3. Proposing differential enforcement by resident attribute. Fix: the fair-housing scan is mandatory every run; statistically meaningful disparity routes to regional before any enforcement escalation.
4. Sending a template that could constitute notice without legal review. Fix: `legal_review_required` banner is automatic for any stage `31_60` and beyond.
5. Processing a reasonable-accommodation / reasonable-modification request through this playbook. Fix: automatic handoff out of this workflow; humans only.
6. Applying a payment plan without ledger check. Fix: ledger snapshot timestamp must be within overlay freshness threshold; stale ledger refuses.
7. Silent write-off. Fix: every write-off opens an approval; GL journal is a draft until approved.
8. Using sample references as operating fact. Fix: confidence banner surfaces `status` tags; sample rows never authoritative.

## Edge cases

- **First-of-month edge:** auto-pay failures cluster on the 1st–3rd; the `1_7` stage shows a transient spike. Workflow notes the seasonality so the weekly review does not overreact.
- **Resident in bankruptcy:** the workflow refuses to advance the case through any legal-stage transition; opens a `bankruptcy_review` flag and routes to legal counsel immediately. Communication drafts are held.
- **Military deployment (SCRA-protected resident):** the workflow checks for an SCRA flag in the lease record; if present, legal-stage transitions are blocked and counsel is routed.
- **Reasonable accommodation pending:** any open accommodation request suspends collections-stage transitions past `31_60` until resolved; counsel notified.
- **Partial cure during cure window:** jurisdiction overlay governs; if overlay treats partial cure as non-cure, case advances. Workflow does not override overlay.
- **Resident disputes balance in writing:** all communications default to `draft_for_review`; PM verifies ledger before any escalation.
- **TPM-managed property:** the workflow drafts the owner-oversight view and the TPM-facing request; does not bypass the TPM.
- **Multiple residents on lease, one facing workout:** ledger is joint; communications address the lease, not individual residents; fair-housing scan is conservative.

## Example invocations

1. "Run this week's delinquency review for Ashford Park. Include fair-housing scan and list every case that should open an approval this week."
2. "Unit 305 at Willow Creek is 45 days past due. What's the next step and what approvals do I need?"
3. "Build the month-end write-off candidate list for the South End portfolio. Route each to the right approval row based on balance size."

## Example outputs

### Output — Weekly delinquency review (abridged, Ashford Park, week ending 2026-04-12)

**Aging distribution.** Counts and dollars by stage (`current`, `1_7`, `8_30`, `31_60`, `61_90`, `91_plus`, `legal_notice`, `eviction_filed`, `judgment`, `write_off`). Week-over-week movement into/out of each bucket. `delinquency_rate_30plus` within band; `collections_rate` within band; `bad_debt_rate` within band.

**Case actions this week.**

- **3 cases in `8_30`.** Two on in-policy payment plan (no gate). One auto-pay failure; reminder drafted `draft_for_review`.
- **2 cases in `31_60`.** One on compliant plan; hold. One plan in default; pre-legal draft prepared per overlay; `approval_request` row 1 opened with Charlotte jurisdiction overlay cure-period deadline attached.
- **1 case in `61_90`.** Legal notice draft per overlay template; `legal_review_required` banner; `approval_request` row 1 opened.
- **0 cases in `91_plus`.**
- **1 case in `legal_notice` (prior week).** Cure-window tracker shows deadline in 6 days; cure-verification action queued.
- **0 cases in `eviction_filed`, `judgment`.**
- **2 candidate write-offs below threshold:** no gate; GL journal draft prepared.

**Fair-housing scan.** No term-list hits. Disparity scan across aging buckets vs. trailing 90-day baseline within tolerance. All `ApprovalOutcome` rows cite `policy_ref`.

**Approvals opened this week.** Row 1 x 2. Row 13 x 0. Row 6 x 2 (write-off below threshold; informational queue).

**Metric impact.** Pro-forma `economic_occupancy` improvement if all cases cure (dollar range), downside if all escalate (dollar range). Reported as sensitivity, not forecast.

**Confidence banner.** `delinquency_playbook_middle_market@2026-03-31, status=starter`. `jurisdiction_legal_notice_rules__charlotte@2026-02-15, status=sample (operator overlay override pending)`. Ledger snapshot 2026-04-12 08:00 local. Fair-housing baseline T90.

### Output — Single-case action brief (abridged, Unit 305, Willow Creek)

**Case state.** Stage `31_60`. Balance above threshold for 44 days. No active payment plan. Resident contacted 7 days ago, no response.

**Proposed next step.** Open `approval_request` row 1 for jurisdiction pre-legal notice draft per overlay template. Notice not sent until approved. Cure-period deadline computed from jurisdiction overlay.

**Alternative paths.**

- If resident responds with in-policy payment plan, hold the notice preparation; PM confirms plan.
- If resident responds with off-policy request, open `approval_request` row 13 in parallel.
- If resident raises a legal defense (retaliation, habitability, fair housing), stop the escalation and open `approval_request` row 3.

**Fair-housing guardrail.** Proposed action consistent with baseline; no disparity signal. No term-list hits in case notes.

**Confidence banner.** Ledger snapshot current; jurisdiction overlay sample-tagged; playbook starter-tagged.
