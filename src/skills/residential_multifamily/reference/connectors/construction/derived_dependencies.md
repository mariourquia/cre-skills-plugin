# Construction Derived Dependencies

Which canonical metrics, workflows, and templates depend on normalized construction data.

## Required normalized inputs

- `construction.dev_budget`: project-level budget scenarios.
- `construction.commitment`: open and closed commitments.
- `construction.change_order`: CO pipeline.
- `construction.draw_request`: draw history.
- `construction.schedule_milestone`: schedule baseline and current forecasts.

## Optional enrichment inputs

- `construction.estimate_line_item`: early-phase estimates before commitments lock.
- `construction.bid_package`: bid history for trade-buyout variance.
- `construction.punch_item`: closeout tracking.

## Confidence minimum

- No open blocker failures on the required inputs.
- No open commitment overdraw (draws against pending COs flagged, not unresolved).
- Current_of_record pointer set for each active project's budget.
- Schedule milestone revision history present.

## Blocking data issues

- Commitment overdraw beyond approved COs.
- Budget coverage insufficient for committed plus approved COs.
- Contingency miscoding (owner vs contractor).
- Draws referencing pending COs unflagged.
- Schedule milestone marked complete without evidence.
- Lien waivers missing on subcontractor-paying draws.

## Fallback mode when partial

- Without dev_budget, cost-to-complete, contingency metrics, and budget-coverage metrics refuse.
- Without commitment, commitment-draw reconciliation refuses; draws cannot be validated.
- Without change_order, overdraw checks degrade to contract-total-only; COs assumed zero.
- Without draw_request, capex spend timeline is unavailable.
- Without schedule_milestone, schedule variance and critical-path metrics refuse.
- Without punch_item, project closeout certification is unavailable.

## Canonical metrics that depend on construction

### Development and Construction family

- `dev_cost_per_unit`, `dev_cost_per_gsf`, `dev_cost_per_nrsf`: require `dev_budget`.
- `contingency_remaining`: requires `dev_budget` (contingency classification) + `change_order`.
- `contingency_burn_rate`: requires `dev_budget` + `change_order` over time.
- `change_orders_pct_of_contract`: requires `commitment` + `change_order`.
- `cost_to_complete`: requires `commitment` + `change_order` + `draw_request` + `dev_budget`.
- `schedule_variance_days`: requires `schedule_milestone`.
- `milestone_slippage_rate`: requires `schedule_milestone` history.
- `trade_buyout_variance`: requires `estimate_line_item` + `commitment`.
- `draw_cycle_time`: requires `draw_request` timestamps.
- `punchlist_closeout_rate`: requires `punch_item`.

### Asset Management family

- `capex_spend_vs_plan`: depends on construction reconciling with gl.capex_actual.
- `renovation_yield_on_cost`: post-renovation rent (from PMS) over capex spend (from construction).

## Example output types

- Construction budget versus actual dashboard.
- Draw package review report (per draw cycle).
- Cost-to-complete forecast.
- Schedule critical-path status report.
- Trade buyout variance report.
- Punch list closeout tracker.
- Contingency burn-down dashboard.

## Dependent workflows

- `capital_project_intake_and_prioritization`
- `capex_estimate_generation`
- `bid_leveling_procurement_review`
- `change_order_review`
- `draw_package_review`
- `schedule_risk_review`
- `cost_to_complete_review`
- `construction_meeting_prep_and_action_tracking`
