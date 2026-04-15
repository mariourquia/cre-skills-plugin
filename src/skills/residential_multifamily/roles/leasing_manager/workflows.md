# Workflows invoked by leasing_manager

| Workflow | Cadence | Trigger |
|---|---|---|
| `workflows/lead_to_lease_funnel_review` | Weekly (owner) | weekly cycle |
| `workflows/renewal_retention` | Monthly + per-lease | lease enters renewal window |
| `workflows/market_rent_refresh` | Quarterly | quarter-end or funnel signal |
| `workflows/rent_comp_intake` | As comps arrive | new comp delivered |
| `workflows/pricing_concession_proposal` | Weekly | new availability or demand shift |
| `workflows/marketing_channel_mix_review` | Monthly | channel cost drift |
| `workflows/tour_script_fair_housing_refresh` | Quarterly | quarter-end |
