# Example 03 — INPUT

## User prompt

> "Cost-to-complete on the Greenbriar value-add. GC just flagged a trade-buyout issue on flooring — came in hotter than our estimate. Give me the CTC, the variance on flooring, and options with approval paths. I have a draw next week."

## Session context

- asker.role: `construction_manager`
- asker.org_id: `examples_org`
- project lookup: `project_id = greenbriar_value_add_01`
- property master: `property_name=Greenbriar`, `segment=middle_market`, `form_factor=garden`, `lifecycle_stage=renovation`, `management_mode=self_managed`, `market=Phoenix`, `submarket=North Tempe`, `unit_count_rentable=180`.
- Project baseline: contract value at NTP $3,180,000; original contingency $318,000 (10%); target substantial completion 2026-08-15.
- Current state (as of 2026-04-12): percent complete cost-loaded 38%; percent complete physical 40%; contingency remaining $221,600 (69.7% of original); approved COs YTD $64,200; pending CO backlog $92,500.
- Flooring issue: GC buyout came in $108,000 over estimate on the flooring trade (LVP + stair treads).
- Finish scope is value-add package (quartz-look counters, upgraded flooring, stainless appliances).

## Reference availability snapshot

- `reference/normalized/material_costs__west_residential.csv` — present, status: sample, as_of 2026-03-31.
- `reference/normalized/labor_rates__phoenix_residential.csv` — present, status: sample, as_of 2026-03-31.
- `reference/normalized/unit_turn_cost_library__middle_market.csv` — present, status: starter, as_of 2026-02-01.
- `reference/normalized/capex_line_items__middle_market_value_add.csv` — present, status: starter, as_of 2026-02-01.
- `reference/normalized/approval_threshold_defaults.csv` — present, status: starter.

## Decision / autonomy context

- decision_severity expected: `recommendation` (may escalate to `action_requires_approval` if an option crosses major CO threshold).
- Gated actions likely: row 10 `change_order_minor`, row 11 `change_order_major` (depending on option), row 9 `award_or_rebid` if rebid is chosen.
