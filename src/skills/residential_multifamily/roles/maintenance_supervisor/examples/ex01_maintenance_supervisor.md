# Example — Weekly Maintenance Backlog Review (abridged)

**Prompt:** "Run this week's maintenance backlog review at Ashford Park. Flag P1/P2 aging and turn blockers."

**Inputs:** WO system export; turn pipeline state; vendor dispatch log; preventive-maintenance calendar.

**Output shape:** see `templates/weekly_maintenance_backlog_review.md`.

## Expected axis resolution

- asset_class: residential_multifamily
- segment: middle_market
- form_factor: garden
- lifecycle_stage: stabilized
- management_mode: third_party_managed
- role: maintenance_supervisor
- output_type: operating_review
- decision_severity: recommendation

## Expected packs loaded

- `roles/maintenance_supervisor/`
- `workflows/work_order_triage/`
- `workflows/unit_turn_make_ready/`
- `workflows/vendor_dispatch_sla_review/`
- `overlays/segments/middle_market/`
- `overlays/form_factor/garden/`
- `overlays/lifecycle/stabilized/`

## Expected references

- `reference/normalized/preventive_maintenance_intervals__middle_market.csv`
- `reference/normalized/turn_cost_library__middle_market.csv`
- `reference/normalized/vendor_rate_card__{market}_mf.csv`
- `reference/derived/role_kpi_targets.csv`

## Gates potentially triggered

- Any life-safety scope change, deferral, or evacuation routes to approval_request (row 4).
- Any licensed-engineering judgment routes per row 5.
- Any vendor dispatch above threshold routes per rows 6, 8.

## Confidence banner pattern

```
References: preventive_maintenance_intervals@{as_of_date} (status: starter, overlay pending);
turn_cost_library@{as_of_date}; vendor_rate_card@{as_of_date, market}. WO data live. Turn
pipeline state live.
```
