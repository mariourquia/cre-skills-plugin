---
name: Rent Comp Intake
slug: rent_comp_intake
version: 0.1.0
status: draft
category: residential_multifamily
subsystem: residential_multifamily
pack_type: workflow
targets:
  - claude_code
stale_data: |
  Comp records have short shelf life; market changes quickly. Confidence tags and source
  types (operator-reported, 3rd-party, shopped) are tracked per record. Normalization
  rules (concession adjustments, unit-type normalization) live in overlays.
applies_to:
  segment: [middle_market]
  form_factor: [garden, walk_up, wrap, suburban_mid_rise, urban_mid_rise]
  lifecycle: [stabilized, renovation, lease_up, recap_support]
  management_mode: [self_managed, third_party_managed, owner_oversight]
  role: [property_manager, leasing_manager, regional_manager, asset_manager]
  output_types: [checklist, memo]
  decision_severity_max: recommendation
references:
  reads:
    - reference/raw/rent_comp/
    - reference/normalized/market_rents__{market}_mf.csv
    - reference/normalized/comp_normalization_rules__middle_market.yaml
  writes:
    - reference/raw/rent_comp/
    - reference/normalized/market_rents__{market}_mf.csv
metrics_used:
  - market_to_lease_gap
  - loss_to_lease
escalation_paths:
  - kind: comp_magnitude_change
    to: regional_manager -> asset_manager -> approval_request per reference update flow
  - kind: source_integrity
    to: regional_manager (source verification)
approvals_required:
  - market_rent_reference_update_above_magnitude_delta
description: |
  Ingests inbound rent comp observations (shopped, 3rd-party, operator-reported), validates,
  normalizes, proposes updates to market_rent_benchmark files, and opens an approval if
  the magnitude delta crosses the overlay threshold. Follows the reference update flow
  end to end.
---

# Rent Comp Intake

## Workflow purpose

Take a raw rent comp observation and move it through the reference layer's update flow so market rent benchmarks stay live. Ingest, validate, normalize, propose, approve (when needed), derive.

## Trigger conditions

- **Explicit:** "I shopped X property; capture comps", "new 3rd-party export", "log comps from call".
- **Implicit:** `workflows/market_rent_refresh` detects a comp bundle; PM drops raw data into `reference/raw/rent_comp/`.
- **Recurring:** ad hoc; any market-survey cycle.

## Inputs (required / optional)

| Input | Type | Required | Notes |
|---|---|---|---|
| Raw comp records | table / json | required | property, unit_type, asking rent, concessions, source |
| Normalization rules | yaml | required | overlay |
| Current market_rent_benchmark | csv | required | to compute delta |

## Outputs

| Output | Type | Shape |
|---|---|---|
| Validated raw records | file | `reference/raw/rent_comp/<yyyy>/<mm>/` |
| Normalized records | file | `reference/normalized/market_rents__{market}_mf.csv` |
| Change log entries | file | append to `archives/change_log.jsonl` |
| Approval request (if above threshold) | request | per overlay delta rule |

## Required context

Asset_class, segment, market, submarket.

## Process

1. **Validation.** Every raw record validated against `_core/schemas/reference_record.yaml` + category schema. Missing fields surfaced.
2. **Normalization.** Apply overlay rules: concession adjustments, unit-type normalization, effective rent math.
3. **Magnitude delta check.** Compare proposed normalized value to current benchmark. If delta above overlay threshold, open `approval_request` per reference update flow before promoting `status=approved`.
4. **Promote to normalized file.** Upsert with `prior_reference_id` linkage; `status=proposed` if gated or auto `approved` otherwise.
5. **Derived recomputation.** Trigger re-derive of any `derived/` file that depends on this category.
6. **Change log entry.** Append to `archives/change_log.jsonl` with old/new, source, confidence, proposer/approver.
7. **Source integrity check.** Verify source_type and source_date; sample-tagged sources never promote to `approved` autonomously.
8. **Confidence banner.** Record `as_of_date` and `status` on the normalized record.

## Metrics used

None directly. Feeds metrics that rely on `market_rent_benchmark`: `market_to_lease_gap`, `loss_to_lease`, `rent_growth_new_lease`.

## Reference files used

- `reference/raw/rent_comp/`
- `reference/normalized/market_rents__{market}_mf.csv`
- `reference/normalized/comp_normalization_rules__middle_market.yaml`

## Escalation points

- Magnitude delta above threshold: regional / AM per reference flow.
- Source integrity concern (unverified source, stale date): regional verification.

## Required approvals

- Market rent reference update above delta threshold (per reference update flow).

## Failure modes

1. Promoting shopped comps without concession normalization. Fix: normalization rules overlay governs.
2. Using sample-tagged third-party data as approved. Fix: sample never auto-approved.
3. Skipping the derived recomputation. Fix: step is mandatory on every normalized update.
4. Silent overwrite of prior record. Fix: `prior_reference_id` linkage.

## Edge cases

- **Conflicting comps from two sources:** surface both; overlay may prefer higher-confidence source; operator resolves.
- **Comp for unit type not in benchmark:** new row; operator decides whether to add unit type to benchmark.
- **Concession-heavy new supply:** effective rent math must apply; surface nominal and effective.

## Example invocations

1. "Log the shopped comps from the Charlotte South End tour."
2. "Ingest the latest 3rd-party export and propose updates."
3. "Update the Ashford Park submarket benchmark with these three comps."

## Example outputs

### Output — Rent comp intake (abridged, three comps for South End)

**Validation.** All three records pass schema.

**Normalization.** Applied concession and unit-type normalization per overlay.

**Delta check.** One comp produces a magnitude delta above overlay threshold; `approval_request` opened per reference update flow.

**Normalized file.** Two records upserted as `approved`; one held as `proposed` pending approval.

**Change log.** Three entries appended.

**Derived.** `market_to_lease_gap` recomputation triggered; downstream skills notified.

**Confidence banner.** `comp_normalization_rules__middle_market@2026-03-31, status=starter`. Raw source types surfaced per record.
