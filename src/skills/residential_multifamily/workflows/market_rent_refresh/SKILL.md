---
name: Market Rent Refresh
slug: market_rent_refresh
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Market references drift constantly. Staleness threshold per category lives in overlays.
  The refresh builds a bundle and hands off to `workflows/rent_comp_intake` for ingestion;
  it does not directly author benchmarks without the intake workflow's normalization and
  approval steps.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [stabilized, renovation, lease_up, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [property_manager, leasing_manager, regional_manager, asset_manager]
  output_types: [checklist, memo, kpi_review]
  decision_severity_max: recommendation
references:
  reads:
    - reference/normalized/market_rents__{market}_mf.csv
    - reference/normalized/concession_benchmarks__{market}_mf.csv
    - reference/normalized/comp_normalization_rules__middle_market.yaml
  writes: []
metrics_used:
  - market_to_lease_gap
  - loss_to_lease
  - rent_growth_new_lease
  - rent_growth_renewal
  - concession_rate
escalation_paths:
  - kind: stale_reference
    to: property_manager -> regional_manager (refresh responsibility)
  - kind: comp_magnitude_change
    to: regional_manager -> asset_manager (via rent_comp_intake)
approvals_required:
  - market_rent_reference_update_above_magnitude_delta
description: |
  Checks freshness of market rent and concession references against overlay staleness
  threshold; organizes a refresh plan (comp sources, shop list, 3rd-party export, submarket
  coverage); produces the intake bundle for `workflows/rent_comp_intake` to process.
  Outputs a current-state memo and a refreshed benchmark view on completion.
---

# Market Rent Refresh

## Workflow purpose

Keep market rent and concession benchmarks fresh. Detect staleness per overlay threshold, organize a refresh (shopped comps, 3rd-party export, operator-reported), and hand off the resulting bundle to `workflows/rent_comp_intake`. Output a current-state view for renewal and pricing decisions.

## Trigger conditions

- **Explicit:** "refresh market rents for X market", "shop comps for submarket Y", "quarterly market survey".
- **Implicit:** reference `as_of_date` older than overlay staleness threshold; renewal or funnel workflow cites stale benchmark; supply event (new delivery) in submarket.
- **Recurring:** quarterly per market; ad hoc when a trigger fires.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Current benchmark files | csv | required | freshness check |
| Shop list | list | required | properties to survey |
| 3rd-party exports | table | optional | where available |
| Operator-reported inputs | list | optional | from PM/leasing |
| Submarket definitions | yaml | required | |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Freshness status | `kpi_review` | per market/submarket reference as_of_date |
| Refresh plan | `checklist` | sources, dates, owners |
| Current-state memo | `memo` | market and concession snapshot |
| Comp bundle | handoff | passed to `workflows/rent_comp_intake` |

## Required context

Asset_class, segment, market, submarket.

## Process

1. **Freshness check.** Scan all benchmarks for the market; identify stale per overlay.
2. **Refresh plan.** For each stale reference, define sources; assign owners and dates.
3. **Collect comps.** Produce raw bundle; hand off to `workflows/rent_comp_intake` for normalization and approval.
4. **Current-state memo.** Market trend narrative with cited sources; no proposed reference changes here (intake owns those).
5. **Downstream notification.** Packs whose reference_manifest reads these files are notified of update.
6. **Confidence banner.** All references surfaced with `as_of_date` and `status`.

## Metrics used

`market_to_lease_gap`, `loss_to_lease`, `rent_growth_new_lease`, `rent_growth_renewal`, `concession_rate` — consumed by downstream workflows.

## Reference files used

- `reference/normalized/market_rents__{market}_mf.csv`
- `reference/normalized/concession_benchmarks__{market}_mf.csv`
- `reference/normalized/comp_normalization_rules__middle_market.yaml`

## Escalation points

- Stale reference: PM -> regional; refresh owner identified.
- Comp magnitude change routed via `workflows/rent_comp_intake`.

## Required approvals

- Handled via `workflows/rent_comp_intake` (delta-gated).

## Failure modes

1. Refresh without normalization. Fix: intake workflow owns normalization.
2. Memo asserting new benchmarks before approval. Fix: memo reports current state; intake proposes updates.
3. Missing submarket coverage. Fix: refresh plan enumerates submarkets explicitly.

## Edge cases

- **New supply delivery mid-survey:** note in memo; additional comp capture if overlay threshold crossed.
- **Market with few comps:** note sparse-sample confidence; operator-reported weighted lower.
- **Concession-heavy market:** effective rent view emphasized.

## Example invocations

1. "Refresh Charlotte market rents; staleness threshold crossed."
2. "Shop five South End properties and route the bundle to intake."
3. "Build the current-state market memo for South End."

## Example outputs

### Output — Market rent refresh plan (abridged, Charlotte South End)

**Freshness status.** Market rent benchmark `as_of` older than overlay threshold; concession benchmark within threshold.

**Refresh plan.** Five properties to shop (owners and dates); 3rd-party export already requested.

**Bundle handoff.** Collected comps sent to `workflows/rent_comp_intake`.

**Current-state memo.** Trend narrative with cited sources; no direct benchmark updates here.

**Confidence banner.** `market_rents__charlotte_mf@2026-03-31 (stale per overlay), status=sample`. Comp sources surfaced per record.
