---
name: Bid Leveling and Procurement Review
slug: bid_leveling_procurement_review
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Bid leveling norms (allowances, exclusions, alternates posture) differ by trade and
  market. Preferred-vendor licensure and insurance freshness drives disqualification at
  leveling; stale cert data must refuse preferred status. Overlay defines acceptable
  ranges; every numeric threshold is overlay-driven.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [stabilized, renovation, lease_up, recap_support, development, construction]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [estimator_preconstruction_lead, construction_manager, asset_manager, development_manager]
  output_types: [memo, estimate, kpi_review]
  decision_severity_max: action_requires_approval
references:
  reads:
    - reference/normalized/capex_line_items__{scope}.csv
    - reference/normalized/labor_rates__{market}.csv
    - reference/normalized/material_costs__{region}_residential.csv
    - reference/normalized/approved_vendor_list__{market}.csv
    - reference/normalized/vendor_rate_cards__{market}.csv
    - reference/derived/contingency_assumptions__{org}.csv
    - reference/normalized/approval_threshold_defaults.csv
  writes: []
metrics_used:
  - trade_buyout_variance
  - dev_cost_per_unit
  - dev_cost_per_gsf
  - dev_cost_per_nrsf
  - contingency_remaining
  - change_orders_pct_of_contract
escalation_paths:
  - kind: bid_award
    to: construction_manager + asset_manager -> approval_request(row 9)
  - kind: bid_award_major
    to: construction_manager + asset_manager + development/executive -> approval_request(row 9)
  - kind: vendor_contract_signature
    to: asset_manager -> legal -> approval_request(row 19)
  - kind: scope_clarification
    to: estimator_preconstruction_lead -> construction_manager
approvals_required:
  - bid_award
  - vendor_contract_signature
description: |
  Normalizes and levels bids received for a defined scope. Performs apples-to-apples
  comparison across bidders by adjusting for included/excluded scope, allowances,
  alternates, and qualifications. Produces the level sheet, the recommended award, the
  scope clarification list, and the approval path. Every award opens a gate regardless of
  dollar (approval matrix row 9).
---

# Bid Leveling and Procurement Review

## Workflow purpose

Turn a set of incoming bids into a comparable, defensible award recommendation. Every award opens an approval gate. Vendor licensure and insurance freshness gate preferred status. Scope clarifications are explicit, not tucked into narrative. The workflow produces the level sheet that humans sign off against — and it refuses to recommend an award that cannot be traced to the bidder's actual scope.

## Trigger conditions

- **Explicit:** "level bids for project X", "review bids for trade Y", "procurement review", "award recommendation".
- **Implicit:** bid package due date passes; estimator flags leveling-ready; capex project has bids in hand.
- **Recurring:** per project; per trade buyout cycle.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Scope statement | memo | required | authoritative scope basis |
| Bid submissions | docs | required | per bidder; PDF or structured |
| Estimator baseline | estimate | required | from `workflows/capex_estimate_generation` |
| Approved vendor list | csv | required | |
| Vendor rate cards | csv | required | |
| Vendor license/insurance status | table | required | freshness check |
| Contingency overlay | csv | required | |
| Approval thresholds | csv | required | |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Level sheet | table | line items x bidders, normalized totals |
| Scope clarification list | `checklist` | open questions per bidder |
| Qualifications summary | table | alternates, exclusions, allowances, exceptions |
| Recommended award memo | `memo` | rationale, risk, comparison to estimator baseline |
| Vendor verification status | table | license, insurance freshness per bidder |
| Approval request | request | row 9; row 19 if contract signature |

## Required context

Asset_class, segment, form_factor, market, and loan context (for covenant sensitivity if the trade is large).

## Process

### Step 1. Confirm scope basis.

Before leveling, the workflow verifies that the scope statement is authoritative (latest drawings, specs, assemblies). Bidders must be bidding to the same scope. If any bidder is clearly bidding off a different scope, workflow opens a scope clarification line and suspends their normalization until resolved.

### Step 2. Normalize each bid.

For each bid:

- Extract line items aligned to estimator's assembly structure.
- Map allowances, alternates, and exclusions; normalize to a comparable basis.
- Apply vendor rate card references where bid is silent on rate.
- Surface qualifications and exceptions.
- Compute a normalized total assuming same scope.

### Step 3. Level sheet compile.

Produce a side-by-side level sheet:

- Columns: estimator baseline, each bidder (normalized total), each bidder (as-submitted total).
- Rows: line items by assembly.
- Variance column per bidder vs. estimator.
- `trade_buyout_variance` computed vs. estimator baseline.

### Step 4. Vendor verification (gate).

For each bidder:

- Approved vendor list membership.
- License and insurance freshness per current overlay.
- Prior performance from `workflows/vendor_dispatch_sla_review` scorecard.

Any bidder with stale licensure or insurance is marked ineligible for award. The workflow never recommends award to an ineligible bidder. (Emergency dispatch exception is not available at bid stage.)

### Step 5. Scope clarification list.

Enumerate open questions that must be answered before award:

- Ambiguous inclusions/exclusions per bidder.
- Alternates requiring decision (add, reject, deferred).
- Allowance adequacy vs. scope.
- Schedule assumptions.
- Payment terms vs. overlay.
- Retainage, lien-release terms.

No bid moves to award recommendation with open red-flag clarifications.

### Step 6. Recommended award (decision point).

Rank eligible bidders by:

- Normalized total.
- Scope completeness.
- Schedule fit.
- Performance history (scorecard).
- Qualifications risk.

