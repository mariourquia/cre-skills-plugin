# Example — Move-Out Administration (abridged)

**Prompt:** "Process move-out for unit 101 at Ashford Park, vacate 2026-04-30."

**Inputs:** lease record + NoticeEvent + resident ledger + inspection record + `reference/normalized/move_out_documents__charlotte.yaml` + `reference/normalized/damage_charge_schedule__{org}.csv`.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- lifecycle_stage: stabilized
- management_mode: third_party_managed
- role: property_manager
- market: Charlotte
- jurisdiction: Charlotte
- output_type: checklist
- decision_severity: action_requires_approval

## Expected packs loaded

- `workflows/move_out_administration/`
- `workflows/unit_turn_make_ready/` (handoff)
- `overlays/segments/middle_market/`
- `overlays/management_mode/third_party_managed/`

## Expected references

- `reference/normalized/move_out_documents__charlotte.yaml`
- `reference/normalized/damage_charge_schedule__{org}.csv`
- `reference/normalized/unit_turn_cost_library__charlotte.csv`
- `reference/normalized/approval_threshold_defaults.csv`

## Gates potentially triggered

- Damage charge waiver above threshold: `approval_request` row 13.
- Fair-housing disparity signal: `approval_request` row 3.

## Expected output shape

- Move-out checklist with owners and statutory deadlines.
- Inspection brief with damages list referencing the schedule.
- Final ledger draft.
- Security-deposit statement with `legal_review_required` banner.
- Turn handoff record triggering `workflows/unit_turn_make_ready`.

## Confidence banner pattern

```
References: move_out_documents__charlotte@2026-03-31 (sample),
damage_charge_schedule@2026-03-31 (starter),
unit_turn_cost_library__charlotte@2026-03-31 (sample).
Data freshness: ledger snapshot and NoticeEvent live.
```
