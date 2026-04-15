# Metrics used by property_manager

All metrics are defined canonically in `_core/metrics.md`. This pack uses them; it does not
redefine them. Target bands are overlay-driven (segment / org overlays).

| Slug | Why this role cares | Cadence |
|---|---|---|
| `physical_occupancy` | Primary operating signal. | Weekly, monthly |
| `leased_occupancy` | Forward-looking; drives pricing. | Weekly |
| `economic_occupancy` | Captures combined vacancy / concession / delinquency drag. | Monthly |
| `notice_exposure` | Near-term vacancy risk. | Weekly |
| `preleased_occupancy` | Upcoming move-ins. | Weekly |
| `lead_response_time` | Funnel top. | Daily, weekly |
| `tour_conversion` | Funnel middle. | Weekly |
| `application_conversion` | Screening health. | Weekly |
| `approval_rate` | Screening discipline; fair-housing watchpoint. | Weekly |
| `move_in_conversion` | Funnel bottom. | Weekly |
| `renewal_offer_rate` | Process discipline — target 100%. | Weekly |
| `renewal_acceptance_rate` | Retention. | Monthly |
| `turnover_rate` | Operating stability. | Monthly, T12 |
| `average_days_vacant` | Revenue-days lost per turn. | Weekly |
| `make_ready_days` | Turn efficiency. | Weekly |
| `open_work_orders` | Maintenance load. | Daily, weekly |
| `work_order_aging` | SLA discipline — P1 zero-tolerance. | Daily (P1), weekly |
| `repeat_work_order_rate` | Quality and vendor signal. | Monthly |
| `delinquency_rate_30plus` | Financial risk. | Weekly |
| `collections_rate` | Revenue capture. | Weekly, monthly |
| `bad_debt_rate` | Write-off discipline. | T12, monthly |
| `concession_rate` | Pricing discipline; policy adherence. | Monthly |
| `rent_growth_new_lease` | Market capture on rollovers. | Monthly |
| `rent_growth_renewal` | Retention pricing discipline. | Monthly |
| `blended_lease_trade_out` | Headline rent growth. | Monthly |
| `market_to_lease_gap` | Pricing opportunity / risk. | As-of |
| `loss_to_lease` | Revenue upside at full rollover. | As-of |
| `payroll_per_unit` | Site labor efficiency. | Monthly, T12 |
| `rm_per_unit` | Repairs discipline. | Monthly, T12 |
| `utilities_per_unit` | Utilities net of RUBS. | Monthly, T12 |
| `controllable_opex_per_unit` | The opex dial the PM owns. | Monthly, T12 |
