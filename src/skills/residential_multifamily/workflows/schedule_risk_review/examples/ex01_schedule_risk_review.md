# Example — Schedule Risk Review (abridged)

**Prompt:** "Run schedule risk review for Willow Creek."

**Inputs:** current schedule + baseline + milestone record + critical-path disruption log + overlay duration assumptions.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: suburban_mid_rise
- market: Charlotte
- project_id: willow_creek_construction
- role: construction_manager
- output_type: memo
- decision_severity: action_requires_approval

## Expected packs loaded

- `workflows/schedule_risk_review/`
- `workflows/cost_to_complete_review/` (invoked for cost consequence)
- `overlays/segments/middle_market/`
- `overlays/lifecycle/construction/`

## Expected references

- `reference/normalized/construction_duration_assumptions__southeast.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Gates potentially triggered

- Rebaseline proposal approval per overlay.
- Executive escalation if slip above threshold.

## Expected output shape

- Schedule delta view with variance metrics.
- Critical-path memo with cause and consequence.
- Rebaseline proposal (if warranted).
- Lease-up delivery scenario view (if applicable).

## Confidence banner pattern

```
References: construction_duration_assumptions__southeast@2026-03-31 (starter).
```
