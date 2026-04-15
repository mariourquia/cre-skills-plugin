# Example 03 — ROUTING

## Matched rules

- `r005_construction_manager` (primary).
- `r009_direct_workflow` — workflows `cost_to_complete_review` + `change_order_review` (nested) + `draw_package_review` (because a draw is next week).

## Axis resolution

| Axis | Resolved to | Source |
|---|---|---|
| `asset_class` | `residential_multifamily` | default |
| `segment` | `middle_market` | project master |
| `form_factor` | `garden` | project master |
| `lifecycle_stage` | `renovation` | project master |
| `management_mode` | `self_managed` | project master |
| `role` | `construction_manager` | session context |
| `workflow` | `cost_to_complete_review` | inferred from "CTC" |
| `market` | `Phoenix` | project master |
| `submarket` | `North Tempe` | project master |
| `output_type` | `memo` + `estimate` | request text |
| `decision_severity` | `recommendation` (promotes to `action_requires_approval` if option crosses major CO threshold) | request |
| `org_id` | `examples_org` | session |

## Packs loaded

- Role pack: `roles/construction_manager/`.
- Workflow packs: `workflows/cost_to_complete_review/`, `workflows/change_order_review/`, `workflows/draw_package_review/`, `workflows/bid_leveling_procurement_review/` (evaluated if rebid is chosen).
- Segment overlay: `overlays/segments/middle_market/` (value-add finish package active).
- Form-factor overlay: `overlays/form_factor/garden/`.
- Lifecycle overlay: `overlays/lifecycle/renovation/`.
- Management-mode overlay: `overlays/management_mode/self_managed/`.
- Org overlay: `overlays/org/examples_org/`.

## References loaded

| Path | Category | as-of | Status | Fallback |
|---|---|---|---|---|
| `reference/normalized/material_costs__west_residential.csv` | material_cost | 2026-03-31 | sample | use_prior_period |
| `reference/normalized/labor_rates__phoenix_residential.csv` | labor_rate | 2026-03-31 | sample | use_prior_period |
| `reference/normalized/unit_turn_cost_library__middle_market.csv` | unit_turn_cost | 2026-02-01 | starter | refuse |
| `reference/normalized/capex_line_items__middle_market_value_add.csv` | capex_line_item | 2026-02-01 | starter | refuse |
| `reference/normalized/approval_threshold_defaults.csv` | approval_threshold_policy | 2026-03-15 | starter | refuse |

## Metrics engaged

- `cost_to_complete`
- `trade_buyout_variance`
- `change_orders_pct_of_contract`
- `contingency_remaining`
- `contingency_burn_rate`
- `schedule_variance_days`
- `dev_cost_per_unit` (contextual)
- `draw_cycle_time` (contextual — draw is next week)

## Gates surfaced

- Row 10 `change_order_minor` — triggers if the option crosses the minor tier (per approval matrix + org overlay).
- Row 11 `change_order_major` — triggers if option crosses major tier.
- Row 9 `award_or_rebid_contract` — if rebid is recommended.
- Row 7 `disbursement_tier_2` — draw package approval path.

## Templates selected

- `templates/capex/change_order_review_sheet.md` (for the flooring CO write-up).
- `templates/capex/change_order_log.md` (running ledger).
- `templates/construction/construction_meeting_agenda_and_action_log.md` (for the weekly OAC meeting that will absorb the decision).
- `templates/construction/draw_package_summary.md` (for next week's draw).
- `templates/capex/vendor_bid_leveling_template.md` (loaded in case rebid is selected).

## Output shape

- Current CTC with reference citations + as_of per input.
- Flooring-trade variance with root-cause and reference comparison.
- Contingency ledger read (contingency_remaining + burn rate vs. % complete).
- Options with cost / schedule / risk and explicit approval gate per option.
- Draft CO review sheet attached for Option 2 path.
- Draw package callout (does this month's draw absorb any of the CO ask?).
- Confidence banner surfacing sample/starter reference status.
