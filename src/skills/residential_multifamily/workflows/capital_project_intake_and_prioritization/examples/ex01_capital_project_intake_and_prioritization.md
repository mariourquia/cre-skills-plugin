# Example — Capex Intake and Prioritization (abridged)

**Prompt:** "Quarterly capex intake for Ashford Park; prioritize backlog."

**Inputs:** intake list + capex line-item library + labor/material references + priority rubric.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- lifecycle_stage: stabilized
- management_mode: third_party_managed
- role: asset_manager
- market: Charlotte
- output_type: memo
- decision_severity: action_requires_approval

## Expected packs loaded

- `workflows/capital_project_intake_and_prioritization/`
- `workflows/capex_estimate_generation/`
- `overlays/segments/middle_market/`

## Expected references

- `reference/normalized/capex_line_items__{scope}.csv`
- `reference/normalized/labor_rates__charlotte.csv`
- `reference/normalized/material_costs__southeast_residential.csv`
- `reference/normalized/capex_priority_rubric__{org}.yaml`
- `reference/normalized/approval_threshold_defaults.csv`

## Gates potentially triggered

- Life-safety deferral: row 4.
- Capex program change above threshold: rows 8-11.

## Expected output shape

- Prioritized backlog with scores, cost ranges, life-safety flags.
- Per-item estimates.
- Backlog memo with sequence.
- Approval request list.

## Confidence banner pattern

```
References: capex_line_items@2026-03-31 (starter), labor_rates__charlotte@2026-03-31 (sample),
material_costs__southeast_residential@2026-03-31 (sample), capex_priority_rubric@2026-03-31 (starter).
```