Propose a recommended award. The workflow does not "select a winner" autonomously; the recommendation is presented with the level sheet and opens `approval_request` row 9.

If the recommendation is **not** the lowest normalized bidder, the memo explicitly justifies (performance, schedule, scope risk, supplier concentration).

### Step 7. Contingency and allowances re-check.

Compare the award package's embedded allowances against overlay contingency assumption. Recommend project-level contingency adjustment if buyout consumes more/less than planned.

### Step 8. Approval path.

- Every bid award opens `approval_request` row 9. Construction_manager + asset_manager minimum; for majors, add development or executive per overlay.
- Contract signature opens row 19 (legal + asset_manager or portfolio_manager).
- Nothing is signed or committed until approvals return `approved`.

### Step 9. Scope lock.

On approved award, the workflow writes a scope-lock record. Subsequent scope changes flow through `workflows/change_order_review`.

### Step 10. Confidence banner.

Surface each reference's `as_of_date` and `status`. Vendor cert freshness is explicit. Estimator baseline `as_of_date` surfaced; if stale, the workflow flags but does not refuse (human decides whether to re-estimate).

## Metrics used

`trade_buyout_variance`, `dev_cost_per_unit`, `dev_cost_per_gsf`, `dev_cost_per_nrsf`, `contingency_remaining`, `change_orders_pct_of_contract` (as downstream risk anchor).

## Reference files used

- `reference/normalized/capex_line_items__{scope}.csv`
- `reference/normalized/labor_rates__{market}.csv`
- `reference/normalized/material_costs__{region}_residential.csv`
- `reference/normalized/approved_vendor_list__{market}.csv`
- `reference/normalized/vendor_rate_cards__{market}.csv`
- `reference/derived/contingency_assumptions__{org}.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Escalation points

- Bid award: `approval_request` row 9.
- Major bid award: row 9 with added approver (development / executive per overlay).
- Contract signature: row 19.
- Scope ambiguity: estimator -> construction_manager.
- Licensure or insurance freshness failure: bidder disqualified; workflow notifies.
- Trade buyout variance above overlay threshold: construction_manager + asset_manager review before award.

## Required approvals

- Bid award (row 9) always.
- Contract signature (row 19).
- Any overlay-added approver for major projects.

## Failure modes

1. Awarding on as-submitted total without normalization. Fix: normalized total is the comparison basis.
2. Recommending a bidder with stale certs. Fix: licensure/insurance gate is automatic.
3. Carrying open clarifications into award. Fix: clarifications must close before award recommendation.
4. Not recomputing contingency post-buyout. Fix: step is mandatory.
5. Lowest-bid selection without risk memo when not recommended. Fix: non-lowest recommendation requires explicit justification.
6. Silent scope change post-award. Fix: scope-lock record handed to change-order review.
7. Sample reference data treated as authoritative. Fix: confidence banner surfaces `status`.

## Edge cases

- **Single-bid situation:** workflow allows the level sheet but flags single-source risk; overlay may require justification or additional bid solicitation.
- **Bidder conflicts (commonly-owned entities):** flagged; disclosure check; overlay governs.
- **Design-assist scope (pricing with incomplete design):** level sheet separated into committed and allowance; proposed post-design re-level.
- **Unit pricing contracts (vs. lump sum):** unit pricing preserved; assumptions documented.
- **Package with self-perform portion:** self-perform portion treated as estimate, not bid; disclosure in memo.
- **International / unusual-currency bid (unlikely for U.S. residential but conservative):** currency normalization with cited rate and date.

## Example invocations

1. "Level the three bids received for the Ashford Park roof replacement and recommend award."
2. "Review the bids for unit renovation cohort 2 at Willow Creek; 4 bidders."
3. "Buyout review for the amenity refresh at Riverbend."

## Example outputs

### Output — Bid leveling recommendation (abridged, roof replacement Ashford Park)

**Scope confirmation.** Basis document version 2.3, dated 2026-03-15, referenced by all bidders.

**Level sheet.** Columns for estimator baseline and three bidders (as-submitted + normalized); variances computed; `trade_buyout_variance` per bidder.

**Vendor verification.** Bidder A: insurance and license current, SLA performance above band. Bidder B: license expiring within overlay window (flagged). Bidder C: insurance lapsed (ineligible; disqualified for award).

**Scope clarification list.** Two open items for Bidder A; one for Bidder B.

**Recommended award.** Bidder A, pending clarification closure. Rationale: normalized total competitive, performance band, schedule fit. Bidder B is lower on normalized total but license expiry flag; if refreshed pre-award, reconsideration.

**Contingency re-check.** Buyout consumes less than overlay contingency; project-level contingency adjustment not recommended.

**Approvals.** `approval_request` row 9 opened for Bidder A pending clarification closure. Row 19 queued for contract signature.

**Confidence banner.** `capex_line_items__roofing@2026-03-31, status=starter`. `labor_rates__charlotte@2026-03-31, status=sample`. `approved_vendor_list__charlotte@2026-04-01, status=starter`. Per-bidder cert freshness surfaced.

### Output — Bid leveling short-form (abridged, single trade)

**Scope basis.** Confirmed.

**Bidders.** Three; all eligible.

**Level.** Normalized totals tight; variance within overlay band.

**Clarifications.** None material.

**Recommendation.** Lowest normalized bidder; rationale anchored to scope completeness and schedule fit.

**Approvals.** Row 9 opened.

**Confidence banner.** References surfaced.
