# Metrics used by development_manager

All metrics are defined canonically in `_core/metrics.md`. This pack uses them; it does not
redefine them. Target bands are reference- and overlay-driven.

| Slug | Why this role cares | Cadence |
|---|---|---|
| `dev_cost_per_unit` | Budget health (estimate/bid/actual). | As-of |
| `dev_cost_per_gsf` | Cost efficiency by GSF. | As-of |
| `dev_cost_per_nrsf` | Cost efficiency by NRSF. | As-of |
| `contingency_remaining` | Risk cushion at as-of. | As-of |
| `contingency_burn_rate` | Burn vs. progress; early-warning signal. | As-of |
| `change_orders_pct_of_contract` | Scope discipline vs. GC contract. | As-of |
| `cost_to_complete` | Forward-looking budget view. | Monthly |
| `schedule_variance_days` | Schedule discipline vs. baseline. | Weekly |
| `milestone_slippage_rate` | Portfolio of milestones status. | As-of |
| `trade_buyout_variance` | Buyout discipline vs. estimate. | Event-stamped |
| `draw_cycle_time` | Lender-process efficiency. | T90 |
| `punchlist_closeout_rate` | Closeout discipline post-TCO. | As-of |
| `lease_up_pace_post_delivery` | Post-TCO leasing execution. | Weekly |
| `stabilization_pace_vs_plan` | Pace to stabilization vs. plan. | Weekly |
