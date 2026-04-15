---
name: Lead-to-Lease Funnel Review
slug: lead_to_lease_funnel_review
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Funnel conversion benchmarks, lead-response SLAs, source-mix benchmarks, and marketing
  cost-per-lease norms are overlay-driven and will drift. Target bands are pulled from
  derived references; sample references in starter commits must be replaced with live data
  before the output is treated as operating fact.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [lease_up, stabilized, renovation]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [property_manager, leasing_manager, regional_manager, asset_manager]
  output_types: [kpi_review, operating_review, memo]
  decision_severity_max: recommendation
references:
  reads:
    - reference/normalized/market_rents__{market}_mf.csv
    - reference/normalized/concession_benchmarks__{market}_mf.csv
    - reference/normalized/occupancy_benchmarks__{market}_mf.csv
    - reference/derived/role_kpi_targets.csv
    - reference/derived/funnel_conversion_benchmarks__middle_market.csv
  writes: []
metrics_used:
  - lead_response_time
  - tour_conversion
  - application_conversion
  - approval_rate
  - move_in_conversion
  - leased_occupancy
  - preleased_occupancy
  - notice_exposure
  - concession_rate
escalation_paths:
  - kind: fair_housing_flag
    to: regional_manager -> approval_request(row 3)
  - kind: concession_above_policy
    to: regional_manager -> approval_request(row 13)
  - kind: screening_drift
    to: regional_manager -> compliance_review
approvals_required:
  - concession_above_policy
description: |
  Diagnostic review of the leasing funnel from lead through move-in. Identifies where the
  funnel is breaking (response time, tour conversion, application conversion, approval,
  move-in), quantifies exposure, surfaces fair-housing and screening-drift flags, and
  proposes a remediation plan with owner-specific target bands. Recurring weekly at the
  property level; invoked ad hoc when notice exposure or leased occupancy slips.
---

# Lead-to-Lease Funnel Review

## Workflow purpose

Diagnose each stage of the property's demand-conversion funnel. Compare actuals against overlay-driven target bands. Isolate the binding constraint (lead volume, response, tour conversion, approval friction, or move-in conversion), surface fair-housing and screening-policy flags, and propose concrete actions scoped to the role that invoked the workflow.

## Trigger conditions

- **Explicit:** "run funnel review", "weekly leasing funnel", "tour conversion drop", "pipeline audit", "why aren't we leasing".
- **Implicit:** `leased_occupancy` below band for two consecutive weeks; `notice_exposure` above band; `lead_response_time` median breaches SLA; step-to-step fall-off in CRM changes materially week over week.
- **Recurring:** weekly for every property at `lifecycle in [lease_up, stabilized, renovation]`.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| CRM lead log (T30) | table | required | `inquiry_ts`, `first_contact_ts`, `source`, `status` |
| Tour log (T30) | table | required | `tour_date`, `outcome`, `lead_id` |
| Application log (T30) | table | required | `submitted_date`, `approval_status`, `policy_ref` |
| Lease log (T30) | table | required | `executed_date`, `move_in_date`, `prior_lease_id` |
| Rent roll snapshot | table | required | to compute `leased_occupancy`, `notice_exposure` |
| Market rent reference | csv | required | for `market_to_lease_gap` context |
| Concession policy overlay | yaml | required | concession ceiling and lead_time windows |
| Org overlay target bands | yaml | optional | falls back to `role_kpi_targets.csv` |
| Source-mix cost export | table | optional | marketing spend by source for CPL |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Funnel KPI table | `kpi_review` | row per stage with actual, band, gap, trend |
| Binding constraint finding | `memo` | narrative with cited metrics and proposed actions |
| Fair-housing flag log | appendix | `approval_rate` disparity scan, screening policy deviations |
| Action list | `checklist` | owner, due date, approval gate if any |
| Confidence banner | banner | reference as-of dates and sample-tag surfacing |

## Required context

Router must resolve: asset_class, segment, form_factor, lifecycle_stage, management_mode, role, and at minimum a market. If market is missing, workflow asks before running any market-relative metric.

## Process

