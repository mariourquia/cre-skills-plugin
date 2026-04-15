# Metrics used by leasing_manager

All metrics are defined canonically in `_core/metrics.md`. This pack uses them; it does not
redefine them. Target bands are overlay-driven.

| Slug | Why this role cares | Cadence |
|---|---|---|
| `lead_response_time` | Top-of-funnel SLA, owned daily. | Daily, weekly |
| `tour_conversion` | Middle of funnel; leading indicator of tour quality. | Weekly |
| `application_conversion` | Screening flow health from the leasing side. | Weekly |
| `approval_rate` | Fair-housing and policy-drift watchpoint. | Weekly |
| `move_in_conversion` | Bottom of funnel; lost-approvals hunt. | Weekly |
| `leased_occupancy` | Primary outcome the role drives. | Weekly |
| `preleased_occupancy` | Future lease-up the role owns. | Weekly |
| `notice_exposure` | Near-term vacancy; drives pricing and marketing intensity. | Weekly |
| `concession_rate` | Pricing discipline; monthly pattern check vs. overlay. | Monthly |
| `rent_growth_new_lease` | Market capture on rollovers. | Monthly |
| `renewal_offer_rate` | Process discipline; 100% target. | Weekly |
| `renewal_acceptance_rate` | Retention outcome. | Monthly |
| `rent_growth_renewal` | Pricing discipline on retained residents. | Monthly |
| `blended_lease_trade_out` | Headline rent growth owned jointly with PM. | Monthly |
| `market_to_lease_gap` | Pricing opportunity on available inventory. | Weekly |
