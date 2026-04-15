---
name: Renewal and Retention
slug: renewal_retention
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Renewal-offer uplift bands, retention conversion benchmarks, concession posture, and
  jurisdiction-specific renewal-notice timing all drift. Uplift bands are overlay-driven.
  Renewal-notice language is jurisdiction-specific and carries a legal_review_required
  banner when the template is invoked.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [stabilized, renovation, lease_up]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [property_manager, leasing_manager, regional_manager, asset_manager]
  output_types: [memo, kpi_review, email_draft, checklist]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/normalized/market_rents__{market}_mf.csv
    - reference/normalized/concession_benchmarks__{market}_mf.csv
    - reference/derived/role_kpi_targets.csv
    - reference/derived/renewal_uplift_bands__middle_market.csv
    - reference/normalized/approval_threshold_defaults.csv
  writes: []
metrics_used:
  - renewal_offer_rate
  - renewal_acceptance_rate
  - rent_growth_renewal
  - renewal_rent_delta_dollars
  - blended_lease_trade_out
  - market_to_lease_gap
  - loss_to_lease
  - concession_rate
  - turnover_rate
  - average_days_vacant
escalation_paths:
  - kind: renewal_above_policy
    to: regional_manager -> approval_request(row 13)
  - kind: non_renewal_notice
    to: property_manager + regional_manager -> approval_request(row 1) if jurisdiction treats as notice
  - kind: fair_housing_flag
    to: approval_request(row 3)
approvals_required:
  - concession_above_policy
  - non_standard_payment_plan
description: |
  Plans, prices, and executes the renewal cycle for leases in the renewal-offer window.
  Segments expiring leases into pricing tiers, computes per-tier offers using
  market_to_lease_gap and prior effective rent, checks every offer against policy bands,
  and produces a draft communication set with all legal-notice templates flagged for
  review. Guards against retention through concession creep. Runs monthly at the property
  and per-tagged trigger when a lease enters its renewal-offer window.
---

# Renewal and Retention

## Workflow purpose

Turn the expiring-lease population into a priced renewal plan that (1) offers every resident a renewal inside the overlay's lead-time window, (2) prices each offer using `market_to_lease_gap` and the resident's prior effective rent, (3) routes any offer outside policy for approval before send, (4) draft-produces resident communications for review, and (5) tracks acceptance through to executed renewal with a loop back to retention-NPV logic when refusals cluster.

## Trigger conditions

- **Explicit:** "build renewal strategy", "renewal plan for June", "price renewals for Ashford Park", "retention plan".
- **Implicit:** lease with `end_date` within `renewal_offer_lead_time` and no renewal_offered event; `renewal_offer_rate` below target band; `renewal_acceptance_rate` trend declining over trailing 90 days.
- **Recurring:** monthly, one calendar-window ahead (e.g., April build for July expirations) at property grain.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Expiring-lease list | table | required | lease_id, end_date, current effective rent, unit_type, resident tenure |
| Rent roll snapshot | table | required | for `loss_to_lease`, `market_to_lease_gap` |
| Market rent reference | csv | required | by unit_type and submarket |
| Concession policy overlay | yaml | required | ceiling and cases allowed |
| Renewal uplift bands | csv | required | overlay-driven per segment / market |
| Resident ledger (T12) | table | optional | payment history informing retention-NPV case |
| Turn cost reference | csv | optional | per-unit turn cost for refusal-case NPV |
| Jurisdiction notice rules | yaml | optional | flags whether renewal notice is statutory |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Renewal segmentation table | table | lease_id, tier, prior effective rent, market rent, proposed offer, band, gap |
| Renewal strategy memo | `memo` | narrative with blended uplift, expected acceptance, budget impact |
| Draft resident communication set | `email_draft` | per-lease letter templates, `legal_review_required` where statutory |
| Approval request bundle | list | any offer outside policy band |
| Acceptance tracker | `checklist` | follow-up cadence, due dates |

