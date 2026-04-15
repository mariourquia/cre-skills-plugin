# Example — Weekly OAC Agenda & Schedule / RFI Memo (abridged)

**Prompt:** "Prepare this week's OAC agenda for Harbor Point. Include 2-week look-ahead, open RFI and submittal list, and trade-coordination issues."

**Inputs:** current construction schedule + baseline; RFI log; submittal log; change-order log; field photos; safety log.

**Output shape:** see `templates/weekly_oac_agenda_and_minutes.md` + `templates/weekly_schedule_rfi_memo.md`.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: suburban_mid_rise
- lifecycle_stage: construction
- role: construction_manager
- output_type: checklist + operating_review
- decision_severity: recommendation

## Expected packs loaded

- `roles/construction_manager/`
- `workflows/weekly_oac_meeting/`
- `workflows/rfi_submittal_queue_review/`
- `workflows/long_lead_procurement_tracker/`
- `overlays/segments/middle_market/`
- `overlays/lifecycle/construction/`

## Expected references

- `reference/normalized/material_costs__{region}_residential.csv`
- `reference/normalized/labor_rates__{market}_residential.csv`
- `reference/normalized/productivity_norms__{region}_residential.csv`
- `reference/normalized/contingency_policy__middle_market.csv`

## Gates potentially triggered

- Any safety incident routes row 4.
- Any code-compliance judgment routes row 5.
- Any RFI decision shifting scope materially routes via development_manager to asset_manager.

## Confidence banner pattern

```
References: material_costs@{as_of_date, region}, labor_rates@{as_of_date, market},
productivity_norms@{as_of_date} (statuses per record). Schedule current as of {tracker_date};
RFI and submittal logs live.
```
