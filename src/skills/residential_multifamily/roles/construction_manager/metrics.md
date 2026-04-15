# Metrics used by construction_manager

All metrics are defined canonically in `_core/metrics.md`. This pack uses them; it does not
redefine them. Target bands are reference- and overlay-driven.

| Slug | Why this role cares | Cadence |
|---|---|---|
| `contingency_remaining` | Risk cushion; watched with development_manager. | As-of |
| `contingency_burn_rate` | Early warning on overrun. | As-of |
| `change_orders_pct_of_contract` | Scope discipline. | As-of |
| `cost_to_complete` | Forward budget view. | Monthly |
| `schedule_variance_days` | Primary schedule KPI against baseline CP. | Weekly |
| `milestone_slippage_rate` | Milestone discipline. | As-of |
| `trade_buyout_variance` | Buyout discipline vs. estimate. | Event-stamped |
| `draw_cycle_time` | Field-side efficiency of draw cycle. | T90 |
| `punchlist_closeout_rate` | Closeout discipline. | Post-TCO |