## Required context

Asset_class, segment, form_factor, lifecycle_stage, management_mode, market, role. The workflow refuses to price without a market rent reference; if absent, routes to `workflows/market_rent_refresh` first.

## Process

1. **Pull expiring-lease population.** Include leases with `end_date` within the overlay's `renewal_offer_lead_time`. Exclude transfers (same household, new unit — handled separately). Annotate residents with tenure, payment record flag (from ledger if provided), and unit turn scope tag (classic vs. renovated).
2. **Compute market rent per unit.** Use `reference/normalized/market_rents__{market}_mf.csv` with submarket and unit_type keys. Compute `market_to_lease_gap` per lease and the property's weighted `loss_to_lease`.
3. **Segment into tiers (decision point).**
   - **Tier A:** in-place effective rent > market (negative `market_to_lease_gap`). Default offer: flat or overlay-defined decrease to retain; case-by-case concession review only.
   - **Tier B:** in-place rent within overlay's band of market. Default offer: median overlay renewal uplift.
   - **Tier C:** in-place rent < market by more than overlay's threshold. Default offer: closer-to-market uplift, with a short-term option for negotiation room.
   - **Tier D (flag only):** payment-record flag, lease-compliance flag, or non-renewal signal from ops. These are not priced in this workflow; they route to the PM for human decision and, if a non-renewal is contemplated, approval gate row 1 opens when jurisdiction treats non-renewal as notice.
4. **Check every offer against policy bands.** Any offer whose uplift falls outside the overlay's renewal uplift band requires `approval_request` row 13. Any offer with a concession exceeds policy also requires row 13. Both open automatically; the workflow does not send.
5. **Fair-housing guardrail scan.** Scan for systematic differential pricing by unit cluster that correlates with protected-class proxies (unit size, building location). Surface statistical outliers for regional review; never propose corrective pricing on a protected-class basis.
6. **Acceptance estimation.** Compute expected `renewal_acceptance_rate` by tier using overlay bands and the property's trailing 90-day baseline. Express downside: if Tier B refusal rate rises X points, expected `turnover_rate`, `average_days_vacant`, and `blended_lease_trade_out` shift; show the sensitivity.
7. **Retention-NPV check (decision point).**
   - If Tier C refusal case would produce a weighted turn cost + vacancy + new-lease trade-out loss that exceeds the dollar value of the accepted uplift, the workflow proposes a softer Tier C offer inside policy before recommending the stretch offer.
   - If the softer offer is still refused on historical data, flag the NPV gap and route to regional_manager for a human call; do not resolve autonomously.
8. **Draft communication set.** Produce per-lease renewal letters with `draft_for_review` banner. Mark `legal_review_required` on any letter whose jurisdiction treats renewal notice (or rent-increase notice) as statutory. Include a portal-message variant and an email variant.
9. **Approval routing.** Bundle every offer requiring `approval_request` row 13 into a single approval packet for the regional_manager, with per-lease rationale and sensitivity numbers. Executor does not send until approvals return `approved`.
10. **Acceptance tracking.** Produce a follow-up checklist: offer sent -> response due -> second nudge window -> non-renewal decision date. Include the PM's response SLA.
11. **Confidence banner.** Surface reference `as_of_date` and `status` tags. Note that jurisdiction-specific rules are overlay-driven.

## Metrics used

`renewal_offer_rate`, `renewal_acceptance_rate`, `rent_growth_renewal`, `renewal_rent_delta_dollars`, `blended_lease_trade_out`, `market_to_lease_gap`, `loss_to_lease`, `concession_rate`, `turnover_rate`, `average_days_vacant`.

## Reference files used

- `reference/normalized/market_rents__{market}_mf.csv`
- `reference/normalized/concession_benchmarks__{market}_mf.csv`
- `reference/derived/role_kpi_targets.csv`
- `reference/derived/renewal_uplift_bands__middle_market.csv`
- `reference/normalized/approval_threshold_defaults.csv`
- `overlays/segments/middle_market/service_standards.md`

