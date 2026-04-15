# Routing Example 03 — Construction manager asks for a cost-to-complete on a renovation

**Inbound request:**

> "Cost-to-complete on the Greenbriar value-add. GC just flagged a trade buyout issue on flooring."

## Axis resolution

| Axis | Resolved to |
|---|---|
| `asset_class` | `residential_multifamily` |
| `segment` | `middle_market` |
| `form_factor` | `garden` |
| `lifecycle_stage` | `renovation` |
| `management_mode` | `self_managed` |
| `role` | `construction_manager` |
| `workflow` | `cost_to_complete_review` |
| `market` | `Phoenix` |
| `output_type` | `memo` + `estimate` |
| `decision_severity` | `recommendation` (may trigger `action_requires_approval` if CO threshold crossed) |

## Packs loaded

- `roles/construction_manager/`.
- `workflows/cost_to_complete_review/`.
- `workflows/change_order_review/` — invoked for the flooring issue.
- `workflows/bid_leveling_procurement_review/` — if rebid is warranted.
- `overlays/lifecycle/renovation/`.
- `overlays/segments/middle_market/` (for finish standards, ROI expectations).
- `overlays/form_factor/garden/` (for typical renovation scope).

## References loaded

- `reference/normalized/material_costs__west_residential.csv` (flooring line items, as-of date).
- `reference/normalized/labor_rates__phoenix_residential.csv`.
- `reference/normalized/unit_turn_cost_library__middle_market.csv` (classic-to-renovated scope).
- `reference/normalized/capex_line_items__middle_market_value_add.csv`.
- `reference/normalized/approval_threshold_defaults.csv` (change order thresholds).

## Gates

- If recommended change order crosses `threshold_co_minor` → approval matrix row 10.
- If it crosses `threshold_co_major` → approval matrix row 11 (adds executive).
- If rebid is recommended, approval matrix row 9 applies to the new award.

## Output shape

- Current cost-to-complete with reference citations and `as_of_date` per input.
- Trade-buyout variance (`trade_buyout_variance`) on flooring with root-cause narrative.
- Contingency burn-rate (`contingency_burn_rate`) vs. percent_complete.
- Options: absorb in contingency / change order / rebid scope. Each option shows dollar, schedule, and risk impact.
- Approval-request draft attached if any option exceeds threshold.
