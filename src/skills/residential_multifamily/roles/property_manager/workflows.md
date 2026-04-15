# Workflows invoked by property_manager

| Workflow | Cadence | Trigger |
|---|---|---|
| `workflows/lead_to_lease_funnel_review` | weekly | weekly site review |
| `workflows/renewal_retention` | monthly + per expiring lease | lease.end_date within renewal_offer_lead_time |
| `workflows/delinquency_collections` | weekly + per bucket move | aging transition event |
| `workflows/move_in_administration` | per move-in | move_in_event |
| `workflows/move_out_administration` | per move-out | move_out_event |
| `workflows/work_order_triage` | daily | new work order, P1 event |
| `workflows/unit_turn_make_ready` | per move-out; weekly portfolio view | turn started |
| `workflows/vendor_dispatch_sla_review` | weekly | vendor SLA breach, repeat WO pattern |
| `workflows/market_rent_refresh` | quarterly | quarter-end or funnel signal |
| `workflows/rent_comp_intake` | as comps arrive | new comp delivered |
| `workflows/capital_project_intake_and_prioritization` | quarterly | quarter-end or life-safety flag |
| `workflows/monthly_property_operating_review` | monthly | month-end close |
| `workflows/budget_build` | annual | budget cycle |
| `workflows/reforecast` | quarterly | reforecast cycle |
