# Metrics used by estimator_preconstruction_lead

All metrics are defined canonically in `_core/metrics.md`. This pack uses them; it does not
redefine them. Target bands are reference- and overlay-driven.

| Slug | Why this role cares | Cadence |
|---|---|---|
| `dev_cost_per_unit` | Primary estimate output at unit grain. | As-of |
| `dev_cost_per_gsf` | Estimate output at GSF grain. | As-of |
| `dev_cost_per_nrsf` | Estimate output at NRSF grain. | As-of |
| `contingency_remaining` | Estimate-to-actual calibration signal. | As-of |
| `change_orders_pct_of_contract` | Backward-looking signal for library calibration. | As-of |
| `trade_buyout_variance` | Bid-leveling outcome. | Event-stamped |
| `cost_to_complete` | Supplied as ETC input to construction/dev teams. | Monthly |