1. **Snapshot the funnel (T7 and T30).** Compute, in order, `lead_response_time` (median and p95), `tour_conversion`, `application_conversion`, `approval_rate`, `move_in_conversion`. Add the resulting state metrics: `leased_occupancy`, `preleased_occupancy`, `notice_exposure`.
2. **Compare to target bands.** Pull `reference/derived/role_kpi_targets.csv`; apply any org overlay override. Color-code each stage within/below/above band. Note the reference `as_of_date`.
3. **Identify the binding constraint.** Walk stages in order; the first metric materially outside band (per overlay's materiality threshold) is the binding constraint. If multiple stages are outside band, rank by leverage on `leased_occupancy`.
4. **Fair-housing guardrail scan.**
   - Scan CRM notes, `Lead.preferences`, marketing copy for the protected-class term list. Any hit opens an advisory line; pattern hits open `approval_request` row 3.
   - Compute `approval_rate` trend vs. the trailing 90-day baseline. Statistically meaningful disparity flags for human review (never an autonomous adverse-action decision).
   - Confirm every `ApprovalOutcome` in the sample cites a `policy_ref`. Missing `policy_ref` is a screening-drift finding.
5. **Concession scan.** Compute `concession_rate` on new leases and compare to the concession policy overlay ceiling. Any lease at or above the ceiling is listed; any lease above policy opens an `approval_request` row 13 or verifies an existing one.
6. **Source-mix attribution (if cost data present).** Join leads and tours to marketing source; compute lead-volume share and tour-conversion by source. Route high-cost / low-conversion sources to the leasing manager for reallocation.
7. **Diagnose with branches.**
   - If `lead_response_time` median above SLA -> recommend staffing / coverage review, evaluate autoresponder posture, and flag the top response-time outliers.
   - If `tour_conversion` below band with response-time green -> recommend tour-quality review, shop-call / mystery-shop pull, amenity walk, comp audit.
   - If `application_conversion` below band -> recommend pricing review against `market_to_lease_gap`, concession-posture recheck, friction audit on the application step itself.
   - If `approval_rate` swing > overlay materiality vs. baseline -> route to fair-housing review and screening-policy confirmation; do not propose an ad-hoc change.
   - If `move_in_conversion` below band -> recommend post-approval friction review (unit readiness, keys, welcome package), review `make_ready_days` in coordination with `workflows/unit_turn_make_ready`.
8. **Propose action list.** Each action names an owner, a due date, and the approval gate it must pass (if any). Mark `draft_for_review` for any resident-facing or vendor-facing communication.
9. **Surface confidence banner.** List every reference cited with `as_of_date` and `status` (sample / starter / live). Outputs never cite sample data as operating fact without the tag.

## Metrics used

`lead_response_time`, `tour_conversion`, `application_conversion`, `approval_rate`, `move_in_conversion`, `leased_occupancy`, `preleased_occupancy`, `notice_exposure`, `concession_rate`. `market_to_lease_gap` as a supporting metric when market rent reference present.

## Reference files used

- `reference/normalized/market_rents__{market}_mf.csv`
- `reference/normalized/concession_benchmarks__{market}_mf.csv`
- `reference/normalized/occupancy_benchmarks__{market}_mf.csv`
- `reference/derived/role_kpi_targets.csv`
- `reference/derived/funnel_conversion_benchmarks__middle_market.csv`
- `overlays/segments/middle_market/service_standards.md` (concession policy pointer)

## Escalation points

- Fair-housing hit (term-list match, disparity signal, missing `policy_ref`) routes to regional_manager and opens an `approval_request` row 3 before any resident-facing response is drafted.
- Proposed concession above policy opens `approval_request` row 13.
- If the binding constraint is a screening-policy gap, the workflow hands off to the regional_manager and the `workflows/renewal_retention` / screening-policy review path rather than proposing changes.

## Required approvals

- Any concession action beyond policy (row 13).
- Fair-housing-flagged dispute (row 3) before public-facing response.

## Failure modes

1. Treating "occupancy" as a single number. Fix: always surface `physical_occupancy`, `leased_occupancy`, `economic_occupancy` together; this workflow uses leased as the state reference.
2. Diagnosing from last week only. Fix: T7 and T30 side by side; weight T30 for structural signal.
3. Recommending concession as a first-line remedy. Fix: concessions are a last resort, always route above policy.
4. Missing the fair-housing scan because the funnel "looks normal". Fix: the scan is mandatory every run, not conditional on funnel state.
5. Recommending a screening policy change to close the funnel. Fix: screening criteria live in the screening_policy overlay; workflow never authors ad-hoc screening criteria.
6. Source-mix narrative without cost data. Fix: if marketing spend absent, note the gap and propose to capture cost data rather than inferring CPL.

## Edge cases

- **Lease-up stage:** band targets pulled from lease_up overlay, not stabilized. `stabilization_pace_vs_plan` is the primary state metric; funnel is the mechanism.
- **Renovation stage, unit mix shifting:** exclude classic-to-renovated unit transitions from the `market_to_lease_gap` calc; note the exclusion in the output.
- **Very small property:** if weekly sample is below `minimum_lead_volume` (from overlay), widen to T30 and annotate low-sample confidence.
- **TPM-managed property:** the workflow produces owner-oversight view and TPM-facing data request if data is missing; never bypasses the TPM.
- **New property (no 90-day history):** disparity scan uses portfolio baseline; `confidence: low` banner applied.

## Example invocations

1. "Run the weekly funnel review for Ashford Park; flag anything below band."
2. "Tours are down at Willow Creek. Diagnose which funnel stage is breaking and propose actions."
3. "Build a May-1-2026 funnel scorecard for the South End portfolio (three assets) with source mix attribution."

## Example outputs

### Output — Funnel review (abridged, week ending 2026-04-12, Ashford Park)

**Funnel KPI table.**

| Stage | Metric | T7 | T30 | Band | Gap | Trend |
|---|---|---|---|---|---|---|
| Response | `lead_response_time` p50 | within | within | (overlay) | zero | flat |
| Tour | `tour_conversion` | within | below | (overlay) | below | declining |
| Application | `application_conversion` | within | within | (overlay) | zero | flat |
| Approval | `approval_rate` | within | within | (overlay) | zero | flat |
| Move-in | `move_in_conversion` | within | within | (overlay) | zero | flat |
| State | `leased_occupancy` | below | below | (overlay) | below | declining |

**Binding constraint.** `tour_conversion` on the T30 view, dragging `leased_occupancy` below band.

**Actions.**

- Tour-quality audit this week (owner: leasing_manager; due: Friday; no approval gate).
- Mystery-shop pull (owner: regional_manager; due: Friday; no approval gate).
- Comp audit invoked via `workflows/market_rent_refresh` (owner: property_manager; due: 10 days; no approval gate).
- No concession action proposed.

**Fair-housing scan.** No term-list hits. `approval_rate` within baseline tolerance. All `ApprovalOutcome` rows in sample cite `policy_ref`.

**Approval requests opened.** None.

**Confidence banner.** `funnel_conversion_benchmarks__middle_market.csv@as_of=2026-03-31, status=sample`. `market_rents__charlotte_mf.csv@as_of=2026-03-31, status=sample`. Funnel data live CRM through 2026-04-12 08:00 local.
