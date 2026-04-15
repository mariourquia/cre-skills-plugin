# Example — Construction Meeting Prep and Action Tracking (abridged)

**Prompt:** "Build the OAC pack for Willow Creek this Wednesday."

**Inputs:** prior action items + schedule state + RFI/submittal log + CO log + safety log + CTC summary.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: suburban_mid_rise
- market: Charlotte
- project_id: willow_creek_construction
- role: construction_manager
- output_type: checklist
- decision_severity: recommendation

## Expected packs loaded

- `workflows/construction_meeting_prep_and_action_tracking/`
- `workflows/schedule_risk_review/` (feeder)
- `workflows/cost_to_complete_review/` (feeder)
- `workflows/change_order_review/` (feeder)
- `overlays/segments/middle_market/`
- `overlays/lifecycle/construction/`

## Expected references

- `reference/normalized/approval_threshold_defaults.csv`

## Gates potentially triggered

- None at the meeting-prep step. Any decision captured in minutes that triggers an approval routes through the relevant workflow.

## Expected output shape

- Agenda with topics and owners.
- Data pack (KPIs, schedule, budget, RFI/CO/safety logs).
- Action-item ledger update with aging.
- Reminder drafts for stale items.

## Confidence banner pattern

```
References: approval_threshold_defaults@2026-03-31 (starter).
```
