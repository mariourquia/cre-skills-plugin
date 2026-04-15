# Metrics used by maintenance_supervisor

All metrics are defined canonically in `_core/metrics.md`. This pack uses them; it does not
redefine them. Target bands are overlay-driven.

| Slug | Why this role cares | Cadence |
|---|---|---|
| `open_work_orders` | Active load; managed daily. | Daily, weekly |
| `work_order_aging` | SLA discipline; P1 is zero-tolerance. | Daily (P1), weekly |
| `repeat_work_order_rate` | Quality and vendor signal; feeds vendor scorecard. | Monthly |
| `make_ready_days` | Turn efficiency; the supervisor's headline outcome. | Weekly |
| `average_days_vacant` | Revenue-days lost per turn; co-owned with leasing. | Weekly |
| `turnover_rate` | Operating stability; influences turn volume. | Monthly, T12 |
| `rm_per_unit` | R&M discipline; the expense dial. | Monthly, T12 |
| `utilities_per_unit` | Utilities net of RUBS; maintenance actions can move this. | Monthly, T12 |
| `controllable_opex_per_unit` | Portion owned via R&M. | Monthly, T12 |