## Escalation points

- Any offer above policy uplift band -> `approval_request` row 13.
- Any concession above policy -> `approval_request` row 13.
- Non-renewal contemplated where jurisdiction treats non-renewal as statutory notice -> `approval_request` row 1.
- Fair-housing disparity signal -> `approval_request` row 3.

## Required approvals

- Concession above policy (row 13).
- Non-standard payment plan attached to a renewal (row 13).
- Jurisdictional non-renewal notice (row 1 if statutory).

## Failure modes

1. Blanket concessions to hit acceptance rate. Fix: every concession is per-lease and routes above policy.
2. Pricing on last quarter's market. Fix: market rent reference is required; stale references (> overlay threshold) force a `workflows/market_rent_refresh` before the workflow runs.
3. Sending letters that are statutory notices without legal review. Fix: `legal_review_required` banner mandatory in jurisdictions that treat renewal notice as notice.
4. Using payment-history flags as a screening proxy. Fix: ledger data is only used in NPV math and PM handoff, not as a pricing input.
5. Over-indexing on acceptance rate, ignoring `blended_lease_trade_out`. Fix: report acceptance and trade-out together; tier breakouts show the trade-off.
6. Silent sample-data usage. Fix: confidence banner surfaces status tags; sample rows never presented as operating fact.

## Edge cases

- **Short-term lease-up property:** use a tighter uplift band (lease-up overlay) and flag when renewal uplift would undermine stabilization pace.
- **Renovation unit recently delivered:** renewal pricing must reflect renovation unit type; exclude pre-renovation leases from benchmarking.
- **Resident in active workout or partial payment plan:** route to PM; renewal offer conditional on plan resolution.
- **Notice already filed (non-renewal in process):** exclude from renewal plan; appears in `workflows/move_out_administration` instead.
- **Very small expiring cohort (< overlay minimum):** run the plan but annotate low-sample confidence.

## Example invocations

1. "Build the June renewal plan for Ashford Park, 28 expirations. Stay inside policy on concessions."
2. "Retention is softening in Willow Creek. Produce a renewal memo with tiering and sensitivity, flag any NPV gaps."
3. "Price renewal offers for the 14 leases expiring August at Riverbend. Draft the resident letters and route anything above policy."

## Example outputs

### Output — Renewal plan (abridged, Ashford Park, 28 leases expiring 2026-06)

**Summary.** 28 expirations segmented A / B / C / D. Weighted `market_to_lease_gap` at property: within band. Expected `renewal_acceptance_rate` consistent with trailing 90-day baseline.

**Segmentation.**

- Tier A (8 leases): in-place > market. Proposed offer: flat with explicit decline option; no concession proposed.
- Tier B (13 leases): in-place within band of market. Proposed offer: median overlay renewal uplift; no concession.
- Tier C (5 leases): in-place < market by more than overlay threshold. Proposed offer: closer-to-market; short-term option as counter.
- Tier D (2 leases): payment-flag / compliance-flag. Handed to PM for decision; not priced here.

**Approvals.** No Tier B / C offers outside band. Two Tier A cases carry an overlay-permitted minor decrease; within policy. Zero `approval_request` row 13 opened.

**Communications.** 28 resident letters drafted with `draft_for_review`; 0 marked `legal_review_required` (jurisdiction overlay: Charlotte does not treat renewal notice as statutory). Portal-message variant produced for each.

**Sensitivity.** If Tier B acceptance falls 5 points vs. baseline, `blended_lease_trade_out` softens and expected incremental vacancy drives turn cost and lost rent per the reference library; memo shows the dollar impact.

**Confidence banner.** `market_rents__charlotte_mf@as_of=2026-03-31, status=sample`. `renewal_uplift_bands__middle_market@as_of=2026-03-31, status=starter`.
